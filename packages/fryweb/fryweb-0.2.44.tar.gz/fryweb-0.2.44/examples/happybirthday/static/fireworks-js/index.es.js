/**
 * name: fireworks-js
 * version: 2.10.7
 * author: Vitalij Ryndin (https://crashmax.ru)
 * homepage: https://fireworks.js.org
 * license MIT
 */
function f(e) {
  return Math.abs(Math.floor(e));
}
function c(e, t) {
  return Math.random() * (t - e) + e;
}
function o(e, t) {
  return Math.floor(c(e, t + 1));
}
function m(e, t, i, s) {
  const n = Math.pow;
  return Math.sqrt(n(e - i, 2) + n(t - s, 2));
}
function x(e, t, i = 1) {
  if (e > 360 || e < 0)
    throw new Error(`Expected hue 0-360 range, got \`${e}\``);
  if (t > 100 || t < 0)
    throw new Error(`Expected lightness 0-100 range, got \`${t}\``);
  if (i > 1 || i < 0)
    throw new Error(`Expected alpha 0-1 range, got \`${i}\``);
  return `hsla(${e}, 100%, ${t}%, ${i})`;
}
const g = (e) => {
  if (typeof e == "object" && e !== null) {
    if (typeof Object.getPrototypeOf == "function") {
      const t = Object.getPrototypeOf(e);
      return t === Object.prototype || t === null;
    }
    return Object.prototype.toString.call(e) === "[object Object]";
  }
  return !1;
}, y = [
  "__proto__",
  "constructor",
  "prototype"
], v = (...e) => e.reduce((t, i) => (Object.keys(i).forEach((s) => {
  y.includes(s) || (Array.isArray(t[s]) && Array.isArray(i[s]) ? t[s] = i[s] : g(t[s]) && g(i[s]) ? t[s] = v(t[s], i[s]) : t[s] = i[s]);
}), t), {});
function b(e, t) {
  let i;
  return (...s) => {
    i && clearTimeout(i), i = setTimeout(() => e(...s), t);
  };
}
class S {
  x;
  y;
  ctx;
  hue;
  friction;
  gravity;
  flickering;
  lineWidth;
  explosionLength;
  angle;
  speed;
  brightness;
  coordinates = [];
  decay;
  alpha = 1;
  constructor({
    x: t,
    y: i,
    ctx: s,
    hue: n,
    decay: h,
    gravity: a,
    friction: r,
    brightness: u,
    flickering: p,
    lineWidth: l,
    explosionLength: d
  }) {
    for (this.x = t, this.y = i, this.ctx = s, this.hue = n, this.gravity = a, this.friction = r, this.flickering = p, this.lineWidth = l, this.explosionLength = d, this.angle = c(0, Math.PI * 2), this.speed = o(1, 10), this.brightness = o(u.min, u.max), this.decay = c(h.min, h.max); this.explosionLength--; )
      this.coordinates.push([t, i]);
  }
  update(t) {
    this.coordinates.pop(), this.coordinates.unshift([this.x, this.y]), this.speed *= this.friction, this.x += Math.cos(this.angle) * this.speed, this.y += Math.sin(this.angle) * this.speed + this.gravity, this.alpha -= this.decay, this.alpha <= this.decay && t();
  }
  draw() {
    const t = this.coordinates.length - 1;
    this.ctx.beginPath(), this.ctx.lineWidth = this.lineWidth, this.ctx.fillStyle = x(this.hue, this.brightness, this.alpha), this.ctx.moveTo(
      this.coordinates[t][0],
      this.coordinates[t][1]
    ), this.ctx.lineTo(this.x, this.y), this.ctx.strokeStyle = x(
      this.hue,
      this.flickering ? c(0, this.brightness) : this.brightness,
      this.alpha
    ), this.ctx.stroke();
  }
}
class E {
  constructor(t, i) {
    this.options = t, this.canvas = i, this.pointerDown = this.pointerDown.bind(this), this.pointerUp = this.pointerUp.bind(this), this.pointerMove = this.pointerMove.bind(this);
  }
  active = !1;
  x;
  y;
  get mouseOptions() {
    return this.options.mouse;
  }
  mount() {
    this.canvas.addEventListener("pointerdown", this.pointerDown), this.canvas.addEventListener("pointerup", this.pointerUp), this.canvas.addEventListener("pointermove", this.pointerMove);
  }
  unmount() {
    this.canvas.removeEventListener("pointerdown", this.pointerDown), this.canvas.removeEventListener("pointerup", this.pointerUp), this.canvas.removeEventListener("pointermove", this.pointerMove);
  }
  usePointer(t, i) {
    const { click: s, move: n } = this.mouseOptions;
    (s || n) && (this.x = t.pageX - this.canvas.offsetLeft, this.y = t.pageY - this.canvas.offsetTop, this.active = i);
  }
  pointerDown(t) {
    this.usePointer(t, this.mouseOptions.click);
  }
  pointerUp(t) {
    this.usePointer(t, !1);
  }
  pointerMove(t) {
    this.usePointer(t, this.active);
  }
}
class O {
  hue;
  rocketsPoint;
  opacity;
  acceleration;
  friction;
  gravity;
  particles;
  explosion;
  mouse;
  boundaries;
  sound;
  delay;
  brightness;
  decay;
  flickering;
  intensity;
  traceLength;
  traceSpeed;
  lineWidth;
  lineStyle;
  autoresize;
  constructor() {
    this.autoresize = !0, this.lineStyle = "round", this.flickering = 50, this.traceLength = 3, this.traceSpeed = 10, this.intensity = 30, this.explosion = 5, this.gravity = 1.5, this.opacity = 0.5, this.particles = 50, this.friction = 0.95, this.acceleration = 1.05, this.hue = {
      min: 0,
      max: 360
    }, this.rocketsPoint = {
      min: 50,
      max: 50
    }, this.lineWidth = {
      explosion: {
        min: 1,
        max: 3
      },
      trace: {
        min: 1,
        max: 2
      }
    }, this.mouse = {
      click: !1,
      move: !1,
      max: 1
    }, this.delay = {
      min: 30,
      max: 60
    }, this.brightness = {
      min: 50,
      max: 80
    }, this.decay = {
      min: 0.015,
      max: 0.03
    }, this.sound = {
      enabled: !1,
      files: [
        "explosion0.mp3",
        "explosion1.mp3",
        "explosion2.mp3"
      ],
      volume: {
        min: 4,
        max: 8
      }
    }, this.boundaries = {
      debug: !1,
      height: 0,
      width: 0,
      x: 50,
      y: 50
    };
  }
  update(t) {
    Object.assign(this, v(this, t));
  }
}
class z {
  constructor(t, i) {
    this.options = t, this.render = i;
  }
  tick = 0;
  rafId = 0;
  fps = 60;
  tolerance = 0.1;
  now;
  mount() {
    this.now = performance.now();
    const t = 1e3 / this.fps, i = (s) => {
      this.rafId = requestAnimationFrame(i);
      const n = s - this.now;
      n >= t - this.tolerance && (this.render(), this.now = s - n % t, this.tick += n * (this.options.intensity * Math.PI) / 1e3);
    };
    this.rafId = requestAnimationFrame(i);
  }
  unmount() {
    cancelAnimationFrame(this.rafId);
  }
}
class L {
  constructor(t, i, s) {
    this.options = t, this.updateSize = i, this.container = s;
  }
  resizer;
  mount() {
    if (!this.resizer) {
      const t = b(() => this.updateSize(), 100);
      this.resizer = new ResizeObserver(t);
    }
    this.options.autoresize && this.resizer.observe(this.container);
  }
  unmount() {
    this.resizer && this.resizer.unobserve(this.container);
  }
}
class M {
  constructor(t) {
    this.options = t, this.init();
  }
  buffers = [];
  audioContext;
  onInit = !1;
  get isEnabled() {
    return this.options.sound.enabled;
  }
  get soundOptions() {
    return this.options.sound;
  }
  init() {
    !this.onInit && this.isEnabled && (this.onInit = !0, this.audioContext = new (window.AudioContext || window.webkitAudioContext)(), this.loadSounds());
  }
  async loadSounds() {
    for (const t of this.soundOptions.files) {
      const i = await (await fetch(t)).arrayBuffer();
      this.audioContext.decodeAudioData(i).then((s) => {
        this.buffers.push(s);
      }).catch((s) => {
        throw s;
      });
    }
  }
  play() {
    if (this.isEnabled && this.buffers.length) {
      const t = this.audioContext.createBufferSource(), i = this.buffers[o(0, this.buffers.length - 1)], s = this.audioContext.createGain();
      t.buffer = i, s.gain.value = c(
        this.soundOptions.volume.min / 100,
        this.soundOptions.volume.max / 100
      ), s.connect(this.audioContext.destination), t.connect(s), t.start(0);
    } else
      this.init();
  }
}
class C {
  x;
  y;
  sx;
  sy;
  dx;
  dy;
  ctx;
  hue;
  speed;
  acceleration;
  traceLength;
  totalDistance;
  angle;
  brightness;
  coordinates = [];
  currentDistance = 0;
  constructor({
    x: t,
    y: i,
    dx: s,
    dy: n,
    ctx: h,
    hue: a,
    speed: r,
    traceLength: u,
    acceleration: p
  }) {
    for (this.x = t, this.y = i, this.sx = t, this.sy = i, this.dx = s, this.dy = n, this.ctx = h, this.hue = a, this.speed = r, this.traceLength = u, this.acceleration = p, this.totalDistance = m(t, i, s, n), this.angle = Math.atan2(n - i, s - t), this.brightness = o(50, 70); this.traceLength--; )
      this.coordinates.push([t, i]);
  }
  update(t) {
    this.coordinates.pop(), this.coordinates.unshift([this.x, this.y]), this.speed *= this.acceleration;
    const i = Math.cos(this.angle) * this.speed, s = Math.sin(this.angle) * this.speed;
    this.currentDistance = m(
      this.sx,
      this.sy,
      this.x + i,
      this.y + s
    ), this.currentDistance >= this.totalDistance ? t(this.dx, this.dy, this.hue) : (this.x += i, this.y += s);
  }
  draw() {
    const t = this.coordinates.length - 1;
    this.ctx.beginPath(), this.ctx.moveTo(
      this.coordinates[t][0],
      this.coordinates[t][1]
    ), this.ctx.lineTo(this.x, this.y), this.ctx.strokeStyle = x(this.hue, this.brightness), this.ctx.stroke();
  }
}
class T {
  target;
  container;
  canvas;
  ctx;
  width;
  height;
  traces = [];
  explosions = [];
  waitStopRaf;
  running = !1;
  opts;
  sound;
  resize;
  mouse;
  raf;
  constructor(t, i = {}) {
    this.target = t, this.container = t, this.opts = new O(), this.createCanvas(this.target), this.updateOptions(i), this.sound = new M(this.opts), this.resize = new L(
      this.opts,
      this.updateSize.bind(this),
      this.container
    ), this.mouse = new E(this.opts, this.canvas), this.raf = new z(this.opts, this.render.bind(this));
  }
  get isRunning() {
    return this.running;
  }
  get version() {
    return "2.10.7";
  }
  get currentOptions() {
    return this.opts;
  }
  start() {
    this.running || (this.canvas.isConnected || this.createCanvas(this.target), this.running = !0, this.resize.mount(), this.mouse.mount(), this.raf.mount());
  }
  stop(t = !1) {
    !this.running || (this.running = !1, this.resize.unmount(), this.mouse.unmount(), this.raf.unmount(), this.clear(), t && this.canvas.remove());
  }
  async waitStop(t) {
    if (!!this.running)
      return new Promise((i) => {
        this.waitStopRaf = () => {
          !this.waitStopRaf || (requestAnimationFrame(this.waitStopRaf), !this.traces.length && !this.explosions.length && (this.waitStopRaf = null, this.stop(t), i()));
        }, this.waitStopRaf();
      });
  }
  pause() {
    this.running = !this.running, this.running ? this.raf.mount() : this.raf.unmount();
  }
  clear() {
    !this.ctx || (this.traces = [], this.explosions = [], this.ctx.clearRect(0, 0, this.width, this.height));
  }
  launch(t = 1) {
    for (let i = 0; i < t; i++)
      this.createTrace();
    this.waitStopRaf || (this.start(), this.waitStop());
  }
  updateOptions(t) {
    this.opts.update(t);
  }
  updateSize({
    width: t = this.container.clientWidth,
    height: i = this.container.clientHeight
  } = {}) {
    this.width = t, this.height = i, this.canvas.width = t, this.canvas.height = i, this.updateBoundaries({
      ...this.opts.boundaries,
      width: t,
      height: i
    });
  }
  updateBoundaries(t) {
    this.updateOptions({ boundaries: t });
  }
  createCanvas(t) {
    t instanceof HTMLCanvasElement ? (t.isConnected || document.body.append(t), this.canvas = t) : (this.canvas = document.createElement("canvas"), this.container.append(this.canvas)), this.ctx = this.canvas.getContext("2d"), this.updateSize();
  }
  render() {
    if (!this.ctx || !this.running)
      return;
    const { opacity: t, lineStyle: i, lineWidth: s } = this.opts;
    this.ctx.globalCompositeOperation = "destination-out", this.ctx.fillStyle = `rgba(0, 0, 0, ${t})`, this.ctx.fillRect(0, 0, this.width, this.height), this.ctx.globalCompositeOperation = "lighter", this.ctx.lineCap = i, this.ctx.lineJoin = "round", this.ctx.lineWidth = c(s.trace.min, s.trace.max), this.initTrace(), this.drawTrace(), this.drawExplosion();
  }
  createTrace() {
    const {
      hue: t,
      rocketsPoint: i,
      boundaries: s,
      traceLength: n,
      traceSpeed: h,
      acceleration: a,
      mouse: r
    } = this.opts;
    const x = this.width * o(i.min, i.max) / 100;
    this.traces.push(
      new C({
        x: x,
        y: this.height,
        dx: x,
        dy: this.mouse.y && r.move || this.mouse.active ? this.mouse.y : o(s.y, s.height * 0.5),
        ctx: this.ctx,
        hue: o(t.min, t.max),
        speed: h,
        acceleration: a,
        traceLength: f(n)
      })
    );
  }
  initTrace() {
    if (this.waitStopRaf)
      return;
    const { delay: t, mouse: i } = this.opts;
    (this.raf.tick > o(t.min, t.max) || this.mouse.active && i.max > this.traces.length) && (this.createTrace(), this.raf.tick = 0);
  }
  drawTrace() {
    let t = this.traces.length;
    for (; t--; )
      this.traces[t].draw(), this.traces[t].update((i, s, n) => {
        this.initExplosion(i, s, n), this.sound.play(), this.traces.splice(t, 1);
      });
  }
  initExplosion(t, i, s) {
    const {
      particles: n,
      flickering: h,
      lineWidth: a,
      explosion: r,
      brightness: u,
      friction: p,
      gravity: l,
      decay: d
    } = this.opts;
    let w = f(n);
    for (; w--; )
      this.explosions.push(
        new S({
          x: t,
          y: i,
          ctx: this.ctx,
          hue: s,
          friction: p,
          gravity: l,
          flickering: o(0, 100) <= h,
          lineWidth: c(
            a.explosion.min,
            a.explosion.max
          ),
          explosionLength: f(r),
          brightness: u,
          decay: d
        })
      );
  }
  drawExplosion() {
    let t = this.explosions.length;
    for (; t--; )
      this.explosions[t].draw(), this.explosions[t].update(() => {
        this.explosions.splice(t, 1);
      });
  }
}
export {
  T as Fireworks,
  T as default
};
