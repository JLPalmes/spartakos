# SPDX-License-Identifier: AGPL-3.0-or-later
"""Recepción HTTP finita con sobre durable; adaptación experimental, no MailboxDirector."""
import argparse
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from keri.core import serdering
from keri.app import storing
import keri_inventory_access as access_lab
from keri_destinations import ROLE, deliver, store
from keri_inventory import digest
from keri_mailbox import MARKER
from keri_mailbox_http import MailboxServer
from keri_profile_http import fetch

RECIPIENT = 'synthetic-recipient'
TOPIC = '/reply'


def connect(root):
    db = sqlite3.connect(root / 'http-inbox.sqlite3')
    db.executescript('''
        CREATE TABLE IF NOT EXISTS progress (source TEXT, recipient TEXT, topic TEXT, next_ordinal INTEGER,
            PRIMARY KEY(source,recipient,topic));
        CREATE TABLE IF NOT EXISTS messages (source TEXT, recipient TEXT, topic TEXT, ordinal INTEGER,
            payload BLOB NOT NULL, digest TEXT NOT NULL, validated INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY(source,recipient,topic,ordinal));
        CREATE TABLE IF NOT EXISTS conflicts (source TEXT, recipient TEXT, topic TEXT, ordinal INTEGER,
            payload BLOB NOT NULL, digest TEXT NOT NULL);
    ''')
    return db


def receive(root, url, limit=None):
    # La URL es la etiqueta local de esta fuente; no acredita la identidad criptográfica del emisor.
    with closing(connect(root)) as db:
        row = db.execute('SELECT next_ordinal FROM progress WHERE source=? AND recipient=? AND topic=?',
                         (url, RECIPIENT, TOPIC)).fetchone()
        ordinal = 0 if row is None else row[0]
        body = fetch(url + '/reply?from=' + str(ordinal))
        received = 0
        for frame in body.split(b'\n\n'):
            fields = dict(line.split(b': ', 1) for line in frame.splitlines() if b': ' in line)
            if b'id' not in fields:
                continue
            if fields.get(b'event') == TOPIC.encode() and b'data' in fields:
                incoming = int(fields[b'id'])
                previous = db.execute('SELECT payload FROM messages WHERE source=? AND recipient=? AND topic=? AND ordinal=?',
                                      (url, RECIPIENT, TOPIC, incoming)).fetchone()
                if previous is not None and previous[0] != fields[b'data']:
                    with db:
                        db.execute('INSERT INTO conflicts VALUES (?,?,?,?,?,?)',
                                   (url, RECIPIENT, TOPIC, incoming, fields[b'data'], digest(fields[b'data'])))
                    raise ValueError('Contenido distinto para una posición recibida; conflicto conservado.')
            if fields.get(b'event') != TOPIC.encode() or b'data' not in fields or int(fields[b'id']) != ordinal:
                raise ValueError('Tema o posición inesperados; no se salta el mensaje.')
            if limit is not None and received >= limit:
                break
            payload = fields[b'data']
            # Sobre, bytes y avance de recepción pertenecen a la misma transacción SQLite.
            with db:
                db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?,0)',
                           (url, RECIPIENT, TOPIC, ordinal, payload, digest(payload)))
                db.execute('INSERT OR REPLACE INTO progress VALUES (?,?,?,?)',
                           (url, RECIPIENT, TOPIC, ordinal + 1))
            ordinal += 1
            received += 1
        return {'received': received, 'next_ordinal': ordinal}


def validate(root, interrupt=False, as_resolver=False, expected_recipient=RECIPIENT):
    expected = json.loads((root / 'public-identifiers.json').read_text())
    processed = 0
    observer_root, observer_name = (root / 'access', 'resolver') if as_resolver else (root, 'http-receiver')
    if as_resolver:
        observer_root.mkdir(mode=0o700, exist_ok=True)
    with closing(connect(root)) as db, store(observer_root, observer_name) as hab:
        if db.execute('SELECT COUNT(*) FROM conflicts').fetchone()[0]:
            raise ValueError('Conflicto de recepción conocido; validación bloqueada.')
        if db.execute('SELECT COUNT(*) FROM messages WHERE validated IS NULL OR validated NOT IN (0,1)').fetchone()[0]:
            raise ValueError('Estado local de validación desconocido; no se omiten entradas.')
        sources = db.execute('SELECT DISTINCT source,recipient,topic FROM messages').fetchall()
        if len(sources) != 1:
            raise ValueError('El ensayo solo admite una fuente y un tema; no decide orden entre fuentes.')
        rows = db.execute('SELECT source,recipient,topic,ordinal,payload,digest FROM messages '
                          'WHERE validated=0 ORDER BY ordinal').fetchall()
        for source, recipient, topic, ordinal, payload, checksum in rows:
            if recipient != expected_recipient or topic != TOPIC or digest(payload) != checksum:
                raise ValueError('Sobre o bytes locales alterados; entrada pendiente conservada.')
            event = serdering.SerderKERI(raw=payload)
            if event.ilk == 'icp' and event.pre in (expected['owner'], expected['provider']):
                deliver(hab, payload)
                if event.pre not in hab.kevers:
                    raise ValueError('Creación no validada.')
            elif event.ilk == 'rpy' and (
                    event.ked['a'] == {'cid': expected['owner'], 'eid': expected['provider'], 'role': ROLE}
                    or (event.ked['r'] == '/loc/scheme' and set(event.ked['a']) == {'eid', 'scheme', 'url'}
                        and event.ked['a']['eid'] == expected['provider'] and event.ked['a']['scheme'] == 'http')):
                deliver(hab, payload)
                if hab.db.rpys.get(keys=(event.said,)) is None:
                    raise ValueError('Respuesta no validada; entrada pendiente conservada.')
            else:
                raise ValueError('Mensaje fuera del escenario; entrada pendiente conservada.')
            if interrupt and event.ilk == 'rpy' and event.ked['r'].endswith('/cut'):
                os._exit(21)
            with db:
                db.execute('UPDATE messages SET validated=1 WHERE source=? AND recipient=? AND topic=? AND ordinal=?',
                           (source, recipient, topic, ordinal))
            processed += 1
        return {'processed': processed, 'pending': db.execute('SELECT COUNT(*) FROM messages WHERE validated=0').fetchone()[0],
                'allowed_in_view': hab.fetchEndAllowed(expected['owner'], ROLE, expected['provider'])}


def restore_after_inbox(root, owner, provider):
    """Puerta conservadora del ensayo de una fuente: pendiente no equivale a permiso actualizado."""
    def check_inbox():
        with closing(connect(root)) as db:
            if db.execute('SELECT COUNT(*) FROM conflicts').fetchone()[0]:
                raise access_lab.InventoryAccessError('inbox_conflict', 'Conflicto de recepción pendiente.')
            count, pending = db.execute('SELECT COUNT(*),COALESCE(SUM(validated IS NOT 1),0) FROM messages').fetchone()
            if not count or pending:
                raise access_lab.InventoryAccessError('inbox_pending', 'La recepción todavía no está validada.')
    check_inbox()
    # Se repite la precaución antes de aplicar, sin afirmar atomicidad entre almacenes.
    return access_lab.restore_authorized(root, owner, provider, before_apply_check=check_inbox)


class HttpDurableInbox(unittest.TestCase):
    def test_complete_http_grant_restore_pending_cut_then_revocation_keeps_existing_copy(self):
        self.complete_flow()

    def test_cut_received_during_object_download_blocks_catalog_apply(self):
        self.complete_flow(during_transfer=True)

    def test_unknown_local_marks_cannot_hide_pending_cut_or_promote_permission(self):
        self.complete_flow(unknown_mark=True)

    def complete_flow(self, during_transfer=False, unknown_mark=False):
        with tempfile.TemporaryDirectory(prefix='spartakos-inbox-full-flow-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            directory = root / 'public-content'
            directory.mkdir()
            (directory / MARKER).write_text('spartakos\n')
            (directory / 'objects').mkdir()
            content = access_lab.inventory.InventoryProvider(directory)
            mailbox_server = MailboxServer(root)
            try:
                content.start()
                # Claves efímeras del escenario, cerradas antes de recibir el buzón; no se exportan.
                with store(root, 'synthetic-owner') as owner, store(root, 'synthetic-provider') as provider:
                    body = access_lab.inventory.encoded({'id': owner.pre + ':post-1', 'revision': 1,
                        'audience': 'public', 'text': 'Publicación ficticia del flujo integrado'})
                    manifest = access_lab.inventory.encoded({'kind': access_lab.inventory.KIND, 'owner': owner.pre,
                        'entries': [{'id': owner.pre + ':post-1', 'revision': 1, 'state': 'active',
                                     'digest': digest(body)}]})
                    anchored = serdering.SerderKERI(raw=owner.interact(data=[{access_lab.inventory.ANCHOR: {'d': digest(manifest)}}]))
                    proof = [{'event': event.raw.decode(), 'signature': owner.sign(ser=event.raw, indexed=True)[0].qb64}
                             for event in (owner.iserder, anchored)]
                    (directory / 'proof.json').write_text(json.dumps(proof))
                    (directory / 'manifest.json').write_bytes(manifest)
                    (directory / 'objects' / digest(body)).write_bytes(body)
                    expected = {'owner': owner.pre, 'provider': provider.pre}
                    (root / 'public-identifiers.json').write_text(json.dumps(expected))
                    stamp = access_lab.stamp
                    cut = owner.makeEndRole(eid=provider.pre, role=ROLE, allow=False, stamp=stamp(2))
                    messages = [owner.makeOwnInception(), provider.makeOwnInception(),
                        provider.makeLocScheme(url=content.url, stamp=stamp(0)),
                        owner.makeEndRole(eid=provider.pre, role=ROLE, stamp=stamp(1)), cut, cut]
                    native = storing.Mailboxer(
                        name='replies', headDirPath=str(root / 'mailbox'), temp=False, reopen=True)
                    try:
                        for message in messages:
                            self.assertTrue(native.storeMsg(RECIPIENT + TOPIC, bytes(message)))
                    finally:
                        native.close()
                mailbox_server.start()
                def run(stage, code=0):
                    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                        '--stage', stage, '--resolver'], capture_output=True, text=True, timeout=20)
                    self.assertEqual(result.returncode, code, result.stderr[-1800:])
                    return json.loads(result.stdout) if code == 0 else result.stderr
                self.assertEqual(receive(root, mailbox_server.url, limit=4), {'received': 4, 'next_ordinal': 4})
                self.assertEqual(run('validate'), {'processed': 4, 'pending': 0, 'allowed_in_view': True})
                if during_transfer:
                    real_fetch = access_lab.inventory.fetch
                    injected = []
                    def fetch_then_receive_cut(url):
                        data = real_fetch(url)
                        if '/objects/' in url and not injected:
                            injected.append(receive(root, mailbox_server.url))
                        return data
                    with patch.object(access_lab.inventory, 'fetch', side_effect=fetch_then_receive_cut):
                        with self.assertRaises(access_lab.InventoryAccessError) as raised:
                            restore_after_inbox(root, expected['owner'], expected['provider'])
                    self.assertEqual(raised.exception.code, 'inbox_pending')
                    self.assertEqual(injected, [{'received': 2, 'next_ordinal': 6}])
                    with closing(sqlite3.connect(root / 'catalog.sqlite3')) as db:
                        self.assertEqual(db.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 0)
                    observed = access_lab.diagnose(root, expected['owner'], expected['provider'])
                    self.assertEqual(observed['attempt']['value'], {'state': 'blocked', 'error_code': 'inbox_pending'})
                    self.assertEqual(observed['inbox']['messages']['value']['pending_count'], 2)
                    self.assertEqual(run('validate'), {'processed': 2, 'pending': 0, 'allowed_in_view': False})
                    self.assertIn('Proveedor no autorizado', run('restore', code=1))
                    return
                self.assertTrue(run('restore')['complete'])
                def report():
                    files = list(root.glob('*.sqlite3'))
                    before = {file.name: (file.read_bytes(), file.stat().st_mtime_ns) for file in files}
                    value = access_lab.diagnose(root, expected['owner'], expected['provider'])
                    self.assertEqual({file.name: (file.read_bytes(), file.stat().st_mtime_ns) for file in files}, before)
                    self.assertFalse(value['atomic_snapshot'])
                    self.assertEqual(value['global_freshness'], 'not_proven')
                    self.assertNotIn('Publicación ficticia', json.dumps(value))
                    return value
                first = report()
                self.assertEqual(first['inbox']['messages']['value']['marked_validated_count'], 4)
                self.assertEqual(first['attempt']['value']['state'], 'complete')
                with closing(sqlite3.connect(root / 'catalog.sqlite3')) as db:
                    before = db.execute('SELECT id,revision,state,body FROM objects').fetchall()
                    self.assertEqual(len(before), 1)
                self.assertEqual(receive(root, mailbox_server.url), {'received': 2, 'next_ordinal': 6})
                if unknown_mark:
                    with closing(connect(root)) as db, db:
                        db.execute("UPDATE messages SET validated='synthetic_unknown' WHERE ordinal>=4")
                    self.assertIn('todavía no está validada', run('restore', code=1))
                    self.assertIn('Estado local de validación desconocido', run('validate', code=1))
                    unknown = report()
                    self.assertEqual(unknown['inbox']['messages']['value']['unrecognized_state_count'], 2)
                    self.assertEqual(unknown['inbox']['messages']['value']['pending_count'], 0)
                    with store(root / 'access', 'resolver') as hab:
                        self.assertTrue(hab.fetchEndAllowed(expected['owner'], ROLE, expected['provider']))
                    with closing(sqlite3.connect(root / 'catalog.sqlite3')) as db:
                        self.assertEqual(db.execute('SELECT id,revision,state,body FROM objects').fetchall(), before)
                    return
                self.assertIn('todavía no está validada', run('restore', code=1))
                pending_report = report()
                self.assertEqual(pending_report['inbox']['messages']['value']['pending_count'], 2)
                self.assertEqual(pending_report['inbox']['transport']['value']['next_ordinal_single_stream'], 6)
                self.assertEqual(pending_report['attempt']['value']['state'], 'complete')
                self.assertEqual(run('validate'), {'processed': 2, 'pending': 0, 'allowed_in_view': False})
                self.assertIn('Proveedor no autorizado', run('restore', code=1))
                final_report = report()
                self.assertEqual(final_report['inbox']['messages']['value']['pending_count'], 0)
                self.assertEqual(final_report['attempt']['value'], {'state': 'blocked', 'error_code': 'unauthorized_provider'})
                self.assertEqual(final_report['catalog']['value']['stored_revision_count'], 1)
                with closing(sqlite3.connect(root / 'catalog.sqlite3')) as db:
                    self.assertEqual(db.execute('SELECT id,revision,state,body FROM objects').fetchall(), before)
            finally:
                mailbox_server.stop()
                content.stop()

    def test_pending_cut_blocks_delivery_until_resolver_validates_and_rejects_provider(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-inbox-access-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            produced = subprocess.run([sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
                '--stage', 'produce', '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
            self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
            expected = json.loads((root / 'public-identifiers.json').read_text())
            server = MailboxServer(root)
            def validate_worker():
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                    '--stage', 'validate', '--resolver'], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr[-1500:])
                return json.loads(result.stdout)
            def blocked(code):
                with patch.object(access_lab.inventory, 'restore') as restoration:
                    with self.assertRaises(access_lab.InventoryAccessError) as raised:
                        restore_after_inbox(root, expected['owner'], expected['provider'])
                    self.assertEqual(raised.exception.code, code)
                    restoration.assert_not_called()
            try:
                server.start()
                self.assertEqual(receive(root, server.url, limit=2), {'received': 2, 'next_ordinal': 2})
                blocked('inbox_pending')
                self.assertEqual(validate_worker(), {'processed': 2, 'pending': 0, 'allowed_in_view': True})
                self.assertEqual(receive(root, server.url), {'received': 2, 'next_ordinal': 4})
                with store(root / 'access', 'resolver') as hab:
                    self.assertTrue(hab.fetchEndAllowed(expected['owner'], ROLE, expected['provider']))
                # Hay concesión anterior, pero el corte recibido todavía no está validado.
                blocked('inbox_pending')
                self.assertEqual(validate_worker(), {'processed': 2, 'pending': 0, 'allowed_in_view': False})
                blocked('unauthorized_provider')
            finally:
                server.stop()

    def prepared(self, root):
        (root / MARKER).write_text('spartakos\n')
        produced = subprocess.run([sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
            '--stage', 'produce', '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
        self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
        server = MailboxServer(root)
        try:
            server.start()
            self.assertEqual(receive(root, server.url), {'received': 4, 'next_ordinal': 4})
            return server.url
        finally:
            server.stop()

    def test_altered_pending_bytes_or_topic_do_not_become_validated(self):
        for kind in ('bytes', 'topic'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(prefix='spartakos-inbox-altered-') as path:
                root = Path(path)
                self.prepared(root)
                with closing(connect(root)) as db, db:
                    if kind == 'bytes':
                        db.execute("UPDATE messages SET payload=? WHERE ordinal=0", (b'altered',))
                    else:
                        db.execute("UPDATE messages SET topic='/unexpected'")
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                    '--stage', 'validate'], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 1)
                self.assertIn('Sobre o bytes locales alterados', result.stderr)
                with closing(connect(root)) as db:
                    self.assertEqual(db.execute('SELECT SUM(validated),COUNT(*) FROM messages').fetchone(), (0, 4))
                    self.assertEqual(db.execute('SELECT next_ordinal FROM progress').fetchone()[0], 4)
                with store(root, 'http-receiver') as hab:
                    self.assertNotIn(json.loads((root / 'public-identifiers.json').read_text())['owner'], hab.kevers)

    def test_conflicting_repeated_position_preserves_both_bytes_and_blocks_validation(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-inbox-conflict-') as path:
            root = Path(path)
            url = self.prepared(root)
            with closing(connect(root)) as db:
                original = db.execute('SELECT payload FROM messages WHERE ordinal=0').fetchone()[0]
            # Respuesta conflictiva inyectada en el límite de transporte; la primera recepción sí usó HTTP real.
            frame = b'id: 0\nevent: /reply\ndata: conflicting-message\n\n'
            with patch.object(sys.modules[__name__], 'fetch', return_value=frame):
                with self.assertRaisesRegex(ValueError, 'conflicto conservado'):
                    receive(root, url)
            with closing(connect(root)) as db:
                self.assertEqual(db.execute('SELECT payload FROM messages WHERE ordinal=0').fetchone()[0], original)
                self.assertEqual(db.execute('SELECT ordinal,payload FROM conflicts').fetchall(), [(0, b'conflicting-message')])
                self.assertEqual(db.execute('SELECT next_ordinal FROM progress').fetchone()[0], 4)
            result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                '--stage', 'validate'], capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 1)
            self.assertIn('Conflicto de recepción conocido', result.stderr)
            with closing(connect(root)) as db:
                self.assertEqual(db.execute('SELECT SUM(validated),COUNT(*) FROM messages').fetchone(), (0, 4))

    def test_http_receive_then_offline_validation_recovers_after_cut_before_mark(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-http-inbox-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            produced = subprocess.run([sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
                '--stage', 'produce', '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
            self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
            server = MailboxServer(root)
            def run(stage, extra=(), code=0):
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                    '--stage', stage, *extra], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, code, result.stderr[-1800:])
                return json.loads(result.stdout) if result.stdout else None
            try:
                server.start()
                self.assertEqual(run('receive', ('--url', server.url)), {'received': 4, 'next_ordinal': 4})
                self.assertEqual(run('receive', ('--url', server.url)), {'received': 0, 'next_ordinal': 4})
                with closing(connect(root)) as db:
                    rows = db.execute('SELECT source,recipient,topic,ordinal,validated FROM messages ORDER BY ordinal').fetchall()
                    self.assertEqual(rows, [(server.url, RECIPIENT, TOPIC, n, 0) for n in range(4)])
                with store(root, 'http-receiver') as hab:
                    self.assertNotIn(json.loads((root / 'public-identifiers.json').read_text())['owner'], hab.kevers)
            finally:
                server.stop()
            run('interrupt', code=21)
            self.assertEqual(run('validate'), {'processed': 2, 'pending': 0, 'allowed_in_view': False})
            self.assertEqual(run('validate'), {'processed': 0, 'pending': 0, 'allowed_in_view': False})


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--stage', choices=['receive', 'validate', 'interrupt', 'restore'])
    parser.add_argument('--url')
    parser.add_argument('--resolver', action='store_true')
    args = parser.parse_args()
    if args.worker:
        if (args.worker / MARKER).read_text() != 'spartakos\n':
            parser.error('Directorio no preparado.')
        if args.stage == 'receive':
            if not args.url:
                parser.error('Falta --url')
            result = receive(args.worker, args.url)
        elif args.stage == 'restore':
            expected = json.loads((args.worker / 'public-identifiers.json').read_text())
            result = restore_after_inbox(args.worker, expected['owner'], expected['provider'])
        elif args.stage in ('validate', 'interrupt'):
            result = validate(args.worker, interrupt=args.stage == 'interrupt', as_resolver=args.resolver)
        else:
            parser.error('Falta --stage')
        print(json.dumps(result))
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
