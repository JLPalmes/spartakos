# SPDX-License-Identifier: AGPL-3.0-or-later
"""Caducidad y evidencia de contradicción en almacenes sintéticos persistidos."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from keri import core, kering
from keri.core import eventing, serdering
from keri.db import basing, dbing
from keri.help import helping
from keri_witnesses import fixture, receipts


def worker(root, phase):
    root = root.resolve()
    if (root / 'SOLO-ENSAYO-SINTETICO').read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    data = json.loads((root / 'events.json').read_text())
    events = [serdering.SerderKERI(raw=item['event'].encode()) for item in data]
    db = basing.Baser(name='lifecycle', headDirPath=str(root), temp=False, reopen=True)
    try:
        if not Path(db.path).resolve().is_relative_to(root):
            raise RuntimeError('Almacén fuera del ensayo.')
        kvy = eventing.Kevery(db=db, local=False)
        def process(index, full=True):
            item = data[index]
            kvy.processEvent(serder=events[index],
                sigers=[core.Siger(qb64=s) for s in item['owner']],
                wigers=[core.Siger(qb64=s) for s in item['witnesses'][:None if full else 1]])
        event = events[-1]
        key = dbing.snKey(event.pre, event.sn)
        digest_key = dbing.dgKey(event.pre, event.said)
        if phase == 'store_pending':
            process(0)
            try:
                process(1, full=False)
            except kering.MissingWitnessSignatureError:
                pass
            else:
                raise AssertionError('Se aceptó sin suficientes recibos.')
            assert db.cntPwes(key) == 1
        elif phase == 'expire_pending':
            assert db.cntPwes(key) == 1
            original = helping.fromIso8601(bytes(db.getDts(digest_key)))
            for seconds in (kvy.TimeoutPWE - 1, kvy.TimeoutPWE):
                with patch('keri.core.eventing.helping.nowUTC', return_value=original + datetime.timedelta(seconds=seconds)):
                    kvy.processEscrowPartialWigs()
                assert db.cntPwes(key) == 1
                assert kvy.kevers[event.pre].sn == 0
            with patch('keri.core.eventing.helping.nowUTC', return_value=original + datetime.timedelta(seconds=kvy.TimeoutPWE + 1)):
                kvy.processEscrowPartialWigs()
            assert db.cntPwes(key) == 0
            assert kvy.kevers[event.pre].sn == 0
            assert bytes(db.getEvt(digest_key)) == event.raw
            # La caducidad de cola no equivale a revocación criptográfica del evento.
            process(1)
            assert kvy.kevers[event.pre].serder.said == event.said
        elif phase == 'verify_pending':
            assert db.cntPwes(key) == 0
            assert kvy.kevers[event.pre].serder.said == event.said
        elif phase == 'store_branch':
            process(0)
            process(1)
            assert db.cntLdes(key) == 0
            assert kvy.kevers[event.pre].serder.said == events[1].said
        elif phase == 'receive_conflict':
            assert kvy.kevers[event.pre].serder.said == events[1].said
            try:
                process(2)
            except kering.LikelyDuplicitousError:
                pass
            else:
                raise AssertionError('No se detectó la otra rama tras reiniciar.')
            assert db.cntLdes(key) == 1
            assert kvy.kevers[event.pre].serder.said == events[1].said
        elif phase == 'store_conflict':
            process(0)
            process(1)
            try:
                process(2)
            except kering.LikelyDuplicitousError:
                pass
            else:
                raise AssertionError('No se detectó la contradicción.')
            assert db.cntLdes(key) == 1
            assert kvy.kevers[event.pre].serder.said == events[1].said
        elif phase in ('reload_conflict', 'expire_conflict', 'verify_conflict'):
            assert kvy.kevers[event.pre].serder.said == events[1].said
            assert bytes(db.getEvt(digest_key)) == event.raw
            stored = [core.Siger(qb64b=bytes(sig)) for sig in db.getSigs(digest_key)]
            assert stored and all(core.Verfer(qb64=events[0].ked['k'][0]).verify(sig.raw, event.raw) for sig in stored)
            if phase == 'reload_conflict':
                assert db.cntLdes(key) == 1
                kvy.processEscrowDuplicitous()
                assert db.cntLdes(key) == 1
            elif phase == 'expire_conflict':
                assert db.cntLdes(key) == 1
                original = helping.fromIso8601(bytes(db.getDts(digest_key)))
                with patch('keri.core.eventing.helping.nowUTC', return_value=original + datetime.timedelta(seconds=kvy.TimeoutLDE + 1)):
                    kvy.processEscrowDuplicitous()
                assert db.cntLdes(key) == 0
            else:
                assert db.cntLdes(key) == 0
            assert kvy.kevers[event.pre].serder.said == events[1].said
        else:
            raise ValueError('Etapa no reconocida.')
        print(json.dumps({'phase': phase, 'ok': True}))
    finally:
        db.close()


class EscrowLifecycle(unittest.TestCase):
    def scenario(self, conflict):
        owner, witnesses, inception = fixture()
        first = eventing.interact(pre=inception.pre, dig=inception.said, sn=1, data=[{'branch': 'a'}])
        other = eventing.interact(pre=inception.pre, dig=inception.said, sn=1, data=[{'branch': 'b'}])
        events = [inception, first, other] if conflict else [inception, first]
        data = [{'event': event.raw.decode(), 'owner': [owner.sign(event.raw, index=0).qb64],
                 'witnesses': [sig.qb64 for sig in receipts(event, witnesses, [0, 1])]} for event in events]
        with tempfile.TemporaryDirectory(prefix='spartakos-lifecycle-') as path:
            root = Path(path)
            (root / 'SOLO-ENSAYO-SINTETICO').write_text('spartakos\n')
            (root / 'events.json').write_text(json.dumps(data))
            phases = ('store_conflict', 'reload_conflict', 'expire_conflict', 'verify_conflict') if conflict else (
                'store_pending', 'expire_pending', 'verify_pending')
            for phase in phases:
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--phase', phase,
                    '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr[-2000:])
                self.assertEqual(json.loads(result.stdout), {'phase': phase, 'ok': True})

    def test_two_persisted_observers_detect_exchanged_branches_after_restart(self):
        owner, witnesses, inception = fixture()
        branches = [eventing.interact(pre=inception.pre, dig=inception.said, sn=1,
                                     data=[{'branch': name}]) for name in ('a', 'b')]
        with tempfile.TemporaryDirectory(prefix='spartakos-persisted-views-') as path:
            roots = [Path(path) / name for name in ('a', 'b')]
            for root, order in zip(roots, (branches, list(reversed(branches)))):
                root.mkdir(mode=0o700)
                (root / 'SOLO-ENSAYO-SINTETICO').write_text('spartakos\n')
                events = [inception, *order]
                data = [{'event': event.raw.decode(), 'owner': [owner.sign(event.raw, index=0).qb64],
                         'witnesses': [sig.qb64 for sig in receipts(event, witnesses, [0, 1])]} for event in events]
                (root / 'events.json').write_text(json.dumps(data))
            for phase in ('store_branch', 'receive_conflict', 'reload_conflict'):
                for root in roots:
                    result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--phase', phase,
                        '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
                    self.assertEqual(result.returncode, 0, result.stderr[-2000:])
                    self.assertEqual(json.loads(result.stdout), {'phase': phase, 'ok': True})

    def test_pending_expiry_boundary_and_explicit_resubmission(self):
        self.scenario(conflict=False)

    def test_conflict_evidence_survives_restart_and_queue_expiry(self):
        self.scenario(conflict=True)


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase')
    parser.add_argument('--state-dir', type=Path)
    args = parser.parse_args()
    if args.phase:
        if args.state_dir is None:
            parser.error('Falta --state-dir')
        worker(args.state_dir, args.phase)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
