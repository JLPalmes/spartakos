# SPDX-License-Identifier: AGPL-3.0-or-later
"""Inventario público experimental: autoridad KERI y restauración transaccional."""
import argparse
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError
import json
import os
from pathlib import Path
import re
import select
import signal
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from keri import core
from keri.core import eventing, serdering
from keri.db import basing, dbing
from keri_profile_http import fetch, MARKER

ANCHOR = 'spartakos_public_inventory_lab_v1'
KIND = 'spartakos-public-inventory-lab-v1'


class InventoryTransitionError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def digest(raw):
    return core.Diger(ser=raw).qb64


def serve(root):
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path in ('/manifest', '/proof'):
                target = root / (self.path[1:] + '.json')
            elif re.fullmatch(r'/objects/[A-Za-z0-9_-]{44}', self.path):
                target = root / 'objects' / self.path.rsplit('/', 1)[1]
            else:
                self.send_error(404)
                return
            if not target.is_file():
                self.send_error(404)
                return
            body = target.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass
    with HTTPServer(('127.0.0.1', 0), Handler) as server:
        print(json.dumps({'port': server.server_port}), flush=True)
        server.serve_forever()


class InventoryProvider:
    def __init__(self, root):
        self.root, self.process = root, None

    def start(self):
        self.process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--serve', str(self.root)],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not select.select([self.process.stdout], [], [], 10)[0]:
            self.stop()
            raise RuntimeError('No arrancó el proveedor.')
        metadata = json.loads(self.process.stdout.readline())
        self.url = f"http://127.0.0.1:{metadata['port']}"

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.communicate(timeout=5)
            self.process = None


def latest_inventory(db, owner):
    found = []
    for dig in db.getKelIter(owner):
        event = serdering.SerderKERI(raw=bytes(db.getEvt(dbing.dgKey(owner, bytes(dig)))))
        if bytes(db.getKeLast(dbing.snKey(owner, event.sn))).decode() != event.said:
            continue
        for value in event.ked.get('a', []):
            if isinstance(value, dict) and ANCHOR in value:
                found.append((event.sn, value[ANCHOR]['d']))
    if not found:
        raise ValueError('Inventario sin autoridad validada.')
    return max(found)


def restore(root, url, owner, interrupt_before_apply=False, before_apply=None):
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    db = basing.Baser(name='inventory-observer', headDirPath=str(root), temp=False, reopen=True)
    catalog = sqlite3.connect(root / 'catalog.sqlite3')
    try:
        if not Path(db.path).resolve().is_relative_to(root.resolve()):
            raise RuntimeError('Almacén fuera del ensayo.')
        catalog.executescript('CREATE TABLE IF NOT EXISTS objects (id TEXT, revision INTEGER, state TEXT, body BLOB, PRIMARY KEY(id,revision)); CREATE TABLE IF NOT EXISTS heads (id TEXT PRIMARY KEY, revision INTEGER);')
        catalog.execute('CREATE TABLE IF NOT EXISTS receipts (identity TEXT PRIMARY KEY, expected_sequence INTEGER, expected_digest TEXT, applied_sequence INTEGER NOT NULL DEFAULT 0, state TEXT, details TEXT)')
        catalog.commit()
        kvy = eventing.Kevery(db=db, local=False)
        proof = json.loads(fetch(url + '/proof'))
        for item in proof:
            event = serdering.SerderKERI(raw=item['event'].encode())
            if event.pre != owner:
                raise ValueError('Identidad de inventario inesperada.')
            kvy.processEvent(serder=event, sigers=[core.Siger(qb64=item['signature'])])
        raw = fetch(url + '/manifest')
        manifest = json.loads(raw)
        if manifest.get('kind') != KIND or manifest.get('owner') != owner:
            raise ValueError('Formato de inventario inesperado.')
        sequence, authorized_digest = latest_inventory(db, owner)
        if digest(raw) != authorized_digest:
            raise ValueError('Inventario sin autorización vigente en esta vista.')
        with catalog:
            catalog.execute("INSERT INTO receipts(identity,expected_sequence,expected_digest,state,details) VALUES (?,?,?,'receiving','{}') ON CONFLICT(identity) DO UPDATE SET expected_sequence=excluded.expected_sequence,expected_digest=excluded.expected_digest,state='receiving',details='{}'",
                            (owner, sequence, authorized_digest))
        entries = manifest['entries']
        if not isinstance(entries, list) or not 0 < len(entries) <= 1000:
            raise ValueError('Inventario fuera del alcance del ensayo.')
        staged, seen, heads, missing, invalid = [], set(), {}, [], []
        for entry in entries:
            identifier, revision, state = entry['id'], entry['revision'], entry['state']
            if not identifier.startswith(owner + ':') or type(revision) is not int or revision < 1 or (identifier, revision) in seen:
                raise ValueError('Identificador, revisión o duplicado inválido.')
            seen.add((identifier, revision))
            heads[identifier] = max(revision, heads.get(identifier, 0))
            if state == 'withdrawn':
                if entry.get('digest') is not None:
                    raise ValueError('Una retirada no debe incluir cuerpo.')
                body = None
            elif state == 'active':
                expected = entry['digest']
                if not re.fullmatch(r'[A-Za-z0-9_-]{44}', expected):
                    raise ValueError('Huella fuera de formato.')
                try:
                    body = fetch(url + '/objects/' + expected)
                except HTTPError as error:
                    # Solo una ausencia HTTP 404 significa objeto faltante.
                    if error.code != 404:
                        raise
                    error.close()
                    missing.append(identifier)
                    continue
                if digest(body) != expected:
                    invalid.append(identifier)
                    continue
                obj = json.loads(body)
                if obj.get('id') != identifier or obj.get('revision') != revision or obj.get('audience') != 'public':
                    invalid.append(identifier)
                    continue
            else:
                raise ValueError('Estado no admitido.')
            staged.append((identifier, revision, state, body))
        if missing or invalid:
            result = {'complete': False, 'missing': sorted(missing), 'invalid': sorted(invalid)}
            with catalog:
                catalog.execute("UPDATE receipts SET state='incomplete',details=? WHERE identity=?", (json.dumps(result), owner))
            return result
        previous_ids = {row[0] for row in catalog.execute('SELECT id FROM heads')}
        if not previous_ids.issubset(heads):
            raise InventoryTransitionError('missing_previous_object', 'Falta un objeto previo sin marcador explícito.')
        for identifier, revision in heads.items():
            previous = catalog.execute('SELECT revision FROM heads WHERE id=?', (identifier,)).fetchone()
            if previous and revision < previous[0]:
                raise InventoryTransitionError('revision_rollback', 'El inventario retrocede una revisión conocida.')
        for identifier, revision, state, body in staged:
            previous = catalog.execute('SELECT state,body FROM objects WHERE id=? AND revision=?', (identifier, revision)).fetchone()
            if previous and previous[1] is not None and state == 'active' and bytes(previous[1]) != body:
                raise InventoryTransitionError('revision_content_rewrite', 'Una revisión conocida no puede cambiar de contenido.')
            if previous and previous[0] in ('withdrawn', 'redacted') and state == 'active':
                raise InventoryTransitionError('retired_revision_reactivation', 'No se restaura el cuerpo de una revisión retirada.')
        if before_apply is not None:
            before_apply()
        if interrupt_before_apply:
            print(json.dumps({'interrupted_before_apply': True}), flush=True)
            os._exit(19)  # Instrumentación de prueba: tras recepción persistida, antes de aplicar catálogo.
        with catalog:
            for identifier, revision, state, body in staged:
                catalog.execute('INSERT OR REPLACE INTO objects VALUES (?,?,?,?)', (identifier, revision, state, body))
            for identifier, revision in heads.items():
                catalog.execute('INSERT OR REPLACE INTO heads VALUES (?,?)', (identifier, revision))
                current = catalog.execute('SELECT state FROM objects WHERE id=? AND revision=?', (identifier, revision)).fetchone()[0]
                if current == 'withdrawn':
                    catalog.execute("UPDATE objects SET state='redacted',body=NULL WHERE id=? AND revision<?", (identifier, revision))
            catalog.execute("UPDATE receipts SET state='complete',applied_sequence=?,details='{}' WHERE identity=?", (sequence, owner))
        return {'complete': True, 'sequence': sequence, 'objects': len(staged), 'globally_current': None}
    except InventoryTransitionError as error:
        catalog.rollback()
        with catalog:
            catalog.execute("UPDATE receipts SET state='rejected',details=? WHERE identity=?",
                            (json.dumps({'error_code': error.code}), owner))
        raise
    finally:
        catalog.close()
        db.close()


class PublicInventory(unittest.TestCase):
    def scenario(self, mode):
        with tempfile.TemporaryDirectory(prefix='spartakos-public-inventory-') as path:
            root = Path(path)
            directories = {name: root / name for name in ('a', 'b', 'observer')}
            for directory in directories.values():
                directory.mkdir(mode=0o700)
                (directory / MARKER).write_text('spartakos\n')
            for name in ('a', 'b'):
                (directories[name] / 'objects').mkdir(mode=0o700)
            owner, later = core.Signer(), core.Signer()
            inception = eventing.incept(keys=[owner.verfer.qb64], ndigs=[core.Diger(ser=later.verfer.qb64b).qb64])
            ids = [inception.pre + ':' + name for name in ('profile', 'post-1', 'post-2', 'post-3')]
            def obj(identifier, revision, text):
                return encoded({'id': identifier, 'revision': revision, 'audience': 'public', 'text': text})
            original = [obj(identifier, 1, text) for identifier, text in zip(ids, ('Perfil ficticio', 'Texto uno', 'Texto dos', 'Texto retirado'))]
            updated = obj(ids[1], 2, 'Texto uno editado')
            def entry(raw):
                value = json.loads(raw)
                return {'id': value['id'], 'revision': value['revision'], 'state': 'active', 'digest': digest(raw)}
            initial_entries = [entry(raw) for raw in original]
            new_entries = [entry(raw) for raw in original[:3]] + [entry(updated),
                {'id': ids[3], 'revision': 2, 'state': 'withdrawn', 'digest': None}]
            rewritten = obj(ids[1], 1, 'Cambio sin nueva revisión')
            if mode == 'revision-reuse':
                new_entries[1] = entry(rewritten)
            elif mode == 'omit-existing':
                new_entries = [item for item in new_entries if item['id'] != ids[2]]
            manifests = [encoded({'kind': KIND, 'owner': inception.pre, 'entries': entries})
                         for entries in (initial_entries, new_entries)]
            first = eventing.interact(pre=inception.pre, dig=inception.said, sn=1, data=[{ANCHOR: {'d': digest(manifests[0])}}])
            second = eventing.interact(pre=inception.pre, dig=first.said, sn=2, data=[{ANCHOR: {'d': digest(manifests[1])}}])
            for name, manifest, history in (('a', manifests[0], [inception, first]), ('b', manifests[1], [inception, first, second])):
                directory = directories[name]
                (directory / 'manifest.json').write_bytes(manifest)
                (directory / 'proof.json').write_text(json.dumps([{'event': event.raw.decode(), 'signature': owner.sign(event.raw, index=0).qb64} for event in history]))
                for raw in (original if name == 'a' else [*original[:3], updated, rewritten]):
                    (directory / 'objects' / digest(raw)).write_bytes(raw)
            a, b = InventoryProvider(directories['a']), InventoryProvider(directories['b'])
            reference = {'target': ids[1], 'revision': 1}
            reference_bytes = encoded(reference)
            (directories['observer'] / 'saved-reference.json').write_bytes(reference_bytes)
            def receive(provider, rejected=False, interrupt=False, expected_error=None):
                args = [sys.executable, str(Path(__file__).resolve()), '--restore', str(directories['observer']),
                        '--url', provider.url, '--owner', inception.pre]
                if interrupt:
                    args.append('--interrupt-before-apply')
                result = subprocess.run(args, capture_output=True, text=True, timeout=20)
                if interrupt:
                    self.assertEqual(result.returncode, 19, result.stderr[-1500:])
                    self.assertEqual(json.loads(result.stdout), {'interrupted_before_apply': True})
                    return None
                if rejected:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(expected_error or 'ValueError: Inventario sin autorización vigente en esta vista.', result.stderr)
                    return None
                self.assertEqual(result.returncode, 0, result.stderr[-1500:])
                return json.loads(result.stdout)
            try:
                a.start()
                b.start()
                self.assertTrue(receive(a)['complete'])
                a.stop()
                import urllib.error
                with self.assertRaises(urllib.error.URLError):
                    fetch(a.url + '/manifest')
                target = directories['b'] / 'objects' / digest(original[2])
                if mode == 'missing':
                    target.unlink()
                elif mode == 'altered':
                    target.write_bytes(b'{"changed":true}')
                elif mode == 'unauthorized':
                    bad = json.loads(manifests[1]); bad['entries'].pop()
                    (directories['b'] / 'manifest.json').write_bytes(encoded(bad))
                    receive(b, rejected=True)
                    with closing(sqlite3.connect(directories['observer'] / 'catalog.sqlite3')) as catalog:
                        self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 4)
                    return
                if mode == 'interrupted':
                    receive(b, interrupt=True)
                    with closing(sqlite3.connect(directories['observer'] / 'catalog.sqlite3')) as catalog:
                        self.assertEqual(catalog.execute('SELECT expected_sequence,applied_sequence,state FROM receipts WHERE identity=?', (inception.pre,)).fetchone(), (2, 1, 'receiving'))
                        self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 4)
                if mode in ('revision-reuse', 'omit-existing'):
                    expected_error = 'InventoryTransitionError: Una revisión conocida no puede cambiar de contenido.' if mode == 'revision-reuse' else 'InventoryTransitionError: Falta un objeto previo sin marcador explícito.'
                    receive(b, rejected=True, expected_error=expected_error)
                    with closing(sqlite3.connect(directories['observer'] / 'catalog.sqlite3')) as catalog:
                        self.assertEqual(catalog.execute('SELECT body FROM objects WHERE id=? AND revision=1', (ids[1],)).fetchone()[0], original[1])
                        self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 4)
                        receipt = catalog.execute('SELECT expected_sequence,applied_sequence,state,details FROM receipts WHERE identity=?', (inception.pre,)).fetchone()
                        self.assertEqual(receipt[:3], (2, 1, 'rejected'))
                        self.assertEqual(json.loads(receipt[3]), {'error_code': 'revision_content_rewrite' if mode == 'revision-reuse' else 'missing_previous_object'})
                    return
                result = receive(b)
                if mode in ('missing', 'altered'):
                    self.assertFalse(result['complete'])
                    self.assertEqual(result['missing' if mode == 'missing' else 'invalid'], [ids[2]])
                    with closing(sqlite3.connect(directories['observer'] / 'catalog.sqlite3')) as catalog:
                        self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 4)
                        receipt = catalog.execute('SELECT expected_sequence,applied_sequence,state,details FROM receipts WHERE identity=?', (inception.pre,)).fetchone()
                        self.assertEqual(receipt[:3], (2, 1, 'incomplete'))
                        self.assertEqual(json.loads(receipt[3]), result)
                        self.assertEqual(catalog.execute('SELECT revision FROM heads WHERE id=?', (ids[3],)).fetchone()[0], 1)
                    target.write_bytes(original[2])
                    self.assertTrue(receive(b)['complete'])
                else:
                    self.assertTrue(result['complete'])
                self.assertTrue(receive(b)['complete'])
                with closing(sqlite3.connect(directories['observer'] / 'catalog.sqlite3')) as catalog:
                    self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 6)
                    self.assertEqual(catalog.execute('SELECT expected_sequence,applied_sequence,state FROM receipts WHERE identity=?', (inception.pre,)).fetchone(), (2, 2, 'complete'))
                    saved_reference = json.loads((directories['observer'] / 'saved-reference.json').read_bytes())
                    self.assertEqual(catalog.execute('SELECT body FROM objects WHERE id=? AND revision=?',
                        (saved_reference['target'], saved_reference['revision'])).fetchone()[0], original[1])
                    self.assertEqual(catalog.execute('SELECT body,state FROM objects WHERE id=? AND revision=1', (ids[3],)).fetchone(), (None, 'redacted'))
                    self.assertEqual(catalog.execute('SELECT state FROM objects WHERE id=? AND revision=2', (ids[3],)).fetchone()[0], 'withdrawn')
                self.assertEqual((directories['observer'] / 'saved-reference.json').read_bytes(), reference_bytes)
                if mode in ('head-rollback', 'reactivate-retired'):
                    if mode == 'head-rollback':
                        later_entries = [entry(raw) for raw in original[:3]] + [new_entries[-1]]
                        error_code = 'revision_rollback'
                        error_message = 'InventoryTransitionError: El inventario retrocede una revisión conocida.'
                    else:
                        reactivated = obj(ids[3], 2, 'Cuerpo retirado que no debe reaparecer')
                        (directories['b'] / 'objects' / digest(reactivated)).write_bytes(reactivated)
                        later_entries = [entry(raw) for raw in original[:3]] + [entry(updated), entry(reactivated)]
                        error_code = 'retired_revision_reactivation'
                        error_message = 'InventoryTransitionError: No se restaura el cuerpo de una revisión retirada.'
                    later_manifest = encoded({'kind': KIND, 'owner': inception.pre, 'entries': later_entries})
                    third = eventing.interact(pre=inception.pre, dig=second.said, sn=3,
                                             data=[{ANCHOR: {'d': digest(later_manifest)}}])
                    history = [inception, first, second, third]
                    (directories['b'] / 'manifest.json').write_bytes(later_manifest)
                    (directories['b'] / 'proof.json').write_text(json.dumps([
                        {'event': event.raw.decode(), 'signature': owner.sign(event.raw, index=0).qb64} for event in history]))
                    receive(b, rejected=True, expected_error=error_message)
                    with closing(sqlite3.connect(directories['observer'] / 'catalog.sqlite3')) as catalog:
                        receipt = catalog.execute('SELECT expected_sequence,applied_sequence,state,details FROM receipts WHERE identity=?', (inception.pre,)).fetchone()
                        self.assertEqual(receipt[:3], (3, 2, 'rejected'))
                        self.assertEqual(json.loads(receipt[3]), {'error_code': error_code})
                        self.assertEqual(catalog.execute('SELECT revision FROM heads WHERE id=?', (ids[1],)).fetchone()[0], 2)
                        self.assertEqual(catalog.execute('SELECT body,state FROM objects WHERE id=? AND revision=2', (ids[3],)).fetchone(), (None, 'withdrawn'))
                    # Una nueva intención del titular, posterior al rechazo, permite reintentar.
                    fourth = eventing.interact(pre=inception.pre, dig=third.said, sn=4,
                                              data=[{ANCHOR: {'d': digest(manifests[1])}}])
                    history.append(fourth)
                    (directories['b'] / 'manifest.json').write_bytes(manifests[1])
                    (directories['b'] / 'proof.json').write_text(json.dumps([
                        {'event': event.raw.decode(), 'signature': owner.sign(event.raw, index=0).qb64} for event in history]))
                    self.assertTrue(receive(b)['complete'])
                    with closing(sqlite3.connect(directories['observer'] / 'catalog.sqlite3')) as catalog:
                        self.assertEqual(catalog.execute('SELECT expected_sequence,applied_sequence,state FROM receipts WHERE identity=?', (inception.pre,)).fetchone(), (4, 4, 'complete'))
                a.start()
                receive(a, rejected=True)
                with closing(sqlite3.connect(directories['observer'] / 'catalog.sqlite3')) as catalog:
                    self.assertIsNone(catalog.execute('SELECT body FROM objects WHERE id=? AND revision=1', (ids[3],)).fetchone()[0])
            finally:
                a.stop()
                b.stop()

    def test_inventory_refs_versions_withdrawal_and_old_origin_return(self):
        self.scenario('complete')

    def test_missing_object_keeps_previous_catalog_until_retry(self):
        self.scenario('missing')

    def test_changed_object_keeps_previous_catalog_until_retry(self):
        self.scenario('altered')

    def test_authorized_manifest_cannot_rewrite_existing_revision(self):
        self.scenario('revision-reuse')

    def test_authorized_head_rollback_is_rejected_and_persisted(self):
        self.scenario('head-rollback')

    def test_authorized_retired_revision_reactivation_is_rejected_and_persisted(self):
        self.scenario('reactivate-retired')

    def test_authorized_manifest_cannot_silently_omit_previous_object(self):
        self.scenario('omit-existing')

    def test_interrupted_receipt_keeps_pending_state_and_resumes(self):
        self.scenario('interrupted')

    def test_altered_manifest_without_owner_anchor_is_rejected(self):
        self.scenario('unauthorized')


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', type=Path)
    parser.add_argument('--restore', type=Path)
    parser.add_argument('--url')
    parser.add_argument('--owner')
    parser.add_argument('--interrupt-before-apply', action='store_true')
    args = parser.parse_args()
    if args.serve:
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
        serve(args.serve)
    elif args.restore:
        if not args.url or not args.owner:
            parser.error('Faltan --url o --owner')
        print(json.dumps(restore(args.restore.resolve(), args.url, args.owner, args.interrupt_before_apply)))
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
