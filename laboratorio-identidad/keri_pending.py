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
import urllib.error
from urllib.parse import urlparse

from keri import core, kering
from keri.core import eventing, serdering
from keri.db import basing, dbing

from keri_witnesses import fixture, receipts
from keri_http import WitnessProcess


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
        elif phase in ('resume', 'unavailable'):
            assert kvy.kevers[pending.pre].sn == 0
            assert db.cntPwes(key) == 1
            # No se reenvía el evento: se añade el recibo y se procesa el escrow persistido.
            receipt = eventing.receipt(pre=pending.pre, sn=pending.sn, said=pending.said)
            if 'http_witness' in data:
                endpoint = data['http_witness']
                url = urlparse(endpoint['url'])
                if url.scheme != 'http' or url.hostname != '127.0.0.1' or url.path != '/receipts':
                    raise RuntimeError('El ensayo solo admite el endpoint local de recibos.')
                witness = WitnessProcess(root)
                witness.identifier, witness.index, witness.url = endpoint['identifier'], endpoint['index'], endpoint['url']
                if phase == 'unavailable':
                    try:
                        witness.request(query=f'pre={pending.pre}&sn={pending.sn}')
                    except urllib.error.URLError:
                        assert kvy.kevers[pending.pre].sn == 0
                        assert db.cntPwes(key) == 1
                        print(json.dumps({'phase': phase, 'ok': True}))
                        return
                    raise AssertionError('El testigo detenido respondió.')
                extra_receipts = witness.request(query=f'pre={pending.pre}&sn={pending.sn}')
            else:
                extra = json.loads((root / 'later-receipt.json').read_text())
                extra_receipts = [core.Siger(qb64=extra['receipt'])]
            try:
                kvy.processReceipt(serder=receipt, wigers=extra_receipts, local=False)
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


class HttpPendingRecovery(unittest.TestCase):
    def test_http_receipt_recovers_persisted_verifier_after_witness_crash(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-combined-') as path:
            root = Path(path)
            observer = root / 'observer'
            observer.mkdir(mode=0o700)
            (observer / 'SOLO-ENSAYO-SINTETICO').write_text('spartakos\n')
            witnesses = []
            try:
                for index in range(3):
                    directory = root / f'witness-{index}'
                    directory.mkdir(mode=0o700)
                    (directory / 'SOLO-ENSAYO-SINTETICO').write_text('spartakos\n')
                    witness = WitnessProcess(directory, guarded=True)
                    witness.index = index
                    witnesses.append(witness)
                    witness.start()
                owner, following = core.Signer(), core.Signer()
                inception = eventing.incept(keys=[owner.verfer.qb64],
                    ndigs=[core.Diger(ser=following.verfer.qb64b).qb64],
                    wits=[w.identifier for w in witnesses], toad=2)
                inception_receipts = [s.qb64 for witness in witnesses for s in witness.request(inception, owner)]
                pending = eventing.interact(pre=inception.pre, dig=inception.said, sn=1)
                first_receipt = witnesses[0].request(pending, owner)[0].qb64
                witnesses[1].request(pending, owner)
                def save_events():
                    data = {'inception': inception.raw.decode(), 'pending': pending.raw.decode(),
                        'inception_owner': [owner.sign(inception.raw, index=0).qb64],
                        'inception_witnesses': inception_receipts,
                        'pending_owner': [owner.sign(pending.raw, index=0).qb64],
                        'first_receipt': first_receipt,
                        'http_witness': {'url': witnesses[1].url, 'identifier': witnesses[1].identifier, 'index': 1}}
                    (observer / 'events.json').write_text(json.dumps(data))
                save_events()
                def stage(phase):
                    result = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                        '--phase', phase, '--state-dir', str(observer)], capture_output=True, text=True, timeout=20)
                    self.assertEqual(result.returncode, 0, result.stderr[-2000:])
                    self.assertEqual(json.loads(result.stdout), {'phase': phase, 'ok': True})
                stage('wait')
                witnesses[1].stop(abrupt=True)
                stage('unavailable')
                witnesses[1].start()
                save_events()  # Solo actualiza la dirección efímera; no añade el recibo faltante.
                stage('resume')
                stage('verify')
                # Otro proceso confirma que el estado final permanece persistido.
                stage('verify')
            finally:
                for witness in witnesses:
                    witness.stop()


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['wait', 'resume', 'verify', 'unavailable'])
    parser.add_argument('--state-dir', type=Path)
    args = parser.parse_args()
    if args.phase:
        if args.state_dir is None:
            parser.error('Falta --state-dir')
        run_phase(args.state_dir, args.phase)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
