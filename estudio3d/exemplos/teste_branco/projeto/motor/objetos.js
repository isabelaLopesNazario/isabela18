// Biblioteca de objetos e cenários. criarObjeto(tipo, props, marca) -> THREE.Object3D
import * as THREE from "./lib/three.module.js";
import { MAT } from "./elenco.js";

const sombra = (o) => { o.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } }); return o; };

export function texturaTexto(linhas, { bg = "#ffffff", fg = "#1f2b42", w = 1024, h = 512, fs = 200, peso = 900, raio = 0, borda = null } = {}) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const x = c.getContext("2d");
  if (bg) {
    x.fillStyle = bg;
    if (raio) { x.beginPath(); x.roundRect(4, 4, w - 8, h - 8, raio); x.fill(); if (borda) { x.lineWidth = 10; x.strokeStyle = borda; x.stroke(); } }
    else x.fillRect(0, 0, w, h);
  }
  const L = Array.isArray(linhas) ? linhas : [linhas];
  x.fillStyle = fg; x.textAlign = "center"; x.textBaseline = "middle";
  L.forEach((ln, i) => {
    let f = typeof ln === "object" ? ln.fs || fs : fs;
    const txt = typeof ln === "object" ? ln.t : ln;
    x.font = `${peso} ${f}px Poppins, "Arial Black", Arial, sans-serif`;
    while (x.measureText(txt).width > w * 0.88 && f > 20) { f -= 4; x.font = `${peso} ${f}px Poppins, "Arial Black", Arial, sans-serif`; }
    if (typeof ln === "object" && ln.cor) x.fillStyle = ln.cor; else x.fillStyle = fg;
    x.fillText(txt, w / 2, h / 2 + (i - (L.length - 1) / 2) * f * 1.15 + 6);
  });
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

// Cartaz que sempre olha para a câmera (rótulos, ícones, balões)
function cartaz(linhas, opts, largura = 3) {
  const w = opts.w || 1024, h = opts.h || 360;
  const tex = texturaTexto(linhas, { ...opts, w, h });
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false }));
  s.scale.set(largura, largura * h / w, 1); s.renderOrder = 10;
  return s;
}

function arvore(s = 1) {
  const g = new THREE.Group();
  const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.18 * s, 0.22 * s, 1.2 * s, 6), MAT("#7a5235")); tr.position.y = 0.6 * s; g.add(tr);
  const co = new THREE.Mesh(new THREE.IcosahedronGeometry(0.95 * s, 0), MAT("#4f9a4a")); co.position.y = 1.7 * s; g.add(co);
  return sombra(g);
}

function predio({ nome = "PREFEITURA", cor = "#3f7fc4", telhado = "#2b5c93", larg = 4.2, alt = 3.2, colunas = false, bandeira = null }) {
  const g = new THREE.Group();
  const corpo = new THREE.Mesh(new THREE.BoxGeometry(larg, alt, 2.6), MAT(cor)); corpo.position.y = alt / 2; g.add(corpo);
  const teto = new THREE.Mesh(new THREE.CylinderGeometry(0.01, larg * 0.62, 1.4, 4), MAT(telhado));
  teto.rotation.y = Math.PI / 4; teto.scale.z = 0.62; teto.position.y = alt + 0.7; g.add(teto);
  if (nome) {
    const placa = new THREE.Mesh(new THREE.PlaneGeometry(larg * 0.8, 0.7), new THREE.MeshBasicMaterial({ map: texturaTexto(nome, { w: 1024, h: 180, fs: 120 }) }));
    placa.position.set(0, alt - 0.45, 1.31); g.add(placa);
  }
  if (colunas) {
    for (let i = 0; i < 4; i++) { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, alt - 0.9, 12), MAT("#f2efe8")); c.position.set(-larg * 0.36 + i * larg * 0.24, (alt - 0.9) / 2, 1.5); g.add(c); }
    const deg = new THREE.Mesh(new THREE.BoxGeometry(larg + 0.6, 0.25, 3.4), MAT("#e7e2d6")); deg.position.y = 0.12; g.add(deg);
  } else {
    for (let i = 0; i < 3; i++) { const j = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.8, 0.05), MAT("#bcd7ee", 0.3)); j.position.set(-larg / 3 + i * (larg / 3), alt * 0.45, 1.31); g.add(j); }
  }
  const porta = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.3, 0.06), MAT("#5d4636")); porta.position.set(0, 0.65, 1.32); g.add(porta);
  if (bandeira) {
    const mastro = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.6, 6), MAT("#8a8f96")); mastro.position.y = alt + 1.9; g.add(mastro);
    const b = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.42, 0.03), MAT(bandeira)); b.position.set(0.37, alt + 2.45, 0); g.add(b);
  }
  return sombra(g);
}

function placa({ texto = "ICMS", cor = "#1f2b42", corTexto = "#e9cf8e", altura = 5.4 }) {
  const g = new THREE.Group();
  const p = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, altura, 8), MAT("#5d4636")); p.position.y = altura / 2; g.add(p);
  const tab = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.8, 0.14), MAT(cor)); tab.position.y = altura + 0.3; g.add(tab);
  const f = new THREE.Mesh(new THREE.PlaneGeometry(1.48, 0.68), new THREE.MeshBasicMaterial({ map: texturaTexto(texto, { bg: cor, fg: corTexto, w: 512, h: 236, fs: 150 }) }));
  f.position.set(0, altura + 0.3, 0.08); g.add(f);
  return sombra(g);
}

function moeda({ texto = "$", cor = "#e1b84a" }) {
  const g = new THREE.Group();
  const d = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 0.22, 40), MAT(cor, 0.35)); d.rotation.x = Math.PI / 2; g.add(d);
  for (const z of [0.115, -0.115]) {
    const f = new THREE.Mesh(new THREE.CircleGeometry(0.78, 40), new THREE.MeshBasicMaterial({ map: texturaTexto(texto, { bg: "#f0cd62", fg: "#8a6512", w: 512, h: 512, fs: texto.length > 2 ? 170 : 260 }) }));
    f.position.z = z; if (z < 0) f.rotation.y = Math.PI; g.add(f);
  }
  return sombra(g);
}

function documento({ titulo = "NOTA", linhas = 5, alerta = false }) {
  const g = new THREE.Group();
  const folha = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.1, 0.05), MAT("#ffffff")); g.add(folha);
  const c = document.createElement("canvas"); c.width = 512; c.height = 672; const x = c.getContext("2d");
  x.fillStyle = "#ffffff"; x.fillRect(0, 0, 512, 672);
  x.fillStyle = "#1f2b42"; x.fillRect(40, 40, 432, 90);
  x.fillStyle = "#ffffff"; x.font = "800 58px Poppins, Arial"; x.textAlign = "center"; x.fillText(titulo, 256, 105);
  for (let i = 0; i < linhas; i++) { x.fillStyle = alerta && i === 2 ? "#e05656" : "#c5ccd6"; x.fillRect(60, 180 + i * 70, i % 2 ? 300 : 390, 26); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const f = new THREE.Mesh(new THREE.PlaneGeometry(1.56, 2.06), new THREE.MeshBasicMaterial({ map: t })); f.position.z = 0.03; g.add(f);
  return sombra(g);
}

function quadro({ linhas = ["IBS + CBS"] }) {
  const g = new THREE.Group();
  const pl = new THREE.Mesh(new THREE.BoxGeometry(4.4, 2.7, 0.12), MAT("#8a8f96")); pl.position.y = 3.2; g.add(pl);
  const tela = new THREE.Mesh(new THREE.PlaneGeometry(4.15, 2.45), new THREE.MeshBasicMaterial({ map: texturaTexto(linhas, { bg: "#ffffff", fg: "#1f2b42", w: 1024, h: 600, fs: 150 }) }));
  tela.position.set(0, 3.2, 0.07); g.add(tela);
  for (const [px, rz] of [[-1.4, 0.18], [1.4, -0.18]]) { const pe = new THREE.Mesh(new THREE.BoxGeometry(0.1, 2.3, 0.1), MAT("#5f646b")); pe.position.set(px, 1.0, 0); pe.rotation.z = rz; g.add(pe); }
  return sombra(g);
}

function gangorra() {
  const g = new THREE.Group();
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 0.6, 1.0, 3), MAT("#7a2a33")); base.position.y = 0.5; base.rotation.y = Math.PI / 6; g.add(base);
  const prancha = new THREE.Group(); prancha.position.y = 1.05; g.add(prancha);
  const tab = new THREE.Mesh(new THREE.BoxGeometry(7, 0.18, 0.9), MAT("#c9ad6e", 0.5)); prancha.add(tab);
  g.userData.prancha = prancha;
  return sombra(g);
}

function escada({ degraus = 4, rotulos = [] }) {
  const g = new THREE.Group();
  for (let i = 0; i < degraus; i++) {
    const d = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.6 * (i + 1), 1.6), MAT(i % 2 ? "#2b3a5c" : "#1f2b42")); d.position.set(i * 1.6, 0.3 * (i + 1), 0); g.add(d);
    if (rotulos[i]) { const s = cartaz(rotulos[i], { bg: "#c9ad6e", fg: "#1f2b42", fs: 150, raio: 60 }, 1.5); s.position.set(i * 1.6, 0.6 * (i + 1) + 0.6, 0.9); g.add(s); }
  }
  return sombra(g);
}

function ponte() {
  const g = new THREE.Group();
  const tab = new THREE.Mesh(new THREE.BoxGeometry(8, 0.25, 1.8), MAT("#8a5a3a")); tab.position.y = 0.6; g.add(tab);
  for (const z of [-0.85, 0.85]) {
    const c = new THREE.Mesh(new THREE.BoxGeometry(8, 0.1, 0.1), MAT("#5d4636")); c.position.set(0, 1.6, z); g.add(c);
    for (let i = 0; i < 6; i++) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.0, 0.12), MAT("#5d4636")); p.position.set(-3.6 + i * 1.44, 1.1, z); g.add(p); }
  }
  const agua = new THREE.Mesh(new THREE.BoxGeometry(5, 0.1, 6), MAT("#5aa7d6", 0.3)); agua.position.y = 0.02; g.add(agua);
  return sombra(g);
}

function lupa() {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new THREE.TorusGeometry(0.75, 0.11, 12, 40), MAT("#9ea3ab", 0.35)));
  g.add(new THREE.Mesh(new THREE.CircleGeometry(0.72, 40), new THREE.MeshStandardMaterial({ color: "#cfe6f5", transparent: true, opacity: 0.35, roughness: 0.05 })));
  const cabo = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.12, 1.2, 12), MAT("#1b1b1b")); cabo.position.y = -1.35; g.add(cabo);
  return sombra(g);
}
function vareta() { return sombra(new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.05, 2.2, 10), MAT("#b9bcc2", 0.4))); }

function celular() {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.1, 0.08), MAT("#1b1b1b")));
  const tela = new THREE.Mesh(new THREE.PlaneGeometry(0.52, 0.98), new THREE.MeshBasicMaterial({ color: "#25d366" })); tela.position.z = 0.045; g.add(tela);
  return sombra(g);
}

function seta({ cor = "#c9ad6e", comp = 2.5 }) {
  const g = new THREE.Group();
  const h = new THREE.Mesh(new THREE.BoxGeometry(comp, 0.25, 0.25), MAT(cor, 0.4)); h.position.x = comp / 2; g.add(h);
  const p = new THREE.Mesh(new THREE.ConeGeometry(0.4, 0.7, 4), MAT(cor, 0.4)); p.rotation.z = -Math.PI / 2; p.position.x = comp + 0.3; g.add(p);
  return sombra(g);
}

function calendario({ texto = "2026" }) {
  const g = new THREE.Group();
  const b = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.6, 0.12), MAT("#ffffff")); g.add(b);
  const topo = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.4, 0.14), MAT("#7a2a33")); topo.position.y = 0.6; g.add(topo);
  const f = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 1.0), new THREE.MeshBasicMaterial({ map: texturaTexto(texto, { w: 512, h: 360, fs: 170 }) })); f.position.set(0, -0.15, 0.07); g.add(f);
  return sombra(g);
}

function grafico({ valores = [0.4, 0.7, 1] , cor = "#c9ad6e" }) {
  const g = new THREE.Group();
  valores.forEach((v, i) => { const b = new THREE.Mesh(new THREE.BoxGeometry(0.6, 2.4 * v, 0.6), MAT(i === valores.length - 1 ? cor : "#1f2b42", 0.5)); b.position.set(i * 0.85, 1.2 * v, 0); g.add(b); });
  return sombra(g);
}

const CATALOGO = {
  arvore: (p) => arvore(p.escala || 1),
  pino: (p) => {
    const g = new THREE.Group(), cor = MAT(p.cor || "#e8432f", 0.35);
    const bola = new THREE.Mesh(new THREE.SphereGeometry(0.6, 28, 20), cor); bola.position.y = 1.55; g.add(bola);
    const ponta = new THREE.Mesh(new THREE.ConeGeometry(0.52, 1.25, 28), cor); ponta.rotation.x = Math.PI; ponta.position.y = 0.72; g.add(ponta);
    const furo = new THREE.Mesh(new THREE.CircleGeometry(0.26, 24), new THREE.MeshBasicMaterial({ color: "#ffffff" })); furo.position.set(0, 1.58, 0.6); g.add(furo);
    const furo2 = furo.clone(); furo2.rotation.y = Math.PI; furo2.position.z = -0.6; g.add(furo2);
    return sombra(g);
  },
  carro: (p) => sombra(carro(p.cor || "#d8463c")),
  predio_iso: (p) => sombra(predioIso(p.larg || 4, p.prof || 4, p.andares || 3, p.cor || "#e9c9a0", p.vidro || "#3b8f9c", Math.random)),
  palanque: (p) => {
    const g = new THREE.Group(), mad = MAT("#d9b48a", 0.7);
    const c = new THREE.Mesh(new THREE.BoxGeometry(1.5, 2.3, 0.9), mad); c.position.y = 1.15; g.add(c);
    const t = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.1, 1.2), mad); t.position.set(0, 2.38, 0.1); t.rotation.x = 0.25; g.add(t);
    for (const sx of [-0.15, 0.15]) { const h = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.5, 8), MAT("#333")); h.position.set(sx, 2.6, -0.1); g.add(h); const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.07, 0.16, 4, 8), MAT("#555", 0.4)); m.position.set(sx, 2.92, -0.05); m.rotation.x = -0.4; g.add(m); }
    if (p.texto) { const s = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 0.42), new THREE.MeshBasicMaterial({ map: texturaTexto(p.texto, { fs: 170, w: 1024, h: 330 }) })); s.position.set(0, 1.6, 0.46); g.add(s); }
    return sombra(g);
  },
  predio, placa, moeda, documento, quadro, gangorra, escada, ponte, lupa, vareta, celular, seta, calendario, grafico,
  rotulo: (p) => cartaz(p.texto, { bg: p.fundo || "#ffffff", fg: p.cor || "#1f2b42", fs: p.tamanho || 170, raio: 170, borda: p.borda || "#7a2a33", h: 300 }, p.largura || 3),
  icone: (p) => cartaz(p.simbolo || "?", { bg: null, fg: p.cor || "#c9ad6e", fs: 420, peso: 900, w: 512, h: 512 }, p.largura || 1.4),
  balao: (p) => cartaz(p.texto, { bg: p.fundo || "#25d366", fg: p.cor || "#ffffff", fs: p.tamanho || 130, raio: 120, h: 300 }, p.largura || 3.6),
};

export function criarObjeto(tipo, props = {}) {
  const f = CATALOGO[tipo];
  if (!f) { console.warn("objeto desconhecido:", tipo); return new THREE.Group(); }
  const o = f(props);
  o.userData.tipo = tipo;
  return o;
}

// ---------------------------------------------------------------- cidade em miniatura (isométrica)
function predioIso(larg, prof, andares, cor, vidro, rnd) {
  const g = new THREE.Group();
  const h = andares * 1.1;
  const corpo = new THREE.Mesh(new THREE.BoxGeometry(larg, h, prof), MAT(cor, 0.8)); corpo.position.y = h / 2; g.add(corpo);
  const beiral = new THREE.Mesh(new THREE.BoxGeometry(larg + 0.25, 0.22, prof + 0.25), MAT("#f3ede2", 0.8)); beiral.position.y = h + 0.11; g.add(beiral);
  for (let a = 0; a < andares; a++) {
    const nj = Math.max(1, Math.floor(larg / 1.1));
    for (let j = 0; j < nj; j++) {
      const x = -larg / 2 + (j + 0.5) * (larg / nj);
      const jan = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.6, 0.05), MAT(vidro, 0.25)); jan.position.set(x, 0.6 + a * 1.1, prof / 2 + 0.02); g.add(jan);
      const jan2 = jan.clone(); jan2.rotation.y = Math.PI / 2; jan2.position.set(larg / 2 + 0.02, 0.6 + a * 1.1, x * (prof / larg)); g.add(jan2);
    }
  }
  // caixas de ar-condicionado no telhado
  for (let k = 0; k < 2; k++) { const ac = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.35, 0.5), MAT("#c9ccd1")); ac.position.set((rnd() - 0.5) * (larg - 1), h + 0.4, (rnd() - 0.5) * (prof - 1)); g.add(ac); }
  return g;
}
function carro(cor) {
  const g = new THREE.Group();
  const b = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.4, 0.75), MAT(cor, 0.4)); b.position.y = 0.38; g.add(b);
  const c = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.32, 0.65), MAT("#dfe9f1", 0.2)); c.position.set(-0.08, 0.72, 0); g.add(c);
  for (const [x, z] of [[-0.48, 0.38], [0.48, 0.38], [-0.48, -0.38], [0.48, -0.38]]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.12, 12), MAT("#2a2a2a")); w.rotation.x = Math.PI / 2; w.position.set(x, 0.18, z); g.add(w); }
  return g;
}
function poste() {
  const g = new THREE.Group();
  const h = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.06, 1.6, 8), MAT("#5d6670")); h.position.y = 0.8; g.add(h);
  const l = new THREE.Mesh(new THREE.SphereGeometry(0.13, 10, 8), MAT("#fff6d8", 0.3)); l.position.y = 1.65; g.add(l);
  return g;
}
function cidadeIso(C) {
  const g = new THREE.Group();
  let seed = 7; const rnd = () => { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
  const T = 30;
  const terra = new THREE.Mesh(new THREE.BoxGeometry(T, 1.6, T), MAT("#7a4e35")); terra.position.y = -0.95; g.add(terra);
  const grama = new THREE.Mesh(new THREE.BoxGeometry(T, 0.3, T), MAT("#8cc265")); grama.position.y = -0.15; grama.receiveShadow = true; g.add(grama);
  // ruas em cruz com faixas brancas e calçadas
  const RUA = 3.2;
  for (const dir of [0, 1]) {
    for (const off of [-7.5, 7.5]) {
      const calc = new THREE.Mesh(new THREE.BoxGeometry(dir ? RUA + 1.2 : T, 0.12, dir ? T : RUA + 1.2), MAT("#d9dbde")); calc.position.set(dir ? off : 0, 0.02, dir ? 0 : off); calc.receiveShadow = true; g.add(calc);
      const rua = new THREE.Mesh(new THREE.BoxGeometry(dir ? RUA : T, 0.14, dir ? T : RUA), MAT("#4b5058", 0.95)); rua.position.set(dir ? off : 0, 0.04, dir ? 0 : off); rua.receiveShadow = true; g.add(rua);
      for (let k = -T / 2 + 1; k < T / 2; k += 2.2) {
        if (Math.abs(k - (-7.5)) < 2 || Math.abs(k - 7.5) < 2) continue;
        const f = new THREE.Mesh(new THREE.BoxGeometry(dir ? 0.14 : 1.0, 0.02, dir ? 1.0 : 0.14), MAT("#ffffff")); f.position.set(dir ? off : k, 0.12, dir ? k : off); g.add(f);
      }
    }
  }
  // quadras: prédios nas bordas, centro livre para a cena
  const cores = ["#e9c9a0", "#f1e6d2", "#cfe0e6", "#e7b98b", "#d6dfe8"], vidros = ["#3b8f9c", "#4a7fb5", "#2f7d86"];
  const quadras = [[-13, -13], [0, -13], [13, -13], [-13, 0], [13, 0], [-13, 13], [13, 13]];
  quadras.forEach(([x, z], i) => {
    const p = predioIso(3 + rnd() * 2, 3 + rnd() * 1.5, 2 + Math.floor(rnd() * 4), cores[i % cores.length], vidros[i % 3], rnd);
    p.position.set(x + (rnd() - 0.5) * 1.5, 0, z + (rnd() - 0.5) * 1.5); g.add(p);
  });
  // árvores low-poly, postes e carros
  for (let k = 0; k < 18; k++) {
    const x = (rnd() - 0.5) * (T - 3), z = (rnd() - 0.5) * (T - 3);
    if (Math.abs(Math.abs(x) - 7.5) < 2.6 || Math.abs(Math.abs(z) - 7.5) < 2.6) continue;
    if (Math.abs(x) < 6 && Math.abs(z) < 6) continue;
    const a = arvore(0.7 + rnd() * 0.4); a.position.set(x, 0, z); g.add(a);
  }
  for (const [x, z] of [[-5.3, -5.3], [5.3, -5.3], [-5.3, 5.3], [5.3, 5.3], [9.7, -3], [-9.7, 3]]) { const p = poste(); p.position.set(x, 0, z); g.add(p); }
  [["#d8463c", -7.5, -10, 0], ["#ffffff", 7.5, 4, 0], ["#2f6fb2", -2, -7.5, 1], ["#e8b93b", 11, 7.5, 1]].forEach(([c, x, z, r]) => { const k = carro(c); k.position.set(x, 0.1, z); k.rotation.y = r ? 0 : Math.PI / 2; g.add(k); });
  // praça central clara (onde ficam os personagens)
  const praca = new THREE.Mesh(new THREE.BoxGeometry(11, 0.1, 11), MAT("#eae4d6")); praca.position.y = 0.02; praca.receiveShadow = true; g.add(praca);
  return sombra(g);
}

// ---------------------------------------------------------------- cenários
export function criarCenario(nome, marca = {}) {
  const g = new THREE.Group();
  const C = { ceu: "#cfe3f2", grama: "#7fb069", chao: "#ead9b8", ...marca.cenario };
  if (nome === "cidade_iso" || nome === "maquete") {
    g.add(cidadeIso(C));
    g.userData.ceu = marca.fundoCidade || "#bcd9ef";
    return g;
  }
  if (nome === "praca" || nome === "cidade") {
    const base = new THREE.Mesh(new THREE.CylinderGeometry(13, 13.4, 1.2, 56), MAT(C.grama)); base.position.y = -0.6; base.receiveShadow = true; g.add(base);
    const borda = new THREE.Mesh(new THREE.CylinderGeometry(13.45, 13.6, 0.6, 56), MAT("#5d4636")); borda.position.y = -1.3; g.add(borda);
    const praca = new THREE.Mesh(new THREE.CylinderGeometry(8, 8, 0.08, 48), MAT(C.chao, 0.95)); praca.position.y = 0.04; praca.receiveShadow = true; g.add(praca);
    [[-10.5, -3], [10.6, -2.5], [-8.8, -8], [9, -7.8], [-11, 3.5], [11.2, 4]].forEach(([x, z], i) => { const a = arvore(1 + (i % 3) * 0.15); a.position.set(x, 0, z); g.add(a); });
  } else if (nome === "escritorio") {
    const piso = new THREE.Mesh(new THREE.BoxGeometry(30, 0.2, 20), MAT("#d8c6a8")); piso.position.y = -0.1; piso.receiveShadow = true; g.add(piso);
    const parede = new THREE.Mesh(new THREE.BoxGeometry(30, 12, 0.3), MAT("#e9edf2")); parede.position.set(0, 6, -6); parede.receiveShadow = true; g.add(parede);
    const faixa = new THREE.Mesh(new THREE.BoxGeometry(30, 0.4, 0.32), MAT("#1f2b42")); faixa.position.set(0, 2.2, -5.95); g.add(faixa);
    const janela = new THREE.Mesh(new THREE.BoxGeometry(5, 3, 0.1), MAT("#bcd7ee", 0.2)); janela.position.set(-6, 6, -5.8); g.add(janela);
  } else { // estudio
    const piso = new THREE.Mesh(new THREE.CylinderGeometry(12, 12, 0.3, 56), MAT("#e6ebef")); piso.position.y = -0.15; piso.receiveShadow = true; g.add(piso);
  }
  g.userData.ceu = nome === "estudio" ? (marca.fundoEstudio || "#dfe6ec") : C.ceu;
  return g;
}
