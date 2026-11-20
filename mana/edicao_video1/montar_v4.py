"""Mana, vídeo da live (v4): título só na vinheta, zoom no rosto dele em 2 momentos
(risada forte e quando ela percebe a voz fina), legenda em todo o vídeo, sem bonequinho e sem memes.
Uso: python3 montar_v4.py   (dentro de mana/edicao_video1)"""
import os, subprocess, textwrap

SRC = "../bruto/live.mov"
TRECHOS = [(0.0, 27.0), (35.5, 72.75)]
ZOOMS = [(44.0, 47.2), (49.7, 52.7)]       # risada forte + "Eu não acredito, ninguém falou nada pra mim"
CONT_Y, CONT_H = 474, 972
FACE_X, FACE_Y = 960, 728
ZMAX = 0.28
GLITCH_FIM = 1.85
FONTE = "fonts/Poppins-ExtraBold.ttf"

def out_t(t):
    return t if t < 27.0 else t - 8.5

def zoom_leve(i, d):
    n = max(1, round(d * 30))
    e = f"min(1,min(in/18,({n}-in)/18))"
    z = f"1+{ZMAX}*({e})*({e})*(3-2*({e}))"
    x = f"max(0,min(iw-iw/zoom,{FACE_X * 2}-iw/zoom/2))"
    y = f"max(0,min(ih-ih/zoom,{FACE_Y * 2}-ih/zoom/2))"
    return (f"[{i}:v]fps=30,crop=1440:1296:0:632,scale=2880:2592,"
            f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s=1080x{CONT_H}:fps=30,pad=1080:1920:0:{CONT_Y}:black")

def base():
    entradas, filtros, rot = [], [], []
    k = 0
    for a, b in TRECHOS:
        cortes = sorted({a, b} | {t for z in ZOOMS for t in z if a < t < b})
        for s, e in zip(cortes, cortes[1:]):
            entradas += ["-ss", f"{s:.3f}", "-t", f"{e - s:.3f}", "-i", SRC]
            zoom = any(z0 <= s and e <= z1 for z0, z1 in ZOOMS)
            v = zoom_leve(k, e - s) if zoom else f"[{k}:v]fps=30,scale=1080:1920"
            filtros += [v + f",setsar=1,format=yuv420p[v{k}]", f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo[a{k}]"]
            rot.append(f"[v{k}][a{k}]")
            k += 1
    filtros.append("".join(rot) + f"concat=n={k}:v=1:a=1[cv][ca]")
    filtros.append("[ca]loudnorm=I=-14:TP=-1.5:LRA=11[ao]")
    open("filtros_v4_base.txt", "w").write(";\n".join(filtros))
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + entradas + ["-filter_complex_script", "filtros_v4_base.txt",
                    "-map", "[cv]", "-map", "[ao]", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-g", "30",
                    "-c:a", "aac", "-b:a", "192k", "base_v4.mp4"], check=True)

def legendas():
    os.makedirs("leg", exist_ok=True)
    out = []
    for j, linha in enumerate(open("legendas.txt", encoding="utf-8").read().strip().splitlines()):
        s, e, txt = linha.split("|", 2)
        s, e = float(s), float(e)
        if 27.0 <= s < 35.5:
            continue
        linhas = textwrap.wrap(txt, 26)
        for k, l in enumerate(linhas):
            f = f"leg/{j:02d}_{k}.txt"
            open(f, "w", encoding="utf-8").write(l)
            y = 1490 + k * 78
            out.append(f"drawtext=fontfile={FONTE}:textfile={f}:expansion=none:fontsize=60:fontcolor=white:"
                       f"borderw=6:bordercolor=black:x=(w-text_w)/2:y={y}:"
                       f"enable='between(t,{out_t(s):.2f},{out_t(min(e, 72.75)):.2f})'")
    return ",".join(out)

def efeitos():
    ent = ["-i", "base_v4.mp4", "-loop", "1", "-t", "3", "-i", "fx/titulo.png"]
    F = ["[1:v]format=rgba,fade=t=in:st=0.15:d=0.25:alpha=1[tit]",
         f"[0:v][tit]overlay=x='if(lt(t,{GLITCH_FIM}),12*sin(t*70),0)':y=780:enable='lt(t,{GLITCH_FIM})':eof_action=pass,"
         + legendas() + ",format=yuv420p[vout]"]
    open("filtros_v4_fx.txt", "w").write(";\n".join(F))
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex_script", "filtros_v4_fx.txt",
                    "-map", "[vout]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-c:a", "copy", "-movflags", "+faststart", "-shortest", "../final/mana_voz_fina_v4.mp4"], check=True)

if __name__ == "__main__":
    base()
    efeitos()
    print("ok")
