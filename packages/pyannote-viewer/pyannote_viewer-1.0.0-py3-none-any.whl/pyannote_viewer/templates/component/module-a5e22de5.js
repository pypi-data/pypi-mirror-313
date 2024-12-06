import { c as Zn, a as It, g as Kn } from "./module-2c3384e6.js";
const Je = /* @__PURE__ */ new Set(), St = /* @__PURE__ */ new Set(), ye = /* @__PURE__ */ new WeakMap(), Qn = Zn({
  deregister: ({ call: e }) => async (t) => {
    const n = ye.get(t);
    if (n === void 0)
      throw new Error("There is no encoder registered with the given port.");
    const r = await e("deregister", { encoderId: n });
    return Je.delete(n), ye.delete(t), r;
  },
  encode: ({ call: e }) => async (t, n) => {
    const r = await e("encode", { encoderInstanceId: t, timeslice: n });
    return St.delete(t), r;
  },
  instantiate: ({ call: e }) => async (t, n) => {
    const r = It(St), o = await e("instantiate", { encoderInstanceId: r, mimeType: t, sampleRate: n });
    return { encoderInstanceId: r, port: o };
  },
  register: ({ call: e }) => async (t) => {
    if (ye.has(t))
      throw new Error("");
    const n = It(Je);
    ye.set(t, n);
    try {
      return await e("register", { encoderId: n, port: t }, [t]);
    } catch (r) {
      throw Je.delete(n), ye.delete(t), r;
    }
  }
}), Jn = (e) => {
  const t = new Worker(e);
  return Qn(t);
}, er = `(()=>{var e={455:function(e,t){!function(e){"use strict";var t=function(e){return function(t){var r=e(t);return t.add(r),r}},r=function(e){return function(t,r){return e.set(t,r),r}},n=void 0===Number.MAX_SAFE_INTEGER?9007199254740991:Number.MAX_SAFE_INTEGER,o=536870912,s=2*o,a=function(e,t){return function(r){var a=t.get(r),c=void 0===a?r.size:a<s?a+1:0;if(!r.has(c))return e(r,c);if(r.size<o){for(;r.has(c);)c=Math.floor(Math.random()*s);return e(r,c)}if(r.size>n)throw new Error("Congratulations, you created a collection of unique numbers which uses all available integers!");for(;r.has(c);)c=Math.floor(Math.random()*n);return e(r,c)}},c=new WeakMap,i=r(c),d=a(i,c),l=t(d);e.addUniqueNumber=l,e.generateUniqueNumber=d}(t)}},t={};function r(n){var o=t[n];if(void 0!==o)return o.exports;var s=t[n]={exports:{}};return e[n].call(s.exports,s,s.exports,r),s.exports}(()=>{"use strict";var e=r(455);const t=new WeakMap,n=new WeakMap,o=(r=>{const o=(s=r,{...s,connect:({call:e})=>async()=>{const{port1:r,port2:n}=new MessageChannel,o=await e("connect",{port:r},[r]);return t.set(n,o),n},disconnect:({call:e})=>async r=>{const n=t.get(r);if(void 0===n)throw new Error("The given port is not connected.");await e("disconnect",{portId:n})},isSupported:({call:e})=>()=>e("isSupported")});var s;return t=>{const r=(e=>{if(n.has(e))return n.get(e);const t=new Map;return n.set(e,t),t})(t);t.addEventListener("message",(({data:e})=>{const{id:t}=e;if(null!==t&&r.has(t)){const{reject:n,resolve:o}=r.get(t);r.delete(t),void 0===e.error?o(e.result):n(new Error(e.error.message))}})),(e=>"function"==typeof e.start)(t)&&t.start();const s=(n,o=null,s=[])=>new Promise(((a,c)=>{const i=(0,e.generateUniqueNumber)(r);r.set(i,{reject:c,resolve:a}),null===o?t.postMessage({id:i,method:n},s):t.postMessage({id:i,method:n,params:o},s)})),a=(e,r,n=[])=>{t.postMessage({id:null,method:e,params:r},n)};let c={};for(const[e,t]of Object.entries(o))c={...c,[e]:t({call:s,notify:a})};return{...c}}})({characterize:({call:e})=>()=>e("characterize"),encode:({call:e})=>(t,r)=>e("encode",{recordingId:t,timeslice:r}),record:({call:e})=>async(t,r,n)=>{await e("record",{recordingId:t,sampleRate:r,typedArrays:n},n.map((({buffer:e})=>e)))}}),s=-32603,a=-32602,c=-32601,i=(e,t)=>Object.assign(new Error(e),{status:t}),d=e=>i('The handler of the method called "'.concat(e,'" returned an unexpected result.'),s),l=(e,t)=>async({data:{id:r,method:n,params:o}})=>{const a=t[n];try{if(void 0===a)throw(e=>i('The requested method called "'.concat(e,'" is not supported.'),c))(n);const t=void 0===o?a():a(o);if(void 0===t)throw(e=>i('The handler of the method called "'.concat(e,'" returned no required result.'),s))(n);const l=t instanceof Promise?await t:t;if(null===r){if(void 0!==l.result)throw d(n)}else{if(void 0===l.result)throw d(n);const{result:t,transferables:o=[]}=l;e.postMessage({id:r,result:t},o)}}catch(t){const{message:n,status:o=-32603}=t;e.postMessage({error:{code:o,message:n},id:r})}},u=new Map,h=(t,r,n)=>({...r,connect:({port:n})=>{n.start();const o=t(n,r),s=(0,e.generateUniqueNumber)(u);return u.set(s,(()=>{o(),n.close(),u.delete(s)})),{result:s}},disconnect:({portId:e})=>{const t=u.get(e);if(void 0===t)throw(e=>i('The specified parameter called "portId" with the given value "'.concat(e,'" does not identify a port connected to this worker.'),a))(e);return t(),{result:null}},isSupported:async()=>{if(await new Promise((e=>{const t=new ArrayBuffer(0),{port1:r,port2:n}=new MessageChannel;r.onmessage=({data:t})=>e(null!==t),n.postMessage(t,[t])}))){const e=n();return{result:e instanceof Promise?await e:e}}return{result:!1}}}),w=(e,t,r=()=>!0)=>{const n=h(w,t,r),o=l(e,n);return e.addEventListener("message",o),()=>e.removeEventListener("message",o)},f=e=>{e.onmessage=null,e.close()},p=new Map,m=new Map,g=((e,t)=>r=>{const n=t.get(r);if(void 0===n)throw new Error("There was no encoder stored with the given id.");e.delete(n),t.delete(r)})(p,m),v=new Map,y=(e=>t=>{const r=e.get(t);if(void 0===r)throw new Error("There was no instance of an encoder stored with the given id.");return r})(v),M=((e,t)=>r=>{const n=t(r);return e.delete(r),n})(v,y),E=((e,t)=>r=>{const[n,o,s,a]=t(r);return s?new Promise((t=>{o.onmessage=({data:s})=>{0===s.length?(e(o),t(n.encode(r,null))):n.record(r,a,s)}})):n.encode(r,null)})(f,M),b=(e=>t=>{for(const[r,n]of Array.from(e.values()))if(r.test(t))return n;throw new Error("There is no encoder registered which could handle the given mimeType.")})(p),T=((e,t,r)=>(n,o,s)=>{if(t.has(n))throw new Error('There is already an encoder instance registered with an id called "'.concat(n,'".'));const a=r(o),{port1:c,port2:i}=new MessageChannel,d=[a,c,!0,s];return t.set(n,d),c.onmessage=({data:t})=>{0===t.length?(e(c),d[2]=!1):a.record(n,s,t.map((e=>"number"==typeof e?new Float32Array(e):e)))},i})(f,v,b),I=((e,t,r)=>async(n,o)=>{const s=r(o),a=await s.characterize(),c=a.toString();if(e.has(c))throw new Error("There is already an encoder stored which handles exactly the same mime types.");if(t.has(n))throw new Error('There is already an encoder registered with an id called "'.concat(n,'".'));return e.set(c,[a,s]),t.set(n,c),a})(p,m,o),A=(e=>(t,r)=>{const[n]=e(t);return n.encode(t,r)})(y);w(self,{deregister:async({encoderId:e})=>(g(e),{result:null}),encode:async({encoderInstanceId:e,timeslice:t})=>{const r=null===t?await E(e):await A(e,t);return{result:r,transferables:r}},instantiate:({encoderInstanceId:e,mimeType:t,sampleRate:r})=>{const n=T(e,t,r);return{result:n,transferables:[n]}},register:async({encoderId:e,port:t})=>({result:await I(e,t)})})})()})();`, tr = new Blob([er], { type: "application/javascript; charset=utf-8" }), Kt = URL.createObjectURL(tr), Fe = Jn(Kt), nr = Fe.deregister, Re = Fe.encode, Qt = Fe.instantiate, rr = Fe.register;
URL.revokeObjectURL(Kt);
const or = (e) => (t, n) => {
  if (e === null)
    throw new Error("A native BlobEvent could not be created.");
  return new e(t, n);
}, sr = (e, t) => (n, r, o) => {
  const s = [];
  let a = r, c = 0;
  for (; c < n.byteLength; )
    if (a === null) {
      const i = t(n, c);
      if (i === null)
        break;
      const { length: u, type: d } = i;
      a = d, c += u;
    } else {
      const i = e(n, c, a, o);
      if (i === null)
        break;
      const { content: u, length: d } = i;
      a = null, c += d, u !== null && s.push(u);
    }
  return { contents: s, currentElementType: a, offset: c };
}, ar = (e, t) => class {
  constructor(r = null) {
    this._listeners = /* @__PURE__ */ new WeakMap(), this._nativeEventTarget = r === null ? e() : r;
  }
  addEventListener(r, o, s) {
    if (o !== null) {
      let a = this._listeners.get(o);
      a === void 0 && (a = t(this, o), typeof o == "function" && this._listeners.set(o, a)), this._nativeEventTarget.addEventListener(r, a, s);
    }
  }
  dispatchEvent(r) {
    return this._nativeEventTarget.dispatchEvent(r);
  }
  removeEventListener(r, o, s) {
    const a = o === null ? void 0 : this._listeners.get(o);
    this._nativeEventTarget.removeEventListener(r, a === void 0 ? null : a, s);
  }
}, ir = (e) => () => {
  if (e === null)
    throw new Error("A native EventTarget could not be created.");
  return e.document.createElement("p");
}, cr = (e = "") => {
  try {
    return new DOMException(e, "InvalidModificationError");
  } catch (t) {
    return t.code = 13, t.message = e, t.name = "InvalidModificationError", t;
  }
}, ur = () => {
  try {
    return new DOMException("", "InvalidStateError");
  } catch (e) {
    return e.code = 11, e.name = "InvalidStateError", e;
  }
}, lr = (e) => {
  if (e !== null && // Bug #14: Before v14.1 Safari did not support the BlobEvent.
  e.BlobEvent !== void 0 && e.MediaStream !== void 0 && /*
   * Bug #10: An early experimental implemenation in Safari v14 did not provide the isTypeSupported() function.
   *
   * Bug #17: Safari up to v14.1.2 throttled the processing on hidden tabs if there was no active audio output. This is not tested
   * here but should be covered by the following test, too.
   */
  (e.MediaRecorder === void 0 || e.MediaRecorder.isTypeSupported !== void 0)) {
    if (e.MediaRecorder === void 0)
      return Promise.resolve(!0);
    const t = e.document.createElement("canvas"), n = t.getContext("2d");
    if (n === null || typeof t.captureStream != "function")
      return Promise.resolve(!1);
    const r = t.captureStream();
    return Promise.all([
      /*
       * Bug #5: Up until v70 Firefox did emit a blob of type video/webm when asked to encode a MediaStream with a video track into an
       * audio codec.
       */
      new Promise((o) => {
        const s = "audio/webm";
        try {
          const a = new e.MediaRecorder(r, { mimeType: s });
          a.addEventListener("dataavailable", ({ data: c }) => o(c.type === s)), a.start(), setTimeout(() => a.stop(), 10);
        } catch (a) {
          o(a.name === "NotSupportedError");
        }
      }),
      /*
       * Bug #1 & #2: Up until v83 Firefox fired an error event with an UnknownError when adding or removing a track.
       *
       * Bug #3 & #4: Up until v112 Chrome dispatched an error event without any error.
       *
       * Bug #6: Up until v113 Chrome emitted a blob without any data when asked to encode a MediaStream with a video track as audio.
       * This is not directly tested here as it can only be tested by recording something for a short time. It got fixed at the same
       * time as #7 and #8.
       *
       * Bug #7 & #8: Up until v113 Chrome dispatched the dataavailable and stop events before it dispatched the error event.
       */
      new Promise((o) => {
        const s = new e.MediaRecorder(r);
        let a = !1, c = !1;
        s.addEventListener("dataavailable", () => a = !0), s.addEventListener("error", (i) => {
          o(!a && !c && "error" in i && i.error !== null && typeof i.error == "object" && "name" in i.error && i.error.name !== "UnknownError");
        }), s.addEventListener("stop", () => c = !0), s.start(), n.fillRect(0, 0, 1, 1), r.removeTrack(r.getVideoTracks()[0]);
      })
    ]).then((o) => o.every((s) => s));
  }
  return Promise.resolve(!1);
}, dr = (e, t, n, r, o, s, a) => class extends s {
  constructor(i, u = {}) {
    const { mimeType: d } = u;
    if (a !== null && // Bug #10: Safari does not yet implement the isTypeSupported() method.
    (d === void 0 || a.isTypeSupported !== void 0 && a.isTypeSupported(d))) {
      const l = e(a, i, u);
      super(l), this._internalMediaRecorder = l;
    } else if (d !== void 0 && o.some((l) => l.test(d)))
      super(), a !== null && a.isTypeSupported !== void 0 && a.isTypeSupported("audio/webm;codecs=pcm") ? this._internalMediaRecorder = r(this, a, i, d) : this._internalMediaRecorder = n(this, i, d);
    else
      throw a !== null && e(a, i, u), t();
    this._ondataavailable = null, this._onerror = null, this._onpause = null, this._onresume = null, this._onstart = null, this._onstop = null;
  }
  get mimeType() {
    return this._internalMediaRecorder.mimeType;
  }
  get ondataavailable() {
    return this._ondataavailable === null ? this._ondataavailable : this._ondataavailable[0];
  }
  set ondataavailable(i) {
    if (this._ondataavailable !== null && this.removeEventListener("dataavailable", this._ondataavailable[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("dataavailable", u), this._ondataavailable = [i, u];
    } else
      this._ondataavailable = null;
  }
  get onerror() {
    return this._onerror === null ? this._onerror : this._onerror[0];
  }
  set onerror(i) {
    if (this._onerror !== null && this.removeEventListener("error", this._onerror[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("error", u), this._onerror = [i, u];
    } else
      this._onerror = null;
  }
  get onpause() {
    return this._onpause === null ? this._onpause : this._onpause[0];
  }
  set onpause(i) {
    if (this._onpause !== null && this.removeEventListener("pause", this._onpause[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("pause", u), this._onpause = [i, u];
    } else
      this._onpause = null;
  }
  get onresume() {
    return this._onresume === null ? this._onresume : this._onresume[0];
  }
  set onresume(i) {
    if (this._onresume !== null && this.removeEventListener("resume", this._onresume[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("resume", u), this._onresume = [i, u];
    } else
      this._onresume = null;
  }
  get onstart() {
    return this._onstart === null ? this._onstart : this._onstart[0];
  }
  set onstart(i) {
    if (this._onstart !== null && this.removeEventListener("start", this._onstart[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("start", u), this._onstart = [i, u];
    } else
      this._onstart = null;
  }
  get onstop() {
    return this._onstop === null ? this._onstop : this._onstop[0];
  }
  set onstop(i) {
    if (this._onstop !== null && this.removeEventListener("stop", this._onstop[1]), typeof i == "function") {
      const u = i.bind(this);
      this.addEventListener("stop", u), this._onstop = [i, u];
    } else
      this._onstop = null;
  }
  get state() {
    return this._internalMediaRecorder.state;
  }
  pause() {
    return this._internalMediaRecorder.pause();
  }
  resume() {
    return this._internalMediaRecorder.resume();
  }
  start(i) {
    return this._internalMediaRecorder.start(i);
  }
  stop() {
    return this._internalMediaRecorder.stop();
  }
  static isTypeSupported(i) {
    return a !== null && // Bug #10: Safari does not yet implement the isTypeSupported() method.
    a.isTypeSupported !== void 0 && a.isTypeSupported(i) || o.some((u) => u.test(i));
  }
}, fr = (e) => e !== null && e.BlobEvent !== void 0 ? e.BlobEvent : null, hr = (e) => e === null || e.MediaRecorder === void 0 ? null : e.MediaRecorder, pr = (e) => (t, n, r) => {
  const o = /* @__PURE__ */ new Map(), s = /* @__PURE__ */ new WeakMap(), a = /* @__PURE__ */ new WeakMap(), c = [], i = new t(n, r), u = /* @__PURE__ */ new WeakMap();
  return i.addEventListener("stop", ({ isTrusted: d }) => {
    d && setTimeout(() => c.shift());
  }), i.addEventListener = /* @__PURE__ */ ((d) => (l, g, w) => {
    let p = g;
    if (typeof g == "function")
      if (l === "dataavailable") {
        const f = [];
        p = (m) => {
          const [[h, A] = [!1, !1]] = c;
          h && !A ? f.push(m) : g.call(i, m);
        }, o.set(g, f), s.set(g, p);
      } else
        l === "error" ? (p = (f) => {
          f instanceof ErrorEvent ? g.call(i, f) : g.call(i, new ErrorEvent("error", { error: f.error }));
        }, a.set(g, p)) : l === "stop" && (p = (f) => {
          for (const [m, h] of o.entries())
            if (h.length > 0) {
              const [A] = h;
              h.length > 1 && Object.defineProperty(A, "data", {
                value: new Blob(h.map(({ data: v }) => v), { type: A.data.type })
              }), h.length = 0, m.call(i, A);
            }
          g.call(i, f);
        }, u.set(g, p));
    return d.call(i, l, p, w);
  })(i.addEventListener), i.removeEventListener = /* @__PURE__ */ ((d) => (l, g, w) => {
    let p = g;
    if (typeof g == "function") {
      if (l === "dataavailable") {
        o.delete(g);
        const f = s.get(g);
        f !== void 0 && (p = f);
      } else if (l === "error") {
        const f = a.get(g);
        f !== void 0 && (p = f);
      } else if (l === "stop") {
        const f = u.get(g);
        f !== void 0 && (p = f);
      }
    }
    return d.call(i, l, p, w);
  })(i.removeEventListener), i.start = /* @__PURE__ */ ((d) => (l) => {
    if (r.mimeType !== void 0 && r.mimeType.startsWith("audio/") && n.getVideoTracks().length > 0)
      throw e();
    return i.state === "inactive" && c.push([l !== void 0, !0]), l === void 0 ? d.call(i) : d.call(i, l);
  })(i.start), i.stop = /* @__PURE__ */ ((d) => () => {
    i.state !== "inactive" && (c[0][1] = !1), d.call(i);
  })(i.stop), i;
}, nt = () => {
  try {
    return new DOMException("", "NotSupportedError");
  } catch (e) {
    return e.code = 9, e.name = "NotSupportedError", e;
  }
}, mr = (e) => (t, n, r, o = 2) => {
  const s = e(t, n);
  if (s === null)
    return s;
  const { length: a, value: c } = s;
  if (r === "master")
    return { content: null, length: a };
  if (n + a + c > t.byteLength)
    return null;
  if (r === "binary") {
    const i = (c / Float32Array.BYTES_PER_ELEMENT - 1) / o, u = Array.from({ length: o }, () => new Float32Array(i));
    for (let d = 0; d < i; d += 1) {
      const l = d * o + 1;
      for (let g = 0; g < o; g += 1)
        u[g][d] = t.getFloat32(n + a + (l + g) * Float32Array.BYTES_PER_ELEMENT, !0);
    }
    return { content: u, length: a + c };
  }
  return { content: null, length: a + c };
}, gr = (e) => (t, n) => {
  const r = e(t, n);
  if (r === null)
    return r;
  const { length: o, value: s } = r;
  return s === 35 ? { length: o, type: "binary" } : s === 46 || s === 97 || s === 88713574 || s === 106212971 || s === 139690087 || s === 172351395 || s === 256095861 ? { length: o, type: "master" } : { length: o, type: "unknown" };
}, wr = (e) => (t, n) => {
  const r = e(t, n);
  if (r === null)
    return r;
  const o = n + Math.floor((r - 1) / 8);
  if (o + r > t.byteLength)
    return null;
  let a = t.getUint8(o) & (1 << 8 - r % 8) - 1;
  for (let c = 1; c < r; c += 1)
    a = (a << 8) + t.getUint8(o + c);
  return { length: r, value: a };
}, Rt = Symbol.observable || "@@observable";
function vr(e) {
  return Symbol.observable || (typeof e == "function" && e.prototype && e.prototype[Symbol.observable] ? (e.prototype[Rt] = e.prototype[Symbol.observable], delete e.prototype[Symbol.observable]) : (e[Rt] = e[Symbol.observable], delete e[Symbol.observable])), e;
}
const Oe = () => {
}, Lt = (e) => {
  throw e;
};
function _r(e) {
  return e ? e.next && e.error && e.complete ? e : {
    complete: (e.complete ?? Oe).bind(e),
    error: (e.error ?? Lt).bind(e),
    next: (e.next ?? Oe).bind(e)
  } : {
    complete: Oe,
    error: Lt,
    next: Oe
  };
}
const yr = (e) => (t, n, r) => e((o) => {
  const s = (a) => o.next(a);
  return t.addEventListener(n, s, r), () => t.removeEventListener(n, s, r);
}), Er = (e, t) => {
  const n = () => {
  }, r = (o) => typeof o[0] == "function";
  return (o) => {
    const s = (...a) => {
      const c = o(r(a) ? t({ next: a[0] }) : t(...a));
      return c !== void 0 ? c : n;
    };
    return s[Symbol.observable] = () => ({
      subscribe: (...a) => ({ unsubscribe: s(...a) })
    }), e(s);
  };
}, br = Er(vr, _r), Jt = yr(br), Ar = (e, t, n) => async (r) => {
  const o = new e([n], { type: "application/javascript; charset=utf-8" }), s = t.createObjectURL(o);
  try {
    await r(s);
  } finally {
    t.revokeObjectURL(s);
  }
}, Cr = (e) => ({ data: t }) => {
  const { id: n } = t;
  if (n !== null) {
    const r = e.get(n);
    if (r !== void 0) {
      const { reject: o, resolve: s } = r;
      e.delete(n), t.error === void 0 ? s(t.result) : o(new Error(t.error.message));
    }
  }
}, Tr = (e) => (t, n) => (r, o = []) => new Promise((s, a) => {
  const c = e(t);
  t.set(c, { reject: a, resolve: s }), n.postMessage({ id: c, ...r }, o);
}), Mr = (e, t, n, r) => (o, s, a = {}) => {
  const c = new o(s, "recorder-audio-worklet-processor", {
    ...a,
    channelCountMode: "explicit",
    numberOfInputs: 1,
    numberOfOutputs: 0
  }), i = /* @__PURE__ */ new Map(), u = t(i, c.port), d = n(c.port, "message")(e(i));
  c.port.start();
  let l = "inactive";
  return Object.defineProperties(c, {
    pause: {
      get() {
        return async () => (r(["recording"], l), l = "paused", u({
          method: "pause"
        }));
      }
    },
    port: {
      get() {
        throw new Error("The port of a RecorderAudioWorkletNode can't be accessed.");
      }
    },
    record: {
      get() {
        return async (g) => (r(["inactive"], l), l = "recording", u({
          method: "record",
          params: { encoderPort: g }
        }, [g]));
      }
    },
    resume: {
      get() {
        return async () => (r(["paused"], l), l = "recording", u({
          method: "resume"
        }));
      }
    },
    stop: {
      get() {
        return async () => {
          r(["paused", "recording"], l), l = "stopped";
          try {
            await u({ method: "stop" });
          } finally {
            d();
          }
        };
      }
    }
  }), c;
}, Nr = (e, t) => {
  if (!e.includes(t))
    throw new Error(`Expected the state to be ${e.map((n) => `"${n}"`).join(" or ")} but it was "${t}".`);
}, Or = '(()=>{"use strict";class e extends AudioWorkletProcessor{constructor(){super(),this._encoderPort=null,this._numberOfChannels=0,this._state="inactive",this.port.onmessage=({data:e})=>{"pause"===e.method?"active"===this._state||"recording"===this._state?(this._state="paused",this._sendAcknowledgement(e.id)):this._sendUnexpectedStateError(e.id):"record"===e.method?"inactive"===this._state?(this._encoderPort=e.params.encoderPort,this._state="active",this._sendAcknowledgement(e.id)):this._sendUnexpectedStateError(e.id):"resume"===e.method?"paused"===this._state?(this._state="active",this._sendAcknowledgement(e.id)):this._sendUnexpectedStateError(e.id):"stop"===e.method?"active"!==this._state&&"paused"!==this._state&&"recording"!==this._state||null===this._encoderPort?this._sendUnexpectedStateError(e.id):(this._stop(this._encoderPort),this._sendAcknowledgement(e.id)):"number"==typeof e.id&&this.port.postMessage({error:{code:-32601,message:"The requested method is not supported."},id:e.id})}}process([e]){if("inactive"===this._state||"paused"===this._state)return!0;if("active"===this._state){if(void 0===e)throw new Error("No channelData was received for the first input.");if(0===e.length)return!0;this._state="recording"}if("recording"===this._state&&null!==this._encoderPort){if(void 0===e)throw new Error("No channelData was received for the first input.");return 0===e.length?this._encoderPort.postMessage(Array.from({length:this._numberOfChannels},(()=>128))):(this._encoderPort.postMessage(e,e.map((({buffer:e})=>e))),this._numberOfChannels=e.length),!0}return!1}_sendAcknowledgement(e){this.port.postMessage({id:e,result:null})}_sendUnexpectedStateError(e){this.port.postMessage({error:{code:-32603,message:"The internal state does not allow to process the given message."},id:e})}_stop(e){e.postMessage([]),e.close(),this._encoderPort=null,this._state="stopped"}}e.parameterDescriptors=[],registerProcessor("recorder-audio-worklet-processor",e)})();', kr = Ar(Blob, URL, Or), Ir = Mr(Cr, Tr(Kn), Jt, Nr), Pt = (e, t, n) => ({ endTime: t, insertTime: n, type: "exponentialRampToValue", value: e }), Bt = (e, t, n) => ({ endTime: t, insertTime: n, type: "linearRampToValue", value: e }), rt = (e, t) => ({ startTime: t, type: "setValue", value: e }), en = (e, t, n) => ({ duration: n, startTime: t, type: "setValueCurve", values: e }), tn = (e, t, { startTime: n, target: r, timeConstant: o }) => r + (t - r) * Math.exp((n - e) / o), me = (e) => e.type === "exponentialRampToValue", Le = (e) => e.type === "linearRampToValue", re = (e) => me(e) || Le(e), ht = (e) => e.type === "setValue", J = (e) => e.type === "setValueCurve", Pe = (e, t, n, r) => {
  const o = e[t];
  return o === void 0 ? r : re(o) || ht(o) ? o.value : J(o) ? o.values[o.values.length - 1] : tn(n, Pe(e, t - 1, o.startTime, r), o);
}, Ut = (e, t, n, r, o) => n === void 0 ? [r.insertTime, o] : re(n) ? [n.endTime, n.value] : ht(n) ? [n.startTime, n.value] : J(n) ? [
  n.startTime + n.duration,
  n.values[n.values.length - 1]
] : [
  n.startTime,
  Pe(e, t - 1, n.startTime, o)
], ot = (e) => e.type === "cancelAndHold", st = (e) => e.type === "cancelScheduledValues", ne = (e) => ot(e) || st(e) ? e.cancelTime : me(e) || Le(e) ? e.endTime : e.startTime, Dt = (e, t, n, { endTime: r, value: o }) => n === o ? o : 0 < n && 0 < o || n < 0 && o < 0 ? n * (o / n) ** ((e - t) / (r - t)) : 0, Wt = (e, t, n, { endTime: r, value: o }) => n + (e - t) / (r - t) * (o - n), Sr = (e, t) => {
  const n = Math.floor(t), r = Math.ceil(t);
  return n === r ? e[n] : (1 - (t - n)) * e[n] + (1 - (r - t)) * e[r];
}, Rr = (e, { duration: t, startTime: n, values: r }) => {
  const o = (e - n) / t * (r.length - 1);
  return Sr(r, o);
}, ke = (e) => e.type === "setTarget";
class Lr {
  constructor(t) {
    this._automationEvents = [], this._currenTime = 0, this._defaultValue = t;
  }
  [Symbol.iterator]() {
    return this._automationEvents[Symbol.iterator]();
  }
  add(t) {
    const n = ne(t);
    if (ot(t) || st(t)) {
      const r = this._automationEvents.findIndex((s) => st(t) && J(s) ? s.startTime + s.duration >= n : ne(s) >= n), o = this._automationEvents[r];
      if (r !== -1 && (this._automationEvents = this._automationEvents.slice(0, r)), ot(t)) {
        const s = this._automationEvents[this._automationEvents.length - 1];
        if (o !== void 0 && re(o)) {
          if (s !== void 0 && ke(s))
            throw new Error("The internal list is malformed.");
          const a = s === void 0 ? o.insertTime : J(s) ? s.startTime + s.duration : ne(s), c = s === void 0 ? this._defaultValue : J(s) ? s.values[s.values.length - 1] : s.value, i = me(o) ? Dt(n, a, c, o) : Wt(n, a, c, o), u = me(o) ? Pt(i, n, this._currenTime) : Bt(i, n, this._currenTime);
          this._automationEvents.push(u);
        }
        if (s !== void 0 && ke(s) && this._automationEvents.push(rt(this.getValue(n), n)), s !== void 0 && J(s) && s.startTime + s.duration > n) {
          const a = n - s.startTime, c = (s.values.length - 1) / s.duration, i = Math.max(2, 1 + Math.ceil(a * c)), u = a / (i - 1) * c, d = s.values.slice(0, i);
          if (u < 1)
            for (let l = 1; l < i; l += 1) {
              const g = u * l % 1;
              d[l] = s.values[l - 1] * (1 - g) + s.values[l] * g;
            }
          this._automationEvents[this._automationEvents.length - 1] = en(d, s.startTime, a);
        }
      }
    } else {
      const r = this._automationEvents.findIndex((a) => ne(a) > n), o = r === -1 ? this._automationEvents[this._automationEvents.length - 1] : this._automationEvents[r - 1];
      if (o !== void 0 && J(o) && ne(o) + o.duration > n)
        return !1;
      const s = me(t) ? Pt(t.value, t.endTime, this._currenTime) : Le(t) ? Bt(t.value, n, this._currenTime) : t;
      if (r === -1)
        this._automationEvents.push(s);
      else {
        if (J(t) && n + t.duration > ne(this._automationEvents[r]))
          return !1;
        this._automationEvents.splice(r, 0, s);
      }
    }
    return !0;
  }
  flush(t) {
    const n = this._automationEvents.findIndex((r) => ne(r) > t);
    if (n > 1) {
      const r = this._automationEvents.slice(n - 1), o = r[0];
      ke(o) && r.unshift(rt(Pe(this._automationEvents, n - 2, o.startTime, this._defaultValue), o.startTime)), this._automationEvents = r;
    }
  }
  getValue(t) {
    if (this._automationEvents.length === 0)
      return this._defaultValue;
    const n = this._automationEvents.findIndex((a) => ne(a) > t), r = this._automationEvents[n], o = (n === -1 ? this._automationEvents.length : n) - 1, s = this._automationEvents[o];
    if (s !== void 0 && ke(s) && (r === void 0 || !re(r) || r.insertTime > t))
      return tn(t, Pe(this._automationEvents, o - 1, s.startTime, this._defaultValue), s);
    if (s !== void 0 && ht(s) && (r === void 0 || !re(r)))
      return s.value;
    if (s !== void 0 && J(s) && (r === void 0 || !re(r) || s.startTime + s.duration > t))
      return t < s.startTime + s.duration ? Rr(t, s) : s.values[s.values.length - 1];
    if (s !== void 0 && re(s) && (r === void 0 || !re(r)))
      return s.value;
    if (r !== void 0 && me(r)) {
      const [a, c] = Ut(this._automationEvents, o, s, r, this._defaultValue);
      return Dt(t, a, c, r);
    }
    if (r !== void 0 && Le(r)) {
      const [a, c] = Ut(this._automationEvents, o, s, r, this._defaultValue);
      return Wt(t, a, c, r);
    }
    return this._defaultValue;
  }
}
const Pr = (e) => ({ cancelTime: e, type: "cancelAndHold" }), Br = (e) => ({ cancelTime: e, type: "cancelScheduledValues" }), Ur = (e, t) => ({ endTime: t, type: "exponentialRampToValue", value: e }), Dr = (e, t) => ({ endTime: t, type: "linearRampToValue", value: e }), Wr = (e, t, n) => ({ startTime: t, target: e, timeConstant: n, type: "setTarget" }), Vr = () => new DOMException("", "AbortError"), xr = (e) => (t, n, [r, o, s], a) => {
  e(t[o], [n, r, s], (c) => c[0] === n && c[1] === r, a);
}, Fr = (e) => (t, n, r) => {
  const o = [];
  for (let s = 0; s < r.numberOfInputs; s += 1)
    o.push(/* @__PURE__ */ new Set());
  e.set(t, {
    activeInputs: o,
    outputs: /* @__PURE__ */ new Set(),
    passiveInputs: /* @__PURE__ */ new WeakMap(),
    renderer: n
  });
}, jr = (e) => (t, n) => {
  e.set(t, { activeInputs: /* @__PURE__ */ new Set(), passiveInputs: /* @__PURE__ */ new WeakMap(), renderer: n });
}, ge = /* @__PURE__ */ new WeakSet(), nn = /* @__PURE__ */ new WeakMap(), rn = /* @__PURE__ */ new WeakMap(), on = /* @__PURE__ */ new WeakMap(), sn = /* @__PURE__ */ new WeakMap(), an = /* @__PURE__ */ new WeakMap(), cn = /* @__PURE__ */ new WeakMap(), at = /* @__PURE__ */ new WeakMap(), it = /* @__PURE__ */ new WeakMap(), ct = /* @__PURE__ */ new WeakMap(), un = {
  construct() {
    return un;
  }
}, Gr = (e) => {
  try {
    const t = new Proxy(e, un);
    new t();
  } catch {
    return !1;
  }
  return !0;
}, Vt = /^import(?:(?:[\s]+[\w]+|(?:[\s]+[\w]+[\s]*,)?[\s]*\{[\s]*[\w]+(?:[\s]+as[\s]+[\w]+)?(?:[\s]*,[\s]*[\w]+(?:[\s]+as[\s]+[\w]+)?)*[\s]*}|(?:[\s]+[\w]+[\s]*,)?[\s]*\*[\s]+as[\s]+[\w]+)[\s]+from)?(?:[\s]*)("([^"\\]|\\.)+"|'([^'\\]|\\.)+')(?:[\s]*);?/, xt = (e, t) => {
  const n = [];
  let r = e.replace(/^[\s]+/, ""), o = r.match(Vt);
  for (; o !== null; ) {
    const s = o[1].slice(1, -1), a = o[0].replace(/([\s]+)?;?$/, "").replace(s, new URL(s, t).toString());
    n.push(a), r = r.slice(o[0].length).replace(/^[\s]+/, ""), o = r.match(Vt);
  }
  return [n.join(";"), r];
}, Ft = (e) => {
  if (e !== void 0 && !Array.isArray(e))
    throw new TypeError("The parameterDescriptors property of given value for processorCtor is not an array.");
}, jt = (e) => {
  if (!Gr(e))
    throw new TypeError("The given value for processorCtor should be a constructor.");
  if (e.prototype === null || typeof e.prototype != "object")
    throw new TypeError("The given value for processorCtor should have a prototype.");
}, $r = (e, t, n, r, o, s, a, c, i, u, d, l, g) => {
  let w = 0;
  return (p, f, m = { credentials: "omit" }) => {
    const h = d.get(p);
    if (h !== void 0 && h.has(f))
      return Promise.resolve();
    const A = u.get(p);
    if (A !== void 0) {
      const E = A.get(f);
      if (E !== void 0)
        return E;
    }
    const v = s(p), T = v.audioWorklet === void 0 ? o(f).then(([E, b]) => {
      const [y, _] = xt(E, b), M = `${y};((a,b)=>{(a[b]=a[b]||[]).push((AudioWorkletProcessor,global,registerProcessor,sampleRate,self,window)=>{${_}
})})(window,'_AWGS')`;
      return n(M);
    }).then(() => {
      const E = g._AWGS.pop();
      if (E === void 0)
        throw new SyntaxError();
      r(v.currentTime, v.sampleRate, () => E(class {
      }, void 0, (b, y) => {
        if (b.trim() === "")
          throw t();
        const _ = it.get(v);
        if (_ !== void 0) {
          if (_.has(b))
            throw t();
          jt(y), Ft(y.parameterDescriptors), _.set(b, y);
        } else
          jt(y), Ft(y.parameterDescriptors), it.set(v, /* @__PURE__ */ new Map([[b, y]]));
      }, v.sampleRate, void 0, void 0));
    }) : Promise.all([
      o(f),
      Promise.resolve(e(l, l))
    ]).then(([[E, b], y]) => {
      const _ = w + 1;
      w = _;
      const [M, S] = xt(E, b), B = `${M};((AudioWorkletProcessor,registerProcessor)=>{${S}
})(${y ? "AudioWorkletProcessor" : "class extends AudioWorkletProcessor {__b=new WeakSet();constructor(){super();(p=>p.postMessage=(q=>(m,t)=>q.call(p,m,t?t.filter(u=>!this.__b.has(u)):t))(p.postMessage))(this.port)}}"},(n,p)=>registerProcessor(n,class extends p{${y ? "" : "__c = (a) => a.forEach(e=>this.__b.add(e.buffer));"}process(i,o,p){${y ? "" : "i.forEach(this.__c);o.forEach(this.__c);this.__c(Object.values(p));"}return super.process(i.map(j=>j.some(k=>k.length===0)?[]:j),o,p)}}));registerProcessor('__sac${_}',class extends AudioWorkletProcessor{process(){return !1}})`, D = new Blob([B], { type: "application/javascript; charset=utf-8" }), I = URL.createObjectURL(D);
      return v.audioWorklet.addModule(I, m).then(() => {
        if (c(v))
          return v;
        const U = a(v);
        return U.audioWorklet.addModule(I, m).then(() => U);
      }).then((U) => {
        if (i === null)
          throw new SyntaxError();
        try {
          new i(U, `__sac${_}`);
        } catch {
          throw new SyntaxError();
        }
      }).finally(() => URL.revokeObjectURL(I));
    });
    return A === void 0 ? u.set(p, /* @__PURE__ */ new Map([[f, T]])) : A.set(f, T), T.then(() => {
      const E = d.get(p);
      E === void 0 ? d.set(p, /* @__PURE__ */ new Set([f])) : E.add(f);
    }).finally(() => {
      const E = u.get(p);
      E !== void 0 && E.delete(f);
    }), T;
  };
}, K = (e, t) => {
  const n = e.get(t);
  if (n === void 0)
    throw new Error("A value with the given key could not be found.");
  return n;
}, je = (e, t) => {
  const n = Array.from(e).filter(t);
  if (n.length > 1)
    throw Error("More than one element was found.");
  if (n.length === 0)
    throw Error("No element was found.");
  const [r] = n;
  return e.delete(r), r;
}, ln = (e, t, n, r) => {
  const o = K(e, t), s = je(o, (a) => a[0] === n && a[1] === r);
  return o.size === 0 && e.delete(t), s;
}, Ae = (e) => K(cn, e), Be = (e) => {
  if (ge.has(e))
    throw new Error("The AudioNode is already stored.");
  ge.add(e), Ae(e).forEach((t) => t(!0));
}, dn = (e) => "port" in e, pt = (e) => {
  if (!ge.has(e))
    throw new Error("The AudioNode is not stored.");
  ge.delete(e), Ae(e).forEach((t) => t(!1));
}, ut = (e, t) => {
  !dn(e) && t.every((n) => n.size === 0) && pt(e);
}, qr = (e, t, n, r, o, s, a, c, i, u, d, l, g) => {
  const w = /* @__PURE__ */ new WeakMap();
  return (p, f, m, h, A) => {
    const { activeInputs: v, passiveInputs: T } = s(f), { outputs: E } = s(p), b = c(p), y = (_) => {
      const M = i(f), S = i(p);
      if (_) {
        const N = ln(T, p, m, h);
        e(v, p, N, !1), !A && !l(p) && n(S, M, m, h), g(f) && Be(f);
      } else {
        const N = r(v, p, m, h);
        t(T, h, N, !1), !A && !l(p) && o(S, M, m, h);
        const L = a(f);
        if (L === 0)
          d(f) && ut(f, v);
        else {
          const P = w.get(f);
          P !== void 0 && clearTimeout(P), w.set(f, setTimeout(() => {
            d(f) && ut(f, v);
          }, L * 1e3));
        }
      }
    };
    return u(E, [f, m, h], (_) => _[0] === f && _[1] === m && _[2] === h, !0) ? (b.add(y), d(p) ? e(v, p, [m, h, y], !0) : t(T, h, [p, m, y], !0), !0) : !1;
  };
}, zr = (e) => (t, n, [r, o, s], a) => {
  const c = t.get(r);
  c === void 0 ? t.set(r, /* @__PURE__ */ new Set([[o, n, s]])) : e(c, [o, n, s], (i) => i[0] === o && i[1] === n, a);
}, Xr = (e) => (t, n) => {
  const r = e(t, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    gain: 0
  });
  n.connect(r).connect(t.destination);
  const o = () => {
    n.removeEventListener("ended", o), n.disconnect(r), r.disconnect();
  };
  n.addEventListener("ended", o);
}, Yr = (e) => (t, n) => {
  e(t).add(n);
}, fn = (e, t) => e.context === t, Gt = (e) => {
  try {
    e.copyToChannel(new Float32Array(1), 0, -1);
  } catch {
    return !1;
  }
  return !0;
}, ue = () => new DOMException("", "IndexSizeError"), Hr = (e) => {
  e.getChannelData = /* @__PURE__ */ ((t) => (n) => {
    try {
      return t.call(e, n);
    } catch (r) {
      throw r.code === 12 ? ue() : r;
    }
  })(e.getChannelData);
}, Zr = {
  numberOfChannels: 1
}, Kr = (e, t, n, r, o, s, a, c) => {
  let i = null;
  return class hn {
    constructor(d) {
      if (o === null)
        throw new Error("Missing the native OfflineAudioContext constructor.");
      const { length: l, numberOfChannels: g, sampleRate: w } = { ...Zr, ...d };
      i === null && (i = new o(1, 1, 44100));
      const p = r !== null && t(s, s) ? new r({ length: l, numberOfChannels: g, sampleRate: w }) : i.createBuffer(g, l, w);
      if (p.numberOfChannels === 0)
        throw n();
      return typeof p.copyFromChannel != "function" ? (a(p), Hr(p)) : t(Gt, () => Gt(p)) || c(p), e.add(p), p;
    }
    static [Symbol.hasInstance](d) {
      return d !== null && typeof d == "object" && Object.getPrototypeOf(d) === hn.prototype || e.has(d);
    }
  };
}, Ge = -34028234663852886e22, mt = -Ge, ae = (e) => ge.has(e), Qr = {
  buffer: null,
  channelCount: 2,
  channelCountMode: "max",
  channelInterpretation: "speakers",
  // Bug #149: Safari does not yet support the detune AudioParam.
  loop: !1,
  loopEnd: 0,
  loopStart: 0,
  playbackRate: 1
}, Jr = (e, t, n, r, o, s, a, c) => class extends e {
  constructor(u, d) {
    const l = s(u), g = { ...Qr, ...d }, w = o(l, g), p = a(l), f = p ? t() : null;
    super(u, !1, w, f), this._audioBufferSourceNodeRenderer = f, this._isBufferNullified = !1, this._isBufferSet = g.buffer !== null, this._nativeAudioBufferSourceNode = w, this._onended = null, this._playbackRate = n(this, p, w.playbackRate, mt, Ge);
  }
  get buffer() {
    return this._isBufferNullified ? null : this._nativeAudioBufferSourceNode.buffer;
  }
  set buffer(u) {
    if (this._nativeAudioBufferSourceNode.buffer = u, u !== null) {
      if (this._isBufferSet)
        throw r();
      this._isBufferSet = !0;
    }
  }
  get loop() {
    return this._nativeAudioBufferSourceNode.loop;
  }
  set loop(u) {
    this._nativeAudioBufferSourceNode.loop = u;
  }
  get loopEnd() {
    return this._nativeAudioBufferSourceNode.loopEnd;
  }
  set loopEnd(u) {
    this._nativeAudioBufferSourceNode.loopEnd = u;
  }
  get loopStart() {
    return this._nativeAudioBufferSourceNode.loopStart;
  }
  set loopStart(u) {
    this._nativeAudioBufferSourceNode.loopStart = u;
  }
  get onended() {
    return this._onended;
  }
  set onended(u) {
    const d = typeof u == "function" ? c(this, u) : null;
    this._nativeAudioBufferSourceNode.onended = d;
    const l = this._nativeAudioBufferSourceNode.onended;
    this._onended = l !== null && l === d ? u : l;
  }
  get playbackRate() {
    return this._playbackRate;
  }
  start(u = 0, d = 0, l) {
    if (this._nativeAudioBufferSourceNode.start(u, d, l), this._audioBufferSourceNodeRenderer !== null && (this._audioBufferSourceNodeRenderer.start = l === void 0 ? [u, d] : [u, d, l]), this.context.state !== "closed") {
      Be(this);
      const g = () => {
        this._nativeAudioBufferSourceNode.removeEventListener("ended", g), ae(this) && pt(this);
      };
      this._nativeAudioBufferSourceNode.addEventListener("ended", g);
    }
  }
  stop(u = 0) {
    this._nativeAudioBufferSourceNode.stop(u), this._audioBufferSourceNodeRenderer !== null && (this._audioBufferSourceNodeRenderer.stop = u);
  }
}, eo = (e, t, n, r, o) => () => {
  const s = /* @__PURE__ */ new WeakMap();
  let a = null, c = null;
  const i = async (u, d) => {
    let l = n(u);
    const g = fn(l, d);
    if (!g) {
      const w = {
        buffer: l.buffer,
        channelCount: l.channelCount,
        channelCountMode: l.channelCountMode,
        channelInterpretation: l.channelInterpretation,
        // Bug #149: Safari does not yet support the detune AudioParam.
        loop: l.loop,
        loopEnd: l.loopEnd,
        loopStart: l.loopStart,
        playbackRate: l.playbackRate.value
      };
      l = t(d, w), a !== null && l.start(...a), c !== null && l.stop(c);
    }
    return s.set(d, l), g ? await e(d, u.playbackRate, l.playbackRate) : await r(d, u.playbackRate, l.playbackRate), await o(u, d, l), l;
  };
  return {
    set start(u) {
      a = u;
    },
    set stop(u) {
      c = u;
    },
    render(u, d) {
      const l = s.get(d);
      return l !== void 0 ? Promise.resolve(l) : i(u, d);
    }
  };
}, to = (e) => "playbackRate" in e, no = (e) => "frequency" in e && "gain" in e, ro = (e) => "offset" in e, oo = (e) => !("frequency" in e) && "gain" in e, so = (e) => "detune" in e && "frequency" in e && !("gain" in e), ao = (e) => "pan" in e, z = (e) => K(nn, e), Ce = (e) => K(on, e), lt = (e, t) => {
  const { activeInputs: n } = z(e);
  n.forEach((o) => o.forEach(([s]) => {
    t.includes(e) || lt(s, [...t, e]);
  }));
  const r = to(e) ? [
    // Bug #149: Safari does not yet support the detune AudioParam.
    e.playbackRate
  ] : dn(e) ? Array.from(e.parameters.values()) : no(e) ? [e.Q, e.detune, e.frequency, e.gain] : ro(e) ? [e.offset] : oo(e) ? [e.gain] : so(e) ? [e.detune, e.frequency] : ao(e) ? [e.pan] : [];
  for (const o of r) {
    const s = Ce(o);
    s !== void 0 && s.activeInputs.forEach(([a]) => lt(a, t));
  }
  ae(e) && pt(e);
}, io = (e) => {
  lt(e.destination, []);
}, co = (e) => e === void 0 || typeof e == "number" || typeof e == "string" && (e === "balanced" || e === "interactive" || e === "playback"), uo = (e, t, n, r, o, s, a, c) => class extends e {
  constructor(u, d) {
    const l = s(u), g = a(l), w = o(l, d, g), p = g ? t(c) : null;
    super(u, !1, w, p), this._isNodeOfNativeOfflineAudioContext = g, this._nativeAudioDestinationNode = w;
  }
  get channelCount() {
    return this._nativeAudioDestinationNode.channelCount;
  }
  set channelCount(u) {
    if (this._isNodeOfNativeOfflineAudioContext)
      throw r();
    if (u > this._nativeAudioDestinationNode.maxChannelCount)
      throw n();
    this._nativeAudioDestinationNode.channelCount = u;
  }
  get channelCountMode() {
    return this._nativeAudioDestinationNode.channelCountMode;
  }
  set channelCountMode(u) {
    if (this._isNodeOfNativeOfflineAudioContext)
      throw r();
    this._nativeAudioDestinationNode.channelCountMode = u;
  }
  get maxChannelCount() {
    return this._nativeAudioDestinationNode.maxChannelCount;
  }
}, lo = (e) => {
  const t = /* @__PURE__ */ new WeakMap(), n = async (r, o) => {
    const s = o.destination;
    return t.set(o, s), await e(r, o, s), s;
  };
  return {
    render(r, o) {
      const s = t.get(o);
      return s !== void 0 ? Promise.resolve(s) : n(r, o);
    }
  };
}, fo = (e, t, n, r, o, s, a, c) => (i, u) => {
  const d = u.listener, l = () => {
    const E = new Float32Array(1), b = t(u, {
      channelCount: 1,
      channelCountMode: "explicit",
      channelInterpretation: "speakers",
      numberOfInputs: 9
    }), y = a(u);
    let _ = !1, M = [0, 0, -1, 0, 1, 0], S = [0, 0, 0];
    const N = () => {
      if (_)
        return;
      _ = !0;
      const D = r(u, 256, 9, 0);
      D.onaudioprocess = ({ inputBuffer: I }) => {
        const U = [
          s(I, E, 0),
          s(I, E, 1),
          s(I, E, 2),
          s(I, E, 3),
          s(I, E, 4),
          s(I, E, 5)
        ];
        U.some((O, R) => O !== M[R]) && (d.setOrientation(...U), M = U);
        const V = [
          s(I, E, 6),
          s(I, E, 7),
          s(I, E, 8)
        ];
        V.some((O, R) => O !== S[R]) && (d.setPosition(...V), S = V);
      }, b.connect(D);
    }, L = (D) => (I) => {
      I !== M[D] && (M[D] = I, d.setOrientation(...M));
    }, P = (D) => (I) => {
      I !== S[D] && (S[D] = I, d.setPosition(...S));
    }, B = (D, I, U) => {
      const V = n(u, {
        channelCount: 1,
        channelCountMode: "explicit",
        channelInterpretation: "discrete",
        offset: I
      });
      V.connect(b, 0, D), V.start(), Object.defineProperty(V.offset, "defaultValue", {
        get() {
          return I;
        }
      });
      const O = e({ context: i }, y, V.offset, mt, Ge);
      return c(O, "value", (R) => () => R.call(O), (R) => (x) => {
        try {
          R.call(O, x);
        } catch ($) {
          if ($.code !== 9)
            throw $;
        }
        N(), y && U(x);
      }), O.cancelAndHoldAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.cancelAndHoldAtTime), O.cancelScheduledValues = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.cancelScheduledValues), O.exponentialRampToValueAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.exponentialRampToValueAtTime), O.linearRampToValueAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.linearRampToValueAtTime), O.setTargetAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.setTargetAtTime), O.setValueAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.setValueAtTime), O.setValueCurveAtTime = /* @__PURE__ */ ((R) => y ? () => {
        throw o();
      } : (...x) => {
        const $ = R.apply(O, x);
        return N(), $;
      })(O.setValueCurveAtTime), O;
    };
    return {
      forwardX: B(0, 0, L(0)),
      forwardY: B(1, 0, L(1)),
      forwardZ: B(2, -1, L(2)),
      positionX: B(6, 0, P(0)),
      positionY: B(7, 0, P(1)),
      positionZ: B(8, 0, P(2)),
      upX: B(3, 0, L(3)),
      upY: B(4, 1, L(4)),
      upZ: B(5, 0, L(5))
    };
  }, { forwardX: g, forwardY: w, forwardZ: p, positionX: f, positionY: m, positionZ: h, upX: A, upY: v, upZ: T } = d.forwardX === void 0 ? l() : d;
  return {
    get forwardX() {
      return g;
    },
    get forwardY() {
      return w;
    },
    get forwardZ() {
      return p;
    },
    get positionX() {
      return f;
    },
    get positionY() {
      return m;
    },
    get positionZ() {
      return h;
    },
    get upX() {
      return A;
    },
    get upY() {
      return v;
    },
    get upZ() {
      return T;
    }
  };
}, Ue = (e) => "context" in e, Te = (e) => Ue(e[0]), le = (e, t, n, r) => {
  for (const o of e)
    if (n(o)) {
      if (r)
        return !1;
      throw Error("The set contains at least one similar element.");
    }
  return e.add(t), !0;
}, $t = (e, t, [n, r], o) => {
  le(e, [t, n, r], (s) => s[0] === t && s[1] === n, o);
}, qt = (e, [t, n, r], o) => {
  const s = e.get(t);
  s === void 0 ? e.set(t, /* @__PURE__ */ new Set([[n, r]])) : le(s, [n, r], (a) => a[0] === n, o);
}, pn = (e) => "inputs" in e, dt = (e, t, n, r) => {
  if (pn(t)) {
    const o = t.inputs[r];
    return e.connect(o, n, 0), [o, n, 0];
  }
  return e.connect(t, n, r), [t, n, r];
}, mn = (e, t, n) => {
  for (const r of e)
    if (r[0] === t && r[1] === n)
      return e.delete(r), r;
  return null;
}, ho = (e, t, n) => je(e, (r) => r[0] === t && r[1] === n), gn = (e, t) => {
  if (!Ae(e).delete(t))
    throw new Error("Missing the expected event listener.");
}, wn = (e, t, n) => {
  const r = K(e, t), o = je(r, (s) => s[0] === n);
  return r.size === 0 && e.delete(t), o;
}, ft = (e, t, n, r) => {
  pn(t) ? e.disconnect(t.inputs[r], n, 0) : e.disconnect(t, n, r);
}, H = (e) => K(rn, e), Ee = (e) => K(sn, e), ie = (e) => at.has(e), Se = (e) => !ge.has(e), zt = (e, t) => new Promise((n) => {
  if (t !== null)
    n(!0);
  else {
    const r = e.createScriptProcessor(256, 1, 1), o = e.createGain(), s = e.createBuffer(1, 2, 44100), a = s.getChannelData(0);
    a[0] = 1, a[1] = 1;
    const c = e.createBufferSource();
    c.buffer = s, c.loop = !0, c.connect(r).connect(e.destination), c.connect(o), c.disconnect(o), r.onaudioprocess = (i) => {
      const u = i.inputBuffer.getChannelData(0);
      Array.prototype.some.call(u, (d) => d === 1) ? n(!0) : n(!1), c.stop(), r.onaudioprocess = null, c.disconnect(r), r.disconnect(e.destination);
    }, c.start();
  }
}), et = (e, t) => {
  const n = /* @__PURE__ */ new Map();
  for (const r of e)
    for (const o of r) {
      const s = n.get(o);
      n.set(o, s === void 0 ? 1 : s + 1);
    }
  n.forEach((r, o) => t(o, r));
}, De = (e) => "context" in e, po = (e) => {
  const t = /* @__PURE__ */ new Map();
  e.connect = /* @__PURE__ */ ((n) => (r, o = 0, s = 0) => {
    const a = De(r) ? n(r, o, s) : n(r, o), c = t.get(r);
    return c === void 0 ? t.set(r, [{ input: s, output: o }]) : c.every((i) => i.input !== s || i.output !== o) && c.push({ input: s, output: o }), a;
  })(e.connect.bind(e)), e.disconnect = /* @__PURE__ */ ((n) => (r, o, s) => {
    if (n.apply(e), r === void 0)
      t.clear();
    else if (typeof r == "number")
      for (const [a, c] of t) {
        const i = c.filter((u) => u.output !== r);
        i.length === 0 ? t.delete(a) : t.set(a, i);
      }
    else if (t.has(r))
      if (o === void 0)
        t.delete(r);
      else {
        const a = t.get(r);
        if (a !== void 0) {
          const c = a.filter((i) => i.output !== o && (i.input !== s || s === void 0));
          c.length === 0 ? t.delete(r) : t.set(r, c);
        }
      }
    for (const [a, c] of t)
      c.forEach((i) => {
        De(a) ? e.connect(a, i.output, i.input) : e.connect(a, i.output);
      });
  })(e.disconnect);
}, mo = (e, t, n, r) => {
  const { activeInputs: o, passiveInputs: s } = Ce(t), { outputs: a } = z(e), c = Ae(e), i = (u) => {
    const d = H(e), l = Ee(t);
    if (u) {
      const g = wn(s, e, n);
      $t(o, e, g, !1), !r && !ie(e) && d.connect(l, n);
    } else {
      const g = ho(o, e, n);
      qt(s, g, !1), !r && !ie(e) && d.disconnect(l, n);
    }
  };
  return le(a, [t, n], (u) => u[0] === t && u[1] === n, !0) ? (c.add(i), ae(e) ? $t(o, e, [n, i], !0) : qt(s, [e, n, i], !0), !0) : !1;
}, go = (e, t, n, r) => {
  const { activeInputs: o, passiveInputs: s } = z(t), a = mn(o[r], e, n);
  return a === null ? [ln(s, e, n, r)[2], !1] : [a[2], !0];
}, wo = (e, t, n) => {
  const { activeInputs: r, passiveInputs: o } = Ce(t), s = mn(r, e, n);
  return s === null ? [wn(o, e, n)[1], !1] : [s[2], !0];
}, gt = (e, t, n, r, o) => {
  const [s, a] = go(e, n, r, o);
  if (s !== null && (gn(e, s), a && !t && !ie(e) && ft(H(e), H(n), r, o)), ae(n)) {
    const { activeInputs: c } = z(n);
    ut(n, c);
  }
}, wt = (e, t, n, r) => {
  const [o, s] = wo(e, n, r);
  o !== null && (gn(e, o), s && !t && !ie(e) && H(e).disconnect(Ee(n), r));
}, vo = (e, t) => {
  const n = z(e), r = [];
  for (const o of n.outputs)
    Te(o) ? gt(e, t, ...o) : wt(e, t, ...o), r.push(o[0]);
  return n.outputs.clear(), r;
}, _o = (e, t, n) => {
  const r = z(e), o = [];
  for (const s of r.outputs)
    s[1] === n && (Te(s) ? gt(e, t, ...s) : wt(e, t, ...s), o.push(s[0]), r.outputs.delete(s));
  return o;
}, yo = (e, t, n, r, o) => {
  const s = z(e);
  return Array.from(s.outputs).filter((a) => a[0] === n && (r === void 0 || a[1] === r) && (o === void 0 || a[2] === o)).map((a) => (Te(a) ? gt(e, t, ...a) : wt(e, t, ...a), s.outputs.delete(a), a[0]));
}, Eo = (e, t, n, r, o, s, a, c, i, u, d, l, g, w, p, f) => class extends u {
  constructor(h, A, v, T) {
    super(v), this._context = h, this._nativeAudioNode = v;
    const E = d(h);
    l(E) && n(zt, () => zt(E, f)) !== !0 && po(v), rn.set(this, v), cn.set(this, /* @__PURE__ */ new Set()), h.state !== "closed" && A && Be(this), e(this, T, v);
  }
  get channelCount() {
    return this._nativeAudioNode.channelCount;
  }
  set channelCount(h) {
    this._nativeAudioNode.channelCount = h;
  }
  get channelCountMode() {
    return this._nativeAudioNode.channelCountMode;
  }
  set channelCountMode(h) {
    this._nativeAudioNode.channelCountMode = h;
  }
  get channelInterpretation() {
    return this._nativeAudioNode.channelInterpretation;
  }
  set channelInterpretation(h) {
    this._nativeAudioNode.channelInterpretation = h;
  }
  get context() {
    return this._context;
  }
  get numberOfInputs() {
    return this._nativeAudioNode.numberOfInputs;
  }
  get numberOfOutputs() {
    return this._nativeAudioNode.numberOfOutputs;
  }
  // tslint:disable-next-line:invalid-void
  connect(h, A = 0, v = 0) {
    if (A < 0 || A >= this._nativeAudioNode.numberOfOutputs)
      throw o();
    const T = d(this._context), E = p(T);
    if (g(h) || w(h))
      throw s();
    if (Ue(h)) {
      const _ = H(h);
      try {
        const S = dt(this._nativeAudioNode, _, A, v), N = Se(this);
        (E || N) && this._nativeAudioNode.disconnect(...S), this.context.state !== "closed" && !N && Se(h) && Be(h);
      } catch (S) {
        throw S.code === 12 ? s() : S;
      }
      if (t(this, h, A, v, E)) {
        const S = i([this], h);
        et(S, r(E));
      }
      return h;
    }
    const b = Ee(h);
    if (b.name === "playbackRate" && b.maxValue === 1024)
      throw a();
    try {
      this._nativeAudioNode.connect(b, A), (E || Se(this)) && this._nativeAudioNode.disconnect(b, A);
    } catch (_) {
      throw _.code === 12 ? s() : _;
    }
    if (mo(this, h, A, E)) {
      const _ = i([this], h);
      et(_, r(E));
    }
  }
  disconnect(h, A, v) {
    let T;
    const E = d(this._context), b = p(E);
    if (h === void 0)
      T = vo(this, b);
    else if (typeof h == "number") {
      if (h < 0 || h >= this.numberOfOutputs)
        throw o();
      T = _o(this, b, h);
    } else {
      if (A !== void 0 && (A < 0 || A >= this.numberOfOutputs) || Ue(h) && v !== void 0 && (v < 0 || v >= h.numberOfInputs))
        throw o();
      if (T = yo(this, b, h, A, v), T.length === 0)
        throw s();
    }
    for (const y of T) {
      const _ = i([this], y);
      et(_, c);
    }
  }
}, bo = (e, t, n, r, o, s, a, c, i, u, d, l, g) => (w, p, f, m = null, h = null) => {
  const A = f.value, v = new Lr(A), T = p ? r(v) : null, E = {
    get defaultValue() {
      return A;
    },
    get maxValue() {
      return m === null ? f.maxValue : m;
    },
    get minValue() {
      return h === null ? f.minValue : h;
    },
    get value() {
      return f.value;
    },
    set value(b) {
      f.value = b, E.setValueAtTime(b, w.context.currentTime);
    },
    cancelAndHoldAtTime(b) {
      if (typeof f.cancelAndHoldAtTime == "function")
        T === null && v.flush(w.context.currentTime), v.add(o(b)), f.cancelAndHoldAtTime(b);
      else {
        const y = Array.from(v).pop();
        T === null && v.flush(w.context.currentTime), v.add(o(b));
        const _ = Array.from(v).pop();
        f.cancelScheduledValues(b), y !== _ && _ !== void 0 && (_.type === "exponentialRampToValue" ? f.exponentialRampToValueAtTime(_.value, _.endTime) : _.type === "linearRampToValue" ? f.linearRampToValueAtTime(_.value, _.endTime) : _.type === "setValue" ? f.setValueAtTime(_.value, _.startTime) : _.type === "setValueCurve" && f.setValueCurveAtTime(_.values, _.startTime, _.duration));
      }
      return E;
    },
    cancelScheduledValues(b) {
      return T === null && v.flush(w.context.currentTime), v.add(s(b)), f.cancelScheduledValues(b), E;
    },
    exponentialRampToValueAtTime(b, y) {
      if (b === 0)
        throw new RangeError();
      if (!Number.isFinite(y) || y < 0)
        throw new RangeError();
      const _ = w.context.currentTime;
      return T === null && v.flush(_), Array.from(v).length === 0 && (v.add(u(A, _)), f.setValueAtTime(A, _)), v.add(a(b, y)), f.exponentialRampToValueAtTime(b, y), E;
    },
    linearRampToValueAtTime(b, y) {
      const _ = w.context.currentTime;
      return T === null && v.flush(_), Array.from(v).length === 0 && (v.add(u(A, _)), f.setValueAtTime(A, _)), v.add(c(b, y)), f.linearRampToValueAtTime(b, y), E;
    },
    setTargetAtTime(b, y, _) {
      return T === null && v.flush(w.context.currentTime), v.add(i(b, y, _)), f.setTargetAtTime(b, y, _), E;
    },
    setValueAtTime(b, y) {
      return T === null && v.flush(w.context.currentTime), v.add(u(b, y)), f.setValueAtTime(b, y), E;
    },
    setValueCurveAtTime(b, y, _) {
      const M = b instanceof Float32Array ? b : new Float32Array(b);
      if (l !== null && l.name === "webkitAudioContext") {
        const S = y + _, N = w.context.sampleRate, L = Math.ceil(y * N), P = Math.floor(S * N), B = P - L, D = new Float32Array(B);
        for (let U = 0; U < B; U += 1) {
          const V = (M.length - 1) / _ * ((L + U) / N - y), O = Math.floor(V), R = Math.ceil(V);
          D[U] = O === R ? M[O] : (1 - (V - O)) * M[O] + (1 - (R - V)) * M[R];
        }
        T === null && v.flush(w.context.currentTime), v.add(d(D, y, _)), f.setValueCurveAtTime(D, y, _);
        const I = P / N;
        I < S && g(E, D[D.length - 1], I), g(E, M[M.length - 1], S);
      } else
        T === null && v.flush(w.context.currentTime), v.add(d(M, y, _)), f.setValueCurveAtTime(M, y, _);
      return E;
    }
  };
  return n.set(E, f), t.set(E, w), e(E, T), E;
}, Ao = (e) => ({
  replay(t) {
    for (const n of e)
      if (n.type === "exponentialRampToValue") {
        const { endTime: r, value: o } = n;
        t.exponentialRampToValueAtTime(o, r);
      } else if (n.type === "linearRampToValue") {
        const { endTime: r, value: o } = n;
        t.linearRampToValueAtTime(o, r);
      } else if (n.type === "setTarget") {
        const { startTime: r, target: o, timeConstant: s } = n;
        t.setTargetAtTime(o, r, s);
      } else if (n.type === "setValue") {
        const { startTime: r, value: o } = n;
        t.setValueAtTime(o, r);
      } else if (n.type === "setValueCurve") {
        const { duration: r, startTime: o, values: s } = n;
        t.setValueCurveAtTime(s, o, r);
      } else
        throw new Error("Can't apply an unknown automation.");
  }
});
class vn {
  constructor(t) {
    this._map = new Map(t);
  }
  get size() {
    return this._map.size;
  }
  entries() {
    return this._map.entries();
  }
  forEach(t, n = null) {
    return this._map.forEach((r, o) => t.call(n, r, o, this));
  }
  get(t) {
    return this._map.get(t);
  }
  has(t) {
    return this._map.has(t);
  }
  keys() {
    return this._map.keys();
  }
  values() {
    return this._map.values();
  }
}
const Co = {
  channelCount: 2,
  // Bug #61: The channelCountMode should be 'max' according to the spec but is set to 'explicit' to achieve consistent behavior.
  channelCountMode: "explicit",
  channelInterpretation: "speakers",
  numberOfInputs: 1,
  numberOfOutputs: 1,
  parameterData: {},
  processorOptions: {}
}, To = (e, t, n, r, o, s, a, c, i, u, d, l, g, w) => class extends t {
  constructor(f, m, h) {
    var A;
    const v = c(f), T = i(v), E = d({ ...Co, ...h });
    g(E);
    const b = it.get(v), y = b == null ? void 0 : b.get(m), _ = T || v.state !== "closed" ? v : (A = a(v)) !== null && A !== void 0 ? A : v, M = o(_, T ? null : f.baseLatency, u, m, y, E), S = T ? r(m, E, y) : null;
    super(f, !0, M, S);
    const N = [];
    M.parameters.forEach((P, B) => {
      const D = n(this, T, P);
      N.push([B, D]);
    }), this._nativeAudioWorkletNode = M, this._onprocessorerror = null, this._parameters = new vn(N), T && e(v, this);
    const { activeInputs: L } = s(this);
    l(M, L);
  }
  get onprocessorerror() {
    return this._onprocessorerror;
  }
  set onprocessorerror(f) {
    const m = typeof f == "function" ? w(this, f) : null;
    this._nativeAudioWorkletNode.onprocessorerror = m;
    const h = this._nativeAudioWorkletNode.onprocessorerror;
    this._onprocessorerror = h !== null && h === m ? f : h;
  }
  get parameters() {
    return this._parameters === null ? this._nativeAudioWorkletNode.parameters : this._parameters;
  }
  get port() {
    return this._nativeAudioWorkletNode.port;
  }
};
function We(e, t, n, r, o) {
  if (typeof e.copyFromChannel == "function")
    t[n].byteLength === 0 && (t[n] = new Float32Array(128)), e.copyFromChannel(t[n], r, o);
  else {
    const s = e.getChannelData(r);
    if (t[n].byteLength === 0)
      t[n] = s.slice(o, o + 128);
    else {
      const a = new Float32Array(s.buffer, o * Float32Array.BYTES_PER_ELEMENT, 128);
      t[n].set(a);
    }
  }
}
const _n = (e, t, n, r, o) => {
  typeof e.copyToChannel == "function" ? t[n].byteLength !== 0 && e.copyToChannel(t[n], r, o) : t[n].byteLength !== 0 && e.getChannelData(r).set(t[n], o);
}, Ve = (e, t) => {
  const n = [];
  for (let r = 0; r < e; r += 1) {
    const o = [], s = typeof t == "number" ? t : t[r];
    for (let a = 0; a < s; a += 1)
      o.push(new Float32Array(128));
    n.push(o);
  }
  return n;
}, Mo = (e, t) => {
  const n = K(ct, e), r = H(t);
  return K(n, r);
}, No = async (e, t, n, r, o, s, a) => {
  const c = t === null ? Math.ceil(e.context.length / 128) * 128 : t.length, i = r.channelCount * r.numberOfInputs, u = o.reduce((m, h) => m + h, 0), d = u === 0 ? null : n.createBuffer(u, c, n.sampleRate);
  if (s === void 0)
    throw new Error("Missing the processor constructor.");
  const l = z(e), g = await Mo(n, e), w = Ve(r.numberOfInputs, r.channelCount), p = Ve(r.numberOfOutputs, o), f = Array.from(e.parameters.keys()).reduce((m, h) => ({ ...m, [h]: new Float32Array(128) }), {});
  for (let m = 0; m < c; m += 128) {
    if (r.numberOfInputs > 0 && t !== null)
      for (let h = 0; h < r.numberOfInputs; h += 1)
        for (let A = 0; A < r.channelCount; A += 1)
          We(t, w[h], A, A, m);
    s.parameterDescriptors !== void 0 && t !== null && s.parameterDescriptors.forEach(({ name: h }, A) => {
      We(t, f, h, i + A, m);
    });
    for (let h = 0; h < r.numberOfInputs; h += 1)
      for (let A = 0; A < o[h]; A += 1)
        p[h][A].byteLength === 0 && (p[h][A] = new Float32Array(128));
    try {
      const h = w.map((v, T) => l.activeInputs[T].size === 0 ? [] : v), A = a(m / n.sampleRate, n.sampleRate, () => g.process(h, p, f));
      if (d !== null)
        for (let v = 0, T = 0; v < r.numberOfOutputs; v += 1) {
          for (let E = 0; E < o[v]; E += 1)
            _n(d, p[v], E, T + E, m);
          T += o[v];
        }
      if (!A)
        break;
    } catch (h) {
      e.dispatchEvent(new ErrorEvent("processorerror", {
        colno: h.colno,
        filename: h.filename,
        lineno: h.lineno,
        message: h.message
      }));
      break;
    }
  }
  return d;
}, Oo = (e, t, n, r, o, s, a, c, i, u, d, l, g, w, p, f) => (m, h, A) => {
  const v = /* @__PURE__ */ new WeakMap();
  let T = null;
  const E = async (b, y) => {
    let _ = d(b), M = null;
    const S = fn(_, y), N = Array.isArray(h.outputChannelCount) ? h.outputChannelCount : Array.from(h.outputChannelCount);
    if (l === null) {
      const L = N.reduce((I, U) => I + U, 0), P = o(y, {
        channelCount: Math.max(1, L),
        channelCountMode: "explicit",
        channelInterpretation: "discrete",
        numberOfOutputs: Math.max(1, L)
      }), B = [];
      for (let I = 0; I < b.numberOfOutputs; I += 1)
        B.push(r(y, {
          channelCount: 1,
          channelCountMode: "explicit",
          channelInterpretation: "speakers",
          numberOfInputs: N[I]
        }));
      const D = a(y, {
        channelCount: h.channelCount,
        channelCountMode: h.channelCountMode,
        channelInterpretation: h.channelInterpretation,
        gain: 1
      });
      D.connect = t.bind(null, B), D.disconnect = i.bind(null, B), M = [P, B, D];
    } else
      S || (_ = new l(y, m));
    if (v.set(y, M === null ? _ : M[2]), M !== null) {
      if (T === null) {
        if (A === void 0)
          throw new Error("Missing the processor constructor.");
        if (g === null)
          throw new Error("Missing the native OfflineAudioContext constructor.");
        const U = b.channelCount * b.numberOfInputs, V = A.parameterDescriptors === void 0 ? 0 : A.parameterDescriptors.length, O = U + V;
        T = No(b, O === 0 ? null : await (async () => {
          const x = new g(
            O,
            // Ceil the length to the next full render quantum.
            // Bug #17: Safari does not yet expose the length.
            Math.ceil(b.context.length / 128) * 128,
            y.sampleRate
          ), $ = [], fe = [];
          for (let j = 0; j < h.numberOfInputs; j += 1)
            $.push(a(x, {
              channelCount: h.channelCount,
              channelCountMode: h.channelCountMode,
              channelInterpretation: h.channelInterpretation,
              gain: 1
            })), fe.push(o(x, {
              channelCount: h.channelCount,
              channelCountMode: "explicit",
              channelInterpretation: "discrete",
              numberOfOutputs: h.channelCount
            }));
          const he = await Promise.all(Array.from(b.parameters.values()).map(async (j) => {
            const X = s(x, {
              channelCount: 1,
              channelCountMode: "explicit",
              channelInterpretation: "discrete",
              offset: j.value
            });
            return await w(x, j, X.offset), X;
          })), pe = r(x, {
            channelCount: 1,
            channelCountMode: "explicit",
            channelInterpretation: "speakers",
            numberOfInputs: Math.max(1, U + V)
          });
          for (let j = 0; j < h.numberOfInputs; j += 1) {
            $[j].connect(fe[j]);
            for (let X = 0; X < h.channelCount; X += 1)
              fe[j].connect(pe, X, j * h.channelCount + X);
          }
          for (const [j, X] of he.entries())
            X.connect(pe, 0, U + j), X.start(0);
          return pe.connect(x.destination), await Promise.all($.map((j) => p(b, x, j))), f(x);
        })(), y, h, N, A, u);
      }
      const L = await T, P = n(y, {
        buffer: null,
        channelCount: 2,
        channelCountMode: "max",
        channelInterpretation: "speakers",
        loop: !1,
        loopEnd: 0,
        loopStart: 0,
        playbackRate: 1
      }), [B, D, I] = M;
      L !== null && (P.buffer = L, P.start(0)), P.connect(B);
      for (let U = 0, V = 0; U < b.numberOfOutputs; U += 1) {
        const O = D[U];
        for (let R = 0; R < N[U]; R += 1)
          B.connect(O, V + R, R);
        V += N[U];
      }
      return I;
    }
    if (S)
      for (const [L, P] of b.parameters.entries())
        await e(
          y,
          P,
          // @todo The definition that TypeScript uses of the AudioParamMap is lacking many methods.
          _.parameters.get(L)
        );
    else
      for (const [L, P] of b.parameters.entries())
        await w(
          y,
          P,
          // @todo The definition that TypeScript uses of the AudioParamMap is lacking many methods.
          _.parameters.get(L)
        );
    return await p(b, y, _), _;
  };
  return {
    render(b, y) {
      c(y, b);
      const _ = v.get(y);
      return _ !== void 0 ? Promise.resolve(_) : E(b, y);
    }
  };
}, ko = (e, t) => (n, r) => {
  const o = t.get(n);
  if (o !== void 0)
    return o;
  const s = e.get(n);
  if (s !== void 0)
    return s;
  try {
    const a = r();
    return a instanceof Promise ? (e.set(n, a), a.catch(() => !1).then((c) => (e.delete(n), t.set(n, c), c))) : (t.set(n, a), a);
  } catch {
    return t.set(n, !1), !1;
  }
}, Io = (e) => (t, n, r) => e(n, t, r), So = (e) => (t, n, r = 0, o = 0) => {
  const s = t[r];
  if (s === void 0)
    throw e();
  return De(n) ? s.connect(n, 0, o) : s.connect(n, 0);
}, Ro = (e) => (t) => (e[0] = t, e[0]), Lo = (e, t, n, r, o, s, a, c) => (i, u) => {
  const d = t.get(i);
  if (d === void 0)
    throw new Error("Missing the expected cycle count.");
  const l = s(i.context), g = c(l);
  if (d === u) {
    if (t.delete(i), !g && a(i)) {
      const w = r(i), { outputs: p } = n(i);
      for (const f of p)
        if (Te(f)) {
          const m = r(f[0]);
          e(w, m, f[1], f[2]);
        } else {
          const m = o(f[0]);
          w.connect(m, f[1]);
        }
    }
  } else
    t.set(i, d - u);
}, Po = (e) => (t, n, r, o) => e(t[o], (s) => s[0] === n && s[1] === r), Bo = (e) => (t, n) => {
  e(t).delete(n);
}, Uo = (e) => "delayTime" in e, Do = (e, t, n) => function r(o, s) {
  const a = Ue(s) ? s : n(e, s);
  if (Uo(a))
    return [];
  if (o[0] === a)
    return [o];
  if (o.includes(a))
    return [];
  const { outputs: c } = t(a);
  return Array.from(c).map((i) => r([...o, a], i[0])).reduce((i, u) => i.concat(u), []);
}, Ie = (e, t, n) => {
  const r = t[n];
  if (r === void 0)
    throw e();
  return r;
}, Wo = (e) => (t, n = void 0, r = void 0, o = 0) => n === void 0 ? t.forEach((s) => s.disconnect()) : typeof n == "number" ? Ie(e, t, n).disconnect() : De(n) ? r === void 0 ? t.forEach((s) => s.disconnect(n)) : o === void 0 ? Ie(e, t, r).disconnect(n, 0) : Ie(e, t, r).disconnect(n, 0, o) : r === void 0 ? t.forEach((s) => s.disconnect(n)) : Ie(e, t, r).disconnect(n, 0), Vo = (e) => (t) => new Promise((n, r) => {
  if (e === null) {
    r(new SyntaxError());
    return;
  }
  const o = e.document.head;
  if (o === null)
    r(new SyntaxError());
  else {
    const s = e.document.createElement("script"), a = new Blob([t], { type: "application/javascript" }), c = URL.createObjectURL(a), i = e.onerror, u = () => {
      e.onerror = i, URL.revokeObjectURL(c);
    };
    e.onerror = (d, l, g, w, p) => {
      if (l === c || l === e.location.href && g === 1 && w === 1)
        return u(), r(p), !1;
      if (i !== null)
        return i(d, l, g, w, p);
    }, s.onerror = () => {
      u(), r(new SyntaxError());
    }, s.onload = () => {
      u(), n();
    }, s.src = c, s.type = "module", o.appendChild(s);
  }
}), xo = (e) => class {
  constructor(n) {
    this._nativeEventTarget = n, this._listeners = /* @__PURE__ */ new WeakMap();
  }
  addEventListener(n, r, o) {
    if (r !== null) {
      let s = this._listeners.get(r);
      s === void 0 && (s = e(this, r), typeof r == "function" && this._listeners.set(r, s)), this._nativeEventTarget.addEventListener(n, s, o);
    }
  }
  dispatchEvent(n) {
    return this._nativeEventTarget.dispatchEvent(n);
  }
  removeEventListener(n, r, o) {
    const s = r === null ? void 0 : this._listeners.get(r);
    this._nativeEventTarget.removeEventListener(n, s === void 0 ? null : s, o);
  }
}, Fo = (e) => (t, n, r) => {
  Object.defineProperties(e, {
    currentFrame: {
      configurable: !0,
      get() {
        return Math.round(t * n);
      }
    },
    currentTime: {
      configurable: !0,
      get() {
        return t;
      }
    }
  });
  try {
    return r();
  } finally {
    e !== null && (delete e.currentFrame, delete e.currentTime);
  }
}, jo = (e) => async (t) => {
  try {
    const n = await fetch(t);
    if (n.ok)
      return [await n.text(), n.url];
  } catch {
  }
  throw e();
}, Go = (e, t) => (n) => t(e, n), $o = (e) => (t) => {
  const n = e(t);
  if (n.renderer === null)
    throw new Error("Missing the renderer of the given AudioNode in the audio graph.");
  return n.renderer;
}, qo = (e) => (t) => {
  var n;
  return (n = e.get(t)) !== null && n !== void 0 ? n : 0;
}, zo = (e) => (t) => {
  const n = e(t);
  if (n.renderer === null)
    throw new Error("Missing the renderer of the given AudioParam in the audio graph.");
  return n.renderer;
}, Xo = (e) => (t) => e.get(t), Z = () => new DOMException("", "InvalidStateError"), Yo = (e) => (t) => {
  const n = e.get(t);
  if (n === void 0)
    throw Z();
  return n;
}, Ho = (e, t) => (n) => {
  let r = e.get(n);
  if (r !== void 0)
    return r;
  if (t === null)
    throw new Error("Missing the native OfflineAudioContext constructor.");
  return r = new t(1, 1, 44100), e.set(n, r), r;
}, Zo = (e) => (t) => {
  const n = e.get(t);
  if (n === void 0)
    throw new Error("The context has no set of AudioWorkletNodes.");
  return n;
}, Ko = () => new DOMException("", "InvalidAccessError"), Qo = (e, t, n, r, o, s) => (a) => (c, i) => {
  const u = e.get(c);
  if (u === void 0) {
    if (!a && s(c)) {
      const d = r(c), { outputs: l } = n(c);
      for (const g of l)
        if (Te(g)) {
          const w = r(g[0]);
          t(d, w, g[1], g[2]);
        } else {
          const w = o(g[0]);
          d.disconnect(w, g[1]);
        }
    }
    e.set(c, i);
  } else
    e.set(c, u + i);
}, Jo = (e) => (t) => e !== null && t instanceof e, es = (e) => (t) => e !== null && typeof e.AudioNode == "function" && t instanceof e.AudioNode, ts = (e) => (t) => e !== null && typeof e.AudioParam == "function" && t instanceof e.AudioParam, ns = (e) => (t) => e !== null && t instanceof e, rs = (e) => e !== null && e.isSecureContext, os = (e, t, n, r) => class extends e {
  constructor(s, a) {
    const c = n(s), i = t(c, a);
    if (r(c))
      throw new TypeError();
    super(s, !0, i, null), this._nativeMediaStreamAudioSourceNode = i;
  }
  get mediaStream() {
    return this._nativeMediaStreamAudioSourceNode.mediaStream;
  }
}, ss = (e, t, n, r, o) => class extends r {
  constructor(a = {}) {
    if (o === null)
      throw new Error("Missing the native AudioContext constructor.");
    let c;
    try {
      c = new o(a);
    } catch (d) {
      throw d.code === 12 && d.message === "sampleRate is not in range" ? t() : d;
    }
    if (c === null)
      throw n();
    if (!co(a.latencyHint))
      throw new TypeError(`The provided value '${a.latencyHint}' is not a valid enum value of type AudioContextLatencyCategory.`);
    if (a.sampleRate !== void 0 && c.sampleRate !== a.sampleRate)
      throw t();
    super(c, 2);
    const { latencyHint: i } = a, { sampleRate: u } = c;
    if (this._baseLatency = typeof c.baseLatency == "number" ? c.baseLatency : i === "balanced" ? 512 / u : i === "interactive" || i === void 0 ? 256 / u : i === "playback" ? 1024 / u : (
      /*
       * @todo The min (256) and max (16384) values are taken from the allowed bufferSize values of a
       * ScriptProcessorNode.
       */
      Math.max(2, Math.min(128, Math.round(i * u / 128))) * 128 / u
    ), this._nativeAudioContext = c, o.name === "webkitAudioContext" ? (this._nativeGainNode = c.createGain(), this._nativeOscillatorNode = c.createOscillator(), this._nativeGainNode.gain.value = 1e-37, this._nativeOscillatorNode.connect(this._nativeGainNode).connect(c.destination), this._nativeOscillatorNode.start()) : (this._nativeGainNode = null, this._nativeOscillatorNode = null), this._state = null, c.state === "running") {
      this._state = "suspended";
      const d = () => {
        this._state === "suspended" && (this._state = null), c.removeEventListener("statechange", d);
      };
      c.addEventListener("statechange", d);
    }
  }
  get baseLatency() {
    return this._baseLatency;
  }
  get state() {
    return this._state !== null ? this._state : this._nativeAudioContext.state;
  }
  close() {
    return this.state === "closed" ? this._nativeAudioContext.close().then(() => {
      throw e();
    }) : (this._state === "suspended" && (this._state = null), this._nativeAudioContext.close().then(() => {
      this._nativeGainNode !== null && this._nativeOscillatorNode !== null && (this._nativeOscillatorNode.stop(), this._nativeGainNode.disconnect(), this._nativeOscillatorNode.disconnect()), io(this);
    }));
  }
  resume() {
    return this._state === "suspended" ? new Promise((a, c) => {
      const i = () => {
        this._nativeAudioContext.removeEventListener("statechange", i), this._nativeAudioContext.state === "running" ? a() : this.resume().then(a, c);
      };
      this._nativeAudioContext.addEventListener("statechange", i);
    }) : this._nativeAudioContext.resume().catch((a) => {
      throw a === void 0 || a.code === 15 ? e() : a;
    });
  }
  suspend() {
    return this._nativeAudioContext.suspend().catch((a) => {
      throw a === void 0 ? e() : a;
    });
  }
}, as = (e, t, n, r, o, s) => class extends n {
  constructor(c, i) {
    super(c), this._nativeContext = c, an.set(this, c), r(c) && o.set(c, /* @__PURE__ */ new Set()), this._destination = new e(this, i), this._listener = t(this, c), this._onstatechange = null;
  }
  get currentTime() {
    return this._nativeContext.currentTime;
  }
  get destination() {
    return this._destination;
  }
  get listener() {
    return this._listener;
  }
  get onstatechange() {
    return this._onstatechange;
  }
  set onstatechange(c) {
    const i = typeof c == "function" ? s(this, c) : null;
    this._nativeContext.onstatechange = i;
    const u = this._nativeContext.onstatechange;
    this._onstatechange = u !== null && u === i ? c : u;
  }
  get sampleRate() {
    return this._nativeContext.sampleRate;
  }
  get state() {
    return this._nativeContext.state;
  }
}, Xt = (e) => {
  const t = new Uint32Array([1179011410, 40, 1163280727, 544501094, 16, 131073, 44100, 176400, 1048580, 1635017060, 4, 0]);
  try {
    const n = e.decodeAudioData(t.buffer, () => {
    });
    return n === void 0 ? !1 : (n.catch(() => {
    }), !0);
  } catch {
  }
  return !1;
}, is = (e, t) => (n, r, o) => {
  const s = /* @__PURE__ */ new Set();
  return n.connect = /* @__PURE__ */ ((a) => (c, i = 0, u = 0) => {
    const d = s.size === 0;
    if (t(c))
      return a.call(n, c, i, u), e(s, [c, i, u], (l) => l[0] === c && l[1] === i && l[2] === u, !0), d && r(), c;
    a.call(n, c, i), e(s, [c, i], (l) => l[0] === c && l[1] === i, !0), d && r();
  })(n.connect), n.disconnect = /* @__PURE__ */ ((a) => (c, i, u) => {
    const d = s.size > 0;
    if (c === void 0)
      a.apply(n), s.clear();
    else if (typeof c == "number") {
      a.call(n, c);
      for (const g of s)
        g[1] === c && s.delete(g);
    } else {
      t(c) ? a.call(n, c, i, u) : a.call(n, c, i);
      for (const g of s)
        g[0] === c && (i === void 0 || g[1] === i) && (u === void 0 || g[2] === u) && s.delete(g);
    }
    const l = s.size === 0;
    d && l && o();
  })(n.disconnect), n;
}, se = (e, t, n) => {
  const r = t[n];
  r !== void 0 && r !== e[n] && (e[n] = r);
}, Me = (e, t) => {
  se(e, t, "channelCount"), se(e, t, "channelCountMode"), se(e, t, "channelInterpretation");
}, cs = (e) => e === null ? null : e.hasOwnProperty("AudioBuffer") ? e.AudioBuffer : null, vt = (e, t, n) => {
  const r = t[n];
  r !== void 0 && r !== e[n].value && (e[n].value = r);
}, us = (e) => {
  e.start = /* @__PURE__ */ ((t) => {
    let n = !1;
    return (r = 0, o = 0, s) => {
      if (n)
        throw Z();
      t.call(e, r, o, s), n = !0;
    };
  })(e.start);
}, yn = (e) => {
  e.start = /* @__PURE__ */ ((t) => (n = 0, r = 0, o) => {
    if (typeof o == "number" && o < 0 || r < 0 || n < 0)
      throw new RangeError("The parameters can't be negative.");
    t.call(e, n, r, o);
  })(e.start);
}, En = (e) => {
  e.stop = /* @__PURE__ */ ((t) => (n = 0) => {
    if (n < 0)
      throw new RangeError("The parameter can't be negative.");
    t.call(e, n);
  })(e.stop);
}, ls = (e, t, n, r, o, s, a, c, i, u, d) => (l, g) => {
  const w = l.createBufferSource();
  return Me(w, g), vt(w, g, "playbackRate"), se(w, g, "buffer"), se(w, g, "loop"), se(w, g, "loopEnd"), se(w, g, "loopStart"), t(n, () => n(l)) || us(w), t(r, () => r(l)) || i(w), t(o, () => o(l)) || u(w, l), t(s, () => s(l)) || yn(w), t(a, () => a(l)) || d(w, l), t(c, () => c(l)) || En(w), e(l, w), w;
}, ds = (e) => e === null ? null : e.hasOwnProperty("AudioContext") ? e.AudioContext : e.hasOwnProperty("webkitAudioContext") ? e.webkitAudioContext : null, fs = (e, t) => (n, r, o) => {
  const s = n.destination;
  if (s.channelCount !== r)
    try {
      s.channelCount = r;
    } catch {
    }
  o && s.channelCountMode !== "explicit" && (s.channelCountMode = "explicit"), s.maxChannelCount === 0 && Object.defineProperty(s, "maxChannelCount", {
    value: r
  });
  const a = e(n, {
    channelCount: r,
    channelCountMode: s.channelCountMode,
    channelInterpretation: s.channelInterpretation,
    gain: 1
  });
  return t(a, "channelCount", (c) => () => c.call(a), (c) => (i) => {
    c.call(a, i);
    try {
      s.channelCount = i;
    } catch (u) {
      if (i > s.maxChannelCount)
        throw u;
    }
  }), t(a, "channelCountMode", (c) => () => c.call(a), (c) => (i) => {
    c.call(a, i), s.channelCountMode = i;
  }), t(a, "channelInterpretation", (c) => () => c.call(a), (c) => (i) => {
    c.call(a, i), s.channelInterpretation = i;
  }), Object.defineProperty(a, "maxChannelCount", {
    get: () => s.maxChannelCount
  }), a.connect(s), a;
}, hs = (e) => e === null ? null : e.hasOwnProperty("AudioWorkletNode") ? e.AudioWorkletNode : null, ps = (e) => {
  const { port1: t } = new MessageChannel();
  try {
    t.postMessage(e);
  } finally {
    t.close();
  }
}, ms = (e, t, n, r, o) => (s, a, c, i, u, d) => {
  if (c !== null)
    try {
      const l = new c(s, i, d), g = /* @__PURE__ */ new Map();
      let w = null;
      if (Object.defineProperties(l, {
        /*
         * Bug #61: Overwriting the property accessors for channelCount and channelCountMode is necessary as long as some
         * browsers have no native implementation to achieve a consistent behavior.
         */
        channelCount: {
          get: () => d.channelCount,
          set: () => {
            throw e();
          }
        },
        channelCountMode: {
          get: () => "explicit",
          set: () => {
            throw e();
          }
        },
        // Bug #156: Chrome and Edge do not yet fire an ErrorEvent.
        onprocessorerror: {
          get: () => w,
          set: (p) => {
            typeof w == "function" && l.removeEventListener("processorerror", w), w = typeof p == "function" ? p : null, typeof w == "function" && l.addEventListener("processorerror", w);
          }
        }
      }), l.addEventListener = /* @__PURE__ */ ((p) => (...f) => {
        if (f[0] === "processorerror") {
          const m = typeof f[1] == "function" ? f[1] : typeof f[1] == "object" && f[1] !== null && typeof f[1].handleEvent == "function" ? f[1].handleEvent : null;
          if (m !== null) {
            const h = g.get(f[1]);
            h !== void 0 ? f[1] = h : (f[1] = (A) => {
              A.type === "error" ? (Object.defineProperties(A, {
                type: { value: "processorerror" }
              }), m(A)) : m(new ErrorEvent(f[0], { ...A }));
            }, g.set(m, f[1]));
          }
        }
        return p.call(l, "error", f[1], f[2]), p.call(l, ...f);
      })(l.addEventListener), l.removeEventListener = /* @__PURE__ */ ((p) => (...f) => {
        if (f[0] === "processorerror") {
          const m = g.get(f[1]);
          m !== void 0 && (g.delete(f[1]), f[1] = m);
        }
        return p.call(l, "error", f[1], f[2]), p.call(l, f[0], f[1], f[2]);
      })(l.removeEventListener), d.numberOfOutputs !== 0) {
        const p = n(s, {
          channelCount: 1,
          channelCountMode: "explicit",
          channelInterpretation: "discrete",
          gain: 0
        });
        return l.connect(p).connect(s.destination), o(l, () => p.disconnect(), () => p.connect(s.destination));
      }
      return l;
    } catch (l) {
      throw l.code === 11 ? r() : l;
    }
  if (u === void 0)
    throw r();
  return ps(d), t(s, a, u, d);
}, gs = (e, t) => e === null ? 512 : Math.max(512, Math.min(16384, Math.pow(2, Math.round(Math.log2(e * t))))), ws = (e) => new Promise((t, n) => {
  const { port1: r, port2: o } = new MessageChannel();
  r.onmessage = ({ data: s }) => {
    r.close(), o.close(), t(s);
  }, r.onmessageerror = ({ data: s }) => {
    r.close(), o.close(), n(s);
  }, o.postMessage(e);
}), vs = async (e, t) => {
  const n = await ws(t);
  return new e(n);
}, _s = (e, t, n, r) => {
  let o = ct.get(e);
  o === void 0 && (o = /* @__PURE__ */ new WeakMap(), ct.set(e, o));
  const s = vs(n, r);
  return o.set(t, s), s;
}, ys = (e, t, n, r, o, s, a, c, i, u, d, l, g) => (w, p, f, m) => {
  if (m.numberOfInputs === 0 && m.numberOfOutputs === 0)
    throw i();
  const h = Array.isArray(m.outputChannelCount) ? m.outputChannelCount : Array.from(m.outputChannelCount);
  if (h.some((C) => C < 1))
    throw i();
  if (h.length !== m.numberOfOutputs)
    throw t();
  if (m.channelCountMode !== "explicit")
    throw i();
  const A = m.channelCount * m.numberOfInputs, v = h.reduce((C, k) => C + k, 0), T = f.parameterDescriptors === void 0 ? 0 : f.parameterDescriptors.length;
  if (A + T > 6 || v > 6)
    throw i();
  const E = new MessageChannel(), b = [], y = [];
  for (let C = 0; C < m.numberOfInputs; C += 1)
    b.push(a(w, {
      channelCount: m.channelCount,
      channelCountMode: m.channelCountMode,
      channelInterpretation: m.channelInterpretation,
      gain: 1
    })), y.push(o(w, {
      channelCount: m.channelCount,
      channelCountMode: "explicit",
      channelInterpretation: "discrete",
      numberOfOutputs: m.channelCount
    }));
  const _ = [];
  if (f.parameterDescriptors !== void 0)
    for (const { defaultValue: C, maxValue: k, minValue: q, name: F } of f.parameterDescriptors) {
      const W = s(w, {
        channelCount: 1,
        channelCountMode: "explicit",
        channelInterpretation: "discrete",
        offset: m.parameterData[F] !== void 0 ? m.parameterData[F] : C === void 0 ? 0 : C
      });
      Object.defineProperties(W.offset, {
        defaultValue: {
          get: () => C === void 0 ? 0 : C
        },
        maxValue: {
          get: () => k === void 0 ? mt : k
        },
        minValue: {
          get: () => q === void 0 ? Ge : q
        }
      }), _.push(W);
    }
  const M = r(w, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "speakers",
    numberOfInputs: Math.max(1, A + T)
  }), S = gs(p, w.sampleRate), N = c(
    w,
    S,
    A + T,
    // Bug #87: Only Firefox will fire an AudioProcessingEvent if there is no connected output.
    Math.max(1, v)
  ), L = o(w, {
    channelCount: Math.max(1, v),
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    numberOfOutputs: Math.max(1, v)
  }), P = [];
  for (let C = 0; C < m.numberOfOutputs; C += 1)
    P.push(r(w, {
      channelCount: 1,
      channelCountMode: "explicit",
      channelInterpretation: "speakers",
      numberOfInputs: h[C]
    }));
  for (let C = 0; C < m.numberOfInputs; C += 1) {
    b[C].connect(y[C]);
    for (let k = 0; k < m.channelCount; k += 1)
      y[C].connect(M, k, C * m.channelCount + k);
  }
  const B = new vn(f.parameterDescriptors === void 0 ? [] : f.parameterDescriptors.map(({ name: C }, k) => {
    const q = _[k];
    return q.connect(M, 0, A + k), q.start(0), [C, q.offset];
  }));
  M.connect(N);
  let D = m.channelInterpretation, I = null;
  const U = m.numberOfOutputs === 0 ? [N] : P, V = {
    get bufferSize() {
      return S;
    },
    get channelCount() {
      return m.channelCount;
    },
    set channelCount(C) {
      throw n();
    },
    get channelCountMode() {
      return m.channelCountMode;
    },
    set channelCountMode(C) {
      throw n();
    },
    get channelInterpretation() {
      return D;
    },
    set channelInterpretation(C) {
      for (const k of b)
        k.channelInterpretation = C;
      D = C;
    },
    get context() {
      return N.context;
    },
    get inputs() {
      return b;
    },
    get numberOfInputs() {
      return m.numberOfInputs;
    },
    get numberOfOutputs() {
      return m.numberOfOutputs;
    },
    get onprocessorerror() {
      return I;
    },
    set onprocessorerror(C) {
      typeof I == "function" && V.removeEventListener("processorerror", I), I = typeof C == "function" ? C : null, typeof I == "function" && V.addEventListener("processorerror", I);
    },
    get parameters() {
      return B;
    },
    get port() {
      return E.port2;
    },
    addEventListener(...C) {
      return N.addEventListener(C[0], C[1], C[2]);
    },
    connect: e.bind(null, U),
    disconnect: u.bind(null, U),
    dispatchEvent(...C) {
      return N.dispatchEvent(C[0]);
    },
    removeEventListener(...C) {
      return N.removeEventListener(C[0], C[1], C[2]);
    }
  }, O = /* @__PURE__ */ new Map();
  E.port1.addEventListener = /* @__PURE__ */ ((C) => (...k) => {
    if (k[0] === "message") {
      const q = typeof k[1] == "function" ? k[1] : typeof k[1] == "object" && k[1] !== null && typeof k[1].handleEvent == "function" ? k[1].handleEvent : null;
      if (q !== null) {
        const F = O.get(k[1]);
        F !== void 0 ? k[1] = F : (k[1] = (W) => {
          d(w.currentTime, w.sampleRate, () => q(W));
        }, O.set(q, k[1]));
      }
    }
    return C.call(E.port1, k[0], k[1], k[2]);
  })(E.port1.addEventListener), E.port1.removeEventListener = /* @__PURE__ */ ((C) => (...k) => {
    if (k[0] === "message") {
      const q = O.get(k[1]);
      q !== void 0 && (O.delete(k[1]), k[1] = q);
    }
    return C.call(E.port1, k[0], k[1], k[2]);
  })(E.port1.removeEventListener);
  let R = null;
  Object.defineProperty(E.port1, "onmessage", {
    get: () => R,
    set: (C) => {
      typeof R == "function" && E.port1.removeEventListener("message", R), R = typeof C == "function" ? C : null, typeof R == "function" && (E.port1.addEventListener("message", R), E.port1.start());
    }
  }), f.prototype.port = E.port1;
  let x = null;
  _s(w, V, f, m).then((C) => x = C);
  const fe = Ve(m.numberOfInputs, m.channelCount), he = Ve(m.numberOfOutputs, h), pe = f.parameterDescriptors === void 0 ? [] : f.parameterDescriptors.reduce((C, { name: k }) => ({ ...C, [k]: new Float32Array(128) }), {});
  let j = !0;
  const X = () => {
    m.numberOfOutputs > 0 && N.disconnect(L);
    for (let C = 0, k = 0; C < m.numberOfOutputs; C += 1) {
      const q = P[C];
      for (let F = 0; F < h[C]; F += 1)
        L.disconnect(q, k + F, F);
      k += h[C];
    }
  }, Ne = /* @__PURE__ */ new Map();
  N.onaudioprocess = ({ inputBuffer: C, outputBuffer: k }) => {
    if (x !== null) {
      const q = l(V);
      for (let F = 0; F < S; F += 128) {
        for (let W = 0; W < m.numberOfInputs; W += 1)
          for (let G = 0; G < m.channelCount; G += 1)
            We(C, fe[W], G, G, F);
        f.parameterDescriptors !== void 0 && f.parameterDescriptors.forEach(({ name: W }, G) => {
          We(C, pe, W, A + G, F);
        });
        for (let W = 0; W < m.numberOfInputs; W += 1)
          for (let G = 0; G < h[W]; G += 1)
            he[W][G].byteLength === 0 && (he[W][G] = new Float32Array(128));
        try {
          const W = fe.map((Y, te) => {
            if (q[te].size > 0)
              return Ne.set(te, S / 128), Y;
            const Qe = Ne.get(te);
            return Qe === void 0 ? [] : (Y.every((Yn) => Yn.every((Hn) => Hn === 0)) && (Qe === 1 ? Ne.delete(te) : Ne.set(te, Qe - 1)), Y);
          });
          j = d(w.currentTime + F / w.sampleRate, w.sampleRate, () => x.process(W, he, pe));
          for (let Y = 0, te = 0; Y < m.numberOfOutputs; Y += 1) {
            for (let _e = 0; _e < h[Y]; _e += 1)
              _n(k, he[Y], _e, te + _e, F);
            te += h[Y];
          }
        } catch (W) {
          j = !1, V.dispatchEvent(new ErrorEvent("processorerror", {
            colno: W.colno,
            filename: W.filename,
            lineno: W.lineno,
            message: W.message
          }));
        }
        if (!j) {
          for (let W = 0; W < m.numberOfInputs; W += 1) {
            b[W].disconnect(y[W]);
            for (let G = 0; G < m.channelCount; G += 1)
              y[F].disconnect(M, G, W * m.channelCount + G);
          }
          if (f.parameterDescriptors !== void 0) {
            const W = f.parameterDescriptors.length;
            for (let G = 0; G < W; G += 1) {
              const Y = _[G];
              Y.disconnect(M, 0, A + G), Y.stop();
            }
          }
          M.disconnect(N), N.onaudioprocess = null, Ze ? X() : kt();
          break;
        }
      }
    }
  };
  let Ze = !1;
  const Ke = a(w, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    gain: 0
  }), Ot = () => N.connect(Ke).connect(w.destination), kt = () => {
    N.disconnect(Ke), Ke.disconnect();
  }, zn = () => {
    if (j) {
      kt(), m.numberOfOutputs > 0 && N.connect(L);
      for (let C = 0, k = 0; C < m.numberOfOutputs; C += 1) {
        const q = P[C];
        for (let F = 0; F < h[C]; F += 1)
          L.connect(q, k + F, F);
        k += h[C];
      }
    }
    Ze = !0;
  }, Xn = () => {
    j && (Ot(), X()), Ze = !1;
  };
  return Ot(), g(V, zn, Xn);
}, Es = (e, t) => (n, r) => {
  const o = n.createChannelMerger(r.numberOfInputs);
  return e !== null && e.name === "webkitAudioContext" && t(n, o), Me(o, r), o;
}, bs = (e) => {
  const t = e.numberOfOutputs;
  Object.defineProperty(e, "channelCount", {
    get: () => t,
    set: (n) => {
      if (n !== t)
        throw Z();
    }
  }), Object.defineProperty(e, "channelCountMode", {
    get: () => "explicit",
    set: (n) => {
      if (n !== "explicit")
        throw Z();
    }
  }), Object.defineProperty(e, "channelInterpretation", {
    get: () => "discrete",
    set: (n) => {
      if (n !== "discrete")
        throw Z();
    }
  });
}, bn = (e, t) => {
  const n = e.createChannelSplitter(t.numberOfOutputs);
  return Me(n, t), bs(n), n;
}, As = (e, t, n, r, o) => (s, a) => {
  if (s.createConstantSource === void 0)
    return n(s, a);
  const c = s.createConstantSource();
  return Me(c, a), vt(c, a, "offset"), t(r, () => r(s)) || yn(c), t(o, () => o(s)) || En(c), e(s, c), c;
}, An = (e, t) => (e.connect = t.connect.bind(t), e.disconnect = t.disconnect.bind(t), e), Cs = (e, t, n, r) => (o, { offset: s, ...a }) => {
  const c = o.createBuffer(1, 2, 44100), i = t(o, {
    buffer: null,
    channelCount: 2,
    channelCountMode: "max",
    channelInterpretation: "speakers",
    loop: !1,
    loopEnd: 0,
    loopStart: 0,
    playbackRate: 1
  }), u = n(o, { ...a, gain: s }), d = c.getChannelData(0);
  d[0] = 1, d[1] = 1, i.buffer = c, i.loop = !0;
  const l = {
    get bufferSize() {
    },
    get channelCount() {
      return u.channelCount;
    },
    set channelCount(p) {
      u.channelCount = p;
    },
    get channelCountMode() {
      return u.channelCountMode;
    },
    set channelCountMode(p) {
      u.channelCountMode = p;
    },
    get channelInterpretation() {
      return u.channelInterpretation;
    },
    set channelInterpretation(p) {
      u.channelInterpretation = p;
    },
    get context() {
      return u.context;
    },
    get inputs() {
      return [];
    },
    get numberOfInputs() {
      return i.numberOfInputs;
    },
    get numberOfOutputs() {
      return u.numberOfOutputs;
    },
    get offset() {
      return u.gain;
    },
    get onended() {
      return i.onended;
    },
    set onended(p) {
      i.onended = p;
    },
    addEventListener(...p) {
      return i.addEventListener(p[0], p[1], p[2]);
    },
    dispatchEvent(...p) {
      return i.dispatchEvent(p[0]);
    },
    removeEventListener(...p) {
      return i.removeEventListener(p[0], p[1], p[2]);
    },
    start(p = 0) {
      i.start.call(i, p);
    },
    stop(p = 0) {
      i.stop.call(i, p);
    }
  }, g = () => i.connect(u), w = () => i.disconnect(u);
  return e(o, i), r(An(l, u), g, w);
}, oe = (e, t) => {
  const n = e.createGain();
  return Me(n, t), vt(n, t, "gain"), n;
}, Ts = (e, { mediaStream: t }) => {
  const n = t.getAudioTracks();
  n.sort((s, a) => s.id < a.id ? -1 : s.id > a.id ? 1 : 0);
  const r = n.slice(0, 1), o = e.createMediaStreamSource(new MediaStream(r));
  return Object.defineProperty(o, "mediaStream", { value: t }), o;
}, Ms = (e) => e === null ? null : e.hasOwnProperty("OfflineAudioContext") ? e.OfflineAudioContext : e.hasOwnProperty("webkitOfflineAudioContext") ? e.webkitOfflineAudioContext : null, _t = (e, t, n, r) => e.createScriptProcessor(t, n, r), de = () => new DOMException("", "NotSupportedError"), Ns = (e, t) => (n, r, o) => (e(r).replay(o), t(r, n, o)), Os = (e, t, n) => async (r, o, s) => {
  const a = e(r);
  await Promise.all(a.activeInputs.map((c, i) => Array.from(c).map(async ([u, d]) => {
    const g = await t(u).render(u, o), w = r.context.destination;
    !n(u) && (r !== w || !n(r)) && g.connect(s, d, i);
  })).reduce((c, i) => [...c, ...i], []));
}, ks = (e, t, n) => async (r, o, s) => {
  const a = t(r);
  await Promise.all(Array.from(a.activeInputs).map(async ([c, i]) => {
    const d = await e(c).render(c, o);
    n(c) || d.connect(s, i);
  }));
}, Is = (e, t, n, r) => (o) => e(Xt, () => Xt(o)) ? Promise.resolve(e(r, r)).then((s) => {
  if (!s) {
    const a = n(o, 512, 0, 1);
    o.oncomplete = () => {
      a.onaudioprocess = null, a.disconnect();
    }, a.onaudioprocess = () => o.currentTime, a.connect(o.destination);
  }
  return o.startRendering();
}) : new Promise((s) => {
  const a = t(o, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    gain: 0
  });
  o.oncomplete = (c) => {
    a.disconnect(), s(c.renderedBuffer);
  }, a.connect(o.destination), o.startRendering();
}), Ss = (e) => (t, n) => {
  e.set(t, n);
}, Rs = (e) => () => {
  if (e === null)
    return !1;
  try {
    new e({ length: 1, sampleRate: 44100 });
  } catch {
    return !1;
  }
  return !0;
}, Ls = (e, t) => async () => {
  if (e === null)
    return !0;
  if (t === null)
    return !1;
  const n = new Blob(['class A extends AudioWorkletProcessor{process(i){this.port.postMessage(i,[i[0][0].buffer])}}registerProcessor("a",A)'], {
    type: "application/javascript; charset=utf-8"
  }), r = new t(1, 128, 44100), o = URL.createObjectURL(n);
  let s = !1, a = !1;
  try {
    await r.audioWorklet.addModule(o);
    const c = new e(r, "a", { numberOfOutputs: 0 }), i = r.createOscillator();
    c.port.onmessage = () => s = !0, c.onprocessorerror = () => a = !0, i.connect(c), i.start(0), await r.startRendering(), await new Promise((u) => setTimeout(u));
  } catch {
  } finally {
    URL.revokeObjectURL(o);
  }
  return s && !a;
}, Ps = (e, t) => () => {
  if (t === null)
    return Promise.resolve(!1);
  const n = new t(1, 1, 44100), r = e(n, {
    channelCount: 1,
    channelCountMode: "explicit",
    channelInterpretation: "discrete",
    gain: 0
  });
  return new Promise((o) => {
    n.oncomplete = () => {
      r.disconnect(), o(n.currentTime !== 0);
    }, n.startRendering();
  });
}, Bs = () => new DOMException("", "UnknownError"), Us = () => typeof window > "u" ? null : window, Ds = (e, t) => (n) => {
  n.copyFromChannel = (r, o, s = 0) => {
    const a = e(s), c = e(o);
    if (c >= n.numberOfChannels)
      throw t();
    const i = n.length, u = n.getChannelData(c), d = r.length;
    for (let l = a < 0 ? -a : 0; l + a < i && l < d; l += 1)
      r[l] = u[l + a];
  }, n.copyToChannel = (r, o, s = 0) => {
    const a = e(s), c = e(o);
    if (c >= n.numberOfChannels)
      throw t();
    const i = n.length, u = n.getChannelData(c), d = r.length;
    for (let l = a < 0 ? -a : 0; l + a < i && l < d; l += 1)
      u[l + a] = r[l];
  };
}, Ws = (e) => (t) => {
  t.copyFromChannel = /* @__PURE__ */ ((n) => (r, o, s = 0) => {
    const a = e(s), c = e(o);
    if (a < t.length)
      return n.call(t, r, c, a);
  })(t.copyFromChannel), t.copyToChannel = /* @__PURE__ */ ((n) => (r, o, s = 0) => {
    const a = e(s), c = e(o);
    if (a < t.length)
      return n.call(t, r, c, a);
  })(t.copyToChannel);
}, Vs = (e) => (t, n) => {
  const r = n.createBuffer(1, 1, 44100);
  t.buffer === null && (t.buffer = r), e(t, "buffer", (o) => () => {
    const s = o.call(t);
    return s === r ? null : s;
  }, (o) => (s) => o.call(t, s === null ? r : s));
}, xs = (e, t) => (n, r) => {
  r.channelCount = 1, r.channelCountMode = "explicit", Object.defineProperty(r, "channelCount", {
    get: () => 1,
    set: () => {
      throw e();
    }
  }), Object.defineProperty(r, "channelCountMode", {
    get: () => "explicit",
    set: () => {
      throw e();
    }
  });
  const o = n.createBufferSource();
  t(r, () => {
    const c = r.numberOfInputs;
    for (let i = 0; i < c; i += 1)
      o.connect(r, 0, i);
  }, () => o.disconnect(r));
}, Fs = (e, t, n) => e.copyFromChannel === void 0 ? e.getChannelData(n)[0] : (e.copyFromChannel(t, n), t[0]), yt = (e, t, n, r) => {
  let o = e;
  for (; !o.hasOwnProperty(t); )
    o = Object.getPrototypeOf(o);
  const { get: s, set: a } = Object.getOwnPropertyDescriptor(o, t);
  Object.defineProperty(e, t, { get: n(s), set: r(a) });
}, js = (e) => ({
  ...e,
  outputChannelCount: e.outputChannelCount !== void 0 ? e.outputChannelCount : e.numberOfInputs === 1 && e.numberOfOutputs === 1 ? (
    /*
     * Bug #61: This should be the computedNumberOfChannels, but unfortunately that is almost impossible to fake. That's why
     * the channelCountMode is required to be 'explicit' as long as there is not a native implementation in every browser. That
     * makes sure the computedNumberOfChannels is equivilant to the channelCount which makes it much easier to compute.
     */
    [e.channelCount]
  ) : Array.from({ length: e.numberOfOutputs }, () => 1)
}), Cn = (e, t, n) => {
  try {
    e.setValueAtTime(t, n);
  } catch (r) {
    if (r.code !== 9)
      throw r;
    Cn(e, t, n + 1e-7);
  }
}, Gs = (e) => {
  const t = e.createBufferSource();
  t.start();
  try {
    t.start();
  } catch {
    return !0;
  }
  return !1;
}, $s = (e) => {
  const t = e.createBufferSource(), n = e.createBuffer(1, 1, 44100);
  t.buffer = n;
  try {
    t.start(0, 1);
  } catch {
    return !1;
  }
  return !0;
}, qs = (e) => {
  const t = e.createBufferSource();
  t.start();
  try {
    t.stop();
  } catch {
    return !1;
  }
  return !0;
}, Tn = (e) => {
  const t = e.createOscillator();
  try {
    t.start(-1);
  } catch (n) {
    return n instanceof RangeError;
  }
  return !1;
}, zs = (e) => {
  const t = e.createBuffer(1, 1, 44100), n = e.createBufferSource();
  n.buffer = t, n.start(), n.stop();
  try {
    return n.stop(), !0;
  } catch {
    return !1;
  }
}, Mn = (e) => {
  const t = e.createOscillator();
  try {
    t.stop(-1);
  } catch (n) {
    return n instanceof RangeError;
  }
  return !1;
}, Xs = (e) => {
  const { port1: t, port2: n } = new MessageChannel();
  try {
    t.postMessage(e);
  } finally {
    t.close(), n.close();
  }
}, Ys = (e) => {
  e.start = /* @__PURE__ */ ((t) => (n = 0, r = 0, o) => {
    const s = e.buffer, a = s === null ? r : Math.min(s.duration, r);
    s !== null && a > s.duration - 0.5 / e.context.sampleRate ? t.call(e, n, 0, 0) : t.call(e, n, a, o);
  })(e.start);
}, Hs = (e, t) => {
  const n = t.createGain();
  e.connect(n);
  const r = /* @__PURE__ */ ((o) => () => {
    o.call(e, n), e.removeEventListener("ended", r);
  })(e.disconnect);
  e.addEventListener("ended", r), An(e, n), e.stop = /* @__PURE__ */ ((o) => {
    let s = !1;
    return (a = 0) => {
      if (s)
        try {
          o.call(e, a);
        } catch {
          n.gain.setValueAtTime(0, a);
        }
      else
        o.call(e, a), s = !0;
    };
  })(e.stop);
}, $e = (e, t) => (n) => {
  const r = { value: e };
  return Object.defineProperties(n, {
    currentTarget: r,
    target: r
  }), typeof t == "function" ? t.call(e, n) : t.handleEvent.call(e, n);
}, Zs = xr(le), Ks = zr(le), Qs = Po(je), Js = /* @__PURE__ */ new WeakMap(), ea = qo(Js), we = ko(/* @__PURE__ */ new Map(), /* @__PURE__ */ new WeakMap()), Q = Us(), Nn = $o(z), Et = Os(z, Nn, ie), ce = Yo(an), ve = Ms(Q), ee = ns(ve), On = /* @__PURE__ */ new WeakMap(), kn = xo($e), qe = ds(Q), ta = Jo(qe), In = es(Q), na = ts(Q), be = hs(Q), ze = Eo(Fr(nn), qr(Zs, Ks, dt, Qs, ft, z, ea, Ae, H, le, ae, ie, Se), we, Qo(at, ft, z, H, Ee, ae), ue, Ko, de, Lo(dt, at, z, H, Ee, ce, ae, ee), Do(On, z, K), kn, ce, ta, In, na, ee, be), ra = /* @__PURE__ */ new WeakSet(), Yt = cs(Q), Sn = Ro(new Uint32Array(1)), oa = Ds(Sn, ue), sa = Ws(Sn), aa = Kr(ra, we, de, Yt, ve, Rs(Yt), oa, sa), bt = Xr(oe), Rn = ks(Nn, Ce, ie), Ln = Io(Rn), Xe = ls(bt, we, Gs, $s, qs, Tn, zs, Mn, Ys, Vs(yt), Hs), Pn = Ns(zo(Ce), Rn), ia = eo(Ln, Xe, H, Pn, Et), At = bo(jr(on), On, sn, Ao, Pr, Br, Ur, Dr, Wr, rt, en, qe, Cn), ca = Jr(ze, ia, At, Z, Xe, ce, ee, $e), ua = uo(ze, lo, ue, Z, fs(oe, yt), ce, ee, Et), Ye = is(le, In), la = xs(Z, Ye), Ct = Es(qe, la), da = Cs(bt, Xe, oe, Ye), Tt = As(bt, we, da, Tn, Mn), fa = Is(we, oe, _t, Ps(oe, ve)), ha = fo(At, Ct, Tt, _t, de, Fs, ee, yt), Bn = /* @__PURE__ */ new WeakMap(), pa = as(ua, ha, kn, ee, Bn, $e), Un = rs(Q), Mt = Fo(Q), Dn = /* @__PURE__ */ new WeakMap(), ma = Ho(Dn, ve), Ht = Un ? $r(
  we,
  de,
  Vo(Q),
  Mt,
  jo(Vr),
  ce,
  ma,
  ee,
  be,
  /* @__PURE__ */ new WeakMap(),
  /* @__PURE__ */ new WeakMap(),
  Ls(be, ve),
  // @todo window is guaranteed to be defined because isSecureContext checks that as well.
  Q
) : void 0, ga = os(ze, Ts, ce, ee), Wn = Zo(Bn), wa = Yr(Wn), Vn = So(ue), va = Bo(Wn), xn = Wo(ue), Fn = /* @__PURE__ */ new WeakMap(), _a = Go(Fn, K), ya = ys(Vn, ue, Z, Ct, bn, Tt, oe, _t, de, xn, Mt, _a, Ye), Ea = ms(Z, ya, oe, de, Ye), ba = Oo(Ln, Vn, Xe, Ct, bn, Tt, oe, va, xn, Mt, H, be, ve, Pn, Et, fa), Aa = Xo(Dn), Ca = Ss(Fn), Zt = Un ? To(wa, ze, At, ba, Ea, z, Aa, ce, ee, be, js, Ca, Xs, $e) : void 0, Ta = ss(Z, de, Bs, pa, qe), jn = "Missing AudioWorklet support. Maybe this is not running in a secure context.", Ma = async (e, t, n, r, o) => {
  const { encoderInstanceId: s, port: a } = await Qt(o, t.sampleRate);
  if (Zt === void 0)
    throw new Error(jn);
  const c = new ca(t, { buffer: e }), i = new ga(t, { mediaStream: r }), u = Ir(Zt, t, { channelCount: n });
  return { audioBufferSourceNode: c, encoderInstanceId: s, mediaStreamAudioSourceNode: i, port: a, recorderAudioWorkletNode: u };
}, Na = (e, t, n, r) => (o, s, a) => {
  var c;
  const i = (c = s.getAudioTracks()[0]) === null || c === void 0 ? void 0 : c.getSettings().sampleRate, u = new Ta({ latencyHint: "playback", sampleRate: i }), d = Math.max(1024, Math.ceil(u.baseLatency * u.sampleRate)), l = new aa({ length: d, sampleRate: u.sampleRate }), g = [], w = kr((_) => {
    if (Ht === void 0)
      throw new Error(jn);
    return Ht(u, _);
  });
  let p = null, f = null, m = null, h = null, A = !0;
  const v = (_) => {
    o.dispatchEvent(e("dataavailable", { data: new Blob(_, { type: a }) }));
  }, T = async (_, M) => {
    const S = await Re(_, M);
    m === null ? g.push(...S) : (v(S), h = T(_, M));
  }, E = () => (A = !0, u.resume()), b = () => {
    m !== null && (p !== null && (s.removeEventListener("addtrack", p), s.removeEventListener("removetrack", p)), f !== null && clearTimeout(f), m.then(async ({ encoderInstanceId: _, mediaStreamAudioSourceNode: M, recorderAudioWorkletNode: S }) => {
      h !== null && (h.catch(() => {
      }), h = null), await S.stop(), M.disconnect(S);
      const N = await Re(_, null);
      m === null && await y(), v([...g, ...N]), g.length = 0, o.dispatchEvent(new Event("stop"));
    }), m = null);
  }, y = () => (A = !1, u.suspend());
  return y(), {
    get mimeType() {
      return a;
    },
    get state() {
      return m === null ? "inactive" : A ? "recording" : "paused";
    },
    pause() {
      if (m === null)
        throw n();
      A && (y(), o.dispatchEvent(new Event("pause")));
    },
    resume() {
      if (m === null)
        throw n();
      A || (E(), o.dispatchEvent(new Event("resume")));
    },
    start(_) {
      var M;
      if (m !== null)
        throw n();
      if (s.getVideoTracks().length > 0)
        throw r();
      o.dispatchEvent(new Event("start"));
      const S = s.getAudioTracks(), N = S.length === 0 ? 2 : (M = S[0].getSettings().channelCount) !== null && M !== void 0 ? M : 2;
      m = Promise.all([
        E(),
        w.then(() => Ma(l, u, N, s, a))
      ]).then(async ([, { audioBufferSourceNode: P, encoderInstanceId: B, mediaStreamAudioSourceNode: D, port: I, recorderAudioWorkletNode: U }]) => (D.connect(U), await new Promise((V) => {
        P.onended = V, P.connect(U), P.start(u.currentTime + d / u.sampleRate);
      }), P.disconnect(U), await U.record(I), _ !== void 0 && (h = T(B, _)), { encoderInstanceId: B, mediaStreamAudioSourceNode: D, recorderAudioWorkletNode: U }));
      const L = s.getTracks();
      p = () => {
        b(), o.dispatchEvent(new ErrorEvent("error", { error: t() }));
      }, s.addEventListener("addtrack", p), s.addEventListener("removetrack", p), f = setInterval(() => {
        const P = s.getTracks();
        (P.length !== L.length || P.some((B, D) => B !== L[D])) && p !== null && p();
      }, 1e3);
    },
    stop: b
  };
};
class tt {
  constructor(t, n = 0, r) {
    if (n < 0 || r !== void 0 && r < 0)
      throw new RangeError();
    const o = t.reduce((d, l) => d + l.byteLength, 0);
    if (n > o || r !== void 0 && n + r > o)
      throw new RangeError();
    const s = [], a = r === void 0 ? o - n : r, c = [];
    let i = 0, u = n;
    for (const d of t)
      if (c.length === 0)
        if (d.byteLength > u) {
          i = d.byteLength - u;
          const l = i > a ? a : i;
          s.push(new DataView(d, u, l)), c.push(d);
        } else
          u -= d.byteLength;
      else if (i < a) {
        i += d.byteLength;
        const l = i > a ? d.byteLength - i + a : d.byteLength;
        s.push(new DataView(d, 0, l)), c.push(d);
      }
    this._buffers = c, this._byteLength = a, this._byteOffset = u, this._dataViews = s, this._internalBuffer = new DataView(new ArrayBuffer(8));
  }
  get buffers() {
    return this._buffers;
  }
  get byteLength() {
    return this._byteLength;
  }
  get byteOffset() {
    return this._byteOffset;
  }
  getFloat32(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.setUint8(2, this.getUint8(t + 2)), this._internalBuffer.setUint8(3, this.getUint8(t + 3)), this._internalBuffer.getFloat32(0, n);
  }
  getFloat64(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.setUint8(2, this.getUint8(t + 2)), this._internalBuffer.setUint8(3, this.getUint8(t + 3)), this._internalBuffer.setUint8(4, this.getUint8(t + 4)), this._internalBuffer.setUint8(5, this.getUint8(t + 5)), this._internalBuffer.setUint8(6, this.getUint8(t + 6)), this._internalBuffer.setUint8(7, this.getUint8(t + 7)), this._internalBuffer.getFloat64(0, n);
  }
  getInt16(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.getInt16(0, n);
  }
  getInt32(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.setUint8(2, this.getUint8(t + 2)), this._internalBuffer.setUint8(3, this.getUint8(t + 3)), this._internalBuffer.getInt32(0, n);
  }
  getInt8(t) {
    const [n, r] = this._findDataViewWithOffset(t);
    return n.getInt8(t - r);
  }
  getUint16(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.getUint16(0, n);
  }
  getUint32(t, n) {
    return this._internalBuffer.setUint8(0, this.getUint8(t + 0)), this._internalBuffer.setUint8(1, this.getUint8(t + 1)), this._internalBuffer.setUint8(2, this.getUint8(t + 2)), this._internalBuffer.setUint8(3, this.getUint8(t + 3)), this._internalBuffer.getUint32(0, n);
  }
  getUint8(t) {
    const [n, r] = this._findDataViewWithOffset(t);
    return n.getUint8(t - r);
  }
  setFloat32(t, n, r) {
    this._internalBuffer.setFloat32(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1)), this.setUint8(t + 2, this._internalBuffer.getUint8(2)), this.setUint8(t + 3, this._internalBuffer.getUint8(3));
  }
  setFloat64(t, n, r) {
    this._internalBuffer.setFloat64(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1)), this.setUint8(t + 2, this._internalBuffer.getUint8(2)), this.setUint8(t + 3, this._internalBuffer.getUint8(3)), this.setUint8(t + 4, this._internalBuffer.getUint8(4)), this.setUint8(t + 5, this._internalBuffer.getUint8(5)), this.setUint8(t + 6, this._internalBuffer.getUint8(6)), this.setUint8(t + 7, this._internalBuffer.getUint8(7));
  }
  setInt16(t, n, r) {
    this._internalBuffer.setInt16(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1));
  }
  setInt32(t, n, r) {
    this._internalBuffer.setInt32(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1)), this.setUint8(t + 2, this._internalBuffer.getUint8(2)), this.setUint8(t + 3, this._internalBuffer.getUint8(3));
  }
  setInt8(t, n) {
    const [r, o] = this._findDataViewWithOffset(t);
    r.setInt8(t - o, n);
  }
  setUint16(t, n, r) {
    this._internalBuffer.setUint16(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1));
  }
  setUint32(t, n, r) {
    this._internalBuffer.setUint32(0, n, r), this.setUint8(t, this._internalBuffer.getUint8(0)), this.setUint8(t + 1, this._internalBuffer.getUint8(1)), this.setUint8(t + 2, this._internalBuffer.getUint8(2)), this.setUint8(t + 3, this._internalBuffer.getUint8(3));
  }
  setUint8(t, n) {
    const [r, o] = this._findDataViewWithOffset(t);
    r.setUint8(t - o, n);
  }
  _findDataViewWithOffset(t) {
    let n = 0;
    for (const r of this._dataViews) {
      const o = n + r.byteLength;
      if (t >= n && t < o)
        return [r, n];
      n = o;
    }
    throw new RangeError();
  }
}
const Oa = (e, t, n) => (r, o, s, a) => {
  const c = [], i = new o(s, { mimeType: "audio/webm;codecs=pcm" });
  let u = null, d = () => {
  };
  const l = (p) => {
    r.dispatchEvent(e("dataavailable", { data: new Blob(p, { type: a }) }));
  }, g = async (p, f) => {
    const m = await Re(p, f);
    i.state === "inactive" ? c.push(...m) : (l(m), u = g(p, f));
  }, w = () => {
    i.state !== "inactive" && (u !== null && (u.catch(() => {
    }), u = null), d(), d = () => {
    }, i.stop());
  };
  return i.addEventListener("error", (p) => {
    w(), r.dispatchEvent(new ErrorEvent("error", {
      error: p.error
    }));
  }), i.addEventListener("pause", () => r.dispatchEvent(new Event("pause"))), i.addEventListener("resume", () => r.dispatchEvent(new Event("resume"))), i.addEventListener("start", () => r.dispatchEvent(new Event("start"))), {
    get mimeType() {
      return a;
    },
    get state() {
      return i.state;
    },
    pause() {
      return i.pause();
    },
    resume() {
      return i.resume();
    },
    start(p) {
      const [f] = s.getAudioTracks();
      if (f !== void 0 && i.state === "inactive") {
        const { channelCount: m, sampleRate: h } = f.getSettings();
        if (m === void 0)
          throw new Error("The channelCount is not defined.");
        if (h === void 0)
          throw new Error("The sampleRate is not defined.");
        let A = !1, v = !1, T = 0, E = Qt(a, h);
        d = () => {
          v = !0;
        };
        const b = Jt(i, "dataavailable")(({ data: y }) => {
          T += 1;
          const _ = y.arrayBuffer();
          E = E.then(async ({ dataView: M = null, elementType: S = null, encoderInstanceId: N, port: L }) => {
            const P = await _;
            T -= 1;
            const B = M === null ? new tt([P]) : new tt([...M.buffers, P], M.byteOffset);
            if (!A && i.state === "recording" && !v) {
              const O = n(B, 0);
              if (O === null)
                return { dataView: B, elementType: S, encoderInstanceId: N, port: L };
              const { value: R } = O;
              if (R !== 172351395)
                return { dataView: M, elementType: S, encoderInstanceId: N, port: L };
              A = !0;
            }
            const { currentElementType: D, offset: I, contents: U } = t(B, S, m), V = I < B.byteLength ? new tt(B.buffers, B.byteOffset + I) : null;
            return U.forEach((O) => L.postMessage(O, O.map(({ buffer: R }) => R))), T === 0 && (i.state === "inactive" || v) && (Re(N, null).then((O) => {
              l([...c, ...O]), c.length = 0, r.dispatchEvent(new Event("stop"));
            }), L.postMessage([]), L.close(), b()), { dataView: V, elementType: D, encoderInstanceId: N, port: L };
          });
        });
        p !== void 0 && E.then(({ encoderInstanceId: y }) => {
          v || (u = g(y, p));
        });
      }
      i.start(100);
    },
    stop: w
  };
}, ka = () => typeof window > "u" ? null : window, Gn = (e, t) => {
  if (t >= e.byteLength)
    return null;
  const n = e.getUint8(t);
  if (n > 127)
    return 1;
  if (n > 63)
    return 2;
  if (n > 31)
    return 3;
  if (n > 15)
    return 4;
  if (n > 7)
    return 5;
  if (n > 3)
    return 6;
  if (n > 1)
    return 7;
  if (n > 0)
    return 8;
  const r = Gn(e, t + 1);
  return r === null ? null : r + 8;
}, Ia = (e, t) => (n) => {
  const r = { value: e };
  return Object.defineProperties(n, {
    currentTarget: r,
    target: r
  }), typeof t == "function" ? t.call(e, n) : t.handleEvent.call(e, n);
}, xe = [], He = ka(), Sa = fr(He), $n = or(Sa), Ra = Na($n, cr, ur, nt), Nt = wr(Gn), La = mr(Nt), Pa = gr(Nt), Ba = sr(La, Pa), Ua = Oa($n, Ba, Nt), Da = ir(He), Wa = hr(He), Ka = dr(pr(nt), nt, Ra, Ua, xe, ar(Da, Ia), Wa), qn = /* @__PURE__ */ new WeakMap(), Qa = async (e) => {
  await nr(e);
  const t = qn.get(e);
  if (t !== void 0) {
    const n = xe.indexOf(t);
    xe.splice(n, 1);
  }
}, Ja = () => lr(He), ei = async (e) => {
  const t = await rr(e);
  xe.push(t), qn.set(e, t);
};
export {
  Ka as MediaRecorder,
  Qa as deregister,
  Ja as isSupported,
  ei as register
};
