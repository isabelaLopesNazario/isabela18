"""Gera um carrossel da DoctorFit (imagens 1080x1350 prontas para o Instagram) no estilo editorial aprovado.

Uso:  python3 gerar_carrossel.py <roteiro.json> <pasta de saída>

roteiro.json:
{
  "slides": [
    {"tipo": "capa",  "foto": "fotos/aluno.jpg", "foco": "50% 30%",
     "rotulo": "TREINO PERSONALIZADO",
     "titulo": "NÃO É SÓ\\n*treinar*",          # *palavra* = serifada itálica limão;  !palavra! = condensada limão
     "texto": "É treinar com **propósito**.",   # **palavra** = negrito limão
     "rodape": ["FOCO", "MÉTODO", "EVOLUÇÃO"]},
    {"tipo": "texto", "foto": "...", "titulo": "...", "texto": "...", "vidro": true},
    {"tipo": "cta",   "foto": "...", "titulo": "...", "texto": "...", "botao": "AGENDE SUA AULA EXPERIMENTAL!"}
  ]
}
Caminhos de foto são relativos ao roteiro.json. Sem foto, o fundo é grafite com granulado.
"""
import html, json, re, subprocess, sys
from pathlib import Path

ROTEIRO = Path(sys.argv[1]).resolve()
SAIDA = Path(sys.argv[2]).resolve()
SAIDA.mkdir(parents=True, exist_ok=True)
BASE = ROTEIRO.parent
SKILL = Path(__file__).resolve().parent.parent
LOGO = (SKILL / "assets" / "logo_transparente.png").as_uri()
dados = json.loads(ROTEIRO.read_text(encoding="utf-8"))
slides = dados["slides"]
N = len(slides)

LIMA, PRETO, BRANCO = "#ccf200", "#0c0c0c", "#f8f8f8"

def titulo_html(t):
    linhas = []
    for linha in t.split("\n"):
        e = html.escape(linha)
        e = re.sub(r"\*(.+?)\*", r'<span class="serif">\1</span>', e)
        e = re.sub(r"!(.+?)!", r'<span class="lima">\1</span>', e)
        linhas.append(f"<span class='ln'>{e}</span>")
    return "".join(linhas)

def texto_html(t):
    e = html.escape(t).replace("\n", "<br>")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", e)

GRAO = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
        "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
        "<feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .10 0'/></filter>"
        "<rect width='100%' height='100%' filter='url(%23n)'/></svg>\")")

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Playfair+Display:ital,wght@1,600;1,700&family=Poppins:wght@400;600;800&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1350px; overflow: hidden; background: {PRETO}; }}
.s {{ position: relative; width: 1080px; height: 1350px; overflow: hidden; color: {BRANCO}; font-family: 'Poppins', sans-serif;
  background: radial-gradient(ellipse 90% 60% at 50% 30%, #23271f 0%, #121411 55%, #060706 100%); }}
.foto {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(.85) contrast(1.05); }}
.escurece {{ position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(6,7,6,.70) 0%, rgba(6,7,6,.15) 32%, rgba(6,7,6,.25) 55%, rgba(6,7,6,.92) 100%); }}
.escurece.forte {{ background: linear-gradient(180deg, rgba(6,7,6,.75) 0%, rgba(6,7,6,.55) 45%, rgba(6,7,6,.94) 100%); }}
.grao {{ position: absolute; inset: 0; background: {GRAO}; pointer-events: none; }}
.curva {{ position: absolute; inset: 0; pointer-events: none; }}
.topo {{ position: absolute; left: 70px; right: 70px; top: 62px; display: flex; justify-content: space-between; align-items: center; }}
.topo img {{ height: 46px; }}
.topo .num {{ font-size: 24px; font-weight: 600; letter-spacing: .12em; color: rgba(248,248,248,.8); }}
.bloco {{ position: absolute; left: 70px; right: 70px; bottom: 150px; }}
.rotulo {{ font-size: 24px; font-weight: 600; letter-spacing: .3em; color: rgba(248,248,248,.8); margin-bottom: 26px; }}
.rotulo::before {{ content: '// '; color: {LIMA}; }}
.tit {{ font-family: 'Oswald', sans-serif; font-weight: 700; text-transform: uppercase; line-height: .98; letter-spacing: -.005em; }}
.capa .tit {{ font-size: 150px; }}
.texto .tit, .cta .tit {{ font-size: 104px; }}
.tit .ln {{ display: block; }}
.tit .serif {{ font-family: 'Playfair Display', serif; font-style: italic; font-weight: 700; text-transform: none; color: {LIMA}; letter-spacing: -.01em; }}
.tit .lima {{ color: {LIMA}; }}
.traco {{ width: 96px; height: 6px; background: {LIMA}; margin: 34px 0 30px; }}
.txt {{ font-size: 36px; line-height: 1.36; max-width: 820px; color: rgba(248,248,248,.92); }}
.txt b {{ color: {LIMA}; font-weight: 800; }}
.vidro {{ padding: 46px 48px; border-radius: 26px; background: rgba(28,31,26,.5); border: 2px solid rgba(255,255,255,.14);
  backdrop-filter: blur(22px); -webkit-backdrop-filter: blur(22px); }}
.botao {{ display: inline-flex; align-items: center; gap: 28px; margin-top: 44px; padding: 26px 30px 26px 44px; border-radius: 80px;
  background: {LIMA}; color: {PRETO}; font-family: 'Oswald', sans-serif; font-weight: 700; font-style: italic; font-size: 46px;
  text-transform: uppercase; line-height: 1; }}
.botao i {{ width: 64px; height: 64px; border-radius: 50%; background: {PRETO}; color: {LIMA}; font-style: normal;
  display: flex; align-items: center; justify-content: center; font-size: 36px; }}
.rodape {{ position: absolute; left: 70px; right: 70px; bottom: 58px; display: flex; gap: 0; border-top: 1px solid rgba(248,248,248,.25); padding-top: 18px; }}
.rodape span {{ flex: 1; font-size: 20px; font-weight: 600; letter-spacing: .22em; color: rgba(248,248,248,.7); }}
.rodape span + span {{ border-left: 1px solid rgba(248,248,248,.25); padding-left: 18px; }}
"""

CURVAS = [
    "M1120 150 C 960 260, 930 420, 1010 600",
    "M-40 1040 C 170 930, 280 990, 340 1150",
    "M1120 760 C 940 840, 910 990, 990 1170",
]

def slide_html(i, s):
    tipo = s.get("tipo", "texto")
    foto = ""
    if s.get("foto"):
        uri = (BASE / s["foto"]).resolve().as_uri()
        foto = f'<img class="foto" src="{uri}" style="object-position:{s.get("foco", "50% 50%")}">'
        foto += f'<div class="escurece{" forte" if tipo != "capa" else ""}"></div>'
    curva = CURVAS[i % len(CURVAS)]
    svg = (f'<svg class="curva" viewBox="0 0 1080 1350"><path d="{curva}" stroke="{LIMA}" stroke-width="14" '
           f'fill="none" stroke-linecap="round"/></svg>')
    rot = f'<div class="rotulo">{html.escape(s["rotulo"])}</div>' if s.get("rotulo") else ""
    txt = f'<div class="txt">{texto_html(s["texto"])}</div>' if s.get("texto") else ""
    corpo = f'{rot}<div class="tit">{titulo_html(s.get("titulo", ""))}</div><div class="traco"></div>{txt}'
    if s.get("botao"):
        corpo += f'<div class="botao">{html.escape(s["botao"])}<i>›</i></div>'
    if s.get("vidro"):
        corpo = f'<div class="vidro">{corpo}</div>'
    rod = ""
    if s.get("rodape"):
        rod = '<div class="rodape">' + "".join(f"<span>{html.escape(r)}</span>" for r in s["rodape"]) + "</div>"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="s {tipo}">{foto}<div class="grao"></div>{svg}
<div class="topo"><img src="{LOGO}" alt="DoctorFit"><span class="num">{i+1:02d}/{N:02d}</span></div>
<div class="bloco">{corpo}</div>{rod}</div></body></html>"""

paginas = []
for i, s in enumerate(slides):
    f = SAIDA / f"slide_{i+1:02d}.html"
    f.write_text(slide_html(i, s), encoding="utf-8")
    paginas.append(str(f))

js = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const f of JSON.parse(process.env.PAGINAS)) {
    await p.goto('file://' + f, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: f.replace(/\\.html$/, '.png') });
  }
  await b.close();
})();
"""
import os
subprocess.run(["node", "-e", js], check=True, env={**os.environ, "PAGINAS": json.dumps(paginas)})
for f in paginas:
    Path(f).unlink()
print(f"ok: {len(paginas)} imagens em {SAIDA}")
