// Monta as cenas descritas em window.__ROTEIRO (já com tempos absolutos) e desenha o quadro do tempo t.
// Determinístico: tudo é função de t (exigência do HyperFrames, que busca quadro a quadro).
// Estilo: luz em 3 faixas (toon), borda clara na silhueta, fundo desfocado, planos de no máximo 2 s
// com a câmera sempre em movimento (geral / médio / rosto / objeto).
import * as THREE from "./lib/three.module.js";
import { criarBoneco, atualizarAtor } from "./elenco.js";
import { criarPalito } from "./elenco_palito.js";
import { criarPH, contornar } from "./elenco_ph.js";
import { criarBranco } from "./elenco_branco.js";
import { criarObjeto, criarCenario } from "./objetos.js";

const R = window.__ROTEIRO;
const W = R.largura || 1080, H = R.altura || 1920;
const ESTILO = R.estilo || "ph";          // ph (padrão da referência) | palito | bloco
const PALITO = ESTILO === "palito", PH = ESTILO === "ph", BRANCO = ESTILO === "branco";
const MAX_PLANO = Math.min(2, R.max_plano || 1.9);
const canvas = document.getElementById("cena");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.autoClear = false;

const ease = (x) => { x = Math.min(1, Math.max(0, x)); return 1 - Math.pow(1 - x, 3); };
const suave = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
const back = (x) => { x = Math.min(1, Math.max(0, x)); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const quique = (x) => { x = Math.min(1, Math.max(0, x)); if (x < 0.6) return (x / 0.6) ** 2; const u = (x - 0.6) / 0.4; return 1 - Math.sin(Math.PI * u) * 0.12 * (1 - u); };
// pseudo-aleatório estável (mesmo vídeo sempre igual)
const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

// ------------------------------------------------------------------ material: 3 faixas de luz + borda clara
const GRAD = (() => {
  const d = new Uint8Array([105, 185, 255]);
  const t = new THREE.DataTexture(d, 3, 1, THREE.RedFormat);
  t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t;
})();
const RIM = R.borda || { cor: "#ffffff", forca: 0.8 };
const cacheMat = new Map();
function toon(mat, rim) {
  if (!mat || !mat.isMeshStandardMaterial || PH || BRANCO) return mat;
  const chave = mat.uuid + (rim ? "r" : "");
  if (cacheMat.has(chave)) return cacheMat.get(chave);
  const m = new THREE.MeshToonMaterial({ color: mat.color, gradientMap: GRAD, map: mat.map || null, transparent: mat.transparent, opacity: mat.opacity, side: mat.side });
  if (rim) {
    m.onBeforeCompile = (sh) => {
      sh.uniforms.rimCor = { value: new THREE.Color(RIM.cor) };
      sh.uniforms.rimForca = { value: RIM.forca };
      sh.fragmentShader = "uniform vec3 rimCor; uniform float rimForca;\n" + sh.fragmentShader.replace("#include <opaque_fragment>", `
        {
          vec3 vd = normalize(vViewPosition);
          float r = 1.0 - max(dot(normal, vd), 0.0);
          float lado = clamp(0.55 + normal.x * 0.6 + normal.y * 0.35, 0.0, 1.0); // contraluz do alto à direita
          r = smoothstep(0.74, 0.8, r) * smoothstep(0.35, 0.75, lado);
          outgoingLight = mix(outgoingLight, rimCor, r * rimForca);
        }
        #include <opaque_fragment>`);
    };
    m.customProgramCacheKey = () => "rim";
  }
  cacheMat.set(chave, m);
  return m;
}
function aplicarToon(obj, rim, lista) {
  obj.traverse((o) => {
    if (!o.isMesh) return;
    o.material = Array.isArray(o.material) ? o.material.map((m) => toon(m, rim)) : toon(o.material, rim);
    if (lista) (Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => lista.add(m));
  });
}

// ------------------------------------------------------------------ desfoque do fundo (2 passadas, 1/4 da resolução)
const BW = Math.round(W / 4), BH = Math.round(H / 4);
const rtA = new THREE.WebGLRenderTarget(BW, BH), rtB = new THREE.WebGLRenderTarget(BW, BH);
const quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const blurMat = new THREE.ShaderMaterial({
  uniforms: { tex: { value: null }, dir: { value: new THREE.Vector2() } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }",
  fragmentShader: `uniform sampler2D tex; uniform vec2 dir; varying vec2 vUv;
    void main(){
      vec4 c = texture2D(tex, vUv) * 0.2270;
      c += (texture2D(tex, vUv + dir * 1.3846) + texture2D(tex, vUv - dir * 1.3846)) * 0.3162;
      c += (texture2D(tex, vUv + dir * 3.2308) + texture2D(tex, vUv - dir * 3.2308)) * 0.0703;
      gl_FragColor = c;
    }`,
  depthTest: false, depthWrite: false,
});
const copiaMat = new THREE.ShaderMaterial({
  uniforms: { tex: { value: null } },
  vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }",
  fragmentShader: "uniform sampler2D tex; varying vec2 vUv; void main(){ gl_FragColor = texture2D(tex, vUv);\n#include <colorspace_fragment>\n}",
  depthTest: false, depthWrite: false,
});
const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), blurMat);
const quadScene = new THREE.Scene(); quadScene.add(quad);
function passar(mat, destino) { quad.material = mat; renderer.setRenderTarget(destino); renderer.clear(); renderer.render(quadScene, quadCam); }

// céu em degradê (azul claro em cima, quase branco no horizonte), como na referência
const CEU_PH = (() => {
  const c = document.createElement("canvas"); c.width = 4; c.height = 256;
  const x = c.getContext("2d"), gr = x.createLinearGradient(0, 0, 0, 256);
  gr.addColorStop(0, "#9fc6e3"); gr.addColorStop(0.55, "#d3e3ee"); gr.addColorStop(1, "#eef2f4");
  x.fillStyle = gr; x.fillRect(0, 0, 4, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
})();

// ------------------------------------------------------------------ montagem
const caixaDe = (obj) => {
  obj.updateMatrixWorld(true);
  const b = new THREE.Box3().setFromObject(obj);
  // sprites (balões, cartazes) não têm volume: usa o tamanho na tela
  obj.traverse((o) => { if (o.isSprite) { const c = o.getWorldPosition(new THREE.Vector3()), e = o.getWorldScale(new THREE.Vector3()); b.expandByPoint(c.clone().add(new THREE.Vector3(e.x / 2, e.y / 2, 0))); b.expandByPoint(c.clone().sub(new THREE.Vector3(e.x / 2, e.y / 2, 0))); } });
  return b;
};

function montarCena(C, ci) {
  const scene = new THREE.Scene();
  const cen = criarCenario(C.cenario || "praca", R.marca || {});
  const ceu = new THREE.Color(cen.userData.ceu);
  scene.background = PH ? CEU_PH : ceu;
  scene.fog = new THREE.Fog(PH ? "#e6eef4" : cen.userData.ceu, 45, 100);
  aplicarToon(cen, false);
  scene.add(cen);
  const fundo = new THREE.Group(); fundo.add(cen); scene.add(fundo);
  scene.add(new THREE.HemisphereLight("#ffffff", PH || BRANCO ? "#cfd6de" : "#b9c4d0", BRANCO ? 1.9 : PH ? 2.1 : 1.25));
  const sol = new THREE.DirectionalLight("#fff6e6", BRANCO ? 2.0 : PH ? 1.7 : 2.6); sol.position.set(7, 16, 12);
  sol.castShadow = true; sol.shadow.mapSize.set(2048, 2048); sol.shadow.radius = 4; sol.shadow.bias = -0.0006; sol.shadow.normalBias = 0.05;
  Object.assign(sol.shadow.camera, { left: -16, right: 16, top: 16, bottom: -16 }); scene.add(sol);

  const fgMats = new Set();
  const atores = (C.atores || []).map((a) => {
    const A = BRANCO ? criarBranco(a.tipo, a.cores || {}) : PH ? criarPH(a.tipo, a.cores || {}) : PALITO ? criarPalito(a.tipo, a.cores || {}) : criarBoneco(a.tipo, a.cores || {});
    const esc = a.escala || 1;
    A.g.scale.setScalar(esc);
    if (a.segura) {
      const o = criarObjeto(a.segura.tipo, a.segura.props || {});
      o.scale.setScalar(a.segura.escala || 0.5);
      if (a.segura.tipo === "vareta") { o.position.set(0, -0.8, 0); }
      else if (a.segura.tipo === "lupa") { o.position.set(0, -0.2, 0.25); o.rotation.set(1.45, 0, -0.5); }
      else { o.position.set(0, -0.1, 0.35); o.rotation.x = Math.PI / 2; }
      A.bracos[a.segura.mao === "E" ? 0 : 1].userData.mao.add(o);
    }
    aplicarToon(A.g, true, fgMats);
    A.g.traverse((m) => { if (m.isMesh) m.receiveShadow = false; }); // sem manchas de sombra no rosto
    scene.add(A.g);
    const p = a.pos || [0, 0];
    A.g.position.set(p[0], a.alt || 0, p[1]); A.g.rotation.y = a.rot || 0;
    return { def: a, A, esc };
  });

  const objetos = (C.objetos || []).map((o) => {
    const grupo = new THREE.Group();
    const obj = criarObjeto(o.tipo, o.props || {});
    grupo.add(obj);
    const ehFundo = o.fora || o.fundo;
    if (PH && !ehFundo && o.contorno !== false) contornar(obj, 0.03);
    aplicarToon(obj, !ehFundo, ehFundo ? null : fgMats);
    (ehFundo ? fundo : scene).add(grupo);
    const [x = 0, y = 0, z = 0] = o.pos || [];
    grupo.position.set(x, y, z);
    if (o.rot) grupo.rotation.set(...o.rot);
    grupo.scale.setScalar(o.escala || 1);
    const caixa = caixaDe(grupo);
    const poeira = new THREE.Group(); poeira.position.set(x, y + (o.alturaPoeira ?? 1.5), z); scene.add(poeira);
    for (let k = 0; k < 8; k++) {
      const p = new THREE.Mesh(new THREE.IcosahedronGeometry(0.35, 0), new THREE.MeshBasicMaterial({ color: "#ffffff", transparent: true, opacity: 0 }));
      p.userData.a = (k / 8) * Math.PI * 2; poeira.add(p);
    }
    poeira.traverse((m) => m.isMesh && fgMats.add(m.material));
    return { def: o, grupo, obj, poeira, caixa, base: new THREE.Vector3(x, y, z) };
  });

  const cam = new THREE.PerspectiveCamera(36, W / H, 0.1, 300);
  // plano geral: cabe tudo (atores, inclusive no fim da caminhada, + objetos)
  const caixa = new THREE.Box3();
  for (const a of atores) {
    caixa.union(caixaDe(a.A.g));
    const fim = (a.def.andar || []).slice(-1)[0];
    if (fim) { const g = a.A.g, px = g.position.x, pz = g.position.z; g.position.set(fim.para[0], g.position.y, fim.para[1]); caixa.union(caixaDe(g)); g.position.set(px, g.position.y, pz); }
  }
  for (const o of objetos) if (!o.def.fora) caixa.union(o.caixa);
  if (caixa.isEmpty()) caixa.set(new THREE.Vector3(-3, 0, -1), new THREE.Vector3(3, 5, 1));
  const geral = enquadrar(caixa, cam, C.camera?.margem ?? 1.06);
  return { C, ci, scene, fundo, cam, atores, objetos, fgMats, geral, ceu: PH ? CEU_PH : ceu, planos: planejar(C, ci, atores, objetos) };
}

// distância para caber a caixa no quadro vertical (com espaço para a legenda embaixo)
function enquadrar(caixa, cam, margem = 1.06, fov = 36) {
  const centro = caixa.getCenter(new THREE.Vector3()), tam = caixa.getSize(new THREE.Vector3());
  const fovV = THREE.MathUtils.degToRad(fov) / 2, fovH = Math.atan(Math.tan(fovV) * cam.aspect);
  const meiaL = (tam.x / 2) * margem + 0.35, meiaA = (tam.y / 2) * margem + 0.5;
  const d = Math.max(meiaL / Math.tan(fovH), meiaA / Math.tan(fovV)) + tam.z / 2;
  // estilo maquete: câmera mais alta, olhando de cima (quase isométrica)
  return { alvo: new THREE.Vector3(centro.x, centro.y - tam.y * 0.08, centro.z), dist: d, alt: centro.y + d * (BRANCO ? 0.42 : 0.18), fov };
}

// divide a cena em planos de no máximo MAX_PLANO segundos e escolhe o tipo de cada um
function planejar(C, ci, atores, objetos) {
  const dur = Math.max(0.1, C.t1 - C.t0);
  const n = Math.max(1, Math.ceil(dur / MAX_PLANO - 0.02));
  const planos = [];
  const quemFala = (t0, t1) => {
    let melhor = null, pts = -1;
    atores.forEach((a, i) => {
      const k = (a.def.acoes || []).filter((x) => x.t >= t0 - 0.3 && x.t < t1).length + (a.def.fala ? 2 : 0) + (i === 0 ? 0.5 : 0);
      if (k > pts) { pts = k; melhor = i; }
    });
    return melhor;
  };
  const tipos = C.camera?.planos; // o roteiro pode forçar: ["geral","rosto",...]
  let ultimo = null;
  for (let i = 0; i < n; i++) {
    const t0 = C.t0 + (dur * i) / n, t1 = C.t0 + (dur * (i + 1)) / n;
    let tipo, foco = null;
    const entra = objetos.findIndex((o) => !o.def.fora && o.def.entra && o.def.entra.t >= t0 - 0.15 && o.def.entra.t < t1 - 0.3);
    if (tipos && tipos[i]) tipo = tipos[i];
    else if (!C.fala && objetos.length) tipo = i % 2 ? "objeto" : "geral"; // fecho sem fala: a mensagem sempre à vista
    else if (i === 0) tipo = ci === 0 || ci === R.cenas.length - 1 || atores.length === 0 || (entra >= 0 && n === 1) ? "geral" : (rnd(ci) < 0.5 ? "geral" : "medio");
    else if (entra >= 0 && ultimo !== "objeto") tipo = "objeto";
    else if (atores.length) tipo = ultimo === "rosto" ? (rnd(ci * 7 + i) < 0.5 ? "geral" : "medio") : "rosto";
    else tipo = "geral";
    if (tipo === "objeto") foco = entra >= 0 ? entra : Math.max(0, objetos.findIndex((o) => !o.def.fora));
    else if (tipo !== "geral") foco = quemFala(t0, t1);
    if (tipo !== "geral" && foco == null) tipo = "geral";
    const lado = (i + ci) % 2 ? 1 : -1;
    planos.push({ t0, t1, tipo, foco, lado, sorteio: rnd(ci * 13 + i * 3) });
    ultimo = tipo;
  }
  return planos;
}

const CENAS = R.cenas.map(montarCena);

// ------------------------------------------------------------------ animação de objetos
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

// ------------------------------------------------------------------ câmera (sempre em movimento)
const _v = new THREE.Vector3();
function atualizarCamera(S, t) {
  const P = S.planos.find((p) => t < p.t1) || S.planos[S.planos.length - 1];
  const u = suave((t - P.t0) / Math.max(0.1, P.t1 - P.t0));
  let alvo, dist, alt, fov, ang;
  if (P.tipo === "rosto" || P.tipo === "medio") {
    const a = S.atores[P.foco];
    a.A.cab.getWorldPosition(_v);
    const fovV = THREE.MathUtils.degToRad(fov = P.tipo === "rosto" ? 30 : 34) / 2;
    const altQuadro = (P.tipo === "rosto" ? 7.2 : 11.5) * a.esc;          // altura de mundo que cabe no quadro
    dist = altQuadro / 2 / Math.tan(fovV);
    // o rosto fica no terço de cima (a legenda fica embaixo, nunca em cima do rosto)
    alvo = _v.clone(); alvo.y -= altQuadro * (P.tipo === "rosto" ? 0.17 : 0.24);
    alt = alvo.y + dist * 0.1;
    ang = a.A.g.rotation.y * 0.7 + P.lado * (0.28 + P.sorteio * 0.15);
  } else if (P.tipo === "objeto") {
    const O = S.objetos[P.foco];
    const cx = O.caixa.clone();
    // objeto pequeno aparece junto de quem o usa: inclui o ator mais próximo
    let perto = null, dmin = 6;
    for (const a of S.atores) { const dd = Math.hypot(a.A.g.position.x - O.base.x, a.A.g.position.z - O.base.z); if (dd < dmin) { dmin = dd; perto = a; } }
    if (perto) cx.union(caixaDe(perto.A.g));
    const e = enquadrar(cx, S.cam, 1.12, 32);
    ({ alvo, dist, alt, fov } = e);
    ang = P.lado * (0.18 + P.sorteio * 0.12);
  } else {
    ({ alvo, dist, alt, fov } = S.geral);
    ang = P.lado * (0.1 + P.sorteio * 0.12);
  }
  // movimento contínuo: aproxima, gira e sobe um pouco ao longo do plano + "soco" leve no corte
  const giro = -P.lado * 0.22 * (u - 0.5);
  const dolly = 1.07 - 0.1 * u;
  const soco = (1 - ease((t - P.t0) / 0.35)) * 0.05;
  const dd = dist * (dolly + soco);
  S.cam.fov = fov; S.cam.updateProjectionMatrix();
  S.cam.position.set(alvo.x + Math.sin(ang + giro) * dd, alt + (u - 0.5) * dist * 0.04, alvo.z + Math.cos(ang + giro) * dd);
  S.cam.lookAt(alvo.x, alvo.y, alvo.z);
  return P;
}

// ------------------------------------------------------------------ quadro
function renderAt(t) {
  let S = CENAS[0];
  for (const c of CENAS) if (t >= c.C.t0) S = c;
  for (const a of S.atores) {
    atualizarAtor(a.A, t, { acoes: a.def.acoes || [], andar: a.def.andar || [], olharPara: a.def.olhar || null, base: { x: a.def.pos?.[0] || 0, z: a.def.pos?.[1] || 0, rot: a.def.rot || 0, y: a.def.alt || 0 } });
    a.A.g.updateMatrixWorld(true);
  }
  for (const o of S.objetos) atualizarObjeto(o, t);
  const P = atualizarCamera(S, t);

  // 1) fundo (cenário + sombras dos personagens) em baixa resolução, desfocado
  for (const m of S.fgMats) { m.colorWrite = false; m.depthWrite = false; }
  S.fundo.visible = true; S.scene.background = S.ceu;
  renderer.setRenderTarget(rtA); renderer.clear(); renderer.render(S.scene, S.cam);
  const forca = BRANCO ? (P.tipo === "geral" ? 0.25 : 0.9) : P.tipo === "geral" ? 0.8 : 1.6; // maquete: a cidade aparece nítida no plano geral
  for (let i = 0; i < 2; i++) {
    blurMat.uniforms.tex.value = rtA.texture; blurMat.uniforms.dir.value.set(forca / BW, 0); passar(blurMat, rtB);
    blurMat.uniforms.tex.value = rtB.texture; blurMat.uniforms.dir.value.set(0, forca / BH); passar(blurMat, rtA);
  }
  copiaMat.uniforms.tex.value = rtA.texture; passar(copiaMat, null);
  // 2) personagens e objetos nítidos por cima
  for (const m of S.fgMats) { m.colorWrite = true; m.depthWrite = true; }
  S.fundo.visible = false; S.scene.background = null;
  renderer.clearDepth();
  renderer.render(S.scene, S.cam);
  S.fundo.visible = true; S.scene.background = S.ceu;
}

window.__planos = CENAS.flatMap((S) => S.planos.map((p) => ({ cena: S.ci, tipo: p.tipo, t0: +p.t0.toFixed(2), t1: +p.t1.toFixed(2) })));
window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
renderAt(0);
