# SPDX-License-Identifier: AGPL-3.0-or-later
"""Consulta mbx y SSE nativos con recepción durable del ensayo, sin MailboxDirector."""
import argparse
from collections import deque
from contextlib import ExitStack, closing
import json
import subprocess
import sys
import os
from pathlib import Path
import tempfile
import time
import unittest
import urllib.request
from unittest.mock import patch

from hio.base import doing

import keri_http_inbox as inbox_lab
from keri.app import indirecting, storing
from keri.core import serdering
from keri_destinations import deliver, store
from keri_profile_http import NoRedirect
from keri_rpy_ingress import ingress_server


class ParsedQueryEnd(indirecting.HttpEnd):
    """Adaptador del ensayo: ejecuta el parser nativo después de encolar la petición."""
    def __init__(self, observer, mailbox):
        self.observer = observer
        self.observed_cues = []
        super().__init__(mbx=mailbox, qrycues=observer.kvy.cues)

    def on_post(self, req, rep):
        super().on_post(req, rep)
        self.observer.psr.parse(ims=self.rxbs)
        self.observed_cues.extend((cue['serder'].said, cue['pre'], dict(cue['topics']))
                                  for cue in self.qrycues if cue.get('kin') == 'stream')


def query_sse(url, message, count, on_record=None):
    event = serdering.SerderKERI(raw=message)
    request = urllib.request.Request(url, data=event.raw, headers={
        'Content-Type': 'application/cesr+json',
        'CESR-ATTACHMENT': bytes(message[event.size:]).decode()})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    records, frame = [], bytearray()
    with opener.open(request, timeout=4) as response:
        if response.status != 200 or not response.headers.get('Content-Type', '').startswith('text/event-stream'):
            raise ValueError('No se recibió el stream SSE nativo esperado.')
        # Lector acotado a las tramas ASCII de este escenario; no cliente SSE general.
        while len(records) < count:
            chunk = response.read(1)
            if not chunk:
                raise ValueError('Stream terminado antes de recibir los mensajes esperados.')
            frame.extend(chunk)
            if len(frame) > 65536:
                raise ValueError('Trama fuera del tamaño del ensayo.')
            if frame.endswith(b'\n\n'):
                fields = dict(line.split(b': ', 1) for line in bytes(frame).splitlines() if b': ' in line)
                if b'id' in fields:
                    record = (int(fields[b'id']), fields.get(b'event'), fields.get(b'data'))
                    if on_record is not None:
                        on_record(record)
                    records.append(record)
                frame.clear()
    return records


def native_worker(root, stage, url=None):
    if (root / inbox_lab.MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    configuration = json.loads((root / 'native-query.json').read_text())
    recipient = configuration['recipient']
    if stage == 'receive':
        if url is None:
            raise ValueError('Falta la URL local del ensayo.')
        with closing(inbox_lab.connect(root)) as db:
            def persist(record):
                ordinal, topic, payload = record
                row = db.execute('SELECT next_ordinal FROM progress WHERE source=? AND recipient=? AND topic=?',
                                 (url, recipient, '/reply')).fetchone()
                expected = 0 if row is None else row[0]
                if ordinal != expected or topic != b'/reply' or payload is None:
                    raise ValueError('Sobre nativo inesperado; no se avanza recepción.')
                with db:
                    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?,0)',
                               (url, recipient, '/reply', ordinal, payload, inbox_lab.digest(payload)))
                    db.execute('INSERT OR REPLACE INTO progress VALUES (?,?,?,?)',
                               (url, recipient, '/reply', ordinal + 1))
            records = query_sse(url, (root / 'query.cesr').read_bytes(), count=configuration.get('count', 4), on_record=persist)
        print(json.dumps({'received': len(records), 'validation_run': False}), flush=True)
        os._exit(20)
    else:
        result = inbox_lab.validate(root, interrupt=stage == 'interrupt', expected_recipient=recipient)
        print(json.dumps(result))


class DurableClientEvents(deque):
    """Adaptador experimental: confirma metadatos antes de retirar el evento del cliente."""
    def __init__(self, root, url, recipient):
        super().__init__()
        self.root, self.url, self.recipient = root, url, recipient

    def popleft(self):
        event = self[0]
        if all(key in event for key in ('id', 'name', 'data')):
            ordinal, topic, payload = int(event['id']), event['name'], event['data'].encode()
            with closing(inbox_lab.connect(self.root)) as db:
                row = db.execute('SELECT next_ordinal FROM progress WHERE source=? AND recipient=? AND topic=?',
                                 (self.url, self.recipient, topic)).fetchone()
                expected = 0 if row is None else row[0]
                if topic != '/reply' or ordinal != expected:
                    raise ValueError('Evento nativo discontinuo; no se retira de la cola.')
                with db:
                    db.execute('INSERT INTO messages VALUES (?,?,?,?,?,?,0)',
                               (self.url, self.recipient, topic, ordinal, payload, inbox_lab.digest(payload)))
                    db.execute('INSERT OR REPLACE INTO progress VALUES (?,?,?,?)',
                               (self.url, self.recipient, topic, ordinal + 1))
        return super().popleft()


class NativeMailboxQuery(unittest.TestCase):
    def test_real_poller_http_client_preserves_event_envelope_before_native_cursor(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-real-poller-') as path, ExitStack() as stack:
            root = Path(path)
            recipient = stack.enter_context(store(root, 'recipient'))
            host = stack.enter_context(store(root, 'controller'))
            deliver(host, recipient.makeOwnInception())
            mailbox = storing.Mailboxer(name='public-poller', headDirPath=str(root / 'mailbox'), temp=False, reopen=True)
            stack.callback(mailbox.close)
            messages = [b'public-poller-one', b'public-poller-two']
            for message in messages:
                self.assertTrue(mailbox.storeMsg(recipient.pre + '/reply', message))
            endpoint = ParsedQueryEnd(host, mailbox)
            with ingress_server(endpoint) as url:
                deliver(recipient, host.makeOwnInception(), host.makeLocScheme(url=url))
                actual_factory = indirecting.agenting.httpClient
                def durable_factory(hab, witness):
                    client, doer = actual_factory(hab, witness)
                    events = DurableClientEvents(root, url, recipient.pre)
                    # Cliente y parser HTTP reales; solo se adapta su contenedor de eventos.
                    client.events = events
                    client.respondent.events = events
                    return client, doer
                poller = indirecting.Poller(hab=recipient, witness=host.pre, topics=['/reply'])
                scheduler = doing.Doist(tock=0.01, doers=[poller])
                with patch.object(indirecting.agenting, 'httpClient', side_effect=durable_factory):
                    try:
                        scheduler.enter()
                        deadline = time.monotonic() + 8
                        while time.monotonic() < deadline:
                            scheduler.recur()
                            progress = recipient.db.tops.get((recipient.pre, host.pre))
                            if progress is not None and progress.topics.get('/reply') == 1:
                                break
                            time.sleep(0.005)
                        else:
                            self.fail('El Poller real no recibió y confirmó el progreso esperado.')
                    finally:
                        scheduler.exit()
                self.assertEqual(list(poller.msgs), messages)
                with closing(inbox_lab.connect(root)) as db:
                    self.assertEqual(db.execute('SELECT recipient,topic,ordinal,payload,validated FROM messages ORDER BY ordinal').fetchall(),
                        [(recipient.pre, '/reply', index, message, 0) for index, message in enumerate(messages)])
                    self.assertEqual(db.execute('SELECT next_ordinal FROM progress').fetchone()[0], 2)
                self.assertEqual(len(endpoint.observed_cues), 1)

    def test_native_sse_durable_envelopes_survive_receiver_exit_and_offline_cut_replay(self):
        self.durable_scenario()

    def test_native_sse_insert_failure_keeps_progress_and_explicit_resume_receives_cut(self):
        self.durable_scenario(failed_write=True)

    def durable_scenario(self, failed_write=False):
        with tempfile.TemporaryDirectory(prefix='spartakos-native-durable-') as path:
            root = Path(path)
            (root / inbox_lab.MARKER).write_text('spartakos\n')
            produced = subprocess.run([sys.executable, str(Path(__file__).with_name('keri_mailbox.py')),
                '--stage', 'produce', '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
            self.assertEqual(produced.returncode, 0, produced.stderr[-1500:])
            with store(root, 'mailbox-controller') as host:
                with store(root, 'query-recipient') as recipient:
                    deliver(host, recipient.makeOwnInception())
                    pre = recipient.pre
                    query = recipient.query(pre=pre, src=host.pre, route='mbx', query={'topics': {'/reply': 0}})
                    (root / 'query.cesr').write_bytes(query)
                    (root / 'native-query.json').write_text(json.dumps({'recipient': pre}))
                mailbox = storing.Mailboxer(name='replies', headDirPath=str(root / 'mailbox'), temp=False, reopen=True)
                try:
                    for _, _, message in list(mailbox.cloneTopicIter('synthetic-recipient/reply')):
                        self.assertTrue(mailbox.storeMsg(pre + '/reply', message))
                    endpoint = ParsedQueryEnd(host, mailbox)
                    with ingress_server(endpoint) as url:
                        if failed_write:
                            with closing(inbox_lab.connect(root)) as db, db:
                                db.execute("CREATE TRIGGER synthetic_native_failure BEFORE INSERT ON messages "
                                           "WHEN (SELECT COUNT(*) FROM messages)>=2 "
                                           "BEGIN SELECT RAISE(ABORT, 'synthetic native persistence failure'); END")
                            failed = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                                '--stage', 'receive', '--url', url], capture_output=True, text=True, timeout=20)
                            self.assertEqual(failed.returncode, 1)
                            self.assertIn('synthetic native persistence failure', failed.stderr)
                            with closing(inbox_lab.connect(root)) as db, db:
                                self.assertEqual(db.execute('SELECT COUNT(*) FROM messages').fetchone()[0], 2)
                                self.assertEqual(db.execute('SELECT next_ordinal FROM progress').fetchone()[0], 2)
                                db.execute('DROP TRIGGER synthetic_native_failure')
                            # Reintento explícito desde el progreso confirmado, con otra consulta firmada.
                            with store(root, 'query-recipient') as signer:
                                query = signer.query(pre=pre, src=host.pre, route='mbx', query={'topics': {'/reply': 2}})
                            (root / 'query.cesr').write_bytes(query)
                            (root / 'native-query.json').write_text(json.dumps({'recipient': pre, 'count': 2}))
                        received = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--worker', str(root),
                            '--stage', 'receive', '--url', url], capture_output=True, text=True, timeout=20)
                        self.assertEqual(received.returncode, 20, received.stderr[-1800:])
                        self.assertEqual(json.loads(received.stdout), {'received': 2 if failed_write else 4, 'validation_run': False})
                        with closing(inbox_lab.connect(root)) as db:
                            self.assertEqual(db.execute('SELECT source,recipient,topic,ordinal,validated FROM messages ORDER BY ordinal').fetchall(),
                                             [(url, pre, '/reply', n, 0) for n in range(4)])
                            self.assertEqual(db.execute('SELECT next_ordinal FROM progress').fetchone()[0], 4)
                        self.assertEqual(endpoint.observed_cues[-1], (serdering.SerderKERI(raw=query).said, pre, {'/reply': 2 if failed_write else 0}))
                finally:
                    mailbox.close()
            # El servidor y el controlador ya están cerrados; no se consulta red al validar.
            with store(root, 'http-receiver') as observer:
                expected = json.loads((root / 'public-identifiers.json').read_text())
                self.assertNotIn(expected['owner'], observer.kevers)
            command = [sys.executable, str(Path(__file__).resolve()), '--worker', str(root), '--stage']
            interrupted = subprocess.run(command + ['interrupt'], capture_output=True, text=True, timeout=20)
            self.assertEqual(interrupted.returncode, 21, interrupted.stderr[-1800:])
            for processed in (2, 0):
                resumed = subprocess.run(command + ['validate'], capture_output=True, text=True, timeout=20)
                self.assertEqual(resumed.returncode, 0, resumed.stderr[-1800:])
                self.assertEqual(json.loads(resumed.stdout), {'processed': processed, 'pending': 0, 'allowed_in_view': False})

    def test_signed_query_native_parser_cue_and_http_sse_keep_ordinals_and_bytes(self):
        self.query_scenario()

    def test_other_known_signer_can_read_public_recipient_fixture_without_read_grant(self):
        self.query_scenario(foreign=True)

    def query_scenario(self, foreign=False):
        with tempfile.TemporaryDirectory(prefix='spartakos-native-query-') as path, ExitStack() as stack:
            root = Path(path)
            recipient = stack.enter_context(store(root, 'recipient'))
            host = stack.enter_context(store(root, 'mailbox-controller'))
            deliver(host, recipient.makeOwnInception())
            signer = recipient
            if foreign:
                signer = stack.enter_context(store(root, 'other-known-reader'))
                deliver(host, signer.makeOwnInception())
                self.assertNotEqual(signer.pre, recipient.pre)
                # No se emite una concesión de lectura entre estas identidades.
            mailbox = storing.Mailboxer(name='public-replies', headDirPath=str(root / 'mailbox'), temp=False, reopen=True)
            stack.callback(mailbox.close)
            messages = [b'public-synthetic-message-one', b'public-synthetic-message-two']
            for message in messages:
                self.assertTrue(mailbox.storeMsg(recipient.pre + '/reply', message))
            endpoint = ParsedQueryEnd(host, mailbox)
            with ingress_server(endpoint) as url:
                message = signer.query(pre=recipient.pre, src=host.pre, route='mbx', query={'topics': {'/reply': 0}})
                query = serdering.SerderKERI(raw=message)
                records = query_sse(url, message, count=2)
                self.assertEqual(records, [(0, b'/reply', messages[0]), (1, b'/reply', messages[1])])
                self.assertEqual(endpoint.observed_cues, [(query.said, recipient.pre, {'/reply': 0})])
                resumed = signer.query(pre=recipient.pre, src=host.pre, route='mbx', query={'topics': {'/reply': 1}})
                self.assertEqual(query_sse(url, resumed, count=1), [(1, b'/reply', messages[1])])
            # La recepción de texto público no crea validación de aplicación o cursor durable.
            self.assertFalse((root / 'http-inbox.sqlite3').exists())


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--stage', choices=['receive', 'validate', 'interrupt'])
    parser.add_argument('--url')
    args = parser.parse_args()
    if args.worker:
        if not args.stage:
            parser.error('Falta --stage')
        native_worker(args.worker, args.stage, args.url)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
