import { g as X, w as x } from "./Index-CQ7HsPvT.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, P = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Result;
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
var $ = m, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ne.call(t, s) && !oe.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: re.current
  };
}
S.Fragment = te;
S.jsx = U;
S.jsxs = U;
G.exports = S;
var w = G.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: j,
  check_outros: se,
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
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: _e,
  insert_hydration: C,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: me,
  transition_in: R,
  transition_out: k,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function W(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ce(
    s,
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
      var l = H(t);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      C(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && he(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? de(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ue(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (R(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      t = M("react-portal-target"), o = me(), e && e.c(), s = A(), this.h();
    },
    l(l) {
      t = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(h), o = ie(l), e && e.l(l), s = A(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      C(l, t, a), n[8](t), C(l, o, a), e && e.m(l, a), C(l, s, a), r = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && R(e, 1)) : (e = W(l), e.c(), R(e, 1), e.m(s.parentNode, s)) : e && (fe(), k(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(l) {
      r || (R(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (h(t), h(o), h(s)), n[8](null), e && e.d(l);
    }
  };
}
function z(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function ve(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = ae(e);
  let {
    svelteInit: i
  } = t;
  const g = x(z(t)), d = x();
  N(n, d, (c) => o(0, s = c));
  const p = x();
  N(n, p, (c) => o(1, r = c));
  const u = [], f = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b
  } = X() || {}, y = i({
    parent: f,
    props: g,
    target: d,
    slot: p,
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b,
    onDestroy(c) {
      u.push(c);
    }
  });
  ye("$$ms-gr-react-wrapper", y), ge(() => {
    g.set(z(t));
  }), be(() => {
    u.forEach((c) => c());
  });
  function E(c) {
    j[c ? "unshift" : "push"](() => {
      s = c, d.set(s);
    });
  }
  function V(c) {
    j[c ? "unshift" : "push"](() => {
      r = c, p.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = L(L({}, t), D(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, l = c.$$scope);
  }, t = D(t), [s, r, d, p, a, i, l, e, E, V];
}
class xe extends le {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const s = x(), r = new xe({
      ...o,
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
          }, a = e.parent ?? O;
          return a.nodes = [...a.nodes, l], F({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), F({
              createPortal: P,
              node: O
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !Re.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function T(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = T(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: l,
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
      listener: l,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = T(e);
      t.push(...a), o.appendChild(l);
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
const v = B(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = J(), [l, a] = Y([]);
  return Q(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Ie(r, u), o && u.classList.add(...o.split(" ")), s) {
        const f = Se(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: I
        } = T(n);
        return i = I, a(_), i.style.display = "contents", g(), (E = e.current) == null || E.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, o, s, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
}), Pe = Ce(({
  slots: n,
  ...t
}) => /* @__PURE__ */ w.jsx(Z, {
  ...t,
  extra: n.extra ? /* @__PURE__ */ w.jsx(v, {
    slot: n.extra
  }) : t.extra,
  icon: n.icon ? /* @__PURE__ */ w.jsx(v, {
    slot: n.icon
  }) : t.icon,
  subTitle: n.subTitle ? /* @__PURE__ */ w.jsx(v, {
    slot: n.subTitle
  }) : t.subTitle,
  title: n.title ? /* @__PURE__ */ w.jsx(v, {
    slot: n.title
  }) : t.title
}));
export {
  Pe as Result,
  Pe as default
};
