const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const srv=http.createServer((q,res)=>{const f=path.join(__dirname,decodeURIComponent(q.url.split('?')[0]));
 fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);return res.end();}res.writeHead(200,{'Content-Type':f.endsWith('.js')?'text/javascript':'text/html'});res.end(d);});}).listen(8765);
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1920,height:1080}});p.on('console',m=>console.log(m.text()));p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('http://localhost:8765/'+(process.argv[2]||'scene.html'));await p.waitForFunction('window.DONE',{timeout:120000});await p.waitForTimeout(500);
await p.screenshot({path:__dirname+'/'+(process.argv[3]||'thumbnail.png')});await b.close();srv.close();})();
