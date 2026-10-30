# SPDX-License-Identifier: AGPL-3.0-or-later
"""Persistencia nativa de respuestas prefirmadas con emisor ya terminado."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from keri import core
from keri.app import storing
from keri.core import eventing
from keri_destinations import ROLE, deliver, stamp, store

MARKER = 'SOLO-ENSAYO-SINTETICO'
TOPIC = 'synthetic-recipient/reply'


def run_stage(root, stage, forged=False):
    root = root.resolve()
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    directory = root / 'mailbox'
    directory.mkdir(mode=0o700, exist_ok=True)
    mailbox = storing.Mailboxer(name='replies', headDirPath=str(directory), temp=False, reopen=True)
    try:
        if not Path(mailbox.path).resolve().is_relative_to(directory):
            raise RuntimeError('Buzón fuera del escenario.')
        if stage == 'produce':
            owner, future = core.Signer(), core.Signer()
            provider = core.Signer(transferable=False)
            inception = eventing.incept(keys=[owner.verfer.qb64], ndigs=[core.Diger(ser=future.verfer.qb64b).qb64])
            seal = eventing.SealEvent(i=inception.pre, s='0', d=inception.said)
            def signed_reply(allow, offset, signer):
                event = eventing.reply(route='/end/role/' + ('add' if allow else 'cut'),
                    data={'cid': inception.pre, 'eid': provider.verfer.qb64, 'role': ROLE}, stamp=stamp(offset))
                if signer is owner:
                    return eventing.messagize(serder=event, sigers=[signer.sign(event.raw, index=0)], seal=seal)
                # Un firmante no transferible distinto del titular no concede autoridad.
                return eventing.messagize(serder=event, cigars=[signer.sign(event.raw)])
            initial = eventing.messagize(serder=inception, sigers=[owner.sign(inception.raw, index=0)])
            grant = signed_reply(True, 1, owner)
            cut = signed_reply(False, 2, owner)
            messages = [initial, grant, signed_reply(False, 3, provider), cut] if forged else [initial, grant, cut, cut]
            for message in messages:
                assert mailbox.storeMsg(TOPIC, bytes(message))
            (root / 'public-identifiers.json').write_text(json.dumps({'owner': inception.pre, 'provider': provider.verfer.qb64}))
            # No se serializan las semillas o claves privadas del emisor.
        else:
            expected = json.loads((root / 'public-identifiers.json').read_text())
            with store(root, 'observer') as observer:
                if stage == 'grant':
                    messages = list(mailbox.cloneTopicIter(TOPIC, fn=0))[:2]
                    assert [item[0] for item in messages] == [0, 1]
                elif stage == 'forged':
                    messages = list(mailbox.cloneTopicIter(TOPIC, fn=2))[:1]
                    assert [item[0] for item in messages] == [2]
                elif stage == 'cut':
                    messages = list(mailbox.cloneTopicIter(TOPIC, fn=3 if forged else 2))
                elif stage == 'replay':
                    messages = list(mailbox.cloneTopicIter(TOPIC, fn=0))
                    assert len(messages) == 4
                elif stage == 'verify':
                    messages = []
                else:
                    raise ValueError('Etapa desconocida.')
                deliver(observer, *(item[2] for item in messages))
                allowed = observer.fetchEndAllowed(expected['owner'], ROLE, expected['provider'])
                assert allowed == (stage in ('grant', 'forged'))
        print(json.dumps({'stage': stage, 'ok': True}))
    finally:
        mailbox.close()


class PersistentSignedMailbox(unittest.TestCase):
    def scenario(self, forged):
        with tempfile.TemporaryDirectory(prefix='spartakos-native-mailbox-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            stages = ('produce', 'grant', 'forged', 'cut', 'verify') if forged else ('produce', 'grant', 'cut', 'replay', 'verify')
            for stage in stages:
                args = [sys.executable, str(Path(__file__).resolve()), '--stage', stage, '--state-dir', str(root)]
                if forged:
                    args.append('--forged')
                result = subprocess.run(args, capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr[-2000:])
                self.assertEqual(json.loads(result.stdout), {'stage': stage, 'ok': True})
            identifiers = json.loads((root / 'public-identifiers.json').read_text())
            self.assertEqual(set(identifiers), {'owner', 'provider'})

    def test_native_mailbox_reopens_after_sender_exit_and_replays_cut(self):
        self.scenario(forged=False)

    def test_stored_wrong_signer_cut_does_not_revoke_before_valid_cut(self):
        self.scenario(forged=True)


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage')
    parser.add_argument('--state-dir', type=Path)
    parser.add_argument('--forged', action='store_true')
    args = parser.parse_args()
    if args.stage:
        if args.state_dir is None:
            parser.error('Falta --state-dir')
        run_stage(args.state_dir, args.stage, args.forged)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
