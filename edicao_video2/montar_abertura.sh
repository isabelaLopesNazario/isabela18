#!/bin/bash
# Monta a abertura quadro a quadro: vídeo -> sombreado -> palavras -> ela (máscara do recorte, cores originais).
# Uso: ./montar_abertura.sh   (gera os PNGs com abertura_textos.js e escreve assets/abertura.mp4)
set -e
T=$(mktemp -d)
node abertura_textos.cjs "$T"
ffmpeg -v error -y -i assets/fala.mp4 -c:v libvpx-vp9 -i assets/ela_gancho.webm \
  -loop 1 -i "$T/sombra.png" -loop 1 -i "$T/t1.png" -loop 1 -i "$T/t2.png" -loop 1 -i "$T/t3.png" -filter_complex "\
[1:v]alphaextract,format=gray,boxblur=1:1[m];\
[0:v]split[base][src];\
[src][m]alphamerge,format=yuva420p[ela];\
[2:v]format=rgba,fade=t=in:st=0.4:d=0.8:alpha=1[sh];\
[3:v]format=rgba,fade=t=in:st=0.55:d=0.6:alpha=1,fade=t=out:st=2.2:d=0.25:alpha=1[a];\
[4:v]format=rgba,fade=t=in:st=2.45:d=0.55:alpha=1,fade=t=out:st=4.0:d=0.25:alpha=1[b];\
[5:v]format=rgba,fade=t=in:st=4.25:d=0.55:alpha=1[c];\
[base][sh]overlay=enable='lt(t,5.7)':eof_action=pass[x1];\
[x1][a]overlay=enable='between(t,0.55,2.45)'[x2];\
[x2][b]overlay=enable='between(t,2.45,4.25)'[x3];\
[x3][c]overlay=enable='between(t,4.25,5.7)'[x4];\
[x4][ela]overlay=enable='lt(t,5.66)':eof_action=pass,trim=0:5.7,setpts=PTS-STARTPTS[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 -g 30 -pix_fmt yuv420p -r 30 assets/abertura.mp4
rm -rf "$T"
