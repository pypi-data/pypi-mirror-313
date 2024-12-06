import { g as $, w as x } from "./Index-Dqc9zrEh.js";
const b = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Descriptions;
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
var te = b, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(r, n, o) {
  var l, t = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) oe.call(n, l) && !le.hasOwnProperty(l) && (t[l] = n[l]);
  if (r && r.defaultProps) for (l in n = r.defaultProps, n) t[l] === void 0 && (t[l] = n[l]);
  return {
    $$typeof: ne,
    type: r,
    key: e,
    ref: s,
    props: t,
    _owner: se.current
  };
}
S.Fragment = re;
S.jsx = G;
S.jsxs = G;
z.exports = S;
var w = z.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: T,
  check_outros: ce,
  children: U,
  claim_element: H,
  claim_space: ae,
  component_subscribe: N,
  compute_slots: de,
  create_slot: ue,
  detach: y,
  element: q,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: C,
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
  const l = (
    /*#slots*/
    r[7].default
  ), t = ue(
    l,
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
      var s = U(n);
      t && t.l(s), s.forEach(y), this.h();
    },
    h() {
      B(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, n, s), t && t.m(n, null), r[9](n), o = !0;
    },
    p(e, s) {
      t && t.p && (!o || s & /*$$scope*/
      64) && we(
        t,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? pe(
          l,
          /*$$scope*/
          e[6],
          s,
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
function xe(r) {
  let n, o, l, t, e = (
    /*$$slots*/
    r[4].default && F(r)
  );
  return {
    c() {
      n = q("react-portal-target"), o = ge(), e && e.c(), l = A(), this.h();
    },
    l(s) {
      n = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(n).forEach(y), o = ae(s), e && e.l(s), l = A(), this.h();
    },
    h() {
      B(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      C(s, n, i), r[8](n), C(s, o, i), e && e.m(s, i), C(s, l, i), t = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && R(e, 1)) : (e = F(s), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (_e(), P(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      t || (R(e), t = !0);
    },
    o(s) {
      P(e), t = !1;
    },
    d(s) {
      s && (y(n), y(o), y(l)), r[8](null), e && e.d(s);
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
function Ce(r, n, o) {
  let l, t, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const i = de(e);
  let {
    svelteInit: c
  } = n;
  const m = x(M(n)), d = x();
  N(r, d, (u) => o(0, l = u));
  const f = x();
  N(r, f, (u) => o(1, t = u));
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
    T[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function J(u) {
    T[u ? "unshift" : "push"](() => {
      t = u, f.set(t);
    });
  }
  return r.$$set = (u) => {
    o(17, n = L(L({}, n), D(u))), "svelteInit" in u && o(5, c = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, n = D(n), [l, t, d, f, i, c, s, e, v, J];
}
class Re extends ie {
  constructor(n) {
    super(), he(this, n, Ce, xe, me, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ie(r) {
  function n(o) {
    const l = x(), t = new Re({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? O;
          return i.nodes = [...i.nodes, s], W({
            createPortal: k,
            node: O
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), W({
              createPortal: k,
              node: O
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(t), t;
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
    const l = r[o];
    return typeof l == "number" && !Se.includes(o) ? n[o] = l + "px" : n[o] = l, n;
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
            clonedElement: s
          } = j(t.props.el);
          return b.cloneElement(t, {
            ...t.props,
            el: s,
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
      listener: s,
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, s, c);
    });
  });
  const l = Array.from(r.childNodes);
  for (let t = 0; t < l.length; t++) {
    const e = l[t];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = j(e);
      n.push(...i), o.appendChild(s);
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
  style: l
}, t) => {
  const e = K(), [s, i] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !r)
      return;
    let c = r;
    function m() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(t, a), o && a.classList.add(...o.split(" ")), l) {
        const p = Oe(l);
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
  }, [r, n, o, l, t]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function V(r, n, o) {
  const l = r.filter(Boolean);
  if (l.length !== 0)
    return l.map((t, e) => {
      var m;
      if (typeof t != "object")
        return t;
      const s = {
        ...t.props,
        key: ((m = t.props) == null ? void 0 : m.key) ?? (o ? `${o}-${e}` : `${e}`)
      };
      let i = s;
      Object.keys(t.slots).forEach((d) => {
        if (!t.slots[d] || !(t.slots[d] instanceof Element) && !t.slots[d].el)
          return;
        const f = d.split(".");
        f.forEach((h, E) => {
          i[h] || (i[h] = {}), E !== f.length - 1 && (i = s[h]);
        });
        const a = t.slots[d];
        let p, _, g = !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, g = a.clone ?? g), i[f[f.length - 1]] = p ? _ ? (...h) => (_(f[f.length - 1], h), /* @__PURE__ */ w.jsx(I, {
          slot: p,
          clone: g
        })) : /* @__PURE__ */ w.jsx(I, {
          slot: p,
          clone: g
        }) : i[f[f.length - 1]], i = s;
      });
      const c = "children";
      return t[c] && (s[c] = V(t[c], n, `${e}`)), s;
    });
}
const je = Ie(({
  slots: r,
  items: n,
  slotItems: o,
  children: l,
  ...t
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [/* @__PURE__ */ w.jsx("div", {
    style: {
      display: "none"
    },
    children: l
  }), /* @__PURE__ */ w.jsx(ee, {
    ...t,
    extra: r.extra ? /* @__PURE__ */ w.jsx(I, {
      slot: r.extra
    }) : t.extra,
    title: r.title ? /* @__PURE__ */ w.jsx(I, {
      slot: r.title
    }) : t.title,
    items: Z(() => n || V(o), [n, o])
  })]
}));
export {
  je as Descriptions,
  je as default
};
