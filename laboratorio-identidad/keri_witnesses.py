# SPDX-License-Identifier: AGPL-3.0-or-later
"""Recibos sintéticos de testigos: sin servidores ni política de producción."""
import os
import unittest

from hio.help import decking
from keri import core, kering
from keri.core import coring, eventing
from keri.db import basing


def fixture():
    owner, following = core.Signer(), core.Signer()
    witnesses = [core.Signer(transferable=False) for _ in range(3)]
    inception = eventing.incept(keys=[owner.verfer.qb64],
                               ndigs=[coring.Diger(ser=following.verfer.qb64b).qb64],
                               wits=[w.verfer.qb64 for w in witnesses], toad=2)
    return owner, witnesses, inception


def receipts(event, witnesses, indices):
    return [witnesses[i].sign(event.raw, index=i) for i in indices]


class WitnessReceipts(unittest.TestCase):
    def test_two_of_three_accepts_with_one_receipt_absent(self):
        owner, witnesses, event = fixture()
        with basing.openDB(name='spartakos-witness-quorum') as db:
            verifier = eventing.Kever(serder=event, sigers=[owner.sign(event.raw, index=0)],
                                     wigers=receipts(event, witnesses, [0, 2]), db=db, local=False, cues=decking.Deck())
            self.assertEqual(verifier.serder.said, event.said)
            self.assertEqual(verifier.toader.num, 2)

    def test_one_receipt_waits_then_retries_with_quorum(self):
        owner, witnesses, event = fixture()
        with basing.openDB(name='spartakos-witness-wait') as db:
            signatures = [owner.sign(event.raw, index=0)]
            with self.assertRaises(kering.MissingWitnessSignatureError):
                eventing.Kever(serder=event, sigers=signatures,
                               wigers=receipts(event, witnesses, [0]), db=db, local=False, cues=decking.Deck())
            # Reenvío explícito con recibos suficientes; no simula recuperación automática.
            verifier = eventing.Kever(serder=event, sigers=signatures,
                                     wigers=receipts(event, witnesses, [0, 1]), db=db, local=False, cues=decking.Deck())
            self.assertEqual(verifier.serder.said, event.said)

    def test_duplicate_receipt_does_not_count_twice(self):
        owner, witnesses, event = fixture()
        with basing.openDB(name='spartakos-witness-duplicate') as db:
            receipt = witnesses[0].sign(event.raw, index=0)
            with self.assertRaises(kering.MissingWitnessSignatureError):
                eventing.Kever(serder=event, sigers=[owner.sign(event.raw, index=0)],
                               wigers=[receipt, receipt], db=db, local=False, cues=decking.Deck())

    def test_impostor_does_not_replace_missing_witness(self):
        owner, witnesses, event = fixture()
        with basing.openDB(name='spartakos-witness-impostor') as db:
            fake = core.Signer(transferable=False).sign(event.raw, index=1)
            with self.assertRaises(kering.MissingWitnessSignatureError):
                eventing.Kever(serder=event, sigers=[owner.sign(event.raw, index=0)],
                               wigers=receipts(event, witnesses, [0]) + [fake], db=db, local=False, cues=decking.Deck())

    def test_remote_interaction_waits_without_replacing_accepted_state(self):
        owner, witnesses, inception = fixture()
        with basing.openDB(name='spartakos-witness-update') as db:
            verifier = eventing.Kever(serder=inception, sigers=[owner.sign(inception.raw, index=0)],
                                     wigers=receipts(inception, witnesses, [0, 1]), db=db, local=False, cues=decking.Deck())
            event = eventing.interact(pre=inception.pre, dig=inception.said, sn=1)
            with self.assertRaises(kering.MissingWitnessSignatureError):
                verifier.update(serder=event, sigers=[owner.sign(event.raw, index=0)],
                                wigers=receipts(event, witnesses, [0]), local=False)
            self.assertEqual(verifier.sn, 0)
            self.assertEqual(verifier.serder.said, inception.said)
            verifier.update(serder=event, sigers=[owner.sign(event.raw, index=0)],
                            wigers=receipts(event, witnesses, [0, 2]), local=False)
            self.assertEqual(verifier.sn, 1)
            self.assertEqual(verifier.serder.said, event.said)

    def test_isolated_observers_can_accept_different_quorate_branches(self):
        owner, witnesses, inception = fixture()
        with basing.openDB(name='spartakos-observer-a') as db_a, basing.openDB(name='spartakos-observer-b') as db_b:
            observers = [eventing.Kevery(db=db, local=False) for db in (db_a, db_b)]
            branches = [eventing.interact(pre=inception.pre, dig=inception.said, sn=1,
                                         data=[{'branch': name}]) for name in ('a', 'b')]
            for observer, branch, indices in zip(observers, branches, ([0, 1], [1, 2])):
                observer.processEvent(serder=inception, sigers=[owner.sign(inception.raw, index=0)],
                                      wigers=receipts(inception, witnesses, [0, 1]))
                observer.processEvent(serder=branch, sigers=[owner.sign(branch.raw, index=0)],
                                      wigers=receipts(branch, witnesses, indices))
                self.assertEqual(observer.kevers[inception.pre].serder.said, branch.said)
            self.assertNotEqual(branches[0].said, branches[1].said)
            # El testigo 1 ha firmado ambas ramas. Solo se detecta al recibir la otra.
            for observer, other, indices in zip(observers, reversed(branches), ([1, 2], [0, 1])):
                with self.assertRaises(kering.LikelyDuplicitousError):
                    observer.processEvent(serder=other, sigers=[owner.sign(other.raw, index=0)],
                                          wigers=receipts(other, witnesses, indices))
            for observer, branch in zip(observers, branches):
                self.assertEqual(observer.kevers[inception.pre].serder.said, branch.said)

    def test_conflicting_events_are_flagged_without_replacing_history(self):
        owner, witnesses, inception = fixture()
        with basing.openDB(name='spartakos-witness-conflict') as db:
            processor = eventing.Kevery(db=db, local=False, cues=decking.Deck())
            processor.processEvent(serder=inception, sigers=[owner.sign(inception.raw, index=0)],
                                   wigers=receipts(inception, witnesses, [0, 1]))
            first = eventing.interact(pre=inception.pre, dig=inception.said, sn=1, data=[{'branch': 'a'}])
            other = eventing.interact(pre=inception.pre, dig=inception.said, sn=1, data=[{'branch': 'b'}])
            processor.processEvent(serder=first, sigers=[owner.sign(first.raw, index=0)],
                                   wigers=receipts(first, witnesses, [0, 1]))
            # Caso adversarial: los mismos testigos firman dos ramas incompatibles.
            with self.assertRaises(kering.LikelyDuplicitousError):
                processor.processEvent(serder=other, sigers=[owner.sign(other.raw, index=0)],
                                       wigers=receipts(other, witnesses, [0, 1]))
            self.assertEqual(processor.kevers[inception.pre].serder.said, first.said)


if __name__ == '__main__':
    os.umask(0o077)
    unittest.main(verbosity=2)
