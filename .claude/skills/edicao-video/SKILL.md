---
name: edicao-video
description: Processo base de edição de vídeos verticais (Reels/TikTok/Shorts) com HyperFrames, FFmpeg e Whisper em português — receber o vídeo bruto (arquivo ou Google Drive), transcrever, cortar pausas, montar, conferir travadas e entregar. Use sempre que a pessoa mandar um vídeo bruto para editar, pedir corte de pausas, legenda, transcrição, letreiros ou "edita esse vídeo". A identidade visual NÃO está aqui: ela vem da skill da empresa (/phcont ou /doctorfit). Se a mensagem não disser de qual empresa é o vídeo, pergunte antes de editar.
---

# Edição de vídeo: processo base

Esta skill é o **como editar**, igual para todas as empresas. O **visual** (cores, fontes, logo, layout, o que a
cliente aprovou) fica na skill de cada empresa:

| Palavra-chave | Empresa | Skill |
|---|---|---|
| `/phcont` ou "PHcont" | PHcont, Assessoria e Consultoria Contábil | `phcont` |
| `/doctorfit` ou "DoctorFit" | DoctorFit, academia | `doctorfit` |

**Antes de tudo, descubra a empresa.** Se a mensagem não tiver a palavra-chave nem deixar claro de qual empresa é,
pergunte ("Esse vídeo é da PHcont ou da DoctorFit?"). Depois carregue a skill da empresa e siga as duas juntas.
Nunca misture as identidades: as duas marcas são totalmente diferentes, e usar a cor ou a logo de uma no vídeo da
outra é o pior erro possível aqui.

Fale com a pessoa em **português simples** (ela não é técnica): explique o que fez e por quê, sem jargão.

## 1. Preparar o ambiente (uma vez por sessão)

O container é temporário: confira e reinstale o que faltar.

```bash
which ffmpeg                       # já vem instalado
npm install -g hyperframes         # CLI HyperFrames (render HTML → vídeo)
pip install -q -U "yt-dlp[default]"
```

Whisper em português: o HyperFrames compila o whisper.cpp na primeira transcrição, mas o download automático dos
modelos falha (o Node não passa pelo proxy). Baixe com curl:

```bash
mkdir -p ~/.cache/hyperframes/whisper/models && cd ~/.cache/hyperframes/whisper/models
for m in small medium; do curl -sSL --retry 4 -o ggml-$m.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-$m.bin; done
```

## 2. Receber o vídeo

- **Chat:** o limite é ~30 MB; vídeos maiores não sobem.
- **Google Drive (o normal):** baixe com
  `curl -sSL -o bruto/video.mov "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`.
  Confira com `file`: se vier "HTML document" com título "Sign-in", o link está **privado**. Peça para ela mudar em
  Compartilhar → Acesso geral → **"Qualquer pessoa com o link"**. Não tente contornar.
- **YouTube:** bloqueia downloads vindos de servidor ("Sign in to confirm you're not a bot"). Peça o arquivo ou um link do Drive.
- GitHub aceita até 100 MB por arquivo (25 MB pelo site).

Pastas, separadas por empresa: `<empresa>/bruto/`, `<empresa>/trabalho/`, `<empresa>/edicao/`, `<empresa>/final/`
(por exemplo `doctorfit/final/`). Os arquivos da PHcont que já existem na raiz do repositório (`bruto/`, `edicao/`,
`final/`…) são da PHcont.

## 3. Transcrever

```bash
hyperframes transcribe bruto/video.mov --engine whisper --model medium --language pt --json
```

Sem `--language pt` o modelo padrão (`small.en`) **traduz para inglês**. Leia o resultado e corrija palavras grudadas,
nomes de marca e termos técnicos (a skill da empresa lista os erros típicos). Quando não tiver certeza de uma palavra,
pergunte.

## 4. Planejar e aprovar

Monte `trabalho/plano.json` (cortes, telas animadas, legenda) e mostre para aprovação **antes de editar**, em tabelas
curtas. Ela costuma responder curto ("pode mandar", "gostei"). Trate "pode mandar o vídeo" como aprovação e assuma o
padrão da skill da empresa no que ficou em aberto, avisando.

## 5. Cortar pausas e preparar a fala

- Ache os silêncios com `silencedetect=n=-35dB:d=0.3` e corte as pausas (deixe ~0,05 s de margem). Use os tempos do
  silencedetect, não os do Whisper, que erra alguns décimos.
- Ache os cortes entre gravações com `scdet=threshold=10` e anote os tempos (passo 6).
- Gere `edicao/assets/fala.mp4`: trim + concat (com `afade` de ~12 ms em cada emenda), `scale=1080:1920`, `fps=30`,
  `loudnorm=I=-14:TP=-1.5:LRA=11`, `-g 30` (keyframe a cada segundo; sem isso o vídeo congela no render).
- Se o bruto termina numa tela de logo, extraia ela à parte. Ela não entra em `fala.mp4`.
- Transcreva de novo o `fala.mp4` para ter os tempos certos de cada palavra na legenda.

## 6. Montar no HyperFrames

Carregue a skill `hyperframes` (contrato: `class="clip"`, `data-start`, `data-duration`, timelines GSAP pausadas,
sem transform CSS em elemento animado). Comece pelo gerador da skill da empresa, quando existir.

```bash
hyperframes check --json
hyperframes snapshot --at <momentos-chave> --json
hyperframes render --output ../final/<nome>_v1.mp4
```

Boas práticas que valem para qualquer empresa (vieram dos ajustes da cliente):

- **Vibe leve:** entradas suaves (opacidade + poucos px, `power2.out`/`sine.inOut`), trocas por dissolvência. Nada de
  zoom brusco, efeito de mola (`back.out`) ou elementos deslizando pela tela.
- **Gráficos sobem devagar e contínuos** (~2 s), acompanhando a fala.
- **Legenda nunca sobre o tronco** da pessoa.
- **Final calmo:** dissolva para a logo e segure a última tela ~2 s.
- **Cortes entre gravações:** o fim de cada gravação costuma ter a pessoa quase parada. Nunca coloque dissolvência nem
  deslize por cima desse trecho: parece vídeo travando, e às vezes aparecem duas imagens dela. Troque o layout
  **exatamente no quadro do corte**, com a imagem nova entrando a 106% e se acomodando em 100% em 0,7 s.
- Áreas seguras das redes: textos importantes entre x 120–888 e y 288–1248.

## 7. Conferir antes de entregar

- `hyperframes check` sem erros. Snapshots dos momentos-chave: textos sem encostar, nada sobre o rosto.
- Áudio: `ffmpeg -i final.mp4 -af ebur128 -f null -` → integrado ≈ **-14 LUFS**.
- **Travadas:** compare quadro a quadro em volta de cada corte e transição (`tblend=all_mode=difference,signalstats`,
  valor `YAVG` por quadro). Valores perto de 0 no render, quando a fonte tem movimento, são congelamento. Um pico
  isolado é um corte, e precisa coincidir com uma troca de layout.
- Confira que **só** aparecem as cores e a logo da empresa certa.

## 8. Entregar

- Mande o MP4 com `SendUserFile` (`display: render`) e um resumo curto do que mudou.
- Versões numeradas (`_v2`, `_v3`…). A aprovada vira também `_FINAL.mp4`.
- Faça commit e push (ignore `edicao/.hyperframes/`).
- Preferência nova da cliente → anote na skill **da empresa**. Melhoria de processo → anote **nesta** skill.
