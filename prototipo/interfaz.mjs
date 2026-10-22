// SPDX-License-Identifier: AGPL-3.0-or-later
import {initialState, transition} from './modelo.mjs';
let state = initialState();
let draft = {text:'', audience:'community'};
const main = document.getElementById('main');
const feedback = document.getElementById('feedback');
const escape = text => String(text).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const examples = [
  {id:'huerto',author:'Inés · Huerto compartido',date:'Hoy, 10:30',text:'El sábado vamos a comparar qué plantas resisten mejor con menos riego. He preparado un pequeño registro. ¿Qué os ha funcionado en vuestras terrazas?',community:'Huerto compartido'},
  {id:'biblioteca',author:'Marcos · Lecturas abiertas',date:'Hoy, 09:15',text:'He encontrado una edición de dominio público que podemos leer sin registrarnos en ninguna plataforma. Propongo comentar un capítulo cada semana.',community:'Lecturas abiertas'},
];
function act(event) {
  try { state = transition(state, event); if(event.type==='publish') draft.text=''; render(); feedback.className=''; feedback.textContent=state.message; }
  catch(error) {feedback.className='error';feedback.textContent=error.message;}
}
function post(item, own=false) {
  const audience = own ? (item.audience === 'public' ? 'Público' : 'Solo integrantes · Operador con acceso') : 'Público';
  return `<article class="post"><div class="meta">${escape(own?'Alicia · Ahora':item.author)} · ${audience}</div><p class="post-text">${escape(item.text)}</p>${own?'':`<div class="actions"><button data-save="${item.id}" aria-pressed="${state.saved.includes(item.id)}">${state.saved.includes(item.id)?'Guardado en mi interés':'Me interesa · Privado'}</button><button data-follow="${item.community}" aria-pressed="${state.followed.includes(item.community)}">${state.followed.includes(item.community)?'Dejar de seguir':'Seguir conversación'}</button></div>`}</article>`;
}
function composer() {return `<section class="panel"><h2>Comparte una idea</h2><form id="composer"><label for="audience">Quién podrá leer</label><select id="audience" name="audience"><option value="community">Mi comunidad · Solo integrantes</option><option value="public">Todo el mundo · Público</option></select><p id="audience-info" class="notice">Solo integrantes. En este modo el operador podría leer el contenido; no hay cifrado de extremo a extremo.</p><label for="text">Tu publicación</label><textarea id="text" name="text" maxlength="3000" required></textarea><div class="actions"><button type="submit" class="primary">Publicar en la simulación</button></div></form></section>`;}
function community() {
  const c=state.community, census=[...new Set([...c.members,...c.protected])];
  return `<h1>Cuaderno compartido</h1><p class="intro">Comunidad ${c.visibility==='private'?'privada':'pública desde la apertura simulada'}. Alicia, Bruno y Carla son participantes ficticios.</p><p class="notice">El historial previo está protegido. La administración no es propietaria de la comunidad.</p><section class="panel"><h2>Apertura de la comunidad</h2><p>Publicar de forma abierta en adelante requiere aprobación expresa de todo el censo protegido. Guardar el historial no elimina esa obligación.</p>${c.visibility==='private'?`<button data-action="propose-open">${c.proposal?'Reiniciar propuesta sin conservar votos':'Preparar propuesta de apertura'}</button>`:'<p>La apertura se ha completado en la simulación.</p>'}${c.proposal?`<p>Propuesta ${c.version}: apertura futura, sin publicar el historial anterior.</p>${census.map(id=>`<div class="person"><span>${escape(id)}${c.protected.includes(id)?' · protección conservada tras la baja':''} · ${c.consents[id]?'Ha consentido':'Sin consentimiento'}</span><div class="actions"><button data-consent="${id}" data-value="yes">Simular consentimiento</button><button data-consent="${id}" data-value="no">Simular negativa</button></div></div>`).join('')}<div class="actions"><button class="primary" data-action="open">Comprobar unanimidad y abrir</button></div>`:''}</section><details><summary>Escenario de prueba: baja durante una propuesta</summary><p>Las bajas cancelan la propuesta y conservan la protección para impedir que se eluda una negativa.</p><button data-remove="carla" ${!c.members.includes('carla')?'disabled':''}>Simular baja de Carla</button></details>${state.posts.filter(p=>p.audience==='community').map(p=>post(p,true)).join('')}`;
}
function render() {
  document.querySelectorAll('nav a').forEach(a=>{if(a.hash===`#${state.page}`) a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  const pages = {
    inicio:()=>`<h1>Tu inicio</h1><p class="intro">Lectura cronológica. Puedes empezar sin importar tu archivo ni encontrar contactos conocidos.</p>${composer()}<h2>Conversaciones abiertas para empezar</h2><p class="meta">Selección de ejemplo identificada. Seguir una conversación es opcional.</p>${examples.map(p=>post(p)).join('')}${state.posts.filter(p=>p.audience==='public').map(p=>post(p,true)).join('')}<p class="meta">Has llegado al final. No hay reproducción ni carga continuas.</p>`,
    explorar:()=>`<h1>Explorar a tu ritmo</h1><p class="intro">Dos comunidades públicas de ejemplo. No usamos tus guardados privados para seleccionarlas.</p>${examples.map(p=>post(p)).join('')}`,
    guardado:()=>`<h1>Mi interés</h1><p class="intro">Solo tú ves esta selección. Guardar no significa estar de acuerdo ni acredita reputación.</p>${state.saved.length?examples.filter(p=>state.saved.includes(p.id)).map(p=>post(p)).join(''):'<p class="empty">Todavía no has guardado nada. Puedes hacerlo desde una conversación.</p>'}`,
    comunidad:community,
    archivo:()=>`<h1>Mi archivo</h1><p class="intro">Conservar historia y reencontrar personas son funciones distintas. Importar es opcional.</p><section class="panel"><h2>Importación de ejemplo</h2><p>Esta demostración no abre archivos personales ni conecta con otras redes.</p><ul><li>Una publicación pública: se conserva en archivo privado hasta que decidas compartirla.</li><li>Una conversación privada: excluida de publicación.</li><li>Una referencia a un contacto: no crea una cuenta ni envía invitaciones.</li></ul><button class="primary" data-action="import-demo">${state.imported?'Repetir importación ficticia':'Incorporar archivo ficticio'}</button></section>${state.imported?'<section class="panel"><h2>Archivo personal · Solo tú</h2><p>Entrada de ejemplo · Fecha original: 12 de mayo de 2024</p><p>Mi primer cuaderno sobre el huerto.</p><p class="notice">Contacto de origen: @persona-ejemplo · Sin vínculo confirmado con una cuenta de Spartakos.</p></section>':''}`,
    continuidad:()=>`<h1>Mi cuenta y salida</h1><p class="intro">El proveedor presta un servicio. No es propietario de tu identidad.</p><section class="panel"><h2>Cambiar de proveedor</h2><p>En el sistema previsto conservarías identidad y referencias, con comprobación de qué datos y servicios se trasladan. Este prototipo no realiza el traslado.</p><p class="notice warning">La continuidad requiere un receptor con capacidad y los medios de recuperación previstos. Una maqueta no demuestra ninguna de esas garantías.</p></section><section class="panel"><h2>Exportar esta demostración</h2><p>Descarga únicamente tus acciones ficticias de esta sesión. No es el formato de exportación definitivo.</p><button id="export">Descargar datos ficticios</button></section><section class="panel"><h2>Recuperación y cuenta huérfana</h2><p>Recuperar identidad no equivale a recuperar claves de contenido cifrado. Una marca de control no recuperado exige revisión; nunca se deduce solo de la inactividad.</p></section>`,
  };
  main.innerHTML = pages[state.page]();
  main.querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>act({type:'save',id:b.dataset.save}));
  main.querySelectorAll('[data-follow]').forEach(b=>b.onclick=()=>act({type:'follow',id:b.dataset.follow}));
  main.querySelectorAll('[data-action]').forEach(b=>b.onclick=()=>act({type:b.dataset.action}));
  main.querySelectorAll('[data-consent]').forEach(b=>b.onclick=()=>act({type:'consent',member:b.dataset.consent,value:b.dataset.value==='yes',version:state.community.version}));
  main.querySelectorAll('[data-remove]').forEach(b=>b.onclick=()=>act({type:'remove-member',member:b.dataset.remove}));
  const form=document.getElementById('composer');
  if(form){
    const audience=document.getElementById('audience');
    audience.value=draft.audience;
    const editor=document.getElementById('text');
    editor.value=draft.text;
    editor.oninput=()=>{draft.text=editor.value;};
    const updateAudience=()=>{draft.audience=audience.value;document.getElementById('audience-info').textContent=audience.value==='public'?'Todo el mundo podrá leer esta publicación.':'Solo integrantes. En este modo el operador podría leer el contenido; no hay cifrado de extremo a extremo.';};
    audience.onchange=updateAudience;
    updateAudience();
    form.onsubmit=e=>{e.preventDefault();act({type:'publish',audience:audience.value,text:document.getElementById('text').value});};
  }
  const exp=document.getElementById('export');
  if(exp) exp.onclick=()=>{
    const data={kind:'spartakos-demo-not-production',lang:'es-ES',saved:state.saved,followed:state.followed,posts:state.posts,importedDemo:state.imported};
    const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
    const a=document.createElement('a');a.href=url;a.download='spartakos-demostracion.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    feedback.textContent='Descarga preparada con datos ficticios de esta sesión.';
  };
}
function navigate(){const page=location.hash.slice(1)||'inicio';try{state=transition(state,{type:'navigate',page});}catch{state.page='inicio';}render();feedback.textContent='';}
window.addEventListener('hashchange',navigate);
navigate();
