// node render.cjs         -> preview.png (all 3 ghouls) + stage1-3.png close-ups
// node render.cjs golems  -> golems.png (all 3 golems) + golem1-3.png close-ups
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
  const golems = process.argv[2] === 'golems';
  const page = golems ? 'golems.html' : 'preview.html';
  const [all, one] = golems ? ['golems.png', 'golem'] : ['preview.png', 'stage'];
  const shots = [[all, '', 2000, 1180], ...[1, 2, 3].map((n) => [`${one}${n}.png`, `?only=${n}`, 1080, 1350])];
  for (const [file, q, w, h] of shots) {
    const p = await b.newPage({viewport: {width: w, height: h}});
    p.on('pageerror', e => console.log('ERR', e.message));
    await p.goto('http://localhost:8767/' + page + q);
    await p.waitForFunction('window.DONE', {timeout: 120000});
    await p.screenshot({path: path.join(__dirname, file)});
    await p.close();
  }
  await b.close(); srv.close();
})();
