import { g as X, w as v } from "./Index-DRLjCSja.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, P = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Card;
var F = {
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
function G(n, t, o) {
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
R.jsx = G;
R.jsxs = G;
F.exports = R;
var E = F.exports;
const {
  SvelteComponent: se,
  assign: T,
  binding_callbacks: j,
  check_outros: le,
  children: U,
  claim_element: H,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ce,
  detach: h,
  element: K,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: C,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: me,
  transition_in: x,
  transition_out: k,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function M(n) {
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
      o || (x(r, e), o = !0);
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
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      t = K("react-portal-target"), o = me(), e && e.c(), l = A(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(h), o = ie(s), e && e.l(s), l = A(), this.h();
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
      16 && x(e, 1)) : (e = M(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (fe(), k(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      r || (x(e), r = !0);
    },
    o(s) {
      k(e), r = !1;
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
  const p = v();
  N(n, p, (c) => o(1, r = c));
  const d = [], f = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: w
  } = X() || {}, b = i({
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
  ye("$$ms-gr-react-wrapper", b), ge(() => {
    g.set(W(t));
  }), be(() => {
    d.forEach((c) => c());
  });
  function y(c) {
    j[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function V(c) {
    j[c ? "unshift" : "push"](() => {
      r = c, p.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = T(T({}, t), D(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = D(t), [l, r, u, p, a, i, s, e, y, V];
}
class Ce extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, I = window.ms_globals.tree;
function xe(n) {
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
function Se(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Re.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function L(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = L(r.props.el);
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
      } = L(e);
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
const O = B(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = J(), [s, a] = Y([]);
  return Q(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Ie(r, d), o && d.classList.add(...o.split(" ")), l) {
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
        } = L(n);
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
  }, [n, t, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), Pe = xe(({
  slots: n,
  ...t
}) => /* @__PURE__ */ E.jsx(Z.Meta, {
  ...t,
  title: n.title ? /* @__PURE__ */ E.jsx(O, {
    slot: n.title
  }) : t.title,
  description: n.description ? /* @__PURE__ */ E.jsx(O, {
    slot: n.description
  }) : t.description,
  avatar: n.avatar ? /* @__PURE__ */ E.jsx(O, {
    slot: n.avatar
  }) : t.avatar
}));
export {
  Pe as CardMeta,
  Pe as default
};
