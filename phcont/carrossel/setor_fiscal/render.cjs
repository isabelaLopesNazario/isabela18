const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (let i = 1; i <= 7; i++) {
    await p.goto('file://' + __dirname + '/carrossel.html?s=' + i, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: __dirname + '/final/phcont_setor_fiscal_' + i + '.png' });
  }
  await b.close();
})();
