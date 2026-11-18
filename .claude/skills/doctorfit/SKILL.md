---
name: doctorfit
description: Identidade da DoctorFit (academia) para editar vídeos verticais no mesmo padrão de edição já aprovado (tela dividida, legenda, transições leves, final calmo) com o visual editorial da academia, e para criar carrosséis do Instagram (1080x1350) no mesmo estilo. Use quando a pessoa escrever /doctorfit, "DoctorFit", "Doctor Fit", ou mandar um vídeo de academia, treino, musculação ou saúde para editar, ou pedir um carrossel/post para a academia. Junto com esta, siga o processo da skill edicao-video. NÃO use para a PHcont (contabilidade) e nunca use as cores ou a logo da PHcont aqui.
---

# DoctorFit: identidade da academia

**Palavra-chave:** `/doctorfit`.

**O jeito de editar é o mesmo da PHcont**: siga a skill **`edicao-video`** (processo e gerador) e o layout aprovado
descrito na skill **`phcont`** (ela em tela cheia no começo e no convite final, tela dividida no meio, gráfico em tela
cheia, legenda fora do tronco, transições leves, final calmo com a logo).

**O que muda é só a marca**: as cores, a logo e o nome na pílula vêm do `marca.json` desta skill. Nunca use as cores,
a logo nem o nome da PHcont num vídeo da DoctorFit.

Pastas da DoctorFit no repositório: `doctorfit/bruto/`, `doctorfit/trabalho/`, `doctorfit/edicao/`,
`doctorfit/final/`, `doctorfit/estilo/`.

## Identidade (preenchida a partir da logo, do feed e das amostras da cliente)

Material salvo em `doctorfit/estilo/` (logo original, feed, referências e `previa_cores.png`). A logo com fundo
transparente está em `assets/logo_transparente.png`. No projeto, copie para `edicao/assets/logo_doctorfit.png`.

**Visual da marca:** fundo preto/grafite, **verde-limão neon** como destaque, texto branco. Os títulos do feed são em
letra condensada **em itálico** e caixa-alta (branco + palavra-chave em limão), com um tracinho limão embaixo e curvas
limão decorativas. O tom é energético e motivacional ("MotivAÇÃO, DedicAÇÃO…", "ON foco / OFF desculpas").

| Cor | Hex | De onde veio | Uso |
|---|---|---|---|
| Verde-limão | `#CCF200` | feed (logo `#D0EC5C`) | destaque: títulos, caixa da legenda, barras, bordas ativas, barra de progresso |
| Preto | `#0C0C0C` | feed | texto sobre o limão, base dos fundos |
| Branco | `#F8F8F8` | logo | texto principal |
| Verde-escuro | `#447038` | amostra da cliente | cor de apoio da marca (reserva; o fundo editorial atual é grafite) |
| Verde | `#50B434` | amostra da cliente | cor de apoio da marca (reserva) |
| Vermelho | `#D63A3A` | referência ON/OFF | lado negativo das comparações (o "OFF") |

## Visual das telas animadas no vídeo (estrutura igual à PHcont, visual editorial)

A cliente escolheu **a mesma estrutura da PHcont** (tela dividida com a animação em cima e ela embaixo, gráfico em tela
cheia etc.), mas com o visual das referências editoriais em `doctorfit/estilo/referencias/ed_*.jpg`:

- **Fundo:** grafite com brilho suave, **granulado de filme** e **curvas grossas em verde-limão** saindo das bordas.
  Sem grade, sem estrelas e sem vidros flutuando, que eram coisa da PHcont.
- **Etiqueta do topo:** microtexto editorial "**//** DOCTORFIT", com as barras em limão. Não é pílula.
- **Títulos:** condensados retos em caixa-alta (Oswald 700) com a **palavra-chave em serifada itálica limão**
  (Playfair Display), como em "NÃO É SÓ *correr*" e "A arte de *recalcular*".
- **Cartões de vidro fosco** (translúcidos com desfoque), borda limão no item ativo.
- **Legenda:** caixa limão com texto preto.

Tudo isso já está no `css_extra` do `marca.json`. O gerador da `edicao-video` aplica sozinho.
Prévia aprovável: `doctorfit/estilo/previa_cores.png` (versão 1) e a prévia editorial gerada a partir deste `marca.json`.

## Carrossel do Instagram

Gerador: `scripts/gerar_carrossel.py <roteiro.json> <pasta de saída>`. Ele cria PNGs 1080x1350 prontos para postar. O
formato do roteiro está no topo do script. Tipos de slide:

| Tipo | Uso | Visual |
|---|---|---|
| `capa` | 1º slide, o gancho | foto em tela cheia, título enorme (150 px), rótulo "// TEMA", tracinho limão, rodapé editorial com 3 palavras separadas por linhas finas |
| `texto` | slides do meio | foto mais escurecida (ou fundo grafite), título médio e texto; `"vidro": true` põe o bloco num cartão de vidro fosco |
| `cta` | último slide | título e botão limão "AGENDE SUA AULA EXPERIMENTAL! ›" |

Marcação no texto: `*palavra*` = serifada itálica limão; `!palavra!` = condensada limão; `**palavra**` = negrito limão
no texto corrido. Todo slide leva a logo no canto superior esquerdo, a numeração "01/08" à direita e uma curva limão.

Fluxo: peça à pessoa o **tema ou o texto** e as **fotos reais da academia** (alunos, professores, equipamentos). Não
use fotos de banco nem as imagens de referência num post de verdade. Escreva o roteiro (6–8 slides: capa → problema →
explicação → prova/benefício → CTA), mostre os textos para aprovar e só depois gere. Entregue as imagens com
`SendUserFile` e salve em `doctorfit/final/carrosseis/<tema>/`.

Referências de carrossel: o feed da academia (`doctorfit/estilo/marca/feed_instagram.png`) e as `ed_*.jpg`.

**A confirmar com a cliente:** se a tela final usa a logo do próprio vídeo bruto (como na PHcont) ou uma vinheta
animada da logo sobre o fundo preto, e qual é a chamada final padrão (o feed usa "Agende sua aula experimental!").

## Preferências da cliente para a DoctorFit

(Vazio por enquanto. Anote aqui cada ajuste pedido para a academia e o porquê.)
