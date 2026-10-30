# SPDX-License-Identifier: AGPL-3.0-or-later
"""Vistas parciales de autorización y entrega, con procesos verificadores nuevos."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import keri_destinations as destinations_lab
from keri_destinations import ROLE, deliver, stamp, store
from keri_authorized_delivery import read_authorized, revise
from keri_profile_http import Provider, MARKER
from keri_profile_state import ProfileState


def run_stage(root, stage, abrupt=False):
    root = root.resolve()
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    fixture = json.loads((root / 'public-messages.json').read_text())
    state = ProfileState(root)
    try:
        with store(root, 'observer') as observer:
            if stage == 'initialize':
                deliver(observer, *(bytes.fromhex(message) for message in fixture['initial']))
            elif stage == 'partial':
                for name in fixture['partial']:
                    deliver(observer, bytes.fromhex(fixture[name]))
            elif stage == 'complete':
                # Entrega repetida deliberada de ambas declaraciones ya firmadas.
                for _ in range(2):
                    deliver(observer, bytes.fromhex(fixture['cut_a']), bytes.fromhex(fixture['add_b']))
            elif stage not in ('verify', 'verify_partial'):
                raise ValueError('Etapa desconocida.')
            expected = {'a'} if stage == 'initialize' else (
                {'b'} if stage in ('complete', 'verify') else set(fixture['expected_partial']))
            for name in ('a', 'b'):
                provider = fixture[name]
                allowed = observer.fetchEndAllowed(fixture['owner'], ROLE, provider) is True
                assert allowed == (name in expected)
                if name in expected:
                    result = read_authorized(observer, state, fixture['owner'], provider)
                    assert result['sequence'] == 1
                    assert result['head_in_this_view']
                    assert result['globally_current'] is None
                else:
                    try:
                        read_authorized(observer, state, fixture['owner'], provider)
                    except PermissionError:
                        pass
                    else:
                        raise AssertionError('Se consultó un proveedor sin autorización.')
            # El perfil inicial ya quedó guardado: ningún cambio parcial lo duplica.
            assert state.connection.execute('SELECT COUNT(*) FROM bodies').fetchone()[0] == 1
            print(json.dumps({'stage': stage, 'authorized': sorted(expected), 'ok': True}), flush=True)
            if abrupt:
                # Caída después de los commits y las lecturas; no durante una escritura.
                os._exit(19)
    finally:
        state.close()


class PartialAuthorizedDelivery(unittest.TestCase):
    def scenario(self, mode, abrupt=False):
        with destinations_lab.EndpointAuthorization().participants() as (root, owner, a, b):
            (root / MARKER).write_text('spartakos\n')
            directories = [root / 'http-a', root / 'http-b']
            body, profile_message = revise(owner, 'Perfil de prueba parcial')
            for directory in directories:
                directory.mkdir(mode=0o700)
                (directory / MARKER).write_text('spartakos\n')
                (directory / 'profile.json').write_bytes(body)
            servers = [Provider(directory) for directory in directories]
            try:
                for server in servers:
                    server.start()
                cut = owner.makeEndRole(eid=a.pre, role=ROLE, allow=False, stamp=stamp(2))
                add = owner.makeEndRole(eid=b.pre, role=ROLE, stamp=stamp(3))
                partial, expected = {'cut-only': (['cut_a'], []), 'add-only': (['add_b'], ['a', 'b']),
                                     'neither': ([], ['a'])}[mode]
                fixture = {'owner': owner.pre, 'a': a.pre, 'b': b.pre,
                    'initial': [bytes(message).hex() for message in (
                        owner.makeOwnInception(), a.makeOwnInception(), b.makeOwnInception(), profile_message,
                        a.makeLocScheme(url=servers[0].url, stamp=stamp(0)),
                        b.makeLocScheme(url=servers[1].url, stamp=stamp(0)),
                        owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1)))],
                    'cut_a': bytes(cut).hex(), 'add_b': bytes(add).hex(),
                    'partial': partial, 'expected_partial': expected}
                (root / 'public-messages.json').write_text(json.dumps(fixture))
                for stage in ('initialize', 'partial', 'verify_partial', 'complete', 'verify'):
                    crash = abrupt and stage == 'partial'
                    args = [sys.executable, str(Path(__file__).resolve()), '--stage', stage, '--state-dir', str(root)]
                    if crash:
                        args.append('--abrupt')
                    result = subprocess.run(args, capture_output=True, text=True, timeout=20)
                    self.assertEqual(result.returncode, 19 if crash else 0, result.stderr[-1800:])
                    response = json.loads(result.stdout)
                    self.assertTrue(response['ok'])
                    self.assertEqual(response['stage'], stage)
                    self.assertEqual(response['authorized'], ['a'] if stage == 'initialize' else (
                        sorted(expected) if stage in ('partial', 'verify_partial') else ['b']))
            finally:
                for server in servers:
                    server.stop()

    def test_revocation_only_has_no_authorized_delivery_until_completion(self):
        self.scenario('cut-only')

    def test_authorization_only_keeps_both_providers_until_completion(self):
        self.scenario('add-only')

    def test_no_change_keeps_previous_provider_in_stale_view(self):
        self.scenario('neither')

    def test_abrupt_verifier_exit_after_partial_commits_resumes(self):
        self.scenario('add-only', abrupt=True)


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage')
    parser.add_argument('--state-dir', type=Path)
    parser.add_argument('--abrupt', action='store_true')
    args = parser.parse_args()
    if args.stage:
        if args.state_dir is None:
            parser.error('Falta --state-dir')
        run_stage(args.state_dir, args.stage, args.abrupt)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
