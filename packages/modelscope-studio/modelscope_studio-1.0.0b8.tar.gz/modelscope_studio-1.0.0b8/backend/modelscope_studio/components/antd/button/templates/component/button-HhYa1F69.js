import { g as Q, w as E } from "./Index-Bedy1tXN.js";
const m = window.ms_globals.React, q = window.ms_globals.React.forwardRef, V = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Button;
var B = {
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
var Z = m, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) te.call(t, l) && !oe.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: ne.current
  };
}
R.Fragment = ee;
R.jsx = F;
R.jsxs = F;
B.exports = R;
var k = B.exports;
const {
  SvelteComponent: re,
  assign: L,
  binding_callbacks: T,
  check_outros: se,
  children: G,
  claim_element: U,
  claim_space: le,
  component_subscribe: N,
  compute_slots: ie,
  create_slot: ce,
  detach: h,
  element: H,
  empty: j,
  exclude_internal_props: A,
  get_all_dirty_from_scope: ae,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert_hydration: v,
  safe_not_equal: _e,
  set_custom_element_data: K,
  space: pe,
  transition_in: C,
  transition_out: O,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: ge,
  onDestroy: we,
  setContext: be
} = window.__gradio__svelte__internal;
function D(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ce(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = H("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = G(t);
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && me(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? de(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ae(
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
      O(o, e), r = !1;
    },
    d(e) {
      e && h(t), o && o.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = H("react-portal-target"), r = pe(), e && e.c(), l = j(), this.h();
    },
    l(s) {
      t = U(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(t).forEach(h), r = le(s), e && e.l(s), l = j(), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      v(s, t, c), n[8](t), v(s, r, c), e && e.m(s, c), v(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = D(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (ue(), O(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      o || (C(e), o = !0);
    },
    o(s) {
      O(e), o = !1;
    },
    d(s) {
      s && (h(t), h(r), h(l)), n[8](null), e && e.d(s);
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
function Ee(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ie(e);
  let {
    svelteInit: i
  } = t;
  const g = E(W(t)), u = E();
  N(n, u, (a) => r(0, l = a));
  const p = E();
  N(n, p, (a) => r(1, o = a));
  const d = [], f = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: w
  } = Q() || {}, b = i({
    parent: f,
    props: g,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: w,
    onDestroy(a) {
      d.push(a);
    }
  });
  be("$$ms-gr-react-wrapper", b), he(() => {
    g.set(W(t));
  }), we(() => {
    d.forEach((a) => a());
  });
  function y(a) {
    T[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  function M(a) {
    T[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = L(L({}, t), A(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = A(t), [l, o, u, p, c, i, s, e, y, M];
}
class ve extends re {
  constructor(t) {
    super(), fe(this, t, Ee, ye, _e, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ce(n) {
  function t(r) {
    const l = E(), o = new ve({
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
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, s], z({
            createPortal: I,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), z({
              createPortal: I,
              node: x
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
function P(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(I(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = P(o.props.el);
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
      } = P(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function xe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = q(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = V(), [s, c] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), xe(o, d), r && d.classList.add(...r.split(" ")), l) {
        const f = Se(l);
        Object.keys(f).forEach((_) => {
          d.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var w, b, y;
        (w = e.current) != null && w.contains(i) && ((b = e.current) == null || b.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = P(n);
        return i = S, c(_), i.style.display = "contents", g(), (y = e.current) == null || y.appendChild(i), _.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (p = e.current) == null || p.appendChild(i);
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
}), Pe = Ce(({
  slots: n,
  ...t
}) => /* @__PURE__ */ k.jsx(X, {
  ...t,
  icon: n.icon ? /* @__PURE__ */ k.jsx(Ie, {
    slot: n.icon
  }) : t.icon
}));
export {
  Pe as Button,
  Pe as default
};
