# Estúdio 3D: vídeos curtos animados feitos por código

Você escreve **um arquivo de roteiro** (`roteiro.json`) dizendo o que é falado e o que aparece em cada cena. O sistema
faz o resto, sem editor de vídeo:

1. **Voz:** usa o áudio gravado (ou uma voz-guia do computador, para rascunho), corta e padroniza o volume.
2. **Sincronia:** transcreve a voz com Whisper e casa cada palavra do roteiro com o instante em que ela é falada.
   Tudo que você marcar "na palavra X" acontece exatamente quando a palavra X é dita.
3. **Cenas 3D:** monta cenário, personagens (com poses e expressões), objetos (com entradas e saídas animadas) e a câmera
   (com enquadramento automático, que mede a cena e afasta até caber tudo).
4. **Legenda:** palavra por palavra (1–2 por vez), com as palavras marcadas com `*asteriscos*` em destaque, já
   escritas como no roteiro (sem os erros da transcrição).
5. **Som:** gera efeitos sonoros (pop, whoosh, baque, puff, plim, moeda) nos momentos certos e uma **trilha própria**
   (acordes e arpejo gerados por código, sem direitos de terceiros), mixa com a voz a -14 LUFS.
6. **Render:** HyperFrames + Three.js desenham quadro a quadro (1080x1920, 30 fps), e o ffmpeg junta tudo, com a
   vinheta final opcional.

## Como usar

```bash
python3 estudio3d/gerar.py <pasta-com-roteiro.json> --previa 2,6,12   # imagens rápidas para conferir
python3 estudio3d/gerar.py <pasta-com-roteiro.json>                   # vídeo final em <pasta>/saida/
```

Exemplo completo: `estudio3d/exemplos/reforma/roteiro.json` (Reforma Tributária, PHcont).

## O roteiro

```json
{
  "nome_saida": "meu_video.mp4",
  "narracao": { "arquivo": "voz.mp3", "inicio": 0, "fim": 28.0 },      // sem "arquivo": voz-guia do computador
  "final":    { "video": "bruto.mov", "inicio": 29.4, "fim": 31.8 },    // opcional: vinheta da logo no fim
  "legenda":  { "palavras": 2, "topo": 1560, "cor_destaque": "#ffd45a" },
  "musica": true, "musica_lufs": -31,
  "cenas": [
    {
      "fala": "*ICMS,* *ISS,* *PIS* e *COFINS* vão *acabar.*",       // texto exato da fala desta cena
      "cenario": "praca",                                            // praca | cidade | escritorio | estudio
      "camera": { "ang0": -0.12, "ang1": 0.08 },                     // giro; distância é automática
      "atores": [
        { "tipo": "consultora", "pos": [-1.6, 2.6], "rot": 0.25,
          "segura": { "tipo": "vareta", "mao": "D" },
          "acoes": [ { "em": "ICMS", "pose": "aponta" }, { "em": "acabar", "pose": "explica" } ],
          "andar": [ { "em": "atravessar", "para": [3, 0], "dur": 2.5 } ] }
      ],
      "objetos": [
        { "tipo": "placa", "props": { "texto": "ICMS" }, "pos": [-2.4, 0, -2],
          "entra": { "modo": "surge", "em": "ICMS" }, "sai": { "modo": "cai", "em": "acabar" } }
      ]
    }
  ]
}
```

**Quando (`em`)**: uma palavra da fala da cena (`"ICMS"`), segundos depois do início da cena (`1.2`), `"inicio"` ou
`"fim"`. `"mais": 0.2` adianta ou atrasa. Uma cena com `"fala": ""` e `"dur": 2` entra depois da narração (fecho visual).

**Personagens** (`motor/elenco.js`): `consultora` (menina explicando, blazer PH), `contador` (terno, gravata dourada,
óculos), `empresario`, `atendente`, `concorrente`, `cliente`. Cores trocáveis com `"cores": {"camisa": "#..."}`.

**Poses**: `parado`, `aponta`, `explica`, `acena`, `assustado`, `pensando`, `comemora`, `triste`, `segura`, `confuso`.
Transição suave, piscada e respiração automáticas; boca abre e fecha nas poses de fala.

**Objetos** (`motor/objetos.js`): `predio` (nome, cor, telhado, colunas, bandeira), `placa`, `moeda`, `documento`
(titulo, alerta), `quadro` (linhas), `gangorra` (anim `inclina`), `escada` (rotulos), `ponte`, `lupa`, `vareta`,
`celular`, `seta`, `calendario`, `grafico` (valores), `arvore`, `rotulo` (pílula de texto), `icone` (?, !, ✓, $),
`balao` (WhatsApp etc.).

**Entradas**: `surge`, `cai`, `sobe`, `desliza`. **Saídas**: `some` (com poeira), `cai`.
**Animações**: `flutua`, `gira`, `pulsa`, `inclina`.

## Para crescer

- Novo personagem: acrescente as cores em `PERSONAGENS` (`elenco.js`).
- Novo objeto: uma função em `CATALOGO` (`objetos.js`).
- Nova pose: uma linha em `POSES` (`elenco.js`).
- Voz natural paga (ElevenLabs): basta gravar o MP3 e apontar em `narracao.arquivo`.
