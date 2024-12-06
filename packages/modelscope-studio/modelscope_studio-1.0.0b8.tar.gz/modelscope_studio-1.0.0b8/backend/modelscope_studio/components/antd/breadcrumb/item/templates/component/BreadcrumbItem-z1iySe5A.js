import { g as Fe, b as Ne } from "./Index-DrUBzDkG.js";
const I = window.ms_globals.React, Ke = window.ms_globals.React.forwardRef, Le = window.ms_globals.React.useRef, Ae = window.ms_globals.React.useState, Me = window.ms_globals.React.useEffect, qe = window.ms_globals.ReactDOM.createPortal;
function Be(e) {
  return e === void 0;
}
function k() {
}
function Te(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function We(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return k;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function x(e) {
  let t;
  return We(e, (n) => t = n)(), t;
}
const C = [];
function y(e, t = k) {
  let n;
  const s = /* @__PURE__ */ new Set();
  function r(l) {
    if (Te(e, l) && (e = l, n)) {
      const u = !C.length;
      for (const a of s)
        a[1](), C.push(a, e);
      if (u) {
        for (let a = 0; a < C.length; a += 2)
          C[a][0](C[a + 1]);
        C.length = 0;
      }
    }
  }
  function o(l) {
    r(l(e));
  }
  function i(l, u = k) {
    const a = [l, u];
    return s.add(a), s.size === 1 && (n = t(r, o) || k), l(e), () => {
      s.delete(a), s.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: r,
    update: o,
    subscribe: i
  };
}
const {
  getContext: ze,
  setContext: Kt
} = window.__gradio__svelte__internal, De = "$$ms-gr-loading-status-key";
function Ue() {
  const e = window.ms_globals.loadingKey++, t = ze(De);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: s,
      options: r
    } = t, {
      generating: o,
      error: i
    } = x(r);
    (n == null ? void 0 : n.status) === "pending" || i && (n == null ? void 0 : n.status) === "error" || (o && (n == null ? void 0 : n.status)) === "generating" ? s.update(({
      map: l
    }) => (l.set(e, n), {
      map: l
    })) : s.update(({
      map: l
    }) => (l.delete(e), {
      map: l
    }));
  };
}
const {
  getContext: D,
  setContext: R
} = window.__gradio__svelte__internal, Ge = "$$ms-gr-slots-key";
function He() {
  const e = y({});
  return R(Ge, e);
}
const Je = "$$ms-gr-render-slot-context-key";
function Ye() {
  const e = R(Je, y({}));
  return (t, n) => {
    e.update((s) => typeof n == "function" ? {
      ...s,
      [t]: n(s[t])
    } : {
      ...s,
      [t]: n
    });
  };
}
const Qe = "$$ms-gr-context-key";
function L(e) {
  return Be(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const Ie = "$$ms-gr-sub-index-context-key";
function Xe() {
  return D(Ie) || null;
}
function be(e) {
  return R(Ie, e);
}
function Ze(e, t, n) {
  var m, g;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const s = Ee(), r = et({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), o = Xe();
  typeof o == "number" && be(void 0);
  const i = Ue();
  typeof e._internal.subIndex == "number" && be(e._internal.subIndex), s && s.subscribe((c) => {
    r.slotKey.set(c);
  }), Ve();
  const l = D(Qe), u = ((m = x(l)) == null ? void 0 : m.as_item) || e.as_item, a = L(l ? u ? ((g = x(l)) == null ? void 0 : g[u]) || {} : x(l) || {} : {}), f = (c, p) => c ? Fe({
    ...c,
    ...p || {}
  }, t) : void 0, _ = y({
    ...e,
    _internal: {
      ...e._internal,
      index: o ?? e._internal.index
    },
    ...a,
    restProps: f(e.restProps, a),
    originalRestProps: e.restProps
  });
  return l ? (l.subscribe((c) => {
    const {
      as_item: p
    } = x(_);
    p && (c = c == null ? void 0 : c[p]), c = L(c), _.update((h) => ({
      ...h,
      ...c || {},
      restProps: f(h.restProps, c)
    }));
  }), [_, (c) => {
    var h, b;
    const p = L(c.as_item ? ((h = x(l)) == null ? void 0 : h[c.as_item]) || {} : x(l) || {});
    return i((b = c.restProps) == null ? void 0 : b.loading_status), _.set({
      ...c,
      _internal: {
        ...c._internal,
        index: o ?? c._internal.index
      },
      ...p,
      restProps: f(c.restProps, p),
      originalRestProps: c.restProps
    });
  }]) : [_, (c) => {
    var p;
    i((p = c.restProps) == null ? void 0 : p.loading_status), _.set({
      ...c,
      _internal: {
        ...c._internal,
        index: o ?? c._internal.index
      },
      restProps: f(c.restProps),
      originalRestProps: c.restProps
    });
  }];
}
const Ce = "$$ms-gr-slot-key";
function Ve() {
  R(Ce, y(void 0));
}
function Ee() {
  return D(Ce);
}
const $e = "$$ms-gr-component-slot-context-key";
function et({
  slot: e,
  index: t,
  subIndex: n
}) {
  return R($e, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(n)
  });
}
function tt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function nt(e, t = !1) {
  try {
    if (t && !tt(e))
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
function rt(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Re = {
  exports: {}
}, N = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var st = I, ot = Symbol.for("react.element"), it = Symbol.for("react.fragment"), lt = Object.prototype.hasOwnProperty, ct = st.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ut = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Se(e, t, n) {
  var s, r = {}, o = null, i = null;
  n !== void 0 && (o = "" + n), t.key !== void 0 && (o = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (s in t) lt.call(t, s) && !ut.hasOwnProperty(s) && (r[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ot,
    type: e,
    key: o,
    ref: i,
    props: r,
    _owner: ct.current
  };
}
N.Fragment = it;
N.jsx = Se;
N.jsxs = Se;
Re.exports = N;
var M = Re.exports;
const dt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ft(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const s = e[n];
    return typeof s == "number" && !dt.includes(n) ? t[n] = s + "px" : t[n] = s, t;
  }, {}) : {};
}
function q(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(qe(I.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: I.Children.toArray(e._reactElement.props.children).map((r) => {
        if (I.isValidElement(r) && r.props.__slot__) {
          const {
            portals: o,
            clonedElement: i
          } = q(r.props.el);
          return I.cloneElement(r, {
            ...r.props,
            el: i,
            children: [...I.Children.toArray(r.props.children), ...o]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: i,
      type: l,
      useCapture: u
    }) => {
      n.addEventListener(l, i, u);
    });
  });
  const s = Array.from(e.childNodes);
  for (let r = 0; r < s.length; r++) {
    const o = s[r];
    if (o.nodeType === 1) {
      const {
        clonedElement: i,
        portals: l
      } = q(o);
      t.push(...l), n.appendChild(i);
    } else o.nodeType === 3 && n.appendChild(o.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function at(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const B = Ke(({
  slot: e,
  clone: t,
  className: n,
  style: s
}, r) => {
  const o = Le(), [i, l] = Ae([]);
  return Me(() => {
    var _;
    if (!o.current || !e)
      return;
    let u = e;
    function a() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), at(r, m), n && m.classList.add(...n.split(" ")), s) {
        const g = ft(s);
        Object.keys(g).forEach((c) => {
          m.style[c] = g[c];
        });
      }
    }
    let f = null;
    if (t && window.MutationObserver) {
      let m = function() {
        var h, b, w;
        (h = o.current) != null && h.contains(u) && ((b = o.current) == null || b.removeChild(u));
        const {
          portals: c,
          clonedElement: p
        } = q(e);
        return u = p, l(c), u.style.display = "contents", a(), (w = o.current) == null || w.appendChild(u), c.length > 0;
      };
      m() || (f = new window.MutationObserver(() => {
        m() && (f == null || f.disconnect());
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      u.style.display = "contents", a(), (_ = o.current) == null || _.appendChild(u);
    return () => {
      var m, g;
      u.style.display = "", (m = o.current) != null && m.contains(u) && ((g = o.current) == null || g.removeChild(u)), f == null || f.disconnect();
    };
  }, [e, t, n, s, r]), I.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...i);
}), {
  getContext: mt,
  setContext: pt
} = window.__gradio__svelte__internal;
function Oe(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(r = ["default"]) {
    const o = r.reduce((i, l) => (i[l] = y([]), i), {});
    return pt(t, {
      itemsMap: o,
      allowedSlots: r
    }), o;
  }
  function s() {
    const {
      itemsMap: r,
      allowedSlots: o
    } = mt(t);
    return function(i, l, u) {
      r && (i ? r[i].update((a) => {
        const f = [...a];
        return o.includes(i) ? f[l] = u : f[l] = void 0, f;
      }) : o.includes("default") && r.default.update((a) => {
        const f = [...a];
        return f[l] = u, f;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: s
  };
}
function T(e, t, n) {
  const s = e.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, o) => {
      var a;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const i = {
        ...r.props,
        key: ((a = r.props) == null ? void 0 : a.key) ?? (n ? `${n}-${o}` : `${o}`)
      };
      let l = i;
      Object.keys(r.slots).forEach((f) => {
        if (!r.slots[f] || !(r.slots[f] instanceof Element) && !r.slots[f].el)
          return;
        const _ = f.split(".");
        _.forEach((h, b) => {
          l[h] || (l[h] = {}), b !== _.length - 1 && (l = i[h]);
        });
        const m = r.slots[f];
        let g, c, p = (t == null ? void 0 : t.clone) ?? !1;
        m instanceof Element ? g = m : (g = m.el, c = m.callback, p = m.clone ?? p), l[_[_.length - 1]] = g ? c ? (...h) => (c(_[_.length - 1], h), /* @__PURE__ */ M.jsx(B, {
          slot: g,
          clone: p
        })) : /* @__PURE__ */ M.jsx(B, {
          slot: g,
          clone: p
        }) : l[_[_.length - 1]], l = i;
      });
      const u = (t == null ? void 0 : t.children) || "children";
      return r[u] && (i[u] = T(r[u], t, `${o}`)), i;
    });
}
function W(e, t) {
  return e ? /* @__PURE__ */ M.jsx(B, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function A({
  key: e,
  setSlotParams: t,
  slots: n
}, s) {
  return n[e] ? (...r) => (t(e, r), W(n[e], {
    clone: !0,
    ...s
  })) : void 0;
}
var ve = {
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
      for (var o = "", i = 0; i < arguments.length; i++) {
        var l = arguments[i];
        l && (o = r(o, s(l)));
      }
      return o;
    }
    function s(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return n.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var i = "";
      for (var l in o)
        t.call(o, l) && o[l] && (i = r(i, l));
      return i;
    }
    function r(o, i) {
      return i ? o ? o + " " + i : o + i : o;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(ve);
var _t = ve.exports;
const gt = /* @__PURE__ */ rt(_t), {
  getItems: ht,
  getSetItemFn: Lt
} = Oe("menu"), {
  getItems: At,
  getSetItemFn: bt
} = Oe("breadcrumb"), {
  SvelteComponent: yt,
  assign: ye,
  check_outros: Pt,
  component_subscribe: E,
  compute_rest_props: Pe,
  create_slot: wt,
  detach: xt,
  empty: we,
  exclude_internal_props: It,
  flush: P,
  get_all_dirty_from_scope: Ct,
  get_slot_changes: Et,
  group_outros: Rt,
  init: St,
  insert_hydration: Ot,
  safe_not_equal: vt,
  transition_in: F,
  transition_out: z,
  update_slot_base: jt
} = window.__gradio__svelte__internal;
function xe(e) {
  let t;
  const n = (
    /*#slots*/
    e[21].default
  ), s = wt(
    n,
    e,
    /*$$scope*/
    e[20],
    null
  );
  return {
    c() {
      s && s.c();
    },
    l(r) {
      s && s.l(r);
    },
    m(r, o) {
      s && s.m(r, o), t = !0;
    },
    p(r, o) {
      s && s.p && (!t || o & /*$$scope*/
      1048576) && jt(
        s,
        n,
        r,
        /*$$scope*/
        r[20],
        t ? Et(
          n,
          /*$$scope*/
          r[20],
          o,
          null
        ) : Ct(
          /*$$scope*/
          r[20]
        ),
        null
      );
    },
    i(r) {
      t || (F(s, r), t = !0);
    },
    o(r) {
      z(s, r), t = !1;
    },
    d(r) {
      s && s.d(r);
    }
  };
}
function kt(e) {
  let t, n, s = (
    /*$mergedProps*/
    e[0].visible && xe(e)
  );
  return {
    c() {
      s && s.c(), t = we();
    },
    l(r) {
      s && s.l(r), t = we();
    },
    m(r, o) {
      s && s.m(r, o), Ot(r, t, o), n = !0;
    },
    p(r, [o]) {
      /*$mergedProps*/
      r[0].visible ? s ? (s.p(r, o), o & /*$mergedProps*/
      1 && F(s, 1)) : (s = xe(r), s.c(), F(s, 1), s.m(t.parentNode, t)) : s && (Rt(), z(s, 1, 1, () => {
        s = null;
      }), Pt());
    },
    i(r) {
      n || (F(s), n = !0);
    },
    o(r) {
      z(s), n = !1;
    },
    d(r) {
      r && xt(t), s && s.d(r);
    }
  };
}
function Ft(e, t, n) {
  const s = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let r = Pe(t, s), o, i, l, u, a, f, {
    $$slots: _ = {},
    $$scope: m
  } = t, {
    gradio: g
  } = t, {
    props: c = {}
  } = t;
  const p = y(c);
  E(e, p, (d) => n(19, f = d));
  let {
    _internal: h = {}
  } = t, {
    as_item: b
  } = t, {
    visible: w = !0
  } = t, {
    elem_id: S = ""
  } = t, {
    elem_classes: O = []
  } = t, {
    elem_style: v = {}
  } = t;
  const U = Ee();
  E(e, U, (d) => n(16, l = d));
  const [G, je] = Ze({
    gradio: g,
    props: f,
    _internal: h,
    visible: w,
    elem_id: S,
    elem_classes: O,
    elem_style: v,
    as_item: b,
    restProps: r
  });
  E(e, G, (d) => n(0, i = d));
  const H = He();
  E(e, H, (d) => n(15, o = d));
  const ke = bt(), K = Ye(), {
    "menu.items": J,
    "dropdownProps.menu.items": Y
  } = ht(["menu.items", "dropdownProps.menu.items"]);
  return E(e, J, (d) => n(18, a = d)), E(e, Y, (d) => n(17, u = d)), e.$$set = (d) => {
    t = ye(ye({}, t), It(d)), n(25, r = Pe(t, s)), "gradio" in d && n(7, g = d.gradio), "props" in d && n(8, c = d.props), "_internal" in d && n(9, h = d._internal), "as_item" in d && n(10, b = d.as_item), "visible" in d && n(11, w = d.visible), "elem_id" in d && n(12, S = d.elem_id), "elem_classes" in d && n(13, O = d.elem_classes), "elem_style" in d && n(14, v = d.elem_style), "$$scope" in d && n(20, m = d.$$scope);
  }, e.$$.update = () => {
    var d, Q, X, Z, V, $, ee, te, ne, re, se, oe, ie, le, ce, ue, de, fe, ae, me, pe, _e;
    if (e.$$.dirty & /*props*/
    256 && p.update((j) => ({
      ...j,
      ...c
    })), je({
      gradio: g,
      props: f,
      _internal: h,
      visible: w,
      elem_id: S,
      elem_classes: O,
      elem_style: v,
      as_item: b,
      restProps: r
    }), e.$$.dirty & /*$mergedProps, $menuItems, $slots, $dropdownMenuItems, $slotKey*/
    491521) {
      const j = {
        ...i.restProps.menu || {},
        ...i.props.menu || {},
        items: (d = i.props.menu) != null && d.items || (Q = i.restProps.menu) != null && Q.items || a.length > 0 ? T(a, {
          clone: !0
        }) : void 0,
        expandIcon: A({
          setSlotParams: K,
          slots: o,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) || ((X = i.props.menu) == null ? void 0 : X.expandIcon) || ((Z = i.restProps.menu) == null ? void 0 : Z.expandIcon),
        overflowedIndicator: W(o["menu.overflowedIndicator"]) || ((V = i.props.menu) == null ? void 0 : V.overflowedIndicator) || (($ = i.restProps.menu) == null ? void 0 : $.overflowedIndicator)
      }, ge = {
        ...((ee = i.restProps.dropdownProps) == null ? void 0 : ee.menu) || {},
        ...((te = i.props.dropdownProps) == null ? void 0 : te.menu) || {},
        items: (re = (ne = i.props.dropdownProps) == null ? void 0 : ne.menu) != null && re.items || (oe = (se = i.restProps.dropdownProps) == null ? void 0 : se.menu) != null && oe.items || u.length > 0 ? T(u, {
          clone: !0
        }) : void 0,
        expandIcon: A({
          setSlotParams: K,
          slots: o,
          key: "dropdownProps.menu.expandIcon"
        }, {
          clone: !0
        }) || ((le = (ie = i.props.dropdownProps) == null ? void 0 : ie.menu) == null ? void 0 : le.expandIcon) || ((ue = (ce = i.restProps.dropdownProps) == null ? void 0 : ce.menu) == null ? void 0 : ue.expandIcon),
        overflowedIndicator: W(o["dropdownProps.menu.overflowedIndicator"]) || ((fe = (de = i.props.dropdownProps) == null ? void 0 : de.menu) == null ? void 0 : fe.overflowedIndicator) || ((me = (ae = i.restProps.dropdownProps) == null ? void 0 : ae.menu) == null ? void 0 : me.overflowedIndicator)
      }, he = {
        ...i.restProps.dropdownProps || {},
        ...i.props.dropdownProps || {},
        dropdownRender: o["dropdownProps.dropdownRender"] ? A({
          setSlotParams: K,
          slots: o,
          key: "dropdownProps.dropdownRender"
        }, {
          clone: !0
        }) : nt(((pe = i.props.dropdownProps) == null ? void 0 : pe.dropdownRender) || ((_e = i.restProps.dropdownProps) == null ? void 0 : _e.dropdownRender)),
        menu: Object.values(ge).filter(Boolean).length > 0 ? ge : void 0
      };
      ke(l, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: gt(i.elem_classes, "ms-gr-antd-breadcrumb-item"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...Ne(i),
          menu: Object.values(j).filter(Boolean).length > 0 ? j : void 0,
          dropdownProps: Object.values(he).filter(Boolean).length > 0 ? he : void 0
        },
        slots: {
          title: o.title
        }
      });
    }
  }, [i, p, U, G, H, J, Y, g, c, h, b, w, S, O, v, o, l, u, a, f, m, _];
}
class Mt extends yt {
  constructor(t) {
    super(), St(this, t, Ft, kt, vt, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), P();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), P();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), P();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), P();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), P();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), P();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), P();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), P();
  }
}
export {
  Mt as default
};
