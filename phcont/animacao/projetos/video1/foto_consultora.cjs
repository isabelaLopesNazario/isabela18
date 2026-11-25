const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--use-angle=swiftshader','--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  p.on('pageerror', e => console.log('ERRO', e.message));
  await p.goto('http://127.0.0.1:8765/ficha_consultora.html'); await p.waitForFunction(() => window.pronto === true, null, { timeout: 60000 });
  await p.screenshot({ path: process.argv[2] }); await b.close(); })();
