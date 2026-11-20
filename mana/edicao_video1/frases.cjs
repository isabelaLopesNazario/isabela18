const { chromium } = require('playwright');
const frases = {
  frase_voz: ['"EU CURTO SUA VOZ, NÉ?"', 'ele, segurando a risada'],
  frase_grava: ['"ALGUÉM GRAVA ISSO AÍ,', 'PELO AMOR DE DEUS"'],
  frase_juro: ['"EU NÃO SABIA,', 'EU JURO POR DEUS"'],
};
const css = `@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@144,900,100,1&family=Caveat:wght@700&display=swap');
html,body{margin:0;width:1080px;height:380px;background:transparent}
.w{position:absolute;left:0;right:0;top:40px;text-align:center}
.l{font-family:Fraunces,serif;font-weight:900;font-variation-settings:'SOFT' 100,'WONK' 1;color:#ffe14d;font-size:66px;line-height:1.05;white-space:nowrap;
 text-shadow:4px 5px 0 #c8321e,0 8px 22px rgba(0,0,0,.6)}
.n{font-family:Caveat,cursive;font-size:52px;color:#fff;margin-top:6px;transform:rotate(-3deg)}`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 380 } });
  for (const [n, [a, c]] of Object.entries(frases)) {
    const seg = n === 'frase_voz' ? `<div class="n">${c}</div>` : `<div class="l">${c}</div>`;
    await p.setContent(`<html><head><style>${css}</style></head><body><div class="w"><div class="l">${a}</div>${seg}</div></body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `fx/${n}.png`, omitBackground: true });
  }
  await b.close();
})();
