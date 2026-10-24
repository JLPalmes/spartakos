// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import {initialData,migrateData,command,view,runDue,refreshLikeCounts} from './dominio.mjs';
const edit=(data,text='Texto corregido',version=1)=>command(data,'bruno',{type:'edit-post',post:'p1',version,text}).data;
test('solo el autor edita con versión vigente y conserva contexto e identidad',()=>{
 const original=initialData();
 assert.throws(()=>command(original,'alicia',{type:'edit-post',post:'p1',version:1,text:'Suplantar'}),{status:403});
 const data=edit(original);const post=data.posts[0];assert.equal(post.version,2);assert.equal(post.author,'bruno');assert.equal(post.community,null);assert.equal(post.audience,'public');assert.equal(post.text,'Texto corregido');
 assert.throws(()=>edit(data,'Obsoleto'),{status:409});assert.equal(data.posts[0].text,'Texto corregido');
 assert.throws(()=>command(data,'bruno',{type:'edit-post',post:'p1',version:2,text:'x',audience:'members'}),{status:400});
 const noOp=edit(data,post.text,2);assert.equal(noOp.revision,data.revision);assert.equal(noOp.posts[0].version,2);
});
test('respuestas, citas y reacción propia mantienen referencia a la versión anterior',()=>{
 let data=command(initialData(),'carla',{type:'like',post:'p1',active:true}).data;
 data=command(data,'alicia',{type:'publish',parent:'p1',text:'Respuesta previa'}).data;
 data=command(data,'alicia',{type:'publish',quote:'p1',audience:'public',text:'Cita previa'}).data;
 data=edit(data);const state=view(data,'carla');
 assert.equal(state.posts.find(p=>p.id==='p1').likedVersion,1);assert.equal(state.posts.find(p=>p.id==='p1').likedByMe,true);
 assert.equal(state.posts.find(p=>p.id==='p3').parentChanged,true);assert.equal(state.posts.find(p=>p.id==='p4').quoteVersion,1);
 data=command(data,'carla',{type:'like',post:'p1',active:true}).data;assert.equal(view(data,'carla').posts[0].likedVersion,1);
 data=command(data,'carla',{type:'like',post:'p1',active:false}).data;data=command(data,'carla',{type:'like',post:'p1',active:true}).data;
 assert.equal(view(data,'carla').posts[0].likedVersion,2);
});
test('retirar vacía el cuerpo y conserva las respuestas independientes sin duplicar',()=>{
 let data=command(initialData(),'alicia',{type:'publish',parent:'p1',text:'Respuesta ajena'}).data;
 data=command(data,'bruno',{type:'withdraw-post',post:'p1',version:1}).data;
 assert.equal(data.posts[0].text,'');assert.equal(data.posts[0].withdrawn,true);assert.equal(data.posts[1].text,initialData().posts[1].text);
 assert.equal(data.posts[2].text,'Respuesta ajena');assert.equal(data.posts[2].parent,'p1');
 assert.throws(()=>command(data,'bruno',{type:'withdraw-post',post:'p1',version:1}),{status:409});
 assert.throws(()=>edit(data,'Volver',2),{status:409});
 assert.throws(()=>command(data,'alicia',{type:'publish',parent:'p1',text:'Nueva'}),{status:409});
 assert.throws(()=>command(data,'alicia',{type:'publish',quote:'p1',text:'Citar retirado',audience:'public'}),{status:409});
});
test('perder acceso impide editar pero el autor conserva la retirada de su texto',()=>{
 let data=command(initialData(),'bruno',{type:'publish',community:'cuaderno',audience:'members',text:'Privado propio'}).data;
 data=command(data,'alicia',{type:'remove',community:'cuaderno',member:'bruno'}).data;
 assert.throws(()=>command(data,'bruno',{type:'edit-post',post:'p3',version:1,text:'No'}),{status:403});
 assert.equal(view(data,'bruno').ownUnavailablePosts[0].text,'Privado propio');assert(!JSON.stringify(view(data,'bruno')).includes('Este cuaderno es privado.'));assert.deepEqual(view(data,'diego').ownUnavailablePosts,[]);
 assert.throws(()=>command(data,'diego',{type:'withdraw-post',post:'p3',version:1}),{status:404});
 data=command(data,'bruno',{type:'withdraw-post',post:'p3',version:1}).data;assert.equal(data.posts[2].text,'');assert.equal(data.posts[2].audience,'members');
});
test('retirada elimina elección y total visible y no deja cuerpos en avisos',()=>{
 let data=command(initialData(),'carla',{type:'like',post:'p1',active:true}).data;
 data=command(data,'alicia',{type:'publish',quote:'p1',audience:'public',text:'Mi comentario independiente'}).data;
 assert.equal(view(data,'bruno').notices.length,1);
 data=command(data,'bruno',{type:'withdraw-post',post:'p1',version:1}).data;
 const state=view(data,'carla');assert.equal(state.posts[0].likedByMe,false);assert.equal(state.posts[0].likeCount,null);assert.equal(state.posts[0].text,'');
 assert.equal(view(data,'bruno').notices.length,0);
 assert.throws(()=>command(data,'carla',{type:'like',post:'p1',active:true}),{status:409});
 data=refreshLikeCounts(data,Date.now()+7200000).data;assert.equal(view(data,'carla').posts[0].likeCount,null);
});
test('cita programada se bloquea si el original fue retirado sin publicar ni avisar',()=>{
 const now=Date.parse('2030-01-01T10:00:00Z');
 let data=command(initialData(now),'alicia',{type:'schedule',quote:'p1',text:'Cita futura',audience:'public',publishAt:'2030-01-01T11:00:00Z',timeZone:'Atlantic/Canary',lateMinutes:15},now).data;
 const edited=command(data,'bruno',{type:'edit-post',post:'p1',version:1,text:'Original actualizado'},now+500).data;const executed=runDue(edited,now+3600000).data;assert.equal(executed.posts.at(-1).quoteVersion,1);assert.equal(executed.posts[0].version,2);
 data=command(data,'bruno',{type:'withdraw-post',post:'p1',version:1},now+1000).data;
 data=runDue(data,now+3600000).data;assert.equal(data.scheduled[0].status,'blocked');assert.equal(data.posts.length,2);assert.equal(view(data,'bruno').notices.length,0);
});
test('migrar versiones previas conserva cuerpos y referencias sin inventar historial',()=>{
 const old=initialData();old.schema=6;delete old.likeVersions;delete old.posts[0].version;old.likes.p1=['carla'];
 const data=migrateData(old);assert.equal(data.schema,7);assert.equal(data.posts[0].text,old.posts[0].text);assert.equal(data.posts[0].version,1);assert.equal(data.likeVersions.p1.carla,1);assert.equal(data.posts[0].history,undefined);
});
test('retirar una cita suprime su aviso, sin retirar el original citado',()=>{
 let data=command(initialData(),'alicia',{type:'publish',quote:'p1',audience:'public',text:'Mi cita'}).data;
 data=command(data,'alicia',{type:'withdraw-post',post:'p3',version:1}).data;
 assert.equal(view(data,'bruno').notices.length,0);assert.equal(data.posts[0].withdrawn,undefined);assert.equal(data.posts[2].quote,null);
});
