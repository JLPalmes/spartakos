// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import {initialData,migrateData,command,view} from './dominio.mjs';
const saveReply={type:'save-draft',kind:'reply',parent:'p2',targetVersion:1,text:'Respuesta pendiente'};
const saveEdit={type:'save-draft',kind:'edit',editPost:'p1',targetVersion:1,text:'Edición pendiente'};
const reply={type:'publish',parent:'p2',draftId:'d1',draftVersion:1,text:'Respuesta final'};
const edit={type:'edit-post',post:'p1',version:1,draftId:'d1',draftVersion:1,text:'Edición final'};
const run=(data,input,actor='bruno')=>command(data,actor,input).data;
test('respuesta guardada es privada, conserva contexto y se consume una sola vez',()=>{
 const data=run(initialData(),saveReply);const d=data.drafts[0];
 assert.equal(d.kind,'reply');assert.equal(d.community,'cuaderno');assert.equal(d.audience,'members');assert.equal(d.parent,'p2');assert.equal(data.posts.length,2);
 for(const actor of ['alicia','carla','diego']){assert.deepEqual(view(data,actor).drafts,[]);assert(!JSON.stringify(view(data,actor)).includes(saveReply.text));}
 const published=run(data,reply);assert.equal(published.posts[2].parent,'p2');assert.equal(published.posts[2].audience,'members');assert.equal(published.drafts[0].status,'published');
 assert.throws(()=>run(published,reply),{status:409});assert(!view(published,'diego').posts.some(p=>p.text===reply.text));
});
test('edición guardada no modifica el original hasta aplicarse y no se repite',()=>{
 const data=run(initialData(),saveEdit);assert.equal(data.posts[0].text,initialData().posts[0].text);assert.equal(view(data,'alicia').drafts.length,0);
 const applied=run(data,edit);assert.equal(applied.posts[0].text,edit.text);assert.equal(applied.posts[0].version,2);assert.equal(applied.posts.length,2);assert.equal(applied.drafts[0].postId,'p1');
 assert.throws(()=>run(applied,edit),{status:409});
 assert.throws(()=>run(initialData(),saveEdit,'alicia'),{status:403});
});
test('un borrador contextual no puede cambiar tipo, destino, audiencia ni programarse',()=>{
 const data=run(initialData(),saveReply);
 for(const patch of [{parent:'p1'},{audience:'public'},{community:null},{quote:'p1'}])assert.throws(()=>run(data,{...reply,...patch}),{status:400});
 assert.throws(()=>run(data,{...saveReply,id:'d1',version:1,kind:'edit',editPost:'p1'}),{status:400});
 assert.throws(()=>run(data,{...reply,type:'schedule'}),{status:400});
 const editing=run(initialData(),saveEdit);assert.throws(()=>run(editing,{...reply,parent:'p1'}),{status:400});
});
test('cambiar la versión de origen requiere revisión expresa y otra carrera se rechaza',()=>{
 let data=run(initialData(),saveEdit);data=run(data,{type:'edit-post',post:'p1',version:1,text:'Versión de otra pestaña'});
 assert.throws(()=>run(data,edit),{status:409});assert.equal(data.drafts[0].status,'draft');
 assert.throws(()=>run(data,{...saveEdit,id:'d1',version:1,targetVersion:2}),{status:400});
 assert.throws(()=>run(data,{...saveEdit,id:'d1',version:1,reviewedVersion:1}),{status:409});
 data=run(data,{...saveEdit,id:'d1',version:1,reviewedVersion:2,text:'He revisado el original'});
 assert.equal(data.drafts[0].targetVersion,2);assert.equal(data.posts[0].text,'Versión de otra pestaña');
 data=run(data,{...edit,version:2,draftVersion:2});assert.equal(data.posts[0].version,3);
});
test('una respuesta guardada a una versión antigua tampoco se envía sin revisión',()=>{
 let data=run(initialData(),saveReply);data=run(data,{type:'edit-post',post:'p2',version:1,text:'Pregunta corregida'},'alicia');
 assert.throws(()=>run(data,reply),{status:409});
 data=run(data,{...saveReply,id:'d1',version:1,reviewedVersion:2});data=run(data,{...reply,draftVersion:2});
 assert.equal(data.posts[2].parentVersion,2);
});
test('conflicto de borradores no pierde texto y la copia conserva la versión de origen',()=>{
 let data=run(initialData(),saveEdit);data=run(data,{...saveEdit,id:'d1',version:1,text:'Guardada desde otra pestaña'});
 assert.throws(()=>run(data,{...saveEdit,id:'d1',version:1,text:'Mi edición local'}),{status:409});
 data=run(data,{...saveEdit,copyOf:'d1',text:'Mi edición local'});assert.equal(data.drafts[0].text,'Guardada desde otra pestaña');assert.equal(data.drafts[1].text,'Mi edición local');assert.equal(data.drafts[1].editPost,'p1');assert.equal(data.drafts[1].targetVersion,1);
});
test('perder membresía conserva los borradores propios sin recuperar contenido ajeno',()=>{
 let data=run(initialData(),saveReply);data=run(data,{type:'remove',community:'cuaderno',member:'bruno'},'alicia');
 data=run(data,{...saveReply,id:'d1',version:1,text:'Sigo preparando mi respuesta'});
 assert.equal(data.drafts[0].audience,'members');assert(!JSON.stringify(view(data,'bruno')).includes('Este cuaderno es privado.'));
 assert.throws(()=>run(data,{...reply,draftVersion:2}),{status:404});
 assert.throws(()=>run(data,{...saveReply,id:'d1',version:2,reviewedVersion:1}),{status:404});
 assert.throws(()=>run(data,{...saveReply,id:'d1',version:2},'diego'),{status:404});
});
test('retirar el original mantiene el borrador, pero impide aplicarlo o revisarlo',()=>{
 let data=run(initialData(),saveEdit);data=run(data,{type:'withdraw-post',post:'p1',version:1});
 data=run(data,{...saveEdit,id:'d1',version:1,text:'Copia propia conservada'});
 assert.throws(()=>run(data,{...edit,version:2,draftVersion:2}),{status:409});
 assert.throws(()=>run(data,{...saveEdit,id:'d1',version:2,reviewedVersion:2}),{status:404});
 assert.equal(data.posts[0].text,'');assert.equal(data.drafts[0].text,'Copia propia conservada');
});
test('papelera y restauración no reactivan una edición aplicada',()=>{
 let data=run(run(initialData(),saveEdit),edit);
 data=run(data,{type:'trash-draft',id:'d1',version:2});data=run(data,{type:'restore-draft',id:'d1',version:3});
 assert.equal(data.drafts[0].status,'published');assert.equal(data.posts[0].version,2);
 assert.throws(()=>run(data,{...edit,version:2,draftVersion:4}),{status:409});
});
test('migrar esquema siete conserva borradores iniciales y no inventa referencias',()=>{
 const old=run(initialData(),{type:'save-draft',text:'Anterior',audience:'public'});old.schema=7;for(const key of ['kind','parent','editPost','targetVersion'])delete old.drafts[0][key];
 const migrated=migrateData(old);assert.equal(migrated.schema,8);assert.equal(migrated.drafts[0].kind,'publication');assert.equal(migrated.drafts[0].text,'Anterior');assert.equal(migrated.drafts[0].version,1);assert.equal(migrated.drafts[0].targetVersion,null);assert.deepEqual(migrated.posts,old.posts);assert.deepEqual(migrateData(migrated),migrated);
});
test('consumir una edición idéntica no cambia la versión pública ni genera otro resultado',()=>{
 const text=initialData().posts[0].text;const data=run(run(initialData(),{...saveEdit,text}),{...edit,text});
 assert.equal(data.posts[0].version,1);assert.equal(data.posts[0].updatedAt,undefined);assert.equal(data.drafts[0].status,'published');assert.equal(data.drafts[0].postVersion,1);assert.equal(data.posts.length,2);
});
test('borradores de respuesta respetan el límite de tres niveles y no revelan IDs privados',()=>{
 let data=run(initialData(),{type:'publish',parent:'p2',text:'Segundo nivel'});data=run(data,{type:'publish',parent:'p3',text:'Tercer nivel'});
 assert.throws(()=>run(data,{...saveReply,parent:'p4'}),{status:409});
 assert.throws(()=>run(data,saveReply,'diego'),{status:404});
 assert.throws(()=>run(initialData(),{...saveReply,targetVersion:2}),{status:400});
});
test('abrir la comunidad no amplía la respuesta preparada y comentar no permite iniciar temas',()=>{
 let data=run(initialData(),saveReply);data.communities[0].visibility='public';
 data=run(data,{type:'set-role',community:'cuaderno',member:'bruno',role:'commenter'},'alicia');
 data=run(data,reply);assert.equal(data.posts[2].audience,'members');assert.equal(data.posts[2].community,'cuaderno');assert(!view(data,'diego').posts.some(p=>p.id==='p3'));
 assert.throws(()=>run(data,{type:'publish',community:'cuaderno',audience:'public',text:'No puedo iniciar un tema'}),{status:403});
});
test('el autor puede guardar el rescate de su edición después de perder acceso o retirar el cuerpo',()=>{
 let data=run(initialData(),{type:'publish',community:'cuaderno',audience:'members',text:'Propio restringido'});
 data=run(data,{type:'remove',community:'cuaderno',member:'bruno'},'alicia');
 data=run(data,{...saveEdit,editPost:'p3'});assert.equal(data.drafts[0].audience,'members');
 assert.throws(()=>run(data,{...edit,post:'p3'}),{status:404});
 data=run(data,{type:'withdraw-post',post:'p3',version:1});
 data=run(data,{...saveEdit,editPost:'p3',text:'Texto local rescatado'});assert.equal(data.drafts[1].editPost,'p3');assert.equal(data.posts[2].text,'');assert.equal(data.drafts[1].text,'Texto local rescatado');
 assert.equal(view(data,'alicia').drafts.length,0);
});
