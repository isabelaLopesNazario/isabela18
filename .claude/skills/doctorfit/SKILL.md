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

## Status: identidade ainda não preenchida

O `marca.json` está marcado com `"_a_preencher"`, e o gerador se recusa a rodar enquanto isso existir. Antes do
primeiro vídeo, peça à pessoa:
1. **A logo** (PNG, de preferência com fundo transparente).
2. **As cores** da marca, se souber os códigos. Se não souber, tire da logo e do feed.
3. **Print do feed do Instagram** da DoctorFit.

Com o material em mãos:
- Tire a paleta amostrando pixels da logo e do feed, como foi feito para a PHcont.
- Faça a logo com fundo transparente (quando vier sobre fundo preto: alpha = máximo dos canais RGB). Salve em
  `assets/` desta skill e em `doctorfit/estilo/marca/`.
- Preencha **todas** as chaves de cor do `marca.json`, mapeando pelo papel de cada cor:

| Chave | Papel no vídeo |
|---|---|
| `destaque` | cor de destaque: palavra-chave do título, caixa da legenda, barras e bordas ativas, barra de progresso |
| `texto_sobre_destaque` | texto dentro da caixa de destaque (precisa de bom contraste com `destaque`) |
| `negativo`, `negativo_claro`, `negativo_texto` | lado "ruim" das comparações (VS), etiqueta, ponto da pílula |
| `texto` | texto principal (normalmente branco) |
| `fundo_centro`, `fundo_meio`, `fundo_borda` | degradê do fundo das telas animadas (do centro para a borda) |
| `escuro`, `cartao`, `pilula_fundo` | sombra da divisão, fundo dos cartões e da pílula (tons bem escuros da cor de fundo) |
| `grade`, `estrela`, `vidro` | detalhes do fundo: grade em perspectiva, pontinhos de luz, vidros translúcidos |

- Mostre à pessoa uma prévia (snapshot de uma tela animada e de uma tela dividida) para aprovar as cores.
- Remova a chave `"_a_preencher"` e atualize esta seção com a paleta aprovada.

Se a DoctorFit tiver uma tela de logo no fim do vídeo bruto, use ela como na PHcont (desacelerada e parada ~2 s).
Se não tiver, faça a logo surgir com uma dissolvência suave sobre o fundo da marca.

## Preferências da cliente para a DoctorFit

(Vazio por enquanto. Anote aqui cada ajuste pedido para a academia e o porquê.)
