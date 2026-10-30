# SPDX-License-Identifier: AGPL-3.0-or-later
"""Entrega HTTP local de perfil público; sin traslado de autoridad ni claves."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from urllib.parse import urlparse

from keri import core
from keri.core import eventing, serdering
from keri.db import basing
from keri_profiles import profile_bytes, profile_event, inspect_copy
from keri_profile_state import ProfileState

MARKER = 'SOLO-ENSAYO-SINTETICO'


def serve(root):
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            files = {'/profile': 'profile.json', '/proof': 'proof.json'}
            name = files.get(self.path)
            if name is None or not (root / name).is_file():
                self.send_error(404)
                return
            body = (root / name).read_bytes()
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


class Provider:
    def __init__(self, root):
        self.root, self.process = root, None

    def start(self):
        self.process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--serve', str(self.root)],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not select.select([self.process.stdout], [], [], 10)[0]:
            self.stop()
            raise RuntimeError('El proveedor no arrancó.')
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


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def fetch(url):
    parsed = urlparse(url)
    if parsed.scheme != 'http' or parsed.hostname != '127.0.0.1':
        raise ValueError('Solo se admiten servicios locales del ensayo.')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(url, timeout=3) as response:
        body = response.read(1024 * 1024 + 1)
        if len(body) > 1024 * 1024:
            raise ValueError('Respuesta demasiado grande para el ensayo.')
        return body


def verify(root, url, expected_owner, bootstrap):
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    db = basing.Baser(name='profile-observer', headDirPath=str(root), temp=False, reopen=True)
    state = ProfileState(root)
    try:
        if not Path(db.path).resolve().is_relative_to(root.resolve()):
            raise RuntimeError('Almacén fuera del ensayo.')
        kvy = eventing.Kevery(db=db, local=False)
        if bootstrap:
            proof = json.loads(fetch(url + '/proof'))
            events = [serdering.SerderKERI(raw=item['event'].encode()) for item in proof]
            if not events or any(event.pre != expected_owner for event in events):
                raise ValueError('La prueba no corresponde al titular esperado.')
            for item, event in zip(proof, events):
                kvy.processEvent(serder=event, sigers=[core.Siger(qb64=item['signature'])])
        body = fetch(url + '/profile')
        state.remember(db, expected_owner, body)
        result = state.view(db, expected_owner, body)
        print(json.dumps({'accepted_copy': True, 'id': result['id'], 'sequence': result['sequence'],
                          'head_in_this_view': result['head_in_this_view'],
                          'confirmation_blocked': result['confirmation_blocked'],
                          'globally_current': result['globally_current']}))
    finally:
        state.close()
        db.close()


class ProfileHttpDelivery(unittest.TestCase):
    def scenario(self, mode):
        with tempfile.TemporaryDirectory(prefix='spartakos-profile-http-') as path:
            root = Path(path)
            directories = {name: root / name for name in ('a', 'b', 'observer', 'fresh-observer')}
            for directory in directories.values():
                directory.mkdir(mode=0o700)
                (directory / MARKER).write_text('spartakos\n')
            # Las claves solo viven en este coordinador sintético; no se escriben en A/B.
            owner, next_key = core.Signer(), core.Signer()
            inception = eventing.incept(keys=[owner.verfer.qb64], ndigs=[core.Diger(ser=next_key.verfer.qb64b).qb64])
            body = profile_bytes(inception.pre, 'Perfil público ficticio')
            first = profile_event(inception.pre, inception.said, 1, body)
            events = [inception, first]
            if mode == 'stale':
                changed = profile_bytes(inception.pre, 'Perfil público actualizado')
                events.append(profile_event(inception.pre, first.said, 2, changed))
            proof = [{'event': event.raw.decode(), 'signature': owner.sign(event.raw, index=0).qb64} for event in events]
            for name in ('a', 'b'):
                (directories[name] / 'profile.json').write_bytes(changed if mode == 'stale' and name == 'a' else body)
                (directories[name] / 'proof.json').write_text(json.dumps(proof))
            a, b = Provider(directories['a']), Provider(directories['b'])
            def check(directory, provider, bootstrap=False, rejected=False, expected_error=None):
                args = [sys.executable, str(Path(__file__).resolve()), '--verify', str(directories[directory]),
                        '--url', provider.url, '--owner', inception.pre]
                if bootstrap:
                    args.append('--bootstrap')
                result = subprocess.run(args, capture_output=True, text=True, timeout=20)
                if rejected:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, '')
                    self.assertIn(expected_error or 'ValueError: No consta un anclaje aceptado del titular para estos bytes.', result.stderr)
                    return None
                self.assertEqual(result.returncode, 0, result.stderr[-1500:])
                return json.loads(result.stdout)
            try:
                a.start()
                b.start()
                initial = check('observer', a, bootstrap=True)
                a.stop()
                with self.assertRaises(urllib.error.URLError):
                    fetch(a.url + '/profile')
                if mode == 'tampered':
                    (directories['b'] / 'profile.json').write_bytes(profile_bytes(inception.pre, 'Cambio ajeno'))
                    check('observer', b, rejected=True)
                    (directories['b'] / 'profile.json').write_bytes(body)
                    self.assertEqual(check('observer', b)['id'], initial['id'])
                elif mode == 'wrong-owner':
                    impostor, later = core.Signer(), core.Signer()
                    fake_inception = eventing.incept(keys=[impostor.verfer.qb64],
                        ndigs=[core.Diger(ser=later.verfer.qb64b).qb64])
                    fake_body = profile_bytes(fake_inception.pre, 'Identidad del proveedor')
                    fake_profile = profile_event(fake_inception.pre, fake_inception.said, 1, fake_body)
                    fake_proof = [{'event': item.raw.decode(), 'signature': impostor.sign(item.raw, index=0).qb64}
                                  for item in (fake_inception, fake_profile)]
                    (directories['b'] / 'profile.json').write_bytes(fake_body)
                    (directories['b'] / 'proof.json').write_text(json.dumps(fake_proof))
                    check('fresh-observer', b, bootstrap=True, rejected=True,
                          expected_error='ValueError: La prueba no corresponde al titular esperado.')
                elif mode == 'no-authority':
                    # El cuerpo correcto sin historia validada no se acepta en un verificador nuevo.
                    check('fresh-observer', b, rejected=True)
                    self.assertEqual(check('fresh-observer', b, bootstrap=True)['id'], initial['id'])
                else:
                    recovered = check('observer', b)
                    self.assertEqual(recovered['id'], initial['id'])
                    self.assertIsNone(recovered['globally_current'])
                    self.assertEqual(recovered['head_in_this_view'], mode != 'stale')
                    if mode == 'recovery':
                        self.assertEqual(recovered['sequence'], initial['sequence'])
                        self.assertEqual(check('fresh-observer', b, bootstrap=True)['id'], initial['id'])
            finally:
                a.stop()
                b.stop()

    def test_delivery_from_b_with_a_off_and_new_verifier(self):
        self.scenario('recovery')

    def test_changed_body_from_b_is_rejected(self):
        self.scenario('tampered')

    def test_body_without_validated_authority_is_rejected(self):
        self.scenario('no-authority')

    def test_b_cannot_replace_pinned_owner_with_its_own_valid_identity(self):
        self.scenario('wrong-owner')

    def test_old_body_from_b_is_historical_in_updated_view(self):
        self.scenario('stale')


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', type=Path)
    parser.add_argument('--verify', type=Path)
    parser.add_argument('--url')
    parser.add_argument('--owner')
    parser.add_argument('--bootstrap', action='store_true')
    args = parser.parse_args()
    if args.serve:
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
        serve(args.serve)
    elif args.verify:
        if not args.url or not args.owner:
            parser.error('Faltan --url o --owner')
        verify(args.verify, args.url, args.owner, args.bootstrap)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
