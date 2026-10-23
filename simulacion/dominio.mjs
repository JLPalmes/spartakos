// SPDX-License-Identifier: AGPL-3.0-or-later
import {replyDepth} from './conversaciones.mjs';
// Reglas de un laboratorio local con identidades ficticias; no protocolo distribuido.
export class RuleError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
const fail = (status, message) => { throw new RuleError(status, message); };
export const accounts = [
  {id:'alicia', name:'Alicia', description:'Administra la comunidad privada'},
  {id:'bruno', name:'Bruno', description:'Puede leer, comentar y publicar en ella'},
  {id:'carla', name:'Carla', description:'Puede leer; no comentar ni publicar en ella'},
  {id:'diego', name:'Diego', description:'No pertenece a la comunidad privada'},
];
export function initialData(now=Date.now()) {
  return {schema:6,drafts:[],nextDraftId:1,likeBatch:{baselineAt:new Date(now).toISOString(),updatedAt:null,generatedAt:null,counts:{},changes:[]},seenQuotes:{}, revision:0, nextId:3,likes:{},scheduled:[],nextScheduleId:1,
    communities:[{id:'cuaderno',name:'Cuaderno compartido',visibility:'private',
      members:{alicia:'admin',bruno:'contributor',carla:'reader'},
      protected:['alicia','bruno','carla'],proposal:null,proposalVersion:0}],
    posts:[
      {id:'p1',author:'bruno',text:'¿Qué libro os gustaría comentar esta semana?',audience:'public',community:null,parent:null,createdAt:'2026-10-22T09:00:00.000Z'},
      {id:'p2',author:'alicia',text:'Este cuaderno es privado. Podemos preparar aquí nuestras ideas.',audience:'members',community:'cuaderno',parent:null,createdAt:'2026-10-22T09:10:00.000Z'},
    ],saved:Object.fromEntries(accounts.map(a=>[a.id,[]]))};
}
export function migrateData(original,now=Date.now()) {
  if(![1,2,3,4,5,6].includes(original.schema))throw Error('Versión de datos no compatible.');
  const data=structuredClone(original);
  if(data.schema===1){data.schema=2;data.likes={};}
  if(data.schema===2){data.schema=3;data.scheduled=[];data.nextScheduleId=1;}
  if(data.schema===3){data.schema=4;data.seenQuotes={};}
  if(data.schema===4){data.schema=5;data.likeBatch={baselineAt:new Date(now).toISOString(),updatedAt:null,generatedAt:null,counts:Object.fromEntries(Object.entries(data.likes??{}).map(([id,actors])=>[id,actors.length])),changes:[]};}
  if(data.schema===5){data.schema=6;data.drafts=[];data.nextDraftId=1;}
  if(!Array.isArray(data.drafts)||!Number.isSafeInteger(data.nextDraftId))throw Error('Registro de borradores no válido.');
  if(!data.likeBatch||!Array.isArray(data.likeBatch.changes))throw Error('Registro de recuentos no válido.');
  if(!data.seenQuotes||typeof data.seenQuotes!=='object'||Array.isArray(data.seenQuotes))throw Error('Registro de avisos no válido.');
  if(!Array.isArray(data.scheduled)||!Number.isSafeInteger(data.nextScheduleId))throw Error('Registro de programación no válido.');
  if(!data.likes || typeof data.likes!=='object' || Array.isArray(data.likes))throw Error('Registro de reacciones no válido.');
  return data;
}
export function canRead(data, actor, post) {
  if (post.audience==='public') return true;
  const community=data.communities.find(c=>c.id===post.community);
  return Boolean(community?.members[actor]);
}
function findCommunity(data, actor, id, {protectedAccess=false}={}) {
  const c=data.communities.find(c=>c.id===id);
  if (!c || (!c.members[actor] && c.visibility!=='public' && !(protectedAccess && c.protected.includes(actor)))) fail(404,'Comunidad no disponible.');
  return c;
}
function admin(c, actor) { if (c.members[actor]!=='admin') fail(403,'Esta acción requiere administración de la comunidad.'); }
export function view(data, actor) {
  const posts=data.posts.filter(p=>canRead(data,actor,p));
  return {revision:data.revision,user:accounts.find(a=>a.id===actor),
    posts:posts.map(p=>({...p,authorName:accounts.find(a=>a.id===p.author)?.name??p.author,
      likedByMe:(data.likes?.[p.id]??[]).includes(actor),
      likeCount:data.likeBatch.updatedAt&&Date.parse(p.createdAt)<Date.parse(data.likeBatch.updatedAt)?data.likeBatch.counts[p.id]??0:null,
      likesUpdatedAt:data.likeBatch.updatedAt,likesGeneratedAt:data.likeBatch.generatedAt})),
    notices:quoteNotices(data,actor),
    drafts:data.drafts.filter(d=>d.author===actor),
    scheduled:data.scheduled.filter(s=>s.author===actor),
    saved:data.saved[actor].filter(id=>posts.some(p=>p.id===id)),
    communities:data.communities.filter(c=>c.visibility==='public'||c.members[actor]).map(c=>({...c,role:c.members[actor]??null})),
    formerProposals:data.communities.filter(c=>!c.members[actor]&&c.proposal&&c.protected.includes(actor)).map(c=>({id:c.id,name:c.name,proposal:c.proposal})),
  };
}
function quoteNotices(data,actor){
  return data.posts.filter(p=>p.quote&&p.author!==actor&&canRead(data,actor,p)&&data.posts.some(q=>q.id===p.quote&&q.author===actor&&canRead(data,actor,q))).map(p=>({id:p.id,post:p.id,quoted:p.quote,authorName:accounts.find(a=>a.id===p.author)?.name??p.author,read:(data.seenQuotes[actor]??[]).includes(p.id)}));
}
export function command(original, actor, input, now=Date.now()) {
  if (!accounts.some(a=>a.id===actor)) fail(401,'Sesión no válida.');
  if (!input || typeof input!=='object' || Array.isArray(input)) fail(400,'Acción no válida.');
  const data=structuredClone(original);
  let message='Cambios guardados.';
  let sourceDraft=null;
  if(['publish','schedule'].includes(input.type)&&input.draftId){
    sourceDraft=data.drafts.find(d=>d.id===input.draftId&&d.author===actor);
    if(!sourceDraft)fail(404,'Borrador no disponible.');
    if(sourceDraft.status!=='draft'||sourceDraft.version!==input.draftVersion)fail(409,'El borrador ha cambiado o ya se ha utilizado. Se conserva tu texto; revisa la versión guardada.');
    if((input.community??null)!==sourceDraft.community||input.parent)fail(400,'El borrador debe conservar su espacio de publicación.');
  }
  if(input.type==='save-draft'){
    const text=typeof input.text==='string'?input.text:'';
    if(!text.trim()||text.length>3000)fail(400,'Escribe entre 1 y 3000 caracteres para guardar el borrador.');
    if(input.parent)fail(400,'Esta versión guarda borradores de publicaciones iniciales, no respuestas.');
    let draft=null,source=null;
    if(input.id||input.copyOf){
      source=data.drafts.find(d=>d.id===(input.id??input.copyOf)&&d.author===actor);
      if(!source)fail(404,'Borrador no disponible.');
      if(input.id&&source.status!=='draft')fail(409,'El borrador ya se ha utilizado.');
      if(input.id){draft=source;if(draft.version!==input.version)fail(409,'Hay otra versión guardada. Tu texto se conserva; puedes guardarlo como copia.');}
      if((input.community??null)!==source.community)fail(400,'Conserva el espacio del borrador original.');
    }
    const community=input.community??null,audience=input.audience;
    let destinationName='Inicio general';
    if(community){
      const c=data.communities.find(c=>c.id===community);
      const retained=source&&source.community===community&&source.audience===audience;
      if(!retained)findCommunity(data,actor,community);
      if(!['members','public'].includes(audience)||(!retained&&c?.visibility==='private'&&audience!=='members'))fail(400,'Audiencia no válida para este borrador.');
      destinationName=source?.destinationName??c?.name??'Comunidad no disponible';
    }else if(audience!=='public')fail(400,'El borrador general debe mantener audiencia pública.');
    const quote=input.quote??null;
    if(quote&&quote!==source?.quote){
      const target=data.posts.find(p=>p.id===quote);
      if(!target||!canRead(data,actor,target))fail(404,'Publicación citada no disponible.');
      if(target.audience!=='public'&&(community!==target.community||audience!=='members'))fail(403,'La cita debe conservar su audiencia restringida.');
    }
    // Una cita conservada tampoco puede ampliar audiencia tras abrirse la comunidad.
    if(quote){const target=data.posts.find(p=>p.id===quote);if(target&&target.audience!=='public'&&(community!==target.community||audience!=='members'))fail(403,'La cita debe conservar su audiencia restringida.');}
    const values={text,community,audience,quote,destinationName,updatedAt:new Date(now).toISOString()};
    if(draft){Object.assign(draft,values);draft.version++;}
    else data.drafts.push({id:`d${data.nextDraftId++}`,author:actor,version:1,status:'draft',createdAt:new Date(now).toISOString(),...values});
    message='Borrador guardado en el servidor. Solo tú lo ves; no está publicado ni programado.';
  }else if(['schedule','edit-schedule','cancel-schedule','publish-schedule'].includes(input.type)) {
    let item;
    if(input.type!=='schedule'){
      item=data.scheduled.find(s=>s.id===input.id&&s.author===actor);
      if(!item)fail(404,'Programación no disponible.');
      if(item.version!==input.version)fail(409,'La programación ha cambiado. Revisa su estado antes de continuar.');
      if(['published','cancelled'].includes(item.status))fail(409,'Esta programación ya ha terminado.');
    }
    if(input.type==='cancel-schedule'){
      item.status='cancelled';item.version++;message='Programación cancelada.';
    }else if(input.type==='publish-schedule'){
      const result=command(data,actor,{...item.publication,type:'publish'},now);
      Object.assign(data,result.data);item=data.scheduled.find(s=>s.id===input.id);
      item.status='published';item.postId=data.posts.at(-1).id;item.version++;message='Publicada ahora; programación finalizada.';
    }else{
      if(input.parent)fail(400,'Esta versión programa publicaciones iniciales, no respuestas.');
      // Valida texto, destino y permisos usando exactamente las reglas de publicación.
      const checked=command(data,actor,{type:'publish',text:input.text,community:input.community,audience:input.audience,quote:input.quote},now).data.posts.at(-1);
      const due=typeof input.publishAt==='string'&&/(Z|[+-]\d{2}:\d{2})$/.test(input.publishAt)?Date.parse(input.publishAt):NaN;
      if(!Number.isFinite(due)||due<=now)fail(400,'Elige una fecha y hora futuras con zona horaria.');
      try{if(typeof input.timeZone!=='string')throw Error();new Intl.DateTimeFormat('es-ES',{timeZone:input.timeZone}).format(due);}catch{fail(400,'Zona horaria no válida.');}
      if(![5,15,60,1440].includes(input.lateMinutes))fail(400,'Elige un margen de retraso de 5, 15, 60 o 1440 minutos.');
      const values={publication:{text:checked.text,community:checked.community,audience:checked.audience,quote:checked.quote??null},publishAt:new Date(due).toISOString(),timeZone:input.timeZone,lateMinutes:input.lateMinutes,status:'pending',reason:null};
      if(item){Object.assign(item,values);item.version++;}
      else data.scheduled.push({id:`s${data.nextScheduleId++}`,author:actor,version:1,createdAt:new Date(now).toISOString(),...values});
      message='Programación guardada. El servidor publicará si conserva permisos y está dentro del margen autorizado.';
    }
  } else if (input.type==='publish') {
    const text=typeof input.text==='string'?input.text.trim():'';
    if (!text || text.length>3000) fail(400,'Escribe entre 1 y 3000 caracteres.');
    let audience='public',community=null,parent=null,quote=null;
    if(input.parent&&input.quote)fail(400,'Una cita inicia una publicación propia, no una respuesta anidada.');
    if (input.parent) {
      const target=data.posts.find(p=>p.id===input.parent);
      if (!target || !canRead(data,actor,target)) fail(404,'Publicación no disponible.');
      parent=target.id;audience=target.audience;community=target.community;
    } else if (input.community) {
      community=input.community;
      const c=findCommunity(data,actor,community);
      if(!['public','members'].includes(input.audience))fail(400,'Indica expresamente la audiencia de la publicación.');
      if(c.visibility==='private'&&input.audience!=='members')fail(400,'Una comunidad privada no admite publicaciones públicas.');
      audience=input.audience;
    } else if (input.audience!=='public') fail(400,'Elige una audiencia válida.');
    if (community) {
      const c=findCommunity(data,actor,community);
      const permitted=parent?['admin','contributor','commenter']:['admin','contributor'];
      if (!permitted.includes(c.members[actor])) fail(403,parent?'No tienes permiso para comentar aquí.':'No tienes permiso para iniciar publicaciones aquí.');
    }
    if(parent&&replyDepth(data.posts,parent)>=2)fail(409,'Se ha alcanzado el límite de tres niveles. Puedes continuar citando en una publicación propia.');
    if(input.quote){
      const target=data.posts.find(p=>p.id===input.quote);
      if(!target||!canRead(data,actor,target))fail(404,'Publicación no disponible.');
      if(target.audience!=='public'&&(audience!=='members'||community!==target.community))fail(403,'Una cita privada debe conservar la comunidad y la audiencia restringida.');
      quote=target.id;
    }
    data.posts.push({id:`p${data.nextId++}`,author:actor,text,audience,community,parent,quote,createdAt:new Date(now).toISOString()});
    message=parent?'Respuesta publicada.':quote?'Publicación con cita guardada. El autor citado dispone de un aviso en la aplicación.':'Publicación guardada.';
  } else if(input.type==='read-notice'){
    if(!quoteNotices(data,actor).some(n=>n.id===input.id))fail(404,'Aviso no disponible.');
    data.seenQuotes[actor]=[...new Set([...(data.seenQuotes[actor]??[]),input.id])];
    message='Aviso marcado como leído.';
  } else if (input.type==='save') {
    const post=data.posts.find(p=>p.id===input.post);
    if (!post || !canRead(data,actor,post)) fail(404,'Publicación no disponible.');
    const saved=data.saved[actor];
    data.saved[actor]=saved.includes(post.id)?saved.filter(id=>id!==post.id):[...saved,post.id];
    message='Guardados actualizados. No se comunica al autor.';
  } else if(input.type==='like') {
    const post=data.posts.find(p=>p.id===input.post);
    if(!post || !canRead(data,actor,post))fail(404,'Publicación no disponible.');
    if(typeof input.active!=='boolean')fail(400,'Indica si quieres añadir o retirar Me gusta.');
    data.likes??={};
    const current=data.likes[post.id]??[];
    if(current.includes(actor)!==input.active)data.likeBatch.changes.push({post:post.id,delta:input.active?1:-1,at:Math.max(now,Date.parse(data.likeBatch.updatedAt??data.likeBatch.baselineAt))});
    data.likes[post.id]=input.active?[...new Set([...current,actor])]:current.filter(id=>id!==actor);
    message=input.active?'Me gusta guardado. Tu elección no se muestra a otras personas.':'Me gusta retirado.';
  } else if (['propose','consent','open','remove','set-role'].includes(input.type)) {
    const c=findCommunity(data,actor,input.community,{protectedAccess:input.type==='consent'});
    if (input.type==='propose') {
      admin(c,actor);
      if(c.visibility!=='private') fail(409,'La comunidad ya es pública.');
      if(c.proposal) fail(409,'Ya hay una propuesta vigente.');
      c.proposal={version:++c.proposalVersion,census:[...new Set([...Object.keys(c.members),...c.protected])],consents:[],history:'protected'};
      message='Propuesta abierta: solo publicaciones futuras; historial previo protegido.';
    } else if (input.type==='consent') {
      if(!c.proposal || input.version!==c.proposal.version) fail(409,'La propuesta ha cambiado o ya está cerrada.');
      if(!c.proposal.census.includes(actor)) fail(403,'No perteneces al censo de esta propuesta.');
      if(typeof input.accept!=='boolean') fail(400,'Debes aceptar o rechazar expresamente.');
      if(!input.accept) {c.proposal=null;message='La negativa cierra la propuesta. La comunidad continúa privada.';}
      else {if(!c.proposal.consents.includes(actor))c.proposal.consents.push(actor);message='Tu consentimiento está registrado para esta propuesta.';}
    } else if(input.type==='open') {
      admin(c,actor);
      if(!c.proposal || input.version!==c.proposal.version) fail(409,'La propuesta ha cambiado o ya está cerrada.');
      if(!c.proposal.census.length || !c.proposal.census.every(id=>c.proposal.consents.includes(id))) fail(409,'Falta consentimiento expreso de todo el censo protegido.');
      c.visibility='public';c.proposal=null;
      message='Comunidad abierta para publicaciones futuras. El historial anterior sigue restringido.';
    } else if(input.type==='set-role') {
      admin(c,actor);
      if(typeof input.member!=='string'||!Object.hasOwn(c.members,input.member))fail(404,'La persona no es integrante actual.');
      if(c.members[input.member]==='admin')fail(409,'La sucesión de administración queda fuera de esta simulación.');
      if(!['reader','commenter','contributor'].includes(input.role))fail(400,'Permiso no válido.');
      c.members[input.member]=input.role;
      message='Permiso actualizado. El consentimiento para abrir la comunidad no cambia con el rol.';
    } else {
      admin(c,actor);
      if(typeof input.member!=='string'||!Object.hasOwn(c.members,input.member)) fail(404,'La persona no es integrante actual.');
      if(c.members[input.member]==='admin') fail(409,'No se puede retirar la única administración en este laboratorio.');
      if(!c.protected.includes(input.member))c.protected.push(input.member);
      delete c.members[input.member];c.proposal=null;c.proposalVersion++;
      message='Baja aplicada. Se cancela la propuesta y se conserva la protección frente a una apertura elusiva.';
    }
  } else fail(400,'Acción desconocida.');
  if(sourceDraft){
    const stored=data.drafts.find(d=>d.id===sourceDraft.id);
    const publication=input.type==='publish'?data.posts.at(-1):data.scheduled.at(-1).publication;
    Object.assign(stored,{text:publication.text,audience:publication.audience,quote:publication.quote??null});
    stored.status=input.type==='publish'?'published':'scheduled';stored.version++;stored.updatedAt=new Date(now).toISOString();
    if(input.type==='publish')stored.postId=data.posts.at(-1).id;else stored.scheduleId=data.scheduled.at(-1).id;
  }
  data.revision++;
  return {data,message};
}

// Una única transición persistida por el servidor: publicación y cierre se guardan juntas.
export function runDue(original,now=Date.now()) {
  let data=structuredClone(original),changed=false;
  for(const id of data.scheduled.filter(s=>s.status==='pending'&&Date.parse(s.publishAt)<=now).map(s=>s.id)){
    let item=data.scheduled.find(s=>s.id===id);
    if(now>Date.parse(item.publishAt)+item.lateMinutes*60000){
      item.status='expired';item.reason='Se superó el margen de retraso autorizado.';
    }else{
      try{
        const result=command(data,item.author,{...item.publication,type:'publish'},now);
        data=result.data;item=data.scheduled.find(s=>s.id===id);
        item.status='published';item.postId=data.posts.at(-1).id;item.reason=null;
      }catch(error){if(!(error instanceof RuleError))throw error;item.status='blocked';item.reason='El destino o los permisos ya no permiten publicar. Revisa y vuelve a programar.';}
    }
    item.version++;changed=true;
  }
  if(changed)data.revision++;
  return {data,changed};
}

// Cortes comunes UTC: [corte anterior, corte actual). No entrega cambios intermedios.
export function refreshLikeCounts(original,now=Date.now()) {
  const cutoff=Math.floor(now/3600000)*3600000,batch=original.likeBatch;
  if(cutoff<Date.parse(batch.baselineAt)||(batch.updatedAt&&cutoff<=Date.parse(batch.updatedAt)))return {data:original,changed:false};
  const data=structuredClone(original),next=data.likeBatch;
  for(const event of next.changes.filter(e=>e.at<cutoff))next.counts[event.post]=(next.counts[event.post]??0)+event.delta;
  next.changes=next.changes.filter(e=>e.at>=cutoff);
  next.updatedAt=new Date(cutoff).toISOString();next.generatedAt=new Date(now).toISOString();
  data.revision++;
  return {data,changed:true};
}
