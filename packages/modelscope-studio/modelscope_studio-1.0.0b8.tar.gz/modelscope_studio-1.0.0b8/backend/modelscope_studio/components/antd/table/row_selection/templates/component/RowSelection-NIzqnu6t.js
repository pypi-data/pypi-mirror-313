import { g as oe, b as ie } from "./Index-Buefr4t-.js";
const w = window.ms_globals.React, le = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, ae = window.ms_globals.ReactDOM.createPortal;
function de(e) {
  return e === void 0;
}
function k() {
}
function me(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function _e(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return k;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function P(e) {
  let t;
  return _e(e, (n) => t = n)(), t;
}
const E = [];
function y(e, t = k) {
  let n;
  const s = /* @__PURE__ */ new Set();
  function r(l) {
    if (me(e, l) && (e = l, n)) {
      const u = !E.length;
      for (const a of s)
        a[1](), E.push(a, e);
      if (u) {
        for (let a = 0; a < E.length; a += 2)
          E[a][0](E[a + 1]);
        E.length = 0;
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
  getContext: pe,
  setContext: it
} = window.__gradio__svelte__internal, ge = "$$ms-gr-loading-status-key";
function be() {
  const e = window.ms_globals.loadingKey++, t = pe(ge);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: s,
      options: r
    } = t, {
      generating: o,
      error: i
    } = P(r);
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
  getContext: T,
  setContext: I
} = window.__gradio__svelte__internal, he = "$$ms-gr-slots-key";
function ye() {
  const e = y({});
  return I(he, e);
}
const xe = "$$ms-gr-render-slot-context-key";
function Ce() {
  const e = I(xe, y({}));
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
const Pe = "$$ms-gr-context-key";
function F(e) {
  return de(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const Q = "$$ms-gr-sub-index-context-key";
function we() {
  return T(Q) || null;
}
function D(e) {
  return I(Q, e);
}
function Ee(e, t, n) {
  var m, g;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const s = Z(), r = Re({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), o = we();
  typeof o == "number" && D(void 0);
  const i = be();
  typeof e._internal.subIndex == "number" && D(e._internal.subIndex), s && s.subscribe((c) => {
    r.slotKey.set(c);
  }), Se();
  const l = T(Pe), u = ((m = P(l)) == null ? void 0 : m.as_item) || e.as_item, a = F(l ? u ? ((g = P(l)) == null ? void 0 : g[u]) || {} : P(l) || {} : {}), d = (c, _) => c ? oe({
    ...c,
    ..._ || {}
  }, t) : void 0, p = y({
    ...e,
    _internal: {
      ...e._internal,
      index: o ?? e._internal.index
    },
    ...a,
    restProps: d(e.restProps, a),
    originalRestProps: e.restProps
  });
  return l ? (l.subscribe((c) => {
    const {
      as_item: _
    } = P(p);
    _ && (c = c == null ? void 0 : c[_]), c = F(c), p.update((b) => ({
      ...b,
      ...c || {},
      restProps: d(b.restProps, c)
    }));
  }), [p, (c) => {
    var b, h;
    const _ = F(c.as_item ? ((b = P(l)) == null ? void 0 : b[c.as_item]) || {} : P(l) || {});
    return i((h = c.restProps) == null ? void 0 : h.loading_status), p.set({
      ...c,
      _internal: {
        ...c._internal,
        index: o ?? c._internal.index
      },
      ..._,
      restProps: d(c.restProps, _),
      originalRestProps: c.restProps
    });
  }]) : [p, (c) => {
    var _;
    i((_ = c.restProps) == null ? void 0 : _.loading_status), p.set({
      ...c,
      _internal: {
        ...c._internal,
        index: o ?? c._internal.index
      },
      restProps: d(c.restProps),
      originalRestProps: c.restProps
    });
  }];
}
const X = "$$ms-gr-slot-key";
function Se() {
  I(X, y(void 0));
}
function Z() {
  return T(X);
}
const Ie = "$$ms-gr-component-slot-context-key";
function Re({
  slot: e,
  index: t,
  subIndex: n
}) {
  return I(Ie, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(n)
  });
}
function Oe(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function N(e, t = !1) {
  try {
    if (t && !Oe(e))
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
function ke(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var V = {
  exports: {}
}, v = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var je = w, ve = Symbol.for("react.element"), Fe = Symbol.for("react.fragment"), Ne = Object.prototype.hasOwnProperty, Ke = je.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(e, t, n) {
  var s, r = {}, o = null, i = null;
  n !== void 0 && (o = "" + n), t.key !== void 0 && (o = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (s in t) Ne.call(t, s) && !Le.hasOwnProperty(s) && (r[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ve,
    type: e,
    key: o,
    ref: i,
    props: r,
    _owner: Ke.current
  };
}
v.Fragment = Fe;
v.jsx = $;
v.jsxs = $;
V.exports = v;
var U = V.exports;
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const s = e[n];
    return typeof s == "number" && !Te.includes(n) ? t[n] = s + "px" : t[n] = s, t;
  }, {}) : {};
}
function K(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(ae(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: o,
            clonedElement: i
          } = K(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: i,
            children: [...w.Children.toArray(r.props.children), ...o]
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
      } = K(o);
      t.push(...l), n.appendChild(i);
    } else o.nodeType === 3 && n.appendChild(o.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Me(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const G = le(({
  slot: e,
  clone: t,
  className: n,
  style: s
}, r) => {
  const o = ce(), [i, l] = ue([]);
  return fe(() => {
    var p;
    if (!o.current || !e)
      return;
    let u = e;
    function a() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Me(r, m), n && m.classList.add(...n.split(" ")), s) {
        const g = Ae(s);
        Object.keys(g).forEach((c) => {
          m.style[c] = g[c];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let m = function() {
        var b, h, C;
        (b = o.current) != null && b.contains(u) && ((h = o.current) == null || h.removeChild(u));
        const {
          portals: c,
          clonedElement: _
        } = K(e);
        return u = _, l(c), u.style.display = "contents", a(), (C = o.current) == null || C.appendChild(u), c.length > 0;
      };
      m() || (d = new window.MutationObserver(() => {
        m() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      u.style.display = "contents", a(), (p = o.current) == null || p.appendChild(u);
    return () => {
      var m, g;
      u.style.display = "", (m = o.current) != null && m.contains(u) && ((g = o.current) == null || g.removeChild(u)), d == null || d.disconnect();
    };
  }, [e, t, n, s, r]), w.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...i);
}), {
  getContext: qe,
  setContext: We
} = window.__gradio__svelte__internal;
function ee(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function n(r = ["default"]) {
    const o = r.reduce((i, l) => (i[l] = y([]), i), {});
    return We(t, {
      itemsMap: o,
      allowedSlots: r
    }), o;
  }
  function s() {
    const {
      itemsMap: r,
      allowedSlots: o
    } = qe(t);
    return function(i, l, u) {
      r && (i ? r[i].update((a) => {
        const d = [...a];
        return o.includes(i) ? d[l] = u : d[l] = void 0, d;
      }) : o.includes("default") && r.default.update((a) => {
        const d = [...a];
        return d[l] = u, d;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: s
  };
}
function te(e, t, n) {
  const s = e.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, o) => {
      var a;
      if (typeof r != "object")
        return r;
      const i = {
        ...r.props,
        key: ((a = r.props) == null ? void 0 : a.key) ?? (n ? `${n}-${o}` : `${o}`)
      };
      let l = i;
      Object.keys(r.slots).forEach((d) => {
        if (!r.slots[d] || !(r.slots[d] instanceof Element) && !r.slots[d].el)
          return;
        const p = d.split(".");
        p.forEach((b, h) => {
          l[b] || (l[b] = {}), h !== p.length - 1 && (l = i[b]);
        });
        const m = r.slots[d];
        let g, c, _ = !1;
        m instanceof Element ? g = m : (g = m.el, c = m.callback, _ = m.clone ?? _), l[p[p.length - 1]] = g ? c ? (...b) => (c(p[p.length - 1], b), /* @__PURE__ */ U.jsx(G, {
          slot: g,
          clone: _
        })) : /* @__PURE__ */ U.jsx(G, {
          slot: g,
          clone: _
        }) : l[p[p.length - 1]], l = i;
      });
      const u = "children";
      return r[u] && (i[u] = te(r[u], t, `${o}`)), i;
    });
}
var ne = {
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
})(ne);
var ze = ne.exports;
const De = /* @__PURE__ */ ke(ze), {
  getItems: Ue,
  getSetItemFn: lt
} = ee("table-row-selection-selection"), {
  getItems: ct,
  getSetItemFn: Ge
} = ee("table-row-selection"), {
  SvelteComponent: He,
  assign: H,
  check_outros: Be,
  component_subscribe: S,
  compute_rest_props: B,
  create_slot: Je,
  detach: Ye,
  empty: J,
  exclude_internal_props: Qe,
  flush: x,
  get_all_dirty_from_scope: Xe,
  get_slot_changes: Ze,
  group_outros: Ve,
  init: $e,
  insert_hydration: et,
  safe_not_equal: tt,
  transition_in: j,
  transition_out: L,
  update_slot_base: nt
} = window.__gradio__svelte__internal;
function Y(e) {
  let t;
  const n = (
    /*#slots*/
    e[19].default
  ), s = Je(
    n,
    e,
    /*$$scope*/
    e[18],
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
      262144) && nt(
        s,
        n,
        r,
        /*$$scope*/
        r[18],
        t ? Ze(
          n,
          /*$$scope*/
          r[18],
          o,
          null
        ) : Xe(
          /*$$scope*/
          r[18]
        ),
        null
      );
    },
    i(r) {
      t || (j(s, r), t = !0);
    },
    o(r) {
      L(s, r), t = !1;
    },
    d(r) {
      s && s.d(r);
    }
  };
}
function st(e) {
  let t, n, s = (
    /*$mergedProps*/
    e[0].visible && Y(e)
  );
  return {
    c() {
      s && s.c(), t = J();
    },
    l(r) {
      s && s.l(r), t = J();
    },
    m(r, o) {
      s && s.m(r, o), et(r, t, o), n = !0;
    },
    p(r, [o]) {
      /*$mergedProps*/
      r[0].visible ? s ? (s.p(r, o), o & /*$mergedProps*/
      1 && j(s, 1)) : (s = Y(r), s.c(), j(s, 1), s.m(t.parentNode, t)) : s && (Ve(), L(s, 1, 1, () => {
        s = null;
      }), Be());
    },
    i(r) {
      n || (j(s), n = !0);
    },
    o(r) {
      L(s), n = !1;
    },
    d(r) {
      r && Ye(t), s && s.d(r);
    }
  };
}
function rt(e, t, n) {
  const s = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let r = B(t, s), o, i, l, u, a, {
    $$slots: d = {},
    $$scope: p
  } = t, {
    gradio: m
  } = t, {
    props: g = {}
  } = t;
  const c = y(g);
  S(e, c, (f) => n(17, a = f));
  let {
    _internal: _ = {}
  } = t, {
    as_item: b
  } = t, {
    visible: h = !0
  } = t, {
    elem_id: C = ""
  } = t, {
    elem_classes: R = []
  } = t, {
    elem_style: O = {}
  } = t;
  const A = Z();
  S(e, A, (f) => n(16, u = f));
  const [M, se] = Ee({
    gradio: m,
    props: a,
    _internal: _,
    visible: h,
    elem_id: C,
    elem_classes: R,
    elem_style: O,
    as_item: b,
    restProps: r
  });
  S(e, M, (f) => n(0, i = f));
  const q = Ce(), W = ye();
  S(e, W, (f) => n(14, o = f));
  const {
    selections: z
  } = Ue(["selections"]);
  S(e, z, (f) => n(15, l = f));
  const re = Ge();
  return e.$$set = (f) => {
    t = H(H({}, t), Qe(f)), n(23, r = B(t, s)), "gradio" in f && n(6, m = f.gradio), "props" in f && n(7, g = f.props), "_internal" in f && n(8, _ = f._internal), "as_item" in f && n(9, b = f.as_item), "visible" in f && n(10, h = f.visible), "elem_id" in f && n(11, C = f.elem_id), "elem_classes" in f && n(12, R = f.elem_classes), "elem_style" in f && n(13, O = f.elem_style), "$$scope" in f && n(18, p = f.$$scope);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*props*/
    128 && c.update((f) => ({
      ...f,
      ...g
    })), se({
      gradio: m,
      props: a,
      _internal: _,
      visible: h,
      elem_id: C,
      elem_classes: R,
      elem_style: O,
      as_item: b,
      restProps: r
    }), e.$$.dirty & /*$mergedProps, $slotKey, $selectionsItems, $slots*/
    114689) {
      const f = ie(i);
      re(u, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: De(i.elem_classes, "ms-gr-antd-table-row-selection"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...f,
          selections: i.props.selections || i.restProps.selections || te(l),
          onCell: N(i.props.onCell || i.restProps.onCell),
          getCheckboxProps: N(i.props.getCheckboxProps || i.restProps.getCheckboxProps),
          renderCell: N(i.props.renderCell || i.restProps.renderCell),
          columnTitle: i.props.columnTitle || i.restProps.columnTitle
        },
        slots: {
          ...o,
          columnTitle: {
            el: o.columnTitle,
            callback: q,
            clone: !0
          },
          renderCell: {
            el: o.renderCell,
            callback: q,
            clone: !0
          }
        }
      });
    }
  }, [i, c, A, M, W, z, m, g, _, b, h, C, R, O, o, l, u, a, p, d];
}
class ut extends He {
  constructor(t) {
    super(), $e(this, t, rt, st, tt, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), x();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), x();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), x();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), x();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), x();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), x();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), x();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), x();
  }
}
export {
  ut as default
};
