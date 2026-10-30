# SPDX-License-Identifier: AGPL-3.0-or-later
"""Lectura HTTP finita del iterador nativo y cursor local de consumo."""
import argparse
from contextlib import closing
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import select
import signal
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urlsplit, parse_qs

from keri.app import indirecting, storing
from keri.core import serdering
from keri_destinations import ROLE, deliver, store
from keri_inventory import InventoryProvider
from keri_mailbox import MARKER, TOPIC
from keri_profile_http import fetch


def serve(root):
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    mailbox = storing.Mailboxer(name='replies', headDirPath=str(root / 'mailbox'), temp=False, reopen=True)
    try:
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urlsplit(self.path)
                try:
                    start = int(parse_qs(parsed.query).get('from', ['0'])[0])
                    if parsed.path != '/reply' or start < 0:
                        raise ValueError()
                except ValueError:
                    self.send_error(400)
                    return
                stream = iter(indirecting.MailboxIterable(mbx=mailbox, pre='synthetic-recipient', topics={'/reply': start}))
                # Adaptación finita del iterador nativo, no suscripción SSE completa.
                body = bytes(next(stream)) + bytes(next(stream))
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass
        with HTTPServer(('127.0.0.1', 0), Handler) as server:
            print(json.dumps({'port': server.server_port}), flush=True)
            server.serve_forever()
    finally:
        mailbox.close()


class MailboxServer(InventoryProvider):
    def start(self):
        self.process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--serve', str(self.root)],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not select.select([self.process.stdout], [], [], 10)[0]:
            self.stop()
            raise RuntimeError('No arrancó la lectura del buzón.')
        self.url = 'http://127.0.0.1:' + str(json.loads(self.process.stdout.readline())['port'])


def consume(root, url, limit=None, interrupt=None):
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    expected = json.loads((root / 'public-identifiers.json').read_text())
    with closing(sqlite3.connect(root / 'consumer.sqlite3')) as cursor:
        cursor.execute('CREATE TABLE IF NOT EXISTS progress (topic TEXT PRIMARY KEY, next_ordinal INTEGER)')
        cursor.execute('INSERT OR IGNORE INTO progress VALUES (?,0)', (TOPIC,))
        cursor.commit()
        next_ordinal = cursor.execute('SELECT next_ordinal FROM progress WHERE topic=?', (TOPIC,)).fetchone()[0]
        raw = fetch(url + '/reply?from=' + str(next_ordinal))
        records = []
        for frame in raw.split(b'\n\n'):
            fields = dict(line.split(b': ', 1) for line in frame.splitlines() if b': ' in line)
            if b'id' not in fields:
                continue
            if fields.get(b'event') != b'/reply' or b'data' not in fields:
                raise ValueError('Trama inesperada.')
            records.append((int(fields[b'id']), fields[b'data']))
        processed = 0
        with store(root, 'observer') as observer:
            for ordinal, message in records:
                if limit is not None and processed >= limit:
                    break
                if ordinal != next_ordinal:
                    raise ValueError('No se permite saltar posiciones del buzón.')
                if interrupt == 'before':
                    print(json.dumps({'interrupted': 'before', 'ordinal': ordinal}), flush=True)
                    os._exit(19)
                event = serdering.SerderKERI(raw=message)
                if event.ilk == 'icp':
                    if event.pre != expected['owner']:
                        raise ValueError('Identidad inesperada.')
                elif event.ilk == 'rpy':
                    if event.ked['a'] != {'cid': expected['owner'], 'eid': expected['provider'], 'role': ROLE}:
                        raise ValueError('Respuesta fuera del escenario.')
                else:
                    raise ValueError('Tipo de evento fuera del ensayo.')
                deliver(observer, message)
                if event.ilk == 'icp':
                    if event.pre not in observer.kevers:
                        raise ValueError('Creación no validada.')
                elif observer.db.rpys.get(keys=(event.said,)) is None:
                    raise ValueError('Respuesta no registrada como validada; cursor sin avanzar.')
                if interrupt == 'after':
                    print(json.dumps({'interrupted': 'after', 'ordinal': ordinal}), flush=True)
                    os._exit(20)
                with cursor:
                    cursor.execute('UPDATE progress SET next_ordinal=? WHERE topic=?', (ordinal + 1, TOPIC))
                next_ordinal, processed = ordinal + 1, processed + 1
            allowed = observer.fetchEndAllowed(expected['owner'], ROLE, expected['provider'])
        print(json.dumps({'next_ordinal': next_ordinal, 'processed': processed, 'allowed_in_view': allowed}))


class MailboxHttpConsumption(unittest.TestCase):
    def scenario(self, interrupt):
        with tempfile.TemporaryDirectory(prefix='spartakos-mailbox-http-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            produced = subprocess.run([sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
                '--stage', 'produce', '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
            self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
            expected = json.loads((root / 'public-identifiers.json').read_text())
            server = MailboxServer(root)
            def worker(extra=(), returncode=0):
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--consume', str(root),
                    '--url', server.url, *extra], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, returncode, result.stderr[-1800:])
                return json.loads(result.stdout)
            try:
                server.start()
                self.assertEqual(worker(('--limit', '2')), {'next_ordinal': 2, 'processed': 2, 'allowed_in_view': True})
                self.assertEqual(worker(('--interrupt', interrupt), 19 if interrupt == 'before' else 20),
                                 {'interrupted': interrupt, 'ordinal': 2})
                with closing(sqlite3.connect(root / 'consumer.sqlite3')) as cursor:
                    self.assertEqual(cursor.execute('SELECT next_ordinal FROM progress').fetchone()[0], 2)
                with store(root, 'observer') as observer:
                    self.assertEqual(observer.fetchEndAllowed(expected['owner'], ROLE, expected['provider']), interrupt == 'before')
                self.assertEqual(worker(), {'next_ordinal': 4, 'processed': 2, 'allowed_in_view': False})
                self.assertEqual(worker(), {'next_ordinal': 4, 'processed': 0, 'allowed_in_view': False})
            finally:
                server.stop()

    def test_native_iterable_sparse_topic_repeats_last_frame_in_same_stream(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-mailbox-native-gap-') as path:
            root = Path(path)
            mailbox = storing.Mailboxer(name='replies', headDirPath=str(root / 'mailbox'), temp=False, reopen=True)
            try:
                for message in (b'initial', b'grant', b'cut', b'cut'):
                    self.assertTrue(mailbox.storeMsg(TOPIC, message))
                self.assertTrue(mailbox.delTopic(TOPIC, on=2))
                stream = iter(indirecting.MailboxIterable(mbx=mailbox, pre='synthetic-recipient', topics={'/reply': 2}))
                self.assertIn(b'retry:', bytes(next(stream)))
                first, repeated = bytes(next(stream)), bytes(next(stream))
                self.assertIn(b'id: 3\n', first)
                self.assertEqual(repeated, first)
                self.assertEqual(stream.topics['/reply'], 4)
                self.assertEqual(bytes(next(stream)), b'')
            finally:
                mailbox.close()

    def test_stale_mailbox_silence_keeps_old_view_until_explicit_other_source(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-mailbox-stale-') as path:
            root = Path(path)
            current, stale = root / 'current', root / 'stale'
            for directory in (current, stale):
                directory.mkdir()
                (directory / MARKER).write_text('spartakos\n')
            produced = subprocess.run([sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
                '--stage', 'produce', '--state-dir', str(current)], capture_output=True, text=True, timeout=20)
            self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
            # Copia pública acotada por API nativa; el buzón antiguo solo conoce creación y concesión.
            source = storing.Mailboxer(name='replies', headDirPath=str(current / 'mailbox'), temp=False, reopen=True)
            target = storing.Mailboxer(name='replies', headDirPath=str(stale / 'mailbox'), temp=False, reopen=True)
            try:
                for ordinal, _, message in source.cloneTopicIter(TOPIC):
                    if ordinal < 2:
                        self.assertTrue(target.storeMsg(TOPIC, message))
            finally:
                target.close()
                source.close()
            servers = [MailboxServer(stale), MailboxServer(current)]
            def worker(server):
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--consume', str(current),
                    '--url', server.url], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr[-1500:])
                return json.loads(result.stdout)
            try:
                for server in servers:
                    server.start()
                self.assertEqual(worker(servers[0]), {'next_ordinal': 2, 'processed': 2, 'allowed_in_view': True})
                self.assertEqual(worker(servers[0]), {'next_ordinal': 2, 'processed': 0, 'allowed_in_view': True})
                # La fuente alternativa la elige el coordinador; no se atribuye descubrimiento automático.
                self.assertEqual(worker(servers[1]), {'next_ordinal': 4, 'processed': 2, 'allowed_in_view': False})
                self.assertEqual(worker(servers[0]), {'next_ordinal': 4, 'processed': 0, 'allowed_in_view': False})
            finally:
                for server in servers:
                    server.stop()

    def blocked_scenario(self, forged):
        with tempfile.TemporaryDirectory(prefix='spartakos-mailbox-blocked-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            args = [sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
                    '--stage', 'produce', '--state-dir', str(root)]
            if forged:
                args.append('--forged')
            produced = subprocess.run(args, capture_output=True, text=True, timeout=20)
            self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
            if not forged:
                mailbox = storing.Mailboxer(name='replies', headDirPath=str(root / 'mailbox'), temp=False, reopen=True)
                try:
                    self.assertTrue(mailbox.delTopic(TOPIC, on=2))
                finally:
                    mailbox.close()
            server = MailboxServer(root)
            try:
                server.start()
                command = [sys.executable, str(Path(__file__).resolve()), '--consume', str(root), '--url', server.url]
                initial = subprocess.run(command + ['--limit', '2'], capture_output=True, text=True, timeout=20)
                self.assertEqual(initial.returncode, 0, initial.stderr[-1500:])
                self.assertEqual(json.loads(initial.stdout)['next_ordinal'], 2)
                # Reabrir el consumidor no transforma el rechazo en avance ni salta al corte posterior.
                for _ in range(2):
                    rejected = subprocess.run(command, capture_output=True, text=True, timeout=20)
                    self.assertNotEqual(rejected.returncode, 0)
                    reason = 'Respuesta no registrada como validada' if forged else 'No se permite saltar posiciones'
                    self.assertIn(reason, rejected.stderr)
                    with closing(sqlite3.connect(root / 'consumer.sqlite3')) as cursor:
                        self.assertEqual(cursor.execute('SELECT next_ordinal FROM progress').fetchone()[0], 2)
                    expected = json.loads((root / 'public-identifiers.json').read_text())
                    with store(root, 'observer') as observer:
                        self.assertTrue(observer.fetchEndAllowed(expected['owner'], ROLE, expected['provider']))
            finally:
                server.stop()

    def test_wrong_signer_blocks_cursor_and_later_cut_without_automatic_skip(self):
        self.blocked_scenario(forged=True)

    def test_missing_ordinal_blocks_cursor_even_with_later_valid_cut(self):
        self.blocked_scenario(forged=False)

    def test_http_cursor_does_not_skip_cut_after_exit_before_validation(self):
        self.scenario('before')

    def test_http_replay_after_validation_before_cursor_commit_keeps_revocation(self):
        self.scenario('after')


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', type=Path)
    parser.add_argument('--consume', type=Path)
    parser.add_argument('--url')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--interrupt', choices=['before', 'after'])
    args = parser.parse_args()
    if args.serve:
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
        serve(args.serve)
    elif args.consume:
        if not args.url:
            parser.error('Falta --url')
        consume(args.consume, args.url, args.limit, args.interrupt)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
