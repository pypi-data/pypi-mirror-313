import { g as $, w as S } from "./Index-DJEMzCHz.js";
const b = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Segmented;
var z = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = b, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(r, t, s) {
  var o, n = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (o in t) le.call(t, o) && !oe.hasOwnProperty(o) && (n[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) n[o] === void 0 && (n[o] = t[o]);
  return {
    $$typeof: ne,
    type: r,
    key: e,
    ref: l,
    props: n,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = G;
R.jsxs = G;
z.exports = R;
var E = z.exports;
const {
  SvelteComponent: ce,
  assign: j,
  binding_callbacks: L,
  check_outros: ae,
  children: U,
  claim_element: H,
  claim_space: ie,
  component_subscribe: T,
  compute_slots: de,
  create_slot: ue,
  detach: y,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: he,
  insert_hydration: x,
  safe_not_equal: me,
  set_custom_element_data: B,
  space: ge,
  transition_in: C,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function D(r) {
  let t, s;
  const o = (
    /*#slots*/
    r[7].default
  ), n = ue(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(t);
      n && n.l(l), l.forEach(y), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      x(e, t, l), n && n.m(t, null), r[9](t), s = !0;
    },
    p(e, l) {
      n && n.p && (!s || l & /*$$scope*/
      64) && be(
        n,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? _e(
          o,
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
      s || (C(n, e), s = !0);
    },
    o(e) {
      O(n, e), s = !1;
    },
    d(e) {
      e && y(t), n && n.d(e), r[9](null);
    }
  };
}
function Se(r) {
  let t, s, o, n, e = (
    /*$$slots*/
    r[4].default && D(r)
  );
  return {
    c() {
      t = q("react-portal-target"), s = ge(), e && e.c(), o = N(), this.h();
    },
    l(l) {
      t = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(y), s = ie(l), e && e.l(l), o = N(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      x(l, t, c), r[8](t), x(l, s, c), e && e.m(l, c), x(l, o, c), n = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = D(l), e.c(), C(e, 1), e.m(o.parentNode, o)) : e && (pe(), O(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(l) {
      n || (C(e), n = !0);
    },
    o(l) {
      O(e), n = !1;
    },
    d(l) {
      l && (y(t), y(s), y(o)), r[8](null), e && e.d(l);
    }
  };
}
function F(r) {
  const {
    svelteInit: t,
    ...s
  } = r;
  return s;
}
function xe(r, t, s) {
  let o, n, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = de(e);
  let {
    svelteInit: a
  } = t;
  const m = S(F(t)), d = S();
  T(r, d, (u) => s(0, o = u));
  const f = S();
  T(r, f, (u) => s(1, n = u));
  const i = [], _ = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: h
  } = $() || {}, w = a({
    parent: _,
    props: m,
    target: d,
    slot: f,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: h,
    onDestroy(u) {
      i.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", w), we(() => {
    m.set(F(t));
  }), ye(() => {
    i.forEach((u) => u());
  });
  function v(u) {
    L[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function J(u) {
    L[u ? "unshift" : "push"](() => {
      n = u, f.set(n);
    });
  }
  return r.$$set = (u) => {
    s(17, t = j(j({}, t), A(u))), "svelteInit" in u && s(5, a = u.svelteInit), "$$scope" in u && s(6, l = u.$$scope);
  }, t = A(t), [o, n, d, f, c, a, l, e, v, J];
}
class Ce extends ce {
  constructor(t) {
    super(), he(this, t, xe, Se, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, k = window.ms_globals.tree;
function Re(r) {
  function t(s) {
    const o = S(), n = new Ce({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, l], M({
            createPortal: I,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== o), M({
              createPortal: I,
              node: k
            });
          }), l;
        },
        ...s.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(r) {
  return r ? Object.keys(r).reduce((t, s) => {
    const o = r[s];
    return typeof o == "number" && !ke.includes(s) ? t[s] = o + "px" : t[s] = o, t;
  }, {}) : {};
}
function P(r) {
  const t = [], s = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(I(b.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: b.Children.toArray(r._reactElement.props.children).map((n) => {
        if (b.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = P(n.props.el);
          return b.cloneElement(n, {
            ...n.props,
            el: l,
            children: [...b.Children.toArray(n.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(r.getEventListeners()).forEach((n) => {
    r.getEventListeners(n).forEach(({
      listener: l,
      type: c,
      useCapture: a
    }) => {
      s.addEventListener(c, l, a);
    });
  });
  const o = Array.from(r.childNodes);
  for (let n = 0; n < o.length; n++) {
    const e = o[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = P(e);
      t.push(...c), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function Oe(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const W = Y(({
  slot: r,
  clone: t,
  className: s,
  style: o
}, n) => {
  const e = K(), [l, c] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !r)
      return;
    let a = r;
    function m() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(n, i), s && i.classList.add(...s.split(" ")), o) {
        const _ = Ie(o);
        Object.keys(_).forEach((p) => {
          i.style[p] = _[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var h, w, v;
        (h = e.current) != null && h.contains(a) && ((w = e.current) == null || w.removeChild(a));
        const {
          portals: p,
          clonedElement: g
        } = P(r);
        return a = g, c(p), a.style.display = "contents", m(), (v = e.current) == null || v.appendChild(a), p.length > 0;
      };
      i() || (d = new window.MutationObserver(() => {
        i() && (d == null || d.disconnect());
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", m(), (f = e.current) == null || f.appendChild(a);
    return () => {
      var i, _;
      a.style.display = "", (i = e.current) != null && i.contains(a) && ((_ = e.current) == null || _.removeChild(a)), d == null || d.disconnect();
    };
  }, [r, t, s, o, n]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function V(r, t, s) {
  const o = r.filter(Boolean);
  if (o.length !== 0)
    return o.map((n, e) => {
      var m;
      if (typeof n != "object")
        return t != null && t.fallback ? t.fallback(n) : n;
      const l = {
        ...n.props,
        key: ((m = n.props) == null ? void 0 : m.key) ?? (s ? `${s}-${e}` : `${e}`)
      };
      let c = l;
      Object.keys(n.slots).forEach((d) => {
        if (!n.slots[d] || !(n.slots[d] instanceof Element) && !n.slots[d].el)
          return;
        const f = d.split(".");
        f.forEach((h, w) => {
          c[h] || (c[h] = {}), w !== f.length - 1 && (c = l[h]);
        });
        const i = n.slots[d];
        let _, p, g = (t == null ? void 0 : t.clone) ?? !1;
        i instanceof Element ? _ = i : (_ = i.el, p = i.callback, g = i.clone ?? g), c[f[f.length - 1]] = _ ? p ? (...h) => (p(f[f.length - 1], h), /* @__PURE__ */ E.jsx(W, {
          slot: _,
          clone: g
        })) : /* @__PURE__ */ E.jsx(W, {
          slot: _,
          clone: g
        }) : c[f[f.length - 1]], c = l;
      });
      const a = (t == null ? void 0 : t.children) || "children";
      return n[a] && (l[a] = V(n[a], t, `${e}`)), l;
    });
}
const je = Re(({
  slotItems: r,
  options: t,
  onChange: s,
  onValueChange: o,
  children: n,
  ...e
}) => /* @__PURE__ */ E.jsxs(E.Fragment, {
  children: [/* @__PURE__ */ E.jsx("div", {
    style: {
      display: "none"
    },
    children: n
  }), /* @__PURE__ */ E.jsx(ee, {
    ...e,
    onChange: (l) => {
      s == null || s(l), o(l);
    },
    options: Z(() => t || V(r, {
      clone: !0
    }), [t, r])
  })]
}));
export {
  je as Segmented,
  je as default
};
