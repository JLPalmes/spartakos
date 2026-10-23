// SPDX-License-Identifier: AGPL-3.0-or-later
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
export function initialData() {
  return {schema:2, revision:0, nextId:3,likes:{},
    communities:[{id:'cuaderno',name:'Cuaderno compartido',visibility:'private',
      members:{alicia:'admin',bruno:'contributor',carla:'reader'},
      protected:['alicia','bruno','carla'],proposal:null,proposalVersion:0}],
    posts:[
      {id:'p1',author:'bruno',text:'¿Qué libro os gustaría comentar esta semana?',audience:'public',community:null,parent:null,createdAt:'2026-10-22T09:00:00.000Z'},
      {id:'p2',author:'alicia',text:'Este cuaderno es privado. Podemos preparar aquí nuestras ideas.',audience:'members',community:'cuaderno',parent:null,createdAt:'2026-10-22T09:10:00.000Z'},
    ],saved:Object.fromEntries(accounts.map(a=>[a.id,[]]))};
}
export function migrateData(original) {
  if(![1,2].includes(original.schema))throw Error('Versión de datos no compatible.');
  const data=structuredClone(original);
  if(data.schema===1){data.schema=2;data.likes={};}
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
      likes:(data.likes?.[p.id]??[]).map(id=>({id,name:accounts.find(a=>a.id===id)?.name??id}))})),
    saved:data.saved[actor].filter(id=>posts.some(p=>p.id===id)),
    communities:data.communities.filter(c=>c.visibility==='public'||c.members[actor]).map(c=>({...c,role:c.members[actor]??null})),
    formerProposals:data.communities.filter(c=>!c.members[actor]&&c.proposal&&c.protected.includes(actor)).map(c=>({id:c.id,name:c.name,proposal:c.proposal})),
  };
}
export function command(original, actor, input) {
  if (!accounts.some(a=>a.id===actor)) fail(401,'Sesión no válida.');
  if (!input || typeof input!=='object' || Array.isArray(input)) fail(400,'Acción no válida.');
  const data=structuredClone(original);
  let message='Cambios guardados.';
  if (input.type==='publish') {
    const text=typeof input.text==='string'?input.text.trim():'';
    if (!text || text.length>3000) fail(400,'Escribe entre 1 y 3000 caracteres.');
    let audience='public',community=null,parent=null;
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
    data.posts.push({id:`p${data.nextId++}`,author:actor,text,audience,community,parent,createdAt:new Date().toISOString()});
    message=parent?'Respuesta publicada.':'Publicación guardada.';
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
    data.likes[post.id]=input.active?[...new Set([...current,actor])]:current.filter(id=>id!==actor);
    message=input.active?'Me gusta añadido para la audiencia de esta publicación.':'Me gusta retirado.';
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
  data.revision++;
  return {data,message};
}
