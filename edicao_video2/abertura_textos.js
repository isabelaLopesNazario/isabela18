const { chromium } = require('playwright');
const out = process.argv[2];
const css = `@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&display=swap');
html,body{margin:0;width:1080px;height:1920px;background:transparent}
.s{position:absolute;left:0;top:0;width:1080px;height:1000px;background:linear-gradient(180deg,rgba(9,16,34,.80) 0%,rgba(9,16,34,.55) 45%,rgba(9,16,34,0) 100%)}
.g{position:absolute;left:40px;width:1000px;text-align:center;font-family:Oswald,sans-serif;font-weight:700;text-transform:uppercase;line-height:1;color:#f7f5f6;white-space:nowrap;text-shadow:0 4px 24px rgba(0,0,0,.35)}
.g em{font-style:normal;color:#c9ad6e}`;
const quadros = {
  sombra: `<div class="s"></div>`,
  t1: `<div class="g" style="top:385px;font-size:170px">PENDÊNCIA<em>?</em></div>`,
  t2: `<div class="g" style="top:385px;font-size:170px">TRAVADA<em>?</em></div>`,
  t3: `<div class="g" style="top:405px;font-size:140px">REGIME <em>ERRADO?</em></div>`,
};
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [n, h] of Object.entries(quadros)) {
    await p.setContent(`<html><head><style>${css}</style></head><body>${h}</body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `${out}/${n}.png`, omitBackground: true });
  }
  await b.close();
})();
