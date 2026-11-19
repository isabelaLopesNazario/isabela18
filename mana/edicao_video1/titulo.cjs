const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 350 } });
  await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const w = await p.evaluate(() => Math.max(...[...document.querySelectorAll('.l')].map(e => e.scrollWidth)));
  console.log('largura', w);
  await p.screenshot({ path: process.argv[3], omitBackground: true }); await b.close(); })();
