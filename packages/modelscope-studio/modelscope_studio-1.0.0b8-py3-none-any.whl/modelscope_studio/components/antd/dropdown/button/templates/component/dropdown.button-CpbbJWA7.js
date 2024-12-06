import { g as ne, w as R, d as re, a as E } from "./Index-DkJBtZD2.js";
const b = window.ms_globals.React, k = window.ms_globals.React.useMemo, H = window.ms_globals.React.useState, V = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, L = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Dropdown;
var q = {
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
var se = b, le = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(n, e, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (l in e) ie.call(e, l) && !ae.hasOwnProperty(l) && (o[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: le,
    type: n,
    key: t,
    ref: s,
    props: o,
    _owner: ue.current
  };
}
O.Fragment = ce;
O.jsx = J;
O.jsxs = J;
q.exports = O;
var v = q.exports;
const {
  SvelteComponent: de,
  assign: F,
  binding_callbacks: N,
  check_outros: fe,
  children: Y,
  claim_element: K,
  claim_space: pe,
  component_subscribe: D,
  compute_slots: _e,
  create_slot: me,
  detach: y,
  element: Q,
  empty: W,
  exclude_internal_props: B,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: S,
  safe_not_equal: ye,
  set_custom_element_data: X,
  space: ve,
  transition_in: C,
  transition_out: T,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ie,
  getContext: xe,
  onDestroy: Re,
  setContext: Se
} = window.__gradio__svelte__internal;
function M(n) {
  let e, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = me(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = Q("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(e);
      o && o.l(s), s.forEach(y), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      S(t, e, s), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ee(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? ge(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : he(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (C(o, t), r = !0);
    },
    o(t) {
      T(o, t), r = !1;
    },
    d(t) {
      t && y(e), o && o.d(t), n[9](null);
    }
  };
}
function Ce(n) {
  let e, r, l, o, t = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      e = Q("react-portal-target"), r = ve(), t && t.c(), l = W(), this.h();
    },
    l(s) {
      e = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(e).forEach(y), r = pe(s), t && t.l(s), l = W(), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      S(s, e, c), n[8](e), S(s, r, c), t && t.m(s, c), S(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && C(t, 1)) : (t = M(s), t.c(), C(t, 1), t.m(l.parentNode, l)) : t && (we(), T(t, 1, 1, () => {
        t = null;
      }), fe());
    },
    i(s) {
      o || (C(t), o = !0);
    },
    o(s) {
      T(t), o = !1;
    },
    d(s) {
      s && (y(e), y(r), y(l)), n[8](null), t && t.d(s);
    }
  };
}
function z(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function ke(n, e, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = _e(t);
  let {
    svelteInit: i
  } = e;
  const g = R(z(e)), a = R();
  D(n, a, (f) => r(0, l = f));
  const d = R();
  D(n, d, (f) => r(1, o = f));
  const u = [], p = xe("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: m,
    subSlotIndex: h
  } = ne() || {}, w = i({
    parent: p,
    props: g,
    target: a,
    slot: d,
    slotKey: _,
    slotIndex: m,
    subSlotIndex: h,
    onDestroy(f) {
      u.push(f);
    }
  });
  Se("$$ms-gr-react-wrapper", w), Ie(() => {
    g.set(z(e));
  }), Re(() => {
    u.forEach((f) => f());
  });
  function x(f) {
    N[f ? "unshift" : "push"](() => {
      l = f, a.set(l);
    });
  }
  function $(f) {
    N[f ? "unshift" : "push"](() => {
      o = f, d.set(o);
    });
  }
  return n.$$set = (f) => {
    r(17, e = F(F({}, e), B(f))), "svelteInit" in f && r(5, i = f.svelteInit), "$$scope" in f && r(6, s = f.$$scope);
  }, e = B(e), [l, o, a, d, c, i, s, t, x, $];
}
class Oe extends de {
  constructor(e) {
    super(), be(this, e, ke, Ce, ye, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, P = window.ms_globals.tree;
function Pe(n) {
  function e(r) {
    const l = R(), o = new Oe({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? P;
          return c.nodes = [...c.nodes, s], G({
            createPortal: L,
            node: P
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), G({
              createPortal: L,
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
      r(e);
    });
  });
}
function je(n) {
  const [e, r] = H(() => E(n));
  return V(() => {
    let l = !0;
    return n.subscribe((t) => {
      l && (l = !1, t === e) || r(t);
    });
  }, [n]), e;
}
function Le(n) {
  const e = k(() => re(n, (r) => r), [n]);
  return je(e);
}
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const l = n[r];
    return typeof l == "number" && !Te.includes(r) ? e[r] = l + "px" : e[r] = l, e;
  }, {}) : {};
}
function A(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(L(b.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: b.Children.toArray(n._reactElement.props.children).map((o) => {
        if (b.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = A(o.props.el);
          return b.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...b.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = A(t);
      e.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Fe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const I = ee(({
  slot: n,
  clone: e,
  className: r,
  style: l
}, o) => {
  const t = te(), [s, c] = H([]);
  return V(() => {
    var d;
    if (!t.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Fe(o, u), r && u.classList.add(...r.split(" ")), l) {
        const p = Ae(l);
        Object.keys(p).forEach((_) => {
          u.style[_] = p[_];
        });
      }
    }
    let a = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var h, w, x;
        (h = t.current) != null && h.contains(i) && ((w = t.current) == null || w.removeChild(i));
        const {
          portals: _,
          clonedElement: m
        } = A(n);
        return i = m, c(_), i.style.display = "contents", g(), (x = t.current) == null || x.appendChild(i), _.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (d = t.current) == null || d.appendChild(i);
    return () => {
      var u, p;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((p = t.current) == null || p.removeChild(i)), a == null || a.disconnect();
    };
  }, [n, e, r, l, o]), b.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function De(n, e = !1) {
  try {
    if (e && !Ne(n))
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
function j(n, e) {
  return k(() => De(n, e), [n, e]);
}
function We(n, e) {
  const r = k(() => b.Children.toArray(n).filter((t) => t.props.node && e === t.props.nodeSlotKey).sort((t, s) => {
    if (t.props.node.slotIndex && s.props.node.slotIndex) {
      const c = E(t.props.node.slotIndex) || 0, i = E(s.props.node.slotIndex) || 0;
      return c - i === 0 && t.props.node.subSlotIndex && s.props.node.subSlotIndex ? (E(t.props.node.subSlotIndex) || 0) - (E(s.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((t) => t.props.node.target), [n, e]);
  return Le(r);
}
function Z(n, e, r) {
  const l = n.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, t) => {
      var g;
      if (typeof o != "object")
        return e != null && e.fallback ? e.fallback(o) : o;
      const s = {
        ...o.props,
        key: ((g = o.props) == null ? void 0 : g.key) ?? (r ? `${r}-${t}` : `${t}`)
      };
      let c = s;
      Object.keys(o.slots).forEach((a) => {
        if (!o.slots[a] || !(o.slots[a] instanceof Element) && !o.slots[a].el)
          return;
        const d = a.split(".");
        d.forEach((h, w) => {
          c[h] || (c[h] = {}), w !== d.length - 1 && (c = s[h]);
        });
        const u = o.slots[a];
        let p, _, m = (e == null ? void 0 : e.clone) ?? !1;
        u instanceof Element ? p = u : (p = u.el, _ = u.callback, m = u.clone ?? m), c[d[d.length - 1]] = p ? _ ? (...h) => (_(d[d.length - 1], h), /* @__PURE__ */ v.jsx(I, {
          slot: p,
          clone: m
        })) : /* @__PURE__ */ v.jsx(I, {
          slot: p,
          clone: m
        }) : c[d[d.length - 1]], c = s;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return o[i] && (s[i] = Z(o[i], e, `${t}`)), s;
    });
}
function Be(n, e) {
  return n ? /* @__PURE__ */ v.jsx(I, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function U({
  key: n,
  setSlotParams: e,
  slots: r
}, l) {
  return r[n] ? (...o) => (e(n, o), Be(r[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const ze = Pe(({
  getPopupContainer: n,
  slots: e,
  menuItems: r,
  children: l,
  dropdownRender: o,
  buttonsRender: t,
  setSlotParams: s,
  ...c
}) => {
  var u, p, _;
  const i = j(n), g = j(o), a = j(t), d = We(l, "buttonsRender");
  return /* @__PURE__ */ v.jsx(oe.Button, {
    ...c,
    buttonsRender: d.length ? (...m) => (s("buttonsRender", m), d.map((h, w) => /* @__PURE__ */ v.jsx(I, {
      slot: h
    }, w))) : a,
    menu: {
      ...c.menu,
      items: k(() => {
        var m;
        return ((m = c.menu) == null ? void 0 : m.items) || Z(r, {
          clone: !0
        });
      }, [r, (u = c.menu) == null ? void 0 : u.items]),
      expandIcon: e["menu.expandIcon"] ? U({
        slots: e,
        setSlotParams: s,
        key: "menu.expandIcon"
      }, {
        clone: !0
      }) : (p = c.menu) == null ? void 0 : p.expandIcon,
      overflowedIndicator: e["menu.overflowedIndicator"] ? /* @__PURE__ */ v.jsx(I, {
        slot: e["menu.overflowedIndicator"]
      }) : (_ = c.menu) == null ? void 0 : _.overflowedIndicator
    },
    getPopupContainer: i,
    dropdownRender: e.dropdownRender ? U({
      slots: e,
      setSlotParams: s,
      key: "dropdownRender"
    }) : g,
    children: l
  });
});
export {
  ze as DropdownButton,
  ze as default
};
