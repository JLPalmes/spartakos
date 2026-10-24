// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import {initialData,migrateData,command,view,runDue} from './dominio.mjs';
import {replyDepth} from './conversaciones.mjs';
function thread(){let data=initialData();for(const parent of ['p2','p3'])data=command(data,'bruno',{type:'publish',parent,text:'Continuación'}).data;return data;}
test('se admiten tres niveles y se rechaza una cuarta respuesta sin mutación',()=>{
 const data=thread();assert.equal(replyDepth(data.posts,'p2'),0);assert.equal(replyDepth(data.posts,'p4'),2);
 assert.throws(()=>command(data,'alicia',{type:'publish',parent:'p4',text:'Cuarto nivel'}),{status:409});
 assert.equal(data.posts.length,4);assert.equal(data.nextId,5);
});
test('citar el último nivel crea una publicación propia con enlace y aviso solo al citado',()=>{
 const data=command(thread(),'alicia',{type:'publish',text:'Nueva conversación',quote:'p4',community:'cuaderno',audience:'members'}).data;
 const post=data.posts.at(-1);assert.equal(post.parent,null);assert.equal(post.quote,'p4');assert.equal(post.author,'alicia');
 assert.equal(replyDepth(data.posts,post.id),0);assert.equal(view(data,'bruno').notices.length,1);
 for(const actor of ['alicia','carla','diego'])assert.equal(view(data,actor).notices.length,0);
 const read=command(data,'bruno',{type:'read-notice',id:post.id}).data;assert.equal(view(read,'bruno').notices[0].read,true);
 assert.throws(()=>command(data,'carla',{type:'read-notice',id:post.id}),{status:404});
});
test('una cita privada no puede trasladarse a público ni a otra comunidad',()=>{
 const data=thread();
 for(const destination of [{audience:'public'},{community:'cuaderno',audience:'public'},{community:'otro',audience:'members'}])assert.throws(()=>command(data,'alicia',{type:'publish',quote:'p4',text:'Cita',...destination}));
 assert.throws(()=>command(data,'diego',{type:'publish',quote:'p4',text:'Cita',audience:'public'}),{status:404});
 assert.throws(()=>command(data,'carla',{type:'publish',quote:'p4',text:'Cita',community:'cuaderno',audience:'members'}),{status:403});
});
test('la cita pública puede crear una publicación general y admite un nuevo hilo de tres niveles',()=>{
 let data=command(initialData(),'alicia',{type:'publish',quote:'p1',text:'Mi publicación',audience:'public'}).data;
 assert.equal(data.posts.at(-1).quote,'p1');assert.equal(view(data,'bruno').notices.length,1);
 for(const parent of ['p3','p4'])data=command(data,'bruno',{type:'publish',parent,text:'Respuesta'}).data;
 assert.throws(()=>command(data,'bruno',{type:'publish',parent:'p5',text:'No'}),{status:409});
 assert.throws(()=>command(data,'bruno',{type:'publish',parent:'p1',quote:'p1',text:'No'}),{status:400});
});
test('el aviso no revela una cita de la que el citado perdió acceso; citarse a uno mismo no avisa',()=>{
 let data=command(thread(),'alicia',{type:'publish',quote:'p4',text:'Cita privada',community:'cuaderno',audience:'members'}).data;
 data=command(data,'alicia',{type:'remove',community:'cuaderno',member:'bruno'}).data;
 assert.deepEqual(view(data,'bruno').notices,[]);
 data=command(initialData(),'bruno',{type:'publish',quote:'p1',text:'Autocita',audience:'public'}).data;
 assert.deepEqual(view(data,'bruno').notices,[]);
});
test('cita programada avisa al publicarse, no al preparar ni cancelar el envío',()=>{
 const now=Date.parse('2030-01-01T10:00:00Z');
 const input={type:'schedule',quote:'p1',text:'Cita futura',audience:'public',publishAt:'2030-01-01T10:01:00Z',timeZone:'Atlantic/Canary',lateMinutes:15};
 let data=command(initialData(),'alicia',input,now).data;
 assert.deepEqual(view(data,'bruno').notices,[]);assert.equal(data.scheduled[0].publication.quote,'p1');
 const published=runDue(data,now+60000).data;assert.equal(view(published,'bruno').notices.length,1);
 data=command(data,'alicia',{type:'cancel-schedule',id:'s1',version:1},now).data;
 assert.deepEqual(view(runDue(data,now+60000).data,'bruno').notices,[]);
});
test('historial profundo se conserva; referencias cíclicas o ausentes no admiten nuevas respuestas',()=>{
 const data=thread();data.posts.push({id:'antiguo',parent:'p4',author:'bruno',text:'Histórico',community:'cuaderno',audience:'members'});
 const old=structuredClone(data);old.schema=3;delete old.seenQuotes;
 const migrated=migrateData(old);for(const original of old.posts){const current=migrated.posts.find(p=>p.id===original.id);for(const [key,value] of Object.entries(original))assert.deepEqual(current[key],value);}assert.equal(replyDepth(migrated.posts,'antiguo'),3);
 assert.throws(()=>command(migrated,'bruno',{type:'publish',parent:'antiguo',text:'No'}),{status:409});
 assert.equal(replyDepth([{id:'a',parent:'a'}],'a'),Infinity);assert.equal(replyDepth([],'ausente'),Infinity);
});
