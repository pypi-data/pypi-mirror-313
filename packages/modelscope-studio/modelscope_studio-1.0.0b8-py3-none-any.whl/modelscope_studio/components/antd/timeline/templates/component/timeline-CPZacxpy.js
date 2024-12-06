import { g as $, w as C } from "./Index-f1Q3_uLn.js";
const b = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Timeline;
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
var te = b, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(r, n, o) {
  var s, t = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) oe.call(n, s) && !se.hasOwnProperty(s) && (t[s] = n[s]);
  if (r && r.defaultProps) for (s in n = r.defaultProps, n) t[s] === void 0 && (t[s] = n[s]);
  return {
    $$typeof: ne,
    type: r,
    key: e,
    ref: l,
    props: t,
    _owner: le.current
  };
}
S.Fragment = re;
S.jsx = G;
S.jsxs = G;
z.exports = S;
var w = z.exports;
const {
  SvelteComponent: ie,
  assign: T,
  binding_callbacks: L,
  check_outros: ce,
  children: U,
  claim_element: H,
  claim_space: ae,
  component_subscribe: D,
  compute_slots: de,
  create_slot: ue,
  detach: y,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: x,
  safe_not_equal: me,
  set_custom_element_data: B,
  space: ge,
  transition_in: R,
  transition_out: P,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function F(r) {
  let n, o;
  const s = (
    /*#slots*/
    r[7].default
  ), t = ue(
    s,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      n = q("svelte-slot"), t && t.c(), this.h();
    },
    l(e) {
      n = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(n);
      t && t.l(l), l.forEach(y), this.h();
    },
    h() {
      B(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      x(e, n, l), t && t.m(n, null), r[9](n), o = !0;
    },
    p(e, l) {
      t && t.p && (!o || l & /*$$scope*/
      64) && we(
        t,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? pe(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (R(t, e), o = !0);
    },
    o(e) {
      P(t, e), o = !1;
    },
    d(e) {
      e && y(n), t && t.d(e), r[9](null);
    }
  };
}
function Ce(r) {
  let n, o, s, t, e = (
    /*$$slots*/
    r[4].default && F(r)
  );
  return {
    c() {
      n = q("react-portal-target"), o = ge(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      n = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(n).forEach(y), o = ae(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      B(n, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      x(l, n, i), r[8](n), x(l, o, i), e && e.m(l, i), x(l, s, i), t = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && R(e, 1)) : (e = F(l), e.c(), R(e, 1), e.m(s.parentNode, s)) : e && (_e(), P(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      t || (R(e), t = !0);
    },
    o(l) {
      P(e), t = !1;
    },
    d(l) {
      l && (y(n), y(o), y(s)), r[8](null), e && e.d(l);
    }
  };
}
function M(r) {
  const {
    svelteInit: n,
    ...o
  } = r;
  return o;
}
function xe(r, n, o) {
  let s, t, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const i = de(e);
  let {
    svelteInit: c
  } = n;
  const m = C(M(n)), d = C();
  D(r, d, (u) => o(0, s = u));
  const f = C();
  D(r, f, (u) => o(1, t = u));
  const a = [], p = Ee("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: h
  } = $() || {}, E = c({
    parent: p,
    props: m,
    target: d,
    slot: f,
    slotKey: _,
    slotIndex: g,
    subSlotIndex: h,
    onDestroy(u) {
      a.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", E), be(() => {
    m.set(M(n));
  }), ye(() => {
    a.forEach((u) => u());
  });
  function v(u) {
    L[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function J(u) {
    L[u ? "unshift" : "push"](() => {
      t = u, f.set(t);
    });
  }
  return r.$$set = (u) => {
    o(17, n = T(T({}, n), A(u))), "svelteInit" in u && o(5, c = u.svelteInit), "$$scope" in u && o(6, l = u.$$scope);
  }, n = A(n), [s, t, d, f, i, c, l, e, v, J];
}
class Re extends ie {
  constructor(n) {
    super(), he(this, n, xe, Ce, me, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ie(r) {
  function n(o) {
    const s = C(), t = new Re({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? O;
          return i.nodes = [...i.nodes, l], W({
            createPortal: k,
            node: O
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), W({
              createPortal: k,
              node: O
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(t), t;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(r) {
  return r ? Object.keys(r).reduce((n, o) => {
    const s = r[o];
    return typeof s == "number" && !Se.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function j(r) {
  const n = [], o = r.cloneNode(!1);
  if (r._reactElement)
    return n.push(k(b.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: b.Children.toArray(r._reactElement.props.children).map((t) => {
        if (b.isValidElement(t) && t.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(t.props.el);
          return b.cloneElement(t, {
            ...t.props,
            el: l,
            children: [...b.Children.toArray(t.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(r.getEventListeners()).forEach((t) => {
    r.getEventListeners(t).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, l, c);
    });
  });
  const s = Array.from(r.childNodes);
  for (let t = 0; t < s.length; t++) {
    const e = s[t];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = j(e);
      n.push(...i), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function ke(r, n) {
  r && (typeof r == "function" ? r(n) : r.current = n);
}
const I = Y(({
  slot: r,
  clone: n,
  className: o,
  style: s
}, t) => {
  const e = K(), [l, i] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !r)
      return;
    let c = r;
    function m() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(t, a), o && a.classList.add(...o.split(" ")), s) {
        const p = Oe(s);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var h, E, v;
        (h = e.current) != null && h.contains(c) && ((E = e.current) == null || E.removeChild(c));
        const {
          portals: _,
          clonedElement: g
        } = j(r);
        return c = g, i(_), c.style.display = "contents", m(), (v = e.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", m(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((p = e.current) == null || p.removeChild(c)), d == null || d.disconnect();
    };
  }, [r, n, o, s, t]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function V(r, n, o) {
  const s = r.filter(Boolean);
  if (s.length !== 0)
    return s.map((t, e) => {
      var m;
      if (typeof t != "object")
        return t;
      const l = {
        ...t.props,
        key: ((m = t.props) == null ? void 0 : m.key) ?? (o ? `${o}-${e}` : `${e}`)
      };
      let i = l;
      Object.keys(t.slots).forEach((d) => {
        if (!t.slots[d] || !(t.slots[d] instanceof Element) && !t.slots[d].el)
          return;
        const f = d.split(".");
        f.forEach((h, E) => {
          i[h] || (i[h] = {}), E !== f.length - 1 && (i = l[h]);
        });
        const a = t.slots[d];
        let p, _, g = !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, g = a.clone ?? g), i[f[f.length - 1]] = p ? _ ? (...h) => (_(f[f.length - 1], h), /* @__PURE__ */ w.jsx(I, {
          slot: p,
          clone: g
        })) : /* @__PURE__ */ w.jsx(I, {
          slot: p,
          clone: g
        }) : i[f[f.length - 1]], i = l;
      });
      const c = "children";
      return t[c] && (l[c] = V(t[c], n, `${e}`)), l;
    });
}
const je = Ie(({
  slots: r,
  items: n,
  slotItems: o,
  children: s,
  ...t
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [/* @__PURE__ */ w.jsx("div", {
    style: {
      display: "none"
    },
    children: s
  }), /* @__PURE__ */ w.jsx(ee, {
    ...t,
    items: Z(() => n || V(o), [n, o]),
    pending: r.pending ? /* @__PURE__ */ w.jsx(I, {
      slot: r.pending
    }) : t.pending,
    pendingDot: r.pendingDot ? /* @__PURE__ */ w.jsx(I, {
      slot: r.pendingDot
    }) : t.pendingDot
  })]
}));
export {
  je as Timeline,
  je as default
};
