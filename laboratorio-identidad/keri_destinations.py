# SPDX-License-Identifier: AGPL-3.0-or-later
"""Declaraciones existentes de rol y dirección; no es un protocolo de traslado."""
from contextlib import contextmanager, ExitStack
import datetime
import os
from pathlib import Path
import tempfile
import unittest

from keri import kering
from keri.app import configing, habbing

ROLE = kering.Roles.agent
BASE = datetime.datetime(2026, 10, 27, 12, tzinfo=datetime.timezone.utc)


def stamp(offset):
    return (BASE + datetime.timedelta(seconds=offset)).isoformat(timespec="microseconds")


@contextmanager
def store(root, name):
    path = (root / name).resolve()
    path.mkdir(mode=0o700, exist_ok=True)
    cf = configing.Configer(name=name, base='lab', temp=False, headDirPath=str(path), reopen=True)
    hby = habbing.Habery(name=name, base='lab', temp=False, headDirPath=str(path), cf=cf)
    try:
        for resource in (hby.cf, hby.db, hby.ks):
            if not Path(resource.path).resolve().is_relative_to(path):
                raise RuntimeError('Recurso fuera del ensayo.')
        yield hby.habByName(name) or hby.makeHab(name=name)
    finally:
        hby.close()


def deliver(observer, *messages):
    for message in messages:
        observer.psr.parse(ims=bytearray(message))


def destinations(observer, owner):
    roles = observer.fetchRoleUrls(owner.pre, role=ROLE, enabled=False, allowed=True)
    return {eid: dict(urls) for _, providers in roles.items() for eid, urls in providers.items()}


class EndpointAuthorization(unittest.TestCase):
    @contextmanager
    def participants(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-destinations-') as path, ExitStack() as stack:
            root = Path(path)
            owner, a, b = [stack.enter_context(store(root, name)) for name in ('owner', 'provider-a', 'provider-b')]
            yield root, owner, a, b

    def setup_observer(self, observer, owner, a, b):
        for hab in (owner, a, b):
            deliver(observer, hab.makeOwnInception())
        deliver(observer,
            a.makeLocScheme(url='http://127.0.0.1:18081', stamp=stamp(0)),
            b.makeLocScheme(url='http://127.0.0.1:18082', stamp=stamp(0)))

    def test_provider_address_requires_owner_authorization(self):
        with self.participants() as (root, owner, a, b), store(root, 'observer') as observer:
            self.setup_observer(observer, owner, a, b)
            self.assertEqual(observer.fetchUrl(a.pre), 'http://127.0.0.1:18081')
            self.assertEqual(destinations(observer, owner), {})
            deliver(observer, owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1)))
            self.assertEqual(destinations(observer, owner), {a.pre: {'http': 'http://127.0.0.1:18081'}})
            self.assertNotIn(owner.pre, a.db.prefixes)
            self.assertNotIn(owner.pre, b.db.prefixes)

    def test_revoke_a_authorize_b_persists_and_rejects_old_replay(self):
        with self.participants() as (root, owner, a, b):
            old = owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1))
            with store(root, 'observer') as observer:
                self.setup_observer(observer, owner, a, b)
                deliver(observer, old,
                    owner.makeEndRole(eid=a.pre, role=ROLE, allow=False, stamp=stamp(2)),
                    owner.makeEndRole(eid=b.pre, role=ROLE, stamp=stamp(3)))
                self.assertEqual(destinations(observer, owner), {b.pre: {'http': 'http://127.0.0.1:18082'}})
            with store(root, 'observer') as observer:
                self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, a.pre), False)
                deliver(observer, old)
                self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, a.pre), False)
                self.assertEqual(destinations(observer, owner), {b.pre: {'http': 'http://127.0.0.1:18082'}})

    def test_provider_cannot_grant_itself_or_revoke_another_for_owner(self):
        with self.participants() as (root, owner, a, b), store(root, 'observer') as observer:
            self.setup_observer(observer, owner, a, b)
            deliver(observer, owner.makeEndRole(eid=b.pre, role=ROLE, stamp=stamp(1)))
            deliver(observer,
                a.reply(route='/end/role/add', data={'cid': owner.pre, 'role': ROLE, 'eid': a.pre}, stamp=stamp(2)),
                a.reply(route='/end/role/cut', data={'cid': owner.pre, 'role': ROLE, 'eid': b.pre}, stamp=stamp(3)),
                a.makeLocScheme(eid=b.pre, url='http://127.0.0.1:18999', stamp=stamp(4)))
            self.assertNotEqual(observer.fetchEndAllowed(owner.pre, ROLE, a.pre), True)
            self.assertEqual(destinations(observer, owner), {b.pre: {'http': 'http://127.0.0.1:18082'}})

    def test_role_allows_multiple_providers_without_automatic_replacement(self):
        with self.participants() as (root, owner, a, b), store(root, 'observer') as observer:
            self.setup_observer(observer, owner, a, b)
            deliver(observer,
                owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1)),
                owner.makeEndRole(eid=b.pre, role=ROLE, stamp=stamp(2)))
            self.assertEqual(set(destinations(observer, owner)), {a.pre, b.pre})

    def test_distinct_dates_converge_under_reverse_delivery(self):
        with self.participants() as (root, owner, a, b):
            add = owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1))
            cut = owner.makeEndRole(eid=a.pre, role=ROLE, allow=False, stamp=stamp(2))
            for name, messages in (('forward', (add, cut)), ('reverse', (cut, add))):
                with store(root, name) as observer:
                    self.setup_observer(observer, owner, a, b)
                    deliver(observer, *messages)
                    self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, a.pre), False)

    def test_equal_dates_keep_first_accepted_role_even_after_reopening(self):
        with self.participants() as (root, owner, a, b):
            add = owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1))
            cut = owner.makeEndRole(eid=a.pre, role=ROLE, allow=False, stamp=stamp(1))
            for name, messages, expected in (('add-first', (add, cut), True), ('cut-first', (cut, add), False)):
                with store(root, name) as observer:
                    self.setup_observer(observer, owner, a, b)
                    deliver(observer, *messages)
                    self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, a.pre), expected)
                with store(root, name) as observer:
                    deliver(observer, *reversed(messages))
                    self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, a.pre), expected)

    def test_new_signing_epoch_precedes_old_epoch_even_with_earlier_date(self):
        with self.participants() as (root, owner, a, b), store(root, 'observer') as observer:
            self.setup_observer(observer, owner, a, b)
            old_add = owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(100))
            deliver(observer, old_add)
            identity = owner.pre
            rotation = owner.rotate()
            deliver(observer, rotation)
            self.assertEqual(observer.kevers[identity].sn, 1)
            deliver(observer, owner.makeEndRole(eid=a.pre, role=ROLE, allow=False, stamp=stamp(1)))
            self.assertEqual(observer.fetchEndAllowed(identity, ROLE, a.pre), False)
            deliver(observer, old_add)
            self.assertEqual(observer.fetchEndAllowed(identity, ROLE, a.pre), False)
            self.assertEqual(owner.pre, identity)

    def test_rotation_does_not_automatically_revoke_existing_provider(self):
        with self.participants() as (root, owner, a, b), store(root, 'observer') as observer:
            self.setup_observer(observer, owner, a, b)
            deliver(observer, owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1)))
            deliver(observer, owner.rotate())
            self.assertEqual(observer.kevers[owner.pre].sn, 1)
            self.assertEqual(observer.fetchEndAllowed(owner.pre, ROLE, a.pre), True)
            self.assertEqual(set(destinations(observer, owner)), {a.pre})

    def test_unupdated_observer_keeps_old_authorization(self):
        with self.participants() as (root, owner, a, b), store(root, 'updated') as updated, store(root, 'stale') as stale:
            for observer in (updated, stale):
                self.setup_observer(observer, owner, a, b)
                deliver(observer, owner.makeEndRole(eid=a.pre, role=ROLE, stamp=stamp(1)))
            deliver(updated,
                owner.makeEndRole(eid=a.pre, role=ROLE, allow=False, stamp=stamp(2)),
                owner.makeEndRole(eid=b.pre, role=ROLE, stamp=stamp(3)))
            self.assertEqual(set(destinations(updated, owner)), {b.pre})
            self.assertEqual(set(destinations(stale, owner)), {a.pre})


if __name__ == '__main__':
    os.umask(0o077)
    unittest.main(verbosity=2)
