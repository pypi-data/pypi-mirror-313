import { g as X, w as x } from "./Index-2IHU-GHS.js";
const h = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, P = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Statistic;
var G = {
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
var $ = h, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ne.call(t, s) && !oe.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: re.current
  };
}
S.Fragment = te;
S.jsx = U;
S.jsxs = U;
G.exports = S;
var m = G.exports;
const {
  SvelteComponent: se,
  assign: L,
  binding_callbacks: T,
  check_outros: le,
  children: H,
  claim_element: K,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ce,
  detach: g,
  element: M,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: v,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: me,
  transition_in: C,
  transition_out: k,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = ce(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = M("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(t);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && he(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? ue(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
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
      k(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = M("react-portal-target"), r = me(), e && e.c(), s = A(), this.h();
    },
    l(l) {
      t = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(g), r = ie(l), e && e.l(l), s = A(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      v(l, t, a), n[8](t), v(l, r, a), e && e.m(l, a), v(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && C(e, 1)) : (e = F(l), e.c(), C(e, 1), e.m(s.parentNode, s)) : e && (fe(), k(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(l) {
      o || (C(e), o = !0);
    },
    o(l) {
      k(e), o = !1;
    },
    d(l) {
      l && (g(t), g(r), g(s)), n[8](null), e && e.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function xe(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = ae(e);
  let {
    svelteInit: i
  } = t;
  const w = x(W(t)), u = x();
  N(n, u, (c) => r(0, s = c));
  const p = x();
  N(n, p, (c) => r(1, o = c));
  const d = [], f = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: R,
    subSlotIndex: b
  } = X() || {}, y = i({
    parent: f,
    props: w,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: R,
    subSlotIndex: b,
    onDestroy(c) {
      d.push(c);
    }
  });
  ye("$$ms-gr-react-wrapper", y), ge(() => {
    w.set(W(t));
  }), be(() => {
    d.forEach((c) => c());
  });
  function E(c) {
    T[c ? "unshift" : "push"](() => {
      s = c, u.set(s);
    });
  }
  function V(c) {
    T[c ? "unshift" : "push"](() => {
      o = c, p.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = L(L({}, t), D(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, l = c.$$scope);
  }, t = D(t), [s, o, u, p, a, i, l, e, E, V];
}
class ve extends se {
  constructor(t) {
    super(), _e(this, t, xe, Ee, pe, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, I = window.ms_globals.tree;
function Ce(n) {
  function t(r) {
    const s = x(), o = new ve({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? I;
          return a.nodes = [...a.nodes, l], z({
            createPortal: P,
            node: I
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), z({
              createPortal: P,
              node: I
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Se.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function j(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...e]
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
      listener: l,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = j(e);
      t.push(...a), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ie(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const O = B(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = J(), [l, a] = Y([]);
  return Q(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(o, d), r && d.classList.add(...r.split(" ")), s) {
        const f = Re(s);
        Object.keys(f).forEach((_) => {
          d.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: R
        } = j(n);
        return i = R, a(_), i.style.display = "contents", w(), (E = e.current) == null || E.appendChild(i), _.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, r, s, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
}), Pe = Ce(({
  children: n,
  value: t,
  slots: r,
  ...s
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [/* @__PURE__ */ m.jsx("div", {
    style: {
      display: "none"
    },
    children: n
  }), /* @__PURE__ */ m.jsx(Z.Countdown, {
    ...s,
    value: typeof t == "number" ? t * 1e3 : t,
    title: r.title ? /* @__PURE__ */ m.jsx(O, {
      slot: r.title
    }) : s.title,
    prefix: r.prefix ? /* @__PURE__ */ m.jsx(O, {
      slot: r.prefix
    }) : s.prefix,
    suffix: r.suffix ? /* @__PURE__ */ m.jsx(O, {
      slot: r.suffix
    }) : s.suffix
  })]
}));
export {
  Pe as StatisticCountdown,
  Pe as default
};
