# SPDX-License-Identifier: AGPL-3.0-or-later
"""Ensayo sintético de API KERIpy; sin servidores, claves reales o protocolo propio."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from keri import core, kering
from keri.app import configing, habbing
from keri.core import coring, eventing
from keri.db import basing

MARKER = 'SPARTAKOS-LABORATORIO-FICTICIO'


def phase(stage, root):
    root = root.resolve()
    if (root / MARKER).read_text() != 'solo datos sintéticos\n':
        raise RuntimeError('Directorio no preparado para este ensayo.')
    checkpoint = root / 'expected-public.json'
    expected = json.loads(checkpoint.read_text()) if checkpoint.exists() else None
    if stage == 'create' and expected is not None:
        raise RuntimeError('No se sobrescribe un ensayo existente.')
    if stage != 'create' and expected is None:
        raise RuntimeError('Falta el estado inicial del ensayo.')
    # Inyectar también Configer: en esta revisión Habery no le propaga headDirPath.
    cf = configing.Configer(name='controller', base='lab', temp=False,
                           headDirPath=str(root), reopen=True)
    hby = habbing.Habery(name='controller', base='lab', temp=False,
                        headDirPath=str(root), cf=cf)
    try:
        for resource in (hby.cf, hby.db, hby.ks):
            if not Path(resource.path).resolve().is_relative_to(root):
                raise RuntimeError('Recurso fuera del directorio de ensayo.')
        hab = hby.makeHab(name='synthetic', icount=1, ncount=1) if stage == 'create' else hby.habByName('synthetic')
        if hab is None:
            raise AssertionError('No se recuperó la identidad persistida.')
        if expected:
            assert hab.pre == expected['identifier']
            assert hab.kever.sn == expected['sequence']
            assert hab.kever.serder.said == expected['digest']
            assert hab.kever.verfers[0].qb64 == expected['public_key']
        if stage == 'rotate':
            hab.rotate()
            assert hab.pre == expected['identifier']
            assert hab.kever.verfers[0].qb64 != expected['public_key']
            assert hab.kever.sn == expected['sequence'] + 1
        elif stage == 'verify':
            hab.interact()
            assert hab.pre == expected['identifier']
            assert hab.kever.sn == expected['sequence'] + 1
        elif stage != 'create':
            raise ValueError('Etapa desconocida.')
        checkpoint.write_text(json.dumps({'identifier': hab.pre, 'sequence': hab.kever.sn,
                                         'digest': hab.kever.serder.said,
                                         'public_key': hab.kever.verfers[0].qb64}))
        print(json.dumps({'stage': stage, 'sequence': hab.kever.sn, 'ok': True}))
    finally:
        hby.close()


def controller(db):
    current, following, future = core.Signer(), core.Signer(), core.Signer()
    event = eventing.incept(keys=[current.verfer.qb64],
                           ndigs=[coring.Diger(ser=following.verfer.qb64b).qb64])
    verifier = eventing.Kever(serder=event, sigers=[current.sign(event.raw, index=0)], db=db)
    return verifier, current, following, future


def state(verifier):
    return verifier.prefixer.qb64, verifier.sn, verifier.serder.said


class KeriSmoke(unittest.TestCase):
    def test_persistence_and_rotation_across_three_processes(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-keri-state-') as path:
            root = Path(path)
            (root / MARKER).write_text('solo datos sintéticos\n')
            for stage, sequence in [('create', 0), ('rotate', 1), ('verify', 2)]:
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                         '--phase', stage, '--state-dir', str(root)],
                                        capture_output=True, text=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stderr[-2000:])
                self.assertEqual(json.loads(result.stdout), {'stage': stage, 'sequence': sequence, 'ok': True})

    def test_invalid_signature_does_not_advance_state(self):
        with basing.openDB(name='spartakos-invalid-signature') as db:
            verifier, current, _, _ = controller(db)
            event = eventing.interact(pre=verifier.prefixer.qb64, dig=verifier.serder.said, sn=1)
            before = state(verifier)
            with self.assertRaises(kering.ValidationError):
                verifier.update(serder=event, sigers=[core.Signer().sign(event.raw, index=0)])
            self.assertEqual(state(verifier), before)
            verifier.update(serder=event, sigers=[current.sign(event.raw, index=0)])
            self.assertEqual(verifier.sn, 1)

    def test_uncommitted_rotation_is_rejected(self):
        with basing.openDB(name='spartakos-uncommitted-key') as db:
            verifier, _, _, future = controller(db)
            attacker = core.Signer()
            event = eventing.rotate(pre=verifier.prefixer.qb64, keys=[attacker.verfer.qb64],
                                   dig=verifier.serder.said, sn=1,
                                   ndigs=[coring.Diger(ser=future.verfer.qb64b).qb64])
            before = state(verifier)
            with self.assertRaises(kering.ValidationError):
                verifier.update(serder=event, sigers=[attacker.sign(event.raw, index=0)])
            self.assertEqual(state(verifier), before)

    def test_previous_key_is_rejected_after_rotation(self):
        with basing.openDB(name='spartakos-previous-key') as db:
            verifier, previous, current, future = controller(db)
            identifier = verifier.prefixer.qb64
            rotation = eventing.rotate(pre=identifier, keys=[current.verfer.qb64],
                                      dig=verifier.serder.said, sn=1,
                                      ndigs=[coring.Diger(ser=future.verfer.qb64b).qb64])
            verifier.update(serder=rotation, sigers=[current.sign(rotation.raw, index=0)])
            event = eventing.interact(pre=identifier, dig=verifier.serder.said, sn=2)
            before = state(verifier)
            with self.assertRaises(kering.ValidationError):
                verifier.update(serder=event, sigers=[previous.sign(event.raw, index=0)])
            self.assertEqual(state(verifier), before)
            verifier.update(serder=event, sigers=[current.sign(event.raw, index=0)])
            self.assertEqual(verifier.prefixer.qb64, identifier)
            self.assertEqual(verifier.sn, 2)

    def test_repeated_event_does_not_advance_state(self):
        with basing.openDB(name='spartakos-replay') as db:
            verifier, current, _, _ = controller(db)
            event = eventing.interact(pre=verifier.prefixer.qb64, dig=verifier.serder.said, sn=1)
            signature = current.sign(event.raw, index=0)
            verifier.update(serder=event, sigers=[signature])
            before = state(verifier)
            with self.assertRaises(kering.ValidationError):
                verifier.update(serder=event, sigers=[signature])
            self.assertEqual(state(verifier), before)


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['create', 'rotate', 'verify'])
    parser.add_argument('--state-dir', type=Path)
    args = parser.parse_args()
    if args.phase:
        if args.state_dir is None:
            parser.error('--phase requiere --state-dir')
        phase(args.phase, args.state_dir)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
