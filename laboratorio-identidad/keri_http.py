# SPDX-License-Identifier: AGPL-3.0-or-later
"""Ensayo HTTP local del servicio ReceiptEnd de KERIpy con reinicios reales."""
import argparse
import json
import os
from pathlib import Path
import select
import signal
import socket
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from hio.base import doing
from hio.core import http

import falcon
from hio.help import decking
from keri import core, kering
from keri.app import configing, habbing, indirecting
from keri.core import coring, eventing, serdering
from keri.db import basing

MARKER = 'SOLO-ENSAYO-SINTETICO'


def serve(root):
    root = root.resolve()
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Falta el marcador del directorio sintético.')
    cf = configing.Configer(name='witness', base='lab', temp=False, headDirPath=str(root), reopen=True)
    hby = habbing.Habery(name='witness', base='lab', temp=False, headDirPath=str(root), cf=cf)
    try:
        for resource in (hby.cf, hby.db, hby.ks):
            if not Path(resource.path).resolve().is_relative_to(root):
                raise RuntimeError('Recurso fuera del ensayo.')
        hab = hby.habByName('witness') or hby.makeHab(name='witness', transferable=False)
        app = falcon.App()
        app.add_route('/receipts', indirecting.ReceiptEnd(hab=hab))
        # hio interpreta port=0 como puerto 80; obtener uno efímero explícito.
        for _ in range(5):
            with socket.socket() as reservation:
                reservation.bind(('127.0.0.1', 0))
                port = reservation.getsockname()[1]
            server = indirecting.createHttpServer('127.0.0.1', port, app)
            if server.reopen():
                break
        else:
            raise RuntimeError('No se pudo abrir un puerto local libre.')
        try:
            print(json.dumps({'port': server.servant.ha[1], 'identifier': hab.pre}), flush=True)
            doing.Doist(real=True, tock=0.01).do(doers=[http.ServerDoer(server=server)])
        finally:
            server.close()
    finally:
        hby.close()


class WitnessProcess:
    def __init__(self, root):
        self.root = root
        self.process = None
        self.identifier = None

    def start(self):
        self.process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--serve', str(self.root)],
                                        stdout=subprocess.PIPE, stderr=None, text=True)
        if not select.select([self.process.stdout], [], [], 15)[0]:
            self.stop()
            raise RuntimeError('El testigo no arrancó a tiempo.')
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError('El testigo terminó durante el arranque.')
        metadata = json.loads(line)
        if self.identifier is not None and self.identifier != metadata['identifier']:
            raise AssertionError('El testigo cambió de identidad al reiniciar.')
        self.identifier = metadata['identifier']
        self.url = f"http://127.0.0.1:{metadata['port']}/receipts"

    def stop(self, abrupt=False):
        if self.process is not None:
            self.process.kill() if abrupt else self.process.terminate()
            try:
                self.process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.communicate(timeout=5)
            self.process = None

    def request(self, event=None, owner=None, query=None):
        if event is not None:
            message = eventing.messagize(serder=event, sigers=[owner.sign(event.raw, index=0)])
            request = urllib.request.Request(self.url, data=event.raw, headers={
                'Content-Type': 'application/cesr+json',
                'CESR-ATTACHMENT': bytes(message[event.size:]).decode('utf-8')})
        else:
            request = urllib.request.Request(self.url + '?' + query)
        # No proxies: las peticiones de este ensayo solo usan el bucle local.
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request, timeout=3) as response:
            if response.status != 200:
                raise AssertionError('No se obtuvo un recibo confirmado.')
            raw = bytearray(response.read())
        receipt = serdering.SerderKERI(raw=raw)
        del raw[:receipt.size]
        counter = core.Counter(qb64b=raw, strip=True, gvrsn=kering.Vrsn_1_0)
        if counter.name == core.Codens.WitnessIdxSigs:
            signatures = [core.Siger(qb64b=raw, strip=True) for _ in range(counter.count)]
        elif counter.name == core.Codens.NonTransReceiptCouples:
            signatures = []
            for _ in range(counter.count):
                verfer = coring.Verfer(qb64b=raw, strip=True)
                cigar = core.Cigar(qb64b=raw, strip=True)
                if verfer.qb64 != self.identifier:
                    raise AssertionError('El recibo pertenece a otro testigo.')
                signatures.append(core.Siger(raw=cigar.raw, index=self.index))
        else:
            raise AssertionError(f'Formato inesperado de recibos: {counter.code}, {counter.count}')
        if raw:
            raise AssertionError('Datos sobrantes en el recibo.')
        if event is not None and (receipt.pre != event.pre or receipt.sn != event.sn or receipt.said != event.said):
            # El SAID de un rct es el digest recepcionado, no un digest nuevo.
            raise AssertionError('El recibo no corresponde al evento enviado.')
        return signatures


class HttpWitnessRecovery(unittest.TestCase):
    def test_endpoint_response_is_not_proof_of_event_acceptance(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-http-invalid-') as directory:
            root = Path(directory)
            (root / MARKER).write_text('spartakos\n')
            witness = WitnessProcess(root)
            witness.index = 0
            try:
                witness.start()
                owner, following = core.Signer(), core.Signer()
                inception = eventing.incept(keys=[owner.verfer.qb64],
                    ndigs=[coring.Diger(ser=following.verfer.qb64b).qb64],
                    wits=[witness.identifier], toad=1)
                witness.request(inception, owner)
                invalid = eventing.interact(pre=inception.pre, dig=inception.said, sn=1)
                impostor = core.Signer()
                # Diagnóstico de la implementación fijada; no es una garantía aprobada.
                receipts = witness.request(invalid, impostor)
                self.assertEqual(len(receipts), 1)
                self.assertTrue(coring.Verfer(qb64=witness.identifier).verify(receipts[0].raw, invalid.raw))
                with self.assertRaises(urllib.error.HTTPError) as missing:
                    witness.request(query=f'pre={inception.pre}&sn=1')
                self.assertEqual(missing.exception.code, 404)
                missing.exception.close()
                with basing.openDB(name='spartakos-http-invalid-observer') as db:
                    verifier = eventing.Kever(serder=inception, sigers=[owner.sign(inception.raw, index=0)],
                        wigers=witness.request(query=f'pre={inception.pre}&sn=0'), db=db,
                        local=False, cues=decking.Deck())
                    with self.assertRaises(kering.ValidationError):
                        verifier.update(serder=invalid, sigers=[impostor.sign(invalid.raw, index=0)],
                                        wigers=receipts, local=False)
                    self.assertEqual(verifier.sn, 0)
            finally:
                witness.stop()

    def test_graceful_outage_and_persisted_recovery(self):
        self.scenario(abrupt=False)

    def test_crash_and_persisted_recovery(self):
        self.scenario(abrupt=True)

    def scenario(self, abrupt):
        with tempfile.TemporaryDirectory(prefix='spartakos-http-witness-') as directory:
            witnesses = []
            try:
                for index in range(3):
                    root = Path(directory) / str(index)
                    root.mkdir(mode=0o700)
                    (root / MARKER).write_text('spartakos\n')
                    witness = WitnessProcess(root)
                    witness.index = index
                    witnesses.append(witness)
                    witness.start()
                owner, following = core.Signer(), core.Signer()
                inception = eventing.incept(keys=[owner.verfer.qb64],
                    ndigs=[coring.Diger(ser=following.verfer.qb64b).qb64],
                    wits=[w.identifier for w in witnesses], toad=2)
                receipts = [sig for w in witnesses for sig in w.request(inception, owner)]
                with basing.openDB(name='spartakos-http-observer') as db:
                    verifier = eventing.Kever(serder=inception, sigers=[owner.sign(inception.raw, index=0)],
                                             wigers=receipts, db=db, local=False, cues=decking.Deck())
                    witnesses[2].stop()
                    first = eventing.interact(pre=inception.pre, dig=inception.said, sn=1)
                    receipts = [sig for w in witnesses[:2] for sig in w.request(first, owner)]
                    verifier.update(serder=first, sigers=[owner.sign(first.raw, index=0)],
                                    wigers=receipts, local=False)
                    self.assertEqual(verifier.sn, 1)
                    witnesses[1].stop(abrupt=abrupt)
                    second = eventing.interact(pre=inception.pre, dig=first.said, sn=2)
                    with self.assertRaises(urllib.error.URLError):
                        witnesses[1].request(second, owner)
                    receipts = witnesses[0].request(second, owner)
                    with self.assertRaises(kering.MissingWitnessSignatureError):
                        verifier.update(serder=second, sigers=[owner.sign(second.raw, index=0)],
                                        wigers=receipts, local=False)
                    self.assertEqual(verifier.serder.said, first.said)
                    witnesses[1].start()
                    # Consulta tras un proceso nuevo: el testigo conservó el evento anterior.
                    old = witnesses[1].request(query=f'pre={inception.pre}&sn=1')
                    self.assertEqual(len(old), 1)
                    self.assertTrue(coring.Verfer(qb64=witnesses[1].identifier).verify(old[0].raw, first.raw))
                    receipts += witnesses[1].request(second, owner)
                    verifier.update(serder=second, sigers=[owner.sign(second.raw, index=0)],
                                    wigers=receipts, local=False)
                    self.assertEqual(verifier.sn, 2)
                    self.assertEqual(verifier.serder.said, second.said)
                    future = core.Signer()
                    rotation = eventing.rotate(pre=inception.pre, dig=second.said, sn=3,
                        keys=[following.verfer.qb64],
                        ndigs=[coring.Diger(ser=future.verfer.qb64b).qb64],
                        wits=[w.identifier for w in witnesses], toad=2)
                    rotation_receipts = [sig for w in witnesses[:2] for sig in w.request(rotation, following)]
                    verifier.update(serder=rotation, sigers=[following.sign(rotation.raw, index=0)],
                                    wigers=rotation_receipts, local=False)
                    self.assertEqual(verifier.prefixer.qb64, inception.pre)
                    self.assertEqual(verifier.sn, 3)
                    self.assertEqual(verifier.verfers[0].qb64, following.verfer.qb64)
                    next_event = eventing.interact(pre=inception.pre, dig=rotation.said, sn=4)
                    with self.assertRaises(kering.ValidationError):
                        verifier.update(serder=next_event, sigers=[owner.sign(next_event.raw, index=0)],
                                        wigers=rotation_receipts, local=False)
                    # Recibos válidos para la rotación no respaldan un evento posterior.
                    with self.assertRaises(kering.MissingWitnessSignatureError):
                        verifier.update(serder=next_event, sigers=[following.sign(next_event.raw, index=0)],
                                        wigers=rotation_receipts, local=False)
                    self.assertEqual(verifier.serder.said, rotation.said)
                    next_receipts = [sig for w in witnesses[:2] for sig in w.request(next_event, following)]
                    verifier.update(serder=next_event, sigers=[following.sign(next_event.raw, index=0)],
                                    wigers=next_receipts, local=False)
                    self.assertEqual(verifier.sn, 4)

            finally:
                for witness in witnesses:
                    witness.stop()


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', type=Path)
    args = parser.parse_args()
    if args.serve:
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
        serve(args.serve)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
