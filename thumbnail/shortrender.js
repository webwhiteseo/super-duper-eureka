const {chromium}=require('playwright');const http=require('http'),fs=require('fs'),path=require('path');
const srv=http.createServer((q,res)=>{const f=path.join(__dirname,decodeURIComponent(q.url.split('?')[0]));
 fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);return res.end();}res.writeHead(200,{'Content-Type':f.endsWith('.js')?'text/javascript':'text/html'});res.end(d);});}).listen(8766);
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('http://localhost:8766/short.html');await p.waitForFunction('window.DONE',{timeout:120000});
fs.mkdirSync(__dirname+'/frames',{recursive:true});
const only=process.argv[2]?process.argv[2].split(',').map(Number):null;const N=150;
for(let i=0;i<N;i++){if(only&&!only.includes(i))continue;await p.evaluate(t=>window.renderAt(t),i/30);
 await p.screenshot({path:`${__dirname}/frames/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();srv.close();})();
