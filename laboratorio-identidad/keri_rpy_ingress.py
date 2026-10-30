# SPDX-License-Identifier: AGPL-3.0-or-later
"""Ingreso HTTP nativo de respuestas firmadas: cola y validación separadas."""
from contextlib import contextmanager
import os
import socket
import threading
import unittest
import urllib.request

import falcon
from hio.base import doing
from hio.core import http
from keri.app import indirecting
from keri.core import serdering
import keri_destinations as destinations_lab
from keri_destinations import ROLE, deliver, stamp, store
from keri_profile_http import NoRedirect


@contextmanager
def ingress_server(endpoint):
    app = falcon.App()
    app.add_route('/', endpoint)
    for _ in range(5):
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1', 0))
            port = reservation.getsockname()[1]
        server = indirecting.createHttpServer('127.0.0.1', port, app)
        if server.reopen():
            break
    else:
        raise RuntimeError('No se pudo abrir el servidor local.')
    stop, ready = threading.Event(), threading.Event()
    errors = []
    def run():
        scheduler = doing.Doist(tock=0.01, doers=[http.ServerDoer(server=server)])
        try:
            scheduler.enter()
            ready.set()
            while not stop.wait(0.005):
                scheduler.recur()
        except Exception as error:
            errors.append(type(error).__name__)
            ready.set()
        finally:
            scheduler.exit()
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    try:
        if not ready.wait(5) or errors:
            raise RuntimeError('No arrancó el ingreso nativo.')
        yield f'http://127.0.0.1:{port}/'
    finally:
        stop.set()
        thread.join(timeout=5)
        server.close()
        if thread.is_alive() or errors:
            raise RuntimeError('El servidor nativo no terminó correctamente.')


def post_reply(url, message):
    event = serdering.SerderKERI(raw=message)
    request = urllib.request.Request(url, data=event.raw, headers={
        'Content-Type': 'application/cesr+json',
        'CESR-ATTACHMENT': bytes(message[event.size:]).decode()})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    with opener.open(request, timeout=3) as response:
        return response.status


class SignedReplyIngress(unittest.TestCase):
    def scenario(self, mode):
        with destinations_lab.EndpointAuthorization().participants() as (root, owner, provider, _), store(root, 'observer') as observer:
            deliver(observer, owner.makeOwnInception(), provider.makeOwnInception())
            endpoint = indirecting.HttpEnd()
            grant = owner.makeEndRole(eid=provider.pre, role=ROLE, stamp=stamp(1))
            cut = owner.makeEndRole(eid=provider.pre, role=ROLE, allow=False, stamp=stamp(2))
            with ingress_server(endpoint) as url:
                self.assertEqual(post_reply(url, grant), 204)
                self.assertIsNone(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre))
                self.assertGreater(len(endpoint.rxbs), 0)
                observer.psr.parse(ims=endpoint.rxbs)
                self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), True)
                if mode == 'forged':
                    forged = provider.reply(route='/end/role/cut',
                        data={'cid': owner.pre, 'eid': provider.pre, 'role': ROLE}, stamp=stamp(3))
                    self.assertEqual(post_reply(url, forged), 204)
                    observer.psr.parse(ims=endpoint.rxbs)
                    self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), True)
                    return
                self.assertEqual(post_reply(url, cut), 204)
                self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), True)
                if mode == 'lost-queue':
                    endpoint.rxbs.clear()  # Pérdida instrumentada de la cola RAM, no caída real del proceso.
                    observer.psr.parse(ims=endpoint.rxbs)
                    self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), True)
                    self.assertEqual(post_reply(url, cut), 204)
                observer.psr.parse(ims=endpoint.rxbs)
                self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), False)
                self.assertEqual(post_reply(url, grant), 204)
                observer.psr.parse(ims=endpoint.rxbs)
                self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, provider.pre), False)

    def test_native_http_carries_grant_cut_and_old_replay(self):
        self.scenario('valid')

    def test_http_ack_does_not_make_wrong_signer_revocation_valid(self):
        self.scenario('forged')

    def test_acknowledged_inmemory_cut_can_be_lost_before_validation(self):
        self.scenario('lost-queue')


if __name__ == '__main__':
    os.umask(0o077)
    unittest.main(verbosity=2)
