# SPDX-License-Identifier: AGPL-3.0-or-later
"""Frontera del cursor nativo: generador real con transporte sustituido en el ensayo."""
import argparse
from collections import deque
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from hio.base import tyming
from keri.app import indirecting
from keri_destinations import store
from keri_mailbox import MARKER

SOURCE = 'synthetic-source'
PAYLOAD = 'synthetic-unvalidated-message'


def checkpoint(root, stage):
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    with store(root, 'receiver') as hab:
        client = SimpleNamespace(requests=deque(), events=deque([
            {'id': '0', 'name': '/reply', 'data': PAYLOAD}]))
        poller = indirecting.Poller(hab=hab, witness=SOURCE, topics=['/reply'])
        # Solo se ejecuta eventDo. No hay planificador HTTP ni respuesta de red real.
        poller.extend = lambda doers: None
        clock = tyming.Tymist()
        stream = poller.eventDo(tymth=clock.tymen())
        with patch.object(indirecting.agenting, 'httpClient', return_value=(client, object())), \
             patch.object(indirecting.httping, 'createCESRRequest') as request:
            next(stream)  # Cesión inicial.
            next(stream)  # Mensaje en RAM; todavía no se ha guardado el cursor.
            assert list(poller.msgs) == [PAYLOAD.encode()]
            before = hab.db.tops.get((hab.pre, SOURCE))
            assert before is None
            if stage == 'after':
                next(stream)  # Persistencia nativa, sin ejecutar parser/validador.
                assert hab.db.tops.get((hab.pre, SOURCE)).topics == {'/reply': 0}
            assert request.call_count == 1
            print(json.dumps({'queued': len(poller.msgs), 'validation_run': False, 'stage': stage}), flush=True)
            os._exit(19 if stage == 'before' else 20)


class NativePollerCheckpoint(unittest.TestCase):
    def test_process_exit_distinguishes_ram_queue_from_persisted_transport_cursor(self):
        for stage in ('before', 'after'):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory(prefix='spartakos-poller-checkpoint-') as path:
                root = Path(path)
                (root / MARKER).write_text('spartakos\n')
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--checkpoint', str(root),
                    '--stage', stage], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 19 if stage == 'before' else 20, result.stderr[-1800:])
                self.assertEqual(json.loads(result.stdout), {'queued': 1, 'validation_run': False, 'stage': stage})
                with store(root, 'receiver') as hab:
                    saved = hab.db.tops.get((hab.pre, SOURCE))
                    self.assertEqual(None if saved is None else saved.topics, None if stage == 'before' else {'/reply': 0})
                    self.assertEqual(list(indirecting.Poller(hab=hab, witness=SOURCE, topics=['/reply']).msgs), [])
                    # No se atribuye al cursor una validación que nunca se ejecutó.
                    self.assertEqual(len(hab.kevers), 1)


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path)
    parser.add_argument('--stage', choices=['before', 'after'])
    args = parser.parse_args()
    if args.checkpoint:
        if not args.stage:
            parser.error('Falta --stage')
        checkpoint(args.checkpoint, args.stage)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
