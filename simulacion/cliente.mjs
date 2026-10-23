// SPDX-License-Identifier: AGPL-3.0-or-later
const $=id=>document.getElementById(id);
const params=new URLSearchParams(location.search);
const slot=params.get('panel')??'principal';
const storageKey=`spartakos-lab:${slot}`;
let token=sessionStorage.getItem(storageKey),state=null,page='inicio',busy=false,connectionLost=false;
let selectedAudience='public';
const drafts=new Map();
const esc=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function status(text,error=false){$('status').textContent=text;$('status').className=error?'error':'';}
async function api(url,{method='GET',body}={}){
  const response=await fetch(url,{method,headers:{...(token?{Authorization:`Bearer ${token}`}:{ }),...(body?{'Content-Type':'application/json'}:{})},...(body?{body:JSON.stringify(body)}:{})});
  const data=await response.json();
  if(!response.ok){const error=Error(data.error??'No se pudo completar la operación.');error.status=response.status;throw error;}
  return data;
}
function showLogin(){token=null;state=null;sessionStorage.removeItem(storageKey);$('login').hidden=false;$('session').hidden=true;$('identity').textContent='Sin sesión ficticia';}
async function enter(account){
  try{if(token)await api('/api/session',{method:'DELETE'}).catch(()=>{});token=null;const result=await api('/api/sessions',{method:'POST',body:{account}});token=result.token;sessionStorage.setItem(storageKey,token);state=await api('/api/state');$('login').hidden=true;$('session').hidden=false;$('text').value='';drafts.clear();selectedAudience='public';render();status('Sesión ficticia abierta.');}
  catch(error){status(error.message,true);}
}
async function send(input){
  if(busy)return false;
  busy=true;document.querySelectorAll('button[type=submit]').forEach(b=>b.disabled=true);
  try{const result=await api('/api/commands',{method:'POST',body:input});state=result.state;render();status(result.message);return true;}
  catch(error){status(error.message,true);if(error.status===401)showLogin();return false;}
  finally{busy=false;document.querySelectorAll('button[type=submit]').forEach(b=>b.disabled=false);updatePublishDisabled();}
}
function post(p,isReply=false){
  const c=state.communities.find(c=>c.id===p.community);
  const mayReply=!p.community||['admin','contributor','commenter'].includes(c?.role);
  const saved=state.saved.includes(p.id);
  return `<${isReply?'div':'article'} class="${isReply?'comment':'post'}"><div class="meta">${esc(p.authorName)} · ${p.audience==='public'?'Público':'Solo integrantes · Operador con acceso'}</div><p class="post-text">${esc(p.text)}</p><div class="actions"><button data-save="${p.id}" aria-pressed="${saved}">${saved?'Guardado · Privado':'Me interesa · Privado'}</button>${!isReply&&mayReply?`<button data-reply="${p.id}" aria-expanded="false">Responder</button>`:''}</div>${!isReply&&mayReply?`<form class="reply-form" data-parent="${p.id}" hidden><label for="reply-${p.id}">Respuesta con la misma audiencia</label><textarea id="reply-${p.id}" maxlength="3000" required>${esc(drafts.get(p.id)??'')}</textarea><button type="submit">Enviar respuesta</button></form>`:''}${!isReply?state.posts.filter(r=>r.parent===p.id).map(r=>post(r,true)).join(''):''}</${isReply?'div':'article'}>`;
}
function proposal(c,former=false){
  const p=c.proposal;if(!p)return '';
  const own=p.consents.includes(state.user.id);
  return `<section class="notice"><h3>Propuesta de apertura ${p.version}</h3><p>Solo afecta a publicaciones futuras. El historial anterior seguirá restringido. Una negativa cierra esta propuesta.</p><ul class="census">${p.census.map(id=>`<li>${esc(id)}: ${p.consents.includes(id)?'ha consentido':'sin consentimiento'}</li>`).join('')}</ul>${p.census.includes(state.user.id)?`<div class="actions"><button data-consent="${c.id}" data-version="${p.version}" data-accept="yes" ${own?'disabled':''}>${own?'Ya has consentido':'Consiento la apertura'}</button><button data-consent="${c.id}" data-version="${p.version}" data-accept="no">No consiento</button></div>`:''}${!former&&c.role==='admin'?`<div class="actions"><button data-open="${c.id}" data-version="${p.version}">Comprobar unanimidad y abrir</button></div>`:''}</section>`;
}
function communities(){
  return `<h1 class="screen-heading">Comunidades</h1>${state.communities.map(c=>`<section class="community"><h2>${esc(c.name)}</h2><p>${c.visibility==='private'?'Privada · Operador con acceso':'Pública · Historial anterior restringido'}</p><p class="badge">Tu permiso: ${{admin:'administración',contributor:'lectura, comentarios y publicaciones',commenter:'lectura y comentarios, sin nuevas publicaciones',reader:'solo lectura'}[c.role]??'lectura pública'}</p>${proposal(c)}${c.role==='admin'&&c.visibility==='private'&&!c.proposal?`<button data-propose="${c.id}">Proponer apertura con historial protegido</button>`:''}${c.role==='admin'?`<details><summary>Permisos de participación</summary>${Object.entries(c.members).filter(([id,role])=>role!=='admin').map(([id,role])=>`<label for="role-${id}">${esc(id)}</label><select id="role-${id}" data-role="${id}" data-community="${c.id}">${[['reader','Solo lectura'],['commenter','Leer y comentar'],['contributor','Leer, comentar y publicar']].map(([value,label])=>`<option value="${value}" ${value===role?'selected':''}>${label}</option>`).join('')}</select>`).join('')}</details><details><summary>Probar una baja de membresía</summary><p>Una baja no permite eludir la protección frente a la apertura. La última administración no se retira desde este laboratorio.</p>${Object.entries(c.members).filter(([id,role])=>role!=='admin').map(([id])=>`<button data-remove="${id}" data-community="${c.id}">Retirar a ${esc(id)}</button>`).join(' ')}</details>`:''}</section>`).join('')}${state.formerProposals.map(c=>`<section class="community"><h2>${esc(c.name)} · Propuesta que te afecta</h2><p>Ya no perteneces a la comunidad. Conservas protección frente a su apertura, sin recuperar acceso al contenido privado.</p>${proposal(c,true)}</section>`).join('')}${!state.communities.length&&!state.formerProposals.length?'<p>No hay comunidades disponibles para esta cuenta.</p>':''}${state.posts.filter(p=>p.community&&!p.parent).map(p=>post(p)).join('')}`;
}
function render(){
  if(!state)return;
  const openReplies=[...document.querySelectorAll('.reply-form:not([hidden])')].map(f=>f.dataset.parent);
  const focused=document.activeElement;
  const focusSnapshot=focused?.closest('.reply-form')?{id:focused.id,start:focused.selectionStart,end:focused.selectionEnd}:null;
  $('identity').textContent=`${state.user.name} · Sesión ficticia`;
  document.title=`${state.user.name} · Spartakos local`;
  $('composer').hidden=page!=='inicio';
  const eligible=state.communities.filter(c=>['admin','contributor'].includes(c.role));
  const options=[{id:'public',name:'Todo el mundo'},...eligible.flatMap(c=>[{id:`${c.id}:members`,name:`${c.name} · Solo integrantes`},...(c.visibility==='public'?[{id:`${c.id}:public`,name:`${c.name} · Público`}]:[])])];
  if(!options.some(o=>o.id===selectedAudience))options.push({id:selectedAudience,name:'Destino anterior sin permiso · Elige una audiencia',disabled:true});
  $('audience').innerHTML=options.map(o=>`<option value="${o.id}" ${o.disabled?'disabled':''}>${esc(o.name)}</option>`).join('');
  $('audience').value=selectedAudience;audienceHelp();updatePublishDisabled();
  document.querySelectorAll('[data-page]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.page===page)));
  if(page==='inicio')$('content').innerHTML=`<h2>Lectura cronológica</h2>${state.posts.filter(p=>!p.parent).slice().reverse().map(p=>post(p)).join('')}<p class="hint">Fin de las publicaciones disponibles.</p>`;
  if(page==='interes')$('content').innerHTML=`<h1 class="screen-heading">Mi interés</h1><p>Solo esta cuenta ve sus guardados. No expresan acuerdo público ni se usan para publicidad.</p>${state.posts.filter(p=>state.saved.includes(p.id)).map(p=>post(p,p.parent!==null)).join('')||'<p>No has guardado publicaciones.</p>'}`;
  if(page==='comunidad')$('content').innerHTML=communities();
  if(page==='cuenta')$('content').innerHTML=`<h1 class="screen-heading">Mi cuenta</h1><p>Actúas como ${esc(state.user.name)}. Las otras sesiones conservan sus propios permisos y guardados.</p><button id="export">Exportar mis aportaciones ficticias</button><p>La exportación de este laboratorio no es un perfil portable de producción.</p><button id="logout">Cerrar esta sesión</button>`;
  document.querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>send({type:'save',post:b.dataset.save}));
  document.querySelectorAll('[data-propose]').forEach(b=>b.onclick=()=>send({type:'propose',community:b.dataset.propose}));
  document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>send({type:'open',community:b.dataset.open,version:Number(b.dataset.version)}));
  document.querySelectorAll('[data-consent]').forEach(b=>b.onclick=()=>send({type:'consent',community:b.dataset.consent,version:Number(b.dataset.version),accept:b.dataset.accept==='yes'}));
  document.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>send({type:'remove',community:b.dataset.community,member:b.dataset.remove}));
  document.querySelectorAll('[data-role]').forEach(select=>select.onchange=()=>send({type:'set-role',community:select.dataset.community,member:select.dataset.role,role:select.value}));
  document.querySelectorAll('[data-reply]').forEach(b=>b.onclick=()=>{const form=document.querySelector(`[data-parent="${b.dataset.reply}"]`);form.hidden=!form.hidden;b.setAttribute('aria-expanded',String(!form.hidden));if(!form.hidden)form.querySelector('textarea').focus();});
  document.querySelectorAll('.reply-form').forEach(form=>{const editor=form.querySelector('textarea');editor.oninput=()=>drafts.set(form.dataset.parent,editor.value);form.onsubmit=async e=>{e.preventDefault();const text=editor.value;if(await send({type:'publish',parent:form.dataset.parent,text})){drafts.delete(form.dataset.parent);render();}};});
  for(const id of openReplies){const form=document.querySelector(`[data-parent="${id}"]`);if(form){form.hidden=false;document.querySelector(`[data-reply="${id}"]`)?.setAttribute('aria-expanded','true');}}
  if(focusSnapshot){const editor=document.getElementById(focusSnapshot.id);if(editor){editor.focus({preventScroll:true});editor.setSelectionRange(focusSnapshot.start,focusSnapshot.end);}}
  if($('logout'))$('logout').onclick=async()=>{await api('/api/session',{method:'DELETE'}).catch(()=>{});showLogin();status('Sesión cerrada.');};
  if($('export'))$('export').onclick=async()=>{try{const data=await api('/api/export');const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download=`spartakos-${state.user.id}-simulacion.json`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}catch(error){status(error.message,true);}};
}
function destinationAvailable(){const [id,mode]=selectedAudience.split(':');return selectedAudience==='public'||state?.communities.some(c=>c.id===id&&['admin','contributor'].includes(c.role)&&(mode==='members'||(mode==='public'&&c.visibility==='public')));}
function updatePublishDisabled(){$('publish').querySelector('button[type=submit]').disabled=busy||!destinationAvailable();}
function audienceHelp(){$('audience-help').textContent=!destinationAvailable()?'Ya no puedes publicar en el destino elegido. El borrador se conserva; elige expresamente otra audiencia.':selectedAudience.endsWith(':members')?'Solo integrantes. El operador puede leer el contenido; no hay cifrado de extremo a extremo.':'Todo el mundo podrá leer esta publicación.';}
$('audience').onchange=()=>{selectedAudience=$('audience').value;audienceHelp();updatePublishDisabled();};
$('publish').onsubmit=async e=>{e.preventDefault();if(!destinationAvailable())return status('Elige una audiencia con permiso antes de publicar.',true);const text=$('text').value;const [community,audience]=selectedAudience.split(':');if(await send({type:'publish',text,...(selectedAudience==='public'?{audience:'public'}:{community,audience})}))$('text').value='';};
document.querySelectorAll('[data-page]').forEach(b=>b.onclick=()=>{page=b.dataset.page;render();status('');});
$('enter').onclick=()=>enter($('account').value);
async function refresh(){
  if(!token||busy||document.hidden)return;
  const requestToken=token;
  try{const fresh=await api('/api/state');if(token!==requestToken)return;if(!state||fresh.revision>state.revision){state=fresh;render();}if(connectionLost){connectionLost=false;status('Conexión restablecida.');}}
  catch(error){if(token!==requestToken)return;if(error.status===401){showLogin();status('El servidor se reinició o la sesión terminó. Puedes volver a entrar.',true);}else if(!connectionLost){connectionLost=true;status('Sin conexión. Se conserva el borrador; los cambios no enviados no están guardados.',true);}}
}
try{
  const result=await api('/api/accounts');$('account').innerHTML=result.accounts.map(a=>`<option value="${a.id}">${esc(a.name)} · ${esc(a.description)}</option>`).join('');
  const requested=result.accounts.some(a=>a.id===params.get('cuenta'))?params.get('cuenta'):null;
  if(requested)$('account').value=requested;
  if(token){try{state=await api('/api/state');$('session').hidden=false;render();}catch{showLogin();if(requested)await enter(requested);}}
  else if(result.accounts.some(a=>a.id===params.get('cuenta')))await enter(params.get('cuenta'));
  else showLogin();
}catch(error){showLogin();status('No se puede conectar con el servidor local. Comprueba que está en marcha.',true);}
setInterval(refresh,1500);
