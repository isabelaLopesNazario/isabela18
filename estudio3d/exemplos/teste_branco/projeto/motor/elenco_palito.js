// Boneco palito: cabeça grande, membros finos, expressões grandes. Mesma interface do elenco.js
// (g, corpo, cab, bracos[].userData.mao, pernas, olhos[{br,pu,sob}], bocas{...}) para as poses funcionarem iguais.
import * as THREE from "./lib/three.module.js";
import { MAT, PERSONAGENS } from "./elenco.js";
const BASIC = (c) => new THREE.MeshBasicMaterial({ color: c });

export function criarPalito(tipo = "empresario", sobrescrever = {}) {
  const P = { ...(PERSONAGENS[tipo] || PERSONAGENS.empresario), ...sobrescrever };
  const membro = P.membro || "#2a2f3a";
  const g = new THREE.Group();
  const corpo = new THREE.Group(); g.add(corpo);
  // tronco fino em cápsula (cor da roupa)
  const tronco = new THREE.Mesh(new THREE.CapsuleGeometry(0.34, 0.95, 8, 18), MAT(P.camisa)); tronco.position.y = 2.15; corpo.add(tronco);
  if (P.terno || P.menina) { const gr = new THREE.Mesh(new THREE.CapsuleGeometry(0.06, 0.55, 4, 8), MAT("#c9ad6e", 0.5)); gr.position.set(0, 2.25, 0.33); corpo.add(gr); }
  if (P.cracha) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.2, 0.02), BASIC("#ffffff")); c.position.set(0.16, 2.35, 0.34); corpo.add(c); }

  const pernas = [];
  for (const sx of [-0.17, 0.17]) {
    const p = new THREE.Group(); p.position.set(sx, 1.45, 0);
    const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.1, 1.15, 6, 10), MAT(P.calca || membro)); m.position.y = -0.7; p.add(m);
    const pe = new THREE.Mesh(new THREE.SphereGeometry(0.17, 14, 10), MAT(P.sapato)); pe.scale.set(1, 0.6, 1.6); pe.position.set(0, -1.35, 0.1); p.add(pe);
    g.add(p); pernas.push(p);
  }
  const bracos = [];
  for (const sx of [-0.42, 0.42]) {
    const b = new THREE.Group(); b.position.set(sx, 2.75, 0);
    const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.09, 1.05, 6, 10), MAT(P.terno || P.menina ? P.camisa : P.pele)); m.position.y = -0.58; b.add(m);
    const mao = new THREE.Group(); mao.position.y = -1.22; b.add(mao);
    mao.add(new THREE.Mesh(new THREE.SphereGeometry(0.16, 14, 10), MAT(P.pele)));
    b.userData.mao = mao; corpo.add(b); bracos.push(b);
  }
  const cab = new THREE.Group(); cab.position.y = 3.85; corpo.add(cab);
  cab.add(new THREE.Mesh(new THREE.SphereGeometry(1.05, 40, 30), MAT(P.pele, 0.7)));
  const cabelo = new THREE.Mesh(new THREE.SphereGeometry(1.085, 40, 30, 0, Math.PI * 2, 0, Math.PI * 0.44), MAT(P.cabelo));
  cabelo.rotation.x = -0.45; cab.add(cabelo);
  const franja = new THREE.Mesh(new THREE.SphereGeometry(0.55, 20, 14), MAT(P.cabelo)); franja.scale.set(1.3, 0.34, 0.75); franja.position.set(0.25, 0.68, 0.72); franja.rotation.z = -0.4; cab.add(franja);
  if (P.menina) {
    const tras = new THREE.Mesh(new THREE.CapsuleGeometry(0.9, 1.0, 8, 20), MAT(P.cabelo)); tras.position.set(0, -0.6, -0.42); tras.scale.set(1.15, 1, 0.55); cab.add(tras);
    for (const sx of [-1, 1]) { const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.26, 1.0, 6, 12), MAT(P.cabelo)); m.position.set(sx * 0.98, -0.5, 0.05); cab.add(m); }
  }
  if (P.oculos) {
    for (const sx of [-0.36, 0.36]) { const a = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.04, 8, 28), BASIC("#111111")); a.position.set(sx, 0.12, 1.02); cab.add(a); }
  }
  // olhos grandes com brilho, sobrancelhas grossas
  const olhos = [];
  for (const sx of [-0.36, 0.36]) {
    const br = new THREE.Mesh(new THREE.SphereGeometry(0.27, 24, 16), BASIC("#ffffff")); br.position.set(sx, 0.12, 0.88); cab.add(br);
    const pu = new THREE.Mesh(new THREE.SphereGeometry(0.14, 16, 12), BASIC("#141414")); pu.position.set(sx, 0.1, 1.0); cab.add(pu);
    const brilho = new THREE.Mesh(new THREE.SphereGeometry(0.045, 8, 6), BASIC("#ffffff")); brilho.position.set(0.05, 0.06, 0.08); pu.add(brilho);
    const sob = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.3, 4, 8), BASIC(P.cabelo)); sob.rotation.z = Math.PI / 2 + (sx < 0 ? 0.15 : -0.15); sob.position.set(sx, 0.52, 0.92); cab.add(sob);
    if (P.menina) { const c = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.04, 0.04), BASIC("#111111")); c.position.set(sx + (sx < 0 ? -0.24 : 0.24), 0.32, 0.88); c.rotation.z = sx < 0 ? 0.6 : -0.6; cab.add(c); }
    olhos.push({ br, pu, sob, sx, sobY: 0.52 });
  }
  // bocas grandes
  const sorriso = new THREE.Mesh(new THREE.TorusGeometry(0.24, 0.045, 8, 22, Math.PI), BASIC("#5a1f18")); sorriso.rotation.z = Math.PI; sorriso.position.set(0.03, -0.34, 0.96); cab.add(sorriso);
  const aberta = new THREE.Group(); aberta.position.set(0.03, -0.42, 1.0); cab.add(aberta);
  const fundo = new THREE.Mesh(new THREE.CircleGeometry(0.22, 28), BASIC("#3e0f0c")); aberta.add(fundo);
  const lingua = new THREE.Mesh(new THREE.CircleGeometry(0.11, 18), BASIC("#d9605a")); lingua.position.set(0, -0.1, 0.005); aberta.add(lingua);
  const dentes = new THREE.Mesh(new THREE.PlaneGeometry(0.28, 0.06), BASIC("#ffffff")); dentes.position.set(0, 0.15, 0.006); aberta.add(dentes);
  const triste = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.045, 8, 22, Math.PI), BASIC("#5a1f18")); triste.position.set(0.03, -0.55, 0.94); cab.add(triste);

  g.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });
  return { g, corpo, cab, bracos, pernas, olhos, bocas: { sorriso, aberta, triste }, tipo, palito: true };
}
