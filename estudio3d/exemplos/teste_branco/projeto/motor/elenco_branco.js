// Boneco branco 3D (referências "homenzinho branco"): liso, sem rosto, cabeça grande, mãos de luva, pés arredondados.
// A expressão vem do corpo (poses). Acessórios: óculos, gravata, cor de destaque. Mesma interface do elenco.js.
import * as THREE from "./lib/three.module.js";
import { PERSONAGENS } from "./elenco.js";

const BRANCO = () => new THREE.MeshStandardMaterial({ color: "#f1f1ef", roughness: 0.55, metalness: 0 });

// tronco liso em forma de pera (mais largo no quadril), feito por revolução
function troncoGeo() {
  const pts = [];
  const perfil = [[0, 0], [0.5, 0.02], [0.62, 0.25], [0.64, 0.6], [0.6, 1.0], [0.55, 1.35], [0.45, 1.6], [0.3, 1.75], [0.22, 1.85], [0.2, 2.0], [0, 2.02]];
  for (const [r, y] of perfil) pts.push(new THREE.Vector2(r, y));
  const g = new THREE.LatheGeometry(new THREE.SplineCurve(pts).getPoints(40), 40);
  g.scale(1, 1, 0.82);
  return g;
}

function maoLuva(mat, lado) {
  const m = new THREE.Group();
  const palma = new THREE.Mesh(new THREE.SphereGeometry(0.2, 20, 14), mat); palma.scale.set(0.85, 1.15, 0.55); palma.position.y = -0.08; m.add(palma);
  for (let i = 0; i < 4; i++) {
    const d = new THREE.Mesh(new THREE.CapsuleGeometry(0.045, 0.16, 4, 8), mat);
    d.position.set(-0.11 + i * 0.075, -0.3 - (i === 1 || i === 2 ? 0.02 : 0), 0); m.add(d);
  }
  const pol = new THREE.Mesh(new THREE.CapsuleGeometry(0.055, 0.12, 4, 8), mat);
  pol.position.set(lado * 0.17, -0.1, 0.06); pol.rotation.z = lado * 0.7; m.add(pol);
  return m;
}

export function criarBranco(tipo = "empresario", sobrescrever = {}) {
  const P = { ...(PERSONAGENS[tipo] || PERSONAGENS.empresario), ...sobrescrever };
  const mat = BRANCO();
  const g = new THREE.Group();
  const corpo = new THREE.Group(); g.add(corpo);
  const tronco = new THREE.Mesh(troncoGeo(), mat); tronco.position.y = 1.15; tronco.scale.setScalar(0.95); corpo.add(tronco);

  const pernas = [];
  for (const sx of [-0.26, 0.26]) {
    const p = new THREE.Group(); p.position.set(sx, 1.35, 0);
    const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.25, 0.85, 8, 16), mat); m.position.y = -0.55; p.add(m);
    const pe = new THREE.Mesh(new THREE.SphereGeometry(0.3, 20, 14), mat); pe.scale.set(0.95, 0.55, 1.45); pe.position.set(0, -1.17, 0.14); p.add(pe);
    g.add(p); pernas.push(p);
  }
  const bracos = [];
  for (const [sx, lado] of [[-0.5, -1], [0.5, 1]]) {
    const b = new THREE.Group(); b.position.set(sx, 2.72, 0);
    const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.15, 0.9, 8, 14), mat); m.position.y = -0.52; b.add(m);
    const mao = new THREE.Group(); mao.position.y = -1.08; b.add(mao);
    mao.add(maoLuva(mat, lado));
    b.userData.mao = mao; corpo.add(b); bracos.push(b);
  }
  const cab = new THREE.Group(); cab.position.y = 3.95; corpo.add(cab);
  cab.add(new THREE.Mesh(new THREE.SphereGeometry(1.08, 48, 36), mat));

  // acessórios
  const cor = P.acessorio || (P.terno || P.menina ? "#1f2b42" : null);
  if (P.terno || P.gravata) {
    const n = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.12, 0.08), new THREE.MeshStandardMaterial({ color: cor || "#222", roughness: 0.5 }));
    n.position.set(0, 2.98, 0.42); corpo.add(n);
    const gr = new THREE.Mesh(new THREE.ConeGeometry(0.15, 0.85, 4), n.material); gr.rotation.set(Math.PI, Math.PI / 4, 0); gr.scale.z = 0.35;
    gr.position.set(0, 2.5, 0.5); gr.rotation.x = Math.PI - 0.12; corpo.add(gr);
  }
  if (P.menina) { // lenço no pescoço com a cor de destaque
    const l = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.09, 10, 24), new THREE.MeshStandardMaterial({ color: P.acessorio || "#c9ad6e", roughness: 0.5 }));
    l.rotation.x = Math.PI / 2; l.position.y = 2.98; corpo.add(l);
  }
  if (P.oculos) {
    const preto = new THREE.MeshStandardMaterial({ color: "#151515", roughness: 0.35 });
    for (const sx of [-0.4, 0.4]) { const a = new THREE.Mesh(new THREE.TorusGeometry(0.33, 0.07, 10, 32), preto); a.position.set(sx * 1.05, 0.2, 1.1); a.rotation.y = sx * 0.9; cab.add(a); }
    const ponte = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.12, 4, 8), preto); ponte.rotation.z = Math.PI / 2; ponte.position.set(0, 0.24, 1.2); cab.add(ponte);
    for (const sx of [-1, 1]) { const h = new THREE.Mesh(new THREE.CapsuleGeometry(0.035, 0.8, 4, 8), preto); h.rotation.x = Math.PI / 2; h.position.set(sx * 0.74, 0.22, 0.55); cab.add(h); }
  }
  g.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });
  // sem rosto: olhos e bocas vazios (as poses mexem só no corpo)
  const vazio = () => new THREE.Group();
  return { g, corpo, cab, bracos, pernas, olhos: [], bocas: { sorriso: vazio(), aberta: vazio(), triste: vazio() }, tipo, branco: true };
}
