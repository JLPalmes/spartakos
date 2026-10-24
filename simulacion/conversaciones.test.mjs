// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import {feedRoots,rootFor,conversationRows} from './conversaciones.mjs';

test('Inicio general y cada comunidad tienen muros distintos, también para contenido público',()=>{
  const posts=[
    {id:'general',parent:null,community:null,audience:'public'},
    {id:'privada-a',parent:null,community:'a',audience:'members'},
    {id:'publica-a',parent:null,community:'a',audience:'public'},
    {id:'publica-b',parent:null,community:'b',audience:'public'},
    {id:'respuesta',parent:'general',community:null,audience:'public'},
  ];
  assert.deepEqual(feedRoots(posts).map(p=>p.id),['general']);
  assert.deepEqual(feedRoots(posts,'a').map(p=>p.id),['publica-a','privada-a']);
  assert.deepEqual(feedRoots(posts,'b').map(p=>p.id),['publica-b']);
});
test('se recorren respuestas profundas sin límite recursivo ni pérdida de contexto',()=>{
  const posts=Array.from({length:2001},(_,i)=>({id:`p${i}`,parent:i?`p${i-1}`:null,community:'a'}));
  const rows=conversationRows(posts,'p0');
  assert.equal(rows.length,2001);assert.equal(rows.at(-1).depth,2000);
  assert.equal(rootFor(posts,'p2000').id,'p0');
});
test('los mensajes conservan orden de conversación y referencia al padre inmediato',()=>{
  const posts=[{id:'r',parent:null},{id:'a',parent:'r'},{id:'b',parent:'r'},{id:'a1',parent:'a'}];
  assert.deepEqual(conversationRows(posts,'r').map(({post,depth})=>[post.id,depth]),[['r',0],['a',1],['a1',2],['b',1]]);
  assert.equal(rootFor(posts,'a1').id,'r');
});
test('ancestros no disponibles o ciclos no producen bucles ni contexto inventado',()=>{
  const posts=[{id:'a',parent:'b'},{id:'b',parent:'a'},{id:'c',parent:'ausente'}];
  assert.equal(rootFor(posts,'a'),null);assert.equal(rootFor(posts,'c'),null);
  assert.equal(rootFor(posts,'desconocido'),null);assert.deepEqual(conversationRows(posts,'desconocido'),[]);
  assert.equal(conversationRows(posts,'a').length,2);
});
