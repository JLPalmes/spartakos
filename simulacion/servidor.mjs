// SPDX-License-Identifier: AGPL-3.0-or-later
import http from 'node:http';
import {randomBytes} from 'node:crypto';
import {readFile,writeFile,mkdir,rename} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {initialData,migrateData,accounts,view,canRead,command,runDue,refreshLikeCounts,RuleError} from './dominio.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const assets=new Map([
  ['/',['index.html','text/html; charset=utf-8']],
  ['/cliente',['cliente.html','text/html; charset=utf-8']],
  ['/cliente.mjs',['cliente.mjs','text/javascript; charset=utf-8']],
  ['/conversaciones.mjs',['conversaciones.mjs','text/javascript; charset=utf-8']],
  ['/estilos.css',['estilos.css','text/css; charset=utf-8']],
]);
export async function createSimulationServer({directory=path.join(here,'../resultados-locales/simulador'),clock=Date.now}={}) {
  await mkdir(directory,{recursive:true,mode:0o700});
  const filename=path.join(directory,'estado.json');
  let data;
  try {
    const original=JSON.parse(await readFile(filename,'utf8'));data=migrateData(original,clock());
    if(original.schema!==data.schema){await writeFile(`${filename}.tmp`,JSON.stringify(data,null,2),{mode:0o600});await rename(`${filename}.tmp`,filename);}
  }
  catch(error){if(error.code!=='ENOENT')throw error;data=initialData(clock());await writeFile(filename,JSON.stringify(data,null,2),{mode:0o600});}
  const sessions=new Map();
  let queue=Promise.resolve();
  function json(res,status,body){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(body));}
  async function body(req){
    if(!String(req.headers['content-type']??'').startsWith('application/json'))throw new RuleError(415,'Se requiere JSON.');
    if(Number(req.headers['content-length']??0)>16384)throw new RuleError(413,'Solicitud demasiado grande.');
    const chunks=[];let size=0;
    for await (const chunk of req){size+=chunk.length;if(size>16384)throw new RuleError(413,'Solicitud demasiado grande.');chunks.push(chunk);}
    try{return JSON.parse(Buffer.concat(chunks).toString('utf8'));}catch{throw new RuleError(400,'JSON no válido.');}
  }
  async function persist(next){
    await writeFile(`${filename}.tmp`,JSON.stringify(next,null,2),{mode:0o600});
    await rename(`${filename}.tmp`,filename);data=next;
  }
  const tick=()=>{
    const task=queue.then(async()=>{const now=clock(),due=runDue(data,now),counts=refreshLikeCounts(due.data,now);if(due.changed||counts.changed)await persist(counts.data);});
    queue=task.catch(()=>{console.error('No se pudo guardar una actualización automática; se reintentará.');});
    return queue;
  };
  let timer;
  const server=http.createServer(async(req,res)=>{
    try{
      const port=server.address().port;
      const allowedHosts=[`127.0.0.1:${port}`,`localhost:${port}`];
      if(!allowedHosts.includes(req.headers.host))throw new RuleError(403,'Host no permitido.');
      const url=new URL(req.url,`http://${req.headers.host}`);
      if(req.headers.origin && req.headers.origin!==`http://${req.headers.host}`)throw new RuleError(403,'Origen no permitido.');
      if(req.method==='GET'&&assets.has(url.pathname)){
        const [file,type]=assets.get(url.pathname);
        const bytes=await readFile(path.join(here,file));
        res.writeHead(200,{'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff',
          'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-src 'self'; frame-ancestors 'self'; base-uri 'none'; form-action 'self'",'Referrer-Policy':'no-referrer'});
        return res.end(bytes);
      }
      if(req.method==='GET'&&url.pathname==='/api/accounts')return json(res,200,{accounts});
      if(req.method==='POST'&&url.pathname==='/api/sessions'){
        const input=await body(req);
        if(!accounts.some(a=>a.id===input?.account))throw new RuleError(400,'Cuenta ficticia desconocida.');
        const token=randomBytes(32).toString('hex');sessions.set(token,input.account);
        return json(res,201,{token});
      }
      const token=(req.headers.authorization??'').replace(/^Bearer /,'');
      const actor=sessions.get(token);
      if(!actor)throw new RuleError(401,'Abre una sesión ficticia para continuar.');
      if(req.method==='GET'&&url.pathname==='/api/state')return json(res,200,view(data,actor));
      if(req.method==='GET'&&url.pathname==='/api/export')return json(res,200,{format:'spartakos-local-simulation-v5',lang:'es-ES',user:actor,drafts:view(data,actor).drafts,scheduled:view(data,actor).scheduled,posts:data.posts.filter(p=>p.author===actor),saved:[...view(data,actor).saved],liked:data.posts.filter(p=>canRead(data,actor,p)&&(data.likes[p.id]??[]).includes(actor)).map(p=>p.id),notice:'Archivo de simulación; no incluye identidad portable ni claves.'});
      if(req.method==='DELETE'&&url.pathname==='/api/session'){sessions.delete(token);return json(res,200,{message:'Sesión cerrada.'});}
      if(req.method==='POST'&&url.pathname==='/api/commands'){
        const input=await body(req);
        const task=queue.then(async()=>{
          const result=command(data,actor,input,clock());
          await persist(result.data);
          return {message:result.message,state:view(data,actor)};
        });
        queue=task.catch(()=>{});
        return json(res,200,await task);
      }
      throw new RuleError(404,'Recurso no disponible.');
    }catch(error){json(res,error.status??500,{error:error.status?error.message:'No se pudo completar la operación.'});}
  });
  server.on('listening',()=>{tick();timer=setInterval(tick,1000);timer.unref();});
  server.on('close',()=>clearInterval(timer));
  return server;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){
  const port=Number(process.env.SPARTAKOS_PORT??8787);
  if(!Number.isInteger(port)||port<0||port>65535)throw Error('Puerto no válido.');
  const server=await createSimulationServer({directory:process.env.SPARTAKOS_DATA_DIR?path.resolve(process.env.SPARTAKOS_DATA_DIR):undefined});
  server.on('error',error=>{console.error(error.code==='EADDRINUSE'?`El puerto ${port} ya está ocupado. Elige otro con SPARTAKOS_PORT.`:'No se pudo iniciar el servidor local.');process.exitCode=1;});
  server.listen(port,'127.0.0.1',()=>console.log(`Spartakos · Laboratorio local: http://127.0.0.1:${server.address().port}\nCuatro cuentas ficticias. Sin contraseñas ni datos reales. Ctrl+C para detener.`));
}
