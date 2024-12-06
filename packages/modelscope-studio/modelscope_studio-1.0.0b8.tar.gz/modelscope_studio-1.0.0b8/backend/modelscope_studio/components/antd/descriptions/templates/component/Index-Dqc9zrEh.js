var At = typeof global == "object" && global && global.Object === Object && global, an = typeof self == "object" && self && self.Object === Object && self, S = At || an || Function("return this")(), O = S.Symbol, Pt = Object.prototype, un = Pt.hasOwnProperty, ln = Pt.toString, q = O ? O.toStringTag : void 0;
function fn(e) {
  var t = un.call(e, q), n = e[q];
  try {
    e[q] = void 0;
    var r = !0;
  } catch {
  }
  var o = ln.call(e);
  return r && (t ? e[q] = n : delete e[q]), o;
}
var cn = Object.prototype, pn = cn.toString;
function gn(e) {
  return pn.call(e);
}
var dn = "[object Null]", _n = "[object Undefined]", qe = O ? O.toStringTag : void 0;
function D(e) {
  return e == null ? e === void 0 ? _n : dn : qe && qe in Object(e) ? fn(e) : gn(e);
}
function E(e) {
  return e != null && typeof e == "object";
}
var bn = "[object Symbol]";
function Pe(e) {
  return typeof e == "symbol" || E(e) && D(e) == bn;
}
function $t(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, o = Array(r); ++n < r; )
    o[n] = t(e[n], n, e);
  return o;
}
var P = Array.isArray, hn = 1 / 0, Ye = O ? O.prototype : void 0, Xe = Ye ? Ye.toString : void 0;
function St(e) {
  if (typeof e == "string")
    return e;
  if (P(e))
    return $t(e, St) + "";
  if (Pe(e))
    return Xe ? Xe.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -hn ? "-0" : t;
}
function H(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function Ct(e) {
  return e;
}
var yn = "[object AsyncFunction]", mn = "[object Function]", vn = "[object GeneratorFunction]", Tn = "[object Proxy]";
function It(e) {
  if (!H(e))
    return !1;
  var t = D(e);
  return t == mn || t == vn || t == yn || t == Tn;
}
var de = S["__core-js_shared__"], Je = function() {
  var e = /[^.]+$/.exec(de && de.keys && de.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function wn(e) {
  return !!Je && Je in e;
}
var On = Function.prototype, An = On.toString;
function U(e) {
  if (e != null) {
    try {
      return An.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var Pn = /[\\^$.*+?()[\]{}|]/g, $n = /^\[object .+?Constructor\]$/, Sn = Function.prototype, Cn = Object.prototype, In = Sn.toString, jn = Cn.hasOwnProperty, En = RegExp("^" + In.call(jn).replace(Pn, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function xn(e) {
  if (!H(e) || wn(e))
    return !1;
  var t = It(e) ? En : $n;
  return t.test(U(e));
}
function Mn(e, t) {
  return e == null ? void 0 : e[t];
}
function K(e, t) {
  var n = Mn(e, t);
  return xn(n) ? n : void 0;
}
var me = K(S, "WeakMap"), Ze = Object.create, Ln = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!H(t))
      return {};
    if (Ze)
      return Ze(t);
    e.prototype = t;
    var n = new e();
    return e.prototype = void 0, n;
  };
}();
function Fn(e, t, n) {
  switch (n.length) {
    case 0:
      return e.call(t);
    case 1:
      return e.call(t, n[0]);
    case 2:
      return e.call(t, n[0], n[1]);
    case 3:
      return e.call(t, n[0], n[1], n[2]);
  }
  return e.apply(t, n);
}
function Rn(e, t) {
  var n = -1, r = e.length;
  for (t || (t = Array(r)); ++n < r; )
    t[n] = e[n];
  return t;
}
var Nn = 800, Dn = 16, Un = Date.now;
function Kn(e) {
  var t = 0, n = 0;
  return function() {
    var r = Un(), o = Dn - (r - n);
    if (n = r, o > 0) {
      if (++t >= Nn)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function Gn(e) {
  return function() {
    return e;
  };
}
var ie = function() {
  try {
    var e = K(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), Bn = ie ? function(e, t) {
  return ie(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: Gn(t),
    writable: !0
  });
} : Ct, zn = Kn(Bn);
function Hn(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r && t(e[n], n, e) !== !1; )
    ;
  return e;
}
var qn = 9007199254740991, Yn = /^(?:0|[1-9]\d*)$/;
function jt(e, t) {
  var n = typeof e;
  return t = t ?? qn, !!t && (n == "number" || n != "symbol" && Yn.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function $e(e, t, n) {
  t == "__proto__" && ie ? ie(e, t, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : e[t] = n;
}
function Se(e, t) {
  return e === t || e !== e && t !== t;
}
var Xn = Object.prototype, Jn = Xn.hasOwnProperty;
function Et(e, t, n) {
  var r = e[t];
  (!(Jn.call(e, t) && Se(r, n)) || n === void 0 && !(t in e)) && $e(e, t, n);
}
function Q(e, t, n, r) {
  var o = !n;
  n || (n = {});
  for (var i = -1, s = t.length; ++i < s; ) {
    var a = t[i], c = void 0;
    c === void 0 && (c = e[a]), o ? $e(n, a, c) : Et(n, a, c);
  }
  return n;
}
var We = Math.max;
function Zn(e, t, n) {
  return t = We(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var r = arguments, o = -1, i = We(r.length - t, 0), s = Array(i); ++o < i; )
      s[o] = r[t + o];
    o = -1;
    for (var a = Array(t + 1); ++o < t; )
      a[o] = r[o];
    return a[t] = n(s), Fn(e, this, a);
  };
}
var Wn = 9007199254740991;
function Ce(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= Wn;
}
function xt(e) {
  return e != null && Ce(e.length) && !It(e);
}
var Qn = Object.prototype;
function Ie(e) {
  var t = e && e.constructor, n = typeof t == "function" && t.prototype || Qn;
  return e === n;
}
function Vn(e, t) {
  for (var n = -1, r = Array(e); ++n < e; )
    r[n] = t(n);
  return r;
}
var kn = "[object Arguments]";
function Qe(e) {
  return E(e) && D(e) == kn;
}
var Mt = Object.prototype, er = Mt.hasOwnProperty, tr = Mt.propertyIsEnumerable, je = Qe(/* @__PURE__ */ function() {
  return arguments;
}()) ? Qe : function(e) {
  return E(e) && er.call(e, "callee") && !tr.call(e, "callee");
};
function nr() {
  return !1;
}
var Lt = typeof exports == "object" && exports && !exports.nodeType && exports, Ve = Lt && typeof module == "object" && module && !module.nodeType && module, rr = Ve && Ve.exports === Lt, ke = rr ? S.Buffer : void 0, ir = ke ? ke.isBuffer : void 0, oe = ir || nr, or = "[object Arguments]", sr = "[object Array]", ar = "[object Boolean]", ur = "[object Date]", lr = "[object Error]", fr = "[object Function]", cr = "[object Map]", pr = "[object Number]", gr = "[object Object]", dr = "[object RegExp]", _r = "[object Set]", br = "[object String]", hr = "[object WeakMap]", yr = "[object ArrayBuffer]", mr = "[object DataView]", vr = "[object Float32Array]", Tr = "[object Float64Array]", wr = "[object Int8Array]", Or = "[object Int16Array]", Ar = "[object Int32Array]", Pr = "[object Uint8Array]", $r = "[object Uint8ClampedArray]", Sr = "[object Uint16Array]", Cr = "[object Uint32Array]", v = {};
v[vr] = v[Tr] = v[wr] = v[Or] = v[Ar] = v[Pr] = v[$r] = v[Sr] = v[Cr] = !0;
v[or] = v[sr] = v[yr] = v[ar] = v[mr] = v[ur] = v[lr] = v[fr] = v[cr] = v[pr] = v[gr] = v[dr] = v[_r] = v[br] = v[hr] = !1;
function Ir(e) {
  return E(e) && Ce(e.length) && !!v[D(e)];
}
function Ee(e) {
  return function(t) {
    return e(t);
  };
}
var Ft = typeof exports == "object" && exports && !exports.nodeType && exports, X = Ft && typeof module == "object" && module && !module.nodeType && module, jr = X && X.exports === Ft, _e = jr && At.process, z = function() {
  try {
    var e = X && X.require && X.require("util").types;
    return e || _e && _e.binding && _e.binding("util");
  } catch {
  }
}(), et = z && z.isTypedArray, Rt = et ? Ee(et) : Ir, Er = Object.prototype, xr = Er.hasOwnProperty;
function Nt(e, t) {
  var n = P(e), r = !n && je(e), o = !n && !r && oe(e), i = !n && !r && !o && Rt(e), s = n || r || o || i, a = s ? Vn(e.length, String) : [], c = a.length;
  for (var f in e)
    (t || xr.call(e, f)) && !(s && // Safari 9 has enumerable `arguments.length` in strict mode.
    (f == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    o && (f == "offset" || f == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    i && (f == "buffer" || f == "byteLength" || f == "byteOffset") || // Skip index properties.
    jt(f, c))) && a.push(f);
  return a;
}
function Dt(e, t) {
  return function(n) {
    return e(t(n));
  };
}
var Mr = Dt(Object.keys, Object), Lr = Object.prototype, Fr = Lr.hasOwnProperty;
function Rr(e) {
  if (!Ie(e))
    return Mr(e);
  var t = [];
  for (var n in Object(e))
    Fr.call(e, n) && n != "constructor" && t.push(n);
  return t;
}
function V(e) {
  return xt(e) ? Nt(e) : Rr(e);
}
function Nr(e) {
  var t = [];
  if (e != null)
    for (var n in Object(e))
      t.push(n);
  return t;
}
var Dr = Object.prototype, Ur = Dr.hasOwnProperty;
function Kr(e) {
  if (!H(e))
    return Nr(e);
  var t = Ie(e), n = [];
  for (var r in e)
    r == "constructor" && (t || !Ur.call(e, r)) || n.push(r);
  return n;
}
function xe(e) {
  return xt(e) ? Nt(e, !0) : Kr(e);
}
var Gr = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, Br = /^\w*$/;
function Me(e, t) {
  if (P(e))
    return !1;
  var n = typeof e;
  return n == "number" || n == "symbol" || n == "boolean" || e == null || Pe(e) ? !0 : Br.test(e) || !Gr.test(e) || t != null && e in Object(t);
}
var J = K(Object, "create");
function zr() {
  this.__data__ = J ? J(null) : {}, this.size = 0;
}
function Hr(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var qr = "__lodash_hash_undefined__", Yr = Object.prototype, Xr = Yr.hasOwnProperty;
function Jr(e) {
  var t = this.__data__;
  if (J) {
    var n = t[e];
    return n === qr ? void 0 : n;
  }
  return Xr.call(t, e) ? t[e] : void 0;
}
var Zr = Object.prototype, Wr = Zr.hasOwnProperty;
function Qr(e) {
  var t = this.__data__;
  return J ? t[e] !== void 0 : Wr.call(t, e);
}
var Vr = "__lodash_hash_undefined__";
function kr(e, t) {
  var n = this.__data__;
  return this.size += this.has(e) ? 0 : 1, n[e] = J && t === void 0 ? Vr : t, this;
}
function N(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
N.prototype.clear = zr;
N.prototype.delete = Hr;
N.prototype.get = Jr;
N.prototype.has = Qr;
N.prototype.set = kr;
function ei() {
  this.__data__ = [], this.size = 0;
}
function le(e, t) {
  for (var n = e.length; n--; )
    if (Se(e[n][0], t))
      return n;
  return -1;
}
var ti = Array.prototype, ni = ti.splice;
function ri(e) {
  var t = this.__data__, n = le(t, e);
  if (n < 0)
    return !1;
  var r = t.length - 1;
  return n == r ? t.pop() : ni.call(t, n, 1), --this.size, !0;
}
function ii(e) {
  var t = this.__data__, n = le(t, e);
  return n < 0 ? void 0 : t[n][1];
}
function oi(e) {
  return le(this.__data__, e) > -1;
}
function si(e, t) {
  var n = this.__data__, r = le(n, e);
  return r < 0 ? (++this.size, n.push([e, t])) : n[r][1] = t, this;
}
function x(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
x.prototype.clear = ei;
x.prototype.delete = ri;
x.prototype.get = ii;
x.prototype.has = oi;
x.prototype.set = si;
var Z = K(S, "Map");
function ai() {
  this.size = 0, this.__data__ = {
    hash: new N(),
    map: new (Z || x)(),
    string: new N()
  };
}
function ui(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function fe(e, t) {
  var n = e.__data__;
  return ui(t) ? n[typeof t == "string" ? "string" : "hash"] : n.map;
}
function li(e) {
  var t = fe(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function fi(e) {
  return fe(this, e).get(e);
}
function ci(e) {
  return fe(this, e).has(e);
}
function pi(e, t) {
  var n = fe(this, e), r = n.size;
  return n.set(e, t), this.size += n.size == r ? 0 : 1, this;
}
function M(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
M.prototype.clear = ai;
M.prototype.delete = li;
M.prototype.get = fi;
M.prototype.has = ci;
M.prototype.set = pi;
var gi = "Expected a function";
function Le(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(gi);
  var n = function() {
    var r = arguments, o = t ? t.apply(this, r) : r[0], i = n.cache;
    if (i.has(o))
      return i.get(o);
    var s = e.apply(this, r);
    return n.cache = i.set(o, s) || i, s;
  };
  return n.cache = new (Le.Cache || M)(), n;
}
Le.Cache = M;
var di = 500;
function _i(e) {
  var t = Le(e, function(r) {
    return n.size === di && n.clear(), r;
  }), n = t.cache;
  return t;
}
var bi = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, hi = /\\(\\)?/g, yi = _i(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(bi, function(n, r, o, i) {
    t.push(o ? i.replace(hi, "$1") : r || n);
  }), t;
});
function mi(e) {
  return e == null ? "" : St(e);
}
function ce(e, t) {
  return P(e) ? e : Me(e, t) ? [e] : yi(mi(e));
}
var vi = 1 / 0;
function k(e) {
  if (typeof e == "string" || Pe(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -vi ? "-0" : t;
}
function Fe(e, t) {
  t = ce(t, e);
  for (var n = 0, r = t.length; e != null && n < r; )
    e = e[k(t[n++])];
  return n && n == r ? e : void 0;
}
function Ti(e, t, n) {
  var r = e == null ? void 0 : Fe(e, t);
  return r === void 0 ? n : r;
}
function Re(e, t) {
  for (var n = -1, r = t.length, o = e.length; ++n < r; )
    e[o + n] = t[n];
  return e;
}
var tt = O ? O.isConcatSpreadable : void 0;
function wi(e) {
  return P(e) || je(e) || !!(tt && e && e[tt]);
}
function Oi(e, t, n, r, o) {
  var i = -1, s = e.length;
  for (n || (n = wi), o || (o = []); ++i < s; ) {
    var a = e[i];
    n(a) ? Re(o, a) : o[o.length] = a;
  }
  return o;
}
function Ai(e) {
  var t = e == null ? 0 : e.length;
  return t ? Oi(e) : [];
}
function Pi(e) {
  return zn(Zn(e, void 0, Ai), e + "");
}
var Ne = Dt(Object.getPrototypeOf, Object), $i = "[object Object]", Si = Function.prototype, Ci = Object.prototype, Ut = Si.toString, Ii = Ci.hasOwnProperty, ji = Ut.call(Object);
function Ei(e) {
  if (!E(e) || D(e) != $i)
    return !1;
  var t = Ne(e);
  if (t === null)
    return !0;
  var n = Ii.call(t, "constructor") && t.constructor;
  return typeof n == "function" && n instanceof n && Ut.call(n) == ji;
}
function xi(e, t, n) {
  var r = -1, o = e.length;
  t < 0 && (t = -t > o ? 0 : o + t), n = n > o ? o : n, n < 0 && (n += o), o = t > n ? 0 : n - t >>> 0, t >>>= 0;
  for (var i = Array(o); ++r < o; )
    i[r] = e[r + t];
  return i;
}
function Mi() {
  this.__data__ = new x(), this.size = 0;
}
function Li(e) {
  var t = this.__data__, n = t.delete(e);
  return this.size = t.size, n;
}
function Fi(e) {
  return this.__data__.get(e);
}
function Ri(e) {
  return this.__data__.has(e);
}
var Ni = 200;
function Di(e, t) {
  var n = this.__data__;
  if (n instanceof x) {
    var r = n.__data__;
    if (!Z || r.length < Ni - 1)
      return r.push([e, t]), this.size = ++n.size, this;
    n = this.__data__ = new M(r);
  }
  return n.set(e, t), this.size = n.size, this;
}
function $(e) {
  var t = this.__data__ = new x(e);
  this.size = t.size;
}
$.prototype.clear = Mi;
$.prototype.delete = Li;
$.prototype.get = Fi;
$.prototype.has = Ri;
$.prototype.set = Di;
function Ui(e, t) {
  return e && Q(t, V(t), e);
}
function Ki(e, t) {
  return e && Q(t, xe(t), e);
}
var Kt = typeof exports == "object" && exports && !exports.nodeType && exports, nt = Kt && typeof module == "object" && module && !module.nodeType && module, Gi = nt && nt.exports === Kt, rt = Gi ? S.Buffer : void 0, it = rt ? rt.allocUnsafe : void 0;
function Bi(e, t) {
  if (t)
    return e.slice();
  var n = e.length, r = it ? it(n) : new e.constructor(n);
  return e.copy(r), r;
}
function zi(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, o = 0, i = []; ++n < r; ) {
    var s = e[n];
    t(s, n, e) && (i[o++] = s);
  }
  return i;
}
function Gt() {
  return [];
}
var Hi = Object.prototype, qi = Hi.propertyIsEnumerable, ot = Object.getOwnPropertySymbols, De = ot ? function(e) {
  return e == null ? [] : (e = Object(e), zi(ot(e), function(t) {
    return qi.call(e, t);
  }));
} : Gt;
function Yi(e, t) {
  return Q(e, De(e), t);
}
var Xi = Object.getOwnPropertySymbols, Bt = Xi ? function(e) {
  for (var t = []; e; )
    Re(t, De(e)), e = Ne(e);
  return t;
} : Gt;
function Ji(e, t) {
  return Q(e, Bt(e), t);
}
function zt(e, t, n) {
  var r = t(e);
  return P(e) ? r : Re(r, n(e));
}
function ve(e) {
  return zt(e, V, De);
}
function Ht(e) {
  return zt(e, xe, Bt);
}
var Te = K(S, "DataView"), we = K(S, "Promise"), Oe = K(S, "Set"), st = "[object Map]", Zi = "[object Object]", at = "[object Promise]", ut = "[object Set]", lt = "[object WeakMap]", ft = "[object DataView]", Wi = U(Te), Qi = U(Z), Vi = U(we), ki = U(Oe), eo = U(me), A = D;
(Te && A(new Te(new ArrayBuffer(1))) != ft || Z && A(new Z()) != st || we && A(we.resolve()) != at || Oe && A(new Oe()) != ut || me && A(new me()) != lt) && (A = function(e) {
  var t = D(e), n = t == Zi ? e.constructor : void 0, r = n ? U(n) : "";
  if (r)
    switch (r) {
      case Wi:
        return ft;
      case Qi:
        return st;
      case Vi:
        return at;
      case ki:
        return ut;
      case eo:
        return lt;
    }
  return t;
});
var to = Object.prototype, no = to.hasOwnProperty;
function ro(e) {
  var t = e.length, n = new e.constructor(t);
  return t && typeof e[0] == "string" && no.call(e, "index") && (n.index = e.index, n.input = e.input), n;
}
var se = S.Uint8Array;
function Ue(e) {
  var t = new e.constructor(e.byteLength);
  return new se(t).set(new se(e)), t;
}
function io(e, t) {
  var n = t ? Ue(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.byteLength);
}
var oo = /\w*$/;
function so(e) {
  var t = new e.constructor(e.source, oo.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var ct = O ? O.prototype : void 0, pt = ct ? ct.valueOf : void 0;
function ao(e) {
  return pt ? Object(pt.call(e)) : {};
}
function uo(e, t) {
  var n = t ? Ue(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.length);
}
var lo = "[object Boolean]", fo = "[object Date]", co = "[object Map]", po = "[object Number]", go = "[object RegExp]", _o = "[object Set]", bo = "[object String]", ho = "[object Symbol]", yo = "[object ArrayBuffer]", mo = "[object DataView]", vo = "[object Float32Array]", To = "[object Float64Array]", wo = "[object Int8Array]", Oo = "[object Int16Array]", Ao = "[object Int32Array]", Po = "[object Uint8Array]", $o = "[object Uint8ClampedArray]", So = "[object Uint16Array]", Co = "[object Uint32Array]";
function Io(e, t, n) {
  var r = e.constructor;
  switch (t) {
    case yo:
      return Ue(e);
    case lo:
    case fo:
      return new r(+e);
    case mo:
      return io(e, n);
    case vo:
    case To:
    case wo:
    case Oo:
    case Ao:
    case Po:
    case $o:
    case So:
    case Co:
      return uo(e, n);
    case co:
      return new r();
    case po:
    case bo:
      return new r(e);
    case go:
      return so(e);
    case _o:
      return new r();
    case ho:
      return ao(e);
  }
}
function jo(e) {
  return typeof e.constructor == "function" && !Ie(e) ? Ln(Ne(e)) : {};
}
var Eo = "[object Map]";
function xo(e) {
  return E(e) && A(e) == Eo;
}
var gt = z && z.isMap, Mo = gt ? Ee(gt) : xo, Lo = "[object Set]";
function Fo(e) {
  return E(e) && A(e) == Lo;
}
var dt = z && z.isSet, Ro = dt ? Ee(dt) : Fo, No = 1, Do = 2, Uo = 4, qt = "[object Arguments]", Ko = "[object Array]", Go = "[object Boolean]", Bo = "[object Date]", zo = "[object Error]", Yt = "[object Function]", Ho = "[object GeneratorFunction]", qo = "[object Map]", Yo = "[object Number]", Xt = "[object Object]", Xo = "[object RegExp]", Jo = "[object Set]", Zo = "[object String]", Wo = "[object Symbol]", Qo = "[object WeakMap]", Vo = "[object ArrayBuffer]", ko = "[object DataView]", es = "[object Float32Array]", ts = "[object Float64Array]", ns = "[object Int8Array]", rs = "[object Int16Array]", is = "[object Int32Array]", os = "[object Uint8Array]", ss = "[object Uint8ClampedArray]", as = "[object Uint16Array]", us = "[object Uint32Array]", y = {};
y[qt] = y[Ko] = y[Vo] = y[ko] = y[Go] = y[Bo] = y[es] = y[ts] = y[ns] = y[rs] = y[is] = y[qo] = y[Yo] = y[Xt] = y[Xo] = y[Jo] = y[Zo] = y[Wo] = y[os] = y[ss] = y[as] = y[us] = !0;
y[zo] = y[Yt] = y[Qo] = !1;
function ne(e, t, n, r, o, i) {
  var s, a = t & No, c = t & Do, f = t & Uo;
  if (n && (s = o ? n(e, r, o, i) : n(e)), s !== void 0)
    return s;
  if (!H(e))
    return e;
  var p = P(e);
  if (p) {
    if (s = ro(e), !a)
      return Rn(e, s);
  } else {
    var d = A(e), b = d == Yt || d == Ho;
    if (oe(e))
      return Bi(e, a);
    if (d == Xt || d == qt || b && !o) {
      if (s = c || b ? {} : jo(e), !a)
        return c ? Ji(e, Ki(s, e)) : Yi(e, Ui(s, e));
    } else {
      if (!y[d])
        return o ? e : {};
      s = Io(e, d, a);
    }
  }
  i || (i = new $());
  var h = i.get(e);
  if (h)
    return h;
  i.set(e, s), Ro(e) ? e.forEach(function(l) {
    s.add(ne(l, t, n, l, e, i));
  }) : Mo(e) && e.forEach(function(l, m) {
    s.set(m, ne(l, t, n, m, e, i));
  });
  var u = f ? c ? Ht : ve : c ? xe : V, g = p ? void 0 : u(e);
  return Hn(g || e, function(l, m) {
    g && (m = l, l = e[m]), Et(s, m, ne(l, t, n, m, e, i));
  }), s;
}
var ls = "__lodash_hash_undefined__";
function fs(e) {
  return this.__data__.set(e, ls), this;
}
function cs(e) {
  return this.__data__.has(e);
}
function ae(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.__data__ = new M(); ++t < n; )
    this.add(e[t]);
}
ae.prototype.add = ae.prototype.push = fs;
ae.prototype.has = cs;
function ps(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r; )
    if (t(e[n], n, e))
      return !0;
  return !1;
}
function gs(e, t) {
  return e.has(t);
}
var ds = 1, _s = 2;
function Jt(e, t, n, r, o, i) {
  var s = n & ds, a = e.length, c = t.length;
  if (a != c && !(s && c > a))
    return !1;
  var f = i.get(e), p = i.get(t);
  if (f && p)
    return f == t && p == e;
  var d = -1, b = !0, h = n & _s ? new ae() : void 0;
  for (i.set(e, t), i.set(t, e); ++d < a; ) {
    var u = e[d], g = t[d];
    if (r)
      var l = s ? r(g, u, d, t, e, i) : r(u, g, d, e, t, i);
    if (l !== void 0) {
      if (l)
        continue;
      b = !1;
      break;
    }
    if (h) {
      if (!ps(t, function(m, w) {
        if (!gs(h, w) && (u === m || o(u, m, n, r, i)))
          return h.push(w);
      })) {
        b = !1;
        break;
      }
    } else if (!(u === g || o(u, g, n, r, i))) {
      b = !1;
      break;
    }
  }
  return i.delete(e), i.delete(t), b;
}
function bs(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r, o) {
    n[++t] = [o, r];
  }), n;
}
function hs(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r) {
    n[++t] = r;
  }), n;
}
var ys = 1, ms = 2, vs = "[object Boolean]", Ts = "[object Date]", ws = "[object Error]", Os = "[object Map]", As = "[object Number]", Ps = "[object RegExp]", $s = "[object Set]", Ss = "[object String]", Cs = "[object Symbol]", Is = "[object ArrayBuffer]", js = "[object DataView]", _t = O ? O.prototype : void 0, be = _t ? _t.valueOf : void 0;
function Es(e, t, n, r, o, i, s) {
  switch (n) {
    case js:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case Is:
      return !(e.byteLength != t.byteLength || !i(new se(e), new se(t)));
    case vs:
    case Ts:
    case As:
      return Se(+e, +t);
    case ws:
      return e.name == t.name && e.message == t.message;
    case Ps:
    case Ss:
      return e == t + "";
    case Os:
      var a = bs;
    case $s:
      var c = r & ys;
      if (a || (a = hs), e.size != t.size && !c)
        return !1;
      var f = s.get(e);
      if (f)
        return f == t;
      r |= ms, s.set(e, t);
      var p = Jt(a(e), a(t), r, o, i, s);
      return s.delete(e), p;
    case Cs:
      if (be)
        return be.call(e) == be.call(t);
  }
  return !1;
}
var xs = 1, Ms = Object.prototype, Ls = Ms.hasOwnProperty;
function Fs(e, t, n, r, o, i) {
  var s = n & xs, a = ve(e), c = a.length, f = ve(t), p = f.length;
  if (c != p && !s)
    return !1;
  for (var d = c; d--; ) {
    var b = a[d];
    if (!(s ? b in t : Ls.call(t, b)))
      return !1;
  }
  var h = i.get(e), u = i.get(t);
  if (h && u)
    return h == t && u == e;
  var g = !0;
  i.set(e, t), i.set(t, e);
  for (var l = s; ++d < c; ) {
    b = a[d];
    var m = e[b], w = t[b];
    if (r)
      var F = s ? r(w, m, b, t, e, i) : r(m, w, b, e, t, i);
    if (!(F === void 0 ? m === w || o(m, w, n, r, i) : F)) {
      g = !1;
      break;
    }
    l || (l = b == "constructor");
  }
  if (g && !l) {
    var C = e.constructor, I = t.constructor;
    C != I && "constructor" in e && "constructor" in t && !(typeof C == "function" && C instanceof C && typeof I == "function" && I instanceof I) && (g = !1);
  }
  return i.delete(e), i.delete(t), g;
}
var Rs = 1, bt = "[object Arguments]", ht = "[object Array]", te = "[object Object]", Ns = Object.prototype, yt = Ns.hasOwnProperty;
function Ds(e, t, n, r, o, i) {
  var s = P(e), a = P(t), c = s ? ht : A(e), f = a ? ht : A(t);
  c = c == bt ? te : c, f = f == bt ? te : f;
  var p = c == te, d = f == te, b = c == f;
  if (b && oe(e)) {
    if (!oe(t))
      return !1;
    s = !0, p = !1;
  }
  if (b && !p)
    return i || (i = new $()), s || Rt(e) ? Jt(e, t, n, r, o, i) : Es(e, t, c, n, r, o, i);
  if (!(n & Rs)) {
    var h = p && yt.call(e, "__wrapped__"), u = d && yt.call(t, "__wrapped__");
    if (h || u) {
      var g = h ? e.value() : e, l = u ? t.value() : t;
      return i || (i = new $()), o(g, l, n, r, i);
    }
  }
  return b ? (i || (i = new $()), Fs(e, t, n, r, o, i)) : !1;
}
function Ke(e, t, n, r, o) {
  return e === t ? !0 : e == null || t == null || !E(e) && !E(t) ? e !== e && t !== t : Ds(e, t, n, r, Ke, o);
}
var Us = 1, Ks = 2;
function Gs(e, t, n, r) {
  var o = n.length, i = o;
  if (e == null)
    return !i;
  for (e = Object(e); o--; ) {
    var s = n[o];
    if (s[2] ? s[1] !== e[s[0]] : !(s[0] in e))
      return !1;
  }
  for (; ++o < i; ) {
    s = n[o];
    var a = s[0], c = e[a], f = s[1];
    if (s[2]) {
      if (c === void 0 && !(a in e))
        return !1;
    } else {
      var p = new $(), d;
      if (!(d === void 0 ? Ke(f, c, Us | Ks, r, p) : d))
        return !1;
    }
  }
  return !0;
}
function Zt(e) {
  return e === e && !H(e);
}
function Bs(e) {
  for (var t = V(e), n = t.length; n--; ) {
    var r = t[n], o = e[r];
    t[n] = [r, o, Zt(o)];
  }
  return t;
}
function Wt(e, t) {
  return function(n) {
    return n == null ? !1 : n[e] === t && (t !== void 0 || e in Object(n));
  };
}
function zs(e) {
  var t = Bs(e);
  return t.length == 1 && t[0][2] ? Wt(t[0][0], t[0][1]) : function(n) {
    return n === e || Gs(n, e, t);
  };
}
function Hs(e, t) {
  return e != null && t in Object(e);
}
function qs(e, t, n) {
  t = ce(t, e);
  for (var r = -1, o = t.length, i = !1; ++r < o; ) {
    var s = k(t[r]);
    if (!(i = e != null && n(e, s)))
      break;
    e = e[s];
  }
  return i || ++r != o ? i : (o = e == null ? 0 : e.length, !!o && Ce(o) && jt(s, o) && (P(e) || je(e)));
}
function Ys(e, t) {
  return e != null && qs(e, t, Hs);
}
var Xs = 1, Js = 2;
function Zs(e, t) {
  return Me(e) && Zt(t) ? Wt(k(e), t) : function(n) {
    var r = Ti(n, e);
    return r === void 0 && r === t ? Ys(n, e) : Ke(t, r, Xs | Js);
  };
}
function Ws(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function Qs(e) {
  return function(t) {
    return Fe(t, e);
  };
}
function Vs(e) {
  return Me(e) ? Ws(k(e)) : Qs(e);
}
function ks(e) {
  return typeof e == "function" ? e : e == null ? Ct : typeof e == "object" ? P(e) ? Zs(e[0], e[1]) : zs(e) : Vs(e);
}
function ea(e) {
  return function(t, n, r) {
    for (var o = -1, i = Object(t), s = r(t), a = s.length; a--; ) {
      var c = s[++o];
      if (n(i[c], c, i) === !1)
        break;
    }
    return t;
  };
}
var ta = ea();
function na(e, t) {
  return e && ta(e, t, V);
}
function ra(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function ia(e, t) {
  return t.length < 2 ? e : Fe(e, xi(t, 0, -1));
}
function oa(e) {
  return e === void 0;
}
function sa(e, t) {
  var n = {};
  return t = ks(t), na(e, function(r, o, i) {
    $e(n, t(r, o, i), r);
  }), n;
}
function aa(e, t) {
  return t = ce(t, e), e = ia(e, t), e == null || delete e[k(ra(t))];
}
function ua(e) {
  return Ei(e) ? void 0 : e;
}
var la = 1, fa = 2, ca = 4, Qt = Pi(function(e, t) {
  var n = {};
  if (e == null)
    return n;
  var r = !1;
  t = $t(t, function(i) {
    return i = ce(i, e), r || (r = i.length > 1), i;
  }), Q(e, Ht(e), n), r && (n = ne(n, la | fa | ca, ua));
  for (var o = t.length; o--; )
    aa(n, t[o]);
  return n;
});
async function pa() {
  window.ms_globals || (window.ms_globals = {}), window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function ga(e) {
  return await pa(), e().then((t) => t.default);
}
function da(e) {
  return e.replace(/(^|_)(\w)/g, (t, n, r, o) => o === 0 ? r.toLowerCase() : r.toUpperCase());
}
const Vt = ["interactive", "gradio", "server", "target", "theme_mode", "root", "name", "visible", "elem_id", "elem_classes", "elem_style", "_internal", "props", "value", "_selectable", "attached_events", "loading_status", "value_is_output"];
function _a(e, t = {}) {
  return sa(Qt(e, Vt), (n, r) => t[r] || da(r));
}
function mt(e) {
  const {
    gradio: t,
    _internal: n,
    restProps: r,
    originalRestProps: o,
    ...i
  } = e;
  return Object.keys(n).reduce((s, a) => {
    const c = a.match(/bind_(.+)_event/);
    if (c) {
      const f = c[1], p = f.split("_"), d = (...h) => {
        const u = h.map((l) => h && typeof l == "object" && (l.nativeEvent || l instanceof Event) ? {
          type: l.type,
          detail: l.detail,
          timestamp: l.timeStamp,
          clientX: l.clientX,
          clientY: l.clientY,
          targetId: l.target.id,
          targetClassName: l.target.className,
          altKey: l.altKey,
          ctrlKey: l.ctrlKey,
          shiftKey: l.shiftKey,
          metaKey: l.metaKey
        } : l);
        let g;
        try {
          g = JSON.parse(JSON.stringify(u));
        } catch {
          g = u.map((l) => l && typeof l == "object" ? Object.fromEntries(Object.entries(l).filter(([, m]) => {
            try {
              return JSON.stringify(m), !0;
            } catch {
              return !1;
            }
          })) : l);
        }
        return t.dispatch(f.replace(/[A-Z]/g, (l) => "_" + l.toLowerCase()), {
          payload: g,
          component: {
            ...i,
            ...Qt(o, Vt)
          }
        });
      };
      if (p.length > 1) {
        let h = {
          ...i.props[p[0]] || (r == null ? void 0 : r[p[0]]) || {}
        };
        s[p[0]] = h;
        for (let g = 1; g < p.length - 1; g++) {
          const l = {
            ...i.props[p[g]] || (r == null ? void 0 : r[p[g]]) || {}
          };
          h[p[g]] = l, h = l;
        }
        const u = p[p.length - 1];
        return h[`on${u.slice(0, 1).toUpperCase()}${u.slice(1)}`] = d, s;
      }
      const b = p[0];
      s[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = d;
    }
    return s;
  }, {});
}
function re() {
}
function ba(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function ha(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return re;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function R(e) {
  let t;
  return ha(e, (n) => t = n)(), t;
}
const G = [];
function L(e, t = re) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function o(a) {
    if (ba(e, a) && (e = a, n)) {
      const c = !G.length;
      for (const f of r)
        f[1](), G.push(f, e);
      if (c) {
        for (let f = 0; f < G.length; f += 2)
          G[f][0](G[f + 1]);
        G.length = 0;
      }
    }
  }
  function i(a) {
    o(a(e));
  }
  function s(a, c = re) {
    const f = [a, c];
    return r.add(f), r.size === 1 && (n = t(o, i) || re), a(e), () => {
      r.delete(f), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: o,
    update: i,
    subscribe: s
  };
}
const {
  getContext: ya,
  setContext: iu
} = window.__gradio__svelte__internal, ma = "$$ms-gr-loading-status-key";
function va() {
  const e = window.ms_globals.loadingKey++, t = ya(ma);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: r,
      options: o
    } = t, {
      generating: i,
      error: s
    } = R(o);
    (n == null ? void 0 : n.status) === "pending" || s && (n == null ? void 0 : n.status) === "error" || (i && (n == null ? void 0 : n.status)) === "generating" ? r.update(({
      map: a
    }) => (a.set(e, n), {
      map: a
    })) : r.update(({
      map: a
    }) => (a.delete(e), {
      map: a
    }));
  };
}
const {
  getContext: pe,
  setContext: ge
} = window.__gradio__svelte__internal, Ta = "$$ms-gr-slots-key";
function wa() {
  const e = L({});
  return ge(Ta, e);
}
const Oa = "$$ms-gr-context-key";
function he(e) {
  return oa(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const kt = "$$ms-gr-sub-index-context-key";
function Aa() {
  return pe(kt) || null;
}
function vt(e) {
  return ge(kt, e);
}
function Pa(e, t, n) {
  var b, h;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = Sa(), o = Ca({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), i = Aa();
  typeof i == "number" && vt(void 0);
  const s = va();
  typeof e._internal.subIndex == "number" && vt(e._internal.subIndex), r && r.subscribe((u) => {
    o.slotKey.set(u);
  }), $a();
  const a = pe(Oa), c = ((b = R(a)) == null ? void 0 : b.as_item) || e.as_item, f = he(a ? c ? ((h = R(a)) == null ? void 0 : h[c]) || {} : R(a) || {} : {}), p = (u, g) => u ? _a({
    ...u,
    ...g || {}
  }, t) : void 0, d = L({
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
      as_item: g
    } = R(d);
    g && (u = u == null ? void 0 : u[g]), u = he(u), d.update((l) => ({
      ...l,
      ...u || {},
      restProps: p(l.restProps, u)
    }));
  }), [d, (u) => {
    var l, m;
    const g = he(u.as_item ? ((l = R(a)) == null ? void 0 : l[u.as_item]) || {} : R(a) || {});
    return s((m = u.restProps) == null ? void 0 : m.loading_status), d.set({
      ...u,
      _internal: {
        ...u._internal,
        index: i ?? u._internal.index
      },
      ...g,
      restProps: p(u.restProps, g),
      originalRestProps: u.restProps
    });
  }]) : [d, (u) => {
    var g;
    s((g = u.restProps) == null ? void 0 : g.loading_status), d.set({
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
const en = "$$ms-gr-slot-key";
function $a() {
  ge(en, L(void 0));
}
function Sa() {
  return pe(en);
}
const tn = "$$ms-gr-component-slot-context-key";
function Ca({
  slot: e,
  index: t,
  subIndex: n
}) {
  return ge(tn, {
    slotKey: L(e),
    slotIndex: L(t),
    subSlotIndex: L(n)
  });
}
function ou() {
  return pe(tn);
}
function Ia(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var nn = {
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
    function n() {
      for (var i = "", s = 0; s < arguments.length; s++) {
        var a = arguments[s];
        a && (i = o(i, r(a)));
      }
      return i;
    }
    function r(i) {
      if (typeof i == "string" || typeof i == "number")
        return i;
      if (typeof i != "object")
        return "";
      if (Array.isArray(i))
        return n.apply(null, i);
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
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(nn);
var ja = nn.exports;
const Tt = /* @__PURE__ */ Ia(ja), {
  getContext: Ea,
  setContext: xa
} = window.__gradio__svelte__internal;
function Ma(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(o = ["default"]) {
    const i = o.reduce((s, a) => (s[a] = L([]), s), {});
    return xa(t, {
      itemsMap: i,
      allowedSlots: o
    }), i;
  }
  function r() {
    const {
      itemsMap: o,
      allowedSlots: i
    } = Ea(t);
    return function(s, a, c) {
      o && (s ? o[s].update((f) => {
        const p = [...f];
        return i.includes(s) ? p[a] = c : p[a] = void 0, p;
      }) : i.includes("default") && o.default.update((f) => {
        const p = [...f];
        return p[a] = c, p;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: r
  };
}
const {
  getItems: La,
  getSetItemFn: su
} = Ma("descriptions"), {
  SvelteComponent: Fa,
  assign: Ae,
  check_outros: Ra,
  claim_component: Na,
  component_subscribe: Y,
  compute_rest_props: wt,
  create_component: Da,
  create_slot: Ua,
  destroy_component: Ka,
  detach: rn,
  empty: ue,
  exclude_internal_props: Ga,
  flush: j,
  get_all_dirty_from_scope: Ba,
  get_slot_changes: za,
  get_spread_object: ye,
  get_spread_update: Ha,
  group_outros: qa,
  handle_promise: Ya,
  init: Xa,
  insert_hydration: on,
  mount_component: Ja,
  noop: T,
  safe_not_equal: Za,
  transition_in: B,
  transition_out: W,
  update_await_block_branch: Wa,
  update_slot_base: Qa
} = window.__gradio__svelte__internal;
function Ot(e) {
  let t, n, r = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: tu,
    then: ka,
    catch: Va,
    value: 24,
    blocks: [, , ,]
  };
  return Ya(
    /*AwaitedDescriptions*/
    e[4],
    r
  ), {
    c() {
      t = ue(), r.block.c();
    },
    l(o) {
      t = ue(), r.block.l(o);
    },
    m(o, i) {
      on(o, t, i), r.block.m(o, r.anchor = i), r.mount = () => t.parentNode, r.anchor = t, n = !0;
    },
    p(o, i) {
      e = o, Wa(r, e, i);
    },
    i(o) {
      n || (B(r.block), n = !0);
    },
    o(o) {
      for (let i = 0; i < 3; i += 1) {
        const s = r.blocks[i];
        W(s);
      }
      n = !1;
    },
    d(o) {
      o && rn(t), r.block.d(o), r.token = null, r = null;
    }
  };
}
function Va(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function ka(e) {
  let t, n;
  const r = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: Tt(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-descriptions"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].restProps,
    /*$mergedProps*/
    e[0].props,
    mt(
      /*$mergedProps*/
      e[0]
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    },
    {
      title: (
        /*$mergedProps*/
        e[0].props.title || /*$mergedProps*/
        e[0].title
      )
    },
    {
      slotItems: (
        /*$items*/
        e[2].length > 0 ? (
          /*$items*/
          e[2]
        ) : (
          /*$children*/
          e[3]
        )
      )
    }
  ];
  let o = {
    $$slots: {
      default: [eu]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let i = 0; i < r.length; i += 1)
    o = Ae(o, r[i]);
  return t = new /*Descriptions*/
  e[24]({
    props: o
  }), {
    c() {
      Da(t.$$.fragment);
    },
    l(i) {
      Na(t.$$.fragment, i);
    },
    m(i, s) {
      Ja(t, i, s), n = !0;
    },
    p(i, s) {
      const a = s & /*$mergedProps, $slots, $items, $children*/
      15 ? Ha(r, [s & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          i[0].elem_style
        )
      }, s & /*$mergedProps*/
      1 && {
        className: Tt(
          /*$mergedProps*/
          i[0].elem_classes,
          "ms-gr-antd-descriptions"
        )
      }, s & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          i[0].elem_id
        )
      }, s & /*$mergedProps*/
      1 && ye(
        /*$mergedProps*/
        i[0].restProps
      ), s & /*$mergedProps*/
      1 && ye(
        /*$mergedProps*/
        i[0].props
      ), s & /*$mergedProps*/
      1 && ye(mt(
        /*$mergedProps*/
        i[0]
      )), s & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          i[1]
        )
      }, s & /*$mergedProps*/
      1 && {
        title: (
          /*$mergedProps*/
          i[0].props.title || /*$mergedProps*/
          i[0].title
        )
      }, s & /*$items, $children*/
      12 && {
        slotItems: (
          /*$items*/
          i[2].length > 0 ? (
            /*$items*/
            i[2]
          ) : (
            /*$children*/
            i[3]
          )
        )
      }]) : {};
      s & /*$$scope*/
      2097152 && (a.$$scope = {
        dirty: s,
        ctx: i
      }), t.$set(a);
    },
    i(i) {
      n || (B(t.$$.fragment, i), n = !0);
    },
    o(i) {
      W(t.$$.fragment, i), n = !1;
    },
    d(i) {
      Ka(t, i);
    }
  };
}
function eu(e) {
  let t;
  const n = (
    /*#slots*/
    e[20].default
  ), r = Ua(
    n,
    e,
    /*$$scope*/
    e[21],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(o) {
      r && r.l(o);
    },
    m(o, i) {
      r && r.m(o, i), t = !0;
    },
    p(o, i) {
      r && r.p && (!t || i & /*$$scope*/
      2097152) && Qa(
        r,
        n,
        o,
        /*$$scope*/
        o[21],
        t ? za(
          n,
          /*$$scope*/
          o[21],
          i,
          null
        ) : Ba(
          /*$$scope*/
          o[21]
        ),
        null
      );
    },
    i(o) {
      t || (B(r, o), t = !0);
    },
    o(o) {
      W(r, o), t = !1;
    },
    d(o) {
      r && r.d(o);
    }
  };
}
function tu(e) {
  return {
    c: T,
    l: T,
    m: T,
    p: T,
    i: T,
    o: T,
    d: T
  };
}
function nu(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[0].visible && Ot(e)
  );
  return {
    c() {
      r && r.c(), t = ue();
    },
    l(o) {
      r && r.l(o), t = ue();
    },
    m(o, i) {
      r && r.m(o, i), on(o, t, i), n = !0;
    },
    p(o, [i]) {
      /*$mergedProps*/
      o[0].visible ? r ? (r.p(o, i), i & /*$mergedProps*/
      1 && B(r, 1)) : (r = Ot(o), r.c(), B(r, 1), r.m(t.parentNode, t)) : r && (qa(), W(r, 1, 1, () => {
        r = null;
      }), Ra());
    },
    i(o) {
      n || (B(r), n = !0);
    },
    o(o) {
      W(r), n = !1;
    },
    d(o) {
      o && rn(t), r && r.d(o);
    }
  };
}
function ru(e, t, n) {
  const r = ["gradio", "props", "_internal", "title", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = wt(t, r), i, s, a, c, f, {
    $$slots: p = {},
    $$scope: d
  } = t;
  const b = ga(() => import("./descriptions-ZPMjMqKz.js"));
  let {
    gradio: h
  } = t, {
    props: u = {}
  } = t;
  const g = L(u);
  Y(e, g, (_) => n(19, i = _));
  let {
    _internal: l = {}
  } = t, {
    title: m
  } = t, {
    as_item: w
  } = t, {
    visible: F = !0
  } = t, {
    elem_id: C = ""
  } = t, {
    elem_classes: I = []
  } = t, {
    elem_style: ee = {}
  } = t;
  const [Ge, sn] = Pa({
    gradio: h,
    props: i,
    _internal: l,
    visible: F,
    elem_id: C,
    elem_classes: I,
    elem_style: ee,
    as_item: w,
    title: m,
    restProps: o
  });
  Y(e, Ge, (_) => n(0, s = _));
  const Be = wa();
  Y(e, Be, (_) => n(1, a = _));
  const {
    items: ze,
    default: He
  } = La(["default", "items"]);
  return Y(e, ze, (_) => n(2, c = _)), Y(e, He, (_) => n(3, f = _)), e.$$set = (_) => {
    t = Ae(Ae({}, t), Ga(_)), n(23, o = wt(t, r)), "gradio" in _ && n(10, h = _.gradio), "props" in _ && n(11, u = _.props), "_internal" in _ && n(12, l = _._internal), "title" in _ && n(13, m = _.title), "as_item" in _ && n(14, w = _.as_item), "visible" in _ && n(15, F = _.visible), "elem_id" in _ && n(16, C = _.elem_id), "elem_classes" in _ && n(17, I = _.elem_classes), "elem_style" in _ && n(18, ee = _.elem_style), "$$scope" in _ && n(21, d = _.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    2048 && g.update((_) => ({
      ..._,
      ...u
    })), sn({
      gradio: h,
      props: i,
      _internal: l,
      visible: F,
      elem_id: C,
      elem_classes: I,
      elem_style: ee,
      as_item: w,
      title: m,
      restProps: o
    });
  }, [s, a, c, f, b, g, Ge, Be, ze, He, h, u, l, m, w, F, C, I, ee, i, p, d];
}
class au extends Fa {
  constructor(t) {
    super(), Xa(this, t, ru, nu, Za, {
      gradio: 10,
      props: 11,
      _internal: 12,
      title: 13,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
    });
  }
  get gradio() {
    return this.$$.ctx[10];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), j();
  }
  get props() {
    return this.$$.ctx[11];
  }
  set props(t) {
    this.$$set({
      props: t
    }), j();
  }
  get _internal() {
    return this.$$.ctx[12];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), j();
  }
  get title() {
    return this.$$.ctx[13];
  }
  set title(t) {
    this.$$set({
      title: t
    }), j();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), j();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), j();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), j();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), j();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), j();
  }
}
export {
  au as I,
  ou as g,
  L as w
};
