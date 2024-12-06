const U = window.ms_globals.React, jr = window.ms_globals.React.forwardRef, Rr = window.ms_globals.React.useRef, Dr = window.ms_globals.React.useState, Fr = window.ms_globals.React.useEffect, Lr = window.ms_globals.ReactDOM.createPortal;
var Wt = typeof global == "object" && global && global.Object === Object && global, Mr = typeof self == "object" && self && self.Object === Object && self, x = Wt || Mr || Function("return this")(), T = x.Symbol, Yt = Object.prototype, Nr = Yt.hasOwnProperty, Ur = Yt.toString, X = T ? T.toStringTag : void 0;
function Gr(e) {
  var t = Nr.call(e, X), r = e[X];
  try {
    e[X] = void 0;
    var n = !0;
  } catch {
  }
  var o = Ur.call(e);
  return n && (t ? e[X] = r : delete e[X]), o;
}
var Kr = Object.prototype, Br = Kr.toString;
function Hr(e) {
  return Br.call(e);
}
var zr = "[object Null]", qr = "[object Undefined]", pt = T ? T.toStringTag : void 0;
function K(e) {
  return e == null ? e === void 0 ? qr : zr : pt && pt in Object(e) ? Gr(e) : Hr(e);
}
function R(e) {
  return e != null && typeof e == "object";
}
var Wr = "[object Symbol]";
function Ce(e) {
  return typeof e == "symbol" || R(e) && K(e) == Wr;
}
function Xt(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length, o = Array(n); ++r < n; )
    o[r] = t(e[r], r, e);
  return o;
}
var S = Array.isArray, Yr = 1 / 0, dt = T ? T.prototype : void 0, gt = dt ? dt.toString : void 0;
function Jt(e) {
  if (typeof e == "string")
    return e;
  if (S(e))
    return Xt(e, Jt) + "";
  if (Ce(e))
    return gt ? gt.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -Yr ? "-0" : t;
}
function W(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function Zt(e) {
  return e;
}
var Xr = "[object AsyncFunction]", Jr = "[object Function]", Zr = "[object GeneratorFunction]", Qr = "[object Proxy]";
function Qt(e) {
  if (!W(e))
    return !1;
  var t = K(e);
  return t == Jr || t == Zr || t == Xr || t == Qr;
}
var _e = x["__core-js_shared__"], _t = function() {
  var e = /[^.]+$/.exec(_e && _e.keys && _e.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function Vr(e) {
  return !!_t && _t in e;
}
var kr = Function.prototype, en = kr.toString;
function B(e) {
  if (e != null) {
    try {
      return en.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var tn = /[\\^$.*+?()[\]{}|]/g, rn = /^\[object .+?Constructor\]$/, nn = Function.prototype, on = Object.prototype, sn = nn.toString, an = on.hasOwnProperty, ln = RegExp("^" + sn.call(an).replace(tn, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function un(e) {
  if (!W(e) || Vr(e))
    return !1;
  var t = Qt(e) ? ln : rn;
  return t.test(B(e));
}
function cn(e, t) {
  return e == null ? void 0 : e[t];
}
function H(e, t) {
  var r = cn(e, t);
  return un(r) ? r : void 0;
}
var me = H(x, "WeakMap"), ht = Object.create, fn = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!W(t))
      return {};
    if (ht)
      return ht(t);
    e.prototype = t;
    var r = new e();
    return e.prototype = void 0, r;
  };
}();
function pn(e, t, r) {
  switch (r.length) {
    case 0:
      return e.call(t);
    case 1:
      return e.call(t, r[0]);
    case 2:
      return e.call(t, r[0], r[1]);
    case 3:
      return e.call(t, r[0], r[1], r[2]);
  }
  return e.apply(t, r);
}
function dn(e, t) {
  var r = -1, n = e.length;
  for (t || (t = Array(n)); ++r < n; )
    t[r] = e[r];
  return t;
}
var gn = 800, _n = 16, hn = Date.now;
function yn(e) {
  var t = 0, r = 0;
  return function() {
    var n = hn(), o = _n - (n - r);
    if (r = n, o > 0) {
      if (++t >= gn)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function bn(e) {
  return function() {
    return e;
  };
}
var ae = function() {
  try {
    var e = H(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), mn = ae ? function(e, t) {
  return ae(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: bn(t),
    writable: !0
  });
} : Zt, vn = yn(mn);
function wn(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length; ++r < n && t(e[r], r, e) !== !1; )
    ;
  return e;
}
var Pn = 9007199254740991, Tn = /^(?:0|[1-9]\d*)$/;
function Vt(e, t) {
  var r = typeof e;
  return t = t ?? Pn, !!t && (r == "number" || r != "symbol" && Tn.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function $e(e, t, r) {
  t == "__proto__" && ae ? ae(e, t, {
    configurable: !0,
    enumerable: !0,
    value: r,
    writable: !0
  }) : e[t] = r;
}
function Ee(e, t) {
  return e === t || e !== e && t !== t;
}
var On = Object.prototype, Sn = On.hasOwnProperty;
function kt(e, t, r) {
  var n = e[t];
  (!(Sn.call(e, t) && Ee(n, r)) || r === void 0 && !(t in e)) && $e(e, t, r);
}
function k(e, t, r, n) {
  var o = !r;
  r || (r = {});
  for (var i = -1, s = t.length; ++i < s; ) {
    var a = t[i], l = void 0;
    l === void 0 && (l = e[a]), o ? $e(r, a, l) : kt(r, a, l);
  }
  return r;
}
var yt = Math.max;
function An(e, t, r) {
  return t = yt(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var n = arguments, o = -1, i = yt(n.length - t, 0), s = Array(i); ++o < i; )
      s[o] = n[t + o];
    o = -1;
    for (var a = Array(t + 1); ++o < t; )
      a[o] = n[o];
    return a[t] = r(s), pn(e, this, a);
  };
}
var xn = 9007199254740991;
function Ie(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= xn;
}
function er(e) {
  return e != null && Ie(e.length) && !Qt(e);
}
var Cn = Object.prototype;
function je(e) {
  var t = e && e.constructor, r = typeof t == "function" && t.prototype || Cn;
  return e === r;
}
function $n(e, t) {
  for (var r = -1, n = Array(e); ++r < e; )
    n[r] = t(r);
  return n;
}
var En = "[object Arguments]";
function bt(e) {
  return R(e) && K(e) == En;
}
var tr = Object.prototype, In = tr.hasOwnProperty, jn = tr.propertyIsEnumerable, Re = bt(/* @__PURE__ */ function() {
  return arguments;
}()) ? bt : function(e) {
  return R(e) && In.call(e, "callee") && !jn.call(e, "callee");
};
function Rn() {
  return !1;
}
var rr = typeof exports == "object" && exports && !exports.nodeType && exports, mt = rr && typeof module == "object" && module && !module.nodeType && module, Dn = mt && mt.exports === rr, vt = Dn ? x.Buffer : void 0, Fn = vt ? vt.isBuffer : void 0, le = Fn || Rn, Ln = "[object Arguments]", Mn = "[object Array]", Nn = "[object Boolean]", Un = "[object Date]", Gn = "[object Error]", Kn = "[object Function]", Bn = "[object Map]", Hn = "[object Number]", zn = "[object Object]", qn = "[object RegExp]", Wn = "[object Set]", Yn = "[object String]", Xn = "[object WeakMap]", Jn = "[object ArrayBuffer]", Zn = "[object DataView]", Qn = "[object Float32Array]", Vn = "[object Float64Array]", kn = "[object Int8Array]", eo = "[object Int16Array]", to = "[object Int32Array]", ro = "[object Uint8Array]", no = "[object Uint8ClampedArray]", oo = "[object Uint16Array]", io = "[object Uint32Array]", v = {};
v[Qn] = v[Vn] = v[kn] = v[eo] = v[to] = v[ro] = v[no] = v[oo] = v[io] = !0;
v[Ln] = v[Mn] = v[Jn] = v[Nn] = v[Zn] = v[Un] = v[Gn] = v[Kn] = v[Bn] = v[Hn] = v[zn] = v[qn] = v[Wn] = v[Yn] = v[Xn] = !1;
function so(e) {
  return R(e) && Ie(e.length) && !!v[K(e)];
}
function De(e) {
  return function(t) {
    return e(t);
  };
}
var nr = typeof exports == "object" && exports && !exports.nodeType && exports, Z = nr && typeof module == "object" && module && !module.nodeType && module, ao = Z && Z.exports === nr, he = ao && Wt.process, q = function() {
  try {
    var e = Z && Z.require && Z.require("util").types;
    return e || he && he.binding && he.binding("util");
  } catch {
  }
}(), wt = q && q.isTypedArray, or = wt ? De(wt) : so, lo = Object.prototype, uo = lo.hasOwnProperty;
function ir(e, t) {
  var r = S(e), n = !r && Re(e), o = !r && !n && le(e), i = !r && !n && !o && or(e), s = r || n || o || i, a = s ? $n(e.length, String) : [], l = a.length;
  for (var f in e)
    (t || uo.call(e, f)) && !(s && // Safari 9 has enumerable `arguments.length` in strict mode.
    (f == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    o && (f == "offset" || f == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    i && (f == "buffer" || f == "byteLength" || f == "byteOffset") || // Skip index properties.
    Vt(f, l))) && a.push(f);
  return a;
}
function sr(e, t) {
  return function(r) {
    return e(t(r));
  };
}
var co = sr(Object.keys, Object), fo = Object.prototype, po = fo.hasOwnProperty;
function go(e) {
  if (!je(e))
    return co(e);
  var t = [];
  for (var r in Object(e))
    po.call(e, r) && r != "constructor" && t.push(r);
  return t;
}
function ee(e) {
  return er(e) ? ir(e) : go(e);
}
function _o(e) {
  var t = [];
  if (e != null)
    for (var r in Object(e))
      t.push(r);
  return t;
}
var ho = Object.prototype, yo = ho.hasOwnProperty;
function bo(e) {
  if (!W(e))
    return _o(e);
  var t = je(e), r = [];
  for (var n in e)
    n == "constructor" && (t || !yo.call(e, n)) || r.push(n);
  return r;
}
function Fe(e) {
  return er(e) ? ir(e, !0) : bo(e);
}
var mo = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, vo = /^\w*$/;
function Le(e, t) {
  if (S(e))
    return !1;
  var r = typeof e;
  return r == "number" || r == "symbol" || r == "boolean" || e == null || Ce(e) ? !0 : vo.test(e) || !mo.test(e) || t != null && e in Object(t);
}
var Q = H(Object, "create");
function wo() {
  this.__data__ = Q ? Q(null) : {}, this.size = 0;
}
function Po(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var To = "__lodash_hash_undefined__", Oo = Object.prototype, So = Oo.hasOwnProperty;
function Ao(e) {
  var t = this.__data__;
  if (Q) {
    var r = t[e];
    return r === To ? void 0 : r;
  }
  return So.call(t, e) ? t[e] : void 0;
}
var xo = Object.prototype, Co = xo.hasOwnProperty;
function $o(e) {
  var t = this.__data__;
  return Q ? t[e] !== void 0 : Co.call(t, e);
}
var Eo = "__lodash_hash_undefined__";
function Io(e, t) {
  var r = this.__data__;
  return this.size += this.has(e) ? 0 : 1, r[e] = Q && t === void 0 ? Eo : t, this;
}
function G(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
G.prototype.clear = wo;
G.prototype.delete = Po;
G.prototype.get = Ao;
G.prototype.has = $o;
G.prototype.set = Io;
function jo() {
  this.__data__ = [], this.size = 0;
}
function fe(e, t) {
  for (var r = e.length; r--; )
    if (Ee(e[r][0], t))
      return r;
  return -1;
}
var Ro = Array.prototype, Do = Ro.splice;
function Fo(e) {
  var t = this.__data__, r = fe(t, e);
  if (r < 0)
    return !1;
  var n = t.length - 1;
  return r == n ? t.pop() : Do.call(t, r, 1), --this.size, !0;
}
function Lo(e) {
  var t = this.__data__, r = fe(t, e);
  return r < 0 ? void 0 : t[r][1];
}
function Mo(e) {
  return fe(this.__data__, e) > -1;
}
function No(e, t) {
  var r = this.__data__, n = fe(r, e);
  return n < 0 ? (++this.size, r.push([e, t])) : r[n][1] = t, this;
}
function D(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
D.prototype.clear = jo;
D.prototype.delete = Fo;
D.prototype.get = Lo;
D.prototype.has = Mo;
D.prototype.set = No;
var V = H(x, "Map");
function Uo() {
  this.size = 0, this.__data__ = {
    hash: new G(),
    map: new (V || D)(),
    string: new G()
  };
}
function Go(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function pe(e, t) {
  var r = e.__data__;
  return Go(t) ? r[typeof t == "string" ? "string" : "hash"] : r.map;
}
function Ko(e) {
  var t = pe(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function Bo(e) {
  return pe(this, e).get(e);
}
function Ho(e) {
  return pe(this, e).has(e);
}
function zo(e, t) {
  var r = pe(this, e), n = r.size;
  return r.set(e, t), this.size += r.size == n ? 0 : 1, this;
}
function F(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
F.prototype.clear = Uo;
F.prototype.delete = Ko;
F.prototype.get = Bo;
F.prototype.has = Ho;
F.prototype.set = zo;
var qo = "Expected a function";
function Me(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(qo);
  var r = function() {
    var n = arguments, o = t ? t.apply(this, n) : n[0], i = r.cache;
    if (i.has(o))
      return i.get(o);
    var s = e.apply(this, n);
    return r.cache = i.set(o, s) || i, s;
  };
  return r.cache = new (Me.Cache || F)(), r;
}
Me.Cache = F;
var Wo = 500;
function Yo(e) {
  var t = Me(e, function(n) {
    return r.size === Wo && r.clear(), n;
  }), r = t.cache;
  return t;
}
var Xo = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, Jo = /\\(\\)?/g, Zo = Yo(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(Xo, function(r, n, o, i) {
    t.push(o ? i.replace(Jo, "$1") : n || r);
  }), t;
});
function Qo(e) {
  return e == null ? "" : Jt(e);
}
function de(e, t) {
  return S(e) ? e : Le(e, t) ? [e] : Zo(Qo(e));
}
var Vo = 1 / 0;
function te(e) {
  if (typeof e == "string" || Ce(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -Vo ? "-0" : t;
}
function Ne(e, t) {
  t = de(t, e);
  for (var r = 0, n = t.length; e != null && r < n; )
    e = e[te(t[r++])];
  return r && r == n ? e : void 0;
}
function ko(e, t, r) {
  var n = e == null ? void 0 : Ne(e, t);
  return n === void 0 ? r : n;
}
function Ue(e, t) {
  for (var r = -1, n = t.length, o = e.length; ++r < n; )
    e[o + r] = t[r];
  return e;
}
var Pt = T ? T.isConcatSpreadable : void 0;
function ei(e) {
  return S(e) || Re(e) || !!(Pt && e && e[Pt]);
}
function ti(e, t, r, n, o) {
  var i = -1, s = e.length;
  for (r || (r = ei), o || (o = []); ++i < s; ) {
    var a = e[i];
    r(a) ? Ue(o, a) : o[o.length] = a;
  }
  return o;
}
function ri(e) {
  var t = e == null ? 0 : e.length;
  return t ? ti(e) : [];
}
function ni(e) {
  return vn(An(e, void 0, ri), e + "");
}
var Ge = sr(Object.getPrototypeOf, Object), oi = "[object Object]", ii = Function.prototype, si = Object.prototype, ar = ii.toString, ai = si.hasOwnProperty, li = ar.call(Object);
function ui(e) {
  if (!R(e) || K(e) != oi)
    return !1;
  var t = Ge(e);
  if (t === null)
    return !0;
  var r = ai.call(t, "constructor") && t.constructor;
  return typeof r == "function" && r instanceof r && ar.call(r) == li;
}
function ci(e, t, r) {
  var n = -1, o = e.length;
  t < 0 && (t = -t > o ? 0 : o + t), r = r > o ? o : r, r < 0 && (r += o), o = t > r ? 0 : r - t >>> 0, t >>>= 0;
  for (var i = Array(o); ++n < o; )
    i[n] = e[n + t];
  return i;
}
function fi() {
  this.__data__ = new D(), this.size = 0;
}
function pi(e) {
  var t = this.__data__, r = t.delete(e);
  return this.size = t.size, r;
}
function di(e) {
  return this.__data__.get(e);
}
function gi(e) {
  return this.__data__.has(e);
}
var _i = 200;
function hi(e, t) {
  var r = this.__data__;
  if (r instanceof D) {
    var n = r.__data__;
    if (!V || n.length < _i - 1)
      return n.push([e, t]), this.size = ++r.size, this;
    r = this.__data__ = new F(n);
  }
  return r.set(e, t), this.size = r.size, this;
}
function A(e) {
  var t = this.__data__ = new D(e);
  this.size = t.size;
}
A.prototype.clear = fi;
A.prototype.delete = pi;
A.prototype.get = di;
A.prototype.has = gi;
A.prototype.set = hi;
function yi(e, t) {
  return e && k(t, ee(t), e);
}
function bi(e, t) {
  return e && k(t, Fe(t), e);
}
var lr = typeof exports == "object" && exports && !exports.nodeType && exports, Tt = lr && typeof module == "object" && module && !module.nodeType && module, mi = Tt && Tt.exports === lr, Ot = mi ? x.Buffer : void 0, St = Ot ? Ot.allocUnsafe : void 0;
function vi(e, t) {
  if (t)
    return e.slice();
  var r = e.length, n = St ? St(r) : new e.constructor(r);
  return e.copy(n), n;
}
function wi(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length, o = 0, i = []; ++r < n; ) {
    var s = e[r];
    t(s, r, e) && (i[o++] = s);
  }
  return i;
}
function ur() {
  return [];
}
var Pi = Object.prototype, Ti = Pi.propertyIsEnumerable, At = Object.getOwnPropertySymbols, Ke = At ? function(e) {
  return e == null ? [] : (e = Object(e), wi(At(e), function(t) {
    return Ti.call(e, t);
  }));
} : ur;
function Oi(e, t) {
  return k(e, Ke(e), t);
}
var Si = Object.getOwnPropertySymbols, cr = Si ? function(e) {
  for (var t = []; e; )
    Ue(t, Ke(e)), e = Ge(e);
  return t;
} : ur;
function Ai(e, t) {
  return k(e, cr(e), t);
}
function fr(e, t, r) {
  var n = t(e);
  return S(e) ? n : Ue(n, r(e));
}
function ve(e) {
  return fr(e, ee, Ke);
}
function pr(e) {
  return fr(e, Fe, cr);
}
var we = H(x, "DataView"), Pe = H(x, "Promise"), Te = H(x, "Set"), xt = "[object Map]", xi = "[object Object]", Ct = "[object Promise]", $t = "[object Set]", Et = "[object WeakMap]", It = "[object DataView]", Ci = B(we), $i = B(V), Ei = B(Pe), Ii = B(Te), ji = B(me), O = K;
(we && O(new we(new ArrayBuffer(1))) != It || V && O(new V()) != xt || Pe && O(Pe.resolve()) != Ct || Te && O(new Te()) != $t || me && O(new me()) != Et) && (O = function(e) {
  var t = K(e), r = t == xi ? e.constructor : void 0, n = r ? B(r) : "";
  if (n)
    switch (n) {
      case Ci:
        return It;
      case $i:
        return xt;
      case Ei:
        return Ct;
      case Ii:
        return $t;
      case ji:
        return Et;
    }
  return t;
});
var Ri = Object.prototype, Di = Ri.hasOwnProperty;
function Fi(e) {
  var t = e.length, r = new e.constructor(t);
  return t && typeof e[0] == "string" && Di.call(e, "index") && (r.index = e.index, r.input = e.input), r;
}
var ue = x.Uint8Array;
function Be(e) {
  var t = new e.constructor(e.byteLength);
  return new ue(t).set(new ue(e)), t;
}
function Li(e, t) {
  var r = t ? Be(e.buffer) : e.buffer;
  return new e.constructor(r, e.byteOffset, e.byteLength);
}
var Mi = /\w*$/;
function Ni(e) {
  var t = new e.constructor(e.source, Mi.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var jt = T ? T.prototype : void 0, Rt = jt ? jt.valueOf : void 0;
function Ui(e) {
  return Rt ? Object(Rt.call(e)) : {};
}
function Gi(e, t) {
  var r = t ? Be(e.buffer) : e.buffer;
  return new e.constructor(r, e.byteOffset, e.length);
}
var Ki = "[object Boolean]", Bi = "[object Date]", Hi = "[object Map]", zi = "[object Number]", qi = "[object RegExp]", Wi = "[object Set]", Yi = "[object String]", Xi = "[object Symbol]", Ji = "[object ArrayBuffer]", Zi = "[object DataView]", Qi = "[object Float32Array]", Vi = "[object Float64Array]", ki = "[object Int8Array]", es = "[object Int16Array]", ts = "[object Int32Array]", rs = "[object Uint8Array]", ns = "[object Uint8ClampedArray]", os = "[object Uint16Array]", is = "[object Uint32Array]";
function ss(e, t, r) {
  var n = e.constructor;
  switch (t) {
    case Ji:
      return Be(e);
    case Ki:
    case Bi:
      return new n(+e);
    case Zi:
      return Li(e, r);
    case Qi:
    case Vi:
    case ki:
    case es:
    case ts:
    case rs:
    case ns:
    case os:
    case is:
      return Gi(e, r);
    case Hi:
      return new n();
    case zi:
    case Yi:
      return new n(e);
    case qi:
      return Ni(e);
    case Wi:
      return new n();
    case Xi:
      return Ui(e);
  }
}
function as(e) {
  return typeof e.constructor == "function" && !je(e) ? fn(Ge(e)) : {};
}
var ls = "[object Map]";
function us(e) {
  return R(e) && O(e) == ls;
}
var Dt = q && q.isMap, cs = Dt ? De(Dt) : us, fs = "[object Set]";
function ps(e) {
  return R(e) && O(e) == fs;
}
var Ft = q && q.isSet, ds = Ft ? De(Ft) : ps, gs = 1, _s = 2, hs = 4, dr = "[object Arguments]", ys = "[object Array]", bs = "[object Boolean]", ms = "[object Date]", vs = "[object Error]", gr = "[object Function]", ws = "[object GeneratorFunction]", Ps = "[object Map]", Ts = "[object Number]", _r = "[object Object]", Os = "[object RegExp]", Ss = "[object Set]", As = "[object String]", xs = "[object Symbol]", Cs = "[object WeakMap]", $s = "[object ArrayBuffer]", Es = "[object DataView]", Is = "[object Float32Array]", js = "[object Float64Array]", Rs = "[object Int8Array]", Ds = "[object Int16Array]", Fs = "[object Int32Array]", Ls = "[object Uint8Array]", Ms = "[object Uint8ClampedArray]", Ns = "[object Uint16Array]", Us = "[object Uint32Array]", m = {};
m[dr] = m[ys] = m[$s] = m[Es] = m[bs] = m[ms] = m[Is] = m[js] = m[Rs] = m[Ds] = m[Fs] = m[Ps] = m[Ts] = m[_r] = m[Os] = m[Ss] = m[As] = m[xs] = m[Ls] = m[Ms] = m[Ns] = m[Us] = !0;
m[vs] = m[gr] = m[Cs] = !1;
function oe(e, t, r, n, o, i) {
  var s, a = t & gs, l = t & _s, f = t & hs;
  if (r && (s = o ? r(e, n, o, i) : r(e)), s !== void 0)
    return s;
  if (!W(e))
    return e;
  var p = S(e);
  if (p) {
    if (s = Fi(e), !a)
      return dn(e, s);
  } else {
    var g = O(e), d = g == gr || g == ws;
    if (le(e))
      return vi(e, a);
    if (g == _r || g == dr || d && !o) {
      if (s = l || d ? {} : as(e), !a)
        return l ? Ai(e, bi(s, e)) : Oi(e, yi(s, e));
    } else {
      if (!m[g])
        return o ? e : {};
      s = ss(e, g, a);
    }
  }
  i || (i = new A());
  var h = i.get(e);
  if (h)
    return h;
  i.set(e, s), ds(e) ? e.forEach(function(c) {
    s.add(oe(c, t, r, c, e, i));
  }) : cs(e) && e.forEach(function(c, b) {
    s.set(b, oe(c, t, r, b, e, i));
  });
  var u = f ? l ? pr : ve : l ? Fe : ee, _ = p ? void 0 : u(e);
  return wn(_ || e, function(c, b) {
    _ && (b = c, c = e[b]), kt(s, b, oe(c, t, r, b, e, i));
  }), s;
}
var Gs = "__lodash_hash_undefined__";
function Ks(e) {
  return this.__data__.set(e, Gs), this;
}
function Bs(e) {
  return this.__data__.has(e);
}
function ce(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.__data__ = new F(); ++t < r; )
    this.add(e[t]);
}
ce.prototype.add = ce.prototype.push = Ks;
ce.prototype.has = Bs;
function Hs(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length; ++r < n; )
    if (t(e[r], r, e))
      return !0;
  return !1;
}
function zs(e, t) {
  return e.has(t);
}
var qs = 1, Ws = 2;
function hr(e, t, r, n, o, i) {
  var s = r & qs, a = e.length, l = t.length;
  if (a != l && !(s && l > a))
    return !1;
  var f = i.get(e), p = i.get(t);
  if (f && p)
    return f == t && p == e;
  var g = -1, d = !0, h = r & Ws ? new ce() : void 0;
  for (i.set(e, t), i.set(t, e); ++g < a; ) {
    var u = e[g], _ = t[g];
    if (n)
      var c = s ? n(_, u, g, t, e, i) : n(u, _, g, e, t, i);
    if (c !== void 0) {
      if (c)
        continue;
      d = !1;
      break;
    }
    if (h) {
      if (!Hs(t, function(b, w) {
        if (!zs(h, w) && (u === b || o(u, b, r, n, i)))
          return h.push(w);
      })) {
        d = !1;
        break;
      }
    } else if (!(u === _ || o(u, _, r, n, i))) {
      d = !1;
      break;
    }
  }
  return i.delete(e), i.delete(t), d;
}
function Ys(e) {
  var t = -1, r = Array(e.size);
  return e.forEach(function(n, o) {
    r[++t] = [o, n];
  }), r;
}
function Xs(e) {
  var t = -1, r = Array(e.size);
  return e.forEach(function(n) {
    r[++t] = n;
  }), r;
}
var Js = 1, Zs = 2, Qs = "[object Boolean]", Vs = "[object Date]", ks = "[object Error]", ea = "[object Map]", ta = "[object Number]", ra = "[object RegExp]", na = "[object Set]", oa = "[object String]", ia = "[object Symbol]", sa = "[object ArrayBuffer]", aa = "[object DataView]", Lt = T ? T.prototype : void 0, ye = Lt ? Lt.valueOf : void 0;
function la(e, t, r, n, o, i, s) {
  switch (r) {
    case aa:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case sa:
      return !(e.byteLength != t.byteLength || !i(new ue(e), new ue(t)));
    case Qs:
    case Vs:
    case ta:
      return Ee(+e, +t);
    case ks:
      return e.name == t.name && e.message == t.message;
    case ra:
    case oa:
      return e == t + "";
    case ea:
      var a = Ys;
    case na:
      var l = n & Js;
      if (a || (a = Xs), e.size != t.size && !l)
        return !1;
      var f = s.get(e);
      if (f)
        return f == t;
      n |= Zs, s.set(e, t);
      var p = hr(a(e), a(t), n, o, i, s);
      return s.delete(e), p;
    case ia:
      if (ye)
        return ye.call(e) == ye.call(t);
  }
  return !1;
}
var ua = 1, ca = Object.prototype, fa = ca.hasOwnProperty;
function pa(e, t, r, n, o, i) {
  var s = r & ua, a = ve(e), l = a.length, f = ve(t), p = f.length;
  if (l != p && !s)
    return !1;
  for (var g = l; g--; ) {
    var d = a[g];
    if (!(s ? d in t : fa.call(t, d)))
      return !1;
  }
  var h = i.get(e), u = i.get(t);
  if (h && u)
    return h == t && u == e;
  var _ = !0;
  i.set(e, t), i.set(t, e);
  for (var c = s; ++g < l; ) {
    d = a[g];
    var b = e[d], w = t[d];
    if (n)
      var L = s ? n(w, b, d, t, e, i) : n(b, w, d, e, t, i);
    if (!(L === void 0 ? b === w || o(b, w, r, n, i) : L)) {
      _ = !1;
      break;
    }
    c || (c = d == "constructor");
  }
  if (_ && !c) {
    var C = e.constructor, $ = t.constructor;
    C != $ && "constructor" in e && "constructor" in t && !(typeof C == "function" && C instanceof C && typeof $ == "function" && $ instanceof $) && (_ = !1);
  }
  return i.delete(e), i.delete(t), _;
}
var da = 1, Mt = "[object Arguments]", Nt = "[object Array]", ne = "[object Object]", ga = Object.prototype, Ut = ga.hasOwnProperty;
function _a(e, t, r, n, o, i) {
  var s = S(e), a = S(t), l = s ? Nt : O(e), f = a ? Nt : O(t);
  l = l == Mt ? ne : l, f = f == Mt ? ne : f;
  var p = l == ne, g = f == ne, d = l == f;
  if (d && le(e)) {
    if (!le(t))
      return !1;
    s = !0, p = !1;
  }
  if (d && !p)
    return i || (i = new A()), s || or(e) ? hr(e, t, r, n, o, i) : la(e, t, l, r, n, o, i);
  if (!(r & da)) {
    var h = p && Ut.call(e, "__wrapped__"), u = g && Ut.call(t, "__wrapped__");
    if (h || u) {
      var _ = h ? e.value() : e, c = u ? t.value() : t;
      return i || (i = new A()), o(_, c, r, n, i);
    }
  }
  return d ? (i || (i = new A()), pa(e, t, r, n, o, i)) : !1;
}
function He(e, t, r, n, o) {
  return e === t ? !0 : e == null || t == null || !R(e) && !R(t) ? e !== e && t !== t : _a(e, t, r, n, He, o);
}
var ha = 1, ya = 2;
function ba(e, t, r, n) {
  var o = r.length, i = o;
  if (e == null)
    return !i;
  for (e = Object(e); o--; ) {
    var s = r[o];
    if (s[2] ? s[1] !== e[s[0]] : !(s[0] in e))
      return !1;
  }
  for (; ++o < i; ) {
    s = r[o];
    var a = s[0], l = e[a], f = s[1];
    if (s[2]) {
      if (l === void 0 && !(a in e))
        return !1;
    } else {
      var p = new A(), g;
      if (!(g === void 0 ? He(f, l, ha | ya, n, p) : g))
        return !1;
    }
  }
  return !0;
}
function yr(e) {
  return e === e && !W(e);
}
function ma(e) {
  for (var t = ee(e), r = t.length; r--; ) {
    var n = t[r], o = e[n];
    t[r] = [n, o, yr(o)];
  }
  return t;
}
function br(e, t) {
  return function(r) {
    return r == null ? !1 : r[e] === t && (t !== void 0 || e in Object(r));
  };
}
function va(e) {
  var t = ma(e);
  return t.length == 1 && t[0][2] ? br(t[0][0], t[0][1]) : function(r) {
    return r === e || ba(r, e, t);
  };
}
function wa(e, t) {
  return e != null && t in Object(e);
}
function Pa(e, t, r) {
  t = de(t, e);
  for (var n = -1, o = t.length, i = !1; ++n < o; ) {
    var s = te(t[n]);
    if (!(i = e != null && r(e, s)))
      break;
    e = e[s];
  }
  return i || ++n != o ? i : (o = e == null ? 0 : e.length, !!o && Ie(o) && Vt(s, o) && (S(e) || Re(e)));
}
function Ta(e, t) {
  return e != null && Pa(e, t, wa);
}
var Oa = 1, Sa = 2;
function Aa(e, t) {
  return Le(e) && yr(t) ? br(te(e), t) : function(r) {
    var n = ko(r, e);
    return n === void 0 && n === t ? Ta(r, e) : He(t, n, Oa | Sa);
  };
}
function xa(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function Ca(e) {
  return function(t) {
    return Ne(t, e);
  };
}
function $a(e) {
  return Le(e) ? xa(te(e)) : Ca(e);
}
function Ea(e) {
  return typeof e == "function" ? e : e == null ? Zt : typeof e == "object" ? S(e) ? Aa(e[0], e[1]) : va(e) : $a(e);
}
function Ia(e) {
  return function(t, r, n) {
    for (var o = -1, i = Object(t), s = n(t), a = s.length; a--; ) {
      var l = s[++o];
      if (r(i[l], l, i) === !1)
        break;
    }
    return t;
  };
}
var ja = Ia();
function Ra(e, t) {
  return e && ja(e, t, ee);
}
function Da(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function Fa(e, t) {
  return t.length < 2 ? e : Ne(e, ci(t, 0, -1));
}
function La(e) {
  return e === void 0;
}
function Ma(e, t) {
  var r = {};
  return t = Ea(t), Ra(e, function(n, o, i) {
    $e(r, t(n, o, i), n);
  }), r;
}
function Na(e, t) {
  return t = de(t, e), e = Fa(e, t), e == null || delete e[te(Da(t))];
}
function Ua(e) {
  return ui(e) ? void 0 : e;
}
var Ga = 1, Ka = 2, Ba = 4, mr = ni(function(e, t) {
  var r = {};
  if (e == null)
    return r;
  var n = !1;
  t = Xt(t, function(i) {
    return i = de(i, e), n || (n = i.length > 1), i;
  }), k(e, pr(e), r), n && (r = oe(r, Ga | Ka | Ba, Ua));
  for (var o = t.length; o--; )
    Na(r, t[o]);
  return r;
});
function Ha(e) {
  return e.replace(/(^|_)(\w)/g, (t, r, n, o) => o === 0 ? n.toLowerCase() : n.toUpperCase());
}
const vr = ["interactive", "gradio", "server", "target", "theme_mode", "root", "name", "visible", "elem_id", "elem_classes", "elem_style", "_internal", "props", "value", "_selectable", "attached_events", "loading_status", "value_is_output"];
function za(e, t = {}) {
  return Ma(mr(e, vr), (r, n) => t[n] || Ha(n));
}
function qa(e) {
  const {
    gradio: t,
    _internal: r,
    restProps: n,
    originalRestProps: o,
    ...i
  } = e;
  return Object.keys(r).reduce((s, a) => {
    const l = a.match(/bind_(.+)_event/);
    if (l) {
      const f = l[1], p = f.split("_"), g = (...h) => {
        const u = h.map((c) => h && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
          type: c.type,
          detail: c.detail,
          timestamp: c.timeStamp,
          clientX: c.clientX,
          clientY: c.clientY,
          targetId: c.target.id,
          targetClassName: c.target.className,
          altKey: c.altKey,
          ctrlKey: c.ctrlKey,
          shiftKey: c.shiftKey,
          metaKey: c.metaKey
        } : c);
        let _;
        try {
          _ = JSON.parse(JSON.stringify(u));
        } catch {
          _ = u.map((c) => c && typeof c == "object" ? Object.fromEntries(Object.entries(c).filter(([, b]) => {
            try {
              return JSON.stringify(b), !0;
            } catch {
              return !1;
            }
          })) : c);
        }
        return t.dispatch(f.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: _,
          component: {
            ...i,
            ...mr(o, vr)
          }
        });
      };
      if (p.length > 1) {
        let h = {
          ...i.props[p[0]] || (n == null ? void 0 : n[p[0]]) || {}
        };
        s[p[0]] = h;
        for (let _ = 1; _ < p.length - 1; _++) {
          const c = {
            ...i.props[p[_]] || (n == null ? void 0 : n[p[_]]) || {}
          };
          h[p[_]] = c, h = c;
        }
        const u = p[p.length - 1];
        return h[`on${u.slice(0, 1).toUpperCase()}${u.slice(1)}`] = g, s;
      }
      const d = p[0];
      s[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = g;
    }
    return s;
  }, {});
}
function ie() {
}
function Wa(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Ya(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return ie;
  }
  const r = e.subscribe(...t);
  return r.unsubscribe ? () => r.unsubscribe() : r;
}
function N(e) {
  let t;
  return Ya(e, (r) => t = r)(), t;
}
const z = [];
function j(e, t = ie) {
  let r;
  const n = /* @__PURE__ */ new Set();
  function o(a) {
    if (Wa(e, a) && (e = a, r)) {
      const l = !z.length;
      for (const f of n)
        f[1](), z.push(f, e);
      if (l) {
        for (let f = 0; f < z.length; f += 2)
          z[f][0](z[f + 1]);
        z.length = 0;
      }
    }
  }
  function i(a) {
    o(a(e));
  }
  function s(a, l = ie) {
    const f = [a, l];
    return n.add(f), n.size === 1 && (r = t(o, i) || ie), a(e), () => {
      n.delete(f), n.size === 0 && r && (r(), r = null);
    };
  }
  return {
    set: o,
    update: i,
    subscribe: s
  };
}
const {
  getContext: Xa,
  setContext: Nl
} = window.__gradio__svelte__internal, Ja = "$$ms-gr-loading-status-key";
function Za() {
  const e = window.ms_globals.loadingKey++, t = Xa(Ja);
  return (r) => {
    if (!t || !r)
      return;
    const {
      loadingStatusMap: n,
      options: o
    } = t, {
      generating: i,
      error: s
    } = N(o);
    (r == null ? void 0 : r.status) === "pending" || s && (r == null ? void 0 : r.status) === "error" || (i && (r == null ? void 0 : r.status)) === "generating" ? n.update(({
      map: a
    }) => (a.set(e, r), {
      map: a
    })) : n.update(({
      map: a
    }) => (a.delete(e), {
      map: a
    }));
  };
}
const {
  getContext: ze,
  setContext: re
} = window.__gradio__svelte__internal, Qa = "$$ms-gr-slots-key";
function Va() {
  const e = j({});
  return re(Qa, e);
}
const ka = "$$ms-gr-render-slot-context-key";
function el() {
  const e = re(ka, j({}));
  return (t, r) => {
    e.update((n) => typeof r == "function" ? {
      ...n,
      [t]: r(n[t])
    } : {
      ...n,
      [t]: r
    });
  };
}
const tl = "$$ms-gr-context-key";
function be(e) {
  return La(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const wr = "$$ms-gr-sub-index-context-key";
function rl() {
  return ze(wr) || null;
}
function Gt(e) {
  return re(wr, e);
}
function nl(e, t, r) {
  var d, h;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = Tr(), o = sl({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), i = rl();
  typeof i == "number" && Gt(void 0);
  const s = Za();
  typeof e._internal.subIndex == "number" && Gt(e._internal.subIndex), n && n.subscribe((u) => {
    o.slotKey.set(u);
  }), ol();
  const a = ze(tl), l = ((d = N(a)) == null ? void 0 : d.as_item) || e.as_item, f = be(a ? l ? ((h = N(a)) == null ? void 0 : h[l]) || {} : N(a) || {} : {}), p = (u, _) => u ? za({
    ...u,
    ..._ || {}
  }, t) : void 0, g = j({
    ...e,
    _internal: {
      ...e._internal,
      index: i ?? e._internal.index
    },
    ...f,
    restProps: p(e.restProps, f),
    originalRestProps: e.restProps
  });
  return a ? (a.subscribe((u) => {
    const {
      as_item: _
    } = N(g);
    _ && (u = u == null ? void 0 : u[_]), u = be(u), g.update((c) => ({
      ...c,
      ...u || {},
      restProps: p(c.restProps, u)
    }));
  }), [g, (u) => {
    var c, b;
    const _ = be(u.as_item ? ((c = N(a)) == null ? void 0 : c[u.as_item]) || {} : N(a) || {});
    return s((b = u.restProps) == null ? void 0 : b.loading_status), g.set({
      ...u,
      _internal: {
        ...u._internal,
        index: i ?? u._internal.index
      },
      ..._,
      restProps: p(u.restProps, _),
      originalRestProps: u.restProps
    });
  }]) : [g, (u) => {
    var _;
    s((_ = u.restProps) == null ? void 0 : _.loading_status), g.set({
      ...u,
      _internal: {
        ...u._internal,
        index: i ?? u._internal.index
      },
      restProps: p(u.restProps),
      originalRestProps: u.restProps
    });
  }];
}
const Pr = "$$ms-gr-slot-key";
function ol() {
  re(Pr, j(void 0));
}
function Tr() {
  return ze(Pr);
}
const il = "$$ms-gr-component-slot-context-key";
function sl({
  slot: e,
  index: t,
  subIndex: r
}) {
  return re(il, {
    slotKey: j(e),
    slotIndex: j(t),
    subSlotIndex: j(r)
  });
}
function al(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function P(e, t = !1) {
  try {
    if (t && !al(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function ll(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Or = {
  exports: {}
}, ge = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ul = U, cl = Symbol.for("react.element"), fl = Symbol.for("react.fragment"), pl = Object.prototype.hasOwnProperty, dl = ul.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, gl = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Sr(e, t, r) {
  var n, o = {}, i = null, s = null;
  r !== void 0 && (i = "" + r), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) pl.call(t, n) && !gl.hasOwnProperty(n) && (o[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: cl,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: dl.current
  };
}
ge.Fragment = fl;
ge.jsx = Sr;
ge.jsxs = Sr;
Or.exports = ge;
var Oe = Or.exports;
const _l = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function hl(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const n = e[r];
    return typeof n == "number" && !_l.includes(r) ? t[r] = n + "px" : t[r] = n, t;
  }, {}) : {};
}
function Se(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(Lr(U.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: U.Children.toArray(e._reactElement.props.children).map((o) => {
        if (U.isValidElement(o) && o.props.__slot__) {
          const {
            portals: i,
            clonedElement: s
          } = Se(o.props.el);
          return U.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...U.Children.toArray(o.props.children), ...i]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: l
    }) => {
      r.addEventListener(a, s, l);
    });
  });
  const n = Array.from(e.childNodes);
  for (let o = 0; o < n.length; o++) {
    const i = n[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Se(i);
      t.push(...a), r.appendChild(s);
    } else i.nodeType === 3 && r.appendChild(i.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function yl(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Ae = jr(({
  slot: e,
  clone: t,
  className: r,
  style: n
}, o) => {
  const i = Rr(), [s, a] = Dr([]);
  return Fr(() => {
    var g;
    if (!i.current || !e)
      return;
    let l = e;
    function f() {
      let d = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (d = l.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), yl(o, d), r && d.classList.add(...r.split(" ")), n) {
        const h = hl(n);
        Object.keys(h).forEach((u) => {
          d.style[u] = h[u];
        });
      }
    }
    let p = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var c, b, w;
        (c = i.current) != null && c.contains(l) && ((b = i.current) == null || b.removeChild(l));
        const {
          portals: u,
          clonedElement: _
        } = Se(e);
        return l = _, a(u), l.style.display = "contents", f(), (w = i.current) == null || w.appendChild(l), u.length > 0;
      };
      d() || (p = new window.MutationObserver(() => {
        d() && (p == null || p.disconnect());
      }), p.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      l.style.display = "contents", f(), (g = i.current) == null || g.appendChild(l);
    return () => {
      var d, h;
      l.style.display = "", (d = i.current) != null && d.contains(l) && ((h = i.current) == null || h.removeChild(l)), p == null || p.disconnect();
    };
  }, [e, t, r, n, o]), U.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...s);
}), {
  getContext: bl,
  setContext: ml
} = window.__gradio__svelte__internal;
function Ar(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function r(o = ["default"]) {
    const i = o.reduce((s, a) => (s[a] = j([]), s), {});
    return ml(t, {
      itemsMap: i,
      allowedSlots: o
    }), i;
  }
  function n() {
    const {
      itemsMap: o,
      allowedSlots: i
    } = bl(t);
    return function(s, a, l) {
      o && (s ? o[s].update((f) => {
        const p = [...f];
        return i.includes(s) ? p[a] = l : p[a] = void 0, p;
      }) : i.includes("default") && o.default.update((f) => {
        const p = [...f];
        return p[a] = l, p;
      }));
    };
  }
  return {
    getItems: r,
    getSetItemFn: n
  };
}
function xr(e, t, r) {
  const n = e.filter(Boolean);
  if (n.length !== 0)
    return n.map((o, i) => {
      var f;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const s = {
        ...o.props,
        key: ((f = o.props) == null ? void 0 : f.key) ?? (r ? `${r}-${i}` : `${i}`)
      };
      let a = s;
      Object.keys(o.slots).forEach((p) => {
        if (!o.slots[p] || !(o.slots[p] instanceof Element) && !o.slots[p].el)
          return;
        const g = p.split(".");
        g.forEach((c, b) => {
          a[c] || (a[c] = {}), b !== g.length - 1 && (a = s[c]);
        });
        const d = o.slots[p];
        let h, u, _ = (t == null ? void 0 : t.clone) ?? !1;
        d instanceof Element ? h = d : (h = d.el, u = d.callback, _ = d.clone ?? _), a[g[g.length - 1]] = h ? u ? (...c) => (u(g[g.length - 1], c), /* @__PURE__ */ Oe.jsx(Ae, {
          slot: h,
          clone: _
        })) : /* @__PURE__ */ Oe.jsx(Ae, {
          slot: h,
          clone: _
        }) : a[g[g.length - 1]], a = s;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return o[l] && (s[l] = xr(o[l], t, `${i}`)), s;
    });
}
function Cr(e, t) {
  return e ? /* @__PURE__ */ Oe.jsx(Ae, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Kt({
  key: e,
  setSlotParams: t,
  slots: r
}, n) {
  return r[e] ? (...o) => (t(e, o), Cr(r[e], {
    clone: !0,
    ...n
  })) : void 0;
}
var $r = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function r() {
      for (var i = "", s = 0; s < arguments.length; s++) {
        var a = arguments[s];
        a && (i = o(i, n(a)));
      }
      return i;
    }
    function n(i) {
      if (typeof i == "string" || typeof i == "number")
        return i;
      if (typeof i != "object")
        return "";
      if (Array.isArray(i))
        return r.apply(null, i);
      if (i.toString !== Object.prototype.toString && !i.toString.toString().includes("[native code]"))
        return i.toString();
      var s = "";
      for (var a in i)
        t.call(i, a) && i[a] && (s = o(s, a));
      return s;
    }
    function o(i, s) {
      return s ? i ? i + " " + s : i + s : i;
    }
    e.exports ? (r.default = r, e.exports = r) : window.classNames = r;
  })();
})($r);
var vl = $r.exports;
const wl = /* @__PURE__ */ ll(vl), {
  getItems: Pl,
  getSetItemFn: Ul
} = Ar("menu"), {
  getItems: Gl,
  getSetItemFn: Tl
} = Ar("table-column"), {
  SvelteComponent: Ol,
  assign: Bt,
  check_outros: Sl,
  component_subscribe: J,
  compute_rest_props: Ht,
  create_slot: Al,
  detach: xl,
  empty: zt,
  exclude_internal_props: Cl,
  flush: I,
  get_all_dirty_from_scope: $l,
  get_slot_changes: El,
  group_outros: Il,
  init: jl,
  insert_hydration: Rl,
  safe_not_equal: Dl,
  transition_in: se,
  transition_out: xe,
  update_slot_base: Fl
} = window.__gradio__svelte__internal;
function qt(e) {
  let t;
  const r = (
    /*#slots*/
    e[20].default
  ), n = Al(
    r,
    e,
    /*$$scope*/
    e[19],
    null
  );
  return {
    c() {
      n && n.c();
    },
    l(o) {
      n && n.l(o);
    },
    m(o, i) {
      n && n.m(o, i), t = !0;
    },
    p(o, i) {
      n && n.p && (!t || i & /*$$scope*/
      524288) && Fl(
        n,
        r,
        o,
        /*$$scope*/
        o[19],
        t ? El(
          r,
          /*$$scope*/
          o[19],
          i,
          null
        ) : $l(
          /*$$scope*/
          o[19]
        ),
        null
      );
    },
    i(o) {
      t || (se(n, o), t = !0);
    },
    o(o) {
      xe(n, o), t = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function Ll(e) {
  let t, r, n = (
    /*$mergedProps*/
    e[0].visible && qt(e)
  );
  return {
    c() {
      n && n.c(), t = zt();
    },
    l(o) {
      n && n.l(o), t = zt();
    },
    m(o, i) {
      n && n.m(o, i), Rl(o, t, i), r = !0;
    },
    p(o, [i]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, i), i & /*$mergedProps*/
      1 && se(n, 1)) : (n = qt(o), n.c(), se(n, 1), n.m(t.parentNode, t)) : n && (Il(), xe(n, 1, 1, () => {
        n = null;
      }), Sl());
    },
    i(o) {
      r || (se(n), r = !0);
    },
    o(o) {
      xe(n), r = !1;
    },
    d(o) {
      o && xl(t), n && n.d(o);
    }
  };
}
function Ml(e, t, r) {
  const n = ["gradio", "props", "_internal", "as_item", "built_in_column", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = Ht(t, n), i, s, a, l, f, {
    $$slots: p = {},
    $$scope: g
  } = t, {
    gradio: d
  } = t, {
    props: h = {}
  } = t;
  const u = j(h);
  J(e, u, (y) => r(18, f = y));
  let {
    _internal: _ = {}
  } = t, {
    as_item: c
  } = t, {
    built_in_column: b
  } = t, {
    visible: w = !0
  } = t, {
    elem_id: L = ""
  } = t, {
    elem_classes: C = []
  } = t, {
    elem_style: $ = {}
  } = t;
  const qe = Tr();
  J(e, qe, (y) => r(16, a = y));
  const [We, Er] = nl({
    gradio: d,
    props: f,
    _internal: _,
    visible: w,
    elem_id: L,
    elem_classes: C,
    elem_style: $,
    as_item: c,
    restProps: o
  }, {
    column_render: "render"
  });
  J(e, We, (y) => r(0, s = y));
  const Ye = Va();
  J(e, Ye, (y) => r(15, i = y));
  const {
    "filterDropdownProps.menu.items": Xe
  } = Pl(["filterDropdownProps.menu.items"]);
  J(e, Xe, (y) => r(17, l = y));
  const Ir = Tl(), M = el();
  return e.$$set = (y) => {
    t = Bt(Bt({}, t), Cl(y)), r(24, o = Ht(t, n)), "gradio" in y && r(6, d = y.gradio), "props" in y && r(7, h = y.props), "_internal" in y && r(8, _ = y._internal), "as_item" in y && r(9, c = y.as_item), "built_in_column" in y && r(10, b = y.built_in_column), "visible" in y && r(11, w = y.visible), "elem_id" in y && r(12, L = y.elem_id), "elem_classes" in y && r(13, C = y.elem_classes), "elem_style" in y && r(14, $ = y.elem_style), "$$scope" in y && r(19, g = y.$$scope);
  }, e.$$.update = () => {
    var y, Je, Ze, Qe, Ve, ke, et, tt, rt, nt, ot, it, st, at, lt, ut;
    if (e.$$.dirty & /*props*/
    128 && u.update((E) => ({
      ...E,
      ...h
    })), Er({
      gradio: d,
      props: f,
      _internal: _,
      visible: w,
      elem_id: L,
      elem_classes: C,
      elem_style: $,
      as_item: c,
      restProps: o
    }), e.$$.dirty & /*$mergedProps, $dropdownMenuItems, $slots, $slotKey, built_in_column*/
    230401) {
      const E = s.props.showSorterTooltip || s.restProps.showSorterTooltip, Y = s.props.sorter || s.restProps.sorter, ct = {
        ...((y = s.restProps.filterDropdownProps) == null ? void 0 : y.menu) || {},
        ...((Je = s.props.filterDropdownProps) == null ? void 0 : Je.menu) || {},
        items: (Qe = (Ze = s.props.filterDropdownProps) == null ? void 0 : Ze.menu) != null && Qe.items || (ke = (Ve = s.restProps.filterDropdownProps) == null ? void 0 : Ve.menu) != null && ke.items || l.length > 0 ? xr(l, {
          clone: !0
        }) : void 0,
        expandIcon: Kt({
          setSlotParams: M,
          slots: i,
          key: "filterDropdownProps.menu.expandIcon"
        }, {
          clone: !0
        }) || ((tt = (et = s.props.filterDropdownProps) == null ? void 0 : et.menu) == null ? void 0 : tt.expandIcon) || ((nt = (rt = s.restProps.filterDropdownProps) == null ? void 0 : rt.menu) == null ? void 0 : nt.expandIcon),
        overflowedIndicator: Cr(i["filterDropdownProps.menu.overflowedIndicator"]) || ((it = (ot = s.props.filterDropdownProps) == null ? void 0 : ot.menu) == null ? void 0 : it.overflowedIndicator) || ((at = (st = s.restProps.filterDropdownProps) == null ? void 0 : st.menu) == null ? void 0 : at.overflowedIndicator)
      }, ft = {
        ...s.restProps.filterDropdownProps || {},
        ...s.props.filterDropdownProps || {},
        dropdownRender: i["filterDropdownProps.dropdownRender"] ? Kt({
          setSlotParams: M,
          slots: i,
          key: "filterDropdownProps.dropdownRender"
        }, {
          clone: !0
        }) : P(((lt = s.props.filterDropdownProps) == null ? void 0 : lt.dropdownRender) || ((ut = s.restProps.filterDropdownProps) == null ? void 0 : ut.dropdownRender)),
        menu: Object.values(ct).filter(Boolean).length > 0 ? ct : void 0
      };
      Ir(a, s._internal.index || 0, b || {
        props: {
          style: s.elem_style,
          className: wl(s.elem_classes, "ms-gr-antd-table-column"),
          id: s.elem_id,
          ...s.restProps,
          ...s.props,
          ...qa(s),
          render: P(s.props.render || s.restProps.render),
          filterDropdownProps: Object.values(ft).filter(Boolean).length > 0 ? ft : void 0,
          filterIcon: P(s.props.filterIcon || s.restProps.filterIcon),
          filterDropdown: P(s.props.filterDropdown || s.restProps.filterDropdown),
          showSorterTooltip: typeof E == "object" ? {
            ...E,
            afterOpenChange: P(typeof E == "object" ? E.afterOpenChange : void 0),
            getPopupContainer: P(typeof E == "object" ? E.getPopupContainer : void 0)
          } : E,
          sorter: typeof Y == "object" ? {
            ...Y,
            compare: P(Y.compare) || Y.compare
          } : P(Y) || s.props.sorter,
          filterSearch: P(s.props.filterSearch || s.restProps.filterSearch) || s.props.filterSearch || s.restProps.filterSearch,
          shouldCellUpdate: P(s.props.shouldCellUpdate || s.restProps.shouldCellUpdate),
          onCell: P(s.props.onCell || s.restProps.onCell),
          onFilter: P(s.props.onFilter || s.restProps.onFilter),
          onHeaderCell: P(s.props.onHeaderCell || s.restProps.onHeaderCell)
        },
        slots: {
          ...i,
          filterIcon: {
            el: i.filterIcon,
            callback: M,
            clone: !0
          },
          filterDropdown: {
            el: i.filterDropdown,
            callback: M,
            clone: !0
          },
          sortIcon: {
            el: i.sortIcon,
            callback: M,
            clone: !0
          },
          title: {
            el: i.title,
            callback: M,
            clone: !0
          },
          render: {
            el: i.render,
            callback: M,
            clone: !0
          }
        }
      });
    }
  }, [s, u, qe, We, Ye, Xe, d, h, _, c, b, w, L, C, $, i, a, l, f, g, p];
}
class Kl extends Ol {
  constructor(t) {
    super(), jl(this, t, Ml, Ll, Dl, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      built_in_column: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), I();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), I();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), I();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), I();
  }
  get built_in_column() {
    return this.$$.ctx[10];
  }
  set built_in_column(t) {
    this.$$set({
      built_in_column: t
    }), I();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), I();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), I();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), I();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), I();
  }
}
export {
  Kl as default
};
