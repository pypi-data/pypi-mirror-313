import { g as X, w as y } from "./Index-8Mmnv35_.js";
const m = window.ms_globals.React, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, Q = window.ms_globals.React.createElement, I = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Row, $ = window.ms_globals.antd.Col;
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
var ee = m, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) oe.call(t, l) && !se.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: re.current
  };
}
R.Fragment = ne;
R.jsx = G;
R.jsxs = G;
F.exports = R;
var k = F.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: T,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ae,
  component_subscribe: N,
  compute_slots: ce,
  create_slot: de,
  detach: h,
  element: K,
  empty: j,
  exclude_internal_props: A,
  get_all_dirty_from_scope: ue,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: v,
  safe_not_equal: me,
  set_custom_element_data: M,
  space: he,
  transition_in: C,
  transition_out: O,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: Ee,
  setContext: ye
} = window.__gradio__svelte__internal;
function D(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = de(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      M(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      v(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ge(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? fe(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ue(
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
function ve(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = K("react-portal-target"), r = he(), e && e.c(), l = j(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(h), r = ae(s), e && e.l(s), l = j(), this.h();
    },
    h() {
      M(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      v(s, t, a), n[8](t), v(s, r, a), e && e.m(s, a), v(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && C(e, 1)) : (e = D(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (_e(), O(e, 1, 1, () => {
        e = null;
      }), ie());
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
function Ce(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ce(e);
  let {
    svelteInit: i
  } = t;
  const g = y(W(t)), u = y();
  N(n, u, (c) => r(0, l = c));
  const p = y();
  N(n, p, (c) => r(1, o = c));
  const d = [], f = be("$$ms-gr-react-wrapper"), {
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
  ye("$$ms-gr-react-wrapper", b), we(() => {
    g.set(W(t));
  }), Ee(() => {
    d.forEach((c) => c());
  });
  function E(c) {
    T[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function q(c) {
    T[c ? "unshift" : "push"](() => {
      o = c, p.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = L(L({}, t), A(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, s = c.$$scope);
  }, t = A(t), [l, o, u, p, a, i, s, e, E, q];
}
class Re extends le {
  constructor(t) {
    super(), pe(this, t, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, x = window.ms_globals.tree;
function Se(n) {
  function t(r) {
    const l = y(), o = new Re({
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
function Ie(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !xe.includes(r) ? t[r] = l + "px" : t[r] = l, t;
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
      } = P(e);
      t.push(...a), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Pe = V(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = B(), [s, a] = J([]);
  return Y(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Oe(o, d), r && d.classList.add(...r.split(" ")), l) {
        const f = Ie(l);
        Object.keys(f).forEach((_) => {
          d.style[_] = f[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var w, b, E;
        (w = e.current) != null && w.contains(i) && ((b = e.current) == null || b.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = P(n);
        return i = S, a(_), i.style.display = "contents", g(), (E = e.current) == null || E.appendChild(i), _.length > 0;
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
}), Le = Se(({
  cols: n,
  children: t,
  ...r
}) => /* @__PURE__ */ k.jsxs(Z, {
  ...r,
  children: [t, n == null ? void 0 : n.map((l, o) => {
    if (!l)
      return;
    const {
      el: e,
      props: s
    } = l;
    return /* @__PURE__ */ Q($, {
      ...s,
      key: o
    }, e && /* @__PURE__ */ k.jsx(Pe, {
      slot: e
    }));
  })]
}));
export {
  Le as Row,
  Le as default
};
