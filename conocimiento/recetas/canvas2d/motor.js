// ===================== MOTOR BASE =====================
// Lienzo lógico 640×360, y hacia abajo. Todo es función pura del tiempo t (segundos).
const W = 640, H = 360, TAU = Math.PI * 2;
const S = { // paleta de escena (papel). Sin negro ni blanco puros.
  paper:'#EFEAE0', ink:'#26222E', cream:'#FFF8EA', red:'#D6453D', blue:'#4C86C6', ochre:'#E7A93B',
  teal:'#3E9C96', rose:'#E2798F', sap:'#79A85E', violet:'#7A5FA8', night:'#1E2448', sky:'#9CC9E6', green:'#1F4A3A'
};
// ---- números y curvas (de core.js de PDoomVideo / ClaudeAnimationBase) ----
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, k) => a + (b - a) * k;
const seg = (t, a, b) => clamp((t - a) / (b - a));           // progreso 0..1 de t en [a,b]
const frac = x => x - Math.floor(x);
const ease = x => { x = clamp(x); return x * x * (3 - 2 * x); };  // smoothstep: entra y sale suave
const easeIn = x => Math.pow(clamp(x), 3);
const easeOut = x => 1 - Math.pow(1 - clamp(x), 3);
const backOut = x => { x = clamp(x); const s = 1.9; return 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2); }; // rebasa y regresa
const elasticOut = x => { x = clamp(x); return x === 0 || x === 1 ? x : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (TAU / 3)) + 1; };
const easeInOutQuint = x => { x = clamp(x); return x < .5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2; };
const hash = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }; // aleatorio estable
function kf(t, keys, e = ease) {                                // keyframes: [[t0,v0],[t1,v1],...]
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) {
    const [a, va] = keys[i - 1], [b, vb] = keys[i], k = e((t - a) / (b - a));
    return Array.isArray(va) ? va.map((v, j) => lerp(v, vb[j], k)) : lerp(va, vb, k);
  }
  return keys[keys.length - 1][1];
}
// ---- ritmo ----
const BPM = 88, BEAT = 60 / BPM;                                 // 88 BPM: el tempo del video musical
const pulse = (t, k = 6) => Math.exp(-frac(t / BEAT) * k);       // 1 en cada beat y decae
const wob = (t, f = 1, ph = 0) => Math.sin((t * f + ph) * TAU);
// ---- principios de animación como funciones puras ----
const spring = (t, t0, k = 6, w = 18) => t < t0 ? 0 : Math.exp(-k * (t - t0)) * Math.sin(w * (t - t0)); // rebote amortiguado
const ring = (t, evs, k = 6, w = 18) => evs.reduce((s, e) => s + spring(t, e, k, w), 0);
const onTwos = t => Math.floor(t * 12 + 1e-6) / 12;              // 12 dibujos por segundo
const arcPt = (p0, p1, h, k) => [lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k) - h * 4 * k * (1 - k)];
const shake = (t, a) => { const f = Math.floor(t * 24); return [(hash(f * 1.7) - .5) * 2 * a, (hash(f * 2.3 + 9) - .5) * 2 * a]; };
function jump(t, t0, t1, h = 3) {       // agacharse → estirarse → arco → aplastarse al caer. Devuelve {dy (en u), sq}
  if (t < t0 - .12) return { dy: 0, sq: 0 };
  if (t < t0) return { dy: 0, sq: .18 * ease(seg(t, t0 - .12, t0)) };
  if (t < t1) { const k = (t - t0) / (t1 - t0); return { dy: -h * 4 * k * (1 - k), sq: -.16 * Math.abs(1 - 2 * k) }; }
  const a = t - t1; return { dy: 0, sq: .22 * Math.exp(-8 * a) * Math.cos(20 * a) };
}
function take(t, t0, amt = 1) {         // sorpresa: aplasta poquito y se estira de golpe
  if (t < t0 - .1) return { sq: 0, dy: 0 };
  if (t < t0) return { sq: .12 * amt * ease(seg(t, t0 - .1, t0)), dy: 0 };
  const a = t - t0; return { sq: -.26 * amt * Math.exp(-6 * a) * Math.cos(16 * a), dy: -1.2 * amt * Math.exp(-7 * a) * Math.max(0, Math.cos(9 * a)) };
}
// ---- azar con semilla y "boil" (línea que hierve a 12 fps) ----
function rngFrom(str) { let h = 2166136261; for (const ch of String(str)) h = Math.imul(h ^ ch.charCodeAt(0), 16777619);
  let a = h >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let q = Math.imul(a ^ a >>> 15, 1 | a); q = q + Math.imul(q ^ q >>> 7, 61 | q) ^ q; return ((q ^ q >>> 14) >>> 0) / 4294967296; }; }
const boil = (key, t, fps = 12) => rngFrom(key + '|' + Math.floor(t * fps)); // misma clave + mismo dibujo = mismo temblor
function mix(a, b, k) { const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16), ch = i => Math.round(lerp((pa >> i) & 255, (pb >> i) & 255, clamp(k)));
  return '#' + ((1 << 24) + (ch(16) << 16) + (ch(8) << 8) + ch(0)).toString(16).slice(1); }
// ---- geometría ----
const ell = (cx, cy, rx, ry, n = 24, rot = 0) => Array.from({ length: n }, (_, i) => { const a = i / n * TAU, x = Math.cos(a) * rx, y = Math.sin(a) * ry;
  return [cx + x * Math.cos(rot) - y * Math.sin(rot), cy + x * Math.sin(rot) + y * Math.cos(rot)]; });
const rect = (x, y, w, h) => [[x, y], [x + w, y], [x + w, y + h], [x, y + h]];
function rrect(x, y, w, h, r, n = 4) { const p = [], c = (cx, cy, a0) => { for (let i = 0; i <= n; i++) { const a = a0 + i / n * Math.PI / 2; p.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } };
  c(x + w - r, y + r, -Math.PI / 2); c(x + w - r, y + h - r, 0); c(x + r, y + h - r, Math.PI / 2); c(x + r, y + r, Math.PI); return p; }
function star(cx, cy, r, inner = .45, n = 5, rot = -Math.PI / 2) { return Array.from({ length: n * 2 }, (_, i) => { const a = rot + i * Math.PI / n, rr = i % 2 ? r * inner : r; return [cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]; }); }
function heart(cx, cy, r, n = 40) { return Array.from({ length: n }, (_, i) => { const a = i / n * TAU, x = 16 * Math.sin(a) ** 3, y = 13 * Math.cos(a) - 5 * Math.cos(2 * a) - 2 * Math.cos(3 * a) - Math.cos(4 * a); return [cx + x * r / 16, cy - y * r / 16]; }); }
// ---- trazo a mano ----
function smoothPath(c, P, close = true) {
  const n = P.length; c.beginPath(); if (n < 2) return;
  if (close) { const m = (a, b) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]; const s = m(P[n - 1], P[0]); c.moveTo(s[0], s[1]);
    for (let i = 0; i < n; i++) { const p = P[i], q = m(p, P[(i + 1) % n]); c.quadraticCurveTo(p[0], p[1], q[0], q[1]); } c.closePath(); }
  else { c.moveTo(P[0][0], P[0][1]); for (let i = 1; i < n - 1; i++) { const p = P[i]; c.quadraticCurveTo(p[0], p[1], (p[0] + P[i + 1][0]) / 2, (p[1] + P[i + 1][1]) / 2); } c.lineTo(P[n - 1][0], P[n - 1][1]); }
}
// ink(c, puntos, {fill, stroke, w, jit, r, close, smooth}): relleno plano + contorno de tinta con segunda pasada fina
function ink(c, pts, o = {}) {
  const r = o.r || (() => .5), j = o.jit ?? 1.2, close = o.close !== false;
  const P = pts.map(p => [p[0] + (r() * 2 - 1) * j, p[1] + (r() * 2 - 1) * j]);
  const path = () => { if (o.smooth === false) { c.beginPath(); P.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); if (close) c.closePath(); } else smoothPath(c, P, close); };
  const ga = c.globalAlpha; // respeta la opacidad que ya traiga el contexto (fundidos, fantasmas)
  if (o.fill && close) { path(); c.globalAlpha = ga * (o.fillA ?? 1); c.fillStyle = o.fill; c.fill(); c.globalAlpha = ga; }
  if (o.stroke !== null) { c.lineJoin = 'round'; c.lineCap = 'round'; c.strokeStyle = o.stroke || S.ink; const w = o.w ?? 2.2;
    path(); c.lineWidth = w; c.stroke(); c.save(); c.translate((r() - .5) * 1.2, (r() - .5) * 1.2); c.globalAlpha = ga * .4; c.lineWidth = w * .5; path(); c.stroke(); c.restore(); }
}
// mancha tipo acuarela: base + 3 manchas translúcidas recortadas (estables, no hierven)
function wash(c, pts, col, seed = 1, o = {}) {
  c.save(); smoothPath(c, pts, true); c.fillStyle = col; c.globalAlpha = o.a ?? 1; c.fill(); c.clip(); c.globalAlpha = 1;
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; pts.forEach(([x, y]) => { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); });
  for (let i = 0; i < 3; i++) { const cx = lerp(x0, x1, hash(seed * 7 + i)), cy = lerp(y0, y1, hash(seed * 13 + i)), rr = (x1 - x0 + y1 - y0) * (.15 + .2 * hash(seed + i * 3));
    const g = c.createRadialGradient(cx, cy, 0, cx, cy, rr); g.addColorStop(0, mix(col, S.ink, .18) + '55'); g.addColorStop(1, mix(col, S.ink, .18) + '00'); c.fillStyle = g; c.fillRect(x0, y0, x1 - x0, y1 - y0); }
  c.restore();
}
// texto con "pop" (de letter()/drawLetters() del repo): escala backOut(pop), sombra de tinta desplazada
function word(c, txt, x, y, size, col, o = {}) {
  const k = o.pop != null ? backOut(o.pop) : 1; if (k <= .01 || (o.alpha ?? 1) <= 0) return;
  c.save(); c.translate(x, y); c.rotate(o.rot || 0); c.scale(k, k); c.globalAlpha = clamp(o.alpha ?? 1);
  c.font = o.font || `800 ${size}px Unbounded, "Arial Black", sans-serif`; c.textAlign = o.align || 'center'; c.textBaseline = 'middle';
  if (o.stroke) { c.lineJoin = 'round'; c.lineWidth = size * .14; c.strokeStyle = o.stroke; c.strokeText(txt, 0, 0); }
  if (o.shadow !== false) { c.fillStyle = S.ink; c.fillText(txt, size * .045, size * .055); }
  c.fillStyle = col; c.fillText(txt, 0, 0); c.restore();
}
// fondo de papel estable (se genera una vez)
let PAPER = null;
function paper(c, tint = S.paper) {
  if (!PAPER || PAPER.tint !== tint) { const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const p = cv.getContext('2d'), r = rngFrom('papel');
    p.fillStyle = tint; p.fillRect(0, 0, W, H);
    for (let i = 0; i < 2600; i++) { p.fillStyle = `rgba(70,55,40,${r() * .06})`; p.fillRect(r() * W, r() * H, 1 + r() * 1.4, 1 + r() * 1.4); }
    p.strokeStyle = 'rgba(80,60,45,.06)'; p.lineWidth = .8; for (let i = 0; i < 150; i++) { const x = r() * W, y = r() * H, l = 4 + r() * 14, a = r() * TAU; p.beginPath(); p.moveTo(x, y); p.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); p.stroke(); }
    const g = p.createRadialGradient(W / 2, H / 2, H * .35, W / 2, H / 2, H * .95); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(60,40,25,.13)'); p.fillStyle = g; p.fillRect(0, 0, W, H);
    PAPER = cv; PAPER.tint = tint; }
  c.drawImage(PAPER, 0, 0);
}
// suelo suave
function ground(c, y = 300, col = S.sap, seed = 2) { wash(c, [[-20, y + 6], [W * .3, y - 6], [W * .7, y + 4], [W + 20, y - 4], [W + 20, H + 20], [-20, H + 20]], col, seed); }
// ---- emotes pintados (nunca letras) ----
function emote(c, kind, x, y, s, k = 1, r) {
  const q = backOut(k); if (q <= .01) return; c.save(); c.translate(x, y); c.scale(q, q); r = r || (() => .5);
  if (kind === '!') { ink(c, [[-s * .22, -s], [s * .22, -s], [s * .1, s * .25], [-s * .1, s * .25]], { fill: S.red, w: 2, r, jit: .6 }); ink(c, ell(0, s * .55, s * .17, s * .17, 10), { fill: S.red, w: 2, r, jit: .4 }); }
  else if (kind === 'heart') ink(c, heart(0, 0, s * .8), { fill: S.rose, w: 2, r, jit: .6 });
  else if (kind === 'drop') ink(c, [[0, -s * .9], [s * .45, 0], [s * .35, s * .45], [0, s * .6], [-s * .35, s * .45], [-s * .45, 0]], { fill: S.sky, w: 2, r, jit: .5 });
  else if (kind === 'spark') ink(c, star(0, 0, s * .9, .3, 4), { fill: S.ochre, w: 2, r, jit: .5, smooth: false });
  else if (kind === 'cloud') { const P = Array.from({ length: 36 }, (_, i) => { const a = i / 36 * TAU, rr = s * (.62 + .14 * Math.abs(Math.cos(a * 2.5))); return [Math.cos(a) * rr * 1.25, Math.min(s * .3, Math.sin(a) * rr * .8)]; });
    ink(c, P, { fill: '#AEB6C6', w: 2, r, jit: .5 }); ink(c, [[0, s * .55], [s * .16, s * .82], [0, s * .95], [-s * .16, s * .82]], { fill: S.sky, w: 1.6, r, jit: .3 }); }
  c.restore();
}
// ---- personaje original "Bolo": gota con antena. (x,y) = suelo entre los pies; u = unidad (~8u de ancho) ----
function bolo(c, x, y, u, o = {}) {
  const r = boil('bolo:' + (o.key ?? 'a'), o.t ?? 0), sq = o.sq || 0, sx = 1 + sq, sy = 1 - sq;
  const col = o.col || S.teal, dk = mix(col, S.ink, .3), w = Math.max(1.6, u * .17), up = Math.max(0, -(o.dy || 0));
  c.save(); c.fillStyle = 'rgba(38,34,46,.16)'; c.beginPath(); c.ellipse(x + (o.dx || 0) * u, y + 2, 4.3 * u * sx / (1 + up * .12), .9 * u / (1 + up * .12), 0, 0, TAU); c.fill(); c.restore();
  c.save(); c.translate(x + (o.dx || 0) * u, y + (o.dy || 0) * u); c.rotate(o.rot || 0); c.scale((o.flip ? -1 : 1) * sx, sy);
  [-1, 1].forEach((s, i) => { const lift = o.walk != null ? Math.max(0, Math.sin(o.walk * Math.PI + i * Math.PI)) * .9 * u : 0;
    ink(c, ell(s * 1.7 * u, -.45 * u - lift, 1.1 * u, .55 * u, 12), { fill: dk, w, r, jit: u * .04 }); });
  const hands = {};
  const arm = (s, a, key) => { if (a == null) return; const bx = s * 3.6 * u, by = -3.3 * u, L = 2.3 * u, ex = bx + s * Math.cos(a) * L, ey = by - Math.sin(a) * L;
    c.lineCap = 'round'; c.strokeStyle = S.ink; c.lineWidth = u * .8; c.beginPath(); c.moveTo(bx, by); c.quadraticCurveTo(bx + s * L * .55, by - Math.sin(a) * L * .35, ex, ey); c.stroke();
    c.strokeStyle = col; c.lineWidth = u * .42; c.stroke(); hands[key] = [x + (o.dx || 0) * u + ex * (o.flip ? -1 : 1) * sx, y + (o.dy || 0) * u + ey * sy]; };
  arm(-1, o.aL, 'L'); arm(1, o.aR, 'R');
  const pts = []; for (let i = 0; i < 30; i++) { const a = i / 30 * TAU; let px = Math.cos(a) * 4 * u, py = -3.7 * u + Math.sin(a) * 3.5 * u; if (py > -.5 * u) py = -.5 * u + (py + .5 * u) * .2; pts.push([px, py]); }
  ink(c, pts, { fill: col, w, r, jit: u * .05 });
  c.save(); smoothPath(c, pts, true); c.clip(); c.fillStyle = dk; c.globalAlpha = .22; c.beginPath(); c.ellipse(2.7 * u, -2.2 * u, 3 * u, 3.4 * u, 0, 0, TAU); c.fill();
  c.globalAlpha = .55; c.fillStyle = S.cream; c.beginPath(); c.ellipse(-2.1 * u, -5.7 * u, .9 * u, .42 * u, -.5, 0, TAU); c.fill(); c.restore();
  const ax = (o.ant || 0) * u; c.strokeStyle = S.ink; c.lineWidth = w; c.lineCap = 'round'; c.beginPath(); c.moveTo(0, -7.1 * u); c.quadraticCurveTo(ax * .3, -8.4 * u, ax, -9.3 * u); c.stroke();
  ink(c, ell(ax, -9.55 * u, .75 * u, .75 * u, 10), { fill: o.tip || S.ochre, w, r, jit: u * .03 });
  const lx = (o.lookX || 0) * .6 * u, ly = (o.lookY || 0) * .5 * u, sqz = clamp(o.squint || 0), E = o.eyes || 'open';
  [-1, 1].forEach(s => { const ex = s * 1.5 * u + lx * .5, ey = -4.6 * u + ly * .3;
    if (E === 'closed' || sqz > .88) { ink(c, [[ex - .8 * u, ey], [ex, ey + .35 * u], [ex + .8 * u, ey]], { close: false, w, r, jit: .3 }); return; }
    if (E === 'happy') { ink(c, [[ex - .8 * u, ey + .3 * u], [ex, ey - .45 * u], [ex + .8 * u, ey + .3 * u]], { close: false, w: w * 1.1, r, jit: .3 }); return; }
    const big = E === 'wide' ? 1.25 : 1, rx = .82 * u * big, ry = 1.05 * u * big * (1 - sqz * .85);
    ink(c, ell(ex, ey, rx, ry, 14), { fill: S.cream, w: w * .9, r, jit: u * .03 });
    c.save(); c.beginPath(); c.ellipse(ex, ey, rx, ry, 0, 0, TAU); c.clip(); c.fillStyle = S.ink; c.beginPath();
    c.arc(ex + lx * .45, ey + ly * .5 + (E === 'sad' ? .3 * u : 0), (E === 'wide' ? .36 : .46) * u, 0, TAU); c.fill(); c.restore();
    if (E === 'sad') ink(c, [[ex - s * .9 * u, ey - 1.5 * u], [ex + s * .7 * u, ey - 1.15 * u]], { close: false, w, r, jit: .3 }); });
  const M = o.mouth; if (M) { const mx = lx * .3, my = -2.55 * u;
    if (M === 'o' || M === 'O') ink(c, ell(mx, my, (M === 'O' ? .6 : .33) * u, (M === 'O' ? .75 : .4) * u, 10), { fill: S.ink, w: w * .7, r, jit: .3 });
    else if (M === 'smile') ink(c, [[mx - .9 * u, my - .2 * u], [mx, my + .45 * u], [mx + .9 * u, my - .2 * u]], { close: false, w, r, jit: .3 });
    else if (M === 'frown') ink(c, [[mx - .8 * u, my + .3 * u], [mx, my - .25 * u], [mx + .8 * u, my + .3 * u]], { close: false, w, r, jit: .3 }); }
  if (o.blush) { c.globalAlpha = .45 * o.blush; c.fillStyle = S.rose; [-1, 1].forEach(s => { c.beginPath(); c.ellipse(s * 2.6 * u, -3.2 * u, .7 * u, .35 * u, 0, 0, TAU); c.fill(); }); c.globalAlpha = 1; }
  c.restore(); return hands;
}
// barrido de pincel (traducción de brushWipe de timeline.js). p 0→.5 cubre, .5→1 se arrastra fuera. Corta la escena en p=.5
function brushWipe(c, p, t, cols = [S.red, mix(S.red, S.ochre, .45)]) {
  if (p <= 0 || p >= 1) return; const n = 5, bh = (H + 220) / n + 24;
  c.save(); c.translate(W / 2, H / 2); c.rotate(-.1); c.translate(-W / 2, -H / 2);
  for (let i = 0; i < n; i++) { const r = boil('wipe' + i, t), y0 = -110 + i * (H + 220) / n, d = [0, .14, .06, .18, .1][i];
    const q = p < .5 ? easeOut(clamp((p * 2 - d) / (1 - d))) : ease(clamp(((p - .5) * 2 - d) / (1 - d)));
    const x0 = p < .5 ? -120 : lerp(-120, W + 160, q), x1 = p < .5 ? lerp(-120, W + 160, q) : W + 160; if (x1 - x0 < 12) continue;
    const pts = [], rag = k => 16 + 22 * hash(i * 31 + k) + (r() - .5) * 8;
    for (let k = 0; k <= 8; k++) pts.push([lerp(x0, x1, k / 8), y0 + Math.sin(k * .9 + i) * 6 + (r() - .5) * 4]);
    for (let k = 1; k < 9; k++) pts.push([x1 + rag(k) - 16, y0 + bh * k / 9]);
    for (let k = 8; k >= 0; k--) pts.push([lerp(x0, x1, k / 8), y0 + bh + Math.sin(k * .8 + i * 2) * 6 + (r() - .5) * 4]);
    if (p >= .5) for (let k = 8; k > 0; k--) pts.push([x0 - rag(k + 20) + 16, y0 + bh * k / 9]);
    const col = i % 2 ? cols[0] : cols[1]; c.save(); smoothPath(c, pts, true); c.fillStyle = col; c.fill(); c.clip();
    c.strokeStyle = mix(col, S.cream, .35); c.globalAlpha = .35; c.lineWidth = 1; for (let k = 0; k < 14; k++) { const yy = y0 + bh * hash(i * 9 + k); c.beginPath(); c.moveTo(x0, yy); c.lineTo(x1 + 40, yy + (r() - .5) * 6); c.stroke(); }
    c.restore(); }
  c.restore();
}
// iris: pinta todo FUERA de la figura (regla evenodd)
function irisShape(c, pts, col = S.ink) { c.save(); c.beginPath(); c.rect(-50, -50, W + 100, H + 100); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.closePath(); c.fillStyle = col; c.fill('evenodd'); c.restore(); }
// trazo que se dibuja: progreso k de una polilínea
function drawOn(P, k) { if (k <= 0) return []; let L = 0; const d = [0]; for (let i = 1; i < P.length; i++) { L += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); d.push(L); }
  const target = L * clamp(k), out = [P[0]]; for (let i = 1; i < P.length; i++) { if (d[i] <= target) out.push(P[i]); else { const f = (target - d[i - 1]) / (d[i] - d[i - 1]); out.push([lerp(P[i - 1][0], P[i][0], f), lerp(P[i - 1][1], P[i][1], f)]); break; } } return out; }
// ===================== FIN DEL MOTOR =====================
