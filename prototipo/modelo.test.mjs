// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import { initialState, transition as step } from './modelo.mjs';

test('guardar no cambia publicaciones, seguimiento ni permisos', () => {
  const before = initialState();
  const after = step(before, {type: 'save', id: 'p1'});
  assert.deepEqual(after.saved, ['p1']);
  assert.deepEqual(after.posts, before.posts);
  assert.deepEqual(after.community, before.community);
  assert.deepEqual(after.followed, []);
  assert.deepEqual(before.saved, []);
});
test('seguir no concede acceso ni altera el censo', () => {
  const state = step(initialState(), {type: 'follow', id: 'ciencia'});
  assert.deepEqual(state.community, initialState().community);
});
test('publicar exige audiencia válida y texto', () => {
  assert.throws(() => step(initialState(), {type: 'publish', audience: 'unknown', text: 'hola'}));
  assert.throws(() => step(initialState(), {type: 'publish', audience: 'public', text: ' '}));
  const s = step(initialState(), {type: 'publish', audience: 'community', text: 'Privado'});
  assert.equal(s.posts[0].audience, 'community');
});
test('importar dos veces es idempotente y no fabrica relaciones activas', () => {
  let s = step(initialState(), {type: 'import-demo'});
  s = step(s, {type: 'import-demo'});
  assert.equal(s.imported, true);
  assert.deepEqual(s.followed, []);
  assert.deepEqual(s.posts, []);
});
test('sin consentimiento y con solo mayoría no se abre', () => {
  let s = step(initialState(), {type: 'propose-open'});
  assert.throws(() => step(s, {type: 'open'}));
  for (const member of ['alicia', 'bruno']) s = step(s, {type: 'consent', member, version: s.community.version, value: true});
  assert.throws(() => step(s, {type: 'open'}));
});
test('una negativa cierra la propuesta y no puede reutilizarse', () => {
  let s = step(initialState(), {type: 'propose-open'});
  s = step(s, {type: 'consent', member: 'carla', version: s.community.version, value: false});
  assert.equal(s.community.visibility, 'private');
  assert.equal(s.community.proposal, false);
  assert.throws(() => step(s, {type: 'consent', member: 'alicia', version: s.community.version, value: true}));
});
test('expulsar a quien no consiente no permite eludir unanimidad', () => {
  let s = step(initialState(), {type: 'propose-open'});
  s = step(s, {type: 'remove-member', member: 'carla'});
  s = step(s, {type: 'propose-open'});
  for (const member of ['alicia', 'bruno']) s = step(s, {type: 'consent', member, version: s.community.version, value: true});
  assert.throws(() => step(s, {type: 'open'}));
  assert.deepEqual(s.community.protected, ['carla']);
});
test('cerrar por negativa y expulsar después tampoco permite eludir protección', () => {
  let s = step(initialState(), {type: 'propose-open'});
  s = step(s, {type: 'consent', member: 'carla', version: s.community.version, value: false});
  s = step(s, {type: 'remove-member', member: 'carla'});
  s = step(s, {type: 'propose-open'});
  for (const member of ['alicia', 'bruno']) s = step(s, {type: 'consent', member, version: s.community.version, value: true});
  assert.throws(() => step(s, {type: 'open'}));
});
test('propuesta nueva rechaza consentimiento de la anterior', () => {
  let s = step(initialState(), {type: 'propose-open'});
  const oldVersion = s.community.version;
  s = step(s, {type: 'propose-open'});
  assert.throws(() => step(s, {type: 'consent', member: 'alicia', version: oldVersion, value: true}));
});
test('unanimidad abre el futuro sin ampliar audiencia del pasado', () => {
  let s = step(initialState(), {type: 'publish', text: 'Anterior', audience: 'community'});
  s = step(s, {type: 'propose-open'});
  for (const member of s.community.members) s = step(s, {type: 'consent', member, version: s.community.version, value: true});
  s = step(s, {type: 'open'});
  assert.equal(s.community.visibility, 'public');
  assert.equal(s.posts[0].audience, 'community');
});
