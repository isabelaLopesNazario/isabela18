"""Mana, vídeo da live (v3):
- título grande NA FRENTE só durante a vinheta "TV com defeito" (0–1,85 s), depois some;
- zoom leve só nas 2 maiores risadas dele;
- sem memes e sem créditos no final;
- frases engraçadas em destaque (estilo do título) na faixa de baixo;
- bonequinho pensativo com ❓ no "eu não acredito".
Uso: python3 montar_v3.py   (dentro de mana/edicao_video1)"""
import subprocess

SRC = "../bruto/live.mov"
TRECHOS = [(0.0, 27.0), (35.5, 72.75)]
ZOOMS = [(44.0, 47.2), (53.8, 56.4)]          # só as risadas mais fortes
CONT_Y, CONT_H = 474, 972
FACE_X, FACE_Y = 960, 728
ZMAX = 0.28
GLITCH_FIM = 1.85

def out_t(t):
    """tempo da fonte -> tempo no vídeo final (o trecho 27–35,5 foi cortado)"""
    return t if t < 27.0 else t - 8.5

FRASES = [  # (arquivo, início e fim na fonte)
    ("fx/frase_voz.png", 36.15, 37.7),
    ("fx/frase_grava.png", 47.1, 49.6),
    ("fx/frase_juro.png", 67.95, 69.5),
]
BONECO = (49.8, 3.4)

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
    open("filtros_v3_base.txt", "w").write(";\n".join(filtros))
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + entradas + ["-filter_complex_script", "filtros_v3_base.txt",
                    "-map", "[cv]", "-map", "[ao]", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-g", "30",
                    "-c:a", "aac", "-b:a", "192k", "base_v3.mp4"], check=True)

def efeitos():
    ent = ["-i", "base_v3.mp4",
           "-loop", "1", "-t", "3", "-i", "fx/titulo.png",
           "-loop", "1", "-t", "5", "-i", "fx/boneco.png",
           "-loop", "1", "-t", "5", "-i", "fx/interrogacao.png"]
    for f, _, _ in FRASES:
        ent += ["-loop", "1", "-t", "4", "-i", f]
    F = []
    # título grande na frente, tremendo junto com o glitch, só até a TV "parar de falhar"
    F.append("[1:v]format=rgba,fade=t=in:st=0.15:d=0.25:alpha=1[tit]")
    F.append(f"[0:v][tit]overlay=x='if(lt(t,{GLITCH_FIM}),12*sin(t*70),0)':y=780:enable='lt(t,{GLITCH_FIM})':eof_action=pass[x0]")
    ant = "[x0]"
    # frases em destaque na faixa de baixo
    for j, (_, s, e) in enumerate(FRASES):
        T0, T1 = out_t(s), out_t(e)
        F.append(f"[{4 + j}:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,setpts=PTS+{T0}/TB[f{j}]")
        nome = f"[x{j + 1}]"
        F.append(f"{ant}[f{j}]overlay=x=0:y=1500:enable='between(t,{T0},{T1})':eof_action=pass{nome}")
        ant = nome
    # bonequinho pensativo + interrogações
    T, D = out_t(BONECO[0]), BONECO[1]
    F.append(f"[2:v]scale=-1:430,format=rgba,setpts=PTS+{T}/TB[bon]")
    F.append(f"[3:v]scale=110:-1,format=rgba,setpts=PTS+{T}/TB,split=3[qa][qb][qc]")
    bx = f"if(lt(t-{T},0.6),-200+(t-{T})/0.6*640,if(lt(t-{T},{D - 0.5}),440+6*sin((t-{T})*5),440+(t-{T}-{D - 0.5})/0.5*700))"
    F.append(f"{ant}[bon]overlay=x='{bx}':y='1475+4*abs(sin((t-{T})*9))':enable='between(t,{T},{T + D})':eof_action=pass[y0]")
    ant = "[y0]"
    for k2, (lab, (qx, qy, dt)) in enumerate(zip(["[qa]", "[qb]", "[qc]"], [(320, 1490, 0.7), (640, 1470, 1.0), (720, 1590, 1.3)])):
        nome = f"[y{k2 + 1}]"
        F.append(f"{ant}{lab}overlay=x={qx}:y='{qy}-25*abs(sin((t-{T}-{dt})*6))':enable='between(t,{T + dt},{T + D - 0.5})':eof_action=pass{nome}")
        ant = nome
    F.append(f"{ant}format=yuv420p[vout]")
    open("filtros_v3_fx.txt", "w").write(";\n".join(F))
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex_script", "filtros_v3_fx.txt",
                    "-map", "[vout]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-c:a", "copy", "-movflags", "+faststart", "-shortest", "../final/mana_voz_fina_v3.mp4"], check=True)

if __name__ == "__main__":
    base()
    efeitos()
    print("ok")
