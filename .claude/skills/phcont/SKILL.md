---
name: phcont
description: Identidade visual e padrão de edição aprovado da PHcont, Assessoria e Consultoria Contábil — azul-marinho e dourado, apresentadora em tela cheia no começo e no final, tela dividida com animações em cima, gráfico em tela cheia, legenda com destaque dourado e a logo do vídeo bruto no final. Use quando a pessoa escrever /phcont, "PHcont", "PH Cont", ou mandar um vídeo de contabilidade, impostos, planejamento tributário ou da equipe do escritório para editar. Junto com esta, siga o processo da skill edicao-video. NÃO use para a DoctorFit (academia).
---

# PHcont: identidade e padrão aprovado

**Palavra-chave:** `/phcont`. Siga o processo da skill **`edicao-video`** (baixar, transcrever, cortar, conferir,
entregar). Esta skill diz **como o vídeo da PHcont deve ficar**.

Arquivos:
- `scripts/gerar_edicao.py`: gerador da versão aprovada (v10, vídeo "Planejamento tributário"). É o ponto de partida.
  Copie para `edicao/` e troque os tempos (`CHART`, `CENAS`, `data-start` dos vídeos), os textos das cenas e a
  lista `G` da legenda.
- `references/estilo-completo.md`: manual de estilo com o histórico de feedback.
- `assets/logo_branca_transparente.png` (fundo escuro), `assets/logo_marinho_transparente.png` (fundo claro).

Pastas da PHcont no repositório: `bruto/`, `trabalho/`, `edicao/`, `final/`, `estilo/` (na raiz).

## A empresa

Escritório de contabilidade sério e elegante. Os vídeos são de uma funcionária falando para a câmera, de camiseta
preta com a logo, no escritório, sobre impostos, planejamento tributário e dicas para empresários. O final sempre
convida a agendar uma análise ("link aqui embaixo").

Erros típicos de transcrição: "PH Count" → **PHcont**, "Agente de" → **Agende**.

## Layout aprovado

| Trecho | Layout |
|---|---|
| **Começo** (gancho, primeiras frases) | Ela **em tela cheia**, sem animação. Legenda na altura do cinto (y ≈ 1500). |
| **Meio** | **Tela dividida**: animação em cima (conteúdo em y ≈ 200–750, pílula "● PHCONT" em y ≈ 196), legenda entre as metades (y ≈ 762), ela embaixo a partir de y = 860 (vídeo deslocado −420 px: cabeça, ombros e tronco). |
| **Gráfico principal** (o dado mais forte) | **Tela cheia** de animação, barras num cartão. Legenda em y ≈ 1100. |
| **Convite final** | Ela **em tela cheia**, legenda no cinto. |
| **Fim** | Dissolvência de 0,6 s para a **tela da logo do vídeo bruto** (fundo preto, "Link na bio!"), com a entrada na metade da velocidade e ~2 s parada. |

Divisão entre as metades: sem linha grossa. Use um degradê escuro de ~220 px no topo do vídeo, um fio dourado de
2 px a 55% e um brilho leve.

## Telas animadas

Estilo das referências 5 e 6 (`estilo/referencias/ref5_explicador_cartoes.mp4`, `ref6_explicador_lista.mp4`):

- Fundo azul-marinho com brilho no centro, grade em perspectiva embaixo, pontinhos de luz e "vidros" translúcidos andando devagar.
- Título centralizado em **Oswald 700 maiúsculo**, branco com a palavra-chave em **dourado**.
- Cartões escuros translúcidos com cantos arredondados. O item ativo ganha borda dourada com brilho. Listas numeradas
  com quadradinho dourado. Comparação com selo **"VS"** dourado, e o lado negativo em bordô com texto riscado.
- Barra de progresso dourada fina no topo.
- Uma tela por ideia, trocando junto com a fala.

## Legenda

Maiúsculas, Poppins 800, branca com sombra, 2–3 palavras por vez, palavra-chave numa **caixa dourada com texto
azul-marinho**.

## Paleta e fontes

| Cor | Hex | Uso |
|---|---|---|
| Azul-marinho | `#1F2B42`; fundo `#0F1C3A`→`#070D1C` | fundos |
| Bordô | `#7A2A33` (claro `#A33A46`; linha da logo `#831C17`) | lado negativo, etiqueta, ponto da pílula |
| Dourado | `#C9AD6E` (marca `#BBA372`) | destaque de título, legenda, barras, bordas ativas |
| Branco | `#F7F5F6` | texto |
| Texto sobre dourado | `#0B1426` | |

Fontes: Oswald (títulos), Poppins (legenda e cartões).

## O que a cliente aprovou e recusou

1. **Não copiar as capas do feed do Instagram.** Do feed vêm só as cores e a logo. O visual segue as referências de vídeo.
2. **Título centralizado e mais baixo**, nunca colado no topo.
3. **Legenda fora do tronco dela**: entre as metades na tela dividida, no cinto quando ela está em tela cheia.
4. **Ela é a principal** no começo e no convite final. Animação por cima nesses trechos incomoda.
5. **Mostrar mais dela** na tela dividida, não só o rosto.
6. **Vibe leve, gráficos subindo devagar, final calmo e sem travadas nos cortes**: veja as boas práticas da `edicao-video`.
7. **Áudio sem trilha** por padrão (só a voz, a -14 LUFS). Pergunte antes de colocar música.
