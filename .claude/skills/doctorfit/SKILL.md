---
name: doctorfit
description: Cores, logo e identidade da DoctorFit (academia) para editar vídeos verticais no mesmo padrão de edição já aprovado (tela dividida, legenda, transições leves, final calmo), só que com a marca da academia. Use quando a pessoa escrever /doctorfit, "DoctorFit", "Doctor Fit", ou mandar um vídeo de academia, treino, musculação ou saúde para editar. Junto com esta, siga o processo da skill edicao-video. NÃO use para a PHcont (contabilidade) e nunca use as cores ou a logo da PHcont aqui.
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
| Verde-escuro | `#447038` | amostra da cliente | tom do brilho no centro do fundo (`fundo_centro` `#1D2A18`) |
| Verde | `#50B434` | amostra da cliente | grade em perspectiva do fundo |
| Vermelho | `#D63A3A` | referência ON/OFF | lado negativo das comparações (o "OFF") |

Fontes: títulos em Oswald 700 **itálico** (`css_extra` no `marca.json`), legenda e cartões em Poppins.

Tudo isso está no `marca.json`. O gerador da `edicao-video` aplica sozinho.

**A confirmar com a cliente:** se a tela final usa a logo do próprio vídeo bruto (como na PHcont) ou uma vinheta
animada da logo sobre o fundo preto, e qual é a chamada final padrão (o feed usa "Agende sua aula experimental!").

## Preferências da cliente para a DoctorFit

(Vazio por enquanto. Anote aqui cada ajuste pedido para a academia e o porquê.)
