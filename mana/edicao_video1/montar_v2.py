"""Mana, vídeo da live (v2): começo original com a vinheta glitch e o título entrando junto,
zoom leve (vai e volta) só em 3 risadas, bonequinho 3D com interrogações no "eu não acredito", memes e créditos.
Uso: python3 montar_v2.py   (dentro de mana/edicao_video1)"""
import subprocess

SRC = "../bruto/live.mov"
TITULO = ["EU ACHANDO QUE TÔ ARRASANDO,", "ENQUANTO TODO MUNDO", "RI DA MINHA VOZ"]
TRECHOS = [(0.0, 27.0), (35.5, 72.75)]
ZOOMS = [(23.2, 26.0), (44.0, 47.2), (53.8, 56.2)]          # só algumas risadas
MEMES = {37.05: ("../memes/meme2.mov", 0.3, 2.3, "crop=1130:1460:72:382"),
         48.0: ("../memes/meme1.mov", 0.0, 1.29, "crop=1032:970:66:592")}
FINAL = ("../memes/meme3.mov", 0.0, 6.7, "crop=600:300:196:570")
SUSTO = 49.95                                              # "Eu não acredito, ninguém falou nada pra mim"
CONT_Y, CONT_H = 474, 972
FACE_X, FACE_Y = 960, 728                                  # rosto dele dentro da área da live (1440x1296)
ZMAX = 0.28                                                # zoom leve: até 1,28x

def pecas():
    out = []
    for a, b in TRECHOS:
        cortes = sorted({a, b} | {t for z in ZOOMS for t in z if a < t < b} | {t for t in MEMES if a < t < b})
        for i in range(len(cortes) - 1):
            s, e = cortes[i], cortes[i + 1]
            out.append(("live", s, e, any(z0 <= s and e <= z1 for z0, z1 in ZOOMS)))
            if e in MEMES:
                out.append(("meme",) + MEMES[e])
    out.append(("meme",) + FINAL)
    return out

def titulo(primeira):
    fs = "fonts/Anton-Regular.ttf"
    # na 1ª peça o título entra durante a vinheta: aparece tremendo e assenta em 1,8 s
    alpha = "alpha='if(lt(t,0.25),0,min(1,(t-0.25)/0.35))':" if primeira else ""
    treme = "+if(lt(t,1.8),9*sin(t*70)*(1.8-t),0)" if primeira else ""
    out = []
    for i, t in enumerate(TITULO):
        cor = "0xFFE14D" if i == 2 else "white"
        out.append(f"drawtext=fontfile={fs}:text='{t}':fontsize=76:fontcolor={cor}:borderw=7:bordercolor=black:"
                   f"{alpha}x='(w-text_w)/2{treme}':y={170 + i * 86}")
    return ",".join(out)

def zoom_leve(i, d):
    n = max(1, round(d * 30))
    e = f"min(1,min(in/18,({n}-in)/18))"                   # sobe em 0,6 s, segura, desce em 0,6 s
    z = f"1+{ZMAX}*({e})*({e})*(3-2*({e}))"                # suavização (smoothstep)
    x = f"max(0,min(iw-iw/zoom,{FACE_X * 2}-iw/zoom/2))"
    y = f"max(0,min(ih-ih/zoom,{FACE_Y * 2}-ih/zoom/2))"
    return (f"[{i}:v]fps=30,crop=1440:1296:0:632,scale=2880:2592,"
            f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s=1080x{CONT_H}:fps=30,pad=1080:1920:0:{CONT_Y}:black")

def montar():
    ps = pecas()
    entradas, filtros, rotulos = [], [], []
    extra = []
    com_titulo = []
    for i, p in enumerate(ps):
        if p[0] == "live":
            _, s, e, zoom = p
            entradas += ["-ss", f"{s:.3f}", "-t", f"{e - s:.3f}", "-i", SRC]
            v = zoom_leve(i, e - s) if zoom else f"[{i}:v]fps=30,scale=1080:1920"
            if s <= SUSTO < e:
                extra.append((i, SUSTO - s))
        else:
            _, f, ma, mb, crop = p
            entradas += ["-ss", f"{ma:.3f}", "-t", f"{mb - ma:.3f}", "-i", f]
            v = (f"[{i}:v]fps=30,{crop},scale=1080:{CONT_H}:force_original_aspect_ratio=decrease,"
                 f"pad=1080:1920:(ow-iw)/2:{CONT_Y}+({CONT_H}-ih)/2:black")
        if p is not ps[-1]:
            filtros.append(v + f",setsar=1[r{i}]")
            com_titulo.append((i, (e - s) if p[0] == "live" else (mb - ma)))
        else:
            filtros.append(v + f",setsar=1,format=yuv420p[b{i}]")
        filtros.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}]")
        rotulos.append((i, f"[a{i}]"))

    # bonequinho 3D (😱) atravessando a tela + interrogações 3D
    n = len(ps)
    entradas += ["-loop", "1", "-t", "60", "-i", "fx/boneco.png", "-loop", "1", "-t", "60", "-i", "fx/interrogacao.png"]
    gi, qi = n, n + 1
    # título (PNG retrô + seleção) sobre cada trecho; no 1º entra com fade e tremendo junto com o glitch
    for k, (i, d) in enumerate(com_titulo):
        ti = n + 2 + k
        entradas += ["-loop", "1", "-t", f"{d:.3f}", "-i", "fx/titulo.png"]
        if i == 0:
            filtros.append(f"[{ti}:v]format=rgba,fade=t=in:st=0.25:d=0.35:alpha=1[t{i}]")
            x = "'if(lt(t,1.8),10*sin(t*70)*(1.8-t),0)'"
        else:
            filtros.append(f"[{ti}:v]format=rgba[t{i}]")
            x = "0"
        filtros.append(f"[r{i}][t{i}]overlay=x={x}:y=150:shortest=1:eof_action=repeat,format=yuv420p[b{i}]")
    finais = {i: f"[b{i}]" for i in range(n)}
    for i, T in extra:
        D = 3.4
        filtros.append(f"[{gi}:v]scale=-1:430,format=rgba[g{i}]")
        filtros.append(f"[{qi}:v]scale=110:-1,format=rgba,split=3[q{i}a][q{i}b][q{i}c]")
        # entra andando da esquerda (0,6 s), para no centro balançando de leve, sai pela direita no fim
        bx = (f"if(lt(t-{T},0.6),-200+(t-{T})/0.6*640,if(lt(t-{T},{D - 0.5}),440+6*sin((t-{T})*5),"
              f"440+(t-{T}-{D - 0.5})/0.5*700))")
        filtros.append(f"[b{i}][g{i}]overlay=x='{bx}':y='1475+4*abs(sin((t-{T})*9))':enable='between(t,{T},{T + D})':shortest=1[c{i}0]")
        pos = [(320, 1490, 0.7), (640, 1470, 1.0), (720, 1590, 1.3)]
        ant = f"[c{i}0]"
        for k, (qx, qy, dt) in enumerate(pos):
            lab = f"[q{i}{'abc'[k]}]"
            nome = f"[c{i}{k + 1}]"
            filtros.append(f"{ant}{lab}overlay=x={qx}:y='{qy}-25*abs(sin((t-{T}-{dt})*6))':enable='between(t,{T + dt},{T + D - 0.5})':shortest=1{nome}")
            ant = nome
        finais[i] = ant

    filtros.append("".join(finais[i] + f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca]")
    filtros.append("[ca]loudnorm=I=-14:TP=-1.5:LRA=11[ao]")
    open("filtros_v2.txt", "w").write(";\n".join(filtros))
    cmd = ["ffmpeg", "-v", "error", "-y"] + entradas + ["-filter_complex_script", "filtros_v2.txt", "-map", "[cv]", "-map", "[ao]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", "../final/mana_voz_fina_v2.mp4"]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    montar()
    print("ok")
