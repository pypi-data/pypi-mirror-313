import { g as Lt, w as x } from "./Index-XdcFYdfz.js";
const b = window.ms_globals.React, Nt = window.ms_globals.React.forwardRef, Tt = window.ms_globals.React.useRef, jt = window.ms_globals.React.useState, bt = window.ms_globals.React.useEffect, Mt = window.ms_globals.React.useMemo, J = window.ms_globals.ReactDOM.createPortal, Kt = window.ms_globals.antdCssinjs.StyleProvider, Ut = window.ms_globals.antd.ConfigProvider, st = window.ms_globals.antd.theme, Wt = window.ms_globals.dayjs;
var kt = {
  exports: {}
}, K = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Bt = b, Gt = Symbol.for("react.element"), Ht = Symbol.for("react.fragment"), Zt = Object.prototype.hasOwnProperty, qt = Bt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Yt = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Et(e, t, n) {
  var r, a = {}, o = null, s = null;
  n !== void 0 && (o = "" + n), t.key !== void 0 && (o = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) Zt.call(t, r) && !Yt.hasOwnProperty(r) && (a[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) a[r] === void 0 && (a[r] = t[r]);
  return {
    $$typeof: Gt,
    type: e,
    key: o,
    ref: s,
    props: a,
    _owner: qt.current
  };
}
K.Fragment = Ht;
K.jsx = Et;
K.jsxs = Et;
kt.exports = K;
var I = kt.exports;
const {
  SvelteComponent: Jt,
  assign: it,
  binding_callbacks: lt,
  check_outros: Qt,
  children: St,
  claim_element: vt,
  claim_space: Xt,
  component_subscribe: ct,
  compute_slots: Vt,
  create_slot: $t,
  detach: C,
  element: Ct,
  empty: ut,
  exclude_internal_props: dt,
  get_all_dirty_from_scope: te,
  get_slot_changes: ee,
  group_outros: ne,
  init: re,
  insert_hydration: D,
  safe_not_equal: ae,
  set_custom_element_data: zt,
  space: oe,
  transition_in: N,
  transition_out: Q,
  update_slot_base: se
} = window.__gradio__svelte__internal, {
  beforeUpdate: ie,
  getContext: le,
  onDestroy: ce,
  setContext: ue
} = window.__gradio__svelte__internal;
function ft(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), a = $t(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Ct("svelte-slot"), a && a.c(), this.h();
    },
    l(o) {
      t = vt(o, "SVELTE-SLOT", {
        class: !0
      });
      var s = St(t);
      a && a.l(s), s.forEach(C), this.h();
    },
    h() {
      zt(t, "class", "svelte-1rt0kpf");
    },
    m(o, s) {
      D(o, t, s), a && a.m(t, null), e[9](t), n = !0;
    },
    p(o, s) {
      a && a.p && (!n || s & /*$$scope*/
      64) && se(
        a,
        r,
        o,
        /*$$scope*/
        o[6],
        n ? ee(
          r,
          /*$$scope*/
          o[6],
          s,
          null
        ) : te(
          /*$$scope*/
          o[6]
        ),
        null
      );
    },
    i(o) {
      n || (N(a, o), n = !0);
    },
    o(o) {
      Q(a, o), n = !1;
    },
    d(o) {
      o && C(t), a && a.d(o), e[9](null);
    }
  };
}
function de(e) {
  let t, n, r, a, o = (
    /*$$slots*/
    e[4].default && ft(e)
  );
  return {
    c() {
      t = Ct("react-portal-target"), n = oe(), o && o.c(), r = ut(), this.h();
    },
    l(s) {
      t = vt(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), St(t).forEach(C), n = Xt(s), o && o.l(s), r = ut(), this.h();
    },
    h() {
      zt(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      D(s, t, i), e[8](t), D(s, n, i), o && o.m(s, i), D(s, r, i), a = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? o ? (o.p(s, i), i & /*$$slots*/
      16 && N(o, 1)) : (o = ft(s), o.c(), N(o, 1), o.m(r.parentNode, r)) : o && (ne(), Q(o, 1, 1, () => {
        o = null;
      }), Qt());
    },
    i(s) {
      a || (N(o), a = !0);
    },
    o(s) {
      Q(o), a = !1;
    },
    d(s) {
      s && (C(t), C(n), C(r)), e[8](null), o && o.d(s);
    }
  };
}
function mt(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function fe(e, t, n) {
  let r, a, {
    $$slots: o = {},
    $$scope: s
  } = t;
  const i = Vt(o);
  let {
    svelteInit: l
  } = t;
  const w = x(mt(t)), d = x();
  ct(e, d, (c) => n(0, r = c));
  const p = x();
  ct(e, p, (c) => n(1, a = c));
  const u = [], _ = le("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: O,
    subSlotIndex: S
  } = Lt() || {}, v = l({
    parent: _,
    props: w,
    target: d,
    slot: p,
    slotKey: h,
    slotIndex: O,
    subSlotIndex: S,
    onDestroy(c) {
      u.push(c);
    }
  });
  ue("$$ms-gr-react-wrapper", v), ie(() => {
    w.set(mt(t));
  }), ce(() => {
    u.forEach((c) => c());
  });
  function P(c) {
    lt[c ? "unshift" : "push"](() => {
      r = c, d.set(r);
    });
  }
  function g(c) {
    lt[c ? "unshift" : "push"](() => {
      a = c, p.set(a);
    });
  }
  return e.$$set = (c) => {
    n(17, t = it(it({}, t), dt(c))), "svelteInit" in c && n(5, l = c.svelteInit), "$$scope" in c && n(6, s = c.$$scope);
  }, t = dt(t), [r, a, d, p, i, l, s, o, P, g];
}
class me extends Jt {
  constructor(t) {
    super(), re(this, t, fe, de, ae, {
      svelteInit: 5
    });
  }
}
const ht = window.ms_globals.rerender, H = window.ms_globals.tree;
function he(e) {
  function t(n) {
    const r = x(), a = new me({
      ...n,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            slotKey: o.slotKey,
            nodes: []
          }, i = o.parent ?? H;
          return i.nodes = [...i.nodes, s], ht({
            createPortal: J,
            node: H
          }), o.onDestroy(() => {
            i.nodes = i.nodes.filter((l) => l.svelteInstance !== r), ht({
              createPortal: J,
              node: H
            });
          }), s;
        },
        ...n.props
      }
    });
    return r.set(a), a;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ye(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return typeof r == "number" && !pe.includes(n) ? t[n] = r + "px" : t[n] = r, t;
  }, {}) : {};
}
function X(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(J(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: b.Children.toArray(e._reactElement.props.children).map((a) => {
        if (b.isValidElement(a) && a.props.__slot__) {
          const {
            portals: o,
            clonedElement: s
          } = X(a.props.el);
          return b.cloneElement(a, {
            ...a.props,
            el: s,
            children: [...b.Children.toArray(a.props.children), ...o]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((a) => {
    e.getEventListeners(a).forEach(({
      listener: s,
      type: i,
      useCapture: l
    }) => {
      n.addEventListener(i, s, l);
    });
  });
  const r = Array.from(e.childNodes);
  for (let a = 0; a < r.length; a++) {
    const o = r[a];
    if (o.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = X(o);
      t.push(...i), n.appendChild(s);
    } else o.nodeType === 3 && n.appendChild(o.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function _e(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Rt = Nt(({
  slot: e,
  clone: t,
  className: n,
  style: r
}, a) => {
  const o = Tt(), [s, i] = jt([]);
  return bt(() => {
    var p;
    if (!o.current || !e)
      return;
    let l = e;
    function w() {
      let u = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (u = l.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), _e(a, u), n && u.classList.add(...n.split(" ")), r) {
        const _ = ye(r);
        Object.keys(_).forEach((h) => {
          u.style[h] = _[h];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var S, v, P;
        (S = o.current) != null && S.contains(l) && ((v = o.current) == null || v.removeChild(l));
        const {
          portals: h,
          clonedElement: O
        } = X(e);
        return l = O, i(h), l.style.display = "contents", w(), (P = o.current) == null || P.appendChild(l), h.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      l.style.display = "contents", w(), (p = o.current) == null || p.appendChild(l);
    return () => {
      var u, _;
      l.style.display = "", (u = o.current) != null && u.contains(l) && ((_ = o.current) == null || _.removeChild(l)), d == null || d.disconnect();
    };
  }, [e, t, n, r, a]), b.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...s);
});
function we(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Pe(e, t = !1) {
  try {
    if (t && !we(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Z(e, t) {
  return Mt(() => Pe(e, t), [e, t]);
}
function ge(e, t) {
  return e ? /* @__PURE__ */ I.jsx(Rt, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function je({
  key: e,
  setSlotParams: t,
  slots: n
}, r) {
  return n[e] ? (...a) => (t(e, a), ge(n[e], {
    clone: !0,
    ...r
  })) : void 0;
}
var Ot = Symbol.for("immer-nothing"), pt = Symbol.for("immer-draftable"), f = Symbol.for("immer-state");
function y(e, ...t) {
  throw new Error(`[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`);
}
var z = Object.getPrototypeOf;
function R(e) {
  return !!e && !!e[f];
}
function k(e) {
  var t;
  return e ? It(e) || Array.isArray(e) || !!e[pt] || !!((t = e.constructor) != null && t[pt]) || W(e) || B(e) : !1;
}
var be = Object.prototype.constructor.toString();
function It(e) {
  if (!e || typeof e != "object") return !1;
  const t = z(e);
  if (t === null)
    return !0;
  const n = Object.hasOwnProperty.call(t, "constructor") && t.constructor;
  return n === Object ? !0 : typeof n == "function" && Function.toString.call(n) === be;
}
function T(e, t) {
  U(e) === 0 ? Reflect.ownKeys(e).forEach((n) => {
    t(n, e[n], e);
  }) : e.forEach((n, r) => t(r, n, e));
}
function U(e) {
  const t = e[f];
  return t ? t.type_ : Array.isArray(e) ? 1 : W(e) ? 2 : B(e) ? 3 : 0;
}
function V(e, t) {
  return U(e) === 2 ? e.has(t) : Object.prototype.hasOwnProperty.call(e, t);
}
function At(e, t, n) {
  const r = U(e);
  r === 2 ? e.set(t, n) : r === 3 ? e.add(n) : e[t] = n;
}
function ke(e, t) {
  return e === t ? e !== 0 || 1 / e === 1 / t : e !== e && t !== t;
}
function W(e) {
  return e instanceof Map;
}
function B(e) {
  return e instanceof Set;
}
function j(e) {
  return e.copy_ || e.base_;
}
function $(e, t) {
  if (W(e))
    return new Map(e);
  if (B(e))
    return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  const n = It(e);
  if (t === !0 || t === "class_only" && !n) {
    const r = Object.getOwnPropertyDescriptors(e);
    delete r[f];
    let a = Reflect.ownKeys(r);
    for (let o = 0; o < a.length; o++) {
      const s = a[o], i = r[s];
      i.writable === !1 && (i.writable = !0, i.configurable = !0), (i.get || i.set) && (r[s] = {
        configurable: !0,
        writable: !0,
        // could live with !!desc.set as well here...
        enumerable: i.enumerable,
        value: e[s]
      });
    }
    return Object.create(z(e), r);
  } else {
    const r = z(e);
    if (r !== null && n)
      return {
        ...e
      };
    const a = Object.create(r);
    return Object.assign(a, e);
  }
}
function at(e, t = !1) {
  return G(e) || R(e) || !k(e) || (U(e) > 1 && (e.set = e.add = e.clear = e.delete = Ee), Object.freeze(e), t && Object.entries(e).forEach(([n, r]) => at(r, !0))), e;
}
function Ee() {
  y(2);
}
function G(e) {
  return Object.isFrozen(e);
}
var Se = {};
function E(e) {
  const t = Se[e];
  return t || y(0, e), t;
}
var A;
function Ft() {
  return A;
}
function ve(e, t) {
  return {
    drafts_: [],
    parent_: e,
    immer_: t,
    // Whenever the modified draft contains a draft from another scope, we
    // need to prevent auto-freezing so the unowned draft can be finalized.
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0
  };
}
function yt(e, t) {
  t && (E("Patches"), e.patches_ = [], e.inversePatches_ = [], e.patchListener_ = t);
}
function tt(e) {
  et(e), e.drafts_.forEach(Ce), e.drafts_ = null;
}
function et(e) {
  e === A && (A = e.parent_);
}
function _t(e) {
  return A = ve(A, e);
}
function Ce(e) {
  const t = e[f];
  t.type_ === 0 || t.type_ === 1 ? t.revoke_() : t.revoked_ = !0;
}
function wt(e, t) {
  t.unfinalizedDrafts_ = t.drafts_.length;
  const n = t.drafts_[0];
  return e !== void 0 && e !== n ? (n[f].modified_ && (tt(t), y(4)), k(e) && (e = M(t, e), t.parent_ || L(t, e)), t.patches_ && E("Patches").generateReplacementPatches_(n[f].base_, e, t.patches_, t.inversePatches_)) : e = M(t, n, []), tt(t), t.patches_ && t.patchListener_(t.patches_, t.inversePatches_), e !== Ot ? e : void 0;
}
function M(e, t, n) {
  if (G(t)) return t;
  const r = t[f];
  if (!r)
    return T(t, (a, o) => Pt(e, r, t, a, o, n)), t;
  if (r.scope_ !== e) return t;
  if (!r.modified_)
    return L(e, r.base_, !0), r.base_;
  if (!r.finalized_) {
    r.finalized_ = !0, r.scope_.unfinalizedDrafts_--;
    const a = r.copy_;
    let o = a, s = !1;
    r.type_ === 3 && (o = new Set(a), a.clear(), s = !0), T(o, (i, l) => Pt(e, r, a, i, l, n, s)), L(e, a, !1), n && e.patches_ && E("Patches").generatePatches_(r, n, e.patches_, e.inversePatches_);
  }
  return r.copy_;
}
function Pt(e, t, n, r, a, o, s) {
  if (R(a)) {
    const i = o && t && t.type_ !== 3 && // Set objects are atomic since they have no keys.
    !V(t.assigned_, r) ? o.concat(r) : void 0, l = M(e, a, i);
    if (At(n, r, l), R(l))
      e.canAutoFreeze_ = !1;
    else return;
  } else s && n.add(a);
  if (k(a) && !G(a)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1)
      return;
    M(e, a), (!t || !t.scope_.parent_) && typeof r != "symbol" && Object.prototype.propertyIsEnumerable.call(n, r) && L(e, a);
  }
}
function L(e, t, n = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && at(t, n);
}
function ze(e, t) {
  const n = Array.isArray(e), r = {
    type_: n ? 1 : 0,
    // Track which produce call this is associated with.
    scope_: t ? t.scope_ : Ft(),
    // True for both shallow and deep changes.
    modified_: !1,
    // Used during finalization.
    finalized_: !1,
    // Track which properties have been assigned (true) or deleted (false).
    assigned_: {},
    // The parent draft state.
    parent_: t,
    // The base state.
    base_: e,
    // The base proxy.
    draft_: null,
    // set below
    // The base copy with any updated values.
    copy_: null,
    // Called by the `produce` function.
    revoke_: null,
    isManual_: !1
  };
  let a = r, o = ot;
  n && (a = [r], o = F);
  const {
    revoke: s,
    proxy: i
  } = Proxy.revocable(a, o);
  return r.draft_ = i, r.revoke_ = s, i;
}
var ot = {
  get(e, t) {
    if (t === f) return e;
    const n = j(e);
    if (!V(n, t))
      return Re(e, n, t);
    const r = n[t];
    return e.finalized_ || !k(r) ? r : r === q(e.base_, t) ? (Y(e), e.copy_[t] = rt(r, e)) : r;
  },
  has(e, t) {
    return t in j(e);
  },
  ownKeys(e) {
    return Reflect.ownKeys(j(e));
  },
  set(e, t, n) {
    const r = xt(j(e), t);
    if (r != null && r.set)
      return r.set.call(e.draft_, n), !0;
    if (!e.modified_) {
      const a = q(j(e), t), o = a == null ? void 0 : a[f];
      if (o && o.base_ === n)
        return e.copy_[t] = n, e.assigned_[t] = !1, !0;
      if (ke(n, a) && (n !== void 0 || V(e.base_, t))) return !0;
      Y(e), nt(e);
    }
    return e.copy_[t] === n && // special case: handle new props with value 'undefined'
    (n !== void 0 || t in e.copy_) || // special case: NaN
    Number.isNaN(n) && Number.isNaN(e.copy_[t]) || (e.copy_[t] = n, e.assigned_[t] = !0), !0;
  },
  deleteProperty(e, t) {
    return q(e.base_, t) !== void 0 || t in e.base_ ? (e.assigned_[t] = !1, Y(e), nt(e)) : delete e.assigned_[t], e.copy_ && delete e.copy_[t], !0;
  },
  // Note: We never coerce `desc.value` into an Immer draft, because we can't make
  // the same guarantee in ES5 mode.
  getOwnPropertyDescriptor(e, t) {
    const n = j(e), r = Reflect.getOwnPropertyDescriptor(n, t);
    return r && {
      writable: !0,
      configurable: e.type_ !== 1 || t !== "length",
      enumerable: r.enumerable,
      value: n[t]
    };
  },
  defineProperty() {
    y(11);
  },
  getPrototypeOf(e) {
    return z(e.base_);
  },
  setPrototypeOf() {
    y(12);
  }
}, F = {};
T(ot, (e, t) => {
  F[e] = function() {
    return arguments[0] = arguments[0][0], t.apply(this, arguments);
  };
});
F.deleteProperty = function(e, t) {
  return F.set.call(this, e, t, void 0);
};
F.set = function(e, t, n) {
  return ot.set.call(this, e[0], t, n, e[0]);
};
function q(e, t) {
  const n = e[f];
  return (n ? j(n) : e)[t];
}
function Re(e, t, n) {
  var a;
  const r = xt(t, n);
  return r ? "value" in r ? r.value : (
    // This is a very special case, if the prop is a getter defined by the
    // prototype, we should invoke it with the draft as context!
    (a = r.get) == null ? void 0 : a.call(e.draft_)
  ) : void 0;
}
function xt(e, t) {
  if (!(t in e)) return;
  let n = z(e);
  for (; n; ) {
    const r = Object.getOwnPropertyDescriptor(n, t);
    if (r) return r;
    n = z(n);
  }
}
function nt(e) {
  e.modified_ || (e.modified_ = !0, e.parent_ && nt(e.parent_));
}
function Y(e) {
  e.copy_ || (e.copy_ = $(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var Oe = class {
  constructor(e) {
    this.autoFreeze_ = !0, this.useStrictShallowCopy_ = !1, this.produce = (t, n, r) => {
      if (typeof t == "function" && typeof n != "function") {
        const o = n;
        n = t;
        const s = this;
        return function(l = o, ...w) {
          return s.produce(l, (d) => n.call(this, d, ...w));
        };
      }
      typeof n != "function" && y(6), r !== void 0 && typeof r != "function" && y(7);
      let a;
      if (k(t)) {
        const o = _t(this), s = rt(t, void 0);
        let i = !0;
        try {
          a = n(s), i = !1;
        } finally {
          i ? tt(o) : et(o);
        }
        return yt(o, r), wt(a, o);
      } else if (!t || typeof t != "object") {
        if (a = n(t), a === void 0 && (a = t), a === Ot && (a = void 0), this.autoFreeze_ && at(a, !0), r) {
          const o = [], s = [];
          E("Patches").generateReplacementPatches_(t, a, o, s), r(o, s);
        }
        return a;
      } else y(1, t);
    }, this.produceWithPatches = (t, n) => {
      if (typeof t == "function")
        return (s, ...i) => this.produceWithPatches(s, (l) => t(l, ...i));
      let r, a;
      return [this.produce(t, n, (s, i) => {
        r = s, a = i;
      }), r, a];
    }, typeof (e == null ? void 0 : e.autoFreeze) == "boolean" && this.setAutoFreeze(e.autoFreeze), typeof (e == null ? void 0 : e.useStrictShallowCopy) == "boolean" && this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    k(e) || y(8), R(e) && (e = Ie(e));
    const t = _t(this), n = rt(e, void 0);
    return n[f].isManual_ = !0, et(t), n;
  }
  finishDraft(e, t) {
    const n = e && e[f];
    (!n || !n.isManual_) && y(9);
    const {
      scope_: r
    } = n;
    return yt(r, t), wt(void 0, r);
  }
  /**
   * Pass true to automatically freeze all copies created by Immer.
   *
   * By default, auto-freezing is enabled.
   */
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  /**
   * Pass true to enable strict shallow copy.
   *
   * By default, immer does not copy the object descriptors such as getter, setter and non-enumrable properties.
   */
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, t) {
    let n;
    for (n = t.length - 1; n >= 0; n--) {
      const a = t[n];
      if (a.path.length === 0 && a.op === "replace") {
        e = a.value;
        break;
      }
    }
    n > -1 && (t = t.slice(n + 1));
    const r = E("Patches").applyPatches_;
    return R(e) ? r(e, t) : this.produce(e, (a) => r(a, t));
  }
};
function rt(e, t) {
  const n = W(e) ? E("MapSet").proxyMap_(e, t) : B(e) ? E("MapSet").proxySet_(e, t) : ze(e, t);
  return (t ? t.scope_ : Ft()).drafts_.push(n), n;
}
function Ie(e) {
  return R(e) || y(10, e), Dt(e);
}
function Dt(e) {
  if (!k(e) || G(e)) return e;
  const t = e[f];
  let n;
  if (t) {
    if (!t.modified_) return t.base_;
    t.finalized_ = !0, n = $(e, t.scope_.immer_.useStrictShallowCopy_);
  } else
    n = $(e, !0);
  return T(n, (r, a) => {
    At(n, r, Dt(a));
  }), t && (t.finalized_ = !1), n;
}
var m = new Oe(), Ae = m.produce;
m.produceWithPatches.bind(m);
m.setAutoFreeze.bind(m);
m.setUseStrictShallowCopy.bind(m);
m.applyPatches.bind(m);
m.createDraft.bind(m);
m.finishDraft.bind(m);
const gt = {
  ar_EG: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ar_EG-DO-ArTTK.js").then((t) => t.a), import("./ar-fHCIoPj1.js").then((t) => t.a)]);
    return {
      antd: e,
      dayjs: "ar"
    };
  },
  az_AZ: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./az_AZ-CmxjyTZw.js").then((t) => t.a), import("./az-CHu-TzEr.js").then((t) => t.a)]);
    return {
      antd: e,
      dayjs: "az"
    };
  },
  bg_BG: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./bg_BG-CyW5YvZJ.js").then((t) => t.b), import("./bg-Ki7juQFr.js").then((t) => t.b)]);
    return {
      antd: e,
      dayjs: "bg"
    };
  },
  bn_BD: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./bn_BD-BDGhtkqA.js").then((t) => t.b), import("./bn-C1rOaf3l.js").then((t) => t.b)]);
    return {
      antd: e,
      dayjs: "bn"
    };
  },
  by_BY: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./by_BY-ama9WtwA.js").then((t) => t.b),
      import("./be-BE1aa8rz.js").then((t) => t.b)
      // Belarusian (Belarus)
    ]);
    return {
      antd: e,
      dayjs: "be"
    };
  },
  ca_ES: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ca_ES-H92AVP9N.js").then((t) => t.c), import("./ca-C9IDu_bB.js").then((t) => t.c)]);
    return {
      antd: e,
      dayjs: "ca"
    };
  },
  cs_CZ: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./cs_CZ-CTY8PaHU.js").then((t) => t.c), import("./cs-ErUXsaT4.js").then((t) => t.c)]);
    return {
      antd: e,
      dayjs: "cs"
    };
  },
  da_DK: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./da_DK-yXSPiiWv.js").then((t) => t.d), import("./da-Cqgr1RF1.js").then((t) => t.d)]);
    return {
      antd: e,
      dayjs: "da"
    };
  },
  de_DE: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./de_DE-LDhTypJY.js").then((t) => t.d), import("./de-CZIUEwzF.js").then((t) => t.d)]);
    return {
      antd: e,
      dayjs: "de"
    };
  },
  el_GR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./el_GR-D3rI11fD.js").then((t) => t.e), import("./el-CqZBjTaR.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "el"
    };
  },
  en_GB: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./en_GB-D9ymhIXw.js").then((t) => t.e), import("./en-gb-BK7lkBEM.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "en-gb"
    };
  },
  en_US: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./en_US-D1lif_4a.js").then((t) => t.e), import("./en-C9kdNcZT.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "en"
    };
  },
  es_ES: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./es_ES-DfXHQrzw.js").then((t) => t.e), import("./es-C_82KqP5.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "es"
    };
  },
  et_EE: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./et_EE-uJwB5F4c.js").then((t) => t.e), import("./et-BWCRlzrm.js").then((t) => t.e)]);
    return {
      antd: e,
      dayjs: "et"
    };
  },
  eu_ES: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./eu_ES-CZ65MvkL.js").then((t) => t.e),
      import("./eu-xv7cVpe1.js").then((t) => t.e)
      // Basque
    ]);
    return {
      antd: e,
      dayjs: "eu"
    };
  },
  fa_IR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fa_IR-DX_e7u3_.js").then((t) => t.f), import("./fa-Gar8mkDa.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fa"
    };
  },
  fi_FI: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fi_FI-B2TeGHEN.js").then((t) => t.f), import("./fi-C7QCr8sc.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fi"
    };
  },
  fr_BE: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fr_BE-DmOGZhKI.js").then((t) => t.f), import("./fr-o_wEfDZY.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fr"
    };
  },
  fr_CA: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fr_CA-D3r53GJO.js").then((t) => t.f), import("./fr-ca-_BfJmq_c.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fr-ca"
    };
  },
  fr_FR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./fr_FR-CBcnvBL1.js").then((t) => t.f), import("./fr-o_wEfDZY.js").then((t) => t.f)]);
    return {
      antd: e,
      dayjs: "fr"
    };
  },
  ga_IE: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ga_IE-Ds3vOZir.js").then((t) => t.g),
      import("./ga-ChwAhbI7.js").then((t) => t.g)
      // Irish
    ]);
    return {
      antd: e,
      dayjs: "ga"
    };
  },
  gl_ES: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./gl_ES-BljlysPn.js").then((t) => t.g),
      import("./gl-DfOhxE0o.js").then((t) => t.g)
      // Galician
    ]);
    return {
      antd: e,
      dayjs: "gl"
    };
  },
  he_IL: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./he_IL-pYPDsdeN.js").then((t) => t.h), import("./he-DpFVe75N.js").then((t) => t.h)]);
    return {
      antd: e,
      dayjs: "he"
    };
  },
  hi_IN: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./hi_IN-CPcBMdNz.js").then((t) => t.h), import("./hi-BvcmFPyT.js").then((t) => t.h)]);
    return {
      antd: e,
      dayjs: "hi"
    };
  },
  hr_HR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./hr_HR-CoP48iRO.js").then((t) => t.h), import("./hr-JvmZq_N8.js").then((t) => t.h)]);
    return {
      antd: e,
      dayjs: "hr"
    };
  },
  hu_HU: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./hu_HU-Bsog27Ld.js").then((t) => t.h), import("./hu-CtObzcCu.js").then((t) => t.h)]);
    return {
      antd: e,
      dayjs: "hu"
    };
  },
  hy_AM: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./hy_AM-YCELCFUb.js").then((t) => t.h),
      import("./am-DNR8PxDz.js").then((t) => t.a)
      // Armenian
    ]);
    return {
      antd: e,
      dayjs: "am"
    };
  },
  id_ID: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./id_ID-UcXhie9S.js").then((t) => t.i), import("./id-DGSUgL3l.js").then((t) => t.i)]);
    return {
      antd: e,
      dayjs: "id"
    };
  },
  is_IS: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./is_IS-CG6f1eV2.js").then((t) => t.i), import("./is-C3F-3gcL.js").then((t) => t.i)]);
    return {
      antd: e,
      dayjs: "is"
    };
  },
  it_IT: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./it_IT-DOPFrKEx.js").then((t) => t.i), import("./it-CQM_jLxk.js").then((t) => t.i)]);
    return {
      antd: e,
      dayjs: "it"
    };
  },
  ja_JP: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ja_JP-EKkCRaFs.js").then((t) => t.j), import("./ja-OXnSatLU.js").then((t) => t.j)]);
    return {
      antd: e,
      dayjs: "ja"
    };
  },
  ka_GE: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ka_GE-dlJbix0q.js").then((t) => t.k),
      import("./ka-D01MHsQd.js").then((t) => t.k)
      // Georgian
    ]);
    return {
      antd: e,
      dayjs: "ka"
    };
  },
  kk_KZ: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./kk_KZ-Fc7oSN6p.js").then((t) => t.k),
      import("./kk-BeUc3-Kt.js").then((t) => t.k)
      // Kazakh
    ]);
    return {
      antd: e,
      dayjs: "kk"
    };
  },
  km_KH: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./km_KH-DsebTA1-.js").then((t) => t.k),
      import("./km-CST9evMk.js").then((t) => t.k)
      // Khmer
    ]);
    return {
      antd: e,
      dayjs: "km"
    };
  },
  kmr_IQ: async () => {
    const [e] = await Promise.all([
      import("./kmr_IQ-CVJiNGGJ.js").then((t) => t.k)
      // Not available in Day.js, so no need to load a locale file.
    ]);
    return {
      antd: e.default,
      dayjs: ""
    };
  },
  kn_IN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./kn_IN-aBqQyBzP.js").then((t) => t.k),
      import("./kn-D14OodGe.js").then((t) => t.k)
      // Kannada
    ]);
    return {
      antd: e,
      dayjs: "kn"
    };
  },
  ko_KR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ko_KR-C2-SGFpb.js").then((t) => t.k), import("./ko-qmu-pQZW.js").then((t) => t.k)]);
    return {
      antd: e,
      dayjs: "ko"
    };
  },
  ku_IQ: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ku_IQ-BdV_DagW.js").then((t) => t.k),
      import("./ku-D2AQOnqx.js").then((t) => t.k)
      // Kurdish (Central)
    ]);
    return {
      antd: e,
      dayjs: "ku"
    };
  },
  lt_LT: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./lt_LT-BJg53765.js").then((t) => t.l), import("./lt-DIzAp-Wr.js").then((t) => t.l)]);
    return {
      antd: e,
      dayjs: "lt"
    };
  },
  lv_LV: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./lv_LV-BdkLQ1fn.js").then((t) => t.l), import("./lv-DA__conM.js").then((t) => t.l)]);
    return {
      antd: e,
      dayjs: "lv"
    };
  },
  mk_MK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./mk_MK-FXHdHBnc.js").then((t) => t.m),
      import("./mk-3yvcwX1A.js").then((t) => t.m)
      // Macedonian
    ]);
    return {
      antd: e,
      dayjs: "mk"
    };
  },
  ml_IN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ml_IN-DfwPZ3mL.js").then((t) => t.m),
      import("./ml-C6uodhEA.js").then((t) => t.m)
      // Malayalam
    ]);
    return {
      antd: e,
      dayjs: "ml"
    };
  },
  mn_MN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./mn_MN-CJTIAk2g.js").then((t) => t.m),
      import("./mn-Br3uVOcm.js").then((t) => t.m)
      // Mongolian
    ]);
    return {
      antd: e,
      dayjs: "mn"
    };
  },
  ms_MY: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ms_MY-BK7czGmE.js").then((t) => t.m), import("./ms-DUJTUpGS.js").then((t) => t.m)]);
    return {
      antd: e,
      dayjs: "ms"
    };
  },
  my_MM: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./my_MM-D2f7K8CI.js").then((t) => t.m),
      import("./my-BlYbBFWN.js").then((t) => t.m)
      // Burmese
    ]);
    return {
      antd: e,
      dayjs: "my"
    };
  },
  nb_NO: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./nb_NO-D1NasaRc.js").then((t) => t.n),
      import("./nb-CcJ_SHYm.js").then((t) => t.n)
      // Norwegian Bokmål
    ]);
    return {
      antd: e,
      dayjs: "nb"
    };
  },
  ne_NP: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ne_NP-UbT0H-i9.js").then((t) => t.n),
      import("./ne-bZC4Q4ac.js").then((t) => t.n)
      // Nepali
    ]);
    return {
      antd: e,
      dayjs: "ne"
    };
  },
  nl_BE: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./nl_BE-BE2M4bSq.js").then((t) => t.n),
      import("./nl-be-CKLBpK02.js").then((t) => t.n)
      // Dutch (Belgium)
    ]);
    return {
      antd: e,
      dayjs: "nl-be"
    };
  },
  nl_NL: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./nl_NL-B9ff-nBQ.js").then((t) => t.n),
      import("./nl-CsjU8QP-.js").then((t) => t.n)
      // Dutch (Netherlands)
    ]);
    return {
      antd: e,
      dayjs: "nl"
    };
  },
  pl_PL: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./pl_PL-XH6pkTU5.js").then((t) => t.p), import("./pl-C3lv5Bkp.js").then((t) => t.p)]);
    return {
      antd: e,
      dayjs: "pl"
    };
  },
  pt_BR: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./pt_BR-Dw8BR5p-.js").then((t) => t.p),
      import("./pt-br-CVPdzmE8.js").then((t) => t.p)
      // Portuguese (Brazil)
    ]);
    return {
      antd: e,
      dayjs: "pt-br"
    };
  },
  pt_PT: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./pt_PT-Bbr6ivrN.js").then((t) => t.p),
      import("./pt-uJBIZHD2.js").then((t) => t.p)
      // Portuguese (Portugal)
    ]);
    return {
      antd: e,
      dayjs: "pt"
    };
  },
  ro_RO: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ro_RO-BJxPKb_l.js").then((t) => t.r), import("./ro-DzPTaGwe.js").then((t) => t.r)]);
    return {
      antd: e,
      dayjs: "ro"
    };
  },
  ru_RU: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./ru_RU-B8uRcYyY.js").then((t) => t.r), import("./ru-BXruTxqU.js").then((t) => t.r)]);
    return {
      antd: e,
      dayjs: "ru"
    };
  },
  si_LK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./si_LK-Dk53O5L6.js").then((t) => t.s),
      import("./si-4rgV0Iqe.js").then((t) => t.s)
      // Sinhala
    ]);
    return {
      antd: e,
      dayjs: "si"
    };
  },
  sk_SK: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./sk_SK-DwNUGqtp.js").then((t) => t.s), import("./sk-BzhjA3mo.js").then((t) => t.s)]);
    return {
      antd: e,
      dayjs: "sk"
    };
  },
  sl_SI: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./sl_SI-B8rTBmFC.js").then((t) => t.s), import("./sl-v9DC-lpy.js").then((t) => t.s)]);
    return {
      antd: e,
      dayjs: "sl"
    };
  },
  sr_RS: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./sr_RS-CCgN6VII.js").then((t) => t.s),
      import("./sr-Vm9Pfp-_.js").then((t) => t.s)
      // Serbian
    ]);
    return {
      antd: e,
      dayjs: "sr"
    };
  },
  sv_SE: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./sv_SE-BW53CLx0.js").then((t) => t.s), import("./sv-DR5Zq5zc.js").then((t) => t.s)]);
    return {
      antd: e,
      dayjs: "sv"
    };
  },
  ta_IN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ta_IN-BgMFFtCc.js").then((t) => t.t),
      import("./ta-HXOxodHI.js").then((t) => t.t)
      // Tamil
    ]);
    return {
      antd: e,
      dayjs: "ta"
    };
  },
  th_TH: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./th_TH-BW7lyZYJ.js").then((t) => t.t), import("./th-BonHWIYs.js").then((t) => t.t)]);
    return {
      antd: e,
      dayjs: "th"
    };
  },
  tk_TK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./tk_TK-BX3j51LJ.js").then((t) => t.t),
      import("./tk-Bzial4cQ.js").then((t) => t.t)
      // Turkmen
    ]);
    return {
      antd: e,
      dayjs: "tk"
    };
  },
  tr_TR: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./tr_TR-BjiunR6z.js").then((t) => t.t), import("./tr-BRD3m_gn.js").then((t) => t.t)]);
    return {
      antd: e,
      dayjs: "tr"
    };
  },
  uk_UA: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./uk_UA-VaFk82-6.js").then((t) => t.u),
      import("./uk-TNXkIB0g.js").then((t) => t.u)
      // Ukrainian
    ]);
    return {
      antd: e,
      dayjs: "uk"
    };
  },
  ur_PK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./ur_PK-DM3nhDdx.js").then((t) => t.u),
      import("./ur-DO-MGqaC.js").then((t) => t.u)
      // Urdu
    ]);
    return {
      antd: e,
      dayjs: "ur"
    };
  },
  uz_UZ: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./uz_UZ-DizjzUMc.js").then((t) => t.u),
      import("./uz-CvDWSM3I.js").then((t) => t.u)
      // Uzbek
    ]);
    return {
      antd: e,
      dayjs: "uz"
    };
  },
  vi_VN: async () => {
    const [{
      default: e
    }] = await Promise.all([import("./vi_VN-CLr_gy3O.js").then((t) => t.v), import("./vi-lCWo2gkP.js").then((t) => t.v)]);
    return {
      antd: e,
      dayjs: "vi"
    };
  },
  zh_CN: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./zh_CN-CGxvWhH0.js").then((t) => t.z),
      import("./zh-cn-OYVkFCuz.js").then((t) => t.z)
      // Chinese (Simplified)
    ]);
    return {
      antd: e,
      dayjs: "zh-cn"
    };
  },
  zh_HK: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./zh_HK-lnRDq4Wa.js").then((t) => t.z),
      import("./zh-hk-BRyGDJu7.js").then((t) => t.z)
      // Chinese (Hong Kong)
    ]);
    return {
      antd: e,
      dayjs: "zh-hk"
    };
  },
  zh_TW: async () => {
    const [{
      default: e
    }] = await Promise.all([
      import("./zh_TW-BTxsuZrT.js").then((t) => t.z),
      import("./zh-tw-amU42Miv.js").then((t) => t.z)
      // Chinese (Taiwan)
    ]);
    return {
      antd: e,
      dayjs: "zh-tw"
    };
  }
}, Fe = (e, t) => Ae(e, (n) => {
  Object.keys(t).forEach((r) => {
    const a = r.split(".");
    let o = n;
    for (let s = 0; s < a.length - 1; s++) {
      const i = a[s];
      o[i] || (o[i] = {}), o = o[i];
    }
    o[a[a.length - 1]] = /* @__PURE__ */ I.jsx(Rt, {
      slot: t[r],
      clone: !0
    });
  });
}), De = he(({
  slots: e,
  themeMode: t,
  id: n,
  className: r,
  style: a,
  locale: o,
  getTargetContainer: s,
  getPopupContainer: i,
  renderEmpty: l,
  setSlotParams: w,
  children: d,
  ...p
}) => {
  var P;
  const [u, _] = jt(), h = {
    dark: t === "dark",
    ...((P = p.theme) == null ? void 0 : P.algorithm) || {}
  }, O = Z(i), S = Z(s), v = Z(l);
  return bt(() => {
    o && gt[o] && gt[o]().then(({
      antd: g,
      dayjs: c
    }) => {
      _(g), Wt.locale(c);
    });
  }, [o]), /* @__PURE__ */ I.jsx("div", {
    id: n,
    className: r,
    style: a,
    children: /* @__PURE__ */ I.jsx(Kt, {
      hashPriority: "high",
      container: document.body,
      children: /* @__PURE__ */ I.jsx(Ut, {
        prefixCls: "ms-gr-ant",
        ...Fe(p, e),
        locale: u,
        getPopupContainer: O,
        getTargetContainer: S,
        renderEmpty: e.renderEmpty ? je({
          slots: e,
          setSlotParams: w,
          key: "renderEmpty"
        }) : v,
        theme: {
          cssVar: !0,
          ...p.theme,
          algorithm: Object.keys(h).map((g) => {
            switch (g) {
              case "dark":
                return h[g] ? st.darkAlgorithm : null;
              case "compact":
                return h[g] ? st.compactAlgorithm : null;
              default:
                return null;
            }
          }).filter(Boolean)
        },
        children: d
      })
    })
  });
});
export {
  De as ConfigProvider,
  De as default
};
