// SPDX-License-Identifier: AGPL-3.0-or-later
import {feedRoots,rootFor,conversationRows,replyDepth} from './conversaciones.mjs';

const $=id=>document.getElementById(id);
const params=new URLSearchParams(location.search);
const storageKey=`spartakos-lab:${params.get('panel')??'principal'}`;
const esc=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let token=sessionStorage.getItem(storageKey),state=null,page='inicio',selectedCommunity=null,busy=false,connectionLost=false;
let activeDraftId=null;
const loadedDrafts=new Map();
const drafts=new Map(),replyDrafts=new Map(),expandedReplies=new Set(),scheduleDrafts=new Map();
const localZone=Intl.DateTimeFormat().resolvedOptions().timeZone;
const dateLabel=(value,zone=localZone)=>new Intl.DateTimeFormat('es-ES',{dateStyle:'medium',timeStyle:'long',timeZone:zone}).format(new Date(value));
function localInput(value){const d=new Date(value),pad=n=>String(n).padStart(2,'0');return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;}
function instant(value){const d=new Date(value);if(!value||!Number.isFinite(d.getTime())||localInput(d)!==value+(value.length===16?':00':''))throw Error('Fecha u hora no válida en esta zona; revisa también los cambios de horario.');return d.toISOString();}
const scopeKey=()=>page==='comunidad'&&selectedCommunity?`community:${selectedCommunity}`:'general';
function currentDraft(){const saved=loadedDrafts.get(activeDraftId);if(saved&&((page==='inicio'&&!saved.community)||(page==='comunidad'&&selectedCommunity===saved.community)))return saved;const key=scopeKey();if(!drafts.has(key)){const c=state?.communities.find(c=>c.id===selectedCommunity);drafts.set(key,{text:'',audience:key==='general'?'public':`${selectedCommunity}:${c?.visibility==='public'?'public':'members'}`});}return drafts.get(key);}
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
    drafts.clear();loadedDrafts.clear();activeDraftId=null;replyDrafts.clear();expandedReplies.clear();scheduleDrafts.clear();page='inicio';selectedCommunity=null;
    $('login').hidden=true;$('session').hidden=false;render();status('Sesión ficticia abierta.');
  }catch(error){status(error.message,true);}
}
async function send(input){
  if(busy)return false;
  busy=true;document.querySelectorAll('textarea').forEach(t=>t.readOnly=true);document.querySelectorAll('button[type=submit]').forEach(b=>b.disabled=true);
  try{const result=await api('/api/commands',{method:'POST',body:input});state=result.state;render();status(result.message);return true;}
  catch(error){status(error.message,true);if(error.status===401)showLogin();return false;}
  finally{busy=false;document.querySelectorAll('textarea').forEach(t=>t.readOnly=false);document.querySelectorAll('button[type=submit]').forEach(b=>b.disabled=false);updatePublishDisabled();}
}
function mayReply(p){const c=state.communities.find(c=>c.id===p.community);return replyDepth(state.posts,p.id)<2&&(!p.community||['admin','contributor','commenter'].includes(c?.role));}
function mayQuote(p){const c=state.communities.find(c=>c.id===p.community);return p.audience==='public'||['admin','contributor'].includes(c?.role);}
function contextLabel(p){const c=state.communities.find(c=>c.id===p.community);return `${p.community?c?.name??'Comunidad':'General'} · ${p.audience==='public'?'Público':'Solo integrantes · Operador con acceso'}`;}
function postMarkup(p,{depth=0,savedView=false}={}){
  const saved=state.saved.includes(p.id),liked=p.likedByMe===true;
  const parent=state.posts.find(q=>q.id===p.parent);
  const replyTo=p.parent?`<p class="reply-to">En respuesta a ${parent?`<button data-context="${parent.id}">${esc(parent.authorName)}</button>`:'otro mensaje de esta conversación'}</p>`:'';
  return `<article id="post-${p.id}" tabindex="-1" class="post ${depth?`reply depth-${Math.min(depth,3)}`:''}">
    <div class="meta">${esc(p.authorName)} · ${esc(contextLabel(p))}</div>${replyTo}
    ${p.quote?quoteMarkup(p.quote):''}<p class="post-text">${esc(p.text)}</p>
    <div class="actions">
      <button class="approval" id="like-${p.id}" data-like="${p.id}" aria-pressed="${liked}" title="${liked?'Retirar':'Añadir'} Me gusta · Identidad oculta para otros usuarios"><span class="approval-mark" aria-hidden="true">✓</span> Me gusta${liked?' · Marcado':''}</button>
      <button id="save-${p.id}" data-save="${p.id}" aria-pressed="${saved}">${saved?'Guardado · Privado':'Guardar · Privado'}</button>
      ${mayReply(p)?`<button id="respond-${p.id}" data-reply="${p.id}" aria-expanded="${expandedReplies.has(p.id)}">Responder</button>`:''}
      ${mayQuote(p)?`<button data-quote="${p.id}">Citar en una publicación</button>`:''}
      ${savedView?`<button data-context="${p.id}">Ver en conversación</button>`:''}
    </div>
    <p class="hint approval-count">${p.likeCount===null||p.likeCount===undefined?'Recuento pendiente del próximo corte horario.':`${p.likeCount} ${p.likeCount===1?'aprobación':'aprobaciones'} · <time datetime="${esc(p.likesUpdatedAt)}" title="${esc(`Corte: ${dateLabel(p.likesUpdatedAt)}. Calculado: ${dateLabel(p.likesGeneratedAt)} (${localZone}).`)}">Recuento a las ${esc(new Intl.DateTimeFormat('es-ES',{hour:'2-digit',minute:'2-digit',timeZone:localZone}).format(new Date(p.likesUpdatedAt)))} · ${esc(new Intl.DateTimeFormat('es-ES',{day:'2-digit',month:'2-digit',timeZone:localZone}).format(new Date(p.likesUpdatedAt)))}</time>`}</p>
    ${replyDepth(state.posts,p.id)>=2?'<p class="hint">Último nivel de respuestas. Para continuar, inicia una publicación con cita.</p>':''}
    ${mayReply(p)?`<form class="reply-form" data-parent="${p.id}" ${expandedReplies.has(p.id)?'':'hidden'}><label for="reply-${p.id}">Responder a ${esc(p.authorName)} · Misma audiencia</label><textarea id="reply-${p.id}" maxlength="3000" required>${esc(replyDrafts.get(p.id)??'')}</textarea><button type="submit">Enviar respuesta</button></form>`:''}
  </article>`;
}
function quoteMarkup(id){const q=state.posts.find(p=>p.id===id);return q?`<blockquote><p>Cita a <button data-context="${q.id}">${esc(q.authorName)}</button></p><p>${esc(q.text.slice(0,300))}${q.text.length>300?'…':''}</p></blockquote>`:'<p>Cita no disponible.</p>';}
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
function updatePublishDisabled(){const disabled=busy||!destinationAvailable();$('publish').querySelector('button[type=submit]').disabled=disabled;$('schedule-toggle').disabled=disabled;$('schedule-confirm').disabled=disabled;$('save-draft').disabled=busy;$('save-draft-copy').disabled=busy;}
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
  const source=draft.quote?state.posts.find(p=>p.id===draft.quote):null;
  const restrictedQuote=Boolean(source&&source.audience!=='public');
  const choose=options.length>1&&destinationAvailable()&&!restrictedQuote;
  $('quote-preview').hidden=!draft.quote;
  $('quote-preview').innerHTML=draft.quote?`${source?`<p>Citarás a ${esc(source.authorName)}. Recibirá un aviso cuando se publique.</p>`:'<p>La publicación citada ya no está disponible. Retira la cita para continuar sin ella.</p>'}${quoteMarkup(draft.quote)}<button type="button" id="remove-quote">Retirar cita</button>`:'';
  $('audience').hidden=!choose;$('audience-label').hidden=!choose;
  $('schedule-options').hidden=!draft.scheduling;$('schedule-toggle').setAttribute('aria-expanded',String(Boolean(draft.scheduling)));
  $('schedule-at').value=draft.publishAt??'';$('schedule-late').value=String(draft.lateMinutes??15);
  $('schedule-zone').textContent=`Zona horaria: ${localZone}. La fecha se fija como un instante; un cambio posterior de zona no la desplaza.`;
  schedulePreview();
  if($('text').value!==draft.text)$('text').value=draft.text;
  draftStatus();
  $('audience-help').textContent=!destinationAvailable()?`Destino conservado: ${draft.destinationName??c?.name??'comunidad'} · ${draft.audience.endsWith(':members')?'Solo integrantes':'Público'}. Ya no puedes publicar aquí; el borrador no se cambia de destino.`:draft.audience.endsWith(':members')?'Solo integrantes. El operador puede leer el contenido; no hay cifrado de extremo a extremo.':inCommunity?'Publicación pública dentro de esta comunidad. No aparecerá en Inicio general.':'Publicación pública en el espacio general, fuera de las comunidades.';
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
  }else if(page==='borradores'){
    $('context').innerHTML='<h1>Borradores</h1><p>Guardados en el servidor y visibles solo para ti. Retomarlos no publica ni programa nada.</p>';
    const saved=state.drafts??[];
    const cards=list=>list.slice().reverse().map(d=>`<article class="post"><p>${esc(d.destinationName)} · ${d.audience==='members'?'Solo integrantes':'Público al publicar'}</p><p class="post-text">${esc(d.text)}</p><p class="hint">Guardado: ${esc(dateLabel(d.updatedAt))}${d.quote?' · Con cita':''}</p>${d.status==='trashed'?`<p>En la papelera. Restaurarlo conserva su estado anterior.</p><button data-restore-draft="${d.id}" data-version="${d.version}">Restaurar borrador</button>`:`${d.status==='draft'?`<button data-load-draft="${d.id}">Retomar borrador</button>`:`<p>${d.status==='published'?'Ya publicado':'Transferido a Programadas'}. Se conserva esta versión como referencia.</p>`}<button data-trash-draft="${d.id}" data-version="${d.version}">Mover a papelera</button>`}</article>`).join('');
    $('content').innerHTML=(cards(saved.filter(d=>d.status==='draft'))||'<p>No tienes borradores pendientes.</p>')+(saved.some(d=>['published','scheduled'].includes(d.status))?`<details data-panel="used-drafts"><summary>Borradores ya utilizados</summary>${cards(saved.filter(d=>['published','scheduled'].includes(d.status)))}</details>`:'')+(saved.some(d=>d.status==='trashed')?`<details data-panel="draft-trash"><summary>Papelera de borradores</summary><p>Recuperable, sin borrado automático. Mover una referencia aquí no retira una publicación ni cancela una programación.</p>${cards(saved.filter(d=>d.status==='trashed'))}</details>`:'');
  }else if(page==='avisos'){
    $('context').innerHTML='<h1>Avisos</h1><p>Citas a tus publicaciones, dentro de su audiencia. Sin correos ni avisos externos.</p>';
    $('content').innerHTML=(state.notices??[]).slice().reverse().map(n=>`<article class="post"><p>${esc(n.authorName)} ha citado una publicación tuya. ${n.read?'Leído':'Sin leer'}</p><button data-notice="${n.id}" data-post="${n.post}">Ver publicación con cita</button></article>`).join('')||'<p>No tienes avisos de citas.</p>';
  }else if(page==='programadas'){
    $('context').innerHTML='<h1>Programadas</h1><p>Solo tú ves estas publicaciones pendientes. Revisa aquí los bloqueos y vencimientos; no se reactivan automáticamente.</p>';
    $('content').innerHTML=scheduledContent();
  }else if(page==='comunidad'){
    $('context').innerHTML=selectedCommunity?`<button id="all-communities">Todas las comunidades</button><h1>${esc(c?.name??currentDraft().destinationName??'Comunidad no disponible')}</h1>${c?`<p>${c.visibility==='private'?'Privada · Solo integrantes · Operador con acceso':'Pública · El historial anterior puede seguir restringido'}</p>`:''}`:'<h1>Comunidades</h1><p>Entra en una comunidad para leer y publicar en su propio espacio.</p>';
    $('content').innerHTML=communityContent();
  }else{
    $('context').innerHTML='<h1>Mi cuenta</h1>';
    $('content').innerHTML=`<p>Actúas como ${esc(state.user.name)}. Tus guardados son privados; tus Me gusta no muestran tu identidad a otros usuarios. No se publican identidades. Los recuentos se actualizan por cortes horarios comunes; tu elección propia se muestra al instante. El servidor local conserva tu elección para permitir retirarla; no hay anonimato frente al proveedor.</p><button id="export">Exportar mis aportaciones ficticias</button><p>Esta exportación no es un perfil portable de producción.</p><button id="logout">Cerrar esta sesión</button>`;
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
function schedulePreview(){
  try{$('schedule-preview').textContent=$('schedule-at').value?`Se publicará el ${dateLabel(instant($('schedule-at').value))} (${localZone}), si conserva permisos.`:'Elige una fecha y hora futuras.';}catch(error){$('schedule-preview').textContent=error.message;}
}
function scheduledContent(){
  const labels={pending:'Pendiente',blocked:'Bloqueada',expired:'Vencida',published:'Publicada',cancelled:'Cancelada'};
  return (state.scheduled??[]).slice().reverse().map(s=>{
    const d=scheduleDrafts.get(s.id)??{text:s.publication.text,at:localInput(s.publishAt),late:s.lateMinutes};
    const active=!['published','cancelled'].includes(s.status);
    return `<article class="post"><h2>${labels[s.status]}</h2><p>${esc(contextLabel(s.publication))}</p><p>${esc(dateLabel(s.publishAt,s.timeZone))} · ${esc(s.timeZone)} · Margen: ${s.lateMinutes} minutos</p><p class="post-text">${esc(s.publication.text)}</p>${s.reason?`<p class="notice">${esc(s.reason)}</p>`:''}${active?`<details data-panel="schedule-${s.id}"><summary>Editar fecha o contenido</summary><form data-edit-schedule="${s.id}" data-version="${s.version}"><p>Destino y audiencia se conservan. Las fechas del editor se muestran en ${esc(localZone)}.</p><label for="scheduled-text-${s.id}">Texto</label><textarea id="scheduled-text-${s.id}" name="text" required maxlength="3000">${esc(d.text)}</textarea><label for="scheduled-at-${s.id}">Nueva fecha y hora</label><input id="scheduled-at-${s.id}" name="at" type="datetime-local" step="1" value="${esc(d.at)}" required><label for="scheduled-late-${s.id}">Margen de retraso</label><select id="scheduled-late-${s.id}" name="late">${[[5,'5 minutos'],[15,'15 minutos'],[60,'1 hora'],[1440,'24 horas']].map(([v,l])=>`<option value="${v}" ${Number(d.late)===v?'selected':''}>${l}</option>`).join('')}</select><button type="submit">Guardar y programar</button></form></details><div class="actions"><button data-publish-schedule="${s.id}" data-version="${s.version}">Publicar ahora</button><button data-cancel-schedule="${s.id}" data-version="${s.version}">Cancelar programación</button></div>`:''}</article>`;
  }).join('')||'<p>No tienes publicaciones programadas.</p>';
}
function draftStatus(){
  const draft=currentDraft(),stored=draft.id?(state.drafts??[]).find(d=>d.id===draft.id):null;
  const conflict=Boolean(stored&&(stored.version!==draft.version||stored.status!=='draft'));
  $('new-composition').hidden=!draft.id;
  $('save-draft-copy').hidden=!conflict;
  const clean=stored&&stored.version===draft.version&&stored.text===draft.text&&(stored.community?`${stored.community}:${stored.audience}`:'public')===draft.audience&&(stored.quote??null)===(draft.quote??null);
  $('draft-status').textContent=conflict?'Hay otra versión guardada. Se conserva lo que estás escribiendo; puedes guardarlo como copia.':clean?`Borrador guardado: ${dateLabel(stored.updatedAt)}.`:draft.text?'Cambios sin guardar. Usa Guardar borrador para recuperarlos tras recargar.':'El texto sin guardar solo se conserva en esta pestaña.';
}
function draftReference(draft){return draft.id?{draftId:draft.id,draftVersion:draft.version}:{};}
function finishComposition(draft,key){
  if(draft.id){loadedDrafts.delete(draft.id);activeDraftId=null;}else{const local=drafts.get(key);if(local){local.text='';delete local.quote;local.scheduling=false;local.publishAt='';}}
}
function bindActions(){
  document.querySelectorAll('[data-trash-draft],[data-restore-draft]').forEach(b=>b.onclick=()=>send({type:b.dataset.trashDraft?'trash-draft':'restore-draft',id:b.dataset.trashDraft??b.dataset.restoreDraft,version:Number(b.dataset.version)}));
  document.querySelectorAll('[data-load-draft]').forEach(b=>b.onclick=()=>{
    const stored=state.drafts.find(d=>d.id===b.dataset.loadDraft&&d.status==='draft');if(!stored)return;
    if(!loadedDrafts.has(stored.id))loadedDrafts.set(stored.id,{...stored,audience:stored.community?`${stored.community}:${stored.audience}`:'public'});
    activeDraftId=stored.id;selectedCommunity=stored.community;page=stored.community?'comunidad':'inicio';render();status('Borrador recuperado. Conserva su destino; no se publica automáticamente.');
  });
  if($('remove-quote'))$('remove-quote').onclick=()=>{delete currentDraft().quote;render();};
  document.querySelectorAll('[data-notice]').forEach(b=>b.onclick=async()=>{if(await send({type:'read-notice',id:b.dataset.notice}))openConversation(b.dataset.post);});
  document.querySelectorAll('[data-quote]').forEach(b=>b.onclick=()=>{
    const source=state.posts.find(p=>p.id===b.dataset.quote);
    if(!source)return;
    const c=state.communities.find(c=>c.id===source.community);
    // La cita pública puede salir a Inicio general; una privada conserva su espacio.
    selectedCommunity=source.community&&['admin','contributor'].includes(c?.role)?source.community:null;
    page=selectedCommunity?'comunidad':'inicio';
    const draft=currentDraft();draft.quote=source.id;
    if(source.audience!=='public')draft.audience=`${source.community}:members`;
    render();$('text').focus();status('Escribe tu propia publicación. El autor citado recibirá un aviso al publicarla.');
  });
  document.querySelectorAll('[data-cancel-schedule],[data-publish-schedule]').forEach(b=>b.onclick=()=>send({type:b.dataset.cancelSchedule?'cancel-schedule':'publish-schedule',id:b.dataset.cancelSchedule??b.dataset.publishSchedule,version:Number(b.dataset.version)}));
  document.querySelectorAll('[data-edit-schedule]').forEach(form=>{
    const id=form.dataset.editSchedule,fields={text:form.querySelector('[name=text]'),at:form.querySelector('[name=at]'),late:form.querySelector('[name=late]')};
    const capture=()=>{const d={text:fields.text.value,at:fields.at.value,late:fields.late.value};scheduleDrafts.set(id,d);return d;};
    Object.values(fields).forEach(f=>f.oninput=capture);
    form.onsubmit=async e=>{e.preventDefault();try{const d=capture(),s=state.scheduled.find(s=>s.id===id);if(await send({type:'edit-schedule',id,version:Number(form.dataset.version),...s.publication,text:d.text,publishAt:instant(d.at),timeZone:localZone,lateMinutes:Number(d.late)})){scheduleDrafts.delete(id);render();}}catch(error){status(error.message,true);}};
  });
  document.querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>send({type:'save',post:b.dataset.save}));
  document.querySelectorAll('[data-like]').forEach(b=>b.onclick=()=>send({type:'like',post:b.dataset.like,active:state.posts.find(p=>p.id===b.dataset.like)?.likedByMe!==true}));
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
async function saveDraft(copy=false){
  const draft=currentDraft(),key=scopeKey(),[community,audience]=draft.audience.split(':');
  const input={type:'save-draft',text:draft.text,quote:draft.quote??null,...(key==='general'?{audience:'public'}:{community,audience}),...(draft.id?(copy?{copyOf:draft.id}:{id:draft.id,version:draft.version}):{})};
  if(await send(input)){
    const saved=draft.id&&!copy?state.drafts.find(d=>d.id===draft.id):state.drafts.at(-1);
    const loaded={...saved,audience:saved.community?`${saved.community}:${saved.audience}`:'public'};
    loadedDrafts.set(saved.id,loaded);activeDraftId=saved.id;
    if(!draft.id){draft.text='';delete draft.quote;}
    render();
  }
}
$('save-draft').onclick=()=>saveDraft();$('save-draft-copy').onclick=()=>saveDraft(true);
$('new-composition').onclick=()=>{activeDraftId=null;render();status('El borrador anterior sigue en Borradores; los cambios sin guardar permanecen en esta pestaña.');};
$('schedule-toggle').onclick=()=>{currentDraft().scheduling=!currentDraft().scheduling;composer();};
$('schedule-at').oninput=()=>{currentDraft().publishAt=$('schedule-at').value;schedulePreview();};
$('schedule-late').onchange=()=>{currentDraft().lateMinutes=Number($('schedule-late').value);};
$('schedule-confirm').onclick=async()=>{
  if(!destinationAvailable())return status('El destino ya no permite publicar.',true);
  try{
    const draft=currentDraft(),key=scopeKey(),[community,audience]=draft.audience.split(':');
    const input={type:'schedule',...draftReference(draft),text:draft.text,quote:draft.quote??null,publishAt:instant(draft.publishAt),timeZone:localZone,lateMinutes:draft.lateMinutes??15,...(key==='general'?{audience:'public'}:{community,audience})};
    if(await send(input)){finishComposition(draft,key);page='programadas';render();}
  }catch(error){status(error.message,true);}
};
$('text').oninput=()=>{currentDraft().text=$('text').value;draftStatus();};
$('audience').onchange=()=>{currentDraft().audience=$('audience').value;composer();};
$('publish').onsubmit=async e=>{
  e.preventDefault();if(!destinationAvailable())return status('El destino perdió permisos. El borrador no se publica en otro espacio.',true);
  const draft=currentDraft(),[community,audience]=draft.audience.split(':'),key=scopeKey();
  const input={type:'publish',...draftReference(draft),text:draft.text,quote:draft.quote??null,...(key==='general'?{audience:'public'}:{community,audience})};
  if(await send(input)){finishComposition(draft,key);render();}
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
