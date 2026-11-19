---
name: mana
description: Edição de vídeos de TikTok da irmã da usuária ("Mana") — vídeos de humor, cortes de live, memes encaixados, legenda estilo TikTok. Use quando a pessoa escrever /mana, "Mana", "vídeo da minha irmã", ou pedir vídeo engraçado/meme/corte de live para TikTok. Junto com esta, siga o processo da skill edicao-video (baixar, transcrever, cortar, conferir, entregar). NÃO use a identidade da PHcont nem da DoctorFit.
---

# Mana: TikTok de humor

**Palavra-chave:** `/mana`. Pastas: `mana/bruto/` (vídeos), `mana/memes/` (takes de meme enviados), `mana/trabalho/`,
`mana/edicao_videoN/`, `mana/final/`.

Formato: vertical 1080x1920, 30 fps. Tom: **humor**, ritmo rápido, sem identidade de marca corporativa.

## Vídeo 1: live com a voz fina (em andamento)

Contexto: numa live de batalha, ela testava o microfone (apertando o botão a voz saía fina, sem apertar saía normal),
mas a live inteira saiu com a voz fina, e a pessoa da batalha começou a rir. Objetivo: deixar o momento engraçado,
encaixando takes de meme que a usuária vai mandar.

Takes de meme enviados (`mana/memes/`, gravações de tela — recorte a área útil antes de usar):
| Arquivo | Meme | Duração | Área útil (crop) | Onde encaixa |
|---|---|---|---|---|
| `meme1.mov` | plateia rindo/aplaudindo (vídeo antigo) | 1,3 s | `crop=1032:970:66:592` | logo depois de uma risada grande ou no "auge" da voz fina |
| `meme2.mov` | cachorro com sorrisinho debochado | 6,2 s (usar ~1,5–2 s) | `crop=1130:1460:72:382` | reação de deboche: quando ele percebe a voz fina ou quando ela tenta falar sério |
| `meme3.mov` | créditos "Directed by Robert B. Weide" (fim de cena constrangedora) | 6,7 s | tela preta com texto (sem crop; cortar o topo com o texto "memes para poner…") | **final do vídeo**, logo depois do momento mais constrangedor |

**Título escolhido pela usuária (texto no topo, o vídeo todo):**
"EU ACHANDO QUE TÔ ARRASANDO, ENQUANTO TODO MUNDO RI DA MINHA VOZ" (usar exatamente assim, em maiúsculas, com
emoji 💀 ou 😭 opcional no fim; letra grossa estilo TikTok, branca com contorno preto, em 2–3 linhas, no alto sem cobrir os rostos).

Arquivo bom: `mana/bruto/live.mov` (Drive, 1440x2560, 60 fps). O envio pelo chat cortou a imagem em 2,7 s, então peça sempre pelo Drive. A gravação começa com 1,8 s de vinheta "glitch": **a usuária quer manter** esse começo, com o título entrando junto (tremendo e assentando).
Transcrição do áudio em `mana/trabalho/transcricao_audio.json` (momentos-chave: 6,9 s "Oi, gentiiim"; 36 s "Eu curto sua
voz, né?"; 45–47 s "Alguém grava isso aí"; 50 s "Eu não acredito, ninguém falou nada pra mim"; 69 s "Eu não sabia, eu juro por Deus").

Ideias de edição de humor:
- **Gancho nos 2 primeiros segundos:** o momento mais engraçado (a risada ou a voz fina mais aguda) antes do contexto.
- Texto de contexto curto no topo ("quando você testa o microfone… e esquece de desligar 💀").
- **Zoom rápido (punch-in) e congelamento** de quadro nas reações, com o meme entrando logo depois.
- **Zoom nas risadas (ajustado na v2):** só em **algumas** risadas (3), e **leve** (até ~1,28x), indo e voltando suave (0,6 s), sem perder a tela dividida. Não fazer zoom forte nem em todas.
- **Efeito "bonequinho 3D" (versão aprovada pela usuária):** o **bonequinho branco 3D pensativo** da referência dela (`mana/edicao_video1/fx/boneco.png`, recortado com `remove-background`), que entra andando pela **faixa preta de baixo** (sem cobrir a live), para coçando a cabeça e sai, com ❓ 3D quicando em volta da cabeça. Versão anterior: emoji 3D 😱 (Microsoft Fluent Emoji, licença MIT, em `mana/edicao_video1/fx/`) atravessando a tela balançando, com ❓ 3D quicando, no momento em que ela fala "eu não acredito". Para outros momentos, outros emojis do mesmo pacote (`https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/<Nome>/3D/<nome>_3d.png`).
- (pedido original: toda vez que o cara rir, zoom no rosto dele) Para achar os
  risos: ouça picos de áudio (`hyperframes audio`/`silencedetect` + transcrição com "[risos]"/"kkk"), confirme olhando
  os quadros, e faça o zoom centrado no rosto dele (no lado da tela onde ele aparece na live dividida), entrando rápido
  (0,15 s) e saindo quando o riso acaba.
- Legenda palavra por palavra estilo TikTok (branca, contorno preto, palavra-chave colorida).
- Efeitos sonoros curtos (boing, record scratch, risada) em volume baixo, só se a usuária quiser.
- Memes: corte só o trecho certo (0,5–2 s), encaixe logo depois do gatilho e volte para a live.

Áudio: TikTok pode silenciar música protegida. Para música de fundo, a usuária escolhe pelo próprio app na hora de postar.

## Histórico

| Vídeo | Arquivo | O que foi feito |
|---|---|---|
| 1. Live com a voz fina (v2) | `mana/final/mana_voz_fina_v2.mp4`, `mana/edicao_video1/montar_v2.py` | começo original com glitch + título tremendo, zoom leve em 3 risadas, 😱 + ❓ 3D no "eu não acredito", memes e créditos |
| 1. Live com a voz fina (v1) | `mana/final/mana_voz_fina_v1.mp4`, montagem `mana/edicao_video1/montar.py` (ffmpeg puro) | título fixo no topo (Anton, branco + última linha amarela), corte do trecho morno 27–35,5 s, 7 zooms ~1,7x no rosto dele nas risadas, cachorro debochado após "Eu curto sua voz, né?", plateia rindo após "alguém grava isso aí", créditos "Directed by Robert B. Weide" no fim; áudio -14 LUFS |
