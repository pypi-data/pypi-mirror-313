import { g as X, w as v } from "./Index-B3aUs9Zh.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Avatar;
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
function U(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ne.call(t, l) && !oe.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: re.current
  };
}
R.Fragment = te;
R.jsx = U;
R.jsxs = U;
G.exports = R;
var h = G.exports;
const {
  SvelteComponent: se,
  assign: L,
  binding_callbacks: j,
  check_outros: le,
  children: H,
  claim_element: K,
  claim_space: ie,
  component_subscribe: A,
  compute_slots: ce,
  create_slot: ae,
  detach: g,
  element: M,
  empty: T,
  exclude_internal_props: N,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: C,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: me,
  transition_in: x,
  transition_out: P,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function D(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ae(
    l,
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
      var s = H(t);
      o && o.l(s), s.forEach(g), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && he(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ue(
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
      r || (x(o, e), r = !0);
    },
    o(e) {
      P(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = M("react-portal-target"), r = me(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      t = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(g), r = ie(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, t, c), n[8](t), C(s, r, c), e && e.m(s, c), C(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && x(e, 1)) : (e = D(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (fe(), P(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      o || (x(e), o = !0);
    },
    o(s) {
      P(e), o = !1;
    },
    d(s) {
      s && (g(t), g(r), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function F(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function ve(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ce(e);
  let {
    svelteInit: i
  } = t;
  const w = v(F(t)), u = v();
  A(n, u, (a) => r(0, l = a));
  const p = v();
  A(n, p, (a) => r(1, o = a));
  const d = [], f = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: b
  } = X() || {}, y = i({
    parent: f,
    props: w,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: b,
    onDestroy(a) {
      d.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", y), ge(() => {
    w.set(F(t));
  }), be(() => {
    d.forEach((a) => a());
  });
  function E(a) {
    j[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  function V(a) {
    j[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = L(L({}, t), N(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = N(t), [l, o, u, p, c, i, s, e, E, V];
}
class Ce extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, I = window.ms_globals.tree;
function xe(n) {
  function t(r) {
    const l = v(), o = new Ce({
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
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, s], W({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), W({
              createPortal: O,
              node: I
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
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Re.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function k(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(o.props.el);
          return m.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...m.Children.toArray(o.props.children), ...e]
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
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = k(e);
      t.push(...c), r.appendChild(s);
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
const z = B(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = J(), [s, c] = Y([]);
  return Q(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(o, d), r && d.classList.add(...r.split(" ")), l) {
        const f = Se(l);
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
          clonedElement: S
        } = k(n);
        return i = S, c(_), i.style.display = "contents", w(), (E = e.current) == null || E.appendChild(i), _.length > 0;
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
  }, [n, t, r, l, o]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), Pe = xe(({
  slots: n,
  children: t,
  ...r
}) => /* @__PURE__ */ h.jsxs(h.Fragment, {
  children: [/* @__PURE__ */ h.jsx("div", {
    style: {
      display: "none"
    },
    children: n.icon || n.src ? t : null
  }), /* @__PURE__ */ h.jsx(Z, {
    ...r,
    icon: n.icon ? /* @__PURE__ */ h.jsx(z, {
      slot: n.icon
    }) : r.icon,
    src: n.src ? /* @__PURE__ */ h.jsx(z, {
      slot: n.src
    }) : r.src || void 0,
    children: n.icon || n.src ? null : t
  })]
}));
export {
  Pe as Avatar,
  Pe as default
};
