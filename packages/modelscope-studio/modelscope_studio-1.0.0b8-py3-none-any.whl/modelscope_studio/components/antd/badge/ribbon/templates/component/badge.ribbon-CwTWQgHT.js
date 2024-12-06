import { g as Q, w as v } from "./Index-BUPBpAMF.js";
const m = window.ms_globals.React, q = window.ms_globals.React.forwardRef, V = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Badge;
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
var Z = m, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(n, t, r) {
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
R.jsx = B;
R.jsxs = B;
z.exports = R;
var E = z.exports;
const {
  SvelteComponent: re,
  assign: L,
  binding_callbacks: T,
  check_outros: se,
  children: G,
  claim_element: U,
  claim_space: le,
  component_subscribe: j,
  compute_slots: ie,
  create_slot: ae,
  detach: h,
  element: H,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: ce,
  get_slot_changes: de,
  group_outros: ue,
  init: fe,
  insert_hydration: C,
  safe_not_equal: _e,
  set_custom_element_data: K,
  space: pe,
  transition_in: x,
  transition_out: P,
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
  ), o = ae(
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
      C(e, t, s), o && o.m(t, null), n[9](t), r = !0;
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
        ) : ce(
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
      t = H("react-portal-target"), r = pe(), e && e.c(), l = N(), this.h();
    },
    l(s) {
      t = U(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(t).forEach(h), r = le(s), e && e.l(s), l = N(), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      C(s, t, a), n[8](t), C(s, r, a), e && e.m(s, a), C(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && x(e, 1)) : (e = D(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (ue(), P(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      o || (x(e), o = !0);
    },
    o(s) {
      P(e), o = !1;
    },
    d(s) {
      s && (h(t), h(r), h(l)), n[8](null), e && e.d(s);
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
function Ee(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ie(e);
  let {
    svelteInit: i
  } = t;
  const g = v(F(t)), u = v();
  j(n, u, (c) => r(0, l = c));
  const p = v();
  j(n, p, (c) => r(1, o = c));
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
    onDestroy(c) {
      d.push(c);
    }
  });
  be("$$ms-gr-react-wrapper", b), he(() => {
    g.set(F(t));
  }), we(() => {
    d.forEach((c) => c());
  });
  function y(c) {
    T[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function M(c) {
    T[c ? "unshift" : "push"](() => {
      o = c, p.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = L(L({}, t), A(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, s = c.$$scope);
  }, t = A(t), [l, o, u, p, a, i, s, e, y, M];
}
class ve extends re {
  constructor(t) {
    super(), fe(this, t, Ee, ye, _e, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, I = window.ms_globals.tree;
function Ce(n) {
  function t(r) {
    const l = v(), o = new ve({
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
          }, a = e.parent ?? I;
          return a.nodes = [...a.nodes, s], W({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), W({
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
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !xe.includes(r) ? t[r] = l + "px" : t[r] = l, t;
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
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = k(e);
      t.push(...a), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Se(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Ie = q(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = V(), [s, a] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Se(o, d), r && d.classList.add(...r.split(" ")), l) {
        const f = Re(l);
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
        } = k(n);
        return i = S, a(_), i.style.display = "contents", g(), (y = e.current) == null || y.appendChild(i), _.length > 0;
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
  children: t,
  ...r
}) => /* @__PURE__ */ E.jsx(E.Fragment, {
  children: /* @__PURE__ */ E.jsx(X.Ribbon, {
    ...r,
    text: n.text ? /* @__PURE__ */ E.jsx(Ie, {
      slot: n.text
    }) : r.text,
    children: t
  })
}));
export {
  Pe as BadgeRibbon,
  Pe as default
};
