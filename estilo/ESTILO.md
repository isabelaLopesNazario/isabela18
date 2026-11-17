# Estilo de edição

## Paleta da empresa

| Cor | Hex (provisório) | Uso |
|---|---|---|
| Azul-marinho | `#0F1E3D` | Fundo principal das telas de motion e dos painéis |
| Bordô | `#7A1F2B` | Cor de destaque: palavra-chave da legenda, telas cheias de impacto, barras e números em destaque |
| Dourado | `#C8A24A` | Detalhes finos: linhas, rótulos "Passo 1", ponto final dos títulos, ícones |
| Branco | `#F5F2EC` (off-white) / `#FFFFFF` | Texto principal e fundo das telas claras |
| Preto | `#0B0B0D` | Fundo alternativo, sombras e texto sobre as telas claras |

> Os hex são aproximados. Se a empresa tiver os códigos oficiais (manual da marca), substituir aqui.

Regra de proporção: muito fundo escuro (marinho/preto) ou claro (off-white), e pouca cor de destaque (bordô/dourado), como as referências fazem com o laranja.

## Formatos

- **Principal:** vertical 9:16, 1080x1920, 30 fps (referências 3 e 4).
- **Alternativo:** horizontal 16:9 para peças de motion puro (referências 1 e 2).

## Estrutura do vídeo (talking head, ref. 4)

1. **Gancho (0–2 s):** rosto em tela cheia + legenda forte.
2. **Tela dividida:** metade de cima com o painel de motion explicando o ponto (fundo marinho), metade de baixo com o rosto.
3. **Passos numerados:** rótulo pequeno em dourado ("Passo 1") e título em branco ("Referência", "Análise", "Roteiro", "Edição").
4. **Números animados:** contadores grandes subindo (ex.: 211, 239) com onda de áudio fina embaixo.
5. Volta para o rosto em tela cheia nos momentos de fala pessoal.
6. **CTA final:** tela com a chamada para comentar ou seguir.

Ritmo: troca de layout ou elemento novo a cada 1–3 s; sem pausas nem respiros.

## Legendas

- **Talking head (ref. 4):** 1 a 2 palavras por vez, centralizadas no terço inferior do rosto; sans-serif limpa, branco; palavra-chave em **bordô** (ou dourado quando o fundo for escuro demais para o bordô).
- **Tutorial / tela gravada (ref. 3):** caixa branca fixa no topo com o título do vídeo (texto preto); legenda embaixo em itálico, cor de destaque **dourado**, frases curtas.

## Motion design (refs. 1 e 2)

- **Tipografia:** mistura de serifada editorial condensada (títulos grandes, como "FÍSICA", "PARTÍCULAS") + sans bold pesada (palavras de impacto, como "PULA", "ESTICA") + monoespaçada pequena para rótulos e notas técnicas ("// cada quadro é…").
- **Telas cheias de palavra:** uma palavra gigante em fundo de cor sólida (bordô) com um rótulo pequeno embaixo à esquerda em caixa preta.
- **Elemento-guia:** um ponto/bolinha (dourado ou bordô) que atravessa as cenas e liga uma ideia à outra.
- **Padrões geométricos** (círculos, meias-luas, quadrados) em bordô/marinho/branco/preto; podem ganhar volume em 3D.
- **Dados:** números grandes com rótulo mono ("QUADROS", "POR SEGUNDO"), barras com uma barra destacada em bordô, ondas de áudio finas.
- **Fechamento:** cartão com o nome/logo da marca em fundo off-white, título grande e subtítulo mono.
- **Transições:** cortes secos no ritmo, palavras que entram letra a letra, zoom/rotação de câmera em texto circular, máscaras deslizando. Sem transições "de programa" (estrela, cortina).

## Áudio

- Trilha instrumental de fundo com batida marcada; cortes visuais caem na batida.
- Voz normalizada para redes (-14 LUFS).

## Não copiar

Marcas d'água do TikTok, @ de outros criadores, logos e músicas das referências.

## Referências

Ficam em `estilo/referencias/`:
1. `ref1_motion_laranja.mov`: motion puro, palavras gigantes, padrões geométricos, dados.
2. `ref2_motion_editorial.mov`: tipografia serifada editorial, partículas, números.
3. `ref3_tutorial_tela.mp4`: tutorial de tela gravada com título no topo e legenda em itálico.
4. `ref4_talking_head.mp4`: rosto + painel de motion dividido, passos numerados, legenda palavra a palavra.
