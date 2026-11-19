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
vid_js = '    tl.fromTo("#bg-luz", { x: 0 }, { x: 2600, duration: 9, ease: "none", repeat: 2 }, 0);\n' + "\n".join(
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
    #bg-luz {{ position: absolute; left: -900px; top: -400px; width: 700px; height: 2800px; }}
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

# ================================================================ cenas do vídeo 2 (Regularização) — ESTILO B: editorial com ícones
# Faixa de cima menor (0–700): conteúdo entre y 230 e 590; legenda em y ≈ 612.

def icone(nome, tam=96):
    """Ícones de traço fino dourado, desenhados aqui (sem imagens externas)."""
    p = {
        "lupa": '<circle cx="42" cy="42" r="26"/><line x1="61" y1="61" x2="86" y2="86"/><path d="M30 42 l8 8 l16 -18"/>',
        "documento": '<path d="M24 10 h38 l18 18 v62 h-56 z"/><path d="M62 10 v18 h18"/><path d="M36 58 l10 10 l20 -22"/>',
        "predio": '<path d="M18 90 v-62 l30 -16 l30 16 v62"/><line x1="10" y1="90" x2="86" y2="90"/><path d="M36 42 h8 M52 42 h8 M36 58 h8 M52 58 h8"/><path d="M42 90 v-16 h12 v16"/>',
        "escudo": '<path d="M48 8 l34 12 v26 c0 22 -15 36 -34 44 c-19 -8 -34 -22 -34 -44 v-26 z"/><path d="M34 48 l10 10 l20 -22"/>',
    }[nome]
    return (f'<svg class="ic" width="{tam}" height="{tam}" viewBox="0 0 96 96" fill="none" stroke="{GOLD}" stroke-width="4" '
            f'stroke-linecap="round" stroke-linejoin="round">{p}</svg>')

EST_B = f"""
    .ed {{ position: absolute; left: 140px; width: 800px; text-align: center; font-family: "Playfair Display", serif; color: {BRANCO};
      line-height: 1.05; text-shadow: 0 6px 30px rgba(0,0,0,.45); }}
    .ed em {{ font-style: italic; color: {GOLD}; }}
    .ic-w {{ position: absolute; left: 0; width: 1080px; text-align: center; }}
    .ic {{ display: inline-block; filter: drop-shadow(0 0 14px rgba(201,173,110,.35)); }}
    .chips {{ position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; gap: 18px; }}
    .chip {{ display: inline-flex; align-items: center; gap: 12px; padding: 14px 24px; border-radius: 40px; border: 2px solid rgba(201,173,110,.55);
      background: rgba(8,14,30,.55); font-family: "Poppins", sans-serif; font-weight: 700; font-size: 30px; color: {BRANCO}; white-space: nowrap; }}
    .chip .ok {{ width: 34px; height: 34px; border-radius: 50%; background: {GOLD}; color: {NAVY_T}; font-size: 22px; font-weight: 800;
      text-align: center; line-height: 34px; }}
    .chip.x {{ border-color: {BORDO_L}; color: #e5a3aa; position: relative; }}
    .chip.x i {{ position: absolute; left: 18px; right: 18px; top: 50%; height: 5px; background: #d0606c; transform-origin: 0 50%; }}
    .regua {{ position: absolute; left: 470px; width: 140px; height: 3px; background: {GOLD}; transform-origin: 50% 50%; }}
"""

def desenha(sel, t, d=0.9):
    """Ícone 'se desenha' (traço aparecendo) e acende."""
    return (f'    tl.fromTo("{sel} .ic *", {{ strokeDasharray: 300, strokeDashoffset: 300 }}, '
            f'{{ strokeDashoffset: 0, duration: {d}, ease: "sine.inOut", stagger: 0.08 }}, {t:.2f});')

def palavra_a_palavra(sel, t, passo=0.09):
    return (f'    tl.fromTo("{sel} .w", {{ opacity: 0, y: 12, filter: "blur(6px)" }}, '
            f'{{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "power2.out", stagger: {passo} }}, {t:.2f});')

def ws(txt):
    """Quebra o título em palavras animáveis; *x* vira itálico dourado."""
    out = []
    for p in re.findall(r"\*[^*]+\*|\S+", txt):
        if p.startswith("*"):
            out.append(f'<span class="w" style="display:inline-block"><em>{html.escape(p.strip("*"))}</em></span>')
        else:
            out.append(f'<span class="w" style="display:inline-block">{html.escape(p)}</span>')
    return " ".join(out)

# diagnóstico (TELA CHEIA) 5.04–9.91  local: diagnóstico 0.99 ; fiscal 1.81 ; cadastral 2.39 ; societário 3.12
D_DUR = 4.87
dg_itens = [("01", "Fiscal", "impostos e obrigações", 1.81), ("02", "Cadastral", "CNPJ, inscrições e certidões", 2.39),
            ("03", "Societário", "contrato social e sócios", 3.12)]
body = [f'      <div id="dg-c0" class="clip" data-start="0.1" data-duration="{D_DUR-0.1:.2f}">',
        f'        <div id="dg-ic" class="ic-w" style="top:236px">{icone("lupa", 100)}</div>',
        f'        <div id="dg-t" class="ed" style="top:350px;font-size:80px">{ws("Diagnóstico da sua *empresa*")}</div>',
        '        <div id="dg-r" class="regua" style="top:545px"></div>',
        '      </div>']
js = [desenha("#dg-ic", 0.1, 1.0), palavra_a_palavra("#dg-t", 0.35),
      '    tl.fromTo("#dg-r", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "sine.inOut" }, 0.9);']
for i, (n, a, b, t) in enumerate(dg_itens):
    top = 590 + i * 150
    body.append(f'      <div id="dg-c{i+1}" class="clip" data-start="{t:.2f}" data-duration="{D_DUR-t:.2f}"><div id="dg-i{i}" class="dgi" style="top:{top}px">'
                f'<span class="num">{n}</span><span class="nm">{a}<small>{html.escape(b)}</small></span></div></div>')
    js.append(entra(f"#dg-i{i}", t + 0.02, 0.5, 12))
    if i > 0:
        js.append(f'    tl.to("#dg-i{i-1} .num", {{ color: "rgba(247,245,246,.35)", duration: 0.4, ease: "sine.inOut" }}, {t:.2f});')
comp("diagnostico", D_DUR, EST_B + f"""
    .dgi {{ position: absolute; left: 230px; width: 640px; height: 130px; display: flex; align-items: center; gap: 34px;
      border-bottom: 1px solid rgba(201,173,110,.35); }}
    .dgi .num {{ font-family: "Playfair Display", serif; font-style: italic; font-size: 84px; color: {GOLD}; width: 120px; }}
    .dgi .nm {{ font-family: "Playfair Display", serif; font-size: 56px; color: {BRANCO}; line-height: 1; }}
    .dgi small {{ display: block; font-family: "Poppins", sans-serif; font-size: 28px; font-weight: 600; opacity: .7; margin-top: 8px; }}
""", "\n".join(body), "\n".join(js))

# regulariza (dividida) 9.91–12.05  local: pendente 1.09
R_DUR = 2.14
comp("regulariza", R_DUR, EST_B, f"""      <div id="rg-c" class="clip" data-start="0" data-duration="{R_DUR:.2f}">
        <div id="rg-ic" class="ic-w" style="top:210px">{icone("documento", 84)}</div>
        <div id="rg-t" class="ed" style="top:306px;font-size:64px">{ws("Regularizamos o que está *pendente*")}</div>
        <div id="rg-ch" class="chips" style="top:486px">
          <span id="rg-a" class="chip"><span class="ok">✓</span>CNPJ</span>
          <span id="rg-b" class="chip"><span class="ok">✓</span>Certidão</span>
          <span id="rg-d" class="chip"><span class="ok">✓</span>Regime</span>
        </div>
      </div>""", "\n".join([desenha("#rg-ic", 0.0, 0.8), palavra_a_palavra("#rg-t", 0.1, 0.07),
                          entra("#rg-a", 0.75, 0.4, 10), entra("#rg-b", 0.95, 0.4, 10), entra("#rg-d", 1.15, 0.4, 10)]))

# negócio novo (dividida) 12.05–15.92  local: negócio 0.43 ; começamos 1.32 ; regime 2.03 ; estrutura 2.66
N_DUR = 3.87
comp("negocio", N_DUR, EST_B, f"""      <div id="ng-c" class="clip" data-start="0.1" data-duration="{N_DUR-0.1:.2f}">
        <div id="ng-ic" class="ic-w" style="top:216px">{icone("predio", 84)}</div>
        <div id="ng-t" class="ed" style="top:334px;font-size:80px">{ws("Negócio *novo?*")}</div>
        <div id="ng-s" class="ic-w" style="top:436px;font-family:Poppins,sans-serif;font-weight:700;font-size:28px;letter-spacing:.2em;color:{GOLD}">JÁ COMEÇA CERTO</div>
        <div id="ng-ch" class="chips" style="top:500px">
          <span id="ng-a" class="chip"><span class="ok">✓</span>Regime certo</span>
          <span id="ng-b" class="chip"><span class="ok">✓</span>Estrutura certa</span>
        </div>
      </div>""", "\n".join([desenha("#ng-ic", 0.0, 0.9), palavra_a_palavra("#ng-t", 0.33), foco("#ng-s", 1.22, 0.4),
                          entra("#ng-a", 1.93, 0.45, 10), entra("#ng-b", 2.56, 0.45, 10)]))

# primeiro ano (dividida) 15.92–18.29  local: surpresas 0.16 ; retrabalhos 0.84 ; primeiro 1.54
P_DUR = 2.37
comp("primeiro", P_DUR, EST_B, f"""      <div id="pa-c" class="clip" data-start="0" data-duration="{P_DUR:.2f}">
        <div id="pa-ic" class="ic-w" style="top:216px">{icone("escudo", 84)}</div>
        <div id="pa-t" class="ed" style="top:334px;font-size:76px">{ws("Primeiro ano *tranquilo*")}</div>
        <div id="pa-ch" class="chips" style="top:480px">
          <span id="pa-a" class="chip x">Surpresas<i id="pa-ra" data-layout-allow-occlusion></i></span>
          <span id="pa-b" class="chip x">Retrabalho<i id="pa-rb" data-layout-allow-occlusion></i></span>
        </div>
      </div>""", "\n".join([desenha("#pa-ic", 0.0, 0.8), palavra_a_palavra("#pa-t", 0.05, 0.08),
                          entra("#pa-a", 0.16, 0.4, 10), '    tl.fromTo("#pa-ra", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "sine.inOut" }, 0.5);',
                          entra("#pa-b", 0.84, 0.4, 10), '    tl.fromTo("#pa-rb", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "sine.inOut" }, 1.15);']))

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
    top = 1500 if (s < CHART[0] or s >= CHEIA2) else (1100 if s < CHART[1] else 612)
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
      #cam video {{ position: absolute; left: 0; top: -450px; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <!-- Voz da apresentadora (contínua) -->
      <audio id="voz" class="clip" src="assets/fala.mp4" data-start="0" data-duration="{FALA_FIM}" data-track-index="5" data-volume="1"></audio>
      <!-- Começo: ela em tela cheia -->
      <div id="camcheia">
        <video id="fala0" class="clip" src="assets/fala.mp4" data-start="0" data-duration="{SAI+0.6:.2f}" data-media-start="0" data-track-index="1" muted playsinline></video>
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

usadas = {"fundo", "legendas", "progresso"} | {c for c, _, _ in CENAS}
for f in C.glob("*.html"):
    if f.stem not in usadas:
        f.unlink()                       # cenas do modelo que este vídeo não usa
    else:
        f.write_text(aplicar_marca(f.read_text()))
(P / "index.html").write_text(aplicar_marca((P / "index.html").read_text()))
print(f"ok: marca {MARCA['nome']}")
