// Boneco no padrão do vídeo de referência da PHCont: corpo de blocos, cabeça redonda bem grande, contorno escuro fino,
// olhos grandes, crachá branco no peito. Mesma interface do elenco.js (as poses funcionam iguais).
import * as THREE from "./lib/three.module.js";
import { PERSONAGENS } from "./elenco.js";

const STD = (c, r = 0.72) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: 0 });
const BASIC = (c) => new THREE.MeshBasicMaterial({ color: c });
const TINTA = new THREE.MeshBasicMaterial({ color: "#1b1e26", side: THREE.BackSide });

// contorno: casca escura um pouco maior, só com as faces de trás
export function contornar(raiz, esp = 0.035) {
  const lista = [];
  raiz.traverse((m) => { if (m.isMesh && !m.userData.semContorno) lista.push(m); });
  for (const m of lista) {
    m.geometry.computeBoundingBox();
    const t = m.geometry.boundingBox.getSize(new THREE.Vector3());
    const c = m.geometry.boundingBox.getCenter(new THREE.Vector3());
    const h = new THREE.Mesh(m.geometry, TINTA);
    h.userData.semContorno = true; h.userData.contorno = true;
    h.scale.set((t.x + esp * 2) / Math.max(t.x, 1e-3), (t.y + esp * 2) / Math.max(t.y, 1e-3), (t.z + esp * 2) / Math.max(t.z, 1e-3));
    h.position.copy(c).multiply(new THREE.Vector3(1 - h.scale.x, 1 - h.scale.y, 1 - h.scale.z));
    h.castShadow = false;
    m.add(h);
  }
}

const caixa = (w, h, d) => new THREE.BoxGeometry(w, h, d);

export function criarPH(tipo = "empresario", sobrescrever = {}) {
  const P = { ...(PERSONAGENS[tipo] || PERSONAGENS.empresario), ...sobrescrever };
  const g = new THREE.Group();
  const corpo = new THREE.Group(); g.add(corpo);

  // tronco: bloco de ombros retos
  const tronco = new THREE.Mesh(caixa(1.2, 1.35, 0.72), STD(P.camisa)); tronco.position.y = 2.18; corpo.add(tronco);
  if (P.terno || P.menina) {
    const camisa = new THREE.Mesh(caixa(0.3, 0.9, 0.02), STD("#f4f2ee")); camisa.position.set(0, 2.45, 0.37); camisa.userData.semContorno = true; corpo.add(camisa);
    const gr = new THREE.Mesh(caixa(0.12, 0.8, 0.03), STD("#d9b85a", 0.5)); gr.position.set(0, 2.38, 0.385); gr.userData.semContorno = true; corpo.add(gr);
  } else {
    // crachá branco no peito
    const cr = new THREE.Mesh(caixa(0.16, 0.22, 0.02), BASIC("#ffffff")); cr.position.set(0.3, 2.45, 0.37); cr.userData.semContorno = true; corpo.add(cr);
  }
  // pernas: blocos finos escuros, sapatos marrons
  const pernas = [];
  for (const sx of [-0.27, 0.27]) {
    const p = new THREE.Group(); p.position.set(sx, 1.52, 0);
    const m = new THREE.Mesh(caixa(0.34, 1.3, 0.38), STD(P.calca)); m.position.y = -0.65; p.add(m);
    const pe = new THREE.Mesh(caixa(0.38, 0.22, 0.6), STD(P.sapato)); pe.position.set(0, -1.38, 0.1); p.add(pe);
    g.add(p); pernas.push(p);
  }
  // braços: blocos finos da cor da roupa, mão redonda
  const bracos = [];
  for (const sx of [-0.73, 0.73]) {
    const b = new THREE.Group(); b.position.set(sx, 2.72, 0);
    const m = new THREE.Mesh(caixa(0.26, 1.15, 0.3), STD(P.camisa)); m.position.y = -0.55; b.add(m);
    const mao = new THREE.Group(); mao.position.y = -1.2; b.add(mao);
    mao.add(new THREE.Mesh(new THREE.SphereGeometry(0.17, 16, 12), STD(P.pele)));
    b.userData.mao = mao; corpo.add(b); bracos.push(b);
  }
  // cabeça grande apoiada direto no tronco
  const cab = new THREE.Group(); cab.position.y = 3.72; corpo.add(cab);
  cab.add(new THREE.Mesh(new THREE.SphereGeometry(1.0, 40, 30), STD(P.pele, 0.65)));
  const cabelo = new THREE.Mesh(new THREE.SphereGeometry(1.035, 40, 30, 0, Math.PI * 2, 0, Math.PI * 0.42), STD(P.cabelo, 0.8));
  cabelo.rotation.x = -0.5; cabelo.rotation.z = 0.08; cab.add(cabelo);
  const topete = new THREE.Mesh(new THREE.SphereGeometry(0.5, 20, 14), STD(P.cabelo, 0.8)); topete.scale.set(1.35, 0.32, 0.8); topete.position.set(-0.22, 0.72, 0.62); topete.rotation.z = 0.35; topete.userData.semContorno = true; cab.add(topete);
  if (P.menina) {
    const tras = new THREE.Mesh(new THREE.CapsuleGeometry(0.88, 1.0, 8, 20), STD(P.cabelo, 0.8)); tras.position.set(0, -0.55, -0.4); tras.scale.set(1.15, 1, 0.55); cab.add(tras);
    for (const sx of [-1, 1]) { const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.24, 1.0, 6, 12), STD(P.cabelo, 0.8)); m.position.set(sx * 0.94, -0.48, 0.05); cab.add(m); }
  }
  // olhos grandes (brancos achatados), pupila preta com brilho
  const olhos = [];
  for (const sx of [-0.34, 0.34]) {
    const br = new THREE.Mesh(new THREE.SphereGeometry(0.25, 24, 16), BASIC("#ffffff")); br.position.set(sx, 0.1, 0.87); br.userData.semContorno = true; cab.add(br);
    const anel = new THREE.Mesh(new THREE.TorusGeometry(0.25, 0.022, 6, 28), BASIC("#1b1e26")); anel.position.set(0, 0, 0.02); br.add(anel);
    const pu = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), BASIC("#14161c")); pu.position.set(sx + 0.03, 0.08, 1.0); pu.userData.semContorno = true; cab.add(pu);
    const brilho = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 6), BASIC("#ffffff")); brilho.position.set(0.04, 0.05, 0.08); pu.add(brilho);
    const sob = new THREE.Mesh(caixa(0.34, 0.08, 0.06), BASIC("#1b1e26")); sob.position.set(sx, 0.47, 0.88); sob.rotation.z = sx < 0 ? 0.12 : -0.12; sob.userData.semContorno = true; cab.add(sob);
    if (P.menina) { const c = new THREE.Mesh(caixa(0.12, 0.04, 0.04), BASIC("#1b1e26")); c.position.set(sx + (sx < 0 ? -0.22 : 0.22), 0.3, 0.86); c.rotation.z = sx < 0 ? 0.6 : -0.6; c.userData.semContorno = true; cab.add(c); }
    olhos.push({ br, pu, sob, sx, sobY: 0.47 });
  }
  if (P.oculos) {
    for (const sx of [-0.34, 0.34]) { const a = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.055, 8, 30), BASIC("#14161c")); a.position.set(sx, 0.1, 1.0); a.userData.semContorno = true; cab.add(a); }
    const pt = new THREE.Mesh(caixa(0.12, 0.05, 0.04), BASIC("#14161c")); pt.position.set(0, 0.14, 1.02); pt.userData.semContorno = true; cab.add(pt);
  }
  // bocas
  const sorriso = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.04, 8, 22, Math.PI), BASIC("#1b1e26")); sorriso.rotation.z = Math.PI; sorriso.position.set(0.04, -0.3, 0.92); cab.add(sorriso);
  const aberta = new THREE.Group(); aberta.position.set(0.04, -0.38, 0.95); cab.add(aberta);
  const fundo = new THREE.Mesh(new THREE.CircleGeometry(0.2, 28, Math.PI, Math.PI), BASIC("#3a1412")); aberta.add(fundo);
  const dentes = new THREE.Mesh(new THREE.PlaneGeometry(0.34, 0.06), BASIC("#ffffff")); dentes.position.set(0, -0.03, 0.005); aberta.add(dentes);
  const lingua = new THREE.Mesh(new THREE.CircleGeometry(0.09, 16), BASIC("#d9605a")); lingua.position.set(0, -0.14, 0.004); aberta.add(lingua);
  const triste = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.04, 8, 22, Math.PI), BASIC("#1b1e26")); triste.position.set(0.04, -0.5, 0.9); cab.add(triste);
  [sorriso, triste, fundo, dentes, lingua].forEach((m) => (m.userData.semContorno = true));

  contornar(g);
  g.traverse((m) => { if (m.isMesh && !m.userData.contorno) { m.castShadow = true; m.receiveShadow = false; } });
  return { g, corpo, cab, bracos, pernas, olhos, bocas: { sorriso, aberta, triste }, tipo, ph: true };
}
