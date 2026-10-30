// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import {initialData,migrateData,command,refreshLikeCounts,view} from './dominio.mjs';
const start=Date.parse('2030-01-01T12:30:00Z'),hour=Date.parse('2030-01-01T13:00:00Z');
const react=(data,actor,active,at,post='p1')=>command(data,actor,{type:'like',post,active},at).data;
const count=(data,actor='alicia',id='p1')=>view(data,actor).posts.find(p=>p.id===id);
test('la elección propia es inmediata y el total espera al corte común',()=>{
 const data=react(initialData(start),'bruno',true,start+1000);
 assert.equal(count(data,'bruno').likedByMe,true);assert.equal(count(data).likeCount,null);
 assert.equal(refreshLikeCounts(data,hour-1).changed,false);
 const result=refreshLikeCounts(data,hour);assert.equal(count(result.data).likeCount,1);
 assert.equal(count(result.data,'diego').likeCount,1);assert.equal(count(result.data).likesUpdatedAt,new Date(hour).toISOString());
});
test('marcar, retirar y repetir no inflan ni publican cambios antes de tiempo',()=>{
 let data=initialData(start);
 data=react(data,'bruno',true,start+1000);data=react(data,'bruno',true,start+2000);data=react(data,'bruno',false,start+3000);
 data=refreshLikeCounts(data,hour).data;assert.equal(count(data).likeCount,0);
 data=react(data,'carla',true,hour+1000);assert.equal(count(data).likeCount,0);
 data=refreshLikeCounts(data,hour+3600000).data;assert.equal(count(data).likeCount,1);
 data=react(data,'carla',false,hour+3601000);assert.equal(count(data).likeCount,1);
 assert.equal(count(refreshLikeCounts(data,hour+7200000).data).likeCount,0);
});
test('un cálculo tardío excluye reacciones en o después del corte',()=>{
 let data=react(initialData(start),'bruno',true,hour-1);
 data=react(data,'carla',true,hour);data=react(data,'alicia',true,hour+1000);
 data=refreshLikeCounts(data,hour+2000).data;assert.equal(count(data).likeCount,1);
 assert.equal(data.likeBatch.generatedAt,new Date(hour+2000).toISOString());
 assert.equal(count(refreshLikeCounts(data,hour+3600000).data).likeCount,3);
});
test('el contador de contenido privado solo llega a sus lectores autorizados',()=>{
 let data=react(initialData(start),'carla',true,start+1000,'p2');data=refreshLikeCounts(data,hour).data;
 assert.equal(count(data,'alicia','p2').likeCount,1);assert.equal(count(data,'diego','p2'),undefined);
 assert(!Object.hasOwn(count(data,'alicia','p2'),'likes'));
});
test('migrar conserva reacciones previas sin inventar una instantánea histórica',()=>{
 const old=initialData(start);old.schema=4;delete old.likeBatch;old.likes={p1:['bruno','carla']};
 let data=migrateData(old,start);assert.deepEqual(data.likes,old.likes);assert.equal(count(data).likeCount,null);
 data=react(data,'carla',false,start+1000);data=refreshLikeCounts(data,hour).data;
 assert.equal(count(data).likeCount,1);assert.deepEqual(migrateData(data,hour+1000),data);
});
test('tras una interrupción se conserva la instantánea hasta ejecutar otro corte',()=>{
 let data=react(initialData(start),'bruno',true,start+1000);data=refreshLikeCounts(data,hour).data;
 data=react(data,'carla',true,hour+1000);
 assert.equal(count(data).likeCount,1);assert.equal(count(data).likesUpdatedAt,new Date(hour).toISOString());
 const resumed=refreshLikeCounts(data,hour+2*3600000+10000).data;
 assert.equal(count(resumed).likeCount,2);assert.equal(count(resumed).likesUpdatedAt,new Date(hour+2*3600000).toISOString());
 assert.deepEqual(resumed.likeBatch.changes,[]);
});
test('un post posterior al corte no aparenta disponer de recuento previo',()=>{
 let data=refreshLikeCounts(initialData(start),hour).data;
 data=command(data,'bruno',{type:'publish',text:'Nuevo',audience:'public'},hour+1000).data;
 assert.equal(count(data,'alicia','p3').likeCount,null);
 assert.equal(count(refreshLikeCounts(data,hour+3600000).data,'alicia','p3').likeCount,0);
});
test('el corte es idempotente, persiste y no retrocede al cambiar el reloj',()=>{
 const data=refreshLikeCounts(initialData(start),hour).data;
 assert.equal(refreshLikeCounts(data,hour+1000).changed,false);assert.equal(refreshLikeCounts(data,hour-3600000).changed,false);
 assert.deepEqual(migrateData(JSON.parse(JSON.stringify(data)),hour+1000),data);
});
