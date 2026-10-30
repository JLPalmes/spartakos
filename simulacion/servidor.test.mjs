// SPDX-License-Identifier: AGPL-3.0-or-later
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,rm,readFile,writeFile} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {request as httpRequest} from 'node:http';
import {createSimulationServer} from './servidor.mjs';
import {initialData} from './dominio.mjs';

async function fixture(t,{clock}={}){
  const directory=await mkdtemp(path.join(os.tmpdir(),'spartakos-http-'));
  let server,url;
  async function start(){server=await createSimulationServer({directory,clock});await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));url=`http://127.0.0.1:${server.address().port}`;}
  async function stop(){server.closeAllConnections();await new Promise(resolve=>server.close(resolve));}
  await start();
  t.after(async()=>{await stop();await rm(directory,{recursive:true,force:true});});
  async function request(route,{token,method='GET',body,origin,headers={}}={}){
    const response=await fetch(url+route,{method,headers:{...(token?{Authorization:`Bearer ${token}`}:{ }),...(body?{'Content-Type':'application/json'}:{ }),...(origin?{Origin:origin}:{}),...headers},...(body?{body:JSON.stringify(body)}:{})});
    return {status:response.status,headers:response.headers,data:await response.json()};
  }
  async function login(account){const r=await request('/api/sessions',{method:'POST',body:{account}});assert.equal(r.status,201);return r.data.token;}
  const tokens=Object.fromEntries(await Promise.all(['alicia','bruno','carla','diego'].map(async actor=>[actor,await login(actor)])));
  const foreignHost=()=>new Promise((resolve,reject)=>{const req=httpRequest(`${url}/api/state`,{headers:{Host:'otro.example',Authorization:`Bearer ${tokens.alicia}`}},response=>{response.resume();resolve(response.statusCode);});req.on('error',reject);req.end();});
  return {request,login,tokens,directory,foreignHost,restart:async seed=>{await stop();if(seed)await writeFile(path.join(directory,'estado.json'),JSON.stringify(seed));await start();},cmd:(actor,body)=>request('/api/commands',{method:'POST',token:tokens[actor],body})};
}
test('las sesiones son independientes y el contenido privado no sale hacia Diego',async t=>{
  const f=await fixture(t);
  const a=await f.request('/api/state',{token:f.tokens.alicia});
  const d=await f.request('/api/state',{token:f.tokens.diego});
  assert.equal(a.data.user.id,'alicia');assert.equal(d.data.user.id,'diego');
  assert(a.data.posts.some(p=>p.id==='p2'));assert(!d.data.posts.some(p=>p.id==='p2'));
  assert.deepEqual(d.data.communities,[]);
  assert(!JSON.stringify(d.data).includes('Cuaderno compartido'));
  assert.equal((await f.request('/api/state')).status,401);
});
test('el servidor rechaza publicación y comentario de una lectora, sin alterar el estado',async t=>{
  const f=await fixture(t);
  assert.equal((await f.cmd('carla',{type:'publish',community:'cuaderno',audience:'members',text:'No autorizado'})).status,403);
  assert.equal((await f.cmd('carla',{type:'publish',parent:'p2',text:'Tampoco autorizado'})).status,403);
  assert.equal((await f.request('/api/state',{token:f.tokens.alicia})).data.revision,0);
});
test('leer y comentar es un permiso diferente de iniciar publicaciones',async t=>{
  const f=await fixture(t);
  assert.equal((await f.cmd('alicia',{type:'set-role',community:'cuaderno',member:'carla',role:'commenter'})).status,200);
  assert.equal((await f.cmd('carla',{type:'publish',parent:'p2',text:'Sí puedo responder'})).status,200);
  assert.equal((await f.cmd('carla',{type:'publish',community:'cuaderno',audience:'members',text:'No puedo iniciar tema'})).status,403);
  const d=await f.request('/api/state',{token:f.tokens.diego});assert(!d.data.posts.some(p=>p.text==='Sí puedo responder'));
});
test('no se revela existencia de objetos privados al consultar sus IDs',async t=>{
  const f=await fixture(t);
  for(const body of [{type:'save',post:'p2'},{type:'publish',parent:'p2',text:'intrusión'},{type:'propose',community:'cuaderno'}])assert.equal((await f.cmd('diego',body)).status,404);
});
test('los guardados no se comparten con otras cuentas ni con el autor',async t=>{
  const f=await fixture(t);await f.cmd('carla',{type:'save',post:'p1'});
  assert.deepEqual((await f.request('/api/state',{token:f.tokens.carla})).data.saved,['p1']);
  assert.deepEqual((await f.request('/api/state',{token:f.tokens.bruno})).data.saved,[]);
});
test('no se puede suplantar al autor ni a otra persona en un consentimiento',async t=>{
  const f=await fixture(t);
  const r=await f.cmd('bruno',{type:'publish',audience:'public',text:'Texto de Bruno',author:'alicia'});
  assert.equal(r.data.state.posts.at(-1).author,'bruno');
  await f.cmd('alicia',{type:'propose',community:'cuaderno'});
  const consent=await f.cmd('bruno',{type:'consent',community:'cuaderno',version:1,accept:true,member:'carla'});
  assert.deepEqual(consent.data.state.communities[0].proposal.consents,['bruno']);
});
test('solo administración propone y la mayoría no abre; unanimidad conserva historial privado',async t=>{
  const f=await fixture(t);
  assert.equal((await f.cmd('bruno',{type:'propose',community:'cuaderno'})).status,403);
  await f.cmd('alicia',{type:'propose',community:'cuaderno'});
  for(const actor of ['alicia','bruno'])await f.cmd(actor,{type:'consent',community:'cuaderno',version:1,accept:true});
  assert.equal((await f.cmd('alicia',{type:'open',community:'cuaderno',version:1})).status,409);
  await f.cmd('carla',{type:'consent',community:'cuaderno',version:1,accept:true});
  assert.equal((await f.cmd('alicia',{type:'open',community:'cuaderno',version:1})).status,200);
  await f.cmd('bruno',{type:'publish',community:'cuaderno',audience:'public',text:'Publicación futura pública'});
  const d=await f.request('/api/state',{token:f.tokens.diego});
  assert.equal(d.data.communities[0].visibility,'public');
  assert(!d.data.posts.some(p=>p.id==='p2'));assert(d.data.posts.some(p=>p.text==='Publicación futura pública'));
  // Comentar una aportación antigua conserva su audiencia aunque el espacio se haya abierto.
  await f.cmd('bruno',{type:'publish',parent:'p2',text:'Respuesta al pasado'});
  assert(!(await f.request('/api/state',{token:f.tokens.diego})).data.posts.some(p=>p.text==='Respuesta al pasado'));
});
test('una negativa y expulsión posterior no permiten eludir el censo',async t=>{
  const f=await fixture(t);
  await f.cmd('alicia',{type:'propose',community:'cuaderno'});
  await f.cmd('carla',{type:'consent',community:'cuaderno',version:1,accept:false});
  await f.cmd('alicia',{type:'remove',community:'cuaderno',member:'carla'});
  await f.cmd('alicia',{type:'propose',community:'cuaderno'});
  const a=await f.request('/api/state',{token:f.tokens.alicia});const version=a.data.communities[0].proposal.version;
  for(const actor of ['alicia','bruno'])await f.cmd(actor,{type:'consent',community:'cuaderno',version,accept:true});
  assert.equal((await f.cmd('alicia',{type:'open',community:'cuaderno',version})).status,409);
  const c=await f.request('/api/state',{token:f.tokens.carla});
  assert(!c.data.posts.some(p=>p.id==='p2'));assert.equal(c.data.formerProposals.length,1);
  assert.equal((await f.cmd('carla',{type:'consent',community:'cuaderno',version:1,accept:true})).status,409);
  assert.equal((await f.cmd('carla',{type:'consent',community:'cuaderno',version,accept:true})).status,200);
});
test('un borrador restringido no amplía audiencia aunque la comunidad se abra',async t=>{
  const f=await fixture(t);
  assert.equal((await f.cmd('bruno',{type:'publish',community:'cuaderno',audience:'public',text:'No público'})).status,400);
  await f.cmd('alicia',{type:'propose',community:'cuaderno'});
  for(const actor of ['alicia','bruno','carla'])await f.cmd(actor,{type:'consent',community:'cuaderno',version:1,accept:true});
  await f.cmd('alicia',{type:'open',community:'cuaderno',version:1});
  assert.equal((await f.cmd('bruno',{type:'publish',community:'cuaderno',audience:'members',text:'Mi borrador seguía privado'})).status,200);
  assert(!(await f.request('/api/state',{token:f.tokens.diego})).data.posts.some(p=>p.text==='Mi borrador seguía privado'));
});
test('revocar publicación bloquea el envío al destino sin convertirlo en público',async t=>{
  const f=await fixture(t);
  await f.cmd('alicia',{type:'set-role',community:'cuaderno',member:'bruno',role:'reader'});
  const r=await f.cmd('bruno',{type:'publish',community:'cuaderno',audience:'members',text:'Borrador pendiente'});
  assert.equal(r.status,403);
  assert(!(await f.request('/api/state',{token:f.tokens.diego})).data.posts.some(p=>p.text==='Borrador pendiente'));
});
test('las escrituras simultáneas no se pierden y se conservan los caracteres Unicode',async t=>{
  const f=await fixture(t);
  const results=await Promise.all(Array.from({length:16},(_,i)=>f.cmd(i%2?'alicia':'bruno',{type:'publish',audience:'public',text:`Simultánea ${i} · 🌱 ñ`})));assert(results.every(r=>r.status===200));
  const s=(await f.request('/api/state',{token:f.tokens.alicia})).data;
  assert.equal(s.posts.length,18);assert.equal(new Set(s.posts.map(p=>p.id)).size,18);assert.equal(s.revision,16);
  assert(s.posts.some(p=>p.text==='Simultánea 15 · 🌱 ñ'));
});
test('datos y guardados sobreviven al reinicio; las sesiones no se guardan en disco',async t=>{
  const f=await fixture(t);
  await f.cmd('bruno',{type:'publish',audience:'public',text:'Persistente'});
  await f.cmd('bruno',{type:'save',post:'p1'});
  const raw=await readFile(path.join(f.directory,'estado.json'),'utf8');assert(!raw.includes(f.tokens.bruno));
  await f.restart();assert.equal((await f.request('/api/state',{token:f.tokens.bruno})).status,401);
  const token=await f.login('bruno');const s=(await f.request('/api/state',{token})).data;
  assert(s.posts.some(p=>p.text==='Persistente'));assert.deepEqual(s.saved,['p1']);
});
test('exportación por cuenta y cierre de sesión no afectan a las demás',async t=>{
  const f=await fixture(t);await f.cmd('bruno',{type:'publish',community:'cuaderno',audience:'members',text:'Aportación propia'});
  const exported=(await f.request('/api/export',{token:f.tokens.bruno})).data;
  assert(exported.posts.every(p=>p.author==='bruno'));assert(!JSON.stringify(exported).includes(f.tokens.bruno));
  await f.request('/api/session',{token:f.tokens.bruno,method:'DELETE'});
  assert.equal((await f.request('/api/state',{token:f.tokens.bruno})).status,401);
  assert.equal((await f.request('/api/state',{token:f.tokens.alicia})).status,200);
});
test('se rechazan orígenes y hosts ajenos y no se sirven archivos de datos',async t=>{
  const f=await fixture(t);
  assert.equal((await f.request('/api/sessions',{method:'POST',body:{account:'alicia'},origin:'https://otro.example'})).status,403);
  assert.equal(await f.foreignHost(),403);
  assert.equal((await f.request('/estado.json',{token:f.tokens.alicia})).status,404);
  assert.equal((await f.request('/api/commands',{method:'POST',token:f.tokens.alicia,body:{type:'publish',audience:'public',text:'x'.repeat(17000)}})).status,413);
});
test('Me gusta es reversible, idempotente y separado de Guardar',async t=>{
  const f=await fixture(t);
  for(let i=0;i<2;i++)assert.equal((await f.cmd('bruno',{type:'like',post:'p1',active:true,actor:'alicia'})).status,200);
  let s=(await f.request('/api/state',{token:f.tokens.alicia})).data;
  assert.equal(s.posts.find(p=>p.id==='p1').likedByMe,false);
  assert.equal((await f.request('/api/state',{token:f.tokens.bruno})).data.posts.find(p=>p.id==='p1').likedByMe,true);
  assert.deepEqual(s.saved,[]);
  assert.deepEqual((await f.request('/api/state',{token:f.tokens.bruno})).data.saved,[]);
  await f.cmd('bruno',{type:'save',post:'p1'});
  await f.cmd('bruno',{type:'like',post:'p1',active:false});
  s=(await f.request('/api/state',{token:f.tokens.bruno})).data;
  assert.equal(s.posts.find(p=>p.id==='p1').likedByMe,false);assert.deepEqual(s.saved,['p1']);
});
test('la reacción de una lectora permanece dentro de la audiencia privada',async t=>{
  const f=await fixture(t);
  assert.equal((await f.cmd('carla',{type:'like',post:'p2',active:true})).status,200);
  const a=(await f.request('/api/state',{token:f.tokens.alicia})).data;
  assert.equal(a.posts.find(p=>p.id==='p2').likedByMe,false);
  assert.equal((await f.request('/api/state',{token:f.tokens.carla})).data.posts.find(p=>p.id==='p2').likedByMe,true);
  const d=(await f.request('/api/state',{token:f.tokens.diego})).data;
  assert(!d.posts.some(p=>p.id==='p2'));
  assert(!JSON.stringify(d).includes('Cuaderno compartido'));
  assert.equal((await f.cmd('diego',{type:'like',post:'p2',active:true})).status,404);
  assert.equal((await f.cmd('diego',{type:'like',post:'inexistente',active:true})).status,404);
});
test('responder a una respuesta hereda comunidad y audiencia sin ampliación',async t=>{
  const f=await fixture(t);
  const r=await f.cmd('bruno',{type:'publish',parent:'p2',text:'Primera respuesta'});
  const parent=r.data.state.posts.at(-1).id;
  const r2=await f.cmd('alicia',{type:'publish',parent,audience:'public',community:null,text:'Respuesta a Bruno'});
  const child=r2.data.state.posts.at(-1);
  assert.equal(child.parent,parent);assert.equal(child.community,'cuaderno');assert.equal(child.audience,'members');
  assert.equal((await f.cmd('carla',{type:'publish',parent:child.id,text:'No puedo comentar'})).status,403);
  assert.equal((await f.cmd('diego',{type:'publish',parent:child.id,text:'No puedo acceder'})).status,404);
  assert(!(await f.request('/api/state',{token:f.tokens.diego})).data.posts.some(p=>[parent,child.id].includes(p.id)));
});
test('una respuesta guardada conserva referencias para volver a su conversación',async t=>{
  const f=await fixture(t);
  const r=await f.cmd('bruno',{type:'publish',parent:'p2',text:'Respuesta guardable'});
  const id=r.data.state.posts.at(-1).id;
  await f.cmd('carla',{type:'save',post:id});
  const state=(await f.request('/api/state',{token:f.tokens.carla})).data;
  assert.deepEqual(state.saved,[id]);assert.equal(state.posts.find(p=>p.id===id).parent,'p2');
  assert(state.posts.some(p=>p.id==='p2'));
  assert.deepEqual((await f.request('/api/state',{token:f.tokens.bruno})).data.saved,[]);
});
test('los datos de la primera versión migran sin perder publicaciones ni guardados',async t=>{
  const f=await fixture(t);
  const legacy=initialData();legacy.schema=1;delete legacy.likes;legacy.saved.bruno=['p1'];legacy.revision=7;
  await f.restart(legacy);
  const token=await f.login('bruno');const state=(await f.request('/api/state',{token})).data;
  assert.equal(state.revision,7);assert.equal(state.posts.length,2);assert.deepEqual(state.saved,['p1']);
  assert(state.posts.every(p=>p.likedByMe===false&&!Object.hasOwn(p,'likes')));
  const persisted=JSON.parse(await readFile(path.join(f.directory,'estado.json'),'utf8'));
  assert.equal(persisted.schema,8);assert.deepEqual(persisted.posts,legacy.posts);
});
test('las reacciones persisten y la exportación solo atribuye las propias',async t=>{
  const f=await fixture(t);
  await f.cmd('bruno',{type:'like',post:'p2',active:true});
  await f.cmd('alicia',{type:'like',post:'p1',active:true});
  await f.restart();const token=await f.login('bruno');
  const state=(await f.request('/api/state',{token})).data;
  assert.equal(state.posts.find(p=>p.id==='p2').likedByMe,true);
  const exported=(await f.request('/api/export',{token})).data;
  assert.deepEqual(exported.liked,['p2']);assert.deepEqual(exported.saved,[]);
  assert.equal(exported.format,'spartakos-local-simulation-v7');
});
test('abrir la comunidad no publica las reacciones de su historial restringido',async t=>{
  const f=await fixture(t);
  await f.cmd('carla',{type:'like',post:'p2',active:true});
  await f.cmd('alicia',{type:'propose',community:'cuaderno'});
  for(const actor of ['alicia','bruno','carla'])await f.cmd(actor,{type:'consent',community:'cuaderno',version:1,accept:true});
  await f.cmd('alicia',{type:'open',community:'cuaderno',version:1});
  const d=(await f.request('/api/state',{token:f.tokens.diego})).data;
  assert(d.communities.some(c=>c.id==='cuaderno'));assert(!d.posts.some(p=>p.id==='p2'));
  assert.equal((await f.cmd('diego',{type:'like',post:'p2',active:true})).status,404);
});
test('Me gusta exige una intención explícita y no admite valores ambiguos',async t=>{
  const f=await fixture(t);
  for(const active of [undefined,'true',1,null])assert.equal((await f.cmd('bruno',{type:'like',post:'p1',active})).status,400);
  const s=(await f.request('/api/state',{token:f.tokens.bruno})).data;
  assert.equal(s.revision,0);assert.equal(s.posts.find(p=>p.id==='p1').likedByMe,false);
});

test('el servidor publica sin cliente abierto, persiste y no repite tras reinicio',async t=>{
 const f=await fixture(t);
 const scheduled=await f.cmd('bruno',{type:'schedule',text:'Envío automático HTTP',community:'cuaderno',audience:'members',publishAt:new Date(Date.now()+1500).toISOString(),timeZone:'Atlantic/Canary',lateMinutes:5});
 assert.equal(scheduled.status,200);
 assert.equal((await f.request('/api/state',{token:f.tokens.alicia})).data.scheduled.length,0);
 assert.equal((await f.request('/api/export',{token:f.tokens.bruno})).data.scheduled.length,1);
 // Durante la espera no hay peticiones HTTP: el temporizador debe ejecutar por sí mismo.
 await new Promise(r=>setTimeout(r,2600));
 const disk=JSON.parse(await readFile(path.join(f.directory,'estado.json'),'utf8'));
 assert.equal(disk.scheduled[0].status,'published');
 assert.equal(disk.posts.filter(p=>p.text==='Envío automático HTTP').length,1);
 await f.restart();const token=await f.login('bruno');
 const state=(await f.request('/api/state',{token})).data;
 assert.equal(state.posts.filter(p=>p.text==='Envío automático HTTP').length,1);
 assert.equal(state.scheduled[0].status,'published');
});
test('acciones sobre programación ajena no revelan su existencia',async t=>{
 const f=await fixture(t);
 await f.cmd('bruno',{type:'schedule',text:'Pendiente privada',community:'cuaderno',audience:'members',publishAt:new Date(Date.now()+3600000).toISOString(),timeZone:'Atlantic/Canary',lateMinutes:15});
 for(const type of ['edit-schedule','cancel-schedule','publish-schedule'])assert.equal((await f.cmd('diego',{type,id:'s1',version:1})).status,404);
 const state=(await f.request('/api/state',{token:f.tokens.diego})).data;
 assert(!JSON.stringify(state).includes('Pendiente privada'));
});
test('HTTP impide cuarto nivel aunque el cliente envíe una solicitud manual',async t=>{
 const f=await fixture(t);
 for(const parent of ['p2','p3'])assert.equal((await f.cmd('bruno',{type:'publish',parent,text:'Respuesta'})).status,200);
 assert.equal((await f.cmd('bruno',{type:'publish',parent:'p4',text:'Exceso'})).status,409);
 const r=await f.cmd('alicia',{type:'publish',quote:'p4',text:'Continúo aquí',community:'cuaderno',audience:'members'});
 assert.equal(r.status,200);assert.equal(r.data.state.posts.at(-1).parent,null);
 const b=(await f.request('/api/state',{token:f.tokens.bruno})).data;
 assert.equal(b.notices.length,1);assert.equal(b.notices[0].quoted,'p4');
});
test('avisos de cita persisten y no se reciben ni se marcan desde otra cuenta',async t=>{
 const f=await fixture(t);
 await f.cmd('alicia',{type:'publish',quote:'p1',text:'Cita pública',audience:'public'});
 assert.equal((await f.cmd('diego',{type:'read-notice',id:'p3'})).status,404);
 assert.equal((await f.cmd('bruno',{type:'read-notice',id:'p3'})).status,200);
 await f.restart();const token=await f.login('bruno');
 const state=(await f.request('/api/state',{token})).data;assert.equal(state.notices[0].read,true);
});

test('la API no entrega identidades ni cantidades en directo de Me gusta a otros usuarios',async t=>{
 const f=await fixture(t);
 await f.cmd('carla',{type:'like',post:'p1',active:true});
 await f.cmd('bruno',{type:'like',post:'p1',active:true});
 for(const actor of ['alicia','bruno','carla','diego']){
  const state=(await f.request('/api/state',{token:f.tokens[actor]})).data;
  const post=state.posts.find(p=>p.id==='p1');
  assert.equal(post.likedByMe,['bruno','carla'].includes(actor));
  assert(!Object.hasOwn(post,'likes'));assert.equal(post.likeCount,null);
  const exported=(await f.request('/api/export',{token:f.tokens[actor]})).data;
  assert.deepEqual(exported.liked,['bruno','carla'].includes(actor)?['p1']:[]);
  assert.deepEqual(state.notices,[]);
 }
 const response=await f.cmd('alicia',{type:'save',post:'p1'});
 assert.equal(response.data.state.posts.find(p=>p.id==='p1').likedByMe,false);
 assert(!Object.hasOwn(response.data.state.posts.find(p=>p.id==='p1'),'likes'));
});
test('el temporizador publica el corte horario sin cliente y lo conserva al reiniciar',async t=>{
 let now=Date.parse('2030-01-01T12:30:00Z');const f=await fixture(t,{clock:()=>now});
 await f.cmd('bruno',{type:'like',post:'p1',active:true});
 assert.equal((await f.request('/api/state',{token:f.tokens.alicia})).data.posts.find(p=>p.id==='p1').likeCount,null);
 now=Date.parse('2030-01-01T13:00:02Z');
 // La reacción posterior al corte no se debe incluir aunque el temporizador aún no haya ejecutado.
 await f.cmd('carla',{type:'like',post:'p1',active:true});
 await new Promise(r=>setTimeout(r,1200));
 const disk=JSON.parse(await readFile(path.join(f.directory,'estado.json'),'utf8'));
 assert.equal(disk.likeBatch.counts.p1,1);assert.equal(disk.likeBatch.updatedAt,'2030-01-01T13:00:00.000Z');
 await f.restart();const token=await f.login('alicia');
 let post=(await f.request('/api/state',{token})).data.posts.find(p=>p.id==='p1');
 assert.equal(post.likeCount,1);assert(!Object.hasOwn(post,'likes'));
 now=Date.parse('2030-01-01T14:00:01Z');await new Promise(r=>setTimeout(r,1200));
 post=(await f.request('/api/state',{token})).data.posts.find(p=>p.id==='p1');assert.equal(post.likeCount,2);
});
test('borradores propios persisten, se exportan y no salen en otras cuentas',async t=>{
 const f=await fixture(t);
 const r=await f.cmd('bruno',{type:'save-draft',text:'Texto privado no publicado',community:'cuaderno',audience:'members',quote:'p2'});
 assert.equal(r.status,200);assert.equal(r.data.state.posts.length,2);
 for(const actor of ['alicia','carla','diego']){
  const state=(await f.request('/api/state',{token:f.tokens[actor]})).data;assert.deepEqual(state.drafts,[]);
  assert(!JSON.stringify(state).includes('Texto privado no publicado'));
  assert.equal((await f.cmd(actor,{type:'save-draft',id:'d1',version:1,text:'Intrusión',audience:'public'})).status,404);
 }
 await f.restart();const token=await f.login('bruno');
 const state=(await f.request('/api/state',{token})).data;assert.equal(state.drafts[0].text,'Texto privado no publicado');assert.equal(state.drafts[0].quote,'p2');
 assert.equal((await f.request('/api/export',{token})).data.drafts.length,1);
});
test('HTTP conserva un borrador tras revocar y revalida al publicarlo sin duplicados',async t=>{
 const f=await fixture(t);const draft={text:'Pendiente',community:'cuaderno',audience:'members'};
 await f.cmd('bruno',{...draft,type:'save-draft'});
 await f.cmd('alicia',{type:'set-role',community:'cuaderno',member:'bruno',role:'reader'});
 const publication={...draft,type:'publish',draftId:'d1',draftVersion:1};
 assert.equal((await f.cmd('bruno',publication)).status,403);
 assert.equal((await f.request('/api/state',{token:f.tokens.bruno})).data.drafts[0].status,'draft');
 await f.cmd('alicia',{type:'set-role',community:'cuaderno',member:'bruno',role:'contributor'});
 assert.equal((await f.cmd('bruno',publication)).status,200);assert.equal((await f.cmd('bruno',publication)).status,409);
});
test('papelera propia persiste y restaurar no publica ni concede permisos',async t=>{
 const f=await fixture(t);await f.cmd('bruno',{type:'save-draft',text:'Recuperable',community:'cuaderno',audience:'members'});
 assert.equal((await f.cmd('bruno',{type:'trash-draft',id:'d1',version:1})).status,200);
 await f.restart();const token=await f.login('bruno');
 const trashed=(await f.request('/api/state',{token})).data;
 assert.equal(trashed.drafts[0].status,'trashed');assert.equal(trashed.drafts[0].text,'Recuperable');
 assert.equal((await f.request('/api/commands',{method:'POST',token,body:{type:'restore-draft',id:'d1',version:2}})).status,200);
 const restored=(await f.request('/api/state',{token})).data;
 assert.equal(restored.drafts[0].status,'draft');assert.equal(restored.posts.length,2);
 const alicia=await f.login('alicia');assert.deepEqual((await f.request('/api/state',{token:alicia})).data.drafts,[]);
});
test('edición HTTP exige versión y persiste sin publicar cuerpos anteriores',async t=>{
 const f=await fixture(t);
 const r=await f.cmd('bruno',{type:'edit-post',post:'p1',version:1,text:'Versión corregida persistente'});assert.equal(r.status,200);assert.equal(r.data.state.posts[0].version,2);
 assert.equal((await f.cmd('bruno',{type:'edit-post',post:'p1',version:1,text:'Obsoleta'})).status,409);
 assert.equal((await f.cmd('alicia',{type:'edit-post',post:'p1',version:2,text:'Ajena'})).status,403);
 await f.restart();const token=await f.login('bruno');const state=(await f.request('/api/state',{token})).data;
 assert.equal(state.posts[0].text,'Versión corregida persistente');assert(!JSON.stringify(state).includes('¿Qué libro os gustaría'));
});
test('retirada HTTP persiste y no filtra el cuerpo por estado, exportación o cita',async t=>{
 const f=await fixture(t);await f.cmd('alicia',{type:'publish',quote:'p1',audience:'public',text:'Comentario independiente'});
 assert.equal((await f.cmd('bruno',{type:'withdraw-post',post:'p1',version:1})).status,200);
 await f.restart();const token=await f.login('bruno');
 for(const route of ['/api/state','/api/export']){const state=(await f.request(route,{token})).data;assert(!JSON.stringify(state).includes('¿Qué libro os gustaría'));assert.equal(state.posts.find(p=>p.id==='p1').text,'');}
 const alicia=await f.login('alicia');const state=(await f.request('/api/state',{token:alicia})).data;
 assert.equal(state.posts.find(p=>p.id==='p3').text,'Comentario independiente');assert.equal(state.posts.find(p=>p.id==='p1').withdrawn,true);
});
test('bloqueo programado persiste y recuperar permisos exige una nueva acción explícita',async t=>{
 let now=Date.parse('2030-01-15T12:00:00Z');const f=await fixture(t,{clock:()=>now});
 const text='Pendiente sintética tras recuperar permisos';
 assert.equal((await f.cmd('bruno',{type:'schedule',text,community:'cuaderno',audience:'members',publishAt:'2030-01-15T12:01:00Z',timeZone:'Atlantic/Canary',lateMinutes:15})).status,200);
 assert.equal((await f.cmd('alicia',{type:'set-role',community:'cuaderno',member:'bruno',role:'reader'})).status,200);
 now+=60000;
 // El reloj avanza, pero no hay consultas del cliente: el temporizador debe bloquear y persistir.
 await new Promise(r=>setTimeout(r,1200));
 let disk=JSON.parse(await readFile(path.join(f.directory,'estado.json'),'utf8'));
 assert.equal(disk.scheduled[0].status,'blocked');assert(disk.scheduled[0].reason);assert(!disk.posts.some(p=>p.text===text));
 await f.restart();f.tokens.bruno=await f.login('bruno');f.tokens.alicia=await f.login('alicia');f.tokens.diego=await f.login('diego');
 assert.equal((await f.cmd('bruno',{type:'publish-schedule',id:'s1',version:2})).status,403);
 assert.equal((await f.cmd('alicia',{type:'set-role',community:'cuaderno',member:'bruno',role:'contributor'})).status,200);
 now+=60000;await new Promise(r=>setTimeout(r,1200));
 disk=JSON.parse(await readFile(path.join(f.directory,'estado.json'),'utf8'));
 assert.equal(disk.scheduled[0].status,'blocked');assert(!disk.posts.some(p=>p.text===text));
 assert.deepEqual((await f.request('/api/state',{token:f.tokens.alicia})).data.scheduled,[]);
 const published=await f.cmd('bruno',{type:'publish-schedule',id:'s1',version:2});assert.equal(published.status,200);assert.equal(published.data.state.scheduled[0].status,'published');
 assert.equal((await f.cmd('bruno',{type:'publish-schedule',id:'s1',version:2})).status,409);
 assert(!(await f.request('/api/state',{token:f.tokens.diego})).data.posts.some(p=>p.text===text));
 await f.restart();const token=await f.login('bruno');
 const state=(await f.request('/api/state',{token})).data;
 assert.equal(state.posts.filter(p=>p.text===text).length,1);assert.equal(state.scheduled[0].status,'published');assert.equal(state.posts.find(p=>p.text===text).audience,'members');
});
test('borrador de respuesta persiste privado y publica una sola vez tras reiniciar',async t=>{
 const f=await fixture(t);const text='Respuesta privada recuperable';
 const saved=await f.cmd('bruno',{type:'save-draft',kind:'reply',parent:'p2',targetVersion:1,text});assert.equal(saved.status,200);assert.equal(saved.data.state.posts.length,2);
 for(const actor of ['alicia','carla','diego'])assert(!JSON.stringify((await f.request('/api/state',{token:f.tokens[actor]})).data).includes(text));
 await f.restart();const token=await f.login('bruno');
 const state=(await f.request('/api/state',{token})).data;assert.equal(state.drafts[0].kind,'reply');assert.equal(state.drafts[0].parent,'p2');assert.equal(state.drafts[0].targetVersion,1);assert.equal(state.drafts[0].text,text);
 const exported=(await f.request('/api/export',{token})).data;assert.equal(exported.drafts[0].audience,'members');
 const body={type:'publish',parent:'p2',text,draftId:'d1',draftVersion:1};
 const sent=await f.request('/api/commands',{method:'POST',token,body});assert.equal(sent.status,200);assert.equal(sent.data.state.drafts[0].status,'published');
 assert.equal((await f.request('/api/commands',{method:'POST',token,body})).status,409);
 await f.restart();const again=await f.login('bruno');const after=(await f.request('/api/state',{token:again})).data;
 assert.equal(after.posts.filter(p=>p.text===text).length,1);assert.equal(after.posts.find(p=>p.text===text).parentVersion,1);
});
test('edición pendiente recupera texto y exige revisar el original nuevo antes de aplicarlo',async t=>{
 const f=await fixture(t);
 assert.equal((await f.cmd('bruno',{type:'save-draft',kind:'edit',editPost:'p1',targetVersion:1,text:'Edición recuperada'})).status,200);
 await f.restart();f.tokens.bruno=await f.login('bruno');
 assert.equal((await f.cmd('bruno',{type:'edit-post',post:'p1',version:1,text:'Cambio de otra pestaña'})).status,200);
 const apply={type:'edit-post',post:'p1',version:1,text:'Edición recuperada',draftId:'d1',draftVersion:1};
 assert.equal((await f.cmd('bruno',apply)).status,409);
 let state=(await f.request('/api/state',{token:f.tokens.bruno})).data;assert.equal(state.drafts[0].text,'Edición recuperada');assert.equal(state.drafts[0].status,'draft');
 assert.equal((await f.cmd('bruno',{type:'save-draft',kind:'edit',id:'d1',version:1,editPost:'p1',text:'Edición revisada',reviewedVersion:2})).status,200);
 assert.equal((await f.cmd('bruno',{...apply,version:2,draftVersion:2,text:'Edición revisada'})).status,200);
 await f.restart();const token=await f.login('bruno');state=(await f.request('/api/state',{token})).data;
 assert.equal(state.posts[0].text,'Edición revisada');assert.equal(state.posts[0].version,3);assert.equal(state.drafts[0].status,'published');
});
test('borradores contextuales conservan texto tras baja sin exponer historial o permitir el envío',async t=>{
 const f=await fixture(t);await f.cmd('bruno',{type:'save-draft',kind:'reply',parent:'p2',targetVersion:1,text:'Privado antes de la baja'});
 await f.cmd('alicia',{type:'remove',community:'cuaderno',member:'bruno'});
 await f.restart();const token=await f.login('bruno');
 const body={type:'save-draft',kind:'reply',id:'d1',version:1,parent:'p2',text:'Texto privado tras la baja'};
 assert.equal((await f.request('/api/commands',{method:'POST',token,body})).status,200);
 const state=(await f.request('/api/state',{token})).data;assert.equal(state.drafts[0].text,body.text);assert(!state.posts.some(p=>p.id==='p2'));assert(!JSON.stringify(state).includes('Este cuaderno es privado.'));
 assert.equal((await f.request('/api/commands',{method:'POST',token,body:{type:'publish',parent:'p2',text:body.text,draftId:'d1',draftVersion:2}})).status,404);
 const other=await f.login('alicia');assert(!(await f.request('/api/export',{token:other})).data.drafts.length);
});
