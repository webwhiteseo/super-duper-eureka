// node render.cjs -> preview.png (all 3) + stage1.png, stage2.png, stage3.png (close-ups)
const {chromium} = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const srv = http.createServer((q, res) => {
  const f = path.join(__dirname, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f, (e, d) => {
    if (e) { res.writeHead(404); return res.end(); }
    const type = f.endsWith('.js') ? 'text/javascript' : f.endsWith('.json') ? 'application/json' : 'text/html';
    res.writeHead(200, {'Content-Type': type}); res.end(d);
  });
}).listen(8767);
(async () => {
  const b = await chromium.launch({args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']});
  const shots = [['preview.png', '', 1920, 1080], ['stage1.png', '?only=1', 1080, 1080], ['stage2.png', '?only=2', 1080, 1080], ['stage3.png', '?only=3', 1080, 1080]];
  for (const [file, q, w, h] of shots) {
    const p = await b.newPage({viewport: {width: w, height: h}});
    p.on('pageerror', e => console.log('ERR', e.message));
    await p.goto('http://localhost:8767/preview.html' + q);
    await p.waitForFunction('window.DONE', {timeout: 120000});
    await p.screenshot({path: path.join(__dirname, file)});
    await p.close();
  }
  await b.close(); srv.close();
})();
