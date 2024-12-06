import { g as ne, w as I, d as re, a as v } from "./Index-CrJlVhpa.js";
const w = window.ms_globals.React, k = window.ms_globals.React.useMemo, q = window.ms_globals.React.useState, V = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, j = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.ColorPicker;
var J = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = w, le = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ae = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ce.call(t, l) && !ue.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: le,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
O.Fragment = ie;
O.jsx = Y;
O.jsxs = Y;
J.exports = O;
var E = J.exports;
const {
  SvelteComponent: de,
  assign: F,
  binding_callbacks: N,
  check_outros: fe,
  children: K,
  claim_element: Q,
  claim_space: pe,
  component_subscribe: H,
  compute_slots: _e,
  create_slot: he,
  detach: S,
  element: X,
  empty: W,
  exclude_internal_props: D,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: be,
  init: we,
  insert_hydration: R,
  safe_not_equal: ye,
  set_custom_element_data: Z,
  space: Ee,
  transition_in: C,
  transition_out: T,
  update_slot_base: xe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Se,
  getContext: ve,
  onDestroy: Ie,
  setContext: Re
} = window.__gradio__svelte__internal;
function G(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = he(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = X("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = Q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(t);
      o && o.l(s), s.forEach(S), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      R(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && xe(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ge(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : me(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (C(o, e), r = !0);
    },
    o(e) {
      T(o, e), r = !1;
    },
    d(e) {
      e && S(t), o && o.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && G(n)
  );
  return {
    c() {
      t = X("react-portal-target"), r = Ee(), e && e.c(), l = W(), this.h();
    },
    l(s) {
      t = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(S), r = pe(s), e && e.l(s), l = W(), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      R(s, t, i), n[8](t), R(s, r, i), e && e.m(s, i), R(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && C(e, 1)) : (e = G(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (be(), T(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(s) {
      o || (C(e), o = !0);
    },
    o(s) {
      T(e), o = !1;
    },
    d(s) {
      s && (S(t), S(r), S(l)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function ke(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = _e(e);
  let {
    svelteInit: c
  } = t;
  const g = I(M(t)), u = I();
  H(n, u, (d) => r(0, l = d));
  const f = I();
  H(n, f, (d) => r(1, o = d));
  const a = [], p = ve("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: h,
    subSlotIndex: m
  } = ne() || {}, b = c({
    parent: p,
    props: g,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: h,
    subSlotIndex: m,
    onDestroy(d) {
      a.push(d);
    }
  });
  Re("$$ms-gr-react-wrapper", b), Se(() => {
    g.set(M(t));
  }), Ie(() => {
    a.forEach((d) => d());
  });
  function y(d) {
    N[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function x(d) {
    N[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return n.$$set = (d) => {
    r(17, t = F(F({}, t), D(d))), "svelteInit" in d && r(5, c = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, t = D(t), [l, o, u, f, i, c, s, e, y, x];
}
class Oe extends de {
  constructor(t) {
    super(), we(this, t, ke, Ce, ye, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, P = window.ms_globals.tree;
function Pe(n) {
  function t(r) {
    const l = I(), o = new Oe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? P;
          return i.nodes = [...i.nodes, s], z({
            createPortal: j,
            node: P
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), z({
              createPortal: j,
              node: P
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function je(n) {
  const [t, r] = q(() => v(n));
  return V(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Te(n) {
  const t = k(() => re(n, (r) => r), [n]);
  return je(t);
}
function Le(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Ae(n, t = !1) {
  try {
    if (t && !Le(n))
      return;
    if (typeof n == "string") {
      let r = n.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function U(n, t) {
  return k(() => Ae(n, t), [n, t]);
}
function Fe(n, t) {
  const r = k(() => w.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const i = v(e.props.node.slotIndex) || 0, c = v(s.props.node.slotIndex) || 0;
      return i - c === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (v(e.props.node.subSlotIndex) || 0) - (v(s.props.node.subSlotIndex) || 0) : i - c;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Te(r);
}
const Ne = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function He(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Ne.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function L(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(j(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = L(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...w.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = L(e);
      t.push(...i), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function We(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const A = ee(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = te(), [s, i] = q([]);
  return V(() => {
    var f;
    if (!e.current || !n)
      return;
    let c = n;
    function g() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), We(o, a), r && a.classList.add(...r.split(" ")), l) {
        const p = He(l);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var m, b, y;
        (m = e.current) != null && m.contains(c) && ((b = e.current) == null || b.removeChild(c));
        const {
          portals: _,
          clonedElement: h
        } = L(n);
        return c = h, i(_), c.style.display = "contents", g(), (y = e.current) == null || y.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", g(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((p = e.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [n, t, r, l, o]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function $(n, t, r) {
  const l = n.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, e) => {
      var g;
      if (typeof o != "object")
        return o;
      const s = {
        ...o.props,
        key: ((g = o.props) == null ? void 0 : g.key) ?? (r ? `${r}-${e}` : `${e}`)
      };
      let i = s;
      Object.keys(o.slots).forEach((u) => {
        if (!o.slots[u] || !(o.slots[u] instanceof Element) && !o.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((m, b) => {
          i[m] || (i[m] = {}), b !== f.length - 1 && (i = s[m]);
        });
        const a = o.slots[u];
        let p, _, h = !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, h = a.clone ?? h), i[f[f.length - 1]] = p ? _ ? (...m) => (_(f[f.length - 1], m), /* @__PURE__ */ E.jsx(A, {
          slot: p,
          clone: h
        })) : /* @__PURE__ */ E.jsx(A, {
          slot: p,
          clone: h
        }) : i[f[f.length - 1]], i = s;
      });
      const c = "children";
      return o[c] && (s[c] = $(o[c], t, `${e}`)), s;
    });
}
function De(n, t) {
  return n ? /* @__PURE__ */ E.jsx(A, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function B({
  key: n,
  setSlotParams: t,
  slots: r
}, l) {
  return r[n] ? (...o) => (t(n, o), De(r[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const Me = Pe(({
  onValueChange: n,
  onChange: t,
  panelRender: r,
  showText: l,
  value: o,
  presets: e,
  presetItems: s,
  children: i,
  value_format: c,
  setSlotParams: g,
  slots: u,
  ...f
}) => {
  const a = U(r), p = U(l), _ = Fe(i);
  return /* @__PURE__ */ E.jsxs(E.Fragment, {
    children: [_.length === 0 && /* @__PURE__ */ E.jsx("div", {
      style: {
        display: "none"
      },
      children: i
    }), /* @__PURE__ */ E.jsx(oe, {
      ...f,
      value: o,
      presets: k(() => e || $(s), [e, s]),
      showText: u.showText ? B({
        slots: u,
        setSlotParams: g,
        key: "showText"
      }) : p || l,
      panelRender: u.panelRender ? B({
        slots: u,
        setSlotParams: g,
        key: "panelRender"
      }) : a,
      onChange: (h, ...m) => {
        if (h.isGradient()) {
          const y = h.getColors().map((x) => {
            const d = {
              rgb: x.color.toRgbString(),
              hex: x.color.toHexString(),
              hsb: x.color.toHsbString()
            };
            return {
              ...x,
              color: d[c]
            };
          });
          t == null || t(y, ...m), n(y);
          return;
        }
        const b = {
          rgb: h.toRgbString(),
          hex: h.toHexString(),
          hsb: h.toHsbString()
        };
        t == null || t(b[c], ...m), n(b[c]);
      },
      children: _.length === 0 ? null : i
    })]
  });
});
export {
  Me as ColorPicker,
  Me as default
};
