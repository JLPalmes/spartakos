// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import {initialData,migrateData,command,runDue,view} from './dominio.mjs';
const now=Date.parse('2030-01-15T12:00:00Z');
const input={type:'schedule',text:'Preparada',community:'cuaderno',audience:'members',publishAt:'2030-01-15T12:01:00Z',timeZone:'Atlantic/Canary',lateMinutes:15};
const make=()=>command(initialData(),'bruno',input,now).data;
test('una programación privada no publica ni se muestra en otras sesiones',()=>{
 const data=make();assert.equal(data.posts.length,2);assert.equal(view(data,'bruno').scheduled.length,1);
 for(const actor of ['alicia','carla','diego'])assert.equal(view(data,actor).scheduled.length,0);
 assert.equal(runDue(data,now).changed,false);
});
test('publica una sola vez en fecha y conserva audiencia y autor',()=>{
 const data=runDue(make(),now+60000).data,p=data.posts.at(-1);
 assert.equal(p.text,'Preparada');assert.equal(p.author,'bruno');assert.equal(p.audience,'members');
 assert.equal(data.scheduled[0].postId,p.id);assert.equal(runDue(data,now+120000).changed,false);
 assert(!view(data,'diego').posts.some(p=>p.text==='Preparada'));
});
test('revocar permisos bloquea sin publicar y restaurarlos no reactiva el envío',()=>{
 let data=command(make(),'alicia',{type:'set-role',community:'cuaderno',member:'bruno',role:'reader'},now).data;
 data=runDue(data,now+60000).data;assert.equal(data.scheduled[0].status,'blocked');assert.equal(data.posts.length,2);
 data=command(data,'alicia',{type:'set-role',community:'cuaderno',member:'bruno',role:'contributor'},now+70000).data;
 assert.equal(runDue(data,now+80000).changed,false);
});
test('un retraso excesivo vence, y uno autorizado publica',()=>{
 assert.equal(runDue(make(),now+17*60000).data.scheduled[0].status,'expired');
 assert.equal(runDue(make(),now+5*60000).data.scheduled[0].status,'published');
});
test('editar exige propiedad y versión; cancelar impide ejecutar',()=>{
 let data=make();assert.throws(()=>command(data,'alicia',{type:'cancel-schedule',id:'s1',version:1},now),{status:404});
 data=command(data,'bruno',{...input,type:'edit-schedule',id:'s1',version:1,text:'Editada',publishAt:'2030-01-15T13:00:00Z'},now).data;
 assert.throws(()=>command(data,'bruno',{type:'cancel-schedule',id:'s1',version:1},now),{status:409});
 data=command(data,'bruno',{type:'cancel-schedule',id:'s1',version:2},now).data;
 assert.equal(runDue(data,now+3600000).changed,false);assert.equal(data.posts.length,2);
});
test('publicar ahora termina la programación; reintentar no duplica',()=>{
 const data=command(make(),'bruno',{type:'publish-schedule',id:'s1',version:1},now).data;
 assert.equal(data.posts.length,3);assert.equal(data.scheduled[0].status,'published');
 assert.throws(()=>command(data,'bruno',{type:'publish-schedule',id:'s1',version:1},now),{status:409});
 assert.equal(runDue(data,now+60000).changed,false);
});
test('no admite pasado, fecha sin zona, zona inválida ni margen arbitrario',()=>{
 for(const patch of [{publishAt:'2030-01-15T11:00:00Z'},{publishAt:'2030-01-15T13:00:00'},{timeZone:'zona-inventada'},{lateMinutes:-1},{parent:'p2'}]){
  assert.throws(()=>command(initialData(),'bruno',{...input,...patch},now),{status:400});
 }
 assert.throws(()=>command(initialData(),'carla',input,now),{status:403});
});
test('abrir una comunidad no amplía la audiencia programada',()=>{
 let data=make();data.communities[0].visibility='public';data=runDue(data,now+60000).data;
 assert.equal(data.posts.at(-1).audience,'members');assert(!view(data,'diego').posts.some(p=>p.text==='Preparada'));
});
test('migración de versiones anteriores preserva datos y no borra programaciones al reiniciar',()=>{
 for(const version of [1,2]){const old=initialData();old.schema=version;delete old.scheduled;delete old.nextScheduleId;if(version===1)delete old.likes;
 const data=migrateData(old);assert.equal(data.schema,8);assert.deepEqual(data.posts,old.posts);assert.deepEqual(data.scheduled,[]);}
 const scheduled=make();assert.deepEqual(migrateData(scheduled),scheduled);
});
test('un bloqueo puede reprogramarse con nueva fecha; no se ejecuta el intento anterior',()=>{
 let data=runDue(make(),now+17*60000).data;
 data=command(data,'bruno',{...input,type:'edit-schedule',id:'s1',version:2,publishAt:'2030-01-15T13:00:00Z'},now+18*60000).data;
 assert.equal(runDue(data,now+19*60000).changed,false);
 assert.equal(runDue(data,now+3600000).data.scheduled[0].status,'published');
});
