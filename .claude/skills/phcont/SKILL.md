---
name: phcont
description: Identidade visual e padrão de edição aprovado da PHcont, Assessoria e Consultoria Contábil — azul-marinho e dourado, apresentadora em tela cheia no começo e no final, tela dividida com animações em cima, gráfico em tela cheia, legenda com destaque dourado e a logo do vídeo bruto no final. Use quando a pessoa escrever /phcont, "PHcont", "PH Cont", ou mandar um vídeo de contabilidade, impostos, planejamento tributário ou da equipe do escritório para editar. Junto com esta, siga o processo da skill edicao-video. NÃO use para a DoctorFit (academia).
---

# PHcont: identidade e padrão aprovado

O layout descrito aqui é **o padrão de edição de todas as empresas**. A DoctorFit usa o mesmo layout, com as cores
e a logo dela.

**Palavra-chave:** `/phcont`. Siga o processo da skill **`edicao-video`** (baixar, transcrever, cortar, conferir,
entregar). Esta skill diz **como o vídeo da PHcont deve ficar**.

Arquivos:
- `marca.json`: cores, logo e texto da pílula da PHcont. Use com o gerador da skill `edicao-video`
  (`python3 gerar_edicao.py . .claude/skills/phcont/marca.json`). Essa é a paleta de referência do gerador.
- `references/estilo-completo.md`: manual de estilo com o histórico de feedback.
- `assets/logo_branca_transparente.png` (fundo escuro), `assets/logo_marinho_transparente.png` (fundo claro).
  No projeto, a logo branca vai em `edicao/assets/logo_branca.png`.

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
| **Meio** | **Tela dividida, com ela como centro da atenção**: faixa animada **menor, no alto** (0–700; conteúdo em y ≈ 200–590), legenda entre as metades (y ≈ 612), ela embaixo a partir de **y = 700** (vídeo deslocado −450 px), ocupando quase 2/3 da tela. No gerador: `SPLIT_TOP = 700`, `SOBE = 0`, `#cam video { top: -450px }`. Pedido da cliente no vídeo 2: "a imagem um pouco mais pra cima e ela mais centro da atenção". |
| **Gráfico principal** (o dado mais forte) | **Tela cheia** de animação, barras num cartão. Legenda em y ≈ 1100. |
| **Convite final** | Ela **em tela cheia**, legenda no cinto. |
| **Fim** | Dissolvência de 0,6 s para a **tela da logo do vídeo bruto** (fundo preto, "Link na bio!"), com a entrada na metade da velocidade e ~2 s parada. |

Divisão entre as metades: **só um sombreado suave** (degradê de ~200 px no topo do vídeo, de 55% a 0%), sem linha.

## Variar o estilo a cada vídeo (pedido da cliente)

A cliente **não quer a mesma receita sempre**: "toda vez que eu te mandar um vídeo, referências diferentes, aplicações
diferentes… tem que sempre ter alguma coisa diferente e que chame a atenção". A estrutura (começo e convite com ela em
tela cheia, meio dividido, logo do bruto no fim) e a identidade (marinho, dourado, logo) ficam. **Mudam o estilo das
telas animadas, os efeitos e os elementos visuais.**

Regras:
1. Antes de montar, leia o **histórico** abaixo e escolha um estilo **diferente dos 2 últimos vídeos**.
2. Traga **pelo menos 1 elemento novo** que ainda não apareceu (um efeito, um tipo de gráfico, um ícone, uma transição).
   Fontes de ideias: o catálogo do HyperFrames (`hyperframes catalog --json`, com cerca de 450 blocos de títulos, transições,
   overlays, gráficos e tipografia cinética; veja a skill `hyperframes-registry`), as referências em `estilo/referencias/`
   e elementos desenhados por você (ícones SVG de traço fino).
3. Escolha elementos que **tenham a ver com o que ela fala** (lupa para diagnóstico, documento para certidão, gráfico
   para números…). Não é enfeite solto.
4. Ao entregar, conte em uma linha o que é novo neste vídeo e **anote no histórico**.

### Catálogo de estilos (dentro da identidade PHcont)

| Estilo | Visual | Usado em |
|---|---|---|
| **A: Explicador com cartões** | fundo marinho com grade em perspectiva, estrelas e vidros; títulos Oswald maiúsculos com palavra dourada; cartões de vidro; lista numerada; "VS"; pílula "● PHCONT" | vídeo 1 (Planejamento tributário) |
| **B: Editorial com ícones** | sem pílula, grade nem vidros; **feixe de luz dourado** atravessando o fundo; títulos em **Playfair Display** com palavra em itálico dourado, entrando **palavra por palavra**; **ícones de traço dourado que se desenham** (lupa, documento, prédio, escudo); etiquetas em linha ("chips") com ✓; numerais grandes em itálico (01, 02, 03) com linhas finas | vídeo 2 (Regularização) |
| **C: Rascunho à mão + mapa** (ref. 7, `estilo/referencias/ref7_rascunho_mapa.mp4`) | fundo **papel quadriculado** escuro; **rabiscos de traço branco que se desenham** (documento com carimbo, prédio, calendário, setas); **anotações manuscritas em dourado** (fonte Caveat em `assets/fonts/`); **texto gigante ATRÁS dela** no gancho (ela recortada na frente); **mapa de ideias** com ela num círculo no centro e ramos dourados até os temas; itens riscados com rabisco bordô | vídeo 2 v3 (Regularização), **a cliente adorou o mapa e o recorte** |
| D: Dados e contadores (ideia) | números grandes contando, anéis de progresso, linha do tempo; tipografia mono para rótulos | — |
| E: Tipografia cinética (ideia) | frase-chave gigante ocupando a faixa, palavras trocando no ritmo da fala, máscara revelando o texto | — |
| F: Documento/papel (ideia) | fundo off-white com textura, "carimbo" dourado, cartões como fichas e notas fiscais estilizadas | — |

### Histórico

| Vídeo | Estilo | Elementos novos |
|---|---|---|
| 1. Planejamento tributário | A | gráfico de barras faturamento × caixa, VS, lista numerada |
| 2. Regularização (v2) | B | ícones que se desenham, feixe de luz, títulos palavra por palavra, chips com ✓, numerais em itálico; layout novo (faixa animada menor) |
| 2. Regularização (v3–v6, **aprovado na v6**) | C | texto atrás dela (marinho, só a cabeça na frente), mapa com o prédio "sua empresa" no centro, rabiscos que se desenham, letra manuscrita |

## Capas do Reels (pedido da cliente: seguir as capas do feed)

Diferente dos vídeos, nas **capas** a cliente quer o estilo do feed (`estilo/marca/feed_instagram_capas.jpg`): foto real dela
(sem recorte nem sombra azul em volta, só vinheta leve), título **embaixo**, dentro do recorte 3:4 (y 240–1680). Dois
modelos em `edicao_video2/capa/`:
- `capa_caixas.html`: Poppins Bold branco em **caixas retas**, a 1ª linha marinho `#1F2B42` e a 2ª bordô `#7A2A33`, deslocada.
- `capa_editorial.html`: degradê marinho embaixo, etiqueta dourada em maiúsculas, título **serifado** (Libre Caslon)
  branco com o final em **itálico dourado** e um traço bordô curto.

## Telas animadas (estilo A, o primeiro aprovado)

Estilo das referências 5 e 6 (`estilo/referencias/ref5_explicador_cartoes.mp4`, `ref6_explicador_lista.mp4`):

- Fundo azul-marinho com brilho no centro, grade em perspectiva embaixo, pontinhos de luz e "vidros" translúcidos andando devagar.
- Título centralizado em **Oswald 700 maiúsculo**, branco com a palavra-chave em **dourado**.
- Cartões escuros translúcidos com cantos arredondados. O item ativo ganha borda dourada com brilho. Listas numeradas
  com quadradinho dourado. Comparação com selo **"VS"** dourado, e o lado negativo em bordô com texto riscado.
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
5. **Mostrar mais dela** na tela dividida, não só o rosto. A partir do vídeo 2: faixa animada menor e mais alta (`SPLIT_TOP = 700`).
9. **Sem barra de progresso** (a barra dourada de tempo no topo foi recusada).
10. **Divisão entre as metades só com sombreado suave**, sem linha dourada e sem sombra forte.
11. **Mapa grande e centralizado** na tela cheia (no centro um desenho do tema, como o prédio "SUA EMPRESA"; o rosto dela no círculo foi recusado, temas em círculos de ~220 px), com a legenda **mais baixa** (y ≈ 1640) para não cobrir o mapa. As anotações ficam para fora, onde as linhas não passam.
8. **Nunca a mesma coisa sempre:** varie o estilo e traga elementos novos a cada vídeo (veja "Variar o estilo").
6. **Vibe leve, gráficos subindo devagar, final calmo e sem travadas nos cortes**: veja as boas práticas da `edicao-video`.
7. **Áudio sem trilha** por padrão (só a voz, a -14 LUFS). Pergunte antes de colocar música.
