# SPDX-License-Identifier: AGPL-3.0-or-later
"""Puerta local experimental: proveedor autorizado, conflicto y restauración."""
from contextlib import closing
import argparse
from pathlib import Path
import subprocess
import sys
import json
import os
import sqlite3
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from keri.core import eventing, serdering
import keri_destinations as destinations_lab
from keri_destinations import ROLE, deliver, stamp, store
import keri_inventory as inventory
from keri_profile_state import ProfileState
from keri_profile_http import MARKER
from keri_diagnostics import diagnose


class InventoryAccessError(PermissionError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def verified_address(root, owner, provider):
    state = ProfileState(root)
    try:
        count = state.connection.execute('SELECT COUNT(*) FROM conflicts WHERE identity=?', (owner,)).fetchone()[0]
        if count:
            raise InventoryAccessError('known_conflict', 'Hay un conflicto registrado para esta identidad.')
    finally:
        state.close()
    with store(root / 'access', 'resolver') as observer:
        if observer.fetchEndAllowed(owner, ROLE, provider) is not True:
            raise InventoryAccessError('unauthorized_provider', 'Proveedor no autorizado en esta vista.')
        address = observer.fetchUrl(provider)
        if not address:
            raise ValueError('No hay dirección validada del proveedor.')
        return address


def restore_authorized(root, owner, provider, interrupt_before_apply=False, interrupt_after_apply=False, before_apply_check=None):
    root = root.resolve()
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    journal = sqlite3.connect(root / 'inventory-access.sqlite3')
    try:
        journal.execute('CREATE TABLE IF NOT EXISTS attempts (identity TEXT, provider TEXT, state TEXT, error_code TEXT, PRIMARY KEY(identity,provider))')
        def record(state, error_code=None):
            with journal:
                journal.execute('INSERT OR REPLACE INTO attempts VALUES (?,?,?,?)', (owner, provider, state, error_code))
        record('checking')
        try:
            address = verified_address(root, owner, provider)
            def recheck():
                if before_apply_check is not None:
                    before_apply_check()
                if verified_address(root, owner, provider) != address:
                    raise InventoryAccessError('address_changed', 'La dirección autorizada cambió durante la recepción.')
            # No hay transacción conjunta entre autorización, conflicto y catálogo.
            result = inventory.restore(root, address, owner, interrupt_before_apply=interrupt_before_apply, before_apply=recheck)
            if interrupt_after_apply:
                print(json.dumps({'interrupted_after_apply': True}), flush=True)
                os._exit(20)  # Solo instrumentación: catálogo confirmado, intento aún sin marcar.
            record('complete' if result['complete'] else 'incomplete')
            return result
        except InventoryAccessError as error:
            record('blocked', error.code)
            raise
        except HTTPError as error:
            record('failed', 'http_' + str(error.code))
            error.close()
            raise
        except URLError:
            record('failed', 'transport_unavailable')
            raise
    finally:
        journal.close()


class InventoryAccess(unittest.TestCase):
    def scenario(self, mode):
        with destinations_lab.EndpointAuthorization().participants() as (root, owner, _, provider):
            (root / MARKER).write_text('spartakos\n')
            (root / 'access').mkdir(mode=0o700)
            directory = root / 'inventory-http'
            directory.mkdir(mode=0o700)
            (directory / MARKER).write_text('spartakos\n')
            (directory / 'objects').mkdir(mode=0o700)
            body = inventory.encoded({'id': owner.pre + ':post-1', 'revision': 1,
                                      'audience': 'public', 'text': 'Objeto público ficticio'})
            manifest = inventory.encoded({'kind': inventory.KIND, 'owner': owner.pre,
                'entries': [{'id': owner.pre + ':post-1', 'revision': 1, 'state': 'active', 'digest': inventory.digest(body)}]})
            inception = owner.iserder
            message = owner.interact(data=[{inventory.ANCHOR: {'d': inventory.digest(manifest)}}])
            anchored = serdering.SerderKERI(raw=message)
            proof = [{'event': event.raw.decode(), 'signature': owner.sign(ser=event.raw, indexed=True)[0].qb64}
                     for event in (inception, anchored)]
            (directory / 'proof.json').write_text(json.dumps(proof))
            (directory / 'manifest.json').write_bytes(manifest)
            (directory / 'objects' / inventory.digest(body)).write_bytes(body)
            server = inventory.InventoryProvider(directory)
            try:
                server.start()
                with store(root / 'access', 'resolver') as observer:
                    deliver(observer, owner.makeOwnInception(), provider.makeOwnInception(),
                            provider.makeLocScheme(url=server.url, stamp=stamp(0)))
                    if mode != 'unauthorized':
                        deliver(observer, owner.makeEndRole(eid=provider.pre, role=ROLE, stamp=stamp(1)))
                def record_conflict():
                    alternate = eventing.interact(pre=owner.pre, dig=inception.said, sn=1,
                                                  data=[{'branch': 'conflicting-fixture'}])
                    evidence = {'inception': inception.raw.decode(),
                        'inception_signature': owner.sign(ser=inception.raw, indexed=True)[0].qb64,
                        'branches': [*proof[1:], {'event': alternate.raw.decode(),
                            'signature': owner.sign(ser=alternate.raw, indexed=True)[0].qb64}]}
                    state = ProfileState(root)
                    try:
                        state.flag_verified_fixture_conflict(evidence)
                    finally:
                        state.close()
                if mode == 'conflict':
                    record_conflict()
                if mode in ('unauthorized', 'conflict'):
                    with patch.object(inventory, 'fetch', side_effect=AssertionError('No debe consultar HTTP')) as network:
                        with self.assertRaises(PermissionError) as blocked:
                            restore_authorized(root, owner.pre, provider.pre)
                        self.assertIn('conflicto' if mode == 'conflict' else 'no autorizado', str(blocked.exception))
                        network.assert_not_called()
                    self.assertFalse((root / 'catalog.sqlite3').exists())
                    with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                        self.assertEqual(journal.execute('SELECT state,error_code FROM attempts').fetchone(),
                            ('blocked', 'known_conflict' if mode == 'conflict' else 'unauthorized_provider'))
                    return
                if mode in ('new-process', 'interrupted-process', 'revoked-after-interrupt', 'conflict-after-interrupt', 'after-apply', 'revoked-after-apply'):
                    def worker(interrupt=False, expected_code=0, after_apply=False):
                        args = [sys.executable, str(Path(__file__).resolve()), '--restore-authorized', str(root),
                                '--owner', owner.pre, '--provider', provider.pre]
                        if interrupt:
                            args.append('--interrupt-before-apply')
                        if after_apply:
                            args.append('--interrupt-after-apply')
                        result = subprocess.run(args, capture_output=True, text=True, timeout=20)
                        self.assertEqual(result.returncode, expected_code, result.stderr[-1800:])
                        return json.loads(result.stdout)
                    after_apply = mode in ('after-apply', 'revoked-after-apply')
                    if after_apply:
                        self.assertEqual(worker(after_apply=True, expected_code=20), {'interrupted_after_apply': True})
                        with closing(sqlite3.connect(root / 'catalog.sqlite3')) as catalog:
                            self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 1)
                            self.assertEqual(catalog.execute('SELECT body FROM objects').fetchone()[0], body)
                            self.assertEqual(catalog.execute('SELECT expected_sequence,applied_sequence,state FROM receipts').fetchone(), (1, 1, 'complete'))
                        with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                            self.assertEqual(journal.execute('SELECT state FROM attempts').fetchone()[0], 'checking')
                        files = [root / name for name in ('catalog.sqlite3', 'inventory-access.sqlite3', 'profile-state.sqlite3')]
                        before = {path.name: (path.read_bytes(), path.stat().st_mtime_ns) for path in files if path.exists()}
                        report = diagnose(root, owner.pre, provider.pre)
                        self.assertEqual(report['receipt']['value']['state'], 'complete')
                        self.assertEqual(report['attempt']['value']['state'], 'checking')
                        self.assertEqual(report['catalog']['value']['stored_revision_count'], 1)
                        self.assertEqual(report['authorization'], 'not_checked')
                        self.assertEqual(report['global_freshness'], 'not_proven')
                        self.assertFalse(report['atomic_snapshot'])
                        self.assertNotIn('Objeto público ficticio', json.dumps(report))
                        self.assertEqual({path.name: (path.read_bytes(), path.stat().st_mtime_ns) for path in files if path.exists()}, before)
                    interrupted = mode != 'new-process' and not after_apply
                    if interrupted:
                        self.assertEqual(worker(interrupt=True, expected_code=19), {'interrupted_before_apply': True})
                        with closing(sqlite3.connect(root / 'catalog.sqlite3')) as catalog:
                            self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 0)
                            self.assertEqual(catalog.execute('SELECT expected_sequence,applied_sequence,state FROM receipts').fetchone(), (1, 0, 'receiving'))
                        with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                            self.assertEqual(journal.execute('SELECT state FROM attempts').fetchone()[0], 'checking')
                    if mode == 'conflict-after-interrupt':
                        record_conflict()
                        self.assertEqual(worker(expected_code=3), {'blocked': 'known_conflict'})
                        # Renovar el rol no resuelve la contradicción del titular.
                        with store(root / 'access', 'resolver') as observer:
                            deliver(observer, owner.makeEndRole(eid=provider.pre, role=ROLE, stamp=stamp(3)))
                        self.assertEqual(worker(expected_code=3), {'blocked': 'known_conflict'})
                        with closing(sqlite3.connect(root / 'catalog.sqlite3')) as catalog:
                            self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 0)
                            self.assertEqual(catalog.execute('SELECT expected_sequence,applied_sequence,state FROM receipts').fetchone(), (1, 0, 'receiving'))
                        with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                            self.assertEqual(journal.execute('SELECT state,error_code FROM attempts').fetchone(), ('blocked', 'known_conflict'))
                        return
                    if mode in ('revoked-after-interrupt', 'revoked-after-apply'):
                        with store(root / 'access', 'resolver') as observer:
                            deliver(observer, owner.makeEndRole(eid=provider.pre, role=ROLE, allow=False, stamp=stamp(2)))
                        self.assertEqual(worker(expected_code=3), {'blocked': 'unauthorized_provider'})
                        with closing(sqlite3.connect(root / 'catalog.sqlite3')) as catalog:
                            self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 1 if after_apply else 0)
                            if after_apply:
                                self.assertEqual(catalog.execute('SELECT body FROM objects').fetchone()[0], body)
                                self.assertEqual(catalog.execute('SELECT state FROM receipts').fetchone()[0], 'complete')
                        if after_apply:
                            report = diagnose(root, owner.pre, provider.pre)
                            self.assertEqual(report['receipt']['value']['state'], 'complete')
                            self.assertEqual(report['attempt']['value'], {'state': 'blocked', 'error_code': 'unauthorized_provider'})
                            self.assertEqual(report['authorization'], 'not_checked')
                        with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                            self.assertEqual(journal.execute('SELECT state,error_code FROM attempts').fetchone(), ('blocked', 'unauthorized_provider'))
                        with store(root / 'access', 'resolver') as observer:
                            deliver(observer, owner.makeEndRole(eid=provider.pre, role=ROLE, stamp=stamp(3)))
                    result = worker()
                    self.assertTrue(result['complete'])
                    self.assertIsNone(result['globally_current'])
                    self.assertTrue(worker()['complete'])
                    with closing(sqlite3.connect(root / 'catalog.sqlite3')) as catalog:
                        self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 1)
                        self.assertEqual(catalog.execute('SELECT body FROM objects').fetchone()[0], body)
                        self.assertEqual(catalog.execute('SELECT expected_sequence,applied_sequence,state FROM receipts').fetchone(), (1, 1, 'complete'))
                    with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                        self.assertEqual(journal.execute('SELECT state,error_code FROM attempts').fetchone(), ('complete', None))
                    return
                if mode in ('provider-offline', 'proof-404'):
                    if mode == 'provider-offline':
                        server.stop()
                        expected_exception, expected_code = URLError, 'transport_unavailable'
                    else:
                        (directory / 'proof.json').unlink()
                        expected_exception, expected_code = HTTPError, 'http_404'
                    with self.assertRaises(expected_exception):
                        restore_authorized(root, owner.pre, provider.pre)
                    with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                        self.assertEqual(journal.execute('SELECT state,error_code FROM attempts').fetchone(), ('failed', expected_code))
                    with closing(sqlite3.connect(root / 'catalog.sqlite3')) as catalog:
                        self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 0)
                        self.assertEqual(catalog.execute('SELECT COUNT(*) FROM receipts').fetchone()[0], 0)
                    if mode == 'provider-offline':
                        server.start()
                        with store(root / 'access', 'resolver') as observer:
                            deliver(observer, provider.makeLocScheme(url=server.url, stamp=stamp(2)))
                    else:
                        (directory / 'proof.json').write_text(json.dumps(proof))
                    self.assertTrue(restore_authorized(root, owner.pre, provider.pre)['complete'])
                    with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                        self.assertEqual(journal.execute('SELECT state,error_code FROM attempts').fetchone(), ('complete', None))
                    return
                original_fetch = inventory.fetch
                changed = False
                def fetching(url):
                    nonlocal changed
                    result = original_fetch(url)
                    if mode == 'revoked-during-read' and url.endswith('/manifest') and not changed:
                        with store(root / 'access', 'resolver') as observer:
                            deliver(observer, owner.makeEndRole(eid=provider.pre, role=ROLE, allow=False, stamp=stamp(2)))
                        changed = True
                    return result
                with patch.object(inventory, 'fetch', side_effect=fetching):
                    if mode == 'revoked-during-read':
                        with self.assertRaises(PermissionError) as blocked:
                            restore_authorized(root, owner.pre, provider.pre)
                        self.assertIn('no autorizado', str(blocked.exception))
                    else:
                        result = restore_authorized(root, owner.pre, provider.pre)
                        self.assertTrue(result['complete'])
                        self.assertIsNone(result['globally_current'])
                with closing(sqlite3.connect(root / 'catalog.sqlite3')) as catalog:
                    if mode == 'revoked-during-read':
                        self.assertTrue(changed)
                        self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 0)
                        self.assertEqual(catalog.execute('SELECT state FROM receipts').fetchone()[0], 'receiving')
                    else:
                        self.assertEqual(catalog.execute('SELECT body FROM objects').fetchone()[0], body)
                with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                    self.assertEqual(journal.execute('SELECT state,error_code FROM attempts').fetchone(),
                        ('blocked', 'unauthorized_provider') if mode == 'revoked-during-read' else ('complete', None))
                if mode == 'revoked-during-read':
                    with store(root / 'access', 'resolver') as observer:
                        deliver(observer, owner.makeEndRole(eid=provider.pre, role=ROLE, stamp=stamp(3)))
                self.assertTrue(restore_authorized(root, owner.pre, provider.pre)['complete'])
                with closing(sqlite3.connect(root / 'inventory-access.sqlite3')) as journal:
                    self.assertEqual(journal.execute('SELECT state,error_code FROM attempts').fetchone(), ('complete', None))
            finally:
                server.stop()

    def test_authorized_endpoint_restores_inventory_and_retries(self):
        self.scenario('authorized')

    def test_known_address_without_role_blocks_before_http(self):
        self.scenario('unauthorized')

    def test_persisted_verified_conflict_blocks_before_http(self):
        self.scenario('conflict')

    def test_authorized_restore_reopens_in_new_verifier_processes(self):
        self.scenario('new-process')

    def test_interrupted_authorized_restore_resumes_in_new_process(self):
        self.scenario('interrupted-process')

    def test_revocation_between_interruption_and_retry_is_rechecked(self):
        self.scenario('revoked-after-interrupt')

    def test_conflict_between_interruption_and_retry_remains_blocking(self):
        self.scenario('conflict-after-interrupt')

    def test_unavailable_provider_failure_is_persisted_and_can_retry(self):
        self.scenario('provider-offline')

    def test_http_missing_proof_failure_is_persisted_and_can_retry(self):
        self.scenario('proof-404')

    def test_exit_after_catalog_apply_does_not_falsify_attempt_and_retry_is_idempotent(self):
        self.scenario('after-apply')

    def test_revocation_after_applied_catalog_blocks_retry_without_erasing_copy(self):
        self.scenario('revoked-after-apply')

    def test_revocation_received_during_download_blocks_catalog_apply(self):
        self.scenario('revoked-during-read')


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--restore-authorized', type=Path)
    parser.add_argument('--owner')
    parser.add_argument('--provider')
    parser.add_argument('--interrupt-before-apply', action='store_true')
    parser.add_argument('--interrupt-after-apply', action='store_true')
    args = parser.parse_args()
    if args.restore_authorized:
        if not args.owner or not args.provider:
            parser.error('Faltan --owner o --provider')
        try:
            result = restore_authorized(args.restore_authorized, args.owner, args.provider, args.interrupt_before_apply, args.interrupt_after_apply)
        except InventoryAccessError as error:
            print(json.dumps({'blocked': error.code}))
            sys.exit(3)
        print(json.dumps(result))
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
