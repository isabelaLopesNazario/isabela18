"""Versão 4 da edição PHcont: tela dividida (animação em cima, apresentadora embaixo),
gráfico em tela cheia, movimentos suaves. Uso: python3 gerar_v4.py <pasta do projeto>"""
import html, random, re, sys
from pathlib import Path

P = Path(sys.argv[1])
C = P / "compositions"
C.mkdir(exist_ok=True)
for f in C.glob("*.html"):
    f.unlink()

GOLD = "#c9ad6e"
BORDO = "#7a2a33"
BORDO_L = "#a33a46"
NAVY_T = "#0b1426"
BRANCO = "#f7f5f6"
SUAVE = "power2.out"

LOGO_DUR = 1.84               # tela da logo do vídeo bruto
TOTAL = 23.24 + LOGO_DUR
FALA_FIM = 23.24
CHART = (4.38, 9.20)          # gráfico em tela cheia
SPLIT_TOP = 860               # onde começa a metade de baixo (vídeo)

BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; }}
    .tit {{ position: absolute; left: 160px; width: 760px; text-align: center; font-family: "Oswald", sans-serif; font-weight: 700;
      color: {BRANCO}; line-height: 1.04; text-transform: uppercase; text-shadow: 0 6px 30px rgba(0,0,0,.45); }}
    .tag {{ position: absolute; left: 0; width: 1080px; text-align: center; }}
    .tag span {{ display: inline-block; padding: 8px 22px; border-radius: 8px; background: {BORDO}; font-family: "Poppins", sans-serif;
      font-weight: 700; font-size: 28px; letter-spacing: .16em; color: {BRANCO}; }}
    .ouro {{ color: {GOLD}; }}
    .card {{ position: absolute; border-radius: 22px; background: rgba(8,14,30,.82); border: 3px solid rgba(255,255,255,.14);
      font-family: "Poppins", sans-serif; color: {BRANCO}; }}
    .card.on {{ border-color: {GOLD}; box-shadow: 0 0 28px rgba(201,173,110,.4), inset 0 0 18px rgba(201,173,110,.1); }}
"""

SOBE = 100                    # quanto as telas animadas sobem
SEM_SUBIR = {"fundo", "legendas", "progresso"}

def comp(cid, dur, css, body, js, saida=True):
    if saida:  # saída suave de toda a cena
        js += f'\n    tl.to("#{cid}-w", {{ opacity: 0, duration: 0.32, ease: "sine.inOut" }}, {dur - 0.34:.2f});'
    (C / f"{cid}.html").write_text(f"""<template>
  <style>{BASE_CSS}{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div id="{cid}-w"{"" if cid in SEM_SUBIR else f' style="transform: translateY(-{SOBE}px)"'}>
{body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
""")

def entra(sel, t, d=0.5, y=14):
    """Entrada suave: sobe um pouco e aparece, sem mola."""
    return f'    tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {d}, ease: "{SUAVE}" }}, {t:.2f});'

def foco(sel, t, d=0.4):
    """Título: aparece desfocado e entra em foco."""
    return f'    tl.fromTo("{sel}", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: {d}, ease: "{SUAVE}" }}, {t:.2f});'

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
      background: radial-gradient(ellipse 90% 60% at 50% 30%, #1b2d55 0%, #0f1c3a 42%, #070d1c 100%); }}
    #bg-grade {{ position: absolute; left: -540px; top: 1180px; width: 2160px; height: 900px; transform-origin: 50% 0%;
      transform: perspective(700px) rotateX(62deg);
      background-image: linear-gradient(rgba(140,170,230,.22) 2px, transparent 2px), linear-gradient(90deg, rgba(140,170,230,.22) 2px, transparent 2px);
      background-size: 120px 120px; -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000 40%); mask-image: linear-gradient(180deg, transparent 0%, #000 40%); }}
    .st {{ position: absolute; border-radius: 50%; background: #e8dcc0; display: block; }}
    .vidro {{ position: absolute; border-radius: 18px; background: rgba(210,220,240,.07); border: 2px solid rgba(255,255,255,.08); filter: blur(1.5px); padding: 18px; }}
    .vidro b {{ display: block; height: 10px; border-radius: 5px; background: rgba(255,255,255,.08); margin: 12px 0; }}
    .vidro b:first-child {{ width: 40%; background: rgba(201,173,110,.18); }}
    #bg-pill {{ position: absolute; left: 0; top: 196px; width: 1080px; text-align: center; }}
    #bg-pill span {{ display: inline-block; padding: 10px 28px; border-radius: 40px; background: rgba(6,11,24,.85); border: 2px solid rgba(255,255,255,.1);
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 28px; letter-spacing: .2em; color: {BRANCO}; }}
    #bg-pill i {{ display: inline-block; width: 13px; height: 13px; border-radius: 50%; background: {BORDO_L}; margin-right: 14px; vertical-align: 3px;
      box-shadow: 0 0 12px {BORDO_L}; }}
""", f"""    <div id="bg-clip" class="clip" data-start="0" data-duration="{TOTAL}" data-layout-ignore>
      <div id="bg">
        <div id="bg-grade"></div>
{estrelas}
{vid_html}
        <div id="bg-pill"><span><i></i>PHCONT</span></div>
      </div>
    </div>""", vid_js, saida=False)

# ================================================================ cenas (metade de cima: y 360–840)
# abertura 0–2.07
comp("abertura", 2.07, """
    #a-tag { top: 390px; }
    #a-l1 { top: 460px; font-size: 118px; }
    #a-l2 { top: 586px; font-size: 118px; }
""", """      <div id="a-c" class="clip" data-start="0" data-duration="2.07">
        <div id="a-tag" class="tag"><span>PLANEJAMENTO TRIBUTÁRIO</span></div>
        <div id="a-l1" class="tit">Imposto alto</div>
        <div id="a-l2" class="tit">não é <span class="ouro">destino</span></div>
      </div>""", "\n".join([foco("#a-l2", 0.96, 0.45)]))

# planejamento 2.07–4.38 (local: "planejamento" 3.35→1.28)
comp("planejamento", 2.31, """
    #p-tag { top: 400px; }
    #p-l1 { top: 470px; font-size: 104px; }
    #p-l2 { top: 586px; font-size: 118px; }
""", """      <div id="p-c1" class="clip" data-start="0" data-duration="2.31">
        <div id="p-tag" class="tag"><span>MUITAS VEZES</span></div>
        <div id="p-l1" class="tit">É falta de</div>
      </div>
      <div id="p-c2" class="clip" data-start="1.24" data-duration="1.07"><div id="p-l2" class="tit ouro">planejamento</div></div>""",
     "\n".join([entra("#p-tag", 0.05), foco("#p-l1", 0.6), foco("#p-l2", 1.24, 0.45)]))

# caixa 4.38–9.20  (TELA CHEIA) local: "empresa" 5.71→1.33 ; fatura 7.08→2.70 ; "bem" 7.44→3.06 ; sobra 8.13→3.75 ; caixa 8.80→4.42
comp("caixa", 4.82, f"""
    #cx-t {{ top: 440px; font-size: 96px; }}
    #cx-card {{ left: 150px; width: 780px; top: 600px; height: 500px; }}
    #cx-base {{ position: absolute; left: 60px; right: 60px; bottom: 80px; height: 3px; background: rgba(255,255,255,.25); }}
    .cx-bar {{ position: absolute; bottom: 83px; width: 220px; border-radius: 12px 12px 0 0; transform-origin: 50% 100%; }}
    #cx-b1 {{ left: 120px; height: 290px; background: {GOLD}; box-shadow: 0 0 26px rgba(201,173,110,.45); }}
    #cx-b2 {{ left: 440px; height: 50px; background: {BORDO_L}; }}
    .cx-lab {{ position: absolute; bottom: 26px; width: 280px; margin-left: -30px; text-align: center; font-weight: 700; font-size: 28px; letter-spacing: .1em; color: rgba(247,245,246,.85); }}
    #cx-l1 {{ left: 120px; }}  #cx-l2 {{ left: 440px; }}
    .cx-val {{ position: absolute; width: 300px; margin-left: -40px; text-align: center; font-weight: 800; font-size: 36px; }}
    #cx-v1 {{ left: 120px; bottom: 390px; color: {GOLD}; }}
    #cx-v2 {{ left: 440px; bottom: 150px; color: {BORDO_L}; }}
""", f"""      <div id="cx-ct" class="clip" data-start="0.3" data-duration="4.52"><div id="cx-t" class="tit">Uma empresa <span class="ouro">boa</span></div></div>
      <div id="cx-cc" class="clip" data-start="0.45" data-duration="4.37">
        <div id="cx-card" class="card">
          <div id="cx-base"></div>
          <div id="cx-b1" class="cx-bar"></div><div id="cx-v1" class="cx-val">FATURA BEM</div>
          <div id="cx-b2" class="cx-bar"></div><div id="cx-v2" class="cx-val">SOBRA POUCO</div>
          <div id="cx-l1" class="cx-lab">FATURAMENTO</div><div id="cx-l2" class="cx-lab">CAIXA</div>
        </div>
      </div>""", "\n".join([
    foco("#cx-t", 0.3, 0.5),
    entra("#cx-card", 0.45, 0.6, 30),
    # barras sobem devagar, de forma contínua
    '    tl.fromTo("#cx-b1", { scaleY: 0 }, { scaleY: 1, duration: 2.3, ease: "sine.inOut" }, 1.1);',
    foco("#cx-v1", 2.9, 0.45),
    '    tl.fromTo("#cx-b2", { scaleY: 0 }, { scaleY: 1, duration: 1.0, ease: "sine.inOut" }, 3.6);',
    foco("#cx-v2", 4.0, 0.4),
    f'    tl.to("#cx-card", {{ borderColor: "{BORDO_L}", boxShadow: "0 0 30px rgba(163,58,70,.45)", duration: 0.5, ease: "sine.inOut" }}, 4.1);',
]))

# problema 9.20–13.55 local: sobre 10.58→1.38 ; vendas 11.12→1.92 ; "é sobre" 11.66→2.46 ; tributada 12.97→3.77
comp("problema", 4.35, f"""
    #pb-t {{ top: 400px; font-size: 80px; }}
    .pb-card {{ top: 600px; width: 330px; height: 220px; padding: 34px 26px; text-align: center; }}
    .pb-card h3 {{ font-size: 40px; font-weight: 800; line-height: 1.1; }}
    .pb-card p {{ font-size: 30px; font-weight: 600; opacity: .9; margin-top: 14px; }}
    #pb-c1 {{ left: 150px; border-color: {BORDO_L}; }}
    #pb-c1 h3 {{ color: #d0606c; }}
    #pb-c2 {{ left: 600px; }}
    #pb-c2 h3 {{ color: {GOLD}; }}
    #pb-vs {{ position: absolute; left: 480px; top: 650px; width: 120px; height: 120px; border-radius: 50%; background: {GOLD};
      color: {NAVY_T}; font-family: "Poppins", sans-serif; font-weight: 800; font-style: italic; font-size: 50px; line-height: 120px; text-align: center;
      box-shadow: 0 0 26px rgba(201,173,110,.5); }}
    #pb-risco {{ position: absolute; left: 60px; top: 58px; width: 210px; height: 6px; background: #d0606c; transform-origin: 0 50%; }}
""", f"""      <div id="pb-ct" class="clip" data-start="0" data-duration="4.35"><div id="pb-t" class="tit">Onde está o <span class="ouro">problema?</span></div></div>
      <div id="pb-cc1" class="clip" data-start="1.38" data-duration="2.97">
        <div id="pb-c1" class="card pb-card"><h3>VENDAS</h3><p>Muitas vezes, não é aqui</p><div id="pb-risco" data-layout-allow-occlusion></div></div>
      </div>
      <div id="pb-cc2" class="clip" data-start="2.46" data-duration="1.89">
        <div id="pb-vs">VS</div>
        <div id="pb-c2" class="card pb-card on"><h3>TRIBUTAÇÃO</h3><p>É aqui que pesa</p></div>
      </div>""", "\n".join([
    foco("#pb-t", 0.1, 0.5),
    entra("#pb-c1", 1.38),
    '    tl.fromTo("#pb-risco", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "sine.inOut" }, 2.05);',
    '    tl.fromTo("#pb-vs", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "power2.out" }, 2.46);',
    entra("#pb-c2", 2.7),
    '    tl.to("#pb-c1", { opacity: 0.45, duration: 0.5, ease: "sine.inOut" }, 3.77);',
]))

# fechamento 13.55–16.60 local: fechar 14.12→0.57 ; pagando 14.69→1.14 ; exatamente 15.16→1.61
comp("fechamento", 3.05, f"""
    #fc-t {{ top: 390px; font-size: 76px; }}
    .fc-nome {{ position: absolute; left: 180px; font-family: "Poppins", sans-serif; font-weight: 600; font-size: 32px; color: rgba(247,245,246,.85); }}
    #fc-n1 {{ top: 522px; }}  #fc-n2 {{ top: 630px; }}
    .fc-barra {{ position: absolute; left: 180px; width: 720px; height: 40px; border-radius: 8px; transform-origin: 0 50%; }}
    #fc-b1 {{ top: 568px; background: rgba(247,245,246,.9); }}
    #fc-b2 {{ top: 676px; background: {GOLD}; box-shadow: 0 0 20px rgba(201,173,110,.4); }}
    #fc-tag {{ position: absolute; left: 0; width: 1080px; top: 748px; text-align: center; font-family: "Poppins", sans-serif; font-weight: 800;
      font-size: 34px; letter-spacing: .1em; color: {GOLD}; }}
""", """      <div id="fc-ct" class="clip" data-start="0" data-duration="3.05"><div id="fc-t" class="tit">Pagando o <span class="ouro">certo</span></div></div>
      <div id="fc-cl" class="clip" data-start="0.5" data-duration="2.55">
        <div id="fc-n1" class="fc-nome">Imposto devido</div><div id="fc-b1" class="fc-barra"></div>
        <div id="fc-n2" class="fc-nome">Imposto pago</div><div id="fc-b2" class="fc-barra"></div>
      </div>
      <div id="fc-cg" class="clip" data-start="1.61" data-duration="1.44"><div id="fc-tag">= EXATAMENTE O DEVIDO</div></div>""", "\n".join([
    foco("#fc-t", 0.1, 0.5),
    entra("#fc-n1", 0.5, 0.4, 12),
    '    tl.fromTo("#fc-b1", { scaleX: 0 }, { scaleX: 1, duration: 1.1, ease: "sine.inOut" }, 0.6);',
    entra("#fc-n2", 1.0, 0.4, 12),
    '    tl.fromTo("#fc-b2", { scaleX: 0 }, { scaleX: 1, duration: 1.1, ease: "sine.inOut" }, 1.14);',
    foco("#fc-tag", 1.75, 0.45),
]))

# lista 16.60–20.24 local: 0 ; diferença 18.53→1.93 ; negócio 19.52→2.92
itens = [("1", "Nem R$ 1 a mais de imposto", 0.05), ("2", "A diferença fica com você", 1.93), ("3", "Reinvestida no seu negócio", 2.75)]
li_css = f"""
    #ls-t {{ top: 380px; font-size: 72px; }}
    .li {{ left: 180px; width: 720px; height: 100px; padding: 0 30px; display: flex; align-items: center; gap: 26px; font-size: 34px; font-weight: 700;
      transition: none; }}
    .li .n {{ flex: none; width: 60px; height: 60px; border-radius: 12px; background: rgba(255,255,255,.12); color: {BRANCO};
      font-size: 34px; font-weight: 800; text-align: center; line-height: 60px; }}
    .li.on .n {{ background: {GOLD}; color: {NAVY_T}; }}
"""
body = ['      <div id="ls-ct" class="clip" data-start="0" data-duration="3.64"><div id="ls-t" class="tit">Fechando o mês <span class="ouro">certo</span></div></div>']
js = [foco("#ls-t", 0.0, 0.4)]
for i, (n, txt, t) in enumerate(itens):
    top = 490 + i * 116
    body.append(f'      <div id="ls-c{n}" class="clip" data-start="{t:.2f}" data-duration="{3.64-t:.2f}"><div id="ls-i{n}" class="card li on" style="top:{top}px"><span class="n">{n}</span><span>{html.escape(txt)}</span></div></div>')
    js.append(entra(f"#ls-i{n}", t + 0.02, 0.45, 16))
    if i > 0:
        prev = itens[i-1][0]
        js.append(f'    tl.to("#ls-i{prev}", {{ borderColor: "rgba(255,255,255,.14)", boxShadow: "0 0 0 rgba(0,0,0,0)", duration: 0.4, ease: "sine.inOut" }}, {t:.2f});')
        js.append(f'    tl.to("#ls-i{prev} .n", {{ backgroundColor: "rgba(255,255,255,.12)", color: "{BRANCO}", duration: 0.4, ease: "sine.inOut" }}, {t:.2f});')
comp("lista", 3.64, li_css, "\n".join(body), "\n".join(js))

# cta 20.24–23.24 local: PHcont 21.85→1.61 ; link 22.57→2.33
comp("cta", 3.0, f"""
    #ct-t {{ top: 390px; font-size: 88px; }}
    #ct-s {{ position: absolute; left: 0; top: 590px; width: 1080px; text-align: center; font-family: "Poppins", sans-serif; font-weight: 600;
      font-size: 30px; color: rgba(247,245,246,.85); }}
    #ct-bw {{ position: absolute; left: 0; top: 660px; width: 1080px; text-align: center; }}
    #ct-btn {{ display: inline-block; position: relative; padding: 22px 52px; border-radius: 60px; border: 4px solid {GOLD}; background: rgba(8,14,30,.85);
      font-family: "Poppins", sans-serif; font-weight: 800; font-size: 36px; letter-spacing: .06em; color: {GOLD}; }}
    #ct-btn2 {{ position: absolute; inset: -4px; border-radius: 60px; background: {GOLD}; color: {NAVY_T}; padding: 22px 0; text-align: center; }}
    #ct-cur {{ position: absolute; left: 690px; top: 730px; width: 64px; }}
""", """      <div id="ct-c" class="clip" data-start="0" data-duration="3">
        <div id="ct-t" class="tit">Agende uma <span class="ouro">análise</span></div>
        <div id="ct-s">com a PHcont · link aqui embaixo</div>
        <div id="ct-bw"><span id="ct-btn">AGENDAR ANÁLISE<span id="ct-btn2">✓ LINK NA BIO</span></span></div>
        <svg id="ct-cur" viewBox="0 0 24 24"><path d="M4 2 L4 20 L9 15 L12.5 22 L15.5 20.6 L12 13.8 L19 13.8 Z" fill="#fff" stroke="#0b1426" stroke-width="1.4" stroke-linejoin="round"/></svg>
      </div>""", "\n".join([
    foco("#ct-t", 0.1, 0.5),
    foco("#ct-s", 0.9, 0.4),
    entra("#ct-btn", 1.1, 0.45, 16),
    '    tl.set("#ct-btn2", { opacity: 0 }, 0);',
    '    tl.fromTo("#ct-cur", { x: 160, y: 200, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.8, ease: "sine.inOut" }, 1.3);',
    '    tl.to("#ct-cur", { scale: 0.88, duration: 0.1, ease: "sine.inOut" }, 2.22);',
    '    tl.to("#ct-cur", { scale: 1, duration: 0.15, ease: "sine.out" }, 2.32);',
    '    tl.to("#ct-btn2", { opacity: 1, duration: 0.25, ease: "sine.inOut" }, 2.28);',
]))

# vinheta (tela cheia)
comp("vinheta", TOTAL - FALA_FIM, f"""
    #vn-logo {{ position: absolute; left: 360px; top: 560px; width: 360px; }}
    #vn-link {{ position: absolute; left: 0; top: 1140px; width: 1080px; text-align: center; font-family: "Poppins", sans-serif; font-weight: 700;
      font-size: 40px; letter-spacing: .2em; color: {GOLD}; }}
""", f"""      <div id="vn-c" class="clip" data-start="0" data-duration="{TOTAL-FALA_FIM:.2f}">
        <img id="vn-logo" src="assets/logo_branca.png" alt="PHcont" />
        <div id="vn-link">LINK NA BIO</div>
      </div>""", "\n".join([
    '    tl.fromTo("#vn-logo", { opacity: 0, scale: 1.04, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.8, ease: "power2.out" }, 0.1);',
    foco("#vn-link", 0.5, 0.5),
]), saida=False)

# ---------------------------------------------------------------- legendas
G = [("Imposto alto",0.16),("não é",0.96),("*destino,*",1.30),("muitas vezes",2.07),("é falta de",2.86),("*planejamento*",3.35),
("Todo mês",4.38),("a gente vê",4.80),("uma empresa",5.47),("*boa,*",6.31),("que fatura",6.75),("bem,",7.44),("mas que *sobra*",7.79),("pouco no",8.52),("*caixa*",8.80),
("Às vezes isso",9.20),("não é nem",10.02),("sobre",10.58),("*vendas,*",11.12),("é sobre como",11.66),("a empresa",12.26),("está",12.74),("*tributada*",12.97),
("Imagina",13.72),("fechar o mês",14.12),("pagando",14.69),("*exatamente*",15.16),("o que deve,",15.84),("nem um *real*",16.60),("a mais.",17.19),
("E *reinvestir*",17.55),("essa",18.25),("*diferença*",18.53),("no seu *negócio*",19.16),("*Agende*",20.24),("uma *análise*",20.73),("com a",21.54),("*PHcont,*",21.85),
("link aqui *embaixo*",22.57)]
ENDS = {"no seu *negócio*": 20.24, "a mais.": 17.55, "*planejamento*": 4.38, "*caixa*": 9.20, "link aqui *embaixo*": FALA_FIM}
divs, gjs = [], []
for i, (txt, s) in enumerate(G):
    e = ENDS.get(txt, G[i+1][1] if i+1 < len(G) else FALA_FIM)
    parts = re.findall(r'\*[^*]+\*|[^\s*]+', txt)
    inner = " ".join(
        f'<span class="w{" hl" if p.startswith("*") else ""}">{html.escape(p.strip("*").upper())}</span>' for p in parts)
    top = 1500 if (s < CHART[0] or s >= 20.24) else (1100 if s < CHART[1] else 762)
    divs.append(f'    <div id="lg{i}" class="grupo clip" data-start="{s:.2f}" data-duration="{e-s:.2f}" style="top:{top}px"><div id="lg{i}-i" class="gi">{inner}</div></div>')
    gjs.append(f'    tl.fromTo("#lg{i}-i", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power2.out" }}, {s:.2f});')
comp("legendas", FALA_FIM, f"""
    .grupo {{ position: absolute; left: 0; width: 1080px; height: 100px; text-align: center; overflow: visible; }}
    .gi {{ display: inline-block; font-family: "Poppins", sans-serif; font-weight: 800; font-size: 56px; line-height: 1.3; color: {BRANCO};
      white-space: nowrap; letter-spacing: .01em; text-shadow: 0 4px 16px rgba(0,0,0,.7), 0 0 3px rgba(0,0,0,.6); }}
    .w {{ margin: 0 4px; }}
    .hl {{ background: {GOLD}; color: {NAVY_T}; padding: 0 16px; border-radius: 6px; text-shadow: none; }}
""", "\n".join(divs), "\n".join(gjs), saida=False)

# ---------------------------------------------------------------- barra de progresso
comp("progresso", TOTAL, f"""
    #pg {{ position: absolute; left: 0; top: 0; width: 1080px; height: 8px; background: {GOLD}; transform-origin: 0 50%; }}
""", f'      <div id="pg-c" class="clip" data-start="0" data-duration="{TOTAL}" data-layout-ignore><div id="pg"></div></div>',
     f'    tl.fromTo("#pg", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {TOTAL}, ease: "none" }}, 0);', saida=False)

# ---------------------------------------------------------------- index
def host(cid, s, d, z, track, kind="graphics"):
    return (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s:.2f}" '
            f'data-duration="{d:.2f}" data-track-index="{track}" data-track-kind="{kind}" data-width="1080" data-height="1920" style="z-index:{z}"></div>')

CENAS = [("caixa", 4.38, 9.20), ("problema", 9.20, 13.55),
         ("fechamento", 13.55, 16.60), ("lista", 16.60, 20.24)]
hosts = [host("fundo", 0, TOTAL, 1, 0)]
hosts += [host(m, s, e - s, 3, 2) for m, s, e in CENAS]
hosts += [host("legendas", 0, FALA_FIM, 5, 3, "captions"), host("progresso", 0, TOTAL, 6, 4)]
SAI, VOLTA = CHART  # a metade de baixo desce no gráfico e volta depois
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
      #cam {{ position: absolute; left: 0; top: {SPLIT_TOP}px; width: 1080px; height: {1920-SPLIT_TOP}px; overflow: hidden; z-index: 4;
        border-top: 2px solid rgba(201,173,110,.55); box-shadow: 0 -10px 40px rgba(0,0,0,.55), 0 -2px 18px rgba(201,173,110,.25); }}
      #cam-sombra {{ position: absolute; left: 0; top: 0; width: 1080px; height: 220px; z-index: 2;
        background: linear-gradient(180deg, rgba(9,16,34,.92) 0%, rgba(9,16,34,.55) 45%, rgba(9,16,34,0) 100%); }}
      #logo-final {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 8; }}
      #camcheia {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; z-index: 4; }}
      #camcheia video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #cam video {{ position: absolute; left: 0; top: -420px; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <!-- Voz da apresentadora (contínua) -->
      <audio id="voz" class="clip" src="assets/fala.mp4" data-start="0" data-duration="{FALA_FIM}" data-track-index="5" data-volume="1"></audio>
      <!-- Começo: ela em tela cheia -->
      <div id="camcheia">
        <video id="fala0" class="clip" src="assets/fala.mp4" data-start="0" data-duration="{SAI+0.6:.2f}" data-media-start="0" data-track-index="1" muted playsinline></video>
        <video id="fala3" class="clip" src="assets/fala.mp4" data-start="20.00" data-duration="{FALA_FIM-20.0:.2f}" data-media-start="20.00" data-track-index="1" muted playsinline></video>
      </div>
      <!-- Final: tela da logo do vídeo bruto -->
      <video id="logo-final" class="clip" src="assets/logo_final.mp4" data-start="{FALA_FIM}" data-duration="{LOGO_DUR}" data-track-index="6" muted playsinline></video>
      <!-- Metade de baixo: ela falando -->
      <div id="cam">
        <video id="fala2" class="clip" src="assets/fala.mp4" data-start="{VOLTA-0.1:.2f}" data-duration="{20.6-(VOLTA-0.1):.2f}" data-media-start="{VOLTA-0.1:.2f}" data-track-index="1" muted playsinline></video>
        <div id="cam-sombra"></div>
      </div>
{chr(10).join(hosts)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // gráfico em tela cheia: a metade de baixo desce e depois volta, suave
      tl.set("#cam", {{ opacity: 0 }}, 0);
      tl.to("#camcheia", {{ opacity: 0, duration: 0.55, ease: "sine.inOut" }}, {SAI:.2f});
      tl.to("#cam", {{ opacity: 1, duration: 0.5, ease: "sine.inOut" }}, {VOLTA-0.1:.2f});
      // final: ela volta em tela cheia para o convite
      tl.to("#camcheia", {{ opacity: 1, duration: 0.45, ease: "sine.inOut" }}, 20.06);
      tl.set("#cam", {{ opacity: 0 }}, 20.53);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print("ok")
