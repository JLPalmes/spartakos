# SPDX-License-Identifier: AGPL-3.0-or-later
"""Flujo público integrado: autorización, copia, actualización y referencias."""
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import unittest
from urllib.error import URLError

from keri.core import serdering
import keri_destinations as destinations_lab
from keri_destinations import ROLE, deliver, stamp, store
import keri_inventory as inventory
import keri_inventory_access as access
from keri_profile_http import MARKER, fetch
from keri_diagnostics import diagnose


class IntegratedPublicFlow(unittest.TestCase):
    def test_owner_updates_multiobject_inventory_after_origin_off_with_stable_reference(self):
        with destinations_lab.EndpointAuthorization().participants() as (root, owner, a, b):
            (root / MARKER).write_text('spartakos\n')
            (root / 'access').mkdir(mode=0o700)
            directories = [root / name for name in ('http-a', 'http-b')]
            for directory in directories:
                directory.mkdir(mode=0o700)
                (directory / MARKER).write_text('spartakos\n')
                (directory / 'objects').mkdir(mode=0o700)
            ids = [owner.pre + ':' + name for name in ('profile', 'post-1', 'post-2')]
            def body(identifier, revision, text):
                return inventory.encoded({'id': identifier, 'revision': revision, 'audience': 'public', 'text': text})
            originals = [body(identifier, 1, text) for identifier, text in zip(ids, ('Perfil ficticio', 'Texto original', 'Texto a retirar'))]
            def entry(raw):
                value = json.loads(raw)
                return {'id': value['id'], 'revision': value['revision'], 'state': 'active', 'digest': inventory.digest(raw)}
            history = [owner.iserder]
            def issue(entries):
                manifest = inventory.encoded({'kind': inventory.KIND, 'owner': owner.pre, 'entries': entries})
                message = owner.interact(data=[{inventory.ANCHOR: {'d': inventory.digest(manifest)}}])
                history.append(serdering.SerderKERI(raw=message))
                return manifest
            def publish(directory, manifest, bodies):
                (directory / 'manifest.json').write_bytes(manifest)
                (directory / 'proof.json').write_text(json.dumps([
                    {'event': event.raw.decode(), 'signature': owner.sign(ser=event.raw, indexed=True)[0].qb64} for event in history]))
                for raw in bodies:
                    (directory / 'objects' / inventory.digest(raw)).write_bytes(raw)
            initial = issue([entry(raw) for raw in originals])
            for directory in directories:
                publish(directory, initial, originals)
            reference = inventory.encoded({'target': ids[1], 'revision': 1})
            (root / 'saved-reference.json').write_bytes(reference)
            servers = [inventory.InventoryProvider(directory) for directory in directories]
            def receive(provider, blocked=False):
                result = subprocess.run([sys.executable, str(Path(access.__file__).resolve()),
                    '--restore-authorized', str(root), '--owner', owner.pre, '--provider', provider.pre],
                    capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 3 if blocked else 0, result.stderr[-1500:])
                value = json.loads(result.stdout)
                if blocked:
                    self.assertEqual(value, {'blocked': 'unauthorized_provider'})
                else:
                    self.assertTrue(value['complete'])
                    self.assertIsNone(value['globally_current'])
                return value
            try:
                for server in servers:
                    server.start()
                with store(root / 'access', 'resolver') as observer:
                    deliver(observer, owner.makeOwnInception(), a.makeOwnInception(), b.makeOwnInception(),
                        a.makeLocScheme(url=servers[0].url, stamp=stamp(0)),
                        b.makeLocScheme(url=servers[1].url, stamp=stamp(0)),
                        owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1)))
                self.assertEqual(receive(a)['sequence'], 1)
                servers[0].stop()
                with self.assertRaises(URLError):
                    fetch(servers[0].url + '/manifest')
                with store(root / 'access', 'resolver') as observer:
                    deliver(observer, owner.makeEndRole(eid=a.pre, role=ROLE, allow=False, stamp=stamp(2)),
                        owner.makeEndRole(eid=b.pre, role=ROLE, stamp=stamp(3)))
                self.assertEqual(receive(b)['sequence'], 1)
                # La revisión nueva se crea de verdad después de apagar A.
                self.assertIsNone(servers[0].process)
                changed = body(ids[1], 2, 'Revisión firmada después del corte')
                updated = issue([entry(originals[0]), entry(originals[1]), entry(changed),
                    {'id': ids[2], 'revision': 2, 'state': 'withdrawn', 'digest': None}])
                publish(directories[1], updated, [originals[0], originals[1], changed])
                self.assertEqual(receive(b)['sequence'], 2)
                self.assertEqual(receive(b)['sequence'], 2)
                with closing(sqlite3.connect(root / 'catalog.sqlite3')) as catalog:
                    saved = json.loads((root / 'saved-reference.json').read_bytes())
                    self.assertEqual(catalog.execute('SELECT body FROM objects WHERE id=? AND revision=?',
                        (saved['target'], saved['revision'])).fetchone()[0], originals[1])
                    self.assertEqual(catalog.execute('SELECT COUNT(*) FROM objects').fetchone()[0], 5)
                    self.assertEqual(catalog.execute('SELECT body,state FROM objects WHERE id=? AND revision=1', (ids[2],)).fetchone(), (None, 'redacted'))
                    self.assertEqual(catalog.execute('SELECT state FROM objects WHERE id=? AND revision=2', (ids[2],)).fetchone()[0], 'withdrawn')
                self.assertEqual((root / 'saved-reference.json').read_bytes(), reference)
                servers[0].start()
                with store(root / 'access', 'resolver') as observer:
                    deliver(observer, a.makeLocScheme(url=servers[0].url, stamp=stamp(4)))
                receive(a, blocked=True)
                self.assertEqual(receive(b)['sequence'], 2)
                report = diagnose(root, owner.pre, b.pre)
                self.assertEqual(report['receipt']['value']['applied_sequence'], 2)
                self.assertEqual(report['attempt']['value']['state'], 'complete')
                self.assertEqual(report['authorization'], 'not_checked')
                self.assertEqual(report['global_freshness'], 'not_proven')
            finally:
                for server in servers:
                    server.stop()


if __name__ == '__main__':
    os.umask(0o077)
    unittest.main(verbosity=2)
