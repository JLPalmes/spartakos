# SPDX-License-Identifier: AGPL-3.0-or-later
"""Prueba acotada del endpoint OOBI nativo; descubrimiento no equivale a sincronización."""
from contextlib import contextmanager, ExitStack
import os
import threading
from pathlib import Path
import tempfile
import unittest
from wsgiref.simple_server import make_server, WSGIRequestHandler

import falcon
from keri_destinations import ROLE, deliver, stamp, store
from keri.end import ending
from keri_profile_http import fetch


class QuietHandler(WSGIRequestHandler):
    def log_message(self, *args):
        pass


@contextmanager
def oobi_server(owner, environment):
    app = falcon.App()
    app.add_route('/oobi/{aid}/{role}', ending.OOBIEnd(hby=environment))
    server = make_server('127.0.0.1', 0, app, handler_class=QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/oobi/{owner.pre}/{ROLE}'
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        if thread.is_alive():
            raise RuntimeError('El servidor de prueba no terminó.')


class NativeOobiTransport(unittest.TestCase):
    def scenario(self, revoke):
        with tempfile.TemporaryDirectory(prefix='spartakos-oobi-') as path, ExitStack() as stack:
            root = Path(path)
            environment, owner = stack.enter_context(store(root, 'owner', with_environment=True))
            provider = stack.enter_context(store(root, 'provider'))
            observer = stack.enter_context(store(root, 'observer'))
            # Precondición explícita: el observador ya conoce al proveedor.
            # Se aísla el transporte de rol/dirección del bootstrap recursivo.
            deliver(observer, provider.makeOwnInception())
            grant = owner.makeEndRole(eid=provider.pre, role=ROLE, stamp=stamp(1))
            deliver(owner, provider.makeOwnInception(),
                    provider.makeLocScheme(url='http://127.0.0.1:18881', stamp=stamp(0)), grant)
            self.assertIsNone(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre))
            with oobi_server(owner, environment) as url:
                messages = fetch(url)
                self.assertGreater(len(messages), 0)
                deliver(observer, messages)
                self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), True)
                self.assertEqual(observer.fetchUrl(provider.pre), 'http://127.0.0.1:18881')
                self.assertIn(owner.pre, observer.kevers)
                if revoke:
                    deliver(owner, owner.makeEndRole(eid=provider.pre, role=ROLE, allow=False, stamp=stamp(2)))
                    self.assertEqual(owner.fetchEndAllowed(owner.pre, ROLE, provider.pre), False)
                    # Medición del comportamiento nativo; no se añade un parche o un corte simulado.
                    deliver(observer, fetch(url))
                    self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), True)
                    # La respuesta de introducción no transportó el corte. El mensaje nativo sí lo hace.
                    deliver(observer, owner.makeEndRole(eid=provider.pre, role=ROLE, allow=False, stamp=stamp(2)))
                    self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), False)

    def test_native_http_response_transports_owner_role_and_provider_location(self):
        self.scenario(revoke=False)

    def test_polling_oobi_does_not_propagate_removed_role_in_this_configuration(self):
        self.scenario(revoke=True)


if __name__ == '__main__':
    os.umask(0o077)
    unittest.main(verbosity=2)
