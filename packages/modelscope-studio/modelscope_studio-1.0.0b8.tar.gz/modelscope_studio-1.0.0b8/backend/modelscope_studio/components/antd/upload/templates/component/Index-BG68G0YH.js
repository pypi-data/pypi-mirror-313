var hn = Object.defineProperty;
var Ye = (e) => {
  throw TypeError(e);
};
var bn = (e, t, n) => t in e ? hn(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var P = (e, t, n) => bn(e, typeof t != "symbol" ? t + "" : t, n), Xe = (e, t, n) => t.has(e) || Ye("Cannot " + n);
var B = (e, t, n) => (Xe(e, t, "read from private field"), n ? n.call(e) : t.get(e)), Je = (e, t, n) => t.has(e) ? Ye("Cannot add the same private member more than once") : t instanceof WeakSet ? t.add(e) : t.set(e, n), We = (e, t, n, r) => (Xe(e, t, "write to private field"), r ? r.call(e, n) : t.set(e, n), n);
var xt = typeof global == "object" && global && global.Object === Object && global, yn = typeof self == "object" && self && self.Object === Object && self, x = xt || yn || Function("return this")(), O = x.Symbol, jt = Object.prototype, mn = jt.hasOwnProperty, vn = jt.toString, J = O ? O.toStringTag : void 0;
function Tn(e) {
  var t = mn.call(e, J), n = e[J];
  try {
    e[J] = void 0;
    var r = !0;
  } catch {
  }
  var o = vn.call(e);
  return r && (t ? e[J] = n : delete e[J]), o;
}
var wn = Object.prototype, On = wn.toString;
function Pn(e) {
  return On.call(e);
}
var An = "[object Null]", $n = "[object Undefined]", Ze = O ? O.toStringTag : void 0;
function U(e) {
  return e == null ? e === void 0 ? $n : An : Ze && Ze in Object(e) ? Tn(e) : Pn(e);
}
function L(e) {
  return e != null && typeof e == "object";
}
var Sn = "[object Symbol]";
function Ce(e) {
  return typeof e == "symbol" || L(e) && U(e) == Sn;
}
function It(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, o = Array(r); ++n < r; )
    o[n] = t(e[n], n, e);
  return o;
}
var $ = Array.isArray, Cn = 1 / 0, Qe = O ? O.prototype : void 0, Ve = Qe ? Qe.toString : void 0;
function Et(e) {
  if (typeof e == "string")
    return e;
  if ($(e))
    return It(e, Et) + "";
  if (Ce(e))
    return Ve ? Ve.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -Cn ? "-0" : t;
}
function X(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function Lt(e) {
  return e;
}
var xn = "[object AsyncFunction]", jn = "[object Function]", In = "[object GeneratorFunction]", En = "[object Proxy]";
function Rt(e) {
  if (!X(e))
    return !1;
  var t = U(e);
  return t == jn || t == In || t == xn || t == En;
}
var he = x["__core-js_shared__"], ke = function() {
  var e = /[^.]+$/.exec(he && he.keys && he.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function Ln(e) {
  return !!ke && ke in e;
}
var Rn = Function.prototype, Fn = Rn.toString;
function G(e) {
  if (e != null) {
    try {
      return Fn.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var Mn = /[\\^$.*+?()[\]{}|]/g, Nn = /^\[object .+?Constructor\]$/, Dn = Function.prototype, Kn = Object.prototype, Un = Dn.toString, Gn = Kn.hasOwnProperty, zn = RegExp("^" + Un.call(Gn).replace(Mn, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function Bn(e) {
  if (!X(e) || Ln(e))
    return !1;
  var t = Rt(e) ? zn : Nn;
  return t.test(G(e));
}
function Hn(e, t) {
  return e == null ? void 0 : e[t];
}
function z(e, t) {
  var n = Hn(e, t);
  return Bn(n) ? n : void 0;
}
var we = z(x, "WeakMap"), et = Object.create, qn = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!X(t))
      return {};
    if (et)
      return et(t);
    e.prototype = t;
    var n = new e();
    return e.prototype = void 0, n;
  };
}();
function Yn(e, t, n) {
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
function Xn(e, t) {
  var n = -1, r = e.length;
  for (t || (t = Array(r)); ++n < r; )
    t[n] = e[n];
  return t;
}
var Jn = 800, Wn = 16, Zn = Date.now;
function Qn(e) {
  var t = 0, n = 0;
  return function() {
    var r = Zn(), o = Wn - (r - n);
    if (n = r, o > 0) {
      if (++t >= Jn)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function Vn(e) {
  return function() {
    return e;
  };
}
var se = function() {
  try {
    var e = z(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), kn = se ? function(e, t) {
  return se(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: Vn(t),
    writable: !0
  });
} : Lt, er = Qn(kn);
function tr(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r && t(e[n], n, e) !== !1; )
    ;
  return e;
}
var nr = 9007199254740991, rr = /^(?:0|[1-9]\d*)$/;
function Ft(e, t) {
  var n = typeof e;
  return t = t ?? nr, !!t && (n == "number" || n != "symbol" && rr.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function xe(e, t, n) {
  t == "__proto__" && se ? se(e, t, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : e[t] = n;
}
function je(e, t) {
  return e === t || e !== e && t !== t;
}
var ir = Object.prototype, or = ir.hasOwnProperty;
function Mt(e, t, n) {
  var r = e[t];
  (!(or.call(e, t) && je(r, n)) || n === void 0 && !(t in e)) && xe(e, t, n);
}
function k(e, t, n, r) {
  var o = !n;
  n || (n = {});
  for (var i = -1, s = t.length; ++i < s; ) {
    var a = t[i], c = void 0;
    c === void 0 && (c = e[a]), o ? xe(n, a, c) : Mt(n, a, c);
  }
  return n;
}
var tt = Math.max;
function sr(e, t, n) {
  return t = tt(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var r = arguments, o = -1, i = tt(r.length - t, 0), s = Array(i); ++o < i; )
      s[o] = r[t + o];
    o = -1;
    for (var a = Array(t + 1); ++o < t; )
      a[o] = r[o];
    return a[t] = n(s), Yn(e, this, a);
  };
}
var ar = 9007199254740991;
function Ie(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= ar;
}
function Nt(e) {
  return e != null && Ie(e.length) && !Rt(e);
}
var ur = Object.prototype;
function Ee(e) {
  var t = e && e.constructor, n = typeof t == "function" && t.prototype || ur;
  return e === n;
}
function lr(e, t) {
  for (var n = -1, r = Array(e); ++n < e; )
    r[n] = t(n);
  return r;
}
var fr = "[object Arguments]";
function nt(e) {
  return L(e) && U(e) == fr;
}
var Dt = Object.prototype, cr = Dt.hasOwnProperty, pr = Dt.propertyIsEnumerable, Le = nt(/* @__PURE__ */ function() {
  return arguments;
}()) ? nt : function(e) {
  return L(e) && cr.call(e, "callee") && !pr.call(e, "callee");
};
function gr() {
  return !1;
}
var Kt = typeof exports == "object" && exports && !exports.nodeType && exports, rt = Kt && typeof module == "object" && module && !module.nodeType && module, dr = rt && rt.exports === Kt, it = dr ? x.Buffer : void 0, _r = it ? it.isBuffer : void 0, ae = _r || gr, hr = "[object Arguments]", br = "[object Array]", yr = "[object Boolean]", mr = "[object Date]", vr = "[object Error]", Tr = "[object Function]", wr = "[object Map]", Or = "[object Number]", Pr = "[object Object]", Ar = "[object RegExp]", $r = "[object Set]", Sr = "[object String]", Cr = "[object WeakMap]", xr = "[object ArrayBuffer]", jr = "[object DataView]", Ir = "[object Float32Array]", Er = "[object Float64Array]", Lr = "[object Int8Array]", Rr = "[object Int16Array]", Fr = "[object Int32Array]", Mr = "[object Uint8Array]", Nr = "[object Uint8ClampedArray]", Dr = "[object Uint16Array]", Kr = "[object Uint32Array]", v = {};
v[Ir] = v[Er] = v[Lr] = v[Rr] = v[Fr] = v[Mr] = v[Nr] = v[Dr] = v[Kr] = !0;
v[hr] = v[br] = v[xr] = v[yr] = v[jr] = v[mr] = v[vr] = v[Tr] = v[wr] = v[Or] = v[Pr] = v[Ar] = v[$r] = v[Sr] = v[Cr] = !1;
function Ur(e) {
  return L(e) && Ie(e.length) && !!v[U(e)];
}
function Re(e) {
  return function(t) {
    return e(t);
  };
}
var Ut = typeof exports == "object" && exports && !exports.nodeType && exports, W = Ut && typeof module == "object" && module && !module.nodeType && module, Gr = W && W.exports === Ut, be = Gr && xt.process, Y = function() {
  try {
    var e = W && W.require && W.require("util").types;
    return e || be && be.binding && be.binding("util");
  } catch {
  }
}(), ot = Y && Y.isTypedArray, Gt = ot ? Re(ot) : Ur, zr = Object.prototype, Br = zr.hasOwnProperty;
function zt(e, t) {
  var n = $(e), r = !n && Le(e), o = !n && !r && ae(e), i = !n && !r && !o && Gt(e), s = n || r || o || i, a = s ? lr(e.length, String) : [], c = a.length;
  for (var f in e)
    (t || Br.call(e, f)) && !(s && // Safari 9 has enumerable `arguments.length` in strict mode.
    (f == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    o && (f == "offset" || f == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    i && (f == "buffer" || f == "byteLength" || f == "byteOffset") || // Skip index properties.
    Ft(f, c))) && a.push(f);
  return a;
}
function Bt(e, t) {
  return function(n) {
    return e(t(n));
  };
}
var Hr = Bt(Object.keys, Object), qr = Object.prototype, Yr = qr.hasOwnProperty;
function Xr(e) {
  if (!Ee(e))
    return Hr(e);
  var t = [];
  for (var n in Object(e))
    Yr.call(e, n) && n != "constructor" && t.push(n);
  return t;
}
function ee(e) {
  return Nt(e) ? zt(e) : Xr(e);
}
function Jr(e) {
  var t = [];
  if (e != null)
    for (var n in Object(e))
      t.push(n);
  return t;
}
var Wr = Object.prototype, Zr = Wr.hasOwnProperty;
function Qr(e) {
  if (!X(e))
    return Jr(e);
  var t = Ee(e), n = [];
  for (var r in e)
    r == "constructor" && (t || !Zr.call(e, r)) || n.push(r);
  return n;
}
function Fe(e) {
  return Nt(e) ? zt(e, !0) : Qr(e);
}
var Vr = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, kr = /^\w*$/;
function Me(e, t) {
  if ($(e))
    return !1;
  var n = typeof e;
  return n == "number" || n == "symbol" || n == "boolean" || e == null || Ce(e) ? !0 : kr.test(e) || !Vr.test(e) || t != null && e in Object(t);
}
var Z = z(Object, "create");
function ei() {
  this.__data__ = Z ? Z(null) : {}, this.size = 0;
}
function ti(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var ni = "__lodash_hash_undefined__", ri = Object.prototype, ii = ri.hasOwnProperty;
function oi(e) {
  var t = this.__data__;
  if (Z) {
    var n = t[e];
    return n === ni ? void 0 : n;
  }
  return ii.call(t, e) ? t[e] : void 0;
}
var si = Object.prototype, ai = si.hasOwnProperty;
function ui(e) {
  var t = this.__data__;
  return Z ? t[e] !== void 0 : ai.call(t, e);
}
var li = "__lodash_hash_undefined__";
function fi(e, t) {
  var n = this.__data__;
  return this.size += this.has(e) ? 0 : 1, n[e] = Z && t === void 0 ? li : t, this;
}
function K(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
K.prototype.clear = ei;
K.prototype.delete = ti;
K.prototype.get = oi;
K.prototype.has = ui;
K.prototype.set = fi;
function ci() {
  this.__data__ = [], this.size = 0;
}
function ce(e, t) {
  for (var n = e.length; n--; )
    if (je(e[n][0], t))
      return n;
  return -1;
}
var pi = Array.prototype, gi = pi.splice;
function di(e) {
  var t = this.__data__, n = ce(t, e);
  if (n < 0)
    return !1;
  var r = t.length - 1;
  return n == r ? t.pop() : gi.call(t, n, 1), --this.size, !0;
}
function _i(e) {
  var t = this.__data__, n = ce(t, e);
  return n < 0 ? void 0 : t[n][1];
}
function hi(e) {
  return ce(this.__data__, e) > -1;
}
function bi(e, t) {
  var n = this.__data__, r = ce(n, e);
  return r < 0 ? (++this.size, n.push([e, t])) : n[r][1] = t, this;
}
function R(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
R.prototype.clear = ci;
R.prototype.delete = di;
R.prototype.get = _i;
R.prototype.has = hi;
R.prototype.set = bi;
var Q = z(x, "Map");
function yi() {
  this.size = 0, this.__data__ = {
    hash: new K(),
    map: new (Q || R)(),
    string: new K()
  };
}
function mi(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function pe(e, t) {
  var n = e.__data__;
  return mi(t) ? n[typeof t == "string" ? "string" : "hash"] : n.map;
}
function vi(e) {
  var t = pe(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function Ti(e) {
  return pe(this, e).get(e);
}
function wi(e) {
  return pe(this, e).has(e);
}
function Oi(e, t) {
  var n = pe(this, e), r = n.size;
  return n.set(e, t), this.size += n.size == r ? 0 : 1, this;
}
function F(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
F.prototype.clear = yi;
F.prototype.delete = vi;
F.prototype.get = Ti;
F.prototype.has = wi;
F.prototype.set = Oi;
var Pi = "Expected a function";
function Ne(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(Pi);
  var n = function() {
    var r = arguments, o = t ? t.apply(this, r) : r[0], i = n.cache;
    if (i.has(o))
      return i.get(o);
    var s = e.apply(this, r);
    return n.cache = i.set(o, s) || i, s;
  };
  return n.cache = new (Ne.Cache || F)(), n;
}
Ne.Cache = F;
var Ai = 500;
function $i(e) {
  var t = Ne(e, function(r) {
    return n.size === Ai && n.clear(), r;
  }), n = t.cache;
  return t;
}
var Si = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, Ci = /\\(\\)?/g, xi = $i(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(Si, function(n, r, o, i) {
    t.push(o ? i.replace(Ci, "$1") : r || n);
  }), t;
});
function ji(e) {
  return e == null ? "" : Et(e);
}
function ge(e, t) {
  return $(e) ? e : Me(e, t) ? [e] : xi(ji(e));
}
var Ii = 1 / 0;
function te(e) {
  if (typeof e == "string" || Ce(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -Ii ? "-0" : t;
}
function De(e, t) {
  t = ge(t, e);
  for (var n = 0, r = t.length; e != null && n < r; )
    e = e[te(t[n++])];
  return n && n == r ? e : void 0;
}
function Ei(e, t, n) {
  var r = e == null ? void 0 : De(e, t);
  return r === void 0 ? n : r;
}
function Ke(e, t) {
  for (var n = -1, r = t.length, o = e.length; ++n < r; )
    e[o + n] = t[n];
  return e;
}
var st = O ? O.isConcatSpreadable : void 0;
function Li(e) {
  return $(e) || Le(e) || !!(st && e && e[st]);
}
function Ri(e, t, n, r, o) {
  var i = -1, s = e.length;
  for (n || (n = Li), o || (o = []); ++i < s; ) {
    var a = e[i];
    n(a) ? Ke(o, a) : o[o.length] = a;
  }
  return o;
}
function Fi(e) {
  var t = e == null ? 0 : e.length;
  return t ? Ri(e) : [];
}
function Mi(e) {
  return er(sr(e, void 0, Fi), e + "");
}
var Ue = Bt(Object.getPrototypeOf, Object), Ni = "[object Object]", Di = Function.prototype, Ki = Object.prototype, Ht = Di.toString, Ui = Ki.hasOwnProperty, Gi = Ht.call(Object);
function zi(e) {
  if (!L(e) || U(e) != Ni)
    return !1;
  var t = Ue(e);
  if (t === null)
    return !0;
  var n = Ui.call(t, "constructor") && t.constructor;
  return typeof n == "function" && n instanceof n && Ht.call(n) == Gi;
}
function Bi(e, t, n) {
  var r = -1, o = e.length;
  t < 0 && (t = -t > o ? 0 : o + t), n = n > o ? o : n, n < 0 && (n += o), o = t > n ? 0 : n - t >>> 0, t >>>= 0;
  for (var i = Array(o); ++r < o; )
    i[r] = e[r + t];
  return i;
}
function Hi() {
  this.__data__ = new R(), this.size = 0;
}
function qi(e) {
  var t = this.__data__, n = t.delete(e);
  return this.size = t.size, n;
}
function Yi(e) {
  return this.__data__.get(e);
}
function Xi(e) {
  return this.__data__.has(e);
}
var Ji = 200;
function Wi(e, t) {
  var n = this.__data__;
  if (n instanceof R) {
    var r = n.__data__;
    if (!Q || r.length < Ji - 1)
      return r.push([e, t]), this.size = ++n.size, this;
    n = this.__data__ = new F(r);
  }
  return n.set(e, t), this.size = n.size, this;
}
function C(e) {
  var t = this.__data__ = new R(e);
  this.size = t.size;
}
C.prototype.clear = Hi;
C.prototype.delete = qi;
C.prototype.get = Yi;
C.prototype.has = Xi;
C.prototype.set = Wi;
function Zi(e, t) {
  return e && k(t, ee(t), e);
}
function Qi(e, t) {
  return e && k(t, Fe(t), e);
}
var qt = typeof exports == "object" && exports && !exports.nodeType && exports, at = qt && typeof module == "object" && module && !module.nodeType && module, Vi = at && at.exports === qt, ut = Vi ? x.Buffer : void 0, lt = ut ? ut.allocUnsafe : void 0;
function ki(e, t) {
  if (t)
    return e.slice();
  var n = e.length, r = lt ? lt(n) : new e.constructor(n);
  return e.copy(r), r;
}
function eo(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, o = 0, i = []; ++n < r; ) {
    var s = e[n];
    t(s, n, e) && (i[o++] = s);
  }
  return i;
}
function Yt() {
  return [];
}
var to = Object.prototype, no = to.propertyIsEnumerable, ft = Object.getOwnPropertySymbols, Ge = ft ? function(e) {
  return e == null ? [] : (e = Object(e), eo(ft(e), function(t) {
    return no.call(e, t);
  }));
} : Yt;
function ro(e, t) {
  return k(e, Ge(e), t);
}
var io = Object.getOwnPropertySymbols, Xt = io ? function(e) {
  for (var t = []; e; )
    Ke(t, Ge(e)), e = Ue(e);
  return t;
} : Yt;
function oo(e, t) {
  return k(e, Xt(e), t);
}
function Jt(e, t, n) {
  var r = t(e);
  return $(e) ? r : Ke(r, n(e));
}
function Oe(e) {
  return Jt(e, ee, Ge);
}
function Wt(e) {
  return Jt(e, Fe, Xt);
}
var Pe = z(x, "DataView"), Ae = z(x, "Promise"), $e = z(x, "Set"), ct = "[object Map]", so = "[object Object]", pt = "[object Promise]", gt = "[object Set]", dt = "[object WeakMap]", _t = "[object DataView]", ao = G(Pe), uo = G(Q), lo = G(Ae), fo = G($e), co = G(we), A = U;
(Pe && A(new Pe(new ArrayBuffer(1))) != _t || Q && A(new Q()) != ct || Ae && A(Ae.resolve()) != pt || $e && A(new $e()) != gt || we && A(new we()) != dt) && (A = function(e) {
  var t = U(e), n = t == so ? e.constructor : void 0, r = n ? G(n) : "";
  if (r)
    switch (r) {
      case ao:
        return _t;
      case uo:
        return ct;
      case lo:
        return pt;
      case fo:
        return gt;
      case co:
        return dt;
    }
  return t;
});
var po = Object.prototype, go = po.hasOwnProperty;
function _o(e) {
  var t = e.length, n = new e.constructor(t);
  return t && typeof e[0] == "string" && go.call(e, "index") && (n.index = e.index, n.input = e.input), n;
}
var ue = x.Uint8Array;
function ze(e) {
  var t = new e.constructor(e.byteLength);
  return new ue(t).set(new ue(e)), t;
}
function ho(e, t) {
  var n = t ? ze(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.byteLength);
}
var bo = /\w*$/;
function yo(e) {
  var t = new e.constructor(e.source, bo.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var ht = O ? O.prototype : void 0, bt = ht ? ht.valueOf : void 0;
function mo(e) {
  return bt ? Object(bt.call(e)) : {};
}
function vo(e, t) {
  var n = t ? ze(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.length);
}
var To = "[object Boolean]", wo = "[object Date]", Oo = "[object Map]", Po = "[object Number]", Ao = "[object RegExp]", $o = "[object Set]", So = "[object String]", Co = "[object Symbol]", xo = "[object ArrayBuffer]", jo = "[object DataView]", Io = "[object Float32Array]", Eo = "[object Float64Array]", Lo = "[object Int8Array]", Ro = "[object Int16Array]", Fo = "[object Int32Array]", Mo = "[object Uint8Array]", No = "[object Uint8ClampedArray]", Do = "[object Uint16Array]", Ko = "[object Uint32Array]";
function Uo(e, t, n) {
  var r = e.constructor;
  switch (t) {
    case xo:
      return ze(e);
    case To:
    case wo:
      return new r(+e);
    case jo:
      return ho(e, n);
    case Io:
    case Eo:
    case Lo:
    case Ro:
    case Fo:
    case Mo:
    case No:
    case Do:
    case Ko:
      return vo(e, n);
    case Oo:
      return new r();
    case Po:
    case So:
      return new r(e);
    case Ao:
      return yo(e);
    case $o:
      return new r();
    case Co:
      return mo(e);
  }
}
function Go(e) {
  return typeof e.constructor == "function" && !Ee(e) ? qn(Ue(e)) : {};
}
var zo = "[object Map]";
function Bo(e) {
  return L(e) && A(e) == zo;
}
var yt = Y && Y.isMap, Ho = yt ? Re(yt) : Bo, qo = "[object Set]";
function Yo(e) {
  return L(e) && A(e) == qo;
}
var mt = Y && Y.isSet, Xo = mt ? Re(mt) : Yo, Jo = 1, Wo = 2, Zo = 4, Zt = "[object Arguments]", Qo = "[object Array]", Vo = "[object Boolean]", ko = "[object Date]", es = "[object Error]", Qt = "[object Function]", ts = "[object GeneratorFunction]", ns = "[object Map]", rs = "[object Number]", Vt = "[object Object]", is = "[object RegExp]", os = "[object Set]", ss = "[object String]", as = "[object Symbol]", us = "[object WeakMap]", ls = "[object ArrayBuffer]", fs = "[object DataView]", cs = "[object Float32Array]", ps = "[object Float64Array]", gs = "[object Int8Array]", ds = "[object Int16Array]", _s = "[object Int32Array]", hs = "[object Uint8Array]", bs = "[object Uint8ClampedArray]", ys = "[object Uint16Array]", ms = "[object Uint32Array]", y = {};
y[Zt] = y[Qo] = y[ls] = y[fs] = y[Vo] = y[ko] = y[cs] = y[ps] = y[gs] = y[ds] = y[_s] = y[ns] = y[rs] = y[Vt] = y[is] = y[os] = y[ss] = y[as] = y[hs] = y[bs] = y[ys] = y[ms] = !0;
y[es] = y[Qt] = y[us] = !1;
function ie(e, t, n, r, o, i) {
  var s, a = t & Jo, c = t & Wo, f = t & Zo;
  if (n && (s = o ? n(e, r, o, i) : n(e)), s !== void 0)
    return s;
  if (!X(e))
    return e;
  var _ = $(e);
  if (_) {
    if (s = _o(e), !a)
      return Xn(e, s);
  } else {
    var g = A(e), h = g == Qt || g == ts;
    if (ae(e))
      return ki(e, a);
    if (g == Vt || g == Zt || h && !o) {
      if (s = c || h ? {} : Go(e), !a)
        return c ? oo(e, Qi(s, e)) : ro(e, Zi(s, e));
    } else {
      if (!y[g])
        return o ? e : {};
      s = Uo(e, g, a);
    }
  }
  i || (i = new C());
  var b = i.get(e);
  if (b)
    return b;
  i.set(e, s), Xo(e) ? e.forEach(function(l) {
    s.add(ie(l, t, n, l, e, i));
  }) : Ho(e) && e.forEach(function(l, m) {
    s.set(m, ie(l, t, n, m, e, i));
  });
  var u = f ? c ? Wt : Oe : c ? Fe : ee, p = _ ? void 0 : u(e);
  return tr(p || e, function(l, m) {
    p && (m = l, l = e[m]), Mt(s, m, ie(l, t, n, m, e, i));
  }), s;
}
var vs = "__lodash_hash_undefined__";
function Ts(e) {
  return this.__data__.set(e, vs), this;
}
function ws(e) {
  return this.__data__.has(e);
}
function le(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.__data__ = new F(); ++t < n; )
    this.add(e[t]);
}
le.prototype.add = le.prototype.push = Ts;
le.prototype.has = ws;
function Os(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r; )
    if (t(e[n], n, e))
      return !0;
  return !1;
}
function Ps(e, t) {
  return e.has(t);
}
var As = 1, $s = 2;
function kt(e, t, n, r, o, i) {
  var s = n & As, a = e.length, c = t.length;
  if (a != c && !(s && c > a))
    return !1;
  var f = i.get(e), _ = i.get(t);
  if (f && _)
    return f == t && _ == e;
  var g = -1, h = !0, b = n & $s ? new le() : void 0;
  for (i.set(e, t), i.set(t, e); ++g < a; ) {
    var u = e[g], p = t[g];
    if (r)
      var l = s ? r(p, u, g, t, e, i) : r(u, p, g, e, t, i);
    if (l !== void 0) {
      if (l)
        continue;
      h = !1;
      break;
    }
    if (b) {
      if (!Os(t, function(m, w) {
        if (!Ps(b, w) && (u === m || o(u, m, n, r, i)))
          return b.push(w);
      })) {
        h = !1;
        break;
      }
    } else if (!(u === p || o(u, p, n, r, i))) {
      h = !1;
      break;
    }
  }
  return i.delete(e), i.delete(t), h;
}
function Ss(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r, o) {
    n[++t] = [o, r];
  }), n;
}
function Cs(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r) {
    n[++t] = r;
  }), n;
}
var xs = 1, js = 2, Is = "[object Boolean]", Es = "[object Date]", Ls = "[object Error]", Rs = "[object Map]", Fs = "[object Number]", Ms = "[object RegExp]", Ns = "[object Set]", Ds = "[object String]", Ks = "[object Symbol]", Us = "[object ArrayBuffer]", Gs = "[object DataView]", vt = O ? O.prototype : void 0, ye = vt ? vt.valueOf : void 0;
function zs(e, t, n, r, o, i, s) {
  switch (n) {
    case Gs:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case Us:
      return !(e.byteLength != t.byteLength || !i(new ue(e), new ue(t)));
    case Is:
    case Es:
    case Fs:
      return je(+e, +t);
    case Ls:
      return e.name == t.name && e.message == t.message;
    case Ms:
    case Ds:
      return e == t + "";
    case Rs:
      var a = Ss;
    case Ns:
      var c = r & xs;
      if (a || (a = Cs), e.size != t.size && !c)
        return !1;
      var f = s.get(e);
      if (f)
        return f == t;
      r |= js, s.set(e, t);
      var _ = kt(a(e), a(t), r, o, i, s);
      return s.delete(e), _;
    case Ks:
      if (ye)
        return ye.call(e) == ye.call(t);
  }
  return !1;
}
var Bs = 1, Hs = Object.prototype, qs = Hs.hasOwnProperty;
function Ys(e, t, n, r, o, i) {
  var s = n & Bs, a = Oe(e), c = a.length, f = Oe(t), _ = f.length;
  if (c != _ && !s)
    return !1;
  for (var g = c; g--; ) {
    var h = a[g];
    if (!(s ? h in t : qs.call(t, h)))
      return !1;
  }
  var b = i.get(e), u = i.get(t);
  if (b && u)
    return b == t && u == e;
  var p = !0;
  i.set(e, t), i.set(t, e);
  for (var l = s; ++g < c; ) {
    h = a[g];
    var m = e[h], w = t[h];
    if (r)
      var N = s ? r(w, m, h, t, e, i) : r(m, w, h, e, t, i);
    if (!(N === void 0 ? m === w || o(m, w, n, r, i) : N)) {
      p = !1;
      break;
    }
    l || (l = h == "constructor");
  }
  if (p && !l) {
    var j = e.constructor, I = t.constructor;
    j != I && "constructor" in e && "constructor" in t && !(typeof j == "function" && j instanceof j && typeof I == "function" && I instanceof I) && (p = !1);
  }
  return i.delete(e), i.delete(t), p;
}
var Xs = 1, Tt = "[object Arguments]", wt = "[object Array]", re = "[object Object]", Js = Object.prototype, Ot = Js.hasOwnProperty;
function Ws(e, t, n, r, o, i) {
  var s = $(e), a = $(t), c = s ? wt : A(e), f = a ? wt : A(t);
  c = c == Tt ? re : c, f = f == Tt ? re : f;
  var _ = c == re, g = f == re, h = c == f;
  if (h && ae(e)) {
    if (!ae(t))
      return !1;
    s = !0, _ = !1;
  }
  if (h && !_)
    return i || (i = new C()), s || Gt(e) ? kt(e, t, n, r, o, i) : zs(e, t, c, n, r, o, i);
  if (!(n & Xs)) {
    var b = _ && Ot.call(e, "__wrapped__"), u = g && Ot.call(t, "__wrapped__");
    if (b || u) {
      var p = b ? e.value() : e, l = u ? t.value() : t;
      return i || (i = new C()), o(p, l, n, r, i);
    }
  }
  return h ? (i || (i = new C()), Ys(e, t, n, r, o, i)) : !1;
}
function Be(e, t, n, r, o) {
  return e === t ? !0 : e == null || t == null || !L(e) && !L(t) ? e !== e && t !== t : Ws(e, t, n, r, Be, o);
}
var Zs = 1, Qs = 2;
function Vs(e, t, n, r) {
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
      var _ = new C(), g;
      if (!(g === void 0 ? Be(f, c, Zs | Qs, r, _) : g))
        return !1;
    }
  }
  return !0;
}
function en(e) {
  return e === e && !X(e);
}
function ks(e) {
  for (var t = ee(e), n = t.length; n--; ) {
    var r = t[n], o = e[r];
    t[n] = [r, o, en(o)];
  }
  return t;
}
function tn(e, t) {
  return function(n) {
    return n == null ? !1 : n[e] === t && (t !== void 0 || e in Object(n));
  };
}
function ea(e) {
  var t = ks(e);
  return t.length == 1 && t[0][2] ? tn(t[0][0], t[0][1]) : function(n) {
    return n === e || Vs(n, e, t);
  };
}
function ta(e, t) {
  return e != null && t in Object(e);
}
function na(e, t, n) {
  t = ge(t, e);
  for (var r = -1, o = t.length, i = !1; ++r < o; ) {
    var s = te(t[r]);
    if (!(i = e != null && n(e, s)))
      break;
    e = e[s];
  }
  return i || ++r != o ? i : (o = e == null ? 0 : e.length, !!o && Ie(o) && Ft(s, o) && ($(e) || Le(e)));
}
function ra(e, t) {
  return e != null && na(e, t, ta);
}
var ia = 1, oa = 2;
function sa(e, t) {
  return Me(e) && en(t) ? tn(te(e), t) : function(n) {
    var r = Ei(n, e);
    return r === void 0 && r === t ? ra(n, e) : Be(t, r, ia | oa);
  };
}
function aa(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function ua(e) {
  return function(t) {
    return De(t, e);
  };
}
function la(e) {
  return Me(e) ? aa(te(e)) : ua(e);
}
function fa(e) {
  return typeof e == "function" ? e : e == null ? Lt : typeof e == "object" ? $(e) ? sa(e[0], e[1]) : ea(e) : la(e);
}
function ca(e) {
  return function(t, n, r) {
    for (var o = -1, i = Object(t), s = r(t), a = s.length; a--; ) {
      var c = s[++o];
      if (n(i[c], c, i) === !1)
        break;
    }
    return t;
  };
}
var pa = ca();
function ga(e, t) {
  return e && pa(e, t, ee);
}
function da(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function _a(e, t) {
  return t.length < 2 ? e : De(e, Bi(t, 0, -1));
}
function ha(e) {
  return e === void 0;
}
function ba(e, t) {
  var n = {};
  return t = fa(t), ga(e, function(r, o, i) {
    xe(n, t(r, o, i), r);
  }), n;
}
function ya(e, t) {
  return t = ge(t, e), e = _a(e, t), e == null || delete e[te(da(t))];
}
function ma(e) {
  return zi(e) ? void 0 : e;
}
var va = 1, Ta = 2, wa = 4, nn = Mi(function(e, t) {
  var n = {};
  if (e == null)
    return n;
  var r = !1;
  t = It(t, function(i) {
    return i = ge(i, e), r || (r = i.length > 1), i;
  }), k(e, Wt(e), n), r && (n = ie(n, va | Ta | wa, ma));
  for (var o = t.length; o--; )
    ya(n, t[o]);
  return n;
});
async function Oa() {
  window.ms_globals || (window.ms_globals = {}), window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function Pa(e) {
  return await Oa(), e().then((t) => t.default);
}
function Aa(e) {
  return e.replace(/(^|_)(\w)/g, (t, n, r, o) => o === 0 ? r.toLowerCase() : r.toUpperCase());
}
const rn = ["interactive", "gradio", "server", "target", "theme_mode", "root", "name", "visible", "elem_id", "elem_classes", "elem_style", "_internal", "props", "value", "_selectable", "attached_events", "loading_status", "value_is_output"];
function $a(e, t = {}) {
  return ba(nn(e, rn), (n, r) => t[r] || Aa(r));
}
function Pt(e) {
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
      const f = c[1], _ = f.split("_"), g = (...b) => {
        const u = b.map((l) => b && typeof l == "object" && (l.nativeEvent || l instanceof Event) ? {
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
        let p;
        try {
          p = JSON.parse(JSON.stringify(u));
        } catch {
          p = u.map((l) => l && typeof l == "object" ? Object.fromEntries(Object.entries(l).filter(([, m]) => {
            try {
              return JSON.stringify(m), !0;
            } catch {
              return !1;
            }
          })) : l);
        }
        return t.dispatch(f.replace(/[A-Z]/g, (l) => "_" + l.toLowerCase()), {
          payload: p,
          component: {
            ...i,
            ...nn(o, rn)
          }
        });
      };
      if (_.length > 1) {
        let b = {
          ...i.props[_[0]] || (r == null ? void 0 : r[_[0]]) || {}
        };
        s[_[0]] = b;
        for (let p = 1; p < _.length - 1; p++) {
          const l = {
            ...i.props[_[p]] || (r == null ? void 0 : r[_[p]]) || {}
          };
          b[_[p]] = l, b = l;
        }
        const u = _[_.length - 1];
        return b[`on${u.slice(0, 1).toUpperCase()}${u.slice(1)}`] = g, s;
      }
      const h = _[0];
      s[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = g;
    }
    return s;
  }, {});
}
function oe() {
}
function Sa(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Ca(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return oe;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function D(e) {
  let t;
  return Ca(e, (n) => t = n)(), t;
}
const H = [];
function M(e, t = oe) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function o(a) {
    if (Sa(e, a) && (e = a, n)) {
      const c = !H.length;
      for (const f of r)
        f[1](), H.push(f, e);
      if (c) {
        for (let f = 0; f < H.length; f += 2)
          H[f][0](H[f + 1]);
        H.length = 0;
      }
    }
  }
  function i(a) {
    o(a(e));
  }
  function s(a, c = oe) {
    const f = [a, c];
    return r.add(f), r.size === 1 && (n = t(o, i) || oe), a(e), () => {
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
  getContext: xa,
  setContext: hu
} = window.__gradio__svelte__internal, ja = "$$ms-gr-loading-status-key";
function Ia() {
  const e = window.ms_globals.loadingKey++, t = xa(ja);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: r,
      options: o
    } = t, {
      generating: i,
      error: s
    } = D(o);
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
  getContext: de,
  setContext: ne
} = window.__gradio__svelte__internal, Ea = "$$ms-gr-slots-key";
function La() {
  const e = M({});
  return ne(Ea, e);
}
const Ra = "$$ms-gr-render-slot-context-key";
function Fa() {
  const e = ne(Ra, M({}));
  return (t, n) => {
    e.update((r) => typeof n == "function" ? {
      ...r,
      [t]: n(r[t])
    } : {
      ...r,
      [t]: n
    });
  };
}
const Ma = "$$ms-gr-context-key";
function me(e) {
  return ha(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const on = "$$ms-gr-sub-index-context-key";
function Na() {
  return de(on) || null;
}
function At(e) {
  return ne(on, e);
}
function Da(e, t, n) {
  var h, b;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = Ua(), o = Ga({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), i = Na();
  typeof i == "number" && At(void 0);
  const s = Ia();
  typeof e._internal.subIndex == "number" && At(e._internal.subIndex), r && r.subscribe((u) => {
    o.slotKey.set(u);
  }), Ka();
  const a = de(Ma), c = ((h = D(a)) == null ? void 0 : h.as_item) || e.as_item, f = me(a ? c ? ((b = D(a)) == null ? void 0 : b[c]) || {} : D(a) || {} : {}), _ = (u, p) => u ? $a({
    ...u,
    ...p || {}
  }, t) : void 0, g = M({
    ...e,
    _internal: {
      ...e._internal,
      index: i ?? e._internal.index
    },
    ...f,
    restProps: _(e.restProps, f),
    originalRestProps: e.restProps
  });
  return a ? (a.subscribe((u) => {
    const {
      as_item: p
    } = D(g);
    p && (u = u == null ? void 0 : u[p]), u = me(u), g.update((l) => ({
      ...l,
      ...u || {},
      restProps: _(l.restProps, u)
    }));
  }), [g, (u) => {
    var l, m;
    const p = me(u.as_item ? ((l = D(a)) == null ? void 0 : l[u.as_item]) || {} : D(a) || {});
    return s((m = u.restProps) == null ? void 0 : m.loading_status), g.set({
      ...u,
      _internal: {
        ...u._internal,
        index: i ?? u._internal.index
      },
      ...p,
      restProps: _(u.restProps, p),
      originalRestProps: u.restProps
    });
  }]) : [g, (u) => {
    var p;
    s((p = u.restProps) == null ? void 0 : p.loading_status), g.set({
      ...u,
      _internal: {
        ...u._internal,
        index: i ?? u._internal.index
      },
      restProps: _(u.restProps),
      originalRestProps: u.restProps
    });
  }];
}
const sn = "$$ms-gr-slot-key";
function Ka() {
  ne(sn, M(void 0));
}
function Ua() {
  return de(sn);
}
const an = "$$ms-gr-component-slot-context-key";
function Ga({
  slot: e,
  index: t,
  subIndex: n
}) {
  return ne(an, {
    slotKey: M(e),
    slotIndex: M(t),
    subSlotIndex: M(n)
  });
}
function bu() {
  return de(an);
}
new Intl.Collator(0, {
  numeric: 1
}).compare;
async function za(e, t) {
  return e.map((n) => new Ba({
    path: n.name,
    orig_name: n.name,
    blob: n,
    size: n.size,
    mime_type: n.type,
    is_stream: t
  }));
}
class Ba {
  constructor({
    path: t,
    url: n,
    orig_name: r,
    size: o,
    blob: i,
    is_stream: s,
    mime_type: a,
    alt_text: c,
    b64: f
  }) {
    P(this, "path");
    P(this, "url");
    P(this, "orig_name");
    P(this, "size");
    P(this, "blob");
    P(this, "is_stream");
    P(this, "mime_type");
    P(this, "alt_text");
    P(this, "b64");
    P(this, "meta", {
      _type: "gradio.FileData"
    });
    this.path = t, this.url = n, this.orig_name = r, this.size = o, this.blob = n ? void 0 : i, this.is_stream = s, this.mime_type = a, this.alt_text = c, this.b64 = f;
  }
}
typeof process < "u" && process.versions && process.versions.node;
var E;
class yu extends TransformStream {
  /** Constructs a new instance. */
  constructor(n = {
    allowCR: !1
  }) {
    super({
      transform: (r, o) => {
        for (r = B(this, E) + r; ; ) {
          const i = r.indexOf(`
`), s = n.allowCR ? r.indexOf("\r") : -1;
          if (s !== -1 && s !== r.length - 1 && (i === -1 || i - 1 > s)) {
            o.enqueue(r.slice(0, s)), r = r.slice(s + 1);
            continue;
          }
          if (i === -1) break;
          const a = r[i - 1] === "\r" ? i - 1 : i;
          o.enqueue(r.slice(0, a)), r = r.slice(i + 1);
        }
        We(this, E, r);
      },
      flush: (r) => {
        if (B(this, E) === "") return;
        const o = n.allowCR && B(this, E).endsWith("\r") ? B(this, E).slice(0, -1) : B(this, E);
        r.enqueue(o);
      }
    });
    Je(this, E, "");
  }
}
E = new WeakMap();
function Ha(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var un = {
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
})(un);
var qa = un.exports;
const $t = /* @__PURE__ */ Ha(qa), {
  SvelteComponent: Ya,
  assign: Se,
  check_outros: Xa,
  claim_component: Ja,
  component_subscribe: ve,
  compute_rest_props: St,
  create_component: Wa,
  create_slot: Za,
  destroy_component: Qa,
  detach: ln,
  empty: fe,
  exclude_internal_props: Va,
  flush: S,
  get_all_dirty_from_scope: ka,
  get_slot_changes: eu,
  get_spread_object: Te,
  get_spread_update: tu,
  group_outros: nu,
  handle_promise: ru,
  init: iu,
  insert_hydration: fn,
  mount_component: ou,
  noop: T,
  safe_not_equal: su,
  transition_in: q,
  transition_out: V,
  update_await_block_branch: au,
  update_slot_base: uu
} = window.__gradio__svelte__internal;
function Ct(e) {
  let t, n, r = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: pu,
    then: fu,
    catch: lu,
    value: 24,
    blocks: [, , ,]
  };
  return ru(
    /*AwaitedUpload*/
    e[5],
    r
  ), {
    c() {
      t = fe(), r.block.c();
    },
    l(o) {
      t = fe(), r.block.l(o);
    },
    m(o, i) {
      fn(o, t, i), r.block.m(o, r.anchor = i), r.mount = () => t.parentNode, r.anchor = t, n = !0;
    },
    p(o, i) {
      e = o, au(r, e, i);
    },
    i(o) {
      n || (q(r.block), n = !0);
    },
    o(o) {
      for (let i = 0; i < 3; i += 1) {
        const s = r.blocks[i];
        V(s);
      }
      n = !1;
    },
    d(o) {
      o && ln(t), r.block.d(o), r.token = null, r = null;
    }
  };
}
function lu(e) {
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
function fu(e) {
  let t, n;
  const r = [
    {
      style: (
        /*$mergedProps*/
        e[3].elem_style
      )
    },
    {
      className: $t(
        /*$mergedProps*/
        e[3].elem_classes,
        "ms-gr-antd-upload"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[3].elem_id
      )
    },
    {
      fileList: (
        /*$mergedProps*/
        e[3].value
      )
    },
    /*$mergedProps*/
    e[3].restProps,
    /*$mergedProps*/
    e[3].props,
    Pt(
      /*$mergedProps*/
      e[3]
    ),
    {
      slots: (
        /*$slots*/
        e[4]
      )
    },
    {
      onValueChange: (
        /*func*/
        e[19]
      )
    },
    {
      upload: (
        /*func_1*/
        e[20]
      )
    },
    {
      setSlotParams: (
        /*setSlotParams*/
        e[8]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [cu]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let i = 0; i < r.length; i += 1)
    o = Se(o, r[i]);
  return t = new /*Upload*/
  e[24]({
    props: o
  }), {
    c() {
      Wa(t.$$.fragment);
    },
    l(i) {
      Ja(t.$$.fragment, i);
    },
    m(i, s) {
      ou(t, i, s), n = !0;
    },
    p(i, s) {
      const a = s & /*$mergedProps, $slots, value, gradio, root, setSlotParams*/
      287 ? tu(r, [s & /*$mergedProps*/
      8 && {
        style: (
          /*$mergedProps*/
          i[3].elem_style
        )
      }, s & /*$mergedProps*/
      8 && {
        className: $t(
          /*$mergedProps*/
          i[3].elem_classes,
          "ms-gr-antd-upload"
        )
      }, s & /*$mergedProps*/
      8 && {
        id: (
          /*$mergedProps*/
          i[3].elem_id
        )
      }, s & /*$mergedProps*/
      8 && {
        fileList: (
          /*$mergedProps*/
          i[3].value
        )
      }, s & /*$mergedProps*/
      8 && Te(
        /*$mergedProps*/
        i[3].restProps
      ), s & /*$mergedProps*/
      8 && Te(
        /*$mergedProps*/
        i[3].props
      ), s & /*$mergedProps*/
      8 && Te(Pt(
        /*$mergedProps*/
        i[3]
      )), s & /*$slots*/
      16 && {
        slots: (
          /*$slots*/
          i[4]
        )
      }, s & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          i[19]
        )
      }, s & /*gradio, root*/
      6 && {
        upload: (
          /*func_1*/
          i[20]
        )
      }, s & /*setSlotParams*/
      256 && {
        setSlotParams: (
          /*setSlotParams*/
          i[8]
        )
      }]) : {};
      s & /*$$scope*/
      2097152 && (a.$$scope = {
        dirty: s,
        ctx: i
      }), t.$set(a);
    },
    i(i) {
      n || (q(t.$$.fragment, i), n = !0);
    },
    o(i) {
      V(t.$$.fragment, i), n = !1;
    },
    d(i) {
      Qa(t, i);
    }
  };
}
function cu(e) {
  let t;
  const n = (
    /*#slots*/
    e[18].default
  ), r = Za(
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
      2097152) && uu(
        r,
        n,
        o,
        /*$$scope*/
        o[21],
        t ? eu(
          n,
          /*$$scope*/
          o[21],
          i,
          null
        ) : ka(
          /*$$scope*/
          o[21]
        ),
        null
      );
    },
    i(o) {
      t || (q(r, o), t = !0);
    },
    o(o) {
      V(r, o), t = !1;
    },
    d(o) {
      r && r.d(o);
    }
  };
}
function pu(e) {
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
function gu(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[3].visible && Ct(e)
  );
  return {
    c() {
      r && r.c(), t = fe();
    },
    l(o) {
      r && r.l(o), t = fe();
    },
    m(o, i) {
      r && r.m(o, i), fn(o, t, i), n = !0;
    },
    p(o, [i]) {
      /*$mergedProps*/
      o[3].visible ? r ? (r.p(o, i), i & /*$mergedProps*/
      8 && q(r, 1)) : (r = Ct(o), r.c(), q(r, 1), r.m(t.parentNode, t)) : r && (nu(), V(r, 1, 1, () => {
        r = null;
      }), Xa());
    },
    i(o) {
      n || (q(r), n = !0);
    },
    o(o) {
      V(r), n = !1;
    },
    d(o) {
      o && ln(t), r && r.d(o);
    }
  };
}
function du(e, t, n) {
  const r = ["gradio", "props", "_internal", "root", "value", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = St(t, r), i, s, a, {
    $$slots: c = {},
    $$scope: f
  } = t;
  const _ = Pa(() => import("./upload-D3-ynDlm.js"));
  let {
    gradio: g
  } = t, {
    props: h = {}
  } = t;
  const b = M(h);
  ve(e, b, (d) => n(17, i = d));
  let {
    _internal: u
  } = t, {
    root: p
  } = t, {
    value: l = []
  } = t, {
    as_item: m
  } = t, {
    visible: w = !0
  } = t, {
    elem_id: N = ""
  } = t, {
    elem_classes: j = []
  } = t, {
    elem_style: I = {}
  } = t;
  const [He, cn] = Da({
    gradio: g,
    props: i,
    _internal: u,
    value: l,
    visible: w,
    elem_id: N,
    elem_classes: j,
    elem_style: I,
    as_item: m,
    restProps: o
  }, {
    form_name: "name"
  });
  ve(e, He, (d) => n(3, s = d));
  const pn = Fa(), qe = La();
  ve(e, qe, (d) => n(4, a = d));
  const gn = (d) => {
    n(0, l = d);
  }, dn = async (d) => (await g.client.upload(await za(d), p) || []).map((_e, _n) => _e && {
    ..._e,
    uid: d[_n].uid
  });
  return e.$$set = (d) => {
    t = Se(Se({}, t), Va(d)), n(23, o = St(t, r)), "gradio" in d && n(1, g = d.gradio), "props" in d && n(10, h = d.props), "_internal" in d && n(11, u = d._internal), "root" in d && n(2, p = d.root), "value" in d && n(0, l = d.value), "as_item" in d && n(12, m = d.as_item), "visible" in d && n(13, w = d.visible), "elem_id" in d && n(14, N = d.elem_id), "elem_classes" in d && n(15, j = d.elem_classes), "elem_style" in d && n(16, I = d.elem_style), "$$scope" in d && n(21, f = d.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    1024 && b.update((d) => ({
      ...d,
      ...h
    })), cn({
      gradio: g,
      props: i,
      _internal: u,
      value: l,
      visible: w,
      elem_id: N,
      elem_classes: j,
      elem_style: I,
      as_item: m,
      restProps: o
    });
  }, [l, g, p, s, a, _, b, He, pn, qe, h, u, m, w, N, j, I, i, c, gn, dn, f];
}
class mu extends Ya {
  constructor(t) {
    super(), iu(this, t, du, gu, su, {
      gradio: 1,
      props: 10,
      _internal: 11,
      root: 2,
      value: 0,
      as_item: 12,
      visible: 13,
      elem_id: 14,
      elem_classes: 15,
      elem_style: 16
    });
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), S();
  }
  get props() {
    return this.$$.ctx[10];
  }
  set props(t) {
    this.$$set({
      props: t
    }), S();
  }
  get _internal() {
    return this.$$.ctx[11];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), S();
  }
  get root() {
    return this.$$.ctx[2];
  }
  set root(t) {
    this.$$set({
      root: t
    }), S();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), S();
  }
  get as_item() {
    return this.$$.ctx[12];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), S();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), S();
  }
  get elem_id() {
    return this.$$.ctx[14];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), S();
  }
  get elem_classes() {
    return this.$$.ctx[15];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), S();
  }
  get elem_style() {
    return this.$$.ctx[16];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), S();
  }
}
export {
  mu as I,
  bu as g,
  M as w
};
