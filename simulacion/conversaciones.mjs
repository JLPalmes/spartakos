// SPDX-License-Identifier: AGPL-3.0-or-later
// Selectores sobre la vista ya autorizada por el servidor.
export function feedRoots(posts,community=null) {
  return posts.filter(p=>p.parent===null&&p.community===community).slice().reverse();
}
export function rootFor(posts,id) {
  const byId=new Map(posts.map(p=>[p.id,p]));
  const visited=new Set();
  let current=byId.get(id);
  while(current?.parent){
    if(visited.has(current.id))return null;
    visited.add(current.id);current=byId.get(current.parent);
  }
  return current??null;
}
export function conversationRows(posts,rootId) {
  const byId=new Map(posts.map(p=>[p.id,p]));
  if(!byId.has(rootId))return [];
  const children=new Map();
  for(const p of posts){if(!children.has(p.parent))children.set(p.parent,[]);children.get(p.parent).push(p);}
  const stack=[{post:byId.get(rootId),depth:0}],rows=[],visited=new Set();
  while(stack.length){
    const row=stack.pop();
    if(visited.has(row.post.id))continue;
    visited.add(row.post.id);rows.push(row);
    for(const post of (children.get(row.post.id)??[]).slice().reverse())stack.push({post,depth:row.depth+1});
  }
  return rows;
}
