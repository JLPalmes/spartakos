# SPDX-License-Identifier: AGPL-3.0-or-later
"""Propuesta de entrada durable con Poller real y transporte sustituido en el ensayo."""
import argparse
from collections import deque
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from hio.base import tyming
from keri.app import indirecting, storing
from keri.core import serdering
from keri_destinations import ROLE, deliver, store
from keri_mailbox import MARKER, TOPIC

SOURCE = 'synthetic-source'


class DurableInbox:
    """Una única fuente/tema del escenario; append termina después de confirmar SQLite."""
    def __init__(self, root):
        self.path = root / 'pending-inbox.sqlite3'
        with closing(sqlite3.connect(self.path)) as db:
            db.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, payload BLOB NOT NULL, validated INTEGER NOT NULL DEFAULT 0)')
            db.commit()

    def append(self, message):
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('INSERT INTO messages (payload) VALUES (?)', (bytes(message),))

    def pending(self):
        with closing(sqlite3.connect(self.path)) as db:
            return db.execute('SELECT id,payload FROM messages WHERE validated=0 ORDER BY id').fetchall()

    def mark_validated(self, number):
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('UPDATE messages SET validated=1 WHERE id=?', (number,))


def worker(root, stage):
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    expected = json.loads((root / 'public-identifiers.json').read_text())
    inbox = DurableInbox(root)
    with store(root, 'receiver') as hab:
        if stage == 'receive':
            saved = hab.db.tops.get((hab.pre, SOURCE))
            start = 0 if saved is None else saved.topics.get('/reply', -1) + 1
            mailbox = storing.Mailboxer(name='replies', headDirPath=str(root / 'mailbox'), temp=False, reopen=True)
            try:
                events = deque({'id': str(ordinal), 'name': '/reply', 'data': message.decode()}
                               for ordinal, _, message in mailbox.cloneTopicIter(TOPIC, fn=start))
            finally:
                mailbox.close()
            client = SimpleNamespace(requests=deque(), events=events)
            poller = indirecting.Poller(hab=hab, witness=SOURCE, topics=['/reply'])
            # Adaptación local explícita: no modifica el componente instalado.
            poller.msgs = inbox
            poller.extend = lambda doers: None
            stream = poller.eventDo(tymth=tyming.Tymist().tymen())
            with patch.object(indirecting.agenting, 'httpClient', return_value=(client, object())), \
                 patch.object(indirecting.httping, 'createCESRRequest'):
                for _ in range(10):
                    next(stream)
                    progress = hab.db.tops.get((hab.pre, SOURCE))
                    if progress is not None and progress.topics.get('/reply') == 3:
                        assert len(inbox.pending()) == 4
                        assert expected['owner'] not in hab.kevers
                        print(json.dumps({'received': 4, 'transport_last': 3, 'validated': 0}), flush=True)
                        os._exit(20)
                raise AssertionError('El generador no confirmó el progreso esperado.')
        else:
            processed = 0
            for number, message in inbox.pending():
                event = serdering.SerderKERI(raw=message)
                if event.ilk == 'icp' and event.pre == expected['owner']:
                    deliver(hab, message)
                    if event.pre not in hab.kevers:
                        raise ValueError('Creación no validada.')
                elif event.ilk == 'rpy' and event.ked['a'] == {
                        'cid': expected['owner'], 'eid': expected['provider'], 'role': ROLE}:
                    deliver(hab, message)
                    if hab.db.rpys.get(keys=(event.said,)) is None:
                        raise ValueError('Respuesta no validada; entrada pendiente conservada.')
                else:
                    raise ValueError('Mensaje fuera del escenario; entrada pendiente conservada.')
                if stage == 'validate-exit' and event.ilk == 'rpy' and event.ked['r'].endswith('/cut'):
                    print(json.dumps({'after_native_validation': True, 'pending': len(inbox.pending())}), flush=True)
                    os._exit(21)
                inbox.mark_validated(number)
                processed += 1
            allowed = hab.fetchEndAllowed(expected['owner'], ROLE, expected['provider'])
            print(json.dumps({'processed': processed, 'pending': len(inbox.pending()), 'allowed_in_view': allowed}))


class DurableNativeInbox(unittest.TestCase):
    def test_failed_sqlite_insert_keeps_cursor_before_cut_and_explicit_retry_recovers(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-inbox-write-failure-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            produced = subprocess.run([sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
                '--stage', 'produce', '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
            self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
            inbox = DurableInbox(root)
            # Fallo lógico de INSERT dentro de una transacción SQLite real; no simula disco lleno.
            with closing(sqlite3.connect(inbox.path)) as db, db:
                db.execute("CREATE TRIGGER synthetic_failure BEFORE INSERT ON messages "
                           "WHEN (SELECT COUNT(*) FROM messages)>=2 "
                           "BEGIN SELECT RAISE(ABORT, 'synthetic persistence failure'); END")
            command = [sys.executable, str(Path(__file__).resolve()), '--worker', str(root)]
            failed = subprocess.run(command + ['--stage', 'receive'], capture_output=True, text=True, timeout=20)
            self.assertEqual(failed.returncode, 1)
            self.assertIn('synthetic persistence failure', failed.stderr)
            self.assertEqual(len(inbox.pending()), 2)
            with store(root, 'receiver') as hab:
                self.assertEqual(hab.db.tops.get((hab.pre, SOURCE)).topics, {'/reply': 1})
                expected = json.loads((root / 'public-identifiers.json').read_text())
                self.assertNotIn(expected['owner'], hab.kevers)
            with closing(sqlite3.connect(inbox.path)) as db, db:
                db.execute('DROP TRIGGER synthetic_failure')
            recovered = subprocess.run(command + ['--stage', 'receive'], capture_output=True, text=True, timeout=20)
            self.assertEqual(recovered.returncode, 20, recovered.stderr[-1500:])
            self.assertEqual(json.loads(recovered.stdout), {'received': 4, 'transport_last': 3, 'validated': 0})
            validated = subprocess.run(command + ['--stage', 'resume'], capture_output=True, text=True, timeout=20)
            self.assertEqual(validated.returncode, 0, validated.stderr[-1500:])
            self.assertEqual(json.loads(validated.stdout), {'processed': 4, 'pending': 0, 'allowed_in_view': False})

    def test_reopen_pending_after_native_cursor_and_repeat_cut_before_validation_mark(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-durable-inbox-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            produced = subprocess.run([sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
                '--stage', 'produce', '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
            self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
            def run(stage, code=0):
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                    '--stage', stage], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, code, result.stderr[-1800:])
                return json.loads(result.stdout)
            self.assertEqual(run('receive', 20), {'received': 4, 'transport_last': 3, 'validated': 0})
            self.assertEqual(len(DurableInbox(root).pending()), 4)
            with store(root, 'receiver') as hab:
                self.assertEqual(hab.db.tops.get((hab.pre, SOURCE)).topics, {'/reply': 3})
                expected = json.loads((root / 'public-identifiers.json').read_text())
                self.assertNotIn(expected['owner'], hab.kevers)
            self.assertEqual(run('validate-exit', 21), {'after_native_validation': True, 'pending': 2})
            self.assertEqual(run('resume'), {'processed': 2, 'pending': 0, 'allowed_in_view': False})
            self.assertEqual(run('resume'), {'processed': 0, 'pending': 0, 'allowed_in_view': False})


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--stage', choices=['receive', 'validate-exit', 'resume'])
    args = parser.parse_args()
    if args.worker:
        if not args.stage:
            parser.error('Falta --stage')
        worker(args.worker, args.stage)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
