// Personagens em estilo "bloquinho" (cabeça redonda, corpo de blocos) com sistema de poses.
// criarBoneco(tipo) -> ator ; atualizarAtor(ator, t, acoes, andar) desenha a pose no tempo t.
import * as THREE from "./lib/three.module.js";

export const MAT = (c, r = 0.85) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: 0 });
const BASIC = (c) => new THREE.MeshBasicMaterial({ color: c });

export const PERSONAGENS = {
  empresario:  { pele: "#c8956b", camisa: "#d8463c", calca: "#2b3140", sapato: "#4a3326", cabelo: "#2a1d14" },
  contador:    { pele: "#7a4a2e", camisa: "#1f2b42", calca: "#1f2b42", sapato: "#3a2a20", cabelo: "#1d140e", oculos: true, terno: true },
  atendente:   { pele: "#8d5a3b", camisa: "#3aa35a", calca: "#2b3140", sapato: "#3a2a20", cabelo: "#1d140e", cracha: true },
  concorrente: { pele: "#e2b48e", camisa: "#e08a2e", calca: "#3a3f4c", sapato: "#4a3326", cabelo: "#6b4428" },
  consultora:  { pele: "#d9a07a", camisa: "#1f2b42", calca: "#1f2b42", sapato: "#7a2a33", cabelo: "#5a3420", menina: true },
  cliente:     { pele: "#a86c48", camisa: "#5b6bd6", calca: "#2b3140", sapato: "#3a2a20", cabelo: "#2a1d14", menina: true },
};

export function criarBoneco(tipo = "empresario", sobrescrever = {}) {
  const P = { ...(PERSONAGENS[tipo] || PERSONAGENS.empresario), ...sobrescrever };
  const g = new THREE.Group();
  const corpo = new THREE.Group(); g.add(corpo);
  const tronco = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.5, 0.62), MAT(P.camisa)); tronco.position.y = 1.95; corpo.add(tronco);
  if (P.terno) {
    const cb = new THREE.Mesh(new THREE.BoxGeometry(0.34, 1.0, 0.02), MAT("#f2efe8")); cb.position.set(0, 2.2, 0.32); corpo.add(cb);
    const gr = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.85, 0.03), MAT("#c9ad6e", 0.5)); gr.position.set(0, 2.15, 0.34); corpo.add(gr);
    for (const sx of [-1, 1]) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.7, 0.03), MAT("#16203a")); l.position.set(sx * 0.22, 2.35, 0.335); l.rotation.z = sx * 0.35; corpo.add(l); }
  }
  if (P.cracha) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.26, 0.02), BASIC("#ffffff")); c.position.set(0.3, 2.3, 0.32); corpo.add(c); }
  if (P.menina) {
    const gola = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.45, 3), MAT("#f2efe8")); gola.rotation.z = Math.PI; gola.position.set(0, 2.5, 0.315); gola.scale.z = 0.05; corpo.add(gola);
    const faixa = new THREE.Mesh(new THREE.BoxGeometry(1.16, 0.08, 0.64), MAT("#c9ad6e", 0.4)); faixa.position.y = 1.4; corpo.add(faixa);
  }
  const pescoco = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.19, 0.35, 10), MAT(P.pele)); pescoco.position.y = 2.85; corpo.add(pescoco);

  const pernas = [];
  for (const sx of [-0.28, 0.28]) {
    const p = new THREE.Group(); p.position.set(sx, 1.2, 0);
    const m = new THREE.Mesh(new THREE.BoxGeometry(0.4, 1.1, 0.44), MAT(P.calca)); m.position.y = -0.55; p.add(m);
    const pe = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.24, 0.66), MAT(P.sapato)); pe.position.set(0, -1.08, 0.1); p.add(pe);
    g.add(p); pernas.push(p);
  }
  const bracos = [];
  for (const sx of [-0.73, 0.73]) {
    const b = new THREE.Group(); b.position.set(sx, 2.6, 0);
    const m = new THREE.Mesh(new THREE.BoxGeometry(0.3, 1.2, 0.34), MAT(P.camisa)); m.position.y = -0.58; b.add(m);
    const mao = new THREE.Group(); mao.position.y = -1.25; b.add(mao);
    mao.add(new THREE.Mesh(new THREE.SphereGeometry(0.19, 14, 10), MAT(P.pele)));
    b.userData.mao = mao;
    corpo.add(b); bracos.push(b);
  }
  const cab = new THREE.Group(); cab.position.y = 3.7; corpo.add(cab);
  cab.add(new THREE.Mesh(new THREE.SphereGeometry(0.88, 32, 24), MAT(P.pele, 0.7)));
  const cabelo = new THREE.Mesh(new THREE.SphereGeometry(0.915, 32, 24, 0, Math.PI * 2, 0, Math.PI * 0.47), MAT(P.cabelo));
  cabelo.rotation.x = -0.42; cab.add(cabelo);
  const franja = new THREE.Mesh(new THREE.SphereGeometry(0.5, 20, 14), MAT(P.cabelo));
  franja.scale.set(1.05, 0.33, 0.7); franja.position.set(0.2, 0.55, 0.6); franja.rotation.z = -0.35; cab.add(franja);
  if (P.menina) {
    const tras = new THREE.Mesh(new THREE.CapsuleGeometry(0.78, 1.1, 8, 20), MAT(P.cabelo)); tras.position.set(0, -0.55, -0.32); tras.scale.set(1.15, 1, 0.6); cab.add(tras);
    for (const sx of [-1, 1]) { const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.22, 1.0, 6, 12), MAT(P.cabelo)); m.position.set(sx * 0.82, -0.45, 0.12); m.rotation.z = sx * 0.08; cab.add(m); }
    franja.scale.set(1.5, 0.4, 0.8); franja.position.set(0.12, 0.55, 0.58);
  }
  const olhos = [];
  for (const sx of [-0.3, 0.3]) {
    const br = new THREE.Mesh(new THREE.SphereGeometry(0.23, 24, 16), BASIC("#ffffff")); br.position.set(sx, 0.08, 0.74); cab.add(br);
    const pu = new THREE.Mesh(new THREE.SphereGeometry(0.11, 16, 12), BASIC("#111111")); pu.position.set(sx, 0.06, 0.85); cab.add(pu);
    const sob = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.07, 0.06), BASIC(P.cabelo)); sob.position.set(sx, 0.42, 0.78); sob.rotation.z = sx < 0 ? 0.1 : -0.1; cab.add(sob);
    if (P.menina) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.04, 0.04), BASIC("#111111")); c.position.set(sx + (sx < 0 ? -0.2 : 0.2), 0.27, 0.78); c.rotation.z = sx < 0 ? 0.6 : -0.6; cab.add(c); }
    olhos.push({ br, pu, sob, sx });
  }
  if (P.oculos) {
    for (const sx of [-0.3, 0.3]) { const a = new THREE.Mesh(new THREE.TorusGeometry(0.25, 0.035, 8, 28), BASIC("#111111")); a.position.set(sx, 0.08, 0.9); cab.add(a); }
    const pt = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.03, 0.03), BASIC("#111111")); pt.position.set(0, 0.12, 0.92); cab.add(pt);
  }
  // bocas: sorriso (arco), aberta (disco escuro), triste (arco invertido)
  const sorriso = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.035, 8, 20, Math.PI), BASIC("#6b2a20")); sorriso.rotation.z = Math.PI; sorriso.position.set(0.03, -0.3, 0.8); cab.add(sorriso);
  const aberta = new THREE.Mesh(new THREE.CircleGeometry(0.16, 24), BASIC("#4a1410")); aberta.position.set(0.03, -0.36, 0.84); aberta.scale.y = 1.2; cab.add(aberta);
  const triste = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.035, 8, 20, Math.PI), BASIC("#6b2a20")); triste.position.set(0.03, -0.45, 0.8); cab.add(triste);

  g.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });
  return { g, corpo, cab, bracos, pernas, olhos, bocas: { sorriso, aberta, triste }, tipo };
}

// ---------------------------------------------------------------- poses
// bE/bD = braço esquerdo/direito do personagem: [rotX, rotZ] ; cab = [rotX, rotY] ; boca ; olhos (escala) ; salto (altura)
export const POSES = {
  parado:    { bE: [0, -0.12], bD: [0, 0.12], cab: [0, 0], boca: "sorriso", olhos: 1, salto: 0 },
  aponta:    { bE: [0, -0.18], bD: [0, 1.4], cab: [0, 0.25], boca: "aberta", olhos: 1, salto: 0 },
  explica:   { bE: [-0.7, -0.35], bD: [-0.7, 0.35], cab: [0, 0], boca: "aberta", olhos: 1, salto: 0 },
  acena:     { bE: [0, -0.12], bD: [0, 2.6], cab: [0, 0], boca: "sorriso", olhos: 1, salto: 0, aceno: 1 },
  assustado: { bE: [-0.3, -2.4], bD: [-0.3, 2.4], cab: [-0.1, 0], boca: "aberta", olhos: 1.4, salto: 0.35 },
  pensando:  { bE: [0, -0.15], bD: [-2.1, 0.55], cab: [0.18, -0.25], boca: "triste", olhos: 1, salto: 0 },
  comemora:  { bE: [0, -2.8], bD: [0, 2.8], cab: [-0.15, 0], boca: "aberta", olhos: 1.1, salto: 0.5, pulo: 1 },
  triste:    { bE: [0, -0.05], bD: [0, 0.05], cab: [0.35, 0], boca: "triste", olhos: 0.9, salto: 0 },
  segura:    { bE: [0, -0.12], bD: [-1.3, 0.2], cab: [0.1, 0], boca: "sorriso", olhos: 1, salto: 0 },
  confuso:   { bE: [0, -0.15], bD: [-2.3, 0.9], cab: [0.1, 0.35], boca: "triste", olhos: 1.15, salto: 0 },
};
const lerp = (a, b, k) => a + (b - a) * k;
const suave = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };

function poseEm(acoes, t) {
  // acoes: [{t, pose}] ordenadas ; transição de 0,3 s
  let ant = POSES.parado, atual = POSES.parado, k = 1, tAtual = -99;
  for (const a of acoes) { if (a.t <= t) { ant = atual; atual = POSES[a.pose] || POSES.parado; tAtual = a.t; } }
  k = suave((t - tAtual) / 0.3);
  return { ant, atual, k, tAtual };
}

export function atualizarAtor(A, t, { acoes = [], andar = [], olharPara = null, base = { x: 0, z: 0, rot: 0, y: 0 } } = {}) {
  const { ant, atual, k, tAtual } = poseEm(acoes, t);
  const mix = (c, i) => lerp(ant[c][i], atual[c][i], k);
  // deslocamento (andar): [{t0, t1, de:[x,z], para:[x,z]}]
  let x = base.x, z = base.z, rot = base.rot, andando = false;
  for (const w of andar) {
    if (t >= w.t0) {
      const u = Math.min(1, (t - w.t0) / Math.max(0.01, w.t1 - w.t0));
      x = lerp(w.de[0], w.para[0], u); z = lerp(w.de[1], w.para[1], u);
      if (u < 1) { andando = true; rot = Math.atan2(w.para[0] - w.de[0], w.para[1] - w.de[1]); }
      else rot = w.rotFinal ?? base.rot;
    }
  }
  A.g.position.x = x; A.g.position.z = z; A.g.rotation.y = rot;
  const passo = andando ? Math.sin(t * 9) : 0;
  A.pernas[0].rotation.x = passo * 0.55; A.pernas[1].rotation.x = -passo * 0.55;

  const desdeAcao = t - tAtual;
  let salto = lerp(ant.salto, atual.salto, k) * Math.sin(Math.PI * Math.min(1, Math.max(0, desdeAcao / 0.45)));
  if (atual.pulo) salto = Math.abs(Math.sin(desdeAcao * 7)) * 0.45;
  A.g.position.y = (base.y || 0) + salto + (andando ? Math.abs(passo) * 0.06 : 0);

  A.bracos[0].rotation.x = mix("bE", 0) + (andando ? -passo * 0.5 : 0);
  A.bracos[0].rotation.z = mix("bE", 1);
  A.bracos[1].rotation.x = mix("bD", 0) + (andando ? passo * 0.5 : 0);
  A.bracos[1].rotation.z = mix("bD", 1) + (atual.aceno ? Math.sin(t * 10) * 0.35 * k : 0);
  A.cab.rotation.x = mix("cab", 0);
  A.cab.rotation.y = mix("cab", 1) + Math.sin(t * 1.7 + x) * 0.04;
  if (olharPara) { A.cab.rotation.y += THREE.MathUtils.clamp((olharPara[0] - x) * 0.12, -0.5, 0.5); }
  A.corpo.children[0].scale.y = 1 + Math.sin(t * 3 + z) * 0.012; // respiração

  const boca = k < 0.5 ? ant.boca : atual.boca;
  for (const [nome, m] of Object.entries(A.bocas)) m.visible = nome === boca;
  if (boca === "aberta") A.bocas.aberta.scale.set(1, 1.0 + Math.abs(Math.sin(t * 11)) * 0.35, 1);
  const pisca = (t + x * 0.37) % 3.1 > 2.97 ? 0.12 : 1;
  const ol = lerp(ant.olhos, atual.olhos, k);
  A.olhos.forEach((o) => { o.br.scale.set(ol, ol * 1.1 * pisca, 0.5); o.pu.scale.set(1, 1.15 * pisca, 0.5); o.sob.position.y = 0.42 + (ol - 1) * 0.3; });
}
