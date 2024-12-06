import { g as $, w as I } from "./Index-BylSfzQt.js";
const w = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Menu;
var z = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = w, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, e, l) {
  var s, r = {}, t = null, o = null;
  l !== void 0 && (t = "" + l), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (s in e) le.call(e, s) && !se.hasOwnProperty(s) && (r[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) r[s] === void 0 && (r[s] = e[s]);
  return {
    $$typeof: ne,
    type: n,
    key: t,
    ref: o,
    props: r,
    _owner: oe.current
  };
}
S.Fragment = re;
S.jsx = G;
S.jsxs = G;
z.exports = S;
var b = z.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: T,
  check_outros: ae,
  children: D,
  claim_element: H,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: de,
  create_slot: ue,
  detach: v,
  element: q,
  empty: A,
  exclude_internal_props: M,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: he,
  init: me,
  insert_hydration: x,
  safe_not_equal: pe,
  set_custom_element_data: B,
  space: ge,
  transition_in: C,
  transition_out: P,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ve,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(n) {
  let e, l;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ue(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = q("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = H(t, "SVELTE-SLOT", {
        class: !0
      });
      var o = D(e);
      r && r.l(o), o.forEach(v), this.h();
    },
    h() {
      B(e, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      x(t, e, o), r && r.m(e, null), n[9](e), l = !0;
    },
    p(t, o) {
      r && r.p && (!l || o & /*$$scope*/
      64) && we(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        l ? _e(
          s,
          /*$$scope*/
          t[6],
          o,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      l || (C(r, t), l = !0);
    },
    o(t) {
      P(r, t), l = !1;
    },
    d(t) {
      t && v(e), r && r.d(t), n[9](null);
    }
  };
}
function Ie(n) {
  let e, l, s, r, t = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      e = q("react-portal-target"), l = ge(), t && t.c(), s = A(), this.h();
    },
    l(o) {
      e = H(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(e).forEach(v), l = ie(o), t && t.l(o), s = A(), this.h();
    },
    h() {
      B(e, "class", "svelte-1rt0kpf");
    },
    m(o, a) {
      x(o, e, a), n[8](e), x(o, l, a), t && t.m(o, a), x(o, s, a), r = !0;
    },
    p(o, [a]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, a), a & /*$$slots*/
      16 && C(t, 1)) : (t = F(o), t.c(), C(t, 1), t.m(s.parentNode, s)) : t && (he(), P(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(o) {
      r || (C(t), r = !0);
    },
    o(o) {
      P(t), r = !1;
    },
    d(o) {
      o && (v(e), v(l), v(s)), n[8](null), t && t.d(o);
    }
  };
}
function U(n) {
  const {
    svelteInit: e,
    ...l
  } = n;
  return l;
}
function xe(n, e, l) {
  let s, r, {
    $$slots: t = {},
    $$scope: o
  } = e;
  const a = de(t);
  let {
    svelteInit: c
  } = e;
  const _ = I(U(e)), d = I();
  N(n, d, (u) => l(0, s = u));
  const f = I();
  N(n, f, (u) => l(1, r = u));
  const i = [], h = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: p
  } = $() || {}, E = c({
    parent: h,
    props: _,
    target: d,
    slot: f,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: p,
    onDestroy(u) {
      i.push(u);
    }
  });
  ye("$$ms-gr-react-wrapper", E), be(() => {
    _.set(U(e));
  }), ve(() => {
    i.forEach((u) => u());
  });
  function y(u) {
    T[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function J(u) {
    T[u ? "unshift" : "push"](() => {
      r = u, f.set(r);
    });
  }
  return n.$$set = (u) => {
    l(17, e = L(L({}, e), M(u))), "svelteInit" in u && l(5, c = u.svelteInit), "$$scope" in u && l(6, o = u.$$scope);
  }, e = M(e), [s, r, d, f, a, c, o, t, y, J];
}
class Ce extends ce {
  constructor(e) {
    super(), me(this, e, xe, Ie, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, k = window.ms_globals.tree;
function Re(n) {
  function e(l) {
    const s = I(), r = new Ce({
      ...l,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? k;
          return a.nodes = [...a.nodes, o], W({
            createPortal: O,
            node: k
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== s), W({
              createPortal: O,
              node: k
            });
          }), o;
        },
        ...l.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(e);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((e, l) => {
    const s = n[l];
    return typeof s == "number" && !Se.includes(l) ? e[l] = s + "px" : e[l] = s, e;
  }, {}) : {};
}
function j(n) {
  const e = [], l = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(O(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: o
          } = j(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: o,
            children: [...w.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: o,
      type: a,
      useCapture: c
    }) => {
      l.addEventListener(a, o, c);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const t = s[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: o,
        portals: a
      } = j(t);
      e.push(...a), l.appendChild(o);
    } else t.nodeType === 3 && l.appendChild(t.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function Oe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const R = Y(({
  slot: n,
  clone: e,
  className: l,
  style: s
}, r) => {
  const t = K(), [o, a] = Q([]);
  return X(() => {
    var f;
    if (!t.current || !n)
      return;
    let c = n;
    function _() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(r, i), l && i.classList.add(...l.split(" ")), s) {
        const h = ke(s);
        Object.keys(h).forEach((m) => {
          i.style[m] = h[m];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var p, E, y;
        (p = t.current) != null && p.contains(c) && ((E = t.current) == null || E.removeChild(c));
        const {
          portals: m,
          clonedElement: g
        } = j(n);
        return c = g, a(m), c.style.display = "contents", _(), (y = t.current) == null || y.appendChild(c), m.length > 0;
      };
      i() || (d = new window.MutationObserver(() => {
        i() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", _(), (f = t.current) == null || f.appendChild(c);
    return () => {
      var i, h;
      c.style.display = "", (i = t.current) != null && i.contains(c) && ((h = t.current) == null || h.removeChild(c)), d == null || d.disconnect();
    };
  }, [n, e, l, s, r]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...o);
});
function Pe(n) {
  return Object.keys(n).reduce((e, l) => (n[l] !== void 0 && (e[l] = n[l]), e), {});
}
function V(n, e, l) {
  const s = n.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, t) => {
      var _;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const o = {
        ...r.props,
        key: ((_ = r.props) == null ? void 0 : _.key) ?? (l ? `${l}-${t}` : `${t}`)
      };
      let a = o;
      Object.keys(r.slots).forEach((d) => {
        if (!r.slots[d] || !(r.slots[d] instanceof Element) && !r.slots[d].el)
          return;
        const f = d.split(".");
        f.forEach((p, E) => {
          a[p] || (a[p] = {}), E !== f.length - 1 && (a = o[p]);
        });
        const i = r.slots[d];
        let h, m, g = (e == null ? void 0 : e.clone) ?? !1;
        i instanceof Element ? h = i : (h = i.el, m = i.callback, g = i.clone ?? g), a[f[f.length - 1]] = h ? m ? (...p) => (m(f[f.length - 1], p), /* @__PURE__ */ b.jsx(R, {
          slot: h,
          clone: g
        })) : /* @__PURE__ */ b.jsx(R, {
          slot: h,
          clone: g
        }) : a[f[f.length - 1]], a = o;
      });
      const c = (e == null ? void 0 : e.children) || "children";
      return r[c] && (o[c] = V(r[c], e, `${t}`)), o;
    });
}
function je(n, e) {
  return n ? /* @__PURE__ */ b.jsx(R, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Le({
  key: n,
  setSlotParams: e,
  slots: l
}, s) {
  return l[n] ? (...r) => (e(n, r), je(l[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Re(({
  slots: n,
  items: e,
  slotItems: l,
  children: s,
  onOpenChange: r,
  onSelect: t,
  onDeselect: o,
  setSlotParams: a,
  ...c
}) => /* @__PURE__ */ b.jsxs(b.Fragment, {
  children: [s, /* @__PURE__ */ b.jsx(ee, {
    ...Pe(c),
    onOpenChange: (_) => {
      r == null || r(_);
    },
    onSelect: (_) => {
      t == null || t(_);
    },
    onDeselect: (_) => {
      o == null || o(_);
    },
    items: Z(() => e || V(l, {
      clone: !0
    }), [e, l]),
    expandIcon: n.expandIcon ? Le({
      key: "expandIcon",
      slots: n,
      setSlotParams: a
    }, {
      clone: !0
    }) : c.expandIcon,
    overflowedIndicator: n.overflowedIndicator ? /* @__PURE__ */ b.jsx(R, {
      slot: n.overflowedIndicator
    }) : c.overflowedIndicator
  })]
}));
export {
  Ne as Menu,
  Ne as default
};
