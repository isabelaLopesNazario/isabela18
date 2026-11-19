"""Monta o vídeo da live (Mana): cortes, zoom no rosto dele a cada risada, memes e título fixo.
Uso: python3 montar.py   (roda dentro de mana/edicao_video1)"""
import subprocess, json

SRC = "../bruto/live.mov"
TITULO = ["EU ACHANDO QUE TÔ ARRASANDO,", "ENQUANTO TODO MUNDO", "RI DA MINHA VOZ"]

# trechos da live mantidos (tempo da fonte)
TRECHOS = [(1.9, 27.0), (35.5, 72.75)]
# risadas dele: zoom no rosto
ZOOMS = [(19.6, 21.0), (23.2, 26.0), (41.2, 43.1), (44.0, 47.2), (53.8, 56.2), (58.5, 60.0), (64.3, 66.8)]
# memes inseridos depois do instante (fonte) indicado
MEMES = {37.05: ("../memes/meme2.mov", 0.3, 2.3, "crop=1130:1460:72:382"),   # cachorro debochado após "Eu curto sua voz, né?"
         48.0: ("../memes/meme1.mov", 0.0, 1.29, "crop=1032:970:66:592")}    # plateia rindo após "alguém grava isso aí"
FINAL = ("../memes/meme3.mov", 0.0, 6.7, "crop=600:300:196:570")              # créditos no fim

# quadro da live: 1440x2560 com a imagem em y 632–1928 → saída 1080x1920 com a imagem em y 474–1446
CONT_Y, CONT_H = 474, 972
ZOOM_CROP = "crop=846:762:537:979"   # ~1,7x no rosto dele (painel da direita)

def pecas():
    """Lista de peças em ordem: ('live', a, b, zoom?) ou ('meme', arquivo, a, b, crop)."""
    out = []
    for a, b in TRECHOS:
        cortes = sorted({a, b} | {t for z in ZOOMS for t in z if a < t < b} | {t for t in MEMES if a < t < b})
        for i in range(len(cortes) - 1):
            s, e = cortes[i], cortes[i + 1]
            zoom = any(z0 <= s and e <= z1 for z0, z1 in ZOOMS)
            out.append(("live", s, e, zoom))
            if e in MEMES:
                f, ma, mb, crop = MEMES[e]
                out.append(("meme", f, ma, mb, crop))
    out.append(("meme",) + FINAL)
    return out

def titulo_filtro():
    fs = "fonts/Anton-Regular.ttf"
    linhas = []
    for i, t in enumerate(TITULO):
        y = 170 + i * 86
        cor = "0xFFE14D" if i == 2 else "white"
        linhas.append(f"drawtext=fontfile={fs}:text='{t}':fontsize=76:fontcolor={cor}:borderw=7:bordercolor=black:x=(w-text_w)/2:y={y}")
    return ",".join(linhas)

def montar():
    ps = pecas()
    entradas, filtros, rotulos = [], [], []
    for i, p in enumerate(ps):
        if p[0] == "live":
            _, s, e, zoom = p
            entradas += ["-ss", f"{s:.3f}", "-t", f"{e - s:.3f}", "-i", SRC]
            if zoom:
                v = f"[{i}:v]fps=30,{ZOOM_CROP},scale=1080:{CONT_H},pad=1080:1920:0:{CONT_Y}:black"
            else:
                v = f"[{i}:v]fps=30,scale=1080:1920"
            a = f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo"
        else:
            _, f, ma, mb, crop = p
            entradas += ["-ss", f"{ma:.3f}", "-t", f"{mb - ma:.3f}", "-i", f]
            v = (f"[{i}:v]fps=30,{crop},scale=1080:{CONT_H}:force_original_aspect_ratio=decrease,"
                 f"pad=1080:1920:(ow-iw)/2:{CONT_Y}+({CONT_H}-ih)/2:black")
            a = f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo"
        final = (p is ps[-1])
        if not final:
            v += "," + titulo_filtro()
        filtros += [v + f",setsar=1,format=yuv420p[v{i}]", a + f"[a{i}]"]
        rotulos.append(f"[v{i}][a{i}]")
    filtros.append("".join(rotulos) + f"concat=n={len(ps)}:v=1:a=1[cv][ca]")
    filtros.append("[ca]loudnorm=I=-14:TP=-1.5:LRA=11[ao]")
    open("filtros.txt", "w").write(";\n".join(filtros))
    cmd = ["ffmpeg", "-v", "error", "-y"] + entradas + ["-filter_complex_script", "filtros.txt", "-map", "[cv]", "-map", "[ao]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", "../final/mana_voz_fina_v1.mp4"]
    subprocess.run(cmd, check=True)
    json.dump([list(map(str, p)) for p in ps], open("pecas.json", "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    montar()
    print("ok")
