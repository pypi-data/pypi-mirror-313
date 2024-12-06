import { g as Q, w as E } from "./Index-BDuD4SO1.js";
const m = window.ms_globals.React, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Layout;
var F = {
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
var Z = m, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) te.call(t, l) && !re.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: ne.current
  };
}
S.Fragment = ee;
S.jsx = G;
S.jsxs = G;
F.exports = S;
var k = F.exports;
const {
  SvelteComponent: oe,
  assign: L,
  binding_callbacks: T,
  check_outros: se,
  children: U,
  claim_element: H,
  claim_space: le,
  component_subscribe: N,
  compute_slots: ie,
  create_slot: ae,
  detach: h,
  element: K,
  empty: j,
  exclude_internal_props: A,
  get_all_dirty_from_scope: ce,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert_hydration: v,
  safe_not_equal: _e,
  set_custom_element_data: M,
  space: pe,
  transition_in: C,
  transition_out: O,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: ge,
  onDestroy: we,
  setContext: ye
} = window.__gradio__svelte__internal;
function D(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = ae(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      M(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && me(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? de(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ce(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (C(r, e), o = !0);
    },
    o(e) {
      O(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function be(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = K("react-portal-target"), o = pe(), e && e.c(), l = j(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(h), o = le(s), e && e.l(s), l = j(), this.h();
    },
    h() {
      M(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      v(s, t, a), n[8](t), v(s, o, a), e && e.m(s, a), v(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && C(e, 1)) : (e = D(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (ue(), O(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      r || (C(e), r = !0);
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
function Ee(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ie(e);
  let {
    svelteInit: i
  } = t;
  const g = E(W(t)), u = E();
  N(n, u, (c) => o(0, l = c));
  const p = E();
  N(n, p, (c) => o(1, r = c));
  const d = [], f = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: R,
    subSlotIndex: w
  } = Q() || {}, y = i({
    parent: f,
    props: g,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: R,
    subSlotIndex: w,
    onDestroy(c) {
      d.push(c);
    }
  });
  ye("$$ms-gr-react-wrapper", y), he(() => {
    g.set(W(t));
  }), we(() => {
    d.forEach((c) => c());
  });
  function b(c) {
    T[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function q(c) {
    T[c ? "unshift" : "push"](() => {
      r = c, p.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = L(L({}, t), A(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = A(t), [l, r, u, p, a, i, s, e, b, q];
}
class ve extends oe {
  constructor(t) {
    super(), fe(this, t, Ee, be, _e, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const l = E(), r = new ve({
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
          }, a = e.parent ?? x;
          return a.nodes = [...a.nodes, s], z({
            createPortal: I,
            node: x
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), z({
              createPortal: I,
              node: x
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
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Se.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function P(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(I(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = P(r.props.el);
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
      } = P(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function xe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = V(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = B(), [s, a] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), xe(r, d), o && d.classList.add(...o.split(" ")), l) {
        const f = Re(l);
        Object.keys(f).forEach((_) => {
          d.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var w, y, b;
        (w = e.current) != null && w.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: R
        } = P(n);
        return i = R, a(_), i.style.display = "contents", g(), (b = e.current) == null || b.appendChild(i), _.length > 0;
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
  }, [n, t, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), Pe = Ce(({
  slots: n,
  ...t
}) => /* @__PURE__ */ k.jsx(X.Sider, {
  ...t,
  trigger: n.trigger ? /* @__PURE__ */ k.jsx(Ie, {
    slot: n.trigger,
    clone: !0
  }) : t.trigger === void 0 ? null : t.trigger === "default" ? void 0 : t.trigger
}));
export {
  Pe as LayoutSider,
  Pe as default
};
