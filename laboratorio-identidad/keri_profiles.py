# SPDX-License-Identifier: AGPL-3.0-or-later
"""Vinculación experimental de perfil público con eventos KERI; sin traslado."""
import json
import os
import unittest

from keri import core, kering
from keri.core import coring, eventing, serdering
from keri.db import basing, dbing
from keri_smoke import controller

KIND = 'spartakos-public-profile-lab-v1'
ANCHOR = 'spartakos_profile_lab_v1'


def profile_id(owner):
    return owner + ':profile'


def profile_bytes(owner, name):
    # Serialización del fixture; no se afirma canonicalización interoperable.
    return json.dumps({'kind': KIND, 'id': profile_id(owner), 'display_name': name},
                      ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def profile_event(owner, previous, sequence, body):
    return eventing.interact(pre=owner, dig=previous, sn=sequence,
        data=[{ANCHOR: {'id': profile_id(owner), 'd': coring.Diger(ser=body).qb64}}])


def validated_revisions(db, owner):
    revisions = []
    for digest in db.getKelIter(owner):
        raw = db.getEvt(dbing.dgKey(owner, bytes(digest)))
        event = serdering.SerderKERI(raw=bytes(raw))
        accepted = db.getKeLast(dbing.snKey(owner, event.sn))
        if accepted is None or bytes(accepted).decode() != event.said:
            continue
        for datum in event.ked.get('a', []):
            anchor = datum.get(ANCHOR) if isinstance(datum, dict) else None
            if isinstance(anchor, dict) and anchor.get('id') == profile_id(owner):
                revisions.append((event.sn, event.said, anchor['d']))
    return sorted(revisions)


def inspect_copy(db, owner, body):
    data = json.loads(body)
    if set(data) != {'kind', 'id', 'display_name'} or data['kind'] != KIND or data['id'] != profile_id(owner):
        raise ValueError('No es el perfil público esperado.')
    digest = coring.Diger(ser=body).qb64
    revisions = validated_revisions(db, owner)
    matches = [item for item in revisions if item[2] == digest]
    if not matches:
        raise ValueError('No consta un anclaje aceptado del titular para estos bytes.')
    revision = matches[-1]
    return {'id': data['id'], 'sequence': revision[0], 'event': revision[1],
            'head_in_this_view': revision == revisions[-1], 'globally_current': None}


class PublicProfileBinding(unittest.TestCase):
    def anchor(self, verifier, signer, body):
        event = profile_event(verifier.prefixer.qb64, verifier.serder.said, verifier.sn + 1, body)
        verifier.update(serder=event, sigers=[signer.sign(event.raw, index=0)])
        return event

    def test_two_storage_copies_preserve_identity_and_authority(self):
        with basing.openDB(name='spartakos-profile-copies') as db:
            verifier, owner, _, _ = controller(db)
            identifier = verifier.prefixer.qb64
            body = profile_bytes(identifier, 'Persona ficticia')
            event = self.anchor(verifier, owner, body)
            # A y B son copias de bytes; no servidores de alojamiento ejecutados.
            copy_a, copy_b = bytes(body), bytes(bytearray(body))
            result = inspect_copy(db, identifier, copy_b)
            self.assertEqual(result, inspect_copy(db, identifier, copy_a))
            self.assertEqual(result['event'], event.said)
            self.assertTrue(result['head_in_this_view'])
            self.assertIsNone(result['globally_current'])

    def test_provider_modification_and_digest_without_anchor_are_rejected(self):
        with basing.openDB(name='spartakos-profile-tampering') as db:
            verifier, owner, _, _ = controller(db)
            identifier = verifier.prefixer.qb64
            body = profile_bytes(identifier, 'Original ficticio')
            self.anchor(verifier, owner, body)
            altered = profile_bytes(identifier, 'Cambio ajeno')
            # Calcular una huella correcta del contenido alterado no concede autoridad.
            self.assertTrue(coring.Diger(ser=altered).verify(ser=altered))
            with self.assertRaises(ValueError):
                inspect_copy(db, identifier, altered)
            impostor = core.Signer()
            event = profile_event(identifier, verifier.serder.said, verifier.sn + 1, altered)
            before = verifier.serder.said
            with self.assertRaises(kering.ValidationError):
                verifier.update(serder=event, sigers=[impostor.sign(event.raw, index=0)])
            self.assertEqual(verifier.serder.said, before)
            with self.assertRaises(ValueError):
                inspect_copy(db, identifier, altered)

    def test_old_valid_copy_is_history_after_new_revision(self):
        with basing.openDB(name='spartakos-profile-history') as db:
            verifier, owner, _, _ = controller(db)
            identifier = verifier.prefixer.qb64
            old, new = [profile_bytes(identifier, name) for name in ('Uno', 'Dos')]
            self.anchor(verifier, owner, old)
            self.anchor(verifier, owner, new)
            self.assertFalse(inspect_copy(db, identifier, old)['head_in_this_view'])
            self.assertTrue(inspect_copy(db, identifier, new)['head_in_this_view'])
            # Conocer el nuevo anclaje no permite reconstruir su cuerpo desde una copia vieja.
            self.assertNotEqual(coring.Diger(ser=old).qb64, validated_revisions(db, identifier)[-1][2])

    def test_wrong_profile_identity_is_rejected_even_if_bytes_are_anchored(self):
        with basing.openDB(name='spartakos-profile-owner') as db:
            verifier, owner, _, _ = controller(db)
            identifier = verifier.prefixer.qb64
            body = profile_bytes(core.Signer().verfer.qb64, 'Otra identidad')
            self.anchor(verifier, owner, body)
            with self.assertRaises(ValueError):
                inspect_copy(db, identifier, body)

    def test_rotation_keeps_profile_id_and_previous_key_cannot_update(self):
        with basing.openDB(name='spartakos-profile-rotation') as db:
            verifier, previous, current, future = controller(db)
            identifier = verifier.prefixer.qb64
            body = profile_bytes(identifier, 'Antes')
            self.anchor(verifier, previous, body)
            rotation = eventing.rotate(pre=identifier, keys=[current.verfer.qb64],
                dig=verifier.serder.said, sn=verifier.sn + 1,
                ndigs=[coring.Diger(ser=future.verfer.qb64b).qb64])
            verifier.update(serder=rotation, sigers=[current.sign(rotation.raw, index=0)])
            changed = profile_bytes(identifier, 'Después')
            event = profile_event(identifier, verifier.serder.said, verifier.sn + 1, changed)
            with self.assertRaises(kering.ValidationError):
                verifier.update(serder=event, sigers=[previous.sign(event.raw, index=0)])
            verifier.update(serder=event, sigers=[current.sign(event.raw, index=0)])
            self.assertEqual(inspect_copy(db, identifier, changed)['id'], profile_id(identifier))
            self.assertFalse(inspect_copy(db, identifier, body)['head_in_this_view'])

    def test_stale_view_cannot_claim_global_freshness(self):
        with basing.openDB(name='spartakos-profile-stale') as db_a, basing.openDB(name='spartakos-profile-updated') as db_b:
            first, owner, _, _ = controller(db_a)
            inception = first.serder
            second = eventing.Kever(serder=inception, sigers=[owner.sign(inception.raw, index=0)], db=db_b)
            identifier = inception.pre
            old, new = [profile_bytes(identifier, name) for name in ('Uno', 'Dos')]
            event = self.anchor(first, owner, old)
            second.update(serder=event, sigers=[owner.sign(event.raw, index=0)])
            self.anchor(second, owner, new)
            self.assertTrue(inspect_copy(db_a, identifier, old)['head_in_this_view'])
            self.assertFalse(inspect_copy(db_b, identifier, old)['head_in_this_view'])
            self.assertIsNone(inspect_copy(db_a, identifier, old)['globally_current'])

    def test_valid_anchors_do_not_resolve_conflicting_histories(self):
        with basing.openDB(name='spartakos-profile-branch-a') as db_a, basing.openDB(name='spartakos-profile-branch-b') as db_b:
            initial, owner, _, _ = controller(db_a)
            inception = initial.serder
            processors = [eventing.Kevery(db=db, local=False) for db in (db_a, db_b)]
            processors[1].processEvent(serder=inception, sigers=[owner.sign(inception.raw, index=0)])
            identifier = inception.pre
            bodies = [profile_bytes(identifier, name) for name in ('Rama A', 'Rama B')]
            events = [profile_event(identifier, inception.said, 1, body) for body in bodies]
            for processor, event in zip(processors, events):
                processor.processEvent(serder=event, sigers=[owner.sign(event.raw, index=0)])
            for db, body in zip((db_a, db_b), bodies):
                self.assertTrue(inspect_copy(db, identifier, body)['head_in_this_view'])
                self.assertIsNone(inspect_copy(db, identifier, body)['globally_current'])
            for processor, other in zip(processors, reversed(events)):
                with self.assertRaises(kering.LikelyDuplicitousError):
                    processor.processEvent(serder=other, sigers=[owner.sign(other.raw, index=0)])
            self.assertNotEqual(processors[0].kevers[identifier].serder.said,
                                processors[1].kevers[identifier].serder.said)


if __name__ == '__main__':
    os.umask(0o077)
    unittest.main(verbosity=2)
