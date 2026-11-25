#!/usr/bin/env python3
"""Estúdio 3D: roteiro.json -> vídeo MP4 vertical com bonequinhos, cenários, câmera, legenda, efeitos e música.

Uso:
  python3 estudio3d/gerar.py <pasta-do-roteiro>            # tudo: voz, sincronia, render, mixagem
  python3 estudio3d/gerar.py <pasta> --previa 2,8,15        # só imagens desses segundos (rápido, para conferir)
  python3 estudio3d/gerar.py <pasta> --sem-render           # só monta o projeto e os sons

Formato do roteiro: veja estudio3d/LEIAME.md.
"""
import json, math, os, re, shutil, subprocess, sys, unicodedata, wave
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent
MOTOR = RAIZ / "motor"
HF = ["node", "/root/.claude/skills/hyperframes/scripts/plugin-cli.mjs"]
SR = 44100


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-3000:])
        raise SystemExit(f"falhou: {' '.join(map(str, cmd[:6]))}")
    return r.stdout


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def dur(arq):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)]).strip())


# ------------------------------------------------------------------ narração
def preparar_narracao(R, base, proj):
    N = R["narracao"]
    saida = proj / "assets" / "narracao.wav"
    if N.get("arquivo"):
        src = (base / N["arquivo"]).resolve()
        ini, fim = N.get("inicio", 0), N.get("fim")
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(ini)] + (["-to", str(fim)] if fim else []) + ["-i", str(src), "-vn"]
        filtro = "loudnorm=I=-14:TP=-1.5:LRA=11"
        if fim:
            filtro = f"afade=t=out:st={max(0, fim - ini - 0.2):.2f}:d=0.2," + filtro
        sh(cmd + ["-af", filtro, "-ar", str(SR), "-ac", "2", str(saida)])
    else:  # voz-guia do sistema (rascunho)
        texto = " ".join(re.sub(r"\*", "", c["fala"]) for c in R["cenas"])
        tmp = proj / "assets" / "guia.wav"
        sh(["espeak-ng", "-v", "pt-br", "-s", "150", "-w", str(tmp), texto])
        sh(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af", "loudnorm=I=-14", "-ar", str(SR), "-ac", "2", str(saida)])
    return saida


def transcrever(narr, proj):
    cache = proj / "trabalho_transcricao.json"
    if cache.exists() and cache.stat().st_mtime > narr.stat().st_mtime:
        return json.loads(cache.read_text())
    out = sh(HF + ["transcribe", str(narr), "--engine", "whisper", "--model", "medium", "--language", "pt", "--json"], cwd=proj)
    info = json.loads(out.strip().splitlines()[-1])
    palavras = json.loads(Path(info["transcriptPath"]).read_text())
    Path(info["transcriptPath"]).unlink(missing_ok=True)
    cache.write_text(json.dumps(palavras, ensure_ascii=False))
    return palavras


# ------------------------------------------------------------------ sincronia roteiro x voz
def alinhar(R, palavras, D):
    """Dá a cada palavra do roteiro o tempo da palavra falada correspondente."""
    toks = []  # (cena, texto original, destaque?)
    for ci, c in enumerate(R["cenas"]):
        for w in c.get("fala", "").split():
            dest = w.startswith("*") or w.endswith("*")
            toks.append({"cena": ci, "txt": w.replace("*", ""), "dest": dest})
    a = [norm(t["txt"]) for t in toks]
    b = [norm(p["text"]) for p in palavras]
    sm = SequenceMatcher(None, a, b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            p = palavras[blk.b + k]
            toks[blk.a + k]["t0"], toks[blk.a + k]["t1"] = p["start"], p["end"]
    # aproximação para palavras não encontradas (parecidas ou interpoladas)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "replace" and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                toks[i1 + k]["t0"], toks[i1 + k]["t1"] = palavras[j1 + k]["start"], palavras[j1 + k]["end"]
    conhecidos = [i for i, t in enumerate(toks) if "t0" in t]
    if not conhecidos:
        raise SystemExit("não consegui casar o roteiro com a voz: confira o texto das falas")
    for i, t in enumerate(toks):
        if "t0" in t:
            continue
        ant = max([j for j in conhecidos if j < i], default=None)
        dep = min([j for j in conhecidos if j > i], default=None)
        ta = toks[ant]["t1"] if ant is not None else 0
        tb = toks[dep]["t0"] if dep is not None else D
        na = i - (ant if ant is not None else -1)
        nb = (dep if dep is not None else len(toks)) - (ant if ant is not None else -1)
        t["t0"] = ta + (tb - ta) * (na - 1) / max(1, nb - 1) if nb > 1 else ta
        t["t1"] = t["t0"] + 0.25
    taxa = len(conhecidos) / len(toks)
    print(f"sincronia: {len(conhecidos)}/{len(toks)} palavras casadas ({taxa:.0%})")
    return toks


def resolver(R, toks, D):
    """Converte 'em': 'palavra' / segundos relativos em tempos absolutos."""
    cenas = R["cenas"]
    inicio = []
    for ci in range(len(cenas)):
        ts = [t["t0"] for t in toks if t["cena"] == ci]
        if ci == 0:
            inicio.append(0.0)
        elif ts:
            inicio.append(min(ts) - 0.08)
        else:  # cena sem fala: entra depois da narração
            inicio.append(max(inicio[-1] + 0.5, D + 0.05))
    extra = cenas[-1].get("dur", 2.0) if not cenas[-1]["fala"].strip() else R.get("cauda", 0.6)
    fim_total = max(D, inicio[-1]) + extra
    for ci, c in enumerate(cenas):
        c["t0"] = round(inicio[ci], 3)
        c["t1"] = round(inicio[ci + 1] if ci + 1 < len(cenas) else fim_total, 3)
        ctoks = [t for t in toks if t["cena"] == ci]

        def quando(ref, padrao=None):
            if ref is None:
                return padrao if padrao is not None else c["t0"]
            if isinstance(ref, (int, float)):
                return c["t0"] + ref
            if isinstance(ref, dict):
                return quando(ref.get("em"), padrao) + ref.get("mais", 0)
            if ref == "inicio":
                return c["t0"]
            if ref == "fim":
                return c["t1"] - 0.4
            alvo = norm(ref.split()[0])
            for t in ctoks:
                if norm(t["txt"]) == alvo or (len(alvo) > 3 and norm(t["txt"]).startswith(alvo)):
                    return t["t0"]
            print(f"  aviso: palavra '{ref}' não está na fala da cena {ci + 1}; usei o início")
            return c["t0"]

        for a in c.get("atores", []):
            a["acoes"] = sorted([{"t": round(quando(x.get("em"), c["t0"]) + x.get("mais", 0), 3), "pose": x["pose"]} for x in a.get("acoes", [])], key=lambda x: x["t"])
            if not a["acoes"] or a["acoes"][0]["t"] > c["t0"]:
                a["acoes"].insert(0, {"t": c["t0"] - 1, "pose": a.get("pose", "parado")})
            novo = []
            for w in a.get("andar", []):
                t0 = quando(w.get("em"), c["t0"]) + w.get("mais", 0)
                novo.append({"t0": t0, "t1": t0 + w.get("dur", 1.5), "de": w.get("de", a.get("pos", [0, 0])), "para": w["para"], "rotFinal": w.get("rotFinal", a.get("rot", 0))})
            a["andar"] = novo
        for o in c.get("objetos", []):
            if "entra" in o:
                e = o["entra"] if isinstance(o["entra"], dict) else {"modo": o["entra"]}
                o["entra"] = {"modo": e.get("modo", "surge"), "t": round(quando(e.get("em"), c["t0"]) + e.get("mais", 0), 3), "dur": e.get("dur", 0.45)}
            if "sai" in o:
                s = o["sai"] if isinstance(o["sai"], dict) else {"modo": o["sai"]}
                o["sai"] = {"modo": s.get("modo", "some"), "t": round(quando(s.get("em"), c["t1"] - 0.4) + s.get("mais", 0), 3), "dur": s.get("dur", 0.35)}
            for an in o.get("anim", []):
                an["t"] = round(quando(an.get("em"), c["t0"]) + an.get("mais", 0), 3)
    return cenas


# ------------------------------------------------------------------ legenda
def legendas(toks, R):
    L = R.get("legenda", {})
    if L.get("desligada"):
        return []
    max_p = L.get("palavras", 2)
    grupos, atual = [], []
    for i, t in enumerate(toks):
        atual.append(t)
        prox = toks[i + 1] if i + 1 < len(toks) else None
        pausa = prox and prox["t0"] - t["t1"] > 0.25
        if len(atual) >= max_p or not prox or pausa or prox["cena"] != t["cena"] or re.search(r"[.,?!;:]$", t["txt"]):
            grupos.append(atual); atual = []
    out = []
    for gi, g in enumerate(grupos):
        ini = g[0]["t0"]
        fim = grupos[gi + 1][0]["t0"] if gi + 1 < len(grupos) else g[-1]["t1"] + 0.4
        fim = min(fim, g[-1]["t1"] + 0.6)
        html = " ".join((f"<b>{w['txt'].upper()}</b>" if w["dest"] else w["txt"].upper()) for w in g)
        html = re.sub(r"[,.;:](</b>)?$", r"\1", html)
        out.append((round(ini, 3), round(max(0.2, fim - ini), 3), html))
    return out


# ------------------------------------------------------------------ sons (gerados, sem direitos de terceiros)
def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))


def sfx(nome):
    rng = np.random.default_rng(7)
    if nome == "pop":
        n = int(0.12 * SR); t = np.arange(n) / SR
        f = 500 + 1400 * t / t[-1]
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.04) * 0.6
    if nome == "plim":
        n = int(0.8 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1318 * t) + 0.6 * np.sin(2 * np.pi * 1976 * t) + 0.3 * np.sin(2 * np.pi * 2637 * t)) * env(n, 0.002, 0.22) * 0.28
    if nome == "whoosh":
        n = int(0.45 * SR); t = np.arange(n) / SR
        r = rng.standard_normal(n)
        k = np.exp(-((t - 0.22) / 0.12) ** 2)
        y = np.convolve(r, np.ones(30) / 30, mode="same") * k
        return y / (np.abs(y).max() + 1e-9) * 0.35
    if nome == "baque":
        n = int(0.35 * SR); t = np.arange(n) / SR
        f = 120 * np.exp(-t * 6) + 45
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.09) * 0.8
    if nome == "puff":
        n = int(0.4 * SR)
        r = np.convolve(rng.standard_normal(n), np.ones(60) / 60, mode="same")
        y = r * env(n, 0.01, 0.12)
        return y / (np.abs(y).max() + 1e-9) * 0.4
    if nome == "moeda":
        n = int(0.6 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 2093 * t) + np.sin(2 * np.pi * 2637 * t) * (t > 0.08)) * env(n, 0.001, 0.15) * 0.25
    return np.zeros(10)


def eventos_sonoros(cenas):
    ev = []
    for ci, c in enumerate(cenas):
        if ci > 0:
            ev.append((c["t0"] - 0.15, "whoosh"))
        for o in c.get("objetos", []):
            e = o.get("entra")
            if e:
                if o.get("som"):
                    ev.append((e["t"], o["som"]))
                elif e["modo"] == "surge":
                    ev.append((e["t"], "moeda" if o["tipo"] == "moeda" else "pop"))
                elif e["modo"] == "cai":
                    ev.append((e["t"] + e.get("dur", 0.45) * 0.6, "baque"))
            s = o.get("sai")
            if s:
                ev.append((s["t"], "puff" if s["modo"] == "some" else "baque"))
        for a in c.get("atores", []):
            for x in a.get("acoes", [])[1:]:
                if x["pose"] in ("assustado",):
                    ev.append((x["t"], "baque"))
                if x["pose"] in ("comemora",):
                    ev.append((x["t"], "plim"))
    return ev


def musica(total, bpm=96):
    """Trilha leve gerada aqui (acordes suaves + arpejo), sem direitos de terceiros."""
    n = int(total * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    bat = 60 / bpm
    prog = [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]]  # Cmaj7 Am7 Fmaj7 G7
    comp = 4 * bat
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    for i in range(int(total / comp) + 1):
        ac = prog[i % 4]; ini = int(i * comp * SR); fim = min(n, int((i + 1) * comp * SR) + int(0.3 * SR))
        if ini >= n:
            break
        tt = np.arange(fim - ini) / SR
        e = np.minimum(1, tt / 0.6) * np.minimum(1, (comp + 0.3 - tt) / 0.5).clip(0, 1)
        for m in ac:
            y[ini:fim] += (np.sin(2 * np.pi * hz(m) * tt) + 0.25 * np.sin(2 * np.pi * hz(m) * 2 * tt)) * e * 0.06
        for k in range(8):  # arpejo em colcheias
            a0 = ini + int(k * bat / 2 * SR); a1 = min(n, a0 + int(0.5 * SR))
            if a0 >= n:
                break
            ta = np.arange(a1 - a0) / SR
            y[a0:a1] += np.sin(2 * np.pi * hz(ac[k % 4] + 12) * ta) * np.exp(-ta / 0.18) * 0.05
        b0 = ini; b1 = min(n, ini + int(comp * SR)); tb = np.arange(b1 - b0) / SR  # baixo
        y[b0:b1] += np.sin(2 * np.pi * hz(ac[0] - 24) * tb) * np.exp(-tb / 1.2) * 0.12
    return y


def grava_wav(arq, y):
    y = np.clip(y, -1, 1)
    st = np.stack([y, y], axis=1)
    with wave.open(str(arq), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


# ------------------------------------------------------------------ projeto HyperFrames
def escrever_projeto(R, cenas, legs, proj, D):
    if (proj / "motor").exists():
        shutil.rmtree(proj / "motor")
    shutil.copytree(MOTOR, proj / "motor")
    (proj / "hyperframes.json").write_text(json.dumps({"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}}))
    (proj / "package.json").write_text('{ "name": "estudio3d-projeto", "private": true, "type": "module" }\n')
    (proj / ".gitignore").write_text(".hyperframes/\n*.mp4\n*.wav\n")
    W, H = R.get("largura", 1080), R.get("altura", 1920)
    L = R.get("legenda", {})
    dados = {"largura": W, "altura": H, "duracao": D, "marca": R.get("marca", {}), "cenas": cenas}
    divs = "\n".join(f'      <div id="lg{i}" class="leg clip" data-start="{s}" data-duration="{d}" data-track-index="1">{h}</div>' for i, (s, d, h) in enumerate(legs))
    js = "\n".join(f'      tl.fromTo("#lg{i}", {{ scale: 0.86, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.14, ease: "power2.out" }}, {s});' for i, (s, d, h) in enumerate(legs))
    html = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #cfe3f2; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; }}
      #cena {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; }}
      .leg {{ position: absolute; left: 0; width: {W}px; top: {L.get('topo', 1560)}px; text-align: center; font-family: "Poppins", sans-serif;
        font-weight: 800; font-size: {L.get('tamanho', 78)}px; color: #fff; letter-spacing: .01em;
        -webkit-text-stroke: 11px #0b1426; paint-order: stroke fill; }}
      .leg b {{ color: {L.get('cor_destaque', '#ffd45a')}; font-weight: 800; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="{W}" data-height="{H}">
      <canvas id="cena" class="clip" data-start="0" data-duration="{D}" data-track-index="0" width="{W}" height="{H}"></canvas>
{divs}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{js}
      window.__timelines["main"] = tl;
    </script>
    <script>window.__ROTEIRO = {json.dumps(dados, ensure_ascii=False)};</script>
    <script type="module">
      window.__hf = window.__hf || {{}};
      window.__hf.buildReady = window.__hf.buildReady || {{}};
      window.__hf.buildReady["cena3d"] = (async () => {{
        try {{ await document.fonts.load('900 100px Poppins'); await document.fonts.load('800 100px Poppins'); }} catch (e) {{}}
        await import("./motor/runtime.js");
      }})();
    </script>
  </body>
</html>
"""
    (proj / "index.html").write_text(html)


def final_marca(R, base, proj):
    F = R.get("final")
    if not F:
        return None
    src = (base / F["video"]).resolve()
    card = proj / "assets" / "final.mp4"
    filtro = (f"[0:v]trim={F.get('inicio', 0)}:{F.get('fim', 999)},setpts=PTS-STARTPTS,scale={R.get('largura', 1080)}:{R.get('altura', 1920)},fps=30[c];"
              f"[c]split[a][b];[a]trim=0:{F.get('lento', 0.6)},setpts=2*(PTS-STARTPTS)[a2];[b]trim=start={F.get('lento', 0.6)},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={F.get('segura', 1.4)}[b2];[a2][b2]concat=n=2:v=1:a=0[v]")
    sh(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-filter_complex", filtro, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(card)])
    return card


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    base = Path(sys.argv[1]).resolve()
    args = sys.argv[2:]
    R = json.loads((base / "roteiro.json").read_text())
    proj = base / "projeto"; (proj / "assets").mkdir(parents=True, exist_ok=True)
    saida = base / "saida"; saida.mkdir(exist_ok=True)

    narr = preparar_narracao(R, base, proj)
    D_voz = dur(narr)
    palavras = transcrever(narr, proj)
    toks = alinhar(R, palavras, D_voz)
    cenas = resolver(R, toks, D_voz)
    D = round(cenas[-1]["t1"], 3)
    legs = legendas(toks, R)
    escrever_projeto(R, cenas, legs, proj, D)
    (proj / "linha_do_tempo.json").write_text(json.dumps({"cenas": [{"n": i + 1, "t0": c["t0"], "t1": c["t1"], "fala": c["fala"]} for i, c in enumerate(cenas)]}, ensure_ascii=False, indent=1))
    for i, c in enumerate(cenas):
        print(f"  cena {i + 1:2d}  {c['t0']:6.2f}–{c['t1']:6.2f}  {c['fala'][:60]}")

    if "--previa" in args:
        ts = args[args.index("--previa") + 1]
        out = sh(HF + ["snapshot", "--at", ts, "--json"], cwd=proj)
        m = re.findall(r'"(/[^"]*contact-sheet[^"]*)"', out)
        if m:
            shutil.copy(m[0], saida / "previa.jpg"); print("prévia:", saida / "previa.jpg")
        return
    if "--sem-render" in args:
        return

    # som
    card = final_marca(R, base, proj)
    total = D + (dur(card) - 0.6 if card else 0)
    fx = np.zeros(int((total + 1) * SR))
    for t, nome in eventos_sonoros(cenas):
        s = sfx(nome); i0 = int(max(0, t) * SR); i1 = min(len(fx), i0 + len(s)); fx[i0:i1] += s[: i1 - i0]
    grava_wav(proj / "assets" / "efeitos.wav", fx * R.get("volume_efeitos", 0.8))
    if R.get("musica", True):
        mu = musica(total + 1)
        fade = np.ones_like(mu); nf = int(2.0 * SR); fade[-nf:] = np.linspace(1, 0, nf)
        grava_wav(proj / "assets" / "musica.wav", mu * fade)

    # render da animação (sem áudio)
    print("renderizando a animação…")
    sh(HF + ["render", "--output", str(proj / "anim.mp4")], cwd=proj)

    video = proj / "anim.mp4"
    if card:
        sh(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(card), "-filter_complex",
            f"[0:v]fps=30,format=yuv420p[a];[1:v]fps=30,format=yuv420p[b];[a][b]xfade=transition=fade:duration=0.6:offset={D - 0.6:.3f}[v]",
            "-map", "[v]", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(proj / "anim_final.mp4")])
        video = proj / "anim_final.mp4"
    ent = ["-i", str(video), "-i", str(narr), "-i", str(proj / "assets" / "efeitos.wav")]
    mix = "[1:a]volume=1.0[v];[2:a]volume=1.0[f];"
    n = 2
    if R.get("musica", True):
        ent += ["-i", str(proj / "assets" / "musica.wav")]
        mix += f"[3:a]loudnorm=I={R.get('musica_lufs', -30)}:TP=-6,volume=1.0[m];"
        n = 3
    rot = "[v][f]" + ("[m]" if n == 3 else "")
    mix += f"{rot}amix=inputs={n}:normalize=0:duration=longest,alimiter=limit=0.95[a]"
    final = saida / R.get("nome_saida", "video.mp4")
    sh(["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex", mix, "-map", "0:v", "-map", "[a]", "-t", f"{total:.3f}",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)])
    print("pronto:", final, f"({total:.1f} s)")


if __name__ == "__main__":
    main()
