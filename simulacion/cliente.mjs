// SPDX-License-Identifier: AGPL-3.0-or-later
import {feedRoots,rootFor,conversationRows} from './conversaciones.mjs';

const $=id=>document.getElementById(id);
const params=new URLSearchParams(location.search);
const storageKey=`spartakos-lab:${params.get('panel')??'principal'}`;
const esc=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let token=sessionStorage.getItem(storageKey),state=null,page='inicio',selectedCommunity=null,busy=false,connectionLost=false;
const drafts=new Map(),replyDrafts=new Map(),expandedReplies=new Set();
const scopeKey=()=>page==='comunidad'&&selectedCommunity?`community:${selectedCommunity}`:'general';
function currentDraft(){const key=scopeKey();if(!drafts.has(key)){const c=state?.communities.find(c=>c.id===selectedCommunity);drafts.set(key,{text:'',audience:key==='general'?'public':`${selectedCommunity}:${c?.visibility==='public'?'public':'members'}`});}return drafts.get(key);}
function status(text,error=false){$('status').textContent=text;$('status').className=error?'error':'';}
async function api(url,{method='GET',body}={}){
  const response=await fetch(url,{method,headers:{...(token?{Authorization:`Bearer ${token}`}:{ }),...(body?{'Content-Type':'application/json'}:{})},...(body?{body:JSON.stringify(body)}:{})});
  const data=await response.json();
  if(!response.ok){const error=Error(data.error??'No se pudo completar la operación.');error.status=response.status;throw error;}
  return data;
}
function showLogin(){token=null;state=null;sessionStorage.removeItem(storageKey);$('login').hidden=false;$('session').hidden=true;$('identity').textContent='Sin sesión ficticia';}
async function enter(account){
  try{
    if(token)await api('/api/session',{method:'DELETE'}).catch(()=>{});
    token=null;
    const result=await api('/api/sessions',{method:'POST',body:{account}});
    token=result.token;sessionStorage.setItem(storageKey,token);state=await api('/api/state');
    drafts.clear();replyDrafts.clear();expandedReplies.clear();page='inicio';selectedCommunity=null;
    $('login').hidden=true;$('session').hidden=false;render();status('Sesión ficticia abierta.');
  }catch(error){status(error.message,true);}
}
async function send(input){
  if(busy)return false;
  busy=true;document.querySelectorAll('button[type=submit]').forEach(b=>b.disabled=true);
  try{const result=await api('/api/commands',{method:'POST',body:input});state=result.state;render();status(result.message);return true;}
  catch(error){status(error.message,true);if(error.status===401)showLogin();return false;}
  finally{busy=false;document.querySelectorAll('button[type=submit]').forEach(b=>b.disabled=false);updatePublishDisabled();}
}
function mayReply(p){const c=state.communities.find(c=>c.id===p.community);return !p.community||['admin','contributor','commenter'].includes(c?.role);}
function contextLabel(p){const c=state.communities.find(c=>c.id===p.community);return `${p.community?c?.name??'Comunidad':'General'} · ${p.audience==='public'?'Público':'Solo integrantes · Operador con acceso'}`;}
function postMarkup(p,{depth=0,savedView=false}={}){
  const saved=state.saved.includes(p.id),likes=p.likes??[],liked=likes.some(a=>a.id===state.user.id);
  const parent=state.posts.find(q=>q.id===p.parent);
  const replyTo=p.parent?`<p class="reply-to">En respuesta a ${parent?`<button data-context="${parent.id}">${esc(parent.authorName)}</button>`:'otro mensaje de esta conversación'}</p>`:'';
  return `<article id="post-${p.id}" tabindex="-1" class="post ${depth?`reply depth-${Math.min(depth,3)}`:''}">
    <div class="meta">${esc(p.authorName)} · ${esc(contextLabel(p))}</div>${replyTo}
    <p class="post-text">${esc(p.text)}</p>
    <div class="actions">
      <button id="like-${p.id}" data-like="${p.id}" aria-pressed="${liked}">${liked?'Te gusta':'Me gusta'}</button>
      <button id="save-${p.id}" data-save="${p.id}" aria-pressed="${saved}">${saved?'Guardado · Privado':'Guardar · Privado'}</button>
      ${mayReply(p)?`<button id="respond-${p.id}" data-reply="${p.id}" aria-expanded="${expandedReplies.has(p.id)}">Responder</button>`:''}
      ${savedView?`<button data-context="${p.id}">Ver en conversación</button>`:''}
    </div>
    ${likes.length?`<details class="reactions"><summary>Reacciones</summary><p>A ${esc(likes.map(a=>a.name).join(', '))} les gusta esta publicación. Visible para su audiencia.</p></details>`:''}
    ${mayReply(p)?`<form class="reply-form" data-parent="${p.id}" ${expandedReplies.has(p.id)?'':'hidden'}><label for="reply-${p.id}">Responder a ${esc(p.authorName)} · Misma audiencia</label><textarea id="reply-${p.id}" maxlength="3000" required>${esc(replyDrafts.get(p.id)??'')}</textarea><button type="submit">Enviar respuesta</button></form>`:''}
  </article>`;
}
function timeline(community){
  const roots=feedRoots(state.posts,community);
  return roots.length?roots.map(root=>`<section class="thread" aria-label="Conversación de ${esc(root.authorName)}">${conversationRows(state.posts,root.id).map(({post,depth})=>postMarkup(post,{depth})).join('')}</section>`).join(''):'<p class="empty">Todavía no hay publicaciones en este espacio.</p>';
}
function proposal(c,former=false){
  const p=c.proposal;if(!p)return '';
  const own=p.consents.includes(state.user.id);
  return `<section class="notice"><h3>Propuesta de apertura ${p.version}</h3><p>Solo afecta a publicaciones futuras. El historial anterior seguirá restringido. Una negativa cierra esta propuesta.</p><ul class="census">${p.census.map(id=>`<li>${esc(id)}: ${p.consents.includes(id)?'ha consentido':'sin consentimiento'}</li>`).join('')}</ul>${p.census.includes(state.user.id)?`<div class="actions"><button data-consent="${c.id}" data-version="${p.version}" data-accept="yes" ${own?'disabled':''}>${own?'Ya has consentido':'Consiento la apertura'}</button><button data-consent="${c.id}" data-version="${p.version}" data-accept="no">No consiento</button></div>`:''}${!former&&c.role==='admin'?`<div class="actions"><button data-open="${c.id}" data-version="${p.version}">Comprobar unanimidad y abrir</button></div>`:''}</section>`;
}
function management(c){
  if(c.role!=='admin')return '';
  return `<details data-panel="roles"><summary>Permisos de participación</summary>${Object.entries(c.members).filter(([,role])=>role!=='admin').map(([id,role])=>`<label for="role-${id}">${esc(id)}</label><select id="role-${id}" data-role="${id}" data-community="${c.id}">${[['reader','Lectura, sin comentarios ni publicaciones'],['commenter','Leer y comentar'],['contributor','Leer, comentar y publicar']].map(([value,label])=>`<option value="${value}" ${value===role?'selected':''}>${label}</option>`).join('')}</select>`).join('')}</details><details data-panel="membership"><summary>Probar una baja de membresía</summary><p>Una baja no permite eludir la protección frente a la apertura. La última administración no se retira desde este laboratorio.</p>${Object.entries(c.members).filter(([,role])=>role!=='admin').map(([id])=>`<button data-remove="${id}" data-community="${c.id}">Retirar a ${esc(id)}</button>`).join(' ')}</details>`;
}
function communityContent(){
  if(!selectedCommunity){
    return `${state.communities.map(c=>`<section class="community"><h2>${esc(c.name)}</h2><p>${c.visibility==='private'?'Privada · Operador con acceso':'Pública'}</p><button data-community="${c.id}" data-enter-community>Entrar en la comunidad</button></section>`).join('')}${state.formerProposals.map(c=>`<section class="community"><h2>${esc(c.name)} · Propuesta que te afecta</h2><p>No tienes acceso al contenido privado. Conservas protección frente a la apertura.</p>${proposal(c,true)}</section>`).join('')}${!state.communities.length&&!state.formerProposals.length?'<p>No hay comunidades disponibles para esta cuenta.</p>':''}`;
  }
  const c=state.communities.find(c=>c.id===selectedCommunity);
  if(!c)return '<p>Ya no tienes acceso a esta comunidad. Si estabas escribiendo, el borrador se conserva sin cambiar de destino.</p>';
  return `<section class="community"><p>Tu permiso: ${{admin:'administración',contributor:'lectura, comentarios y publicaciones',commenter:'lectura y comentarios',reader:'lectura y reacciones, sin comentarios ni publicaciones'}[c.role]??'lectura pública y reacciones'}</p>${proposal(c)}${c.role==='admin'&&c.visibility==='private'&&!c.proposal?`<button data-propose="${c.id}">Proponer apertura con historial protegido</button>`:''}${management(c)}</section><h2>Conversaciones de esta comunidad</h2>${timeline(c.id)}`;
}
function destinationAvailable(){
  const audience=currentDraft().audience;
  if(scopeKey()==='general')return audience==='public';
  const [id,mode]=audience.split(':');
  return id===selectedCommunity&&state?.communities.some(c=>c.id===id&&['admin','contributor'].includes(c.role)&&(mode==='members'||(mode==='public'&&c.visibility==='public')));
}
function updatePublishDisabled(){$('publish').querySelector('button[type=submit]').disabled=busy||!destinationAvailable();}
function composer(){
  const draft=currentDraft(),c=state.communities.find(c=>c.id===selectedCommunity);
  const inCommunity=page==='comunidad'&&selectedCommunity;
  const allowed=Boolean(c&&['admin','contributor'].includes(c.role));
  $('composer').hidden=!(page==='inicio'||(inCommunity&&(allowed||draft.text)));
  const options=!inCommunity?[{id:'public',name:'General · Público'}]:allowed?[
    {id:`${c.id}:members`,name:`${c.name} · Solo integrantes`},
    ...(c.visibility==='public'?[{id:`${c.id}:public`,name:`${c.name} · Público`}]:[]),
  ]:[];
  if(!options.some(o=>o.id===draft.audience))options.push({id:draft.audience,name:'Destino anterior sin permiso · Borrador protegido',disabled:true});
  $('audience').innerHTML=options.map(o=>`<option value="${o.id}" ${o.disabled?'disabled':''}>${esc(o.name)}</option>`).join('');
  $('audience').value=draft.audience;
  if($('text').value!==draft.text)$('text').value=draft.text;
  $('audience-help').textContent=!destinationAvailable()?'Ya no puedes publicar en el destino elegido. El borrador se conserva; no se cambia a público.':draft.audience.endsWith(':members')?'Solo integrantes. El operador puede leer el contenido; no hay cifrado de extremo a extremo.':inCommunity?'Publicación pública dentro de esta comunidad. No aparecerá en Inicio general.':'Publicación pública en el espacio general, fuera de las comunidades.';
  updatePublishDisabled();
}
function render(){
  if(!state)return;
  const active=document.activeElement;
  const focus=active?.id?{id:active.id,start:active.selectionStart,end:active.selectionEnd}:null;
  const panels=[...document.querySelectorAll('details[data-panel][open]')].map(d=>d.dataset.panel);
  $('identity').textContent=`${state.user.name} · Sesión ficticia`;
  document.title=`${state.user.name} · Spartakos local`;
  document.querySelectorAll('[data-page]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.page===page)));
  const c=state.communities.find(c=>c.id===selectedCommunity);
  if(page==='inicio'){
    $('context').innerHTML='<h1>Inicio general</h1><p>Publicaciones fuera de las comunidades, en orden cronológico.</p>';
    $('content').innerHTML=timeline(null);
  }else if(page==='guardados'){
    $('context').innerHTML='<h1>Guardados</h1><p>Tu colección privada. Guardar no expresa Me gusta ni avisa al autor.</p>';
    $('content').innerHTML=state.posts.filter(p=>state.saved.includes(p.id)).map(p=>postMarkup(p,{savedView:true})).join('')||'<p>No has guardado publicaciones.</p>';
  }else if(page==='comunidad'){
    $('context').innerHTML=selectedCommunity?`<button id="all-communities">Todas las comunidades</button><h1>${esc(c?.name??'Comunidad no disponible')}</h1>${c?`<p>${c.visibility==='private'?'Privada · Solo integrantes · Operador con acceso':'Pública · El historial anterior puede seguir restringido'}</p>`:''}`:'<h1>Comunidades</h1><p>Entra en una comunidad para leer y publicar en su propio espacio.</p>';
    $('content').innerHTML=communityContent();
  }else{
    $('context').innerHTML='<h1>Mi cuenta</h1>';
    $('content').innerHTML=`<p>Actúas como ${esc(state.user.name)}. Tus guardados son privados; tus Me gusta respetan la audiencia de cada publicación.</p><button id="export">Exportar mis aportaciones ficticias</button><p>Esta exportación no es un perfil portable de producción.</p><button id="logout">Cerrar esta sesión</button>`;
  }
  composer();bindActions();
  for(const panel of panels){const details=document.querySelector(`details[data-panel="${panel}"]`);if(details)details.open=true;}
  if(focus){const element=$(focus.id);if(element&&!element.hidden){if(document.activeElement!==element)element.focus({preventScroll:true});if(element.tagName==='TEXTAREA'&&focus.start!==null)element.setSelectionRange(focus.start,focus.end);}}
}
function openConversation(id){
  const root=rootFor(state.posts,id);
  if(!root)return status('La conversación ya no está disponible.',true);
  page=root.community?'comunidad':'inicio';selectedCommunity=root.community;render();
  const target=$(`post-${id}`);if(target){target.scrollIntoView({block:'center'});target.focus({preventScroll:true});}
}
function bindActions(){
  document.querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>send({type:'save',post:b.dataset.save}));
  document.querySelectorAll('[data-like]').forEach(b=>b.onclick=()=>send({type:'like',post:b.dataset.like,active:!(state.posts.find(p=>p.id===b.dataset.like)?.likes??[]).some(a=>a.id===state.user.id)}));
  document.querySelectorAll('[data-enter-community]').forEach(b=>b.onclick=()=>{selectedCommunity=b.dataset.community;page='comunidad';render();status('');});
  if($('all-communities'))$('all-communities').onclick=()=>{selectedCommunity=null;render();};
  document.querySelectorAll('[data-context]').forEach(b=>b.onclick=()=>openConversation(b.dataset.context));
  document.querySelectorAll('[data-propose]').forEach(b=>b.onclick=()=>send({type:'propose',community:b.dataset.propose}));
  document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>send({type:'open',community:b.dataset.open,version:Number(b.dataset.version)}));
  document.querySelectorAll('[data-consent]').forEach(b=>b.onclick=()=>send({type:'consent',community:b.dataset.consent,version:Number(b.dataset.version),accept:b.dataset.accept==='yes'}));
  document.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>send({type:'remove',community:b.dataset.community,member:b.dataset.remove}));
  document.querySelectorAll('[data-role]').forEach(s=>s.onchange=()=>send({type:'set-role',community:s.dataset.community,member:s.dataset.role,role:s.value}));
  document.querySelectorAll('[data-reply]').forEach(b=>b.onclick=()=>{
    const id=b.dataset.reply,form=document.querySelector(`[data-parent="${id}"]`);
    form.hidden=!form.hidden;b.setAttribute('aria-expanded',String(!form.hidden));
    if(form.hidden)expandedReplies.delete(id);else{expandedReplies.add(id);form.querySelector('textarea').focus();}
  });
  document.querySelectorAll('.reply-form').forEach(form=>{
    const editor=form.querySelector('textarea'),id=form.dataset.parent;
    editor.oninput=()=>replyDrafts.set(id,editor.value);
    form.onsubmit=async e=>{e.preventDefault();if(await send({type:'publish',parent:id,text:editor.value})){replyDrafts.delete(id);expandedReplies.delete(id);render();}};
  });
  if($('logout'))$('logout').onclick=async()=>{await api('/api/session',{method:'DELETE'}).catch(()=>{});showLogin();status('Sesión cerrada.');};
  if($('export'))$('export').onclick=async()=>{
    try{const data=await api('/api/export');const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download=`spartakos-${state.user.id}-simulacion.json`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}catch(error){status(error.message,true);}
  };
}
$('text').oninput=()=>{currentDraft().text=$('text').value;};
$('audience').onchange=()=>{currentDraft().audience=$('audience').value;composer();};
$('publish').onsubmit=async e=>{
  e.preventDefault();if(!destinationAvailable())return status('El destino perdió permisos. El borrador no se publica en otro espacio.',true);
  const draft=currentDraft(),[community,audience]=draft.audience.split(':'),key=scopeKey();
  const input={type:'publish',text:draft.text,...(key==='general'?{audience:'public'}:{community,audience})};
  if(await send(input)){drafts.get(key).text='';render();}
};
document.querySelectorAll('[data-page]').forEach(b=>b.onclick=()=>{page=b.dataset.page;if(page==='comunidad')selectedCommunity=null;render();status('');});
$('enter').onclick=()=>enter($('account').value);
async function refresh(){
  if(!token||busy||document.hidden)return;
  const requestToken=token;
  try{const fresh=await api('/api/state');if(token!==requestToken)return;if(!state||fresh.revision>state.revision){state=fresh;render();}if(connectionLost){connectionLost=false;status('Conexión restablecida.');}}
  catch(error){if(token!==requestToken)return;if(error.status===401){showLogin();status('El servidor se reinició o la sesión terminó. Puedes volver a entrar.',true);}else if(!connectionLost){connectionLost=true;status('Sin conexión. Se conservan los borradores; los cambios no enviados no están guardados.',true);}}
}
try{
  const result=await api('/api/accounts');$('account').innerHTML=result.accounts.map(a=>`<option value="${a.id}">${esc(a.name)} · ${esc(a.description)}</option>`).join('');
  const requested=result.accounts.some(a=>a.id===params.get('cuenta'))?params.get('cuenta'):null;
  if(requested)$('account').value=requested;
  if(token){try{state=await api('/api/state');$('session').hidden=false;render();}catch{showLogin();if(requested)await enter(requested);}}
  else if(requested)await enter(requested);else showLogin();
}catch{showLogin();status('No se puede conectar con el servidor local. Comprueba que está en marcha.',true);}
setInterval(refresh,1500);
