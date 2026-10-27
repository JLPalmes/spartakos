# SPDX-License-Identifier: AGPL-3.0-or-later
"""Persistencia de eventos pendientes de recibos entre procesos verificadores."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from keri import core, kering
from keri.core import eventing, serdering
from keri.db import basing, dbing

from keri_witnesses import fixture, receipts


def run_phase(root, phase):
    root = root.resolve()
    if (root / 'SOLO-ENSAYO-SINTETICO').read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    data = json.loads((root / 'events.json').read_text())
    inception = serdering.SerderKERI(raw=data['inception'].encode())
    pending = serdering.SerderKERI(raw=data['pending'].encode())
    db = basing.Baser(name='observer', headDirPath=str(root), temp=False, reopen=True)
    try:
        if not Path(db.path).resolve().is_relative_to(root):
            raise RuntimeError('Almacén fuera del ensayo.')
        kvy = eventing.Kevery(db=db, local=False)
        key = dbing.snKey(pending.pre, pending.sn)
        if phase == 'wait':
            kvy.processEvent(serder=inception,
                sigers=[core.Siger(qb64=s) for s in data['inception_owner']],
                wigers=[core.Siger(qb64=s) for s in data['inception_witnesses']])
            try:
                kvy.processEvent(serder=pending,
                    sigers=[core.Siger(qb64=s) for s in data['pending_owner']],
                    wigers=[core.Siger(qb64=data['first_receipt'])])
            except kering.MissingWitnessSignatureError:
                pass
            else:
                raise AssertionError('Se aceptó sin suficientes recibos.')
            assert db.cntPwes(key) == 1
            assert kvy.kevers[pending.pre].sn == 0
        elif phase == 'resume':
            assert kvy.kevers[pending.pre].sn == 0
            assert db.cntPwes(key) == 1
            # No se reenvía el evento: se añade el recibo y se procesa el escrow persistido.
            receipt = eventing.receipt(pre=pending.pre, sn=pending.sn, said=pending.said)
            extra = json.loads((root / 'later-receipt.json').read_text())
            try:
                kvy.processReceipt(serder=receipt, wigers=[core.Siger(qb64=extra['receipt'])], local=False)
            except kering.UnverifiedReceiptError:
                pass  # La API guarda primero el recibo en su propio escrow.
            kvy.processEscrowUnverWitness()
            kvy.processEscrowPartialWigs()
            assert kvy.kevers[pending.pre].serder.said == pending.said
            assert db.cntPwes(key) == 0
            kvy.processEscrowPartialWigs()
            assert kvy.kevers[pending.pre].sn == 1
        elif phase == 'verify':
            assert kvy.kevers[pending.pre].serder.said == pending.said
            assert db.cntPwes(key) == 0
        else:
            raise ValueError('Etapa inválida.')
        print(json.dumps({'phase': phase, 'ok': True}))
    finally:
        db.close()


class PendingRecovery(unittest.TestCase):
    def test_escrow_survives_and_resumes_across_three_processes(self):
        owner, witnesses, inception = fixture()
        pending = eventing.interact(pre=inception.pre, dig=inception.said, sn=1)
        with tempfile.TemporaryDirectory(prefix='spartakos-pending-') as path:
            root = Path(path)
            (root / 'SOLO-ENSAYO-SINTETICO').write_text('spartakos\n')
            data = {'inception': inception.raw.decode(), 'pending': pending.raw.decode(),
                'inception_owner': [owner.sign(inception.raw, index=0).qb64],
                'inception_witnesses': [s.qb64 for s in receipts(inception, witnesses, [0, 1])],
                'pending_owner': [owner.sign(pending.raw, index=0).qb64],
                'first_receipt': witnesses[0].sign(pending.raw, index=0).qb64}
            (root / 'events.json').write_text(json.dumps(data))
            for phase in ('wait', 'resume', 'verify'):
                if phase == 'resume':
                    (root / 'later-receipt.json').write_text(json.dumps({
                        'receipt': witnesses[1].sign(pending.raw, index=1).qb64}))
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                    '--phase', phase, '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr[-2000:])
                self.assertEqual(json.loads(result.stdout), {'phase': phase, 'ok': True})


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['wait', 'resume', 'verify'])
    parser.add_argument('--state-dir', type=Path)
    args = parser.parse_args()
    if args.phase:
        if args.state_dir is None:
            parser.error('Falta --state-dir')
        run_phase(args.state_dir, args.phase)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
