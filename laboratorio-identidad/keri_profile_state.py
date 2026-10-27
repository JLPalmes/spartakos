# SPDX-License-Identifier: AGPL-3.0-or-later
"""Estado local experimental de perfil y conflicto entre procesos."""
import argparse
import datetime
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from keri import core, kering
from keri.core import eventing, serdering
from keri.db import basing, dbing
from keri.help import helping
from keri_profiles import profile_bytes, profile_event, inspect_copy


class ProfileState:
    """Registro local del arnés, no registro distribuido ni consenso."""
    def __init__(self, root):
        self.connection = sqlite3.connect(root / 'profile-state.sqlite3')
        self.connection.execute('CREATE TABLE IF NOT EXISTS bodies (digest TEXT PRIMARY KEY, body BLOB NOT NULL)')
        self.connection.execute('CREATE TABLE IF NOT EXISTS conflicts (identity TEXT, evidence TEXT, PRIMARY KEY(identity, evidence))')
        self.connection.commit()

    def remember(self, db, owner, body):
        result = inspect_copy(db, owner, body)
        with self.connection:
            self.connection.execute('INSERT OR IGNORE INTO bodies VALUES (?, ?)',
                                    (core.Diger(ser=body).qb64, body))
        return result

    def flag_verified_fixture_conflict(self, data):
        # Alcance deliberado: dos interacciones sn=1 contra la misma creación,
        # sin rotación, delegación ni testigos. La biblioteca valida ambas ramas.
        inception = serdering.SerderKERI(raw=data['inception'].encode())
        branches = [serdering.SerderKERI(raw=item['event'].encode()) for item in data['branches']]
        if branches[0].said == branches[1].said or any(
                branch.pre != inception.pre or branch.sn != 1 or branch.ked['p'] != inception.said
                for branch in branches):
            raise ValueError('Fuera del escenario de conflicto del ensayo.')
        for index, branch in enumerate(branches):
            with basing.openDB(name='spartakos-independent-branch-check') as db:
                verifier = eventing.Kever(serder=inception,
                    sigers=[core.Siger(qb64=data['inception_signature'])], db=db, local=False)
                verifier.update(serder=branch,
                    sigers=[core.Siger(qb64=data['branches'][index]['signature'])], local=False)
                if verifier.serder.said != branch.said:
                    raise ValueError('No se validó la rama.')
        # Evidencia pública sintética completa, sin secretos; commit antes de caducar colas.
        evidence = json.dumps(data, sort_keys=True)
        with self.connection:
            self.connection.execute('INSERT OR IGNORE INTO conflicts VALUES (?, ?)', (inception.pre, evidence))

    def view(self, db, owner, body):
        result = inspect_copy(db, owner, body)
        conflicts = self.connection.execute('SELECT COUNT(*) FROM conflicts WHERE identity=?', (owner,)).fetchone()[0]
        return {**result, 'conflict_recorded': bool(conflicts),
                'confirmation_blocked': bool(conflicts), 'global_freshness_proven': False}

    def close(self):
        self.connection.close()


def phase(root, stage):
    root = root.resolve()
    if (root / 'SOLO-ENSAYO-SINTETICO').read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado.')
    data = json.loads((root / 'fixture.json').read_text())
    inception = serdering.SerderKERI(raw=data['inception'].encode())
    first, other = [serdering.SerderKERI(raw=item['event'].encode()) for item in data['branches']]
    body = data['body'].encode()
    db = basing.Baser(name='profile-observer', headDirPath=str(root), temp=False, reopen=True)
    state = ProfileState(root)
    try:
        if not Path(db.path).resolve().is_relative_to(root):
            raise RuntimeError('Almacén fuera del ensayo.')
        kvy = eventing.Kevery(db=db, local=False)
        if stage == 'initialize':
            kvy.processEvent(serder=inception, sigers=[core.Siger(qb64=data['inception_signature'])])
            kvy.processEvent(serder=first, sigers=[core.Siger(qb64=data['branches'][0]['signature'])])
            state.remember(db, inception.pre, body)
        elif stage == 'conflict':
            try:
                kvy.processEvent(serder=other, sigers=[core.Siger(qb64=data['branches'][1]['signature'])])
            except kering.LikelyDuplicitousError:
                pass
            else:
                raise AssertionError('No se detectó conflicto.')
            state.flag_verified_fixture_conflict(data)
        elif stage == 'expire':
            assert state.view(db, inception.pre, body)['confirmation_blocked']
            key = dbing.dgKey(other.pre, other.said)
            timestamp = helping.fromIso8601(bytes(db.getDts(key)))
            with patch('keri.core.eventing.helping.nowUTC',
                       return_value=timestamp + datetime.timedelta(seconds=kvy.TimeoutLDE + 1)):
                kvy.processEscrowDuplicitous()
            assert db.cntLdes(dbing.snKey(other.pre, other.sn)) == 0
        elif stage not in ('verify_clean', 'verify_blocked'):
            raise ValueError('Etapa desconocida.')
        stored = state.connection.execute('SELECT body FROM bodies WHERE digest=?',
                                         (core.Diger(ser=body).qb64,)).fetchone()
        assert stored and bytes(stored[0]) == body
        result = state.view(db, inception.pre, bytes(stored[0]))
        assert result['head_in_this_view']
        assert result['confirmation_blocked'] == (stage in ('conflict', 'expire', 'verify_blocked'))
        assert result['globally_current'] is None
        print(json.dumps({'stage': stage, 'ok': True}))
    finally:
        state.close()
        db.close()


class PersistedProfileState(unittest.TestCase):
    def fixture(self, root):
        owner, next_key = core.Signer(), core.Signer()
        inception = eventing.incept(keys=[owner.verfer.qb64], ndigs=[core.Diger(ser=next_key.verfer.qb64b).qb64])
        bodies = [profile_bytes(inception.pre, name) for name in ('Perfil A', 'Perfil B')]
        branches = [profile_event(inception.pre, inception.said, 1, body) for body in bodies]
        data = {'inception': inception.raw.decode(), 'inception_signature': owner.sign(inception.raw, index=0).qb64,
                'branches': [{'event': branch.raw.decode(), 'signature': owner.sign(branch.raw, index=0).qb64}
                             for branch in branches], 'body': bodies[0].decode()}
        (root / 'SOLO-ENSAYO-SINTETICO').write_text('spartakos\n')
        (root / 'fixture.json').write_text(json.dumps(data))
        return data

    def scenario(self, stages):
        with tempfile.TemporaryDirectory(prefix='spartakos-profile-state-') as path:
            root = Path(path)
            self.fixture(root)
            for stage in stages:
                result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--stage', stage,
                    '--state-dir', str(root)], capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr[-2000:])
                self.assertEqual(json.loads(result.stdout), {'stage': stage, 'ok': True})

    def test_profile_body_and_binding_survive_new_verifier_process(self):
        self.scenario(('initialize', 'verify_clean'))

    def test_conflict_blocks_after_restart_and_queue_expiry(self):
        self.scenario(('initialize', 'conflict', 'verify_blocked', 'expire', 'verify_blocked'))

    def test_invalid_signature_cannot_create_verified_conflict_record(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-profile-false-conflict-') as path:
            root = Path(path)
            data = self.fixture(root)
            other = serdering.SerderKERI(raw=data['branches'][1]['event'].encode())
            data['branches'][1]['signature'] = core.Signer().sign(other.raw, index=0).qb64
            state = ProfileState(root)
            try:
                with self.assertRaises(kering.ValidationError):
                    state.flag_verified_fixture_conflict(data)
                self.assertEqual(state.connection.execute('SELECT COUNT(*) FROM conflicts').fetchone()[0], 0)
            finally:
                state.close()


if __name__ == '__main__':
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage')
    parser.add_argument('--state-dir', type=Path)
    args = parser.parse_args()
    if args.stage:
        if args.state_dir is None:
            parser.error('Falta --state-dir')
        phase(args.state_dir, args.stage)
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
