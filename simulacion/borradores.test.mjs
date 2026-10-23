// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import {initialData,migrateData,command,view} from './dominio.mjs';
const input={type:'save-draft',text:'  Texto pendiente\ncon formato  ',community:'cuaderno',audience:'members',quote:'p2'};
const save=()=>command(initialData(),'bruno',input).data;
test('guardar es privado y no publica, programa ni avisa; conserva texto y cita',()=>{
 const data=save();assert.equal(data.posts.length,2);assert.equal(data.scheduled.length,0);
 const saved=view(data,'bruno').drafts[0];assert.equal(saved.text,input.text);assert.equal(saved.quote,'p2');
 for(const actor of ['alicia','carla','diego']){assert.deepEqual(view(data,actor).drafts,[]);assert.deepEqual(view(data,actor).notices,[]);}
});
test('el borrador se conserva editable sin permisos y no se convierte en público',()=>{
 let data=command(save(),'alicia',{type:'remove',community:'cuaderno',member:'bruno'}).data;
 data=command(data,'bruno',{...input,id:'d1',version:1,text:'Continúo escribiendo sin acceso'}).data;
 assert.equal(view(data,'bruno').drafts[0].audience,'members');
 assert.throws(()=>command(data,'bruno',{type:'publish',draftId:'d1',draftVersion:2,...input,type:'publish'}),{status:404});
 assert.throws(()=>command(data,'bruno',{...input,id:'d1',version:2,community:null,audience:'public'}),{status:400});
});
test('los conflictos no sobrescriben y se puede guardar como copia',()=>{
 let data=command(save(),'bruno',{...input,id:'d1',version:1,text:'Versión de otra pestaña'}).data;
 assert.throws(()=>command(data,'bruno',{...input,id:'d1',version:1,text:'Mi texto'}),{status:409});
 data=command(data,'bruno',{...input,copyOf:'d1',text:'Mi texto'}).data;
 assert.equal(data.drafts[0].text,'Versión de otra pestaña');assert.equal(data.drafts[1].text,'Mi texto');
 assert.throws(()=>command(data,'alicia',{...input,id:'d1',version:2}),{status:404});
});
test('publicar utiliza el borrador una sola vez y conserva la versión publicada',()=>{
 const publication={type:'publish',draftId:'d1',draftVersion:1,community:'cuaderno',audience:'members',quote:'p2',text:'Texto final'};
 const data=command(save(),'bruno',publication).data;
 assert.equal(data.drafts[0].status,'published');assert.equal(data.drafts[0].text,'Texto final');assert.equal(data.drafts[0].postId,'p3');
 assert.throws(()=>command(data,'bruno',publication),{status:409});assert.equal(view(data,'alicia').notices.length,1);
 const copied=command(data,'bruno',{...input,copyOf:'d1',text:'Nueva versión conservada'}).data;assert.equal(copied.drafts[1].status,'draft');assert.equal(copied.posts.length,3);
});
test('programar traslada una vez a pendientes; un error mantiene el borrador',()=>{
 const now=Date.parse('2030-01-01T10:00:00Z');
 const scheduling={type:'schedule',draftId:'d1',draftVersion:1,community:'cuaderno',audience:'members',quote:'p2',text:'Programada',timeZone:'Atlantic/Canary',lateMinutes:15,publishAt:'2030-01-01T11:00:00Z'};
 const initial=save();assert.throws(()=>command(initial,'bruno',{...scheduling,publishAt:'incorrecta'},now),{status:400});assert.equal(initial.drafts[0].status,'draft');
 const data=command(initial,'bruno',scheduling,now).data;
 assert.equal(data.drafts[0].status,'scheduled');assert.equal(data.drafts[0].scheduleId,'s1');assert.equal(data.posts.length,2);
 assert.throws(()=>command(data,'bruno',scheduling,now),{status:409});
});
test('migrar preserva datos y guardar rechaza citas privadas fuera de su comunidad',()=>{
 const old=initialData();old.schema=5;delete old.drafts;delete old.nextDraftId;
 const data=migrateData(old);assert.equal(data.schema,6);assert.deepEqual(data.posts,old.posts);assert.deepEqual(data.drafts,[]);
 assert.throws(()=>command(data,'bruno',{...input,community:null,audience:'public'}),{status:403});
 assert.throws(()=>command(data,'bruno',{...input,text:' '}),{status:400});
 const saved=save();assert.deepEqual(migrateData(saved).drafts,saved.drafts);
});
