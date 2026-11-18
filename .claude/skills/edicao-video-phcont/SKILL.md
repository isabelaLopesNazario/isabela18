---
name: edicao-video-phcont
description: Edita vídeos verticais (Reels/TikTok/Shorts) da PHcont Assessoria e Consultoria Contábil no padrão aprovado pela cliente — apresentadora falando, tela dividida com animações em cima (fundo azul-marinho, títulos condensados, cartões dourados), gráfico em tela cheia, legenda palavra a palavra com destaque dourado e a logo do vídeo bruto no final. Use sempre que a pessoa mandar um vídeo bruto (arquivo, link do Google Drive) para editar, pedir corte de pausas, legenda, transcrição, letreiros, "edita esse vídeo", "faz igual ao último", ou mencionar PHcont, PH Cont, contabilidade, planejamento tributário em vídeo — mesmo que não diga "skill" nem "PHcont".
---

# Edição de vídeo PHcont

Fluxo completo, do vídeo bruto ao MP4 final, no estilo que a cliente aprovou depois de 10 versões.
Fale com a pessoa em **português simples** (ela não é técnica): explique o que fez e por quê, sem jargão.

Arquivos desta skill:
- `scripts/gerar_edicao.py` — gerador da edição aprovada (projeto HyperFrames completo). É o ponto de partida de todo vídeo novo.
- `references/estilo-completo.md` — o manual de estilo inteiro, com o histórico de feedback. Leia quando precisar de detalhe visual.
- `assets/logo_branca_transparente.png`, `assets/logo_marinho_transparente.png` — logos com fundo transparente.

## 1. Preparar o ambiente (uma vez por sessão)

O container é temporário: confira e reinstale o que faltar.

```bash
which ffmpeg                       # já vem instalado
npm install -g hyperframes         # CLI HyperFrames (render HTML → vídeo)
pip install -q -U "yt-dlp[default]"
```

Whisper em português: o HyperFrames compila o whisper.cpp na primeira transcrição, mas o download automático
dos modelos falha (o Node não passa pelo proxy). Baixe com curl:

```bash
mkdir -p ~/.cache/hyperframes/whisper/models && cd ~/.cache/hyperframes/whisper/models
for m in small medium; do curl -sSL --retry 4 -o ggml-$m.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-$m.bin; done
```

Se `hyperframes transcribe` reclamar do runtime, rode uma vez qualquer transcrição curta para ele compilar.

## 2. Receber o vídeo

- **Chat:** o limite é ~30 MB; vídeos maiores não sobem.
- **Google Drive (o normal):** baixe com
  `curl -sSL -o bruto/video.mov "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`.
  Confira com `file`: se vier "HTML document" com título "Sign-in", o link está **privado**. Peça para ela mudar
  em Compartilhar → Acesso geral → **"Qualquer pessoa com o link"**. Não tente contornar.
- **YouTube:** bloqueia downloads vindos de servidor ("Sign in to confirm you're not a bot"). Peça o arquivo ou link do Drive.
- GitHub aceita até 100 MB por arquivo (25 MB pelo site). Vídeos > 50 MB geram aviso, mas sobem.

Estrutura do repositório: `bruto/` (originais), `estilo/` (manual e referências), `trabalho/` (transcrição e plano),
`edicao/` (projeto HyperFrames), `final/` (vídeos prontos).

## 3. Transcrever

```bash
hyperframes transcribe bruto/video.mov --engine whisper --model medium --language pt --json
```

Sem `--language pt` o modelo padrão (`small.en`) **traduz para inglês**. O resultado (`transcript.json`, palavra a palavra com
início e fim) vai para a pasta do projeto atual; mova para `trabalho/`. Leia e corrija erros típicos:
"PH Count" → **PHcont**, palavras grudadas ("Ereinvestir"), "Agente de" → "Agende". Quando não tiver certeza
de uma palavra, pergunte.

## 4. Planejar e aprovar

Monte `trabalho/plano.json` (cortes, telas animadas, legenda) e **mostre para aprovação antes de editar**, em tabelas
curtas: o que corta, o que aparece em cada trecho. Ela costuma responder curto ("pode mandar", "gostei"); trate
"pode mandar o vídeo" como aprovação e assuma o padrão desta skill no que ficou em aberto, avisando.

## 5. Cortar pausas e preparar a fala

- Ache silêncios com `silencedetect=n=-35dB:d=0.3` e corte todos (o estilo não tem respiros), deixando ~0,05 s de margem.
- Use os tempos do silencedetect, não os do Whisper (o Whisper erra alguns décimos).
- Ache os cortes entre gravações com `scdet=threshold=10` e anote os tempos: eles importam no passo 6.
- Gere `edicao/assets/fala.mp4`: trim + concat (com `afade` de ~12 ms em cada emenda para não estalar), `scale=1080:1920`,
  `fps=30`, `loudnorm=I=-14:TP=-1.5:LRA=11`, `-g 30` (keyframe a cada segundo; sem isso o vídeo congela no render).
- **Não inclua a tela da logo do bruto** em `fala.mp4`: extraia ela à parte (passo 6).
- Transcreva de novo o `fala.mp4` para ter os tempos certos de cada palavra na legenda.

## 6. Montar a edição (HyperFrames)

Copie `scripts/gerar_edicao.py` para `edicao/` e adapte os dados do vídeo novo: os tempos (`CHART`, `CENAS`, os
`data-start` dos vídeos), os textos de cada cena e a lista `G` da legenda. Depois:

```bash
python3 gerar_edicao.py .                         # escreve index.html e compositions/
hyperframes check --json                          # corrija todo erro; avalie os avisos
hyperframes snapshot --at 1.5,6,12,18,22 --json   # olhe as imagens antes de renderizar
hyperframes render --output ../final/<nome>.mp4
```

Antes de renderizar, carregue a skill `hyperframes` (contrato da composição: `class="clip"`, `data-start`,
`data-duration`, timelines GSAP pausadas e sem transform CSS em elemento animado).

### O layout aprovado

| Trecho | Layout |
|---|---|
| **Começo** (gancho, primeiras frases) | Ela **em tela cheia**, sem animação. Legenda na altura do cinto (y ≈ 1500). |
| **Meio** | **Tela dividida**: animação em cima (conteúdo em y ≈ 200–750, etiqueta "● PHCONT" em y ≈ 196), legenda entre as metades (y ≈ 762), ela embaixo a partir de y = 860 (vídeo deslocado −420 px para mostrar cabeça, ombros e tronco). |
| **Gráfico principal** (o dado mais forte do vídeo) | **Tela cheia** de animação, barras dentro de um cartão. Legenda em y ≈ 1100. |
| **Convite final** ("agende…", "link aqui embaixo") | Ela **em tela cheia** de novo, legenda no cinto. |
| **Fim** | Dissolvência de 0,6 s para a **tela da logo do vídeo bruto**: a entrada desacelerada (metade da velocidade) e "Link na bio!" parado ~2 s. |

Divisão entre as metades: **sem linha grossa**. Use um degradê escuro (≈ 220 px) no topo do vídeo, um fio dourado
de 2 px a 55% e um brilho leve.

### Telas animadas (estilo das refs. 5 e 6, em `estilo/referencias/`)

- Fundo azul-marinho com brilho no centro, grade em perspectiva embaixo, pontinhos de luz e "vidros" translúcidos andando devagar.
- Título centralizado em **Oswald 700 maiúsculo**, branco com a palavra-chave em **dourado**.
- Cartões escuros translúcidos com cantos arredondados. O item ativo ganha borda dourada com brilho. Listas numeradas
  com quadradinho dourado. Comparações com selo **"VS"** dourado, e o lado negativo em bordô (texto riscado).
- Barra de progresso dourada fina no topo.
- Uma tela por ideia, trocando junto com a fala (2–4 s cada).

### Legenda

Maiúsculas, Poppins 800, branca com sombra, 2–3 palavras por vez, palavra-chave numa **caixa dourada com texto
azul-marinho**. Entra com fade + 10 px de subida em 0,14 s.

### Paleta e fontes

| Cor | Hex | Uso |
|---|---|---|
| Azul-marinho | `#1F2B42` / fundo `#0F1C3A`→`#070D1C` | fundos |
| Bordô | `#7A2A33` (claro `#A33A46`) | lado negativo, etiqueta, ponto da pílula |
| Dourado | `#C9AD6E` (marca `#BBA372`) | destaque de título, legenda, barras, bordas ativas |
| Branco | `#F7F5F6` | texto |
| Texto sobre dourado | `#0B1426` | |

Fontes: Oswald (títulos), Poppins (legenda e cartões). As duas já vêm no HyperFrames.

## 7. O que a cliente aprovou e recusou (não repetir os erros)

Cada item veio de um pedido dela. Entender o porquê ajuda a decidir casos novos.

1. **Não copiar as capas do feed do Instagram.** Do feed vêm só as cores e a logo. O visual segue as referências de vídeo.
2. **Título mais centralizado e mais baixo**, nunca colado no topo.
3. **Legenda nunca sobre o tronco dela.** Na tela dividida, a legenda fica entre as metades. Com ela em tela cheia, fica no cinto.
4. **Ela é a principal no começo e no convite final.** Animação por cima nesses trechos incomoda.
5. **Vibe leve.** Nada de zoom brusco no rosto, efeito de mola (`back.out`), "impulso" ou elementos deslizando pela
   tela. Use entradas suaves (opacidade + poucos px, `power2.out`/`sine.inOut`) e trocas por dissolvência.
6. **Gráficos sobem devagar e contínuos** (~2 s, `sine.inOut`), acompanhando a fala.
7. **Mostrar mais dela** na tela dividida (cabeça, ombros e tronco), não só o rosto.
8. **Final calmo:** nada de corte seco para a logo. Dissolva, desacelere a entrada da logo e segure no fim.
9. **Travadas nos cortes entre gravações:** o fim de cada gravação costuma ter ela quase parada. Nunca coloque
   dissolvência nem deslize por cima desse trecho: parece vídeo travando, e às vezes aparecem duas imagens dela.
   Encerre a tela animada um pouco antes e troque o layout **exatamente no quadro do corte**, com a imagem nova
   entrando a 106% e se acomodando em 100% em 0,7 s.

## 8. Conferir antes de entregar

- `hyperframes check` sem erros.
- Snapshots dos momentos-chave: textos sem encostar, nada sobre o rosto.
- Áudio: `ffmpeg -i final.mp4 -af ebur128 -f null -` → integrado ≈ **-14 LUFS**.
- **Travadas:** compare quadro a quadro em volta de cada corte e transição
  (`tblend=all_mode=difference,signalstats`, valor `YAVG` por quadro). Uma sequência de valores perto de 0 no
  render, quando a fonte tem movimento, é congelamento. Um pico isolado é corte, e precisa coincidir com uma troca de layout.
- Áreas seguras: título e cartões entre x 120–888 e y 288–1248. O `check` avisa.

## 9. Entregar

- Mande o MP4 com `SendUserFile` (`display: render`) e um resumo curto do que mudou.
- Versões numeradas em `final/` (`_v2`, `_v3`…). A aprovada vira também `_FINAL.mp4`.
- Faça commit e push de `edicao/`, `final/`, `trabalho/` e `estilo/` (ignore `edicao/.hyperframes/`).
- Atualize `estilo/ESTILO.md` com qualquer preferência nova que ela der.
