"""Gerador da edição no padrão aprovado (tela dividida, gráfico em tela cheia, transições leves).

Uso:  python3 gerar_edicao.py <pasta do projeto> <marca.json da empresa>
      (ex.: .claude/skills/phcont/marca.json  ou  .claude/skills/doctorfit/marca.json)

O LAYOUT e o JEITO DE EDITAR são os mesmos para todas as empresas; as CORES, o texto da pílula e a logo vêm do
marca.json. O código abaixo é escrito com a paleta de referência (a da PHcont) e, no fim, cada cor é trocada
pela cor equivalente da marca escolhida.

MODELO: os tempos, os textos das cenas e a lista G da legenda são os do vídeo "Planejamento tributário" (PHcont).
Para um vídeo novo, troque esses dados.
"""
import html, json, random, re, sys
from pathlib import Path

P = Path(sys.argv[1])
if len(sys.argv) < 3:
    sys.exit("Informe o marca.json da empresa: python3 gerar_edicao.py <projeto> <marca.json>")
MARCA = json.load(open(sys.argv[2], encoding="utf-8"))
if "_a_preencher" in MARCA:
    sys.exit(f"A identidade de {MARCA.get('nome')} ainda não foi preenchida: {MARCA['_a_preencher']}")
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

LOGO_DUR = 3.73               # tela da logo do vídeo bruto (entrada desacelerada + pausa)
LOGO_INI = 21.90              # a logo começa a aparecer por cima dela
TOTAL = LOGO_INI + LOGO_DUR
FALA_FIM = 22.23
CHART = (5.04, 9.91)          # gráfico em tela cheia
CHEIA2 = 18.29                # volta para ela em tela cheia (exatamente no corte da 4ª gravação)
SPLIT_TOP = 700               # onde começa a metade de baixo (vídeo)

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

SOBE = 0                      # quanto as telas animadas sobem
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
    .vidro {{ display: none; }}
    #bg-pill {{ display: none; }}
    #bg-luz {{ display: none; }}
    .st {{ display: none; }}
    #bg::after {{ content: ""; position: absolute; inset: 0;
      background-image: linear-gradient(rgba(255,255,255,.055) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.055) 2px, transparent 2px);
      background-size: 54px 54px; }}
    #bg-luz b {{ position: absolute; inset: 0; transform: rotate(24deg);
      background: linear-gradient(90deg, rgba(201,173,110,0) 0%, rgba(201,173,110,.10) 45%, rgba(255,240,210,.16) 50%, rgba(201,173,110,.10) 55%, rgba(201,173,110,0) 100%); }}
    #bg-pill {{ position: absolute; left: 0; top: 172px; width: 1080px; text-align: center; }}
    #bg-pill span {{ display: inline-block; padding: 10px 28px; border-radius: 40px; background: rgba(6,11,24,.85); border: 2px solid rgba(255,255,255,.1);
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 28px; letter-spacing: .2em; color: {BRANCO}; }}
    #bg-pill i {{ display: inline-block; width: 13px; height: 13px; border-radius: 50%; background: {BORDO_L}; margin-right: 14px; vertical-align: 3px;
      box-shadow: 0 0 12px {BORDO_L}; }}
""", f"""    <div id="bg-clip" class="clip" data-start="0" data-duration="{TOTAL}" data-layout-ignore>
      <div id="bg">
        <div id="bg-luz"><b></b></div>
{estrelas}
{vid_html}
        <div id="bg-pill"><span><i></i>PHCONT</span></div>
      </div>
    </div>""", vid_js, saida=False)

# ================================================================ cenas do vídeo 2 — ESTILO C: rascunho à mão + mapa + texto atrás dela
# Faixa de cima (0–700): conteúdo entre y 200 e 590; legenda em y ≈ 612. Diagnóstico em tela cheia.

FONTE_MAO = '@font-face { font-family: "Caveat"; src: url("assets/fonts/caveat.woff2") format("woff2"); font-weight: 400 700; }'
EST_C = f"""
    {FONTE_MAO}
    .mao {{ font-family: "Caveat", cursive; font-weight: 700; color: {GOLD}; }}
    .tt {{ position: absolute; left: 140px; width: 800px; text-align: center; font-family: "Oswald", sans-serif; font-weight: 700;
      text-transform: uppercase; color: {BRANCO}; line-height: 1.02; }}
    .tt em {{ font-family: "Caveat", cursive; font-style: normal; text-transform: none; color: {GOLD}; font-size: 1.25em; }}
    .rab {{ position: absolute; overflow: visible; }}
    .rab path, .rab circle, .rab rect, .rab line {{ fill: none; stroke: {BRANCO}; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }}
    .rab .ouro {{ stroke: {GOLD}; }}
    .rab .bordo {{ stroke: #d0606c; stroke-width: 6; }}
"""

def risca(sel, t, d=0.8, stagger=0.06):
    """O traço do rabisco aparece como se estivesse sendo desenhado."""
    return (f'    tl.fromTo("{sel}", {{ strokeDasharray: 1400, strokeDashoffset: 1400 }}, '
            f'{{ strokeDashoffset: 0, duration: {d}, ease: "sine.inOut", stagger: {stagger} }}, {t:.2f});')

def svg(id_, x, y, w, h, corpo):
    return f'<svg id="{id_}" class="rab" style="left:{x}px;top:{y}px" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{corpo}</svg>'

# ---------------------------------------------------------------- texto ATRÁS dela no gancho (0–5.64)
comp("atras", 5.64, f"""
    .gig {{ position: absolute; left: 40px; width: 1000px; text-align: center; font-family: "Oswald", sans-serif; font-weight: 700;
      text-transform: uppercase; line-height: 1; letter-spacing: .005em; color: #14203a; white-space: nowrap;
      text-shadow: 0 0 18px rgba(255,255,255,.35); }}
    .gig em {{ font-style: normal; color: {GOLD}; text-shadow: 0 2px 10px rgba(9,16,34,.35); }}
""", """      <div id="at-1" class="clip" data-start="0.55" data-duration="1.9"><div id="at-1i" class="gig" style="top:385px;font-size:170px">PENDÊNCIA<em>?</em></div></div>
      <div id="at-2" class="clip" data-start="2.45" data-duration="1.8"><div id="at-2i" class="gig" style="top:385px;font-size:170px">TRAVADA<em>?</em></div></div>
      <div id="at-3" class="clip" data-start="4.25" data-duration="1.39"><div id="at-3i" class="gig" style="top:405px;font-size:140px">REGIME <em>ERRADO?</em></div></div>""",
     "\n".join([foco("#at-1i", 0.55, 0.35), foco("#at-2i", 2.45, 0.3), foco("#at-3i", 4.25, 0.3), '    tl.to("#atras-w", { opacity: 0, duration: 0.5, ease: "sine.inOut" }, 5.04);']))

# ---------------------------------------------------------------- MAPA do diagnóstico (TELA CHEIA) 5.04–9.91
# local: diagnóstico 0.99 ; fiscal 1.81 ; cadastral 2.39 ; societário 3.12
D_DUR = 4.87
CX, CY = 540, 960                       # centro do mapa (ela)
nos = [("fiscal", 225, 650, "FISCAL", "impostos e<br>obrigações", 1.81),
       ("cadastral", 855, 650, "CADASTRAL", "CNPJ e<br>certidões", 2.39),
       ("societario", 540, 1330, "SOCIETÁRIO", "contrato e sócios", 3.12)]
def _ramo(i, x, y):
    import math
    dx, dy = x - CX, y - CY; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    x0, y0 = CX + ux * 160, CY - 20 + uy * (160 if uy < 0.9 else 225)          # sai da borda da foto dela
    x1, y1 = x - ux * 120, y - uy * 120              # chega na borda do círculo do tema
    k = 28 if uy < 0.9 else 0
    mx, my = (x0 + x1) / 2 - uy * k, (y0 + y1) / 2 + ux * k
    return f'<path id="mp-l{i}" class="ouro" d="M{x0:.0f} {y0:.0f} Q {mx:.0f} {my:.0f} {x1:.0f} {y1:.0f}"/>'
ramos = "".join(_ramo(i, x, y) for i, (_, x, y, *_r) in enumerate(nos))
body = [f'      <div id="mp-ct" class="clip" data-start="0.15" data-duration="{D_DUR-0.15:.2f}">',
        '        <div id="mp-t" class="tt" style="top:290px;font-size:82px">Diagnóstico da sua <em>empresa</em></div>',
        f'        {svg("mp-ramos", 0, 0, 1080, 1300, ramos)}',
        f'        {svg("mp-emp", CX-150, CY-170, 300, 300, "<circle class=\'ouro\' cx=\'150\' cy=\'150\' r=\'140\'/><path d=\'M95 225 v-110 l55 -32 l55 32 v110\'/><path d=\'M78 225 h144\'/><path d=\'M118 135 h16 M166 135 h16 M118 165 h16 M166 165 h16 M118 195 h16 M166 195 h16\'/><path d=\'M141 225 v-24 h18 v24\'/>")}',
        f'        <div id="mp-emp-t" style="position:absolute;left:{CX-200}px;top:{CY+140}px;width:400px;text-align:center;font-family:Oswald,sans-serif;font-weight:700;font-size:44px;color:{BRANCO}">SUA EMPRESA</div>',        f'        <div id="mp-nota" class="mao" style="position:absolute;left:{CX+165}px;top:{CY+40}px;font-size:50px;transform:rotate(-6deg)">a gente<br>analisa tudo</div>',
        '      </div>']
js = [foco("#mp-t", 0.15, 0.45),
      risca("#mp-emp *", 0.3, 1.0, 0.05), foco("#mp-emp-t", 0.8, 0.4),
      foco("#mp-nota", 0.95, 0.4)]
for i, (k, x, y, nome, nota, t) in enumerate(nos):
    body.append(f'      <div id="mp-c{i}" class="clip" data-start="{t:.2f}" data-duration="{D_DUR-t:.2f}">'
                f'<div id="mp-n{i}" style="position:absolute;left:{x-170}px;top:{y-115}px;width:340px;height:330px;text-align:center">'
                f'{svg(f"mp-o{i}", 55, 0, 230, 230, "<circle cx=\'115\' cy=\'115\' r=\'108\'/>")}'
                f'<div style="position:absolute;left:0;top:88px;font-family:Oswald,sans-serif;font-weight:700;font-size:{48 if len(nome) < 9 else 38}px;width:340px;color:{BRANCO}">{nome}</div>'
                f'<div class="mao" style="position:absolute;left:0;top:238px;font-size:46px;width:340px;line-height:1;text-align:{["left","right","center"][i]};padding:0 10px">{nota}</div></div></div>')
    js.append(risca(f"#mp-l{i}", t - 0.15, 0.5))
    js.append(risca(f"#mp-o{i} circle", t, 0.55))
    js.append(foco(f"#mp-n{i} > div", t + 0.1, 0.35))
comp("diagnostico", D_DUR, EST_C, "\n".join(body), "\n".join(js))

# ---------------------------------------------------------------- regulariza (dividida) 9.91–12.05  local: pendente 1.09
R_DUR = 2.14
doc = ('<path d="M20 10 h90 l40 40 v170 h-130 z"/><path d="M110 10 v40 h40"/>'
       '<path d="M42 90 h80 M42 120 h80 M42 150 h50"/><circle class="ouro" cx="120" cy="185" r="34"/><path class="ouro" d="M104 186 l12 12 l22 -26"/>')
itens = [("CNPJ", 0.6), ("certidão", 0.9), ("regime", 1.2)]
linhas = "".join(f'<div id="rg-l{i}" class="mao" style="position:absolute;left:440px;top:{372 + i*68}px;font-size:58px;color:{BRANCO}">'
                 f'{txt} <span style="color:{GOLD}">✓</span></div>' for i, (txt, _) in enumerate(itens))
comp("regulariza", R_DUR, EST_C, f"""      <div id="rg-c" class="clip" data-start="0" data-duration="{R_DUR:.2f}">
        <div id="rg-t" class="tt" style="top:205px;font-size:62px">Regularizamos o que está <em>pendente</em></div>
        {svg("rg-doc", 240, 360, 170, 240, doc)}
        {linhas}
      </div>""", "\n".join([foco("#rg-t", 0.05, 0.35), risca("#rg-doc *", 0.15, 0.9, 0.05)]
                         + [foco(f"#rg-l{i}", t, 0.3) for i, (_, t) in enumerate(itens)]))

# ---------------------------------------------------------------- negócio novo (dividida) 12.05–15.92
# local: negócio 0.43 ; começamos 1.32 ; regime 2.03 ; estrutura 2.66
N_DUR = 3.87
predio = ('<path d="M30 230 v-160 l70 -40 l70 40 v160"/><path d="M10 230 h180"/>'
          '<path d="M62 100 h20 M118 100 h20 M62 140 h20 M118 140 h20 M62 180 h20 M118 180 h20"/><path d="M88 230 v-34 h24 v34"/>')
seta = '<path class="ouro" d="M10 60 C 60 10, 120 10, 170 50"/><path class="ouro" d="M150 30 l22 20 l-28 10"/>'
comp("negocio", N_DUR, EST_C, f"""      <div id="ng-c" class="clip" data-start="0.1" data-duration="{N_DUR-0.1:.2f}">
        <div id="ng-t" class="tt" style="top:205px;font-size:80px">Negócio <em>novo?</em></div>
        {svg("ng-pr", 210, 330, 200, 240, predio)}
        {svg("ng-se", 400, 330, 190, 80, seta)}
        <div id="ng-s" class="mao" style="position:absolute;left:590px;top:330px;font-size:50px;transform:rotate(-4deg)">já começa certo!</div>
        <div id="ng-a" class="mao" style="position:absolute;left:470px;top:430px;font-size:56px;color:{BRANCO}">regime certo <span style="color:{GOLD}">✓</span></div>
        <div id="ng-b" class="mao" style="position:absolute;left:470px;top:500px;font-size:56px;color:{BRANCO}">estrutura certa <span style="color:{GOLD}">✓</span></div>
      </div>""", "\n".join([foco("#ng-t", 0.1, 0.4), risca("#ng-pr *", 0.3, 1.0, 0.05), risca("#ng-se *", 1.25, 0.45),
                          foco("#ng-s", 1.4, 0.35), foco("#ng-a", 2.03, 0.35), foco("#ng-b", 2.66, 0.35)]))

# ---------------------------------------------------------------- primeiro ano (dividida) 15.92–18.29
# local: surpresas 0.16 ; retrabalhos 0.84 ; primeiro 1.54
P_DUR = 2.37
cal = ('<rect x="10" y="30" width="170" height="160" rx="14"/><path d="M10 72 h170 M52 14 v34 M138 14 v34"/>'
       '<path class="ouro" d="M60 132 l22 22 l46 -52"/>')
comp("primeiro", P_DUR, EST_C, f"""      <div id="pa-c" class="clip" data-start="0" data-duration="{P_DUR:.2f}">
        <div id="pa-t" class="tt" style="top:205px;font-size:80px">Primeiro <em>ano</em></div>
        {svg("pa-cal", 220, 340, 190, 200, cal)}
        <div id="pa-a" class="mao" style="position:absolute;left:470px;top:340px;font-size:58px;color:{BRANCO}"><span style="position:relative;display:inline-block">surpresas<i id="pa-ra" style="position:absolute;left:-6px;right:-6px;top:52%;height:6px;background:#d0606c;border-radius:3px;transform-origin:0 50%" data-layout-allow-occlusion></i></span></div>
        <div id="pa-b" class="mao" style="position:absolute;left:470px;top:410px;font-size:58px;color:{BRANCO}"><span style="position:relative;display:inline-block">retrabalhos<i id="pa-rb" style="position:absolute;left:-6px;right:-6px;top:52%;height:6px;background:#d0606c;border-radius:3px;transform-origin:0 50%" data-layout-allow-occlusion></i></span></div>
        <div id="pa-ok" class="mao" style="position:absolute;left:470px;top:490px;font-size:64px">tranquilo ✓</div>
      </div>""", "\n".join([foco("#pa-t", 0.05, 0.35), risca("#pa-cal *", 0.1, 0.8, 0.05),
                          foco("#pa-a", 0.16, 0.3), '    tl.fromTo("#pa-ra", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "sine.inOut" }, 0.45);',
                          foco("#pa-b", 0.84, 0.3), '    tl.fromTo("#pa-rb", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "sine.inOut" }, 1.1);', foco("#pa-ok", 1.54, 0.4)]))

# ---------------------------------------------------------------- legendas
G = [("CNPJ com",0.04),("*pendência,*",0.63),("certidão negativa",1.52),("*travada*",2.52),("ou empresa",3.24),("aberta no",3.76),("regime *errado?*",4.31),
("A gente faz",5.28),("um *diagnóstico*",5.91),("*fiscal,*",6.85),("*cadastral*",7.43),("e *societário*",8.09),("da sua empresa.",8.89),
("*Regularizamos*",9.91),("o que está",10.53),("*pendente*",11.00),("e, se for",11.52),("abrir um",12.09),("negócio *novo,*",12.48),("já começamos",13.37),
("no *regime*",13.96),("e nas *estruturas*",14.48),("*certas,*",15.36),("sem *surpresas*",15.92),("e sem *retrabalhos*",16.56),("no primeiro ano.",17.35),
("Fale com a gente",18.32),("antes que a",19.10),("*pendência*",19.80),("vire *problema.*",20.25),("Clique no",21.32),("*Saiba Mais!*",21.68)]
ENDS = {"regime *errado?*": CHART[0], "da sua empresa.": CHART[1], "no primeiro ano.": CHEIA2, "*Saiba Mais!*": FALA_FIM}
divs, gjs = [], []
for i, (txt, s) in enumerate(G):
    e = ENDS.get(txt, G[i+1][1] if i+1 < len(G) else FALA_FIM)
    parts = re.findall(r'\*[^*]+\*|[^\s*]+', txt)
    inner = " ".join(
        f'<span class="w{" hl" if p.startswith("*") else ""}">{html.escape(p.strip("*").upper())}</span>' for p in parts)
    top = 1500 if (s < CHART[0] or s >= CHEIA2) else (1640 if s < CHART[1] else 612)
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

CENAS = [("diagnostico", 5.04, 9.91), ("regulariza", 9.91, 12.05),
         ("negocio", 12.05, 15.92), ("primeiro", 15.92, CHEIA2)]
hosts = [host("fundo", 0, TOTAL, 1, 0)]
hosts += [host(m, s, e - s, 3, 2) for m, s, e in CENAS]
hosts += [host("legendas", 0, FALA_FIM, 7, 3, "captions")]
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
        box-shadow: 0 -8px 30px rgba(0,0,0,.25); }}
      #cam-sombra {{ position: absolute; left: 0; top: 0; width: 1080px; height: 200px; z-index: 2;
        background: linear-gradient(180deg, rgba(9,16,34,.55) 0%, rgba(9,16,34,.22) 45%, rgba(9,16,34,0) 100%); }}
      #logo-final {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; z-index: 9; }}
      #camcheia {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; z-index: 4; }}
      #camcheia video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      #cam video {{ position: absolute; left: 0; top: -450px; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <!-- Voz da apresentadora (contínua) -->
      <audio id="voz" class="clip" src="assets/fala.mp4" data-start="0" data-duration="{FALA_FIM}" data-track-index="5" data-volume="1"></audio>
      <!-- Começo: ela em tela cheia -->
      <div id="camcheia">
        <video id="fala0" class="clip" src="assets/abertura.mp4" data-start="0" data-duration="{SAI+0.6:.2f}" data-media-start="0" data-track-index="1" muted playsinline></video>
        <video id="fala3" class="clip" src="assets/fala.mp4" data-start="{CHEIA2:.2f}" data-duration="{FALA_FIM-CHEIA2:.2f}" data-media-start="{CHEIA2:.2f}" data-track-index="1" muted playsinline></video>
      </div>
      <!-- Final: tela da logo do vídeo bruto -->
      <video id="logo-final" class="clip" src="assets/logo_final_lento.mp4" data-start="{LOGO_INI}" data-duration="{LOGO_DUR}" data-track-index="6" muted playsinline></video>
      <!-- Metade de baixo: ela falando -->
      <div id="cam">
        <video id="fala2" class="clip" src="assets/fala.mp4" data-start="{VOLTA:.2f}" data-duration="{CHEIA2+0.5-VOLTA:.2f}" data-media-start="{VOLTA:.2f}" data-track-index="1" muted playsinline></video>
        <div id="cam-sombra"></div>
      </div>
{chr(10).join(hosts)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // gráfico em tela cheia: a metade de baixo desce e depois volta, suave
      tl.set("#cam", {{ opacity: 0 }}, 0);
      tl.to("#camcheia", {{ opacity: 0, duration: 0.55, ease: "sine.inOut" }}, {SAI:.2f});
      tl.to("#cam", {{ opacity: 1, duration: 0.5, ease: "sine.inOut" }}, {VOLTA:.2f});
      // final: ela volta em tela cheia para o convite
      // troca direta no corte da 2ª gravação; a imagem entra levemente aproximada e se acomoda
      tl.set("#camcheia", {{ opacity: 1, transformOrigin: "540px 760px" }}, {CHEIA2:.2f});
      tl.fromTo("#camcheia", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.7, ease: "power2.out" }}, {CHEIA2:.2f});
      tl.set("#cam", {{ opacity: 0 }}, {CHEIA2:.2f});
      // final: dissolve suave dela para a logo
      tl.fromTo("#logo-final", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "sine.inOut" }}, {LOGO_INI});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")

# ---------------------------------------------------------------- aplicar a marca
REF = json.load(open(Path(__file__).with_name("marca_referencia.json"), encoding="utf-8"))

def _rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def aplicar_marca(texto):
    """Troca, numa passada só, cada cor da paleta de referência pela cor da marca (hex e rgba)."""
    troca_hex, troca_rgb = {}, {}
    for chave, cor_ref in REF.items():
        if str(cor_ref).startswith("#") and chave in MARCA:
            troca_hex[cor_ref.lower()] = MARCA[chave]
            troca_rgb[_rgb(cor_ref)] = _rgb(MARCA[chave])
    texto = re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: troca_hex.get(m.group(0).lower(), m.group(0)), texto)
    def _rgba(m):
        k = tuple(int(x) for x in m.group(1, 2, 3))
        R, G_, B = troca_rgb.get(k, k)
        return f"rgba({R},{G_},{B},"
    texto = re.sub(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,", _rgba, texto)
    texto = texto.replace(REF["pilula"], MARCA["pilula"]).replace(REF["nome"], MARCA["nome"])
    texto = texto.replace(REF["logo"], MARCA["logo"])
    if MARCA.get("css_extra"):            # ajustes de estilo da marca (ex.: título em itálico)
        texto = texto.replace("  </style>", f"    {MARCA['css_extra']}\n  </style>", 1)
    return texto

usadas = {"fundo", "legendas", "progresso", "atras"} | {c for c, _, _ in CENAS}
for f in C.glob("*.html"):
    if f.stem not in usadas:
        f.unlink()                       # cenas do modelo que este vídeo não usa
    else:
        f.write_text(aplicar_marca(f.read_text()))
(P / "index.html").write_text(aplicar_marca((P / "index.html").read_text()))
print(f"ok: marca {MARCA['nome']}")
