import { g as Z, w as v } from "./Index-BKaF-s80.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.createElement, P = window.ms_globals.ReactDOM.createPortal, L = window.ms_globals.antd.Splitter;
var G = {
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
var $ = m, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ne.call(t, l) && !oe.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: re.current
  };
}
R.Fragment = te;
R.jsx = U;
R.jsxs = U;
G.exports = R;
var w = G.exports;
const {
  SvelteComponent: se,
  assign: T,
  binding_callbacks: j,
  check_outros: le,
  children: H,
  claim_element: K,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ce,
  detach: h,
  element: M,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: pe,
  insert_hydration: C,
  safe_not_equal: _e,
  set_custom_element_data: q,
  space: me,
  transition_in: S,
  transition_out: O,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = ce(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = M("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(t);
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && he(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? ue(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (S(r, e), o = !0);
    },
    o(e) {
      O(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = M("react-portal-target"), o = me(), e && e.c(), l = A(), this.h();
    },
    l(s) {
      t = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(h), o = ie(s), e && e.l(s), l = A(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      C(s, t, a), n[8](t), C(s, o, a), e && e.m(s, a), C(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && S(e, 1)) : (e = F(s), e.c(), S(e, 1), e.m(l.parentNode, l)) : e && (fe(), O(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      r || (S(e), r = !0);
    },
    o(s) {
      O(e), r = !1;
    },
    d(s) {
      s && (h(t), h(o), h(l)), n[8](null), e && e.d(s);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function ve(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ae(e);
  let {
    svelteInit: i
  } = t;
  const g = v(W(t)), u = v();
  N(n, u, (c) => o(0, l = c));
  const _ = v();
  N(n, _, (c) => o(1, r = c));
  const d = [], f = we("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: x,
    subSlotIndex: b
  } = Z() || {}, y = i({
    parent: f,
    props: g,
    target: u,
    slot: _,
    slotKey: p,
    slotIndex: x,
    subSlotIndex: b,
    onDestroy(c) {
      d.push(c);
    }
  });
  ye("$$ms-gr-react-wrapper", y), ge(() => {
    g.set(W(t));
  }), be(() => {
    d.forEach((c) => c());
  });
  function E(c) {
    j[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function V(c) {
    j[c ? "unshift" : "push"](() => {
      r = c, _.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = T(T({}, t), D(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = D(t), [l, r, u, _, a, i, s, e, E, V];
}
class Ce extends se {
  constructor(t) {
    super(), pe(this, t, ve, Ee, _e, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(n) {
  function t(o) {
    const l = v(), r = new Ce({
      ...o,
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
          }, a = e.parent ?? I;
          return a.nodes = [...a.nodes, s], z({
            createPortal: P,
            node: I
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), z({
              createPortal: P,
              node: I
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Re.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function k(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...m.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = k(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Ie(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Pe = B(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = J(), [s, a] = Y([]);
  return Q(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(r, d), o && d.classList.add(...o.split(" ")), l) {
        const f = xe(l);
        Object.keys(f).forEach((p) => {
          d.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: p,
          clonedElement: x
        } = k(n);
        return i = x, a(p), i.style.display = "contents", g(), (E = e.current) == null || E.appendChild(i), p.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), ke = Se(({
  items: n,
  children: t,
  ...o
}) => /* @__PURE__ */ w.jsxs(w.Fragment, {
  children: [/* @__PURE__ */ w.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ w.jsx(L, {
    ...o,
    children: n == null ? void 0 : n.map((l, r) => {
      if (!l)
        return;
      const {
        el: e,
        props: s
      } = l;
      return /* @__PURE__ */ X(L.Panel, {
        ...s,
        key: r
      }, e && /* @__PURE__ */ w.jsx(Pe, {
        slot: e
      }));
    })
  })]
}));
export {
  ke as Splitter,
  ke as default
};
