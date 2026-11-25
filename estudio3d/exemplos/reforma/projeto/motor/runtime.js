// Monta as cenas descritas em window.__ROTEIRO (já com tempos absolutos) e desenha o quadro do tempo t.
// Determinístico: tudo é função de t (exigência do HyperFrames, que busca quadro a quadro).
import * as THREE from "./lib/three.module.js";
import { criarBoneco, atualizarAtor } from "./elenco.js";
import { criarObjeto, criarCenario } from "./objetos.js";

const R = window.__ROTEIRO;
const W = R.largura || 1080, H = R.altura || 1920;
const canvas = document.getElementById("cena");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const ease = (x) => { x = Math.min(1, Math.max(0, x)); return 1 - Math.pow(1 - x, 3); };
const suave = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
const back = (x) => { x = Math.min(1, Math.max(0, x)); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const quique = (x) => { x = Math.min(1, Math.max(0, x)); if (x < 0.6) return (x / 0.6) ** 2; const u = (x - 0.6) / 0.4; return 1 - Math.sin(Math.PI * u) * 0.12 * (1 - u); };

function montarCena(C) {
  const scene = new THREE.Scene();
  const cen = criarCenario(C.cenario || "praca", R.marca || {});
  scene.background = new THREE.Color(cen.userData.ceu);
  scene.fog = new THREE.Fog(cen.userData.ceu, 40, 90);
  scene.add(cen);
  scene.add(new THREE.HemisphereLight("#ffffff", "#c2ccd6", 1.9));
  const sol = new THREE.DirectionalLight("#fff8ec", 2.3); sol.position.set(6, 16, 14);
  sol.castShadow = true; sol.shadow.mapSize.set(2048, 2048);
  Object.assign(sol.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16 }); scene.add(sol);

  const atores = (C.atores || []).map((a) => {
    const A = criarBoneco(a.tipo, a.cores || {});
    A.g.scale.setScalar(a.escala || 1);
    if (a.segura) {
      const o = criarObjeto(a.segura.tipo, a.segura.props || {});
      o.scale.setScalar(a.segura.escala || 0.5);
      if (a.segura.tipo === "vareta") { o.position.set(0, -0.8, 0); }
      else if (a.segura.tipo === "lupa") { o.position.set(0, -0.2, 0.25); o.rotation.set(1.45, 0, -0.5); }
      else { o.position.set(0, -0.1, 0.35); o.rotation.x = Math.PI / 2; }
      A.bracos[a.segura.mao === "E" ? 0 : 1].userData.mao.add(o);
    }
    scene.add(A.g);
    return { def: a, A };
  });

  const objetos = (C.objetos || []).map((o) => {
    const grupo = new THREE.Group();
    const obj = criarObjeto(o.tipo, o.props || {});
    grupo.add(obj); scene.add(grupo);
    const [x = 0, y = 0, z = 0] = o.pos || [];
    grupo.position.set(x, y, z);
    if (o.rot) grupo.rotation.set(...o.rot);
    // poeira para a saída "some"
    const poeira = new THREE.Group(); poeira.position.set(x, y + (o.alturaPoeira ?? 1.5), z); scene.add(poeira);
    for (let k = 0; k < 8; k++) {
      const p = new THREE.Mesh(new THREE.IcosahedronGeometry(0.35, 0), new THREE.MeshStandardMaterial({ color: "#ffffff", roughness: 1, transparent: true, opacity: 0, flatShading: true }));
      p.userData.a = (k / 8) * Math.PI * 2; poeira.add(p);
    }
    return { def: o, grupo, obj, poeira, base: new THREE.Vector3(x, y, z) };
  });

  const cam = new THREE.PerspectiveCamera(C.camera?.fov || 36, W / H, 0.1, 300);
  // enquadramento automático: cabe tudo (atores + objetos) com margem, se o roteiro não fixar a distância
  const c = (C.camera = C.camera || {});
  if (c.dist == null && c.dist0 == null && c.dist1 == null) {
    const caixa = new THREE.Box3();
    scene.updateMatrixWorld(true);
    for (const a of atores) {
      const p = a.def.pos || [0, 0], fim = (a.def.andar || []).slice(-1)[0];
      a.A.g.position.set(p[0], a.def.alt || 0, p[1]); a.A.g.rotation.y = a.def.rot || 0; a.A.g.updateMatrixWorld(true);
      caixa.expandByObject(a.A.g);
      if (fim) { a.A.g.position.set(fim.para[0], a.def.alt || 0, fim.para[1]); a.A.g.updateMatrixWorld(true); caixa.expandByObject(a.A.g); }
    }
    for (const o of objetos) { if (o.def.fora) continue; caixa.expandByObject(o.grupo); }
    if (!caixa.isEmpty()) {
      const centro = caixa.getCenter(new THREE.Vector3()), tam = caixa.getSize(new THREE.Vector3());
      const fovV = THREE.MathUtils.degToRad(cam.fov) / 2, fovH = Math.atan(Math.tan(fovV) * cam.aspect);
      const margem = c.margem ?? 1.06;
      // a legenda ocupa a parte de baixo: o conteúdo fica na parte de cima/meio do quadro
      const meiaL = (tam.x / 2) * margem + 0.35, meiaA = (tam.y / 2) * margem + 0.5;
      const d = Math.max(meiaL / Math.tan(fovH), meiaA / Math.tan(fovV)) + tam.z / 2;
      c.dist1 = d; c.dist0 = d * (c.aproxima === false ? 1 : 1.12);
      c.alvo = c.alvo || [centro.x, centro.y - tam.y * 0.08, centro.z];
      c.altura = c.altura ?? centro.y + d * 0.18;
    }
  }
  return { C, scene, cam, atores, objetos };
}

const CENAS = R.cenas.map(montarCena);

function atualizarObjeto(O, t) {
  const d = O.def, e = d.entra || { t: -1, modo: "nenhum" }, s = d.sai;
  const esc = d.escala || 1;
  let k = 1, dy = 0, rz = 0, rx = 0, dx = 0;
  const u = (t - e.t) / (e.dur || 0.45);
  if (t < e.t && e.modo !== "nenhum") k = 0.0001;
  else if (e.modo === "surge") k = Math.max(0.0001, back(u));
  else if (e.modo === "cai") { dy = (1 - quique(u)) * 7; }
  else if (e.modo === "sobe") { dy = -(1 - ease(u)) * 4; k = Math.max(0.0001, ease(u * 1.5)); }
  else if (e.modo === "desliza") { dx = -(1 - ease(u)) * 10; }
  if (s && t >= s.t) {
    const v = (t - s.t) / (s.dur || 0.35);
    if (s.modo === "some") k = Math.max(0.0001, 1 - ease(v));
    else if (s.modo === "cai") { rz = ease(v) * 1.4 * (d.lado || 1); dy = -ease(v) * 0.4; k = Math.max(0.0001, 1 - ease((v - 0.6) * 2.5)); }
    const w = (t - s.t) / 0.6;
    O.poeira.children.forEach((m) => {
      const on = s.modo === "some" && w > 0 && w < 1;
      m.material.opacity = on ? 0.9 * (1 - w) : 0;
      const r = 0.3 + ease(w) * 1.5;
      m.position.set(Math.cos(m.userData.a) * r, Math.sin(m.userData.a) * r * 0.6 + ease(w) * 0.5, 0);
      m.scale.setScalar(on ? 0.6 + w * 0.8 : 0.0001);
    });
  }
  // animações contínuas / pontuais
  let ry = 0, bob = 0;
  for (const a of d.anim || []) {
    if (a.tipo === "gira") ry += (t - (a.t || 0)) * (a.vel || 1.5);
    if (a.tipo === "flutua") bob += Math.sin(t * (a.vel || 2.2)) * (a.amp || 0.15);
    if (a.tipo === "inclina" && O.obj.userData.prancha) {
      const lista = (d.anim || []).filter((b) => b.tipo === "inclina" && b.t <= t);
      const atual = lista.length ? lista[lista.length - 1] : null;
      const antes = lista.length > 1 ? lista[lista.length - 2].ang : 0;
      if (atual) O.obj.userData.prancha.rotation.z = antes + (atual.ang - antes) * back((t - atual.t) / 0.6);
    }
    if (a.tipo === "pulsa" && t >= a.t) { const p = 1 + Math.sin((t - a.t) * 8) * 0.06; k *= p; }
  }
  O.grupo.scale.setScalar(esc * k);
  O.grupo.position.set(O.base.x + dx, O.base.y + dy + bob, O.base.z);
  O.grupo.rotation.z = (d.rot?.[2] || 0) + rz;
  O.grupo.rotation.x = (d.rot?.[0] || 0) + rx;
  O.grupo.rotation.y = (d.rot?.[1] || 0) + ry;
}

function atualizarCamera(S, t) {
  const c = S.C.camera || {}, C = S.C;
  const u = suave((t - C.t0) / Math.max(0.1, C.t1 - C.t0));
  const alvo = c.alvo || [0, 3, 0];
  const ang = (c.ang0 ?? -0.15) + ((c.ang1 ?? 0.15) - (c.ang0 ?? -0.15)) * u;
  const dist = (c.dist0 ?? c.dist ?? 18) + ((c.dist1 ?? c.dist ?? 18) - (c.dist0 ?? c.dist ?? 18)) * u;
  const alt = (c.alt0 ?? c.altura ?? 6.5) + ((c.alt1 ?? c.altura ?? 6.5) - (c.alt0 ?? c.altura ?? 6.5)) * u;
  // "soco" de zoom na entrada da cena (leve)
  const soco = c.soco === false ? 0 : (1 - ease((t - C.t0) / 0.5)) * 1.2;
  S.cam.position.set(alvo[0] + Math.sin(ang) * (dist + soco), alt, alvo[2] + Math.cos(ang) * (dist + soco));
  S.cam.lookAt(alvo[0], alvo[1], alvo[2]);
}

function renderAt(t) {
  let S = CENAS[0];
  for (const c of CENAS) if (t >= c.C.t0) S = c;
  for (const a of S.atores) atualizarAtor(a.A, t, { acoes: a.def.acoes || [], andar: a.def.andar || [], olharPara: a.def.olhar || null, base: { x: a.def.pos?.[0] || 0, z: a.def.pos?.[1] || 0, rot: a.def.rot || 0, y: a.def.alt || 0 } });
  for (const o of S.objetos) atualizarObjeto(o, t);
  atualizarCamera(S, t);
  renderer.render(S.scene, S.cam);
}

window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
renderAt(0);
