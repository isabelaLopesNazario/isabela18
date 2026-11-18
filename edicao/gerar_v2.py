"""Gera a versão 2 da edição PHcont (estilo explicador: fundo marinho, títulos centrais, cartões)."""
import html, random, re, sys
from pathlib import Path

P = Path(sys.argv[1])
C = P / "compositions"
C.mkdir(exist_ok=True)

GOLD = "#c9ad6e"      # dourado da marca, levemente mais claro para brilho em fundo escuro
GOLD_D = "#bba372"
BORDO = "#7a2a33"
BORDO_L = "#a33a46"
NAVY_T = "#0b1426"
BRANCO = "#f7f5f6"

TOTAL = 25.64
FALA_FIM = 23.24
# (id, início, fim)
MOTION = [("abertura", 0.0, 2.07), ("caixa", 4.38, 9.20), ("problema", 10.58, 13.55),
          ("lista", 16.60, 20.24), ("cta", 20.24, 23.24), ("vinheta", 23.24, TOTAL)]
FACE = [("f1", 2.07, 4.38), ("f2", 9.20, 10.58), ("f3", 13.55, 16.60)]

BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; }}
    .tit {{ position: absolute; left: 192px; width: 696px; text-align: center; font-family: "Oswald", sans-serif; font-weight: 700;
      color: {BRANCO}; line-height: 1.02; text-transform: uppercase; text-shadow: 0 6px 30px rgba(0,0,0,.45); }}
    .ouro {{ color: {GOLD}; }}
    .card {{ position: absolute; left: 180px; width: 720px; border-radius: 22px; background: rgba(8,14,30,.82);
      border: 3px solid rgba(255,255,255,.14); font-family: "Poppins", sans-serif; color: {BRANCO}; }}
    .card.on {{ border-color: {GOLD}; box-shadow: 0 0 28px rgba(201,173,110,.45), inset 0 0 18px rgba(201,173,110,.12); }}
"""

def comp(cid, dur, css, body, js):
    (C / f"{cid}.html").write_text(f"""<template>
  <style>{BASE_CSS}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
""")

def blur_in(sel, t, d=0.18, px=10):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, filter: "blur({px}px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: {d}, ease: "power4.out" }}, {t:.2f});'

def pop(sel, t, d=0.35):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, scale: 0.92, y: 18 }}, {{ opacity: 1, scale: 1, y: 0, duration: {d}, ease: "back.out(1.4)" }}, {t:.2f});'

# ---------------------------------------------------------------- fundo
random.seed(7)
estrelas = "\n".join(
    f'        <i class="st" style="left:{random.randint(20,1060)}px;top:{random.randint(160,1500)}px;opacity:{random.uniform(.25,.8):.2f};width:{random.choice([3,3,4,5])}px;height:{random.choice([3,3,4,5])}px"></i>'
    for _ in range(46))
vidros = [(-60, 360, 330, 230), (760, 230, 300, 210), (40, 1380, 360, 250), (700, 1250, 340, 240), (860, 880, 260, 180)]
vid_html = "\n".join(f'        <div id="bg-v{i}" class="vidro" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><b></b><b></b><b></b></div>'
                     for i, (x, y, w, h) in enumerate(vidros))
vid_js = "\n".join(
    f'    tl.fromTo("#bg-v{i}", {{ x: 0, y: 0 }}, {{ x: {random.choice([-1,1])*random.randint(30,60)}, y: {random.choice([-1,1])*random.randint(40,90)}, duration: {TOTAL}, ease: "none" }}, 0);'
    for i in range(len(vidros)))
comp("fundo", TOTAL, f"""
    #bg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden;
      background: radial-gradient(ellipse 90% 60% at 50% 36%, #1b2d55 0%, #0f1c3a 42%, #070d1c 100%); }}
    #bg-grade {{ position: absolute; left: -540px; top: 1180px; width: 2160px; height: 900px; transform-origin: 50% 0%;
      transform: perspective(700px) rotateX(62deg);
      background-image: linear-gradient(rgba(140,170,230,.22) 2px, transparent 2px), linear-gradient(90deg, rgba(140,170,230,.22) 2px, transparent 2px);
      background-size: 120px 120px; -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 40%); mask-image: linear-gradient(180deg, transparent 0%, #000 40%); }}
    .st {{ position: absolute; border-radius: 50%; background: #e8dcc0; display: block; }}
    .vidro {{ position: absolute; border-radius: 18px; background: rgba(210,220,240,.07); border: 2px solid rgba(255,255,255,.08); filter: blur(1.5px); padding: 18px; }}
    .vidro b {{ display: block; height: 10px; border-radius: 5px; background: rgba(255,255,255,.08); margin: 12px 0; }}
    .vidro b:first-child {{ width: 40%; background: rgba(201,173,110,.18); }}
    #bg-pill {{ position: absolute; left: 0; top: 300px; width: 1080px; text-align: center; }}
    #bg-pill span {{ display: inline-block; padding: 12px 30px; border-radius: 40px; background: rgba(6,11,24,.85); border: 2px solid rgba(255,255,255,.1);
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 30px; letter-spacing: .2em; color: {BRANCO}; }}
    #bg-pill i {{ display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: {BORDO_L}; margin-right: 14px; vertical-align: 3px;
      box-shadow: 0 0 12px {BORDO_L}; }}
""", f"""    <div id="bg-clip" class="clip" data-start="0" data-duration="{TOTAL}" data-layout-ignore>
      <div id="bg">
        <div id="bg-grade"></div>
{estrelas}
{vid_html}
        <div id="bg-pill"><span><i></i>PHCONT</span></div>
      </div>
    </div>""", vid_js)

# ---------------------------------------------------------------- abertura (0–2.07)
comp("abertura", 2.07, f"""
    #a-tag {{ position: absolute; left: 0; top: 520px; width: 1080px; text-align: center; }}
    #a-tag span {{ display: inline-block; padding: 8px 22px; border-radius: 8px; background: {BORDO}; font-family: "Poppins", sans-serif;
      font-weight: 700; font-size: 30px; letter-spacing: .16em; color: {BRANCO}; }}
    #a-l1 {{ top: 590px; font-size: 112px; }}
    #a-l2 {{ top: 712px; font-size: 112px; }}
""", """    <div id="a-c" class="clip" data-start="0" data-duration="2.07">
      <div id="a-tag"><span>PLANEJAMENTO TRIBUTÁRIO</span></div>
      <div id="a-l1" class="tit">Imposto alto</div>
      <div id="a-l2" class="tit">não é <span class="ouro">destino</span></div>
    </div>""", "\n".join([
    blur_in("#a-l2", 0.96, 0.2, 12),
    '    tl.fromTo("#a-l1", { scale: 1.04 }, { scale: 1, duration: 0.5, ease: "expo.out" }, 0);',
]))

# ---------------------------------------------------------------- caixa (4.38–9.20) local
# fatura 7.08→2.70 ; sobra 8.13→3.75 ; caixa 8.80→4.42
comp("caixa", 4.82, f"""
    #cx-t {{ top: 500px; font-size: 84px; }}
    #cx-card {{ top: 640px; height: 420px; }}
    #cx-base {{ position: absolute; left: 60px; right: 60px; bottom: 74px; height: 3px; background: rgba(255,255,255,.25); }}
    .cx-bar {{ position: absolute; bottom: 77px; width: 200px; border-radius: 10px 10px 0 0; transform-origin: 50% 100%; }}
    #cx-b1 {{ left: 110px; height: 210px; background: {GOLD}; box-shadow: 0 0 26px rgba(201,173,110,.5); }}
    #cx-b2 {{ left: 410px; height: 44px; background: {BORDO_L}; }}
    .cx-lab {{ position: absolute; bottom: 22px; width: 200px; text-align: center; font-weight: 700; font-size: 28px; letter-spacing: .1em; color: rgba(247,245,246,.85); }}
    #cx-l1 {{ left: 110px; }}  #cx-l2 {{ left: 410px; }}
    .cx-val {{ position: absolute; width: 280px; margin-left: -40px; text-align: center; font-weight: 800; font-size: 34px; }}
    #cx-v1 {{ left: 110px; bottom: 300px; color: {GOLD}; }}
    #cx-v2 {{ left: 410px; bottom: 136px; color: {BORDO_L}; }}
""", f"""    <div id="cx-ct" class="clip" data-start="0.05" data-duration="4.77"><div id="cx-t" class="tit">Uma empresa <span class="ouro">boa</span></div></div>
    <div id="cx-cc" class="clip" data-start="0.35" data-duration="4.47">
      <div id="cx-card" class="card">
        <div id="cx-base"></div>
        <div id="cx-b1" class="cx-bar"></div><div id="cx-v1" class="cx-val">FATURA BEM</div>
        <div id="cx-b2" class="cx-bar"></div><div id="cx-v2" class="cx-val">SOBRA POUCO</div>
        <div id="cx-l1" class="cx-lab">FATURAMENTO</div><div id="cx-l2" class="cx-lab">CAIXA</div>
      </div>
    </div>""", "\n".join([
    blur_in("#cx-t", 0.05),
    pop("#cx-card", 0.35),
    '    tl.fromTo(["#cx-b1", "#cx-b2"], { scaleY: 0 }, { scaleY: 0.06, duration: 0.3, ease: "power2.out" }, 0.6);',
    '    tl.to("#cx-b1", { scaleY: 1, duration: 0.7, ease: "expo.out" }, 2.70);',
    blur_in("#cx-v1", 2.85, 0.2, 8),
    '    tl.to("#cx-b2", { scaleY: 1, duration: 0.5, ease: "expo.out" }, 3.75);',
    blur_in("#cx-v2", 3.85, 0.2, 8),
    '    tl.to("#cx-card", { borderColor: "#a33a46", boxShadow: "0 0 30px rgba(163,58,70,.5)", duration: 0.25, ease: "power2.out" }, 4.42);',
]))

# ---------------------------------------------------------------- problema (10.58–13.55) local
# vendas 11.12→0.54 ; "é sobre" 11.66→1.08 ; tributada 12.97→2.39
comp("problema", 2.97, f"""
    #pb-t {{ top: 420px; font-size: 84px; }}
    .pb-card {{ height: 170px; padding: 30px 40px; }}
    .pb-card h3 {{ font-size: 46px; font-weight: 800; letter-spacing: .02em; line-height: 1.1; }}
    .pb-card p {{ font-size: 32px; font-weight: 600; opacity: .9; margin-top: 6px; }}
    #pb-c1 {{ top: 630px; border-color: {BORDO_L}; box-shadow: 0 0 22px rgba(163,58,70,.35); }}
    #pb-c1 h3 {{ color: #d0606c; }}
    #pb-c2 {{ top: 890px; }}
    #pb-c2 h3 {{ color: {GOLD}; }}
    #pb-vs {{ position: absolute; left: 470px; top: 772px; width: 140px; height: 140px; border-radius: 50%; background: {GOLD};
      color: {NAVY_T}; font-family: "Poppins", sans-serif; font-weight: 800; font-style: italic; font-size: 58px; line-height: 140px; text-align: center;
      box-shadow: 0 0 30px rgba(201,173,110,.55); }}
    #pb-risco {{ position: absolute; left: 34px; top: 52px; width: 230px; height: 7px; background: #d0606c; transform-origin: 0 50%; }}
""", f"""    <div id="pb-ct" class="clip" data-start="0" data-duration="2.97"><div id="pb-t" class="tit">Onde está o <span class="ouro">problema?</span></div></div>
    <div id="pb-cc1" class="clip" data-start="0.5" data-duration="2.47">
      <div id="pb-c1" class="card pb-card"><h3>VENDAS</h3><p>Muitas vezes, não é aqui</p><div id="pb-risco" data-layout-allow-occlusion></div></div>
    </div>
    <div id="pb-cc2" class="clip" data-start="1.08" data-duration="1.89">
      <div id="pb-c2" class="card pb-card on"><h3>TRIBUTAÇÃO</h3><p>Como a empresa está enquadrada</p></div>
      <div id="pb-vs">VS</div>
    </div>""", "\n".join([
    blur_in("#pb-t", 0.02),
    pop("#pb-c1", 0.5),
    '    tl.fromTo("#pb-risco", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "expo.out" }, 0.85);',
    '    tl.fromTo("#pb-vs", { scale: 0, rotation: -25 }, { scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }, 1.08);',
    pop("#pb-c2", 1.25),
    '    tl.to("#pb-c1", { opacity: 0.5, duration: 0.25, ease: "power2.out" }, 2.39);',
    '    tl.to("#pb-c2", { scale: 1.04, duration: 0.25, ease: "power2.out" }, 2.39);',
]))

# ---------------------------------------------------------------- lista (16.60–20.24) local
# "nem um real" 0 ; diferença 18.53→1.93 ; negócio 19.52→2.92
itens = [("1", "Nem R$ 1 a mais de imposto", 0.05), ("2", "A diferença fica com você", 1.93), ("3", "Reinvestida no seu negócio", 2.92)]
li_css = f"""
    #ls-t {{ top: 420px; font-size: 84px; }}
    .li {{ height: 124px; padding: 0 34px; display: flex; align-items: center; gap: 28px; font-size: 38px; font-weight: 700; }}
    .li .n {{ flex: none; width: 70px; height: 70px; border-radius: 14px; background: rgba(255,255,255,.12); color: {BRANCO};
      font-size: 40px; font-weight: 800; text-align: center; line-height: 70px; }}
    .li.on .n {{ background: {GOLD}; color: {NAVY_T}; }}
"""
body = ['    <div id="ls-ct" class="clip" data-start="0" data-duration="3.64"><div id="ls-t" class="tit">Fechando o mês <span class="ouro">certo</span></div></div>']
js = [blur_in("#ls-t", 0.0)]
for i, (n, txt, t) in enumerate(itens):
    top = 630 + i * 145
    body.append(f'    <div id="ls-c{n}" class="clip" data-start="{t:.2f}" data-duration="{3.64-t:.2f}"><div id="ls-i{n}" class="card li on" style="top:{top}px"><span class="n">{n}</span><span>{html.escape(txt)}</span></div></div>')
    js.append(pop(f"#ls-i{n}", t + 0.02, 0.3))
    if i > 0:
        prev = itens[i-1][0]
        js.append(f'    tl.to("#ls-i{prev}", {{ borderColor: "rgba(255,255,255,.14)", boxShadow: "0 0 0 rgba(0,0,0,0)", duration: 0.2, ease: "power2.out" }}, {t:.2f});')
        js.append(f'    tl.to("#ls-i{prev} .n", {{ backgroundColor: "rgba(255,255,255,.12)", color: "{BRANCO}", duration: 0.2, ease: "power2.out" }}, {t:.2f});')
comp("lista", 3.64, li_css, "\n".join(body), "\n".join(js))

# ---------------------------------------------------------------- cta (20.24–23.24) local
# PHcont 21.85→1.61 ; link 22.57→2.33
comp("cta", 3.0, f"""
    #ct-av {{ position: absolute; left: 440px; top: 380px; width: 200px; height: 200px; border-radius: 50%; overflow: hidden;
      border: 6px solid {GOLD}; box-shadow: 0 0 30px rgba(201,173,110,.5); }}
    #ct-av img {{ width: 100%; height: 100%; display: block; }}
    #ct-t {{ top: 610px; font-size: 88px; }}
    #ct-s {{ position: absolute; left: 0; top: 812px; width: 1080px; text-align: center; font-family: "Poppins", sans-serif; font-weight: 600;
      font-size: 30px; color: rgba(247,245,246,.85); }}
    #ct-bw {{ position: absolute; left: 0; top: 890px; width: 1080px; text-align: center; }}
    #ct-btn {{ display: inline-block; position: relative; padding: 22px 52px; border-radius: 60px; border: 4px solid {GOLD}; background: rgba(8,14,30,.85);
      font-family: "Poppins", sans-serif; font-weight: 800; font-size: 36px; letter-spacing: .06em; color: {GOLD}; }}
    #ct-btn2 {{ position: absolute; inset: -4px; border-radius: 60px; background: {GOLD}; color: {NAVY_T}; padding: 22px 0; text-align: center; }}
    #ct-cur {{ position: absolute; left: 690px; top: 960px; width: 64px; }}
""", f"""    <div id="ct-c" class="clip" data-start="0" data-duration="3">
      <div id="ct-av"><img src="assets/avatar.png" alt="" /></div>
      <div id="ct-t" class="tit">Agende uma <span class="ouro">análise</span></div>
      <div id="ct-s">com a PHcont · link aqui embaixo</div>
      <div id="ct-bw"><span id="ct-btn">AGENDAR ANÁLISE<span id="ct-btn2">✓ LINK NA BIO</span></span></div>
      <svg id="ct-cur" viewBox="0 0 24 24"><path d="M4 2 L4 20 L9 15 L12.5 22 L15.5 20.6 L12 13.8 L19 13.8 Z" fill="#fff" stroke="#0b1426" stroke-width="1.4" stroke-linejoin="round"/></svg>
    </div>""", "\n".join([
    pop("#ct-av", 0.0, 0.4),
    blur_in("#ct-t", 0.08),
    blur_in("#ct-s", 0.9, 0.2, 6),
    pop("#ct-btn", 1.2, 0.3),
    '    tl.set("#ct-btn2", { opacity: 0 }, 0);',
    '    tl.fromTo("#ct-cur", { x: 160, y: 220, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.55, ease: "power3.out" }, 1.3);',
    '    tl.to("#ct-cur", { scale: 0.85, duration: 0.08, ease: "power2.in" }, 2.27);',
    '    tl.to("#ct-cur", { scale: 1, duration: 0.12, ease: "power2.out" }, 2.35);',
    '    tl.to("#ct-btn", { scale: 0.95, duration: 0.08, ease: "power2.in" }, 2.27);',
    '    tl.to("#ct-btn", { scale: 1, duration: 0.18, ease: "back.out(2)" }, 2.35);',
    '    tl.to("#ct-btn2", { opacity: 1, duration: 0.12, ease: "power2.out" }, 2.33);',
]))

# ---------------------------------------------------------------- vinheta
comp("vinheta", TOTAL - FALA_FIM, f"""
    #vn-logo {{ position: absolute; left: 360px; top: 560px; width: 360px; }}
    #vn-link {{ position: absolute; left: 0; top: 1140px; width: 1080px; text-align: center; font-family: "Poppins", sans-serif; font-weight: 700;
      font-size: 40px; letter-spacing: .2em; color: {GOLD}; }}
""", f"""    <div id="vn-c" class="clip" data-start="0" data-duration="{TOTAL-FALA_FIM:.2f}">
      <img id="vn-logo" src="assets/logo_branca.png" alt="PHcont" />
      <div id="vn-link">LINK NA BIO</div>
    </div>""", "\n".join([
    '    tl.fromTo("#vn-logo", { opacity: 0, scale: 1.08, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 0.0);',
    blur_in("#vn-link", 0.25, 0.3, 6),
]))

# ---------------------------------------------------------------- legendas
G = [("Imposto alto",0.16),("não é",0.96),("*destino,*",1.30),("muitas vezes",2.07),("é falta de",2.86),("*planejamento*",3.35),
("Todo mês",4.38),("a gente vê",4.80),("uma empresa",5.47),("*boa,*",6.31),("que fatura",6.75),("bem,",7.44),("mas que *sobra*",7.79),("pouco no",8.52),("*caixa*",8.80),
("Às vezes isso",9.20),("não é nem",10.02),("sobre",10.58),("*vendas,*",11.12),("é sobre como",11.66),("a empresa",12.26),("está",12.74),("*tributada*",12.97),
("Imagina",13.72),("fechar o mês",14.12),("pagando",14.69),("*exatamente*",15.16),("o que deve,",15.84),("nem um *real*",16.60),("a mais.",17.19),
("E *reinvestir*",17.55),("essa",18.25),("*diferença*",18.53),("no seu *negócio*",19.16),("*Agende*",20.24),("uma *análise*",20.73),("com a",21.54),("*PHcont,*",21.85),
("link aqui *embaixo*",22.57)]
ENDS = {"no seu *negócio*": 20.24, "a mais.": 17.55, "*planejamento*": 4.38, "link aqui *embaixo*": FALA_FIM}
divs, gjs = [], []
for i, (txt, s) in enumerate(G):
    e = ENDS.get(txt, G[i+1][1] if i+1 < len(G) else FALA_FIM)
    parts = re.findall(r'\*[^*]+\*|[^\s*]+', txt)
    inner = " ".join(
        f'<span class="w{" hl" if p.startswith("*") else ""}">{html.escape(p.strip("*").upper())}</span>' for p in parts)
    divs.append(f'    <div id="lg{i}" class="grupo clip" data-start="{s:.2f}" data-duration="{e-s:.2f}"><div id="lg{i}-i" class="gi">{inner}</div></div>')
    gjs.append(f'    tl.fromTo("#lg{i}-i", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.1, ease: "power3.out" }}, {s:.2f});')
comp("legendas", FALA_FIM, f"""
    .grupo {{ position: absolute; left: 0; top: 1130px; width: 1080px; height: 110px; text-align: center; overflow: visible; }}
    .gi {{ display: inline-block; font-family: "Poppins", sans-serif; font-weight: 800; font-size: 58px; line-height: 1.3; color: {BRANCO};
      white-space: nowrap; letter-spacing: .01em; text-shadow: 0 4px 16px rgba(0,0,0,.7), 0 0 3px rgba(0,0,0,.6); }}
    .w {{ margin: 0 4px; }}
    .hl {{ background: {GOLD}; color: {NAVY_T}; padding: 0 16px; border-radius: 6px; text-shadow: none; }}
""", "\n".join(divs), "\n".join(gjs))

# ---------------------------------------------------------------- barra de progresso
comp("progresso", TOTAL, f"""
    #pg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 8px; background: {GOLD}; transform-origin: 0 50%; }}
""", f'    <div id="pg-c" class="clip" data-start="0" data-duration="{TOTAL}" data-layout-ignore><div id="pg"></div></div>',
     f'    tl.fromTo("#pg", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {TOTAL}, ease: "none" }}, 0);')

# ---------------------------------------------------------------- index
def host(cid, s, d, z, track, kind="graphics"):
    return (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s:.2f}" '
            f'data-duration="{d:.2f}" data-track-index="{track}" data-track-kind="{kind}" data-width="1080" data-height="1920" style="z-index:{z}"></div>')

videos = "\n".join(
    f'        <video id="{fid}" class="clip" src="assets/fala.mp4" data-start="{s:.2f}" data-duration="{e-s:.2f}" data-media-start="{s:.2f}" '
    f'data-track-index="1" muted playsinline></video>' for fid, s, e in FACE)
hosts = [host("fundo", 0, TOTAL, 1, 0)]
hosts += [host(m, s, e - s, 3, 2) for m, s, e in MOTION]
hosts += [host("legendas", 0, FALA_FIM, 5, 3, "captions"), host("progresso", 0, TOTAL, 6, 4)]
(P / "index.html").write_text(f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #070d1c; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      #cam {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; z-index: 2; }}
      #cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <!-- Voz da apresentadora (contínua) -->
      <audio id="voz" class="clip" src="assets/fala.mp4" data-start="0" data-duration="{FALA_FIM}" data-track-index="5" data-volume="1"></audio>
      <!-- Trechos em que ela aparece em tela cheia -->
      <div id="cam">
{videos}
      </div>
{chr(10).join(hosts)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#cam", {{ transformOrigin: "540px 720px", scale: 1 }}, 0);
      // f1: punch-in em "planejamento"
      tl.set("#cam", {{ scale: 1.12 }}, 3.35);
      tl.set("#cam", {{ scale: 1 }}, 4.38);
      // f2: entra já levemente aproximado
      tl.set("#cam", {{ scale: 1.06 }}, 9.20);
      tl.set("#cam", {{ scale: 1 }}, 10.58);
      // f3: punch-in em "exatamente"
      tl.set("#cam", {{ scale: 1.1 }}, 15.16);
      tl.set("#cam", {{ scale: 1 }}, 16.60);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print("ok")
