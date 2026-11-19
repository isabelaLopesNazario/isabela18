---
name: edicao-video
description: Processo base de edição de vídeos verticais (Reels/TikTok/Shorts) com HyperFrames, FFmpeg e Whisper em português — receber o vídeo bruto (arquivo ou Google Drive), transcrever, cortar pausas, montar, conferir travadas e entregar. Use sempre que a pessoa mandar um vídeo bruto para editar, pedir corte de pausas, legenda, transcrição, letreiros ou "edita esse vídeo". A identidade visual NÃO está aqui, ela vem da skill da empresa (/phcont ou /doctorfit). Se a mensagem não disser de qual empresa é o vídeo, pergunte antes de editar.
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
sem transform CSS em elemento animado).

**O layout e o jeito de editar são os mesmos para todas as empresas**: tela dividida, gráfico em tela cheia, legenda
entre as metades, transições leves e final calmo (detalhes na skill `phcont`, que foi onde esse padrão foi aprovado).
O que muda de uma empresa para outra é **só cor, logo e o nome na pílula**, e isso vem do `marca.json` de cada
empresa. Por isso existe um gerador único nesta skill:

```bash
cp <esta skill>/scripts/gerar_edicao.py <esta skill>/scripts/marca_referencia.json edicao/
# no gerar_edicao.py: troque os tempos (CHART, CENAS, data-start dos vídeos), os textos das cenas e a lista G da legenda
python3 gerar_edicao.py . <skill da empresa>/marca.json     # ex.: .claude/skills/doctorfit/marca.json
```

O gerador troca todas as cores da paleta de referência pelas da empresa e se recusa a rodar se o `marca.json` ainda
estiver marcado como "a preencher". Copie a logo da empresa para `edicao/assets/` com o nome indicado em `"logo"`.

```bash
hyperframes check --json
hyperframes snapshot --at <momentos-chave> --json
hyperframes render --output ../final/<nome>_v1.mp4
```

Boas práticas que valem para qualquer empresa (vieram dos ajustes da cliente):

- **Cada vídeo com algo novo:** a cliente não quer a mesma receita sempre. A estrutura e a identidade ficam; o estilo das
  telas, os efeitos e os elementos visuais mudam a cada vídeo. Siga a seção "Variar o estilo" e o histórico da skill da
  empresa, e use o catálogo do HyperFrames como fonte de ideias.

- **Vibe leve:** entradas suaves (opacidade + poucos px, `power2.out`/`sine.inOut`), trocas por dissolvência. Nada de
  zoom brusco, efeito de mola (`back.out`) ou elementos deslizando pela tela.
- **Gráficos sobem devagar e contínuos** (~2 s), acompanhando a fala.
- **Legenda nunca sobre o tronco** da pessoa.
- **Final calmo:** dissolva para a logo e segure a última tela ~2 s.
- **Cortes entre gravações:** o fim de cada gravação costuma ter a pessoa quase parada. Nunca coloque dissolvência nem
  deslize por cima desse trecho: parece vídeo travando, e às vezes aparecem duas imagens dela. Troque o layout
  **exatamente no quadro do corte**, com a imagem nova entrando a 106% e se acomodando em 100% em 0,7 s.
- Sem barra de progresso e sem linhas fortes nas divisões: só sombreado suave.
- **Animações lentas e suaves:** a cliente achou as entradas rápidas demais. O gerador multiplica a duração de toda
  entrada por `SUAVIDADE = 1.8` (texto ~0,6–0,9 s, desenhos ~1,5–1,8 s), sem mudar o momento em que cada coisa começa.
  Se escrever cenas à mão, já use durações nesse ritmo.
- Riscar palavra: **linha reta** vermelha/bordô, não em onda.
- Áreas seguras das redes: textos importantes entre x 120–888 e y 288–1248.

### Recorte da pessoa (texto atrás dela, figurinha, círculo)

A cliente gosta de **elementos atrás da pessoa** e de **ela recortada** dentro das animações.

- Instale uma vez por sessão (o download automático falha por causa do CUDA):
  `npm install onnxruntime-node@1.21.1 --onnxruntime-node-install-cuda=skip --prefix "/root/.cache/hyperframes/optional/onnxruntime-node@1.21.1"`
- **Foto parada:** `hyperframes remove-background quadro.png -o recorte.png` gera um PNG transparente em ~1 s. Para
  o "nó" do mapa, use um **círculo com borda branca** recortado do quadro. Fica melhor que figurinha com corte reto.
- **Texto atrás dela em movimento: NUNCA sobreponha o WebM recortado ao vídeo no HyperFrames.** Os dois não batem
  quadro a quadro, e aparece "ela dupla" (uma imagem atrás e outra na frente, com zoom diferente), o que a cliente recusou.
  Faça a abertura **pré-montada no ffmpeg**, quadro a quadro, usando só a máscara do recorte:
  1. Recorte o trecho: `remove-background trecho.mp4 -o ela.webm --quality best`.
  2. Gere PNGs transparentes (1080x1920) do sombreado e de cada palavra com Playwright (`omitBackground: true`); veja o
     modelo `edicao_video2/abertura_textos.js` no repositório.
  3. No ffmpeg: `[webm]alphaextract` vira a máscara; `[video][máscara]alphamerge` vira "ela" com as cores **originais**
     (decodifique o WebM com `-c:v libvpx-vp9` para ler o alpha); então vídeo → sombreado → palavras (com
     `fade ... alpha=1` e `enable=between(t,a,b)`) → "ela" por cima. Exporte `abertura.mp4` com `-g 30`.
  4. No gerador, use `abertura.mp4` como fonte do primeiro trecho em tela cheia (no lugar de `fala.mp4`).
- **Texto atrás dela:** sombreado **azul-marinho** suave no alto (só no fundo, porque ela fica por cima, sem sombra),
  palavras brancas com a palavra-chave em dourado, em uma linha, ~140–170 px, e **só o topo da cabeça** passando na frente.
- **Mapa:** no centro, use um **desenho do tema** (ex.: prédio "SUA EMPRESA"), não o rosto dela num círculo (recusado).

### Capa do Reels (quando pedirem)

PNG 1080x1920. Tudo que importa fica no meio, entre y 240 e 1680, porque a grade do perfil mostra só o recorte 3:4
central. Receita aprovada (vídeo 2 PHcont, `edicao_video2/capa/`): escolha um quadro com ela sorrindo e de boca quase
fechada; use o mesmo quadro desfocado com degradê da marca como fundo e o recorte dela (`remove-background`) por cima;
a pergunta-gancho em duas linhas atrás dela, com **só o topo da cabeça** passando na frente da palavra grande; uma caixa
com o benefício, uma linha de apoio, uma anotação manuscrita e a logo embaixo. Gere com Playwright (`capa/foto.cjs`).

## 7. Conferir antes de entregar

- `hyperframes check` sem erros. Snapshots dos momentos-chave: textos sem encostar, nada sobre o rosto.
- Áudio: `ffmpeg -i final.mp4 -af ebur128 -f null -` → integrado ≈ **-14 LUFS**.
- **Travadas:** compare quadro a quadro em volta de cada corte e transição (`tblend=all_mode=difference,signalstats`,
  valor `YAVG` por quadro). Valores perto de 0 no render, quando a fonte tem movimento, são congelamento. Um pico
  isolado é um corte, e precisa coincidir com uma troca de layout.
- Confira que **só** aparecem as cores e a logo da empresa certa (procure os hex da outra marca nos HTML gerados).

## 8. Entregar

- Mande o MP4 com `SendUserFile` (`display: render`) e um resumo curto do que mudou.
- Versões numeradas (`_v2`, `_v3`…). A aprovada vira também `_FINAL.mp4`.
- Faça commit e push (ignore `edicao/.hyperframes/`).
- Preferência nova da cliente → anote na skill **da empresa**. Melhoria de processo → anote **nesta** skill.
