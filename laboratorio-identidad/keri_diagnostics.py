# SPDX-License-Identifier: AGPL-3.0-or-later
"""Observación local de registros del arnés; no valida autoridad ni consulta red."""
import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import unittest

MARKER = 'SOLO-ENSAYO-SINTETICO'
STATES = {'checking', 'blocked', 'failed', 'receiving', 'incomplete', 'rejected', 'complete'}
CODES = {'inbox_pending', 'inbox_conflict', 'known_conflict', 'unauthorized_provider', 'address_changed', 'transport_unavailable',
         'revision_rollback', 'retired_revision_reactivation', 'revision_content_rewrite', 'missing_previous_object'}


def read_record(path, query, parameters=()):
    if not path.is_file():
        return {'read_status': 'absent', 'value': None}
    try:
        with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)) as db:
            db.execute('PRAGMA query_only=ON')
            row = db.execute(query, parameters).fetchone()
        return {'read_status': 'available' if row is not None else 'no_record', 'value': row}
    except sqlite3.DatabaseError:
        return {'read_status': 'unreadable', 'value': None}


def code(value):
    return value if isinstance(value, str) and (value in CODES or re.fullmatch(r'http_[0-9]{3}', value)) else None


def diagnose(root, owner, provider):
    root = root.resolve()
    if (root / MARKER).read_text() != 'spartakos\n':
        raise RuntimeError('Directorio no preparado para diagnóstico sintético.')
    receipt = read_record(root / 'catalog.sqlite3',
        'SELECT expected_sequence,applied_sequence,state,details FROM receipts WHERE identity=?', (owner,))
    if receipt['value'] is not None:
        expected, applied, state, raw_details = receipt['value']
        try:
            details = json.loads(raw_details)
            details = details if isinstance(details, dict) else {}
        except (ValueError, TypeError):
            details = {}
        receipt['value'] = {'expected_sequence': expected if type(expected) is int and expected >= 0 else None,
            'applied_sequence': applied if type(applied) is int and applied >= 0 else None,
            'state': state if state in STATES else 'unrecognized', 'error_code': code(details.get('error_code')),
            'missing_count': len(details['missing']) if isinstance(details.get('missing'), list) else None,
            'invalid_count': len(details['invalid']) if isinstance(details.get('invalid'), list) else None}
    attempt = read_record(root / 'inventory-access.sqlite3',
        'SELECT state,error_code FROM attempts WHERE identity=? AND provider=?', (owner, provider))
    if attempt['value'] is not None:
        state, error = attempt['value']
        attempt['value'] = {'state': state if state in STATES else 'unrecognized', 'error_code': code(error)}
    catalog = read_record(root / 'catalog.sqlite3', 'SELECT COUNT(*) FROM objects')
    if catalog['value'] is not None:
        catalog['value'] = {'stored_revision_count': catalog['value'][0]}
    conflict = read_record(root / 'profile-state.sqlite3',
        'SELECT COUNT(*) FROM conflicts WHERE identity=?', (owner,))
    if conflict['value'] is not None:
        conflict['value'] = {'recorded_conflict': bool(conflict['value'][0]), 'coverage': 'limited_fixture_only'}
    inbox_messages = read_record(root / 'http-inbox.sqlite3',
        'SELECT COUNT(*),COALESCE(SUM(validated=0),0),COALESCE(SUM(validated=1),0),'
        'COALESCE(SUM(validated IS NULL OR validated NOT IN (0,1)),0) FROM messages')
    if inbox_messages['value'] is not None:
        total, pending, validated, unrecognized = inbox_messages['value']
        inbox_messages['value'] = {'received_count': total, 'pending_count': pending,
            'marked_validated_count': validated, 'unrecognized_state_count': unrecognized}
    inbox_progress = read_record(root / 'http-inbox.sqlite3',
        'SELECT COUNT(*),MIN(next_ordinal) FROM progress')
    if inbox_progress['value'] is not None:
        count, ordinal = inbox_progress['value']
        inbox_progress['value'] = {'stream_count': count, 'next_ordinal_single_stream':
            ordinal if count == 1 and type(ordinal) is int and ordinal >= 0 else None}
    inbox_conflicts = read_record(root / 'http-inbox.sqlite3', 'SELECT COUNT(*) FROM conflicts')
    if inbox_conflicts['value'] is not None:
        inbox_conflicts['value'] = {'recorded_count': inbox_conflicts['value'][0]}
    return {'kind': 'spartakos-local-diagnostics-lab-v1', 'receipt': receipt, 'attempt': attempt,
        'catalog': catalog, 'conflict_record': conflict,
        'inbox': {'messages': inbox_messages, 'transport': inbox_progress, 'conflicts': inbox_conflicts,
                  'validation': 'local_marks_only_not_revalidated'}, 'authorization': 'not_checked',
        'global_freshness': 'not_proven', 'atomic_snapshot': False,
        'scope': 'local_records_only_no_cryptographic_revalidation'}


class DiagnosticBoundaries(unittest.TestCase):
    def test_inbox_summary_hides_routes_and_payload_and_distinguishes_unknown_marks(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-diagnostics-inbox-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            secret = 'syntheticprivatecontent'
            with closing(sqlite3.connect(root / 'http-inbox.sqlite3')) as db, db:
                db.execute('CREATE TABLE messages (payload,validated)')
                db.executemany('INSERT INTO messages VALUES (?,?)', [(secret, 0), (secret, 1), (secret, secret)])
                db.execute('CREATE TABLE progress (source,next_ordinal)')
                db.execute('INSERT INTO progress VALUES (?,?)', (secret, 3))
                db.execute('CREATE TABLE conflicts (payload)')
                db.execute('INSERT INTO conflicts VALUES (?)', (secret,))
            target = root / 'http-inbox.sqlite3'
            before = (target.read_bytes(), target.stat().st_mtime_ns)
            report = diagnose(root, 'synthetic-owner', 'synthetic-provider')
            self.assertEqual(report['inbox']['messages']['value'], {'received_count': 3, 'pending_count': 1,
                'marked_validated_count': 1, 'unrecognized_state_count': 1})
            self.assertEqual(report['inbox']['transport']['value'], {'stream_count': 1, 'next_ordinal_single_stream': 3})
            self.assertEqual(report['inbox']['conflicts']['value'], {'recorded_count': 1})
            self.assertNotIn(secret, json.dumps(report))
            self.assertEqual((target.read_bytes(), target.stat().st_mtime_ns), before)
            target.write_bytes(b'not a database')
            self.assertEqual(diagnose(root, 'synthetic-owner', 'synthetic-provider')['inbox']['messages']['read_status'], 'unreadable')

    def test_absent_records_remain_unknown_without_creating_databases(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-diagnostics-empty-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            before = set(root.iterdir())
            report = diagnose(root, 'synthetic-owner', 'synthetic-provider')
            self.assertEqual(report['conflict_record'], {'read_status': 'absent', 'value': None})
            self.assertEqual(report['receipt']['read_status'], 'absent')
            self.assertEqual(report['authorization'], 'not_checked')
            self.assertEqual(report['inbox']['messages'], {'read_status': 'absent', 'value': None})
            self.assertFalse(report['atomic_snapshot'])
            self.assertEqual(set(root.iterdir()), before)

    def test_unexpected_metadata_is_not_echoed_as_diagnostic_content(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-diagnostics-metadata-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            secret = 'syntheticprivatecontent'
            with closing(sqlite3.connect(root / 'catalog.sqlite3')) as db:
                db.execute('CREATE TABLE receipts (identity,expected_sequence,applied_sequence,state,details)')
                db.execute('INSERT INTO receipts VALUES (?,?,?,?,?)',
                           ('synthetic-owner', secret, 1, secret, json.dumps({'error_code': secret})))
                db.commit()
            report = diagnose(root, 'synthetic-owner', 'synthetic-provider')
            self.assertEqual(report['receipt']['value']['state'], 'unrecognized')
            self.assertIsNone(report['receipt']['value']['expected_sequence'])
            self.assertIsNone(report['receipt']['value']['error_code'])
            self.assertNotIn(secret, json.dumps(report))

    def test_unreadable_database_is_not_reported_as_empty_or_successful(self):
        with tempfile.TemporaryDirectory(prefix='spartakos-diagnostics-corrupt-') as path:
            root = Path(path)
            (root / MARKER).write_text('spartakos\n')
            target = root / 'profile-state.sqlite3'
            target.write_bytes(b'not a sqlite database')
            before = (target.read_bytes(), target.stat().st_mtime_ns)
            report = diagnose(root, 'synthetic-owner', 'synthetic-provider')
            self.assertEqual(report['conflict_record'], {'read_status': 'unreadable', 'value': None})
            self.assertEqual((target.read_bytes(), target.stat().st_mtime_ns), before)
            self.assertNotIn('not a sqlite database', json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', type=Path)
    parser.add_argument('--owner')
    parser.add_argument('--provider')
    args = parser.parse_args()
    if args.state_dir:
        if not args.owner or not args.provider:
            parser.error('Faltan --owner o --provider')
        print(json.dumps(diagnose(args.state_dir, args.owner, args.provider), ensure_ascii=False))
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
