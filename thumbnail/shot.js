const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+__dirname+'/thumb.html');await p.waitForTimeout(1500);
await p.screenshot({path:__dirname+'/thumbnail.png'});await b.close();})();
