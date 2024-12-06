import { g as Z, w as C } from "./Index-CqFgpvsM.js";
const h = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Switch;
var G = {
  exports: {}
}, k = {};
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
k.Fragment = te;
k.jsx = U;
k.jsxs = U;
G.exports = k;
var m = G.exports;
const {
  SvelteComponent: se,
  assign: L,
  binding_callbacks: j,
  check_outros: le,
  children: H,
  claim_element: K,
  claim_space: ie,
  component_subscribe: T,
  compute_slots: ce,
  create_slot: ae,
  detach: w,
  element: M,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: v,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: he,
  transition_in: S,
  transition_out: O,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ge,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function D(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = ae(
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
      r && r.l(l), l.forEach(w), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && me(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? ue(
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
      o || (S(r, e), o = !0);
    },
    o(e) {
      O(r, e), o = !1;
    },
    d(e) {
      e && w(t), r && r.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = M("react-portal-target"), o = he(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(w), o = ie(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, t, c), n[8](t), v(l, o, c), e && e.m(l, c), v(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && S(e, 1)) : (e = D(l), e.c(), S(e, 1), e.m(s.parentNode, s)) : e && (fe(), O(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(l) {
      r || (S(e), r = !0);
    },
    o(l) {
      O(e), r = !1;
    },
    d(l) {
      l && (w(t), w(o), w(s)), n[8](null), e && e.d(l);
    }
  };
}
function F(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ce(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ce(e);
  let {
    svelteInit: i
  } = t;
  const g = C(F(t)), u = C();
  T(n, u, (a) => o(0, s = a));
  const p = C();
  T(n, p, (a) => o(1, r = a));
  const d = [], f = ge("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: x,
    subSlotIndex: b
  } = Z() || {}, y = i({
    parent: f,
    props: g,
    target: u,
    slot: p,
    slotKey: _,
    slotIndex: x,
    subSlotIndex: b,
    onDestroy(a) {
      d.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", y), we(() => {
    g.set(F(t));
  }), be(() => {
    d.forEach((a) => a());
  });
  function E(a) {
    j[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  function B(a) {
    j[a ? "unshift" : "push"](() => {
      r = a, p.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = L(L({}, t), A(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, t = A(t), [s, r, u, p, c, i, l, e, E, B];
}
class ve extends se {
  constructor(t) {
    super(), _e(this, t, Ce, Ee, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, R = window.ms_globals.tree;
function Se(n) {
  function t(o) {
    const s = C(), r = new ve({
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
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, l], W({
            createPortal: I,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), W({
              createPortal: I,
              node: R
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
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !ke.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function P(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(I(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = P(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...h.Children.toArray(r.props.children), ...e]
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
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = P(e);
      t.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Re(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const z = J(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = Y(), [l, c] = Q([]);
  return X(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Re(r, d), o && d.classList.add(...o.split(" ")), s) {
        const f = xe(s);
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
          clonedElement: x
        } = P(n);
        return i = x, c(_), i.style.display = "contents", g(), (E = e.current) == null || E.appendChild(i), _.length > 0;
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
  }, [n, t, o, s, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
}), Oe = Se(({
  slots: n,
  children: t,
  onValueChange: o,
  onChange: s,
  ...r
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [/* @__PURE__ */ m.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ m.jsx(V, {
    ...r,
    onChange: (e, ...l) => {
      o == null || o(e), s == null || s(e, ...l);
    },
    checkedChildren: n.checkedChildren ? /* @__PURE__ */ m.jsx(z, {
      slot: n.checkedChildren
    }) : r.checkedChildren,
    unCheckedChildren: n.unCheckedChildren ? /* @__PURE__ */ m.jsx(z, {
      slot: n.unCheckedChildren
    }) : r.unCheckedChildren
  })]
}));
export {
  Oe as Switch,
  Oe as default
};
