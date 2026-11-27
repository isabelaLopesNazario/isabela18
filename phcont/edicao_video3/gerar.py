"""PHcont vídeo 3 (Reforma Tributária), estilo H: infográfico em cima + ela num cartão; tela cheia nos momentos de impacto.
Gera index.html (HyperFrames). Tempos na fala já sem pausas (assets/fala.mp4)."""
import json, re
from pathlib import Path

AQUI = Path(__file__).parent
W = json.load(open(AQUI / "assets/transcript.json"))
W = W["words"] if isinstance(W, dict) else W
CORRIGE = {"SMS,": "ICMS,"}
for w in W:
    w["text"] = CORRIGE.get(w["text"], w["text"])

FIM_FALA = 27.30
CORTES = [3.62, 5.89, 10.34, 13.10, 13.88, 23.01, 26.17]           # emendas da fala (troca de layout ou "soco" leve)
CARD_INI, CARD_FIM = 5.89, 23.01                                    # trecho com ela no cartão
LOGO_INI, LOGO_DUR = FIM_FALA - 0.3, 4.7
TOTAL = round(LOGO_INI + LOGO_DUR, 2)
DEST = {"icms", "iss", "pis", "cofins", "acabar", "empresa", "lugar", "ibs", "cbs", "preço", "margem", "crédito", "mais",
        "menos", "ano", "etapa", "plano", "concorrente", "entender", "estudando", "primeiro", "dia", "whatsapp"}
CENAS = [0, 3.62, 5.89, 10.34, 13.10, 17.04, 23.01, 26.17, FIM_FALA]

def t(palavra, n=1):
    """instante em que a n-ésima ocorrência da palavra começa"""
    k = 0
    for w in W:
        if re.sub(r"[^\wç]", "", w["text"].lower()) == palavra:
            k += 1
            if k == n:
                return round(w["start"], 2)
    raise KeyError(palavra)

# ---------------------------------------------------------------- legenda (1–3 palavras, minúsculas como falado)
# grupos escolhidos à mão (até 3 palavras, quebrando onde a frase respira e nas trocas de cena)
FRASES = ["ICMS", "ISS", "PIS e COFINS", "vão acabar", "A sua empresa", "está pronta", "para o que", "vem no lugar?",
          "O IBS e", "o CBS", "mudam preço", "margem", "e crédito", "Tem gente", "que vai", "pagar mais", "e tem gente",
          "que vai", "pagar menos", "Essa mudança", "dura um ano", "com regras", "diferentes", "a cada etapa", "Imagina",
          "atravessar", "essa mudança", "com um plano", "na mão", "Enquanto", "o concorrente", "ainda está",
          "tentando entender", "Fale com quem", "está estudando", "a mudança", "desde o", "primeiro dia", "Chame a gente", "no WhatsApp"]
grupos, k = [], 0
for f in FRASES:
    n = len(f.split()); grupos.append(W[k:k + n]); k += n
assert k == len(W), (k, len(W))
legs = []
for gi, g in enumerate(grupos):
    ini = g[0]["start"]
    fim = grupos[gi + 1][0]["start"] if gi + 1 < len(grupos) else FIM_FALA
    def fmt(w):
        txt = re.sub(r"[,.;]$", "", w["text"])
        chave = re.sub(r"[^\wç]", "", txt.lower())
        return f"<b>{txt}</b>" if chave in DEST else txt
    html = " ".join(fmt(w) for w in g)
    html = html[0].upper() + html[1:] if gi == 0 else html
    cartao = CARD_INI <= ini < CARD_FIM
    legs.append((round(ini, 2), round(min(fim, CENAS[[c for c in range(len(CENAS)) if CENAS[c] <= ini][-1] + 1]) - ini, 2), html, cartao))

# ---------------------------------------------------------------- HTML
L = []
def clip(id_, ini, dur, inner, cls="", track=3):
    L.append(f'<div id="{id_}" class="clip {cls}" data-start="{ini}" data-duration="{round(dur, 2)}" data-track-index="{track}">{inner}</div>')

# Cena 1 (tela cheia): os 4 tributos grandes, riscados em "acabar"
trib = ["ICMS", "ISS", "PIS", "COFINS"]
inner = '<div class="rot">— REFORMA TRIBUTÁRIA —</div><div class="tribs">' + "".join(
    f'<span class="trib" id="tr{i}">{n}<i class="risco" id="rk{i}"></i></span>' for i, n in enumerate(trib)) + "</div>"
clip("c1", 0, 3.62, inner, "topo")
# Cena 2: pergunta
clip("c2", 3.62, 5.89 - 3.62, '<div class="rot" id="c2r">— A SUA EMPRESA ESTÁ PRONTA? —</div><div class="big" id="c2t">O QUE VEM<br>NO <em>LUGAR?</em></div>', "topo")
# Cena 3 (cartão): mapa IBS + CBS
inner = '''<div class="rot">— O QUE MUDA —</div><div class="tit" id="c3t">IBS + CBS <em>MUDAM</em></div>
<svg class="ligas" viewBox="0 0 1080 640"><path id="lg0" d="M450 440 C 410 440, 390 440, 350 440"/><path id="lg1" d="M540 520 C 540 535, 540 545, 540 560"/><path id="lg2" d="M630 440 C 670 440, 690 440, 730 440"/></svg>
<div class="nucleo" id="nuc"><div class="raios"></div><span>IBS<br>+ CBS</span></div>
<div class="no" id="no0" style="left:110px;top:395px"><small>IMPACTO</small>PREÇO</div>
<div class="no" id="no1" style="left:420px;top:560px"><small>IMPACTO</small>MARGEM</div>
<div class="no" id="no2" style="left:730px;top:395px"><small>IMPACTO</small>CRÉDITO</div>'''
clip("c3", 5.89, 10.34 - 5.89, inner, "info")
# Cena 4: paga mais x paga menos
inner = '''<div class="rot">— QUEM PAGA —</div><div class="tit">MAIS <em>OU</em> MENOS?</div>
<div class="linha neg" id="pm0"><b class="sinal">↑</b><div><strong>Paga mais</strong><small>tem gente que vai pagar mais</small></div></div>
<div class="linha pos" id="pm1"><b class="sinal">↓</b><div><strong>Paga menos</strong><small>e tem gente que vai pagar menos</small></div></div>'''
clip("c4", 10.34, 13.10 - 10.34, inner, "info")
# Cena 5: linha do tempo
inner = '''<div class="rot">— TRANSIÇÃO —</div><div class="tit">A MUDANÇA DURA <em>1 ANO</em></div>
<div class="regua"><div class="trilho"></div><div class="barra" id="barra"></div>''' + "".join(
    f'<div class="marco" id="mc{i}" style="left:{40 + i * 266}px"><i></i><span>ETAPA {i + 1}</span></div>' for i in range(4)) + '''</div>
<div class="sub" id="c5s">regras diferentes a cada etapa</div>'''
clip("c5", 13.10, 17.04 - 13.10, inner, "info")
# Cena 6: com plano x sem plano
inner = '''<div class="rot">— QUEM SE PREPARA —</div><div class="tit">COM PLANO <em>× SEM PLANO</em></div>
<div class="linha pos" id="cp0"><b class="sinal">✓</b><div><strong>Você</strong><small>atravessa a mudança com um plano na mão</small></div></div>
<div class="linha neg" id="cp1"><b class="sinal">−</b><div><strong>Concorrente</strong><small>ainda está tentando entender</small></div><span class="pilula" id="pil">plano: ?</span></div>'''
clip("c6", 17.04, 23.01 - 17.04, inner, "info")
# Cena 7 (tela cheia): desde o 1º dia
clip("c7", 23.01, 26.17 - 23.01, '<div class="rot" id="c7r">— ESTUDANDO A MUDANÇA —</div><div class="big" id="c7t" style="font-size:132px">DESDE O <em>1º DIA</em></div>', "topo")
# Cena 8: ela desfocada + chamada
clip("c8", 26.17, FIM_FALA - 26.17, '<div class="centro" id="c8t">CHAME A GENTE<br>NO <em>WHATSAPP</em></div>', "meio", track=7)

leg_html = "\n".join(f'<div id="lg{i}" class="clip leg {"leg-card" if c else "leg-cheia"}" data-start="{s}" data-duration="{d}" data-track-index="8">{h}</div>'
                     for i, (s, d, h, c) in enumerate(legs))

A = []  # animações (gsap)
def a(js): A.append("      " + js)
EN = "power2.out"
# cena 1
a(f'tl.fromTo("#c1 .rot", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, 0.05);')
for i, n in enumerate(trib):
    a(f'tl.fromTo("#tr{i}", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:.6, ease:"{EN}"}}, {max(0.05, t(n.lower()) - 0.05)});')
    a(f'tl.fromTo("#rk{i}", {{scaleX:0}}, {{scaleX:1, duration:.45, ease:"power2.inOut"}}, {t("acabar") + i * 0.09:.2f});')
    a(f'tl.to("#tr{i}", {{color:"rgba(247,245,246,.45)", duration:.4}}, {t("acabar") + i * 0.09:.2f});')
# cena 2
a(f'tl.fromTo("#c2r", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, 3.7);')
a(f'tl.fromTo("#c2t", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:.8, ease:"{EN}"}}, {t("que", 1) - 0.1});')
# cena 3
a(f'tl.fromTo("#c3 .rot, #c3t", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:.7, stagger:.12, ease:"{EN}"}}, 5.95);')
a(f'tl.fromTo("#nuc", {{opacity:0, scale:.85}}, {{opacity:1, scale:1, duration:.9, ease:"{EN}"}}, {t("ibs")});')
a(f'tl.fromTo("#nuc .raios", {{rotation:0}}, {{rotation:40, duration:4.5, ease:"none"}}, {t("ibs")});')
for i, p in enumerate(["preço", "margem", "crédito"]):
    a(f'tl.fromTo("#lg{i}", {{strokeDashoffset:400}}, {{strokeDashoffset:0, duration:.8, ease:"sine.inOut"}}, {t(p) - 0.35:.2f});')
    a(f'tl.fromTo("#no{i}", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, {t(p) - 0.05:.2f});')
    a(f'tl.to("#no{i}", {{borderColor:"#C9AD6E", boxShadow:"0 0 26px rgba(201,173,110,.35)", duration:.4}}, {t(p):.2f});')
    if i:
        a(f'tl.to("#no{i - 1}", {{borderColor:"rgba(201,173,110,.35)", boxShadow:"0 0 0 rgba(0,0,0,0)", duration:.4}}, {t(p):.2f});')
# cena 4
a(f'tl.fromTo("#c4 .rot, #c4 .tit", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:.7, stagger:.12, ease:"{EN}"}}, 10.4);')
a(f'tl.fromTo("#pm0", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, {t("mais") - 0.3:.2f});')
a(f'tl.to("#pm0", {{borderColor:"#A33A46", duration:.4}}, {t("mais"):.2f});')
a(f'tl.fromTo("#pm1", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, {t("menos") - 0.3:.2f});')
a(f'tl.to("#pm1", {{borderColor:"#C9AD6E", duration:.4}}, {t("menos"):.2f});')
a(f'tl.to("#pm0", {{borderColor:"rgba(163,58,70,.45)", duration:.4}}, {t("menos"):.2f});')
# cena 5
a(f'tl.fromTo("#c5 .rot, #c5 .tit", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:.7, stagger:.12, ease:"{EN}"}}, 13.15);')
a(f'tl.fromTo("#c5 .regua", {{opacity:0}}, {{opacity:1, duration:.6}}, 13.5);')
a(f'tl.fromTo("#barra", {{width:0}}, {{width:838, duration:{t("etapa") + 0.3 - t("ano"):.2f}, ease:"sine.inOut"}}, {t("ano"):.2f});')
for i, quando in enumerate([t("ano"), t("regras"), t("cada"), t("etapa")]):
    a(f'tl.to("#mc{i} i", {{borderColor:"#C9AD6E", backgroundColor:"#C9AD6E", boxShadow:"0 0 18px rgba(201,173,110,.6)", duration:.35}}, {quando + 0.1:.2f});')
    a(f'tl.to("#mc{i} span", {{color:"#C9AD6E", duration:.35}}, {quando + 0.1:.2f});')
a(f'tl.fromTo("#c5s", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, {t("regras"):.2f});')
# cena 6
a(f'tl.fromTo("#c6 .rot, #c6 .tit", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:.7, stagger:.12, ease:"{EN}"}}, 17.1);')
a(f'tl.fromTo("#cp0", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, {t("atravessar"):.2f});')
a(f'tl.to("#cp0", {{borderColor:"#C9AD6E", boxShadow:"0 0 26px rgba(201,173,110,.25)", duration:.4}}, {t("plano"):.2f});')
a(f'tl.fromTo("#cp1", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, {t("concorrente") - 0.2:.2f});')
a(f'tl.fromTo("#pil", {{opacity:0, scale:.8, rotation:-8}}, {{opacity:1, scale:1, rotation:-6, duration:.6, ease:"{EN}"}}, {t("entender") - 0.1:.2f});')
# cena 7
a(f'tl.fromTo("#c7r", {{opacity:0, y:10}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, {t("estudando") - 0.3:.2f});')
a(f'tl.fromTo("#c7t", {{opacity:0, y:18}}, {{opacity:1, y:0, duration:.8, ease:"{EN}"}}, {t("desde") - 0.1:.2f});')
# cena 8: ela desfoca e a chamada entra no meio
a(f'tl.fromTo("#cheia2", {{filter:"blur(0px) brightness(1)"}}, {{filter:"blur(22px) brightness(.55)", duration:.6, ease:"sine.out"}}, 26.17);')
a(f'tl.fromTo("#c8t", {{opacity:0, y:14}}, {{opacity:1, y:0, duration:.6, ease:"{EN}"}}, 26.25);')
# entrada do cartão (no quadro do corte) e "socos" leves nas outras emendas
a(f'tl.fromTo("#cardbox", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:.7, ease:"{EN}"}}, {CARD_INI});')
for c in CORTES:
    alvo = "#cardin" if CARD_INI <= c < CARD_FIM else ("#cheia1in" if c < CARD_INI else "#cheia2in")
    a(f'tl.fromTo("{alvo}", {{scale:1.06}}, {{scale:1, duration:.7, ease:"sine.out"}}, {c});')
# quem aparece (os vídeos ficam em camadas; troca exatamente no quadro do corte)
a('tl.set("#cardbox", {autoAlpha:0}, 0); tl.set("#cheia2", {autoAlpha:0}, 0);')
a(f'tl.set("#cheia1", {{autoAlpha:0}}, {CARD_INI}); tl.set("#cardbox", {{visibility:"visible"}}, {CARD_INI});')
a(f'tl.set("#cardbox", {{autoAlpha:0}}, {CARD_FIM}); tl.set("#cheia2", {{autoAlpha:1}}, {CARD_FIM});')
# legendas
for i, (s, d, h, c) in enumerate(legs):
    a(f'tl.fromTo("#lg{i}", {{opacity:0, y:6}}, {{opacity:1, y:0, duration:.18, ease:"{EN}"}}, {s});')
# final: dissolve para a logo
a(f'tl.fromTo("#logo-final", {{opacity:0}}, {{opacity:1, duration:.6, ease:"sine.inOut"}}, {LOGO_INI});')

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#070d1c; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:Poppins, sans-serif; color:#F7F5F6; }}
/* fundo: marinho escuro com grade de pontinhos e brilho dourado atrás do infográfico */
#fundo {{ position:absolute; inset:0; background:
   radial-gradient(520px 360px at 540px 360px, rgba(201,173,110,.16), rgba(201,173,110,0) 70%),
   radial-gradient(circle, rgba(247,245,246,.13) 1.6px, transparent 1.8px) 0 0/34px 34px,
   linear-gradient(180deg, #0d1a36 0%, #070d1c 100%); }}
/* ela em tela cheia */
.cheia {{ position:absolute; inset:0; overflow:hidden; z-index:2; }}
.cheiain {{ position:absolute; inset:0; }}
.cheia video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
.cheia::after {{ content:""; position:absolute; left:0; right:0; top:0; height:760px;
   background:linear-gradient(180deg, rgba(7,13,28,.78) 0%, rgba(7,13,28,.45) 45%, rgba(7,13,28,0) 100%); }}
/* ela no cartão */
#cardbox {{ position:absolute; left:170px; top:800px; width:740px; height:1040px; border-radius:40px; overflow:hidden; z-index:2;
   border:2px solid rgba(201,173,110,.45); box-shadow:0 30px 80px rgba(0,0,0,.55); }}
#cardin {{ position:absolute; inset:0; }}
#cardin video {{ position:absolute; left:-170px; top:-380px; width:1080px; height:1920px; object-fit:cover; }}
/* textos */
.topo, .info, .meio {{ position:absolute; inset:0; z-index:5; }}
.rot {{ position:absolute; left:0; right:0; top:150px; text-align:center; font-weight:600; font-size:28px; letter-spacing:.34em; color:#C9AD6E; }}
.tribs {{ position:absolute; left:60px; right:60px; top:200px; display:flex; flex-wrap:wrap; justify-content:center; gap:4px 34px; }}
.trib {{ position:relative; font-family:Oswald, sans-serif; font-weight:700; font-size:120px; line-height:1.02; color:#C9AD6E; }}
.risco {{ position:absolute; left:-8px; right:-8px; top:52%; height:12px; background:#A33A46; transform-origin:left center; border-radius:3px; }}
.big {{ position:absolute; left:0; right:0; top:210px; text-align:center; font-family:Oswald, sans-serif; font-weight:700; font-size:150px; line-height:1.0; }}
.big em, .tit em, .centro em {{ font-style:normal; color:#C9AD6E; }}
.tit {{ position:absolute; left:40px; right:40px; top:205px; text-align:center; font-family:Oswald, sans-serif; font-weight:700; font-size:84px; line-height:1.05; }}
.centro {{ position:absolute; left:0; right:0; top:760px; text-align:center; font-family:Oswald, sans-serif; font-weight:700; font-size:132px; line-height:1.02; }}
/* mapa */
.ligas {{ position:absolute; left:0; top:0; width:1080px; height:640px; }}
.ligas path {{ fill:none; stroke:#C9AD6E; stroke-width:3; stroke-dasharray:400; opacity:.85; }}
.nucleo {{ position:absolute; left:450px; top:350px; width:180px; height:180px; border-radius:50%; border:3px solid #C9AD6E; display:grid; place-items:center;
   background:radial-gradient(circle, #1b2a4d 0%, #0d1730 70%); box-shadow:0 0 50px rgba(201,173,110,.35); }}
.nucleo span {{ position:relative; text-align:center; font-family:Oswald, sans-serif; font-weight:700; font-size:44px; line-height:.95; }}
.raios {{ position:absolute; inset:12px; border-radius:50%;
   background:repeating-conic-gradient(rgba(201,173,110,.32) 0 1.2deg, transparent 1.2deg 15deg);
   -webkit-mask:radial-gradient(circle, transparent 52%, #000 53%); mask:radial-gradient(circle, transparent 52%, #000 53%); }}
.no {{ position:absolute; width:240px; padding:14px 18px; border-radius:18px; border:2px solid rgba(201,173,110,.35); background:rgba(13,23,48,.92);
   font-family:Oswald, sans-serif; font-weight:700; font-size:46px; text-align:center; line-height:1; }}
.no small {{ display:block; font-family:Poppins; font-weight:600; font-size:16px; letter-spacing:.24em; color:#C9AD6E; margin-bottom:6px; }}
/* linhas (paga mais/menos, com/sem plano) */
.linha {{ position:absolute; left:90px; right:90px; height:132px; border-radius:22px; display:flex; align-items:center; gap:26px; padding:0 30px;
   background:rgba(13,23,48,.92); border:2px solid rgba(201,173,110,.3); }}
#pm0, #cp0 {{ top:345px; }} #pm1, #cp1 {{ top:500px; }}
.linha.neg {{ border-color:rgba(163,58,70,.45); }}
.sinal {{ flex:none; width:64px; height:64px; border-radius:16px; display:grid; place-items:center; font-size:40px; font-weight:700; }}
.pos .sinal {{ background:#C9AD6E; color:#0B1426; }} .neg .sinal {{ background:#A33A46; color:#fff; }}
.linha strong {{ display:block; font-size:44px; font-weight:700; line-height:1.1; }}
.linha small {{ display:block; font-size:25px; color:rgba(247,245,246,.66); margin-top:2px; }}
.pilula {{ position:absolute; right:26px; top:-18px; background:#A33A46; color:#fff; font-weight:700; font-size:24px; padding:6px 18px; border-radius:30px; }}
/* linha do tempo */
.regua {{ position:absolute; left:100px; width:880px; top:400px; height:140px; }}
.trilho {{ position:absolute; left:0; right:0; top:40px; height:10px; border-radius:6px; background:rgba(247,245,246,.12); }}
.barra {{ position:absolute; left:0; top:40px; height:10px; width:0; border-radius:6px; background:linear-gradient(90deg, #BBA372, #E2C98C); box-shadow:0 0 18px rgba(201,173,110,.6); }}
.marco {{ position:absolute; top:22px; width:0; }}
.marco i {{ position:absolute; left:-23px; top:0; width:46px; height:46px; border-radius:50%; border:3px solid rgba(247,245,246,.3); background:#0d1730; }}
.marco span {{ position:absolute; left:-90px; width:180px; top:66px; text-align:center; font-weight:600; font-size:24px; letter-spacing:.14em; color:rgba(247,245,246,.45); }}
.marco.on i {{ border-color:#C9AD6E; background:#C9AD6E; box-shadow:0 0 18px rgba(201,173,110,.6); }}
.marco.on span {{ color:#C9AD6E; }}
.sub {{ position:absolute; left:0; right:0; top:575px; text-align:center; font-size:30px; color:rgba(247,245,246,.7); }}
/* legenda */
.leg {{ position:absolute; left:0; right:0; text-align:center; font-weight:700; font-size:54px; color:#fff; z-index:8;
   text-shadow:0 3px 14px rgba(0,0,0,.6); }}
.leg b {{ color:#C9AD6E; font-weight:700; }}
.leg-card {{ top:700px; }} .leg-cheia {{ top:1530px; }}
#logo-final {{ position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover; z-index:20; opacity:0; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <audio id="voz" class="clip" src="assets/fala.mp4" data-start="0" data-duration="{FIM_FALA}" data-track-index="5" data-volume="1"></audio>
  <div id="fundo"></div>
  <div id="cheia1" class="cheia"><div id="cheia1in" class="cheiain">
    <video id="v1" class="clip" src="assets/fala.mp4" data-start="0" data-duration="{CARD_INI}" data-media-start="0" data-track-index="1" muted playsinline></video></div></div>
  <div id="cardbox"><div id="cardin">
    <video id="v2" class="clip" src="assets/fala.mp4" data-start="{CARD_INI}" data-duration="{round(CARD_FIM - CARD_INI, 2)}" data-media-start="{CARD_INI}" data-track-index="1" muted playsinline></video></div></div>
  <div id="cheia2" class="cheia"><div id="cheia2in" class="cheiain">
    <video id="v3" class="clip" src="assets/fala.mp4" data-start="{CARD_FIM}" data-duration="{round(LOGO_INI + 0.7 - CARD_FIM, 2)}" data-media-start="{CARD_FIM}" data-track-index="1" muted playsinline></video></div></div>
  {chr(10).join("  " + x for x in L)}
{leg_html}
  <video id="logo-final" class="clip" src="assets/logo_final_lento.mp4" data-start="{LOGO_INI}" data-duration="{LOGO_DUR}" data-track-index="6" muted playsinline></video>
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
{chr(10).join(A)}
  tl.set({{}}, {{}}, {TOTAL});
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
(AQUI / "index.html").write_text(html)
print("cenas ok; legendas:", len(legs), "| duração", TOTAL)
for s, d, h, c in legs:
    print(f"{s:6.2f} {d:4.2f} {'C' if c else 'T'} {re.sub('<[^>]+>', '', h)}")
