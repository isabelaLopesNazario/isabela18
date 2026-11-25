// Elenco da animação PHcont (estilo bloquinho low-poly, como as refs IMEPPI e o elenco feito pela equipe).
// Uso: import { criarBoneco, PERSONAGENS } from "./elenco.js";
import * as THREE from "./lib/three.module.js";

export const MAT = (c, r = 0.85) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: 0 });
const BASIC = (c) => new THREE.MeshBasicMaterial({ color: c });

export const PERSONAGENS = {
  empresario: { pele: "#c8956b", camisa: "#d8463c", calca: "#2b3140", sapato: "#4a3326", cabelo: "#2a1d14", oculos: false, terno: false, cracha: false },
  contador:   { pele: "#7a4a2e", camisa: "#1f2b42", calca: "#1f2b42", sapato: "#3a2a20", cabelo: "#1d140e", oculos: true,  terno: true,  cracha: false },
  atendente:  { pele: "#8d5a3b", camisa: "#3aa35a", calca: "#2b3140", sapato: "#3a2a20", cabelo: "#1d140e", oculos: false, terno: false, cracha: true },
  concorrente:{ pele: "#e2b48e", camisa: "#e08a2e", calca: "#3a3f4c", sapato: "#4a3326", cabelo: "#6b4428", oculos: false, terno: false, cracha: false },
};

export function criarBoneco(tipo = "empresario") {
  const P = PERSONAGENS[tipo];
  const g = new THREE.Group();
  const corpo = new THREE.Group(); g.add(corpo);
  const tronco = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.5, 0.62), MAT(P.camisa)); tronco.position.y = 1.95; corpo.add(tronco);
  if (P.terno) {
    const camisaB = new THREE.Mesh(new THREE.BoxGeometry(0.34, 1.0, 0.02), MAT("#f2efe8")); camisaB.position.set(0, 2.2, 0.32); corpo.add(camisaB);
    const gravata = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.85, 0.03), MAT("#c9ad6e", 0.5)); gravata.position.set(0, 2.15, 0.34); corpo.add(gravata);
    for (const sx of [-1, 1]) {
      const lapela = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.7, 0.03), MAT("#16203a")); lapela.position.set(sx * 0.22, 2.35, 0.335); lapela.rotation.z = sx * 0.35; corpo.add(lapela);
    }
  }
  if (P.cracha) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.26, 0.02), BASIC("#ffffff")); c.position.set(0.3, 2.3, 0.32); corpo.add(c); }
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
    const mao = new THREE.Mesh(new THREE.SphereGeometry(0.19, 14, 10), MAT(P.pele)); mao.position.y = -1.25; b.add(mao);
    b.userData.mao = mao;
    corpo.add(b); bracos.push(b);
  }
  const cab = new THREE.Group(); cab.position.y = 3.7; corpo.add(cab);
  cab.add(new THREE.Mesh(new THREE.SphereGeometry(0.88, 32, 24), MAT(P.pele, 0.7)));
  // cabelo: cobre topo, laterais e nuca, com franja de lado (como o elenco v2 da equipe)
  const cabelo = new THREE.Mesh(new THREE.SphereGeometry(0.915, 32, 24, 0, Math.PI * 2, 0, Math.PI * 0.47), MAT(P.cabelo));
  cabelo.rotation.x = -0.42; cab.add(cabelo);
  const franja = new THREE.Mesh(new THREE.SphereGeometry(0.5, 20, 14), MAT(P.cabelo));
  franja.scale.set(1.05, 0.33, 0.7); franja.position.set(0.2, 0.55, 0.6); franja.rotation.z = -0.35; cab.add(franja);

  const olhos = [];
  for (const sx of [-0.3, 0.3]) {
    const br = new THREE.Mesh(new THREE.SphereGeometry(0.23, 24, 16), BASIC("#ffffff")); br.position.set(sx, 0.08, 0.74); br.scale.set(0.95, 1.1, 0.5); cab.add(br);
    const pu = new THREE.Mesh(new THREE.SphereGeometry(0.11, 16, 12), BASIC("#111111")); pu.position.set(sx, 0.06, 0.85); pu.scale.set(1, 1.15, 0.5); cab.add(pu);
    const sob = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.07, 0.06), BASIC(P.cabelo)); sob.position.set(sx, 0.42, 0.78); sob.rotation.z = sx < 0 ? 0.1 : -0.1; cab.add(sob);
    olhos.push({ br, pu, sob });
  }
  if (P.oculos) {
    for (const sx of [-0.3, 0.3]) {
      const aro = new THREE.Mesh(new THREE.TorusGeometry(0.25, 0.035, 8, 28), BASIC("#111111")); aro.position.set(sx, 0.08, 0.9); cab.add(aro);
    }
    const ponte = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.03, 0.03), BASIC("#111111")); ponte.position.set(0, 0.12, 0.92); cab.add(ponte);
  }
  // boca: sorriso fechado (pode virar "aberta" via escala)
  const boca = new THREE.Mesh(new THREE.TorusGeometry(0.17, 0.035, 8, 20, Math.PI), BASIC("#6b2a20"));
  boca.rotation.z = Math.PI; boca.position.set(0.03, -0.33, 0.8); cab.add(boca);

  g.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });
  return { g, corpo, cab, bracos, pernas, olhos, boca, tipo };
}

// --- adereços
export function vareta() {
  const v = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.05, 2.2, 10), MAT("#b9bcc2", 0.4));
  v.castShadow = true; return v;
}
export function lupa() {
  const g = new THREE.Group();
  const aro = new THREE.Mesh(new THREE.TorusGeometry(0.75, 0.11, 12, 40), MAT("#9ea3ab", 0.35)); g.add(aro);
  const vidro = new THREE.Mesh(new THREE.CircleGeometry(0.72, 40), new THREE.MeshStandardMaterial({ color: "#cfe6f5", transparent: true, opacity: 0.35, roughness: 0.05 })); g.add(vidro);
  const cabo = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.12, 1.2, 12), MAT("#1b1b1b")); cabo.position.set(0, -1.35, 0); g.add(cabo);
  g.traverse((m) => { if (m.isMesh) m.castShadow = true; });
  return g;
}
export function quadro(texturaCanvas) {
  const g = new THREE.Group();
  const placa = new THREE.Mesh(new THREE.BoxGeometry(4.4, 2.7, 0.12), MAT("#8a8f96"));
  placa.position.y = 3.2; g.add(placa);
  const tela = new THREE.Mesh(new THREE.PlaneGeometry(4.15, 2.45), texturaCanvas ? new THREE.MeshBasicMaterial({ map: texturaCanvas }) : BASIC("#ffffff"));
  tela.position.set(0, 3.2, 0.07); g.add(tela);
  for (const [x, rz] of [[-1.4, 0.18], [1.4, -0.18], [0, 0]]) {
    const pe = new THREE.Mesh(new THREE.BoxGeometry(0.1, 2.3, 0.1), MAT("#5f646b"));
    pe.position.set(x, 1.0, x === 0 ? -0.35 : 0); pe.rotation.z = rz; if (x === 0) pe.rotation.x = -0.18; g.add(pe);
  }
  g.traverse((m) => { if (m.isMesh) m.castShadow = true; });
  g.userData.tela = tela;
  return g;
}
