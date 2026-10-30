# SPDX-License-Identifier: AGPL-3.0-or-later
"""Composición experimental de rol autorizado y entrega HTTP de perfil público."""
import os
import sys
import unittest
import urllib.error
from unittest.mock import patch

import keri_destinations as destinations_lab
from keri_destinations import ROLE, deliver, stamp, store
from keri_profile_http import Provider, fetch, MARKER
from keri_profile_state import ProfileState
from keri_profiles import ANCHOR, profile_id, profile_bytes, inspect_copy
from keri import core


def read_authorized(observer, state, owner_id, provider_id):
    # agent solo se interpreta como proveedor de entrega en este ensayo;
    # no concede escritura del perfil ni prueba actualidad global.
    if observer.fetchEndAllowed(owner_id, ROLE, provider_id) is not True:
        raise PermissionError('El proveedor no está autorizado en esta vista.')
    address = observer.fetchUrl(provider_id)
    if not address:
        raise ValueError('No hay dirección verificada del proveedor.')
    body = fetch(address + '/profile')
    state.remember(observer.db, owner_id, body)
    return state.view(observer.db, owner_id, body)


def revise(owner, name):
    body = profile_bytes(owner.pre, name)
    message = owner.interact(data=[{ANCHOR: {'id': profile_id(owner.pre),
                                           'd': core.Diger(ser=body).qb64}}])
    return body, message


class AuthorizedDelivery(unittest.TestCase):
    def scenario(self, mode):
        with destinations_lab.EndpointAuthorization().participants() as (root, owner, a, b):
            directories = [root / 'http-a', root / 'http-b']
            for directory in directories:
                directory.mkdir(mode=0o700)
                (directory / MARKER).write_text('spartakos\n')
            first, first_message = revise(owner, 'Perfil inicial')
            for directory in directories:
                (directory / 'profile.json').write_bytes(first)
            servers = [Provider(directory) for directory in directories]
            state = ProfileState(root)
            try:
                for server in servers:
                    server.start()
                with store(root, 'observer') as observer:
                    for identity in (owner, a, b):
                        deliver(observer, identity.makeOwnInception())
                    deliver(observer, first_message,
                        a.makeLocScheme(url=servers[0].url, stamp=stamp(0)),
                        b.makeLocScheme(url=servers[1].url, stamp=stamp(0)))
                    if mode == 'unauthorized':
                        # La dirección es conocida, pero no hay autorización.
                        self.assertEqual(observer.fetchUrl(b.pre), servers[1].url)
                        with patch.object(sys.modules[__name__], 'fetch', side_effect=AssertionError('No debe abrir HTTP')) as blocked_fetch:
                            with self.assertRaises(PermissionError):
                                read_authorized(observer, state, owner.pre, b.pre)
                            blocked_fetch.assert_not_called()
                        deliver(observer, owner.makeEndRole(eid=b.pre, role=ROLE, stamp=stamp(1)))
                        result = read_authorized(observer, state, owner.pre, b.pre)
                        self.assertTrue(result['head_in_this_view'])
                        self.assertIsNone(result['globally_current'])
                        return
                    deliver(observer, owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1)))
                    initial = read_authorized(observer, state, owner.pre, a.pre)
                    servers[0].stop()
                    with self.assertRaises(urllib.error.URLError):
                        read_authorized(observer, state, owner.pre, a.pre)
                    deliver(observer,
                        owner.makeEndRole(eid=a.pre, role=ROLE, allow=False, stamp=stamp(2)),
                        owner.makeEndRole(eid=b.pre, role=ROLE, stamp=stamp(3)))
                    with self.assertRaises(PermissionError):
                        read_authorized(observer, state, owner.pre, a.pre)
                    result = read_authorized(observer, state, owner.pre, b.pre)
                    self.assertEqual(result['id'], initial['id'])
                    self.assertEqual(result['sequence'], initial['sequence'])
                    if mode == 'update':
                        changed, message = revise(owner, 'Perfil actualizado con A apagado')
                        (directories[1] / 'profile.json').write_bytes(changed)
                        deliver(observer, message)
                        result = read_authorized(observer, state, owner.pre, b.pre)
                        self.assertEqual(result['sequence'], initial['sequence'] + 1)
                        self.assertTrue(result['head_in_this_view'])
                        servers[0].start()
                        deliver(observer, a.makeLocScheme(url=servers[0].url, stamp=stamp(4)))
                        with self.assertRaises(PermissionError):
                            read_authorized(observer, state, owner.pre, a.pre)
                        old_body = fetch(servers[0].url + '/profile')
                        self.assertFalse(inspect_copy(observer.db, owner.pre, old_body)['head_in_this_view'])
                # Reabrir la vista persistida: el endpoint anterior no recupera su rol.
                with store(root, 'observer') as observer:
                    with self.assertRaises(PermissionError):
                        read_authorized(observer, state, owner.pre, a.pre)
                    result = read_authorized(observer, state, owner.pre, b.pre)
                    self.assertEqual(result['sequence'], 2 if mode == 'update' else 1)
                    self.assertIsNone(result['globally_current'])
            finally:
                state.close()
                for server in servers:
                    server.stop()

    def test_known_address_without_owner_role_is_rejected_before_http(self):
        self.scenario('unauthorized')

    def test_revoked_a_and_authorized_b_resolve_and_deliver_with_a_off(self):
        self.scenario('handover')

    def test_new_profile_at_b_and_returning_a_do_not_restore_old_role(self):
        self.scenario('update')


if __name__ == '__main__':
    os.umask(0o077)
    unittest.main(verbosity=2)
