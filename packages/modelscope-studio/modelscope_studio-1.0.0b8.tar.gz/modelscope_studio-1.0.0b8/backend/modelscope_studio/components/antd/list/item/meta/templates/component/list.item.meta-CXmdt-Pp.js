import { g as X, w as v } from "./Index-BmsEThgr.js";
const h = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, P = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.List;
var z = {
  exports: {}
}, I = {};
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
function G(n, t, r) {
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
I.Fragment = te;
I.jsx = G;
I.jsxs = G;
z.exports = I;
var p = z.exports;
const {
  SvelteComponent: se,
  assign: j,
  binding_callbacks: T,
  check_outros: le,
  children: U,
  claim_element: H,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ce,
  detach: g,
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
function F(n) {
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
      t = K("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
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
      k(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = K("react-portal-target"), r = me(), e && e.c(), l = A(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(g), r = ie(s), e && e.l(s), l = A(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      C(s, t, a), n[8](t), C(s, r, a), e && e.m(s, a), C(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && x(e, 1)) : (e = F(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (fe(), k(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      o || (x(e), o = !0);
    },
    o(s) {
      k(e), o = !1;
    },
    d(s) {
      s && (g(t), g(r), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
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
  const a = ae(e);
  let {
    svelteInit: i
  } = t;
  const w = v(M(t)), u = v();
  N(n, u, (c) => r(0, l = c));
  const m = v();
  N(n, m, (c) => r(1, o = c));
  const d = [], f = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: R,
    subSlotIndex: b
  } = X() || {}, y = i({
    parent: f,
    props: w,
    target: u,
    slot: m,
    slotKey: _,
    slotIndex: R,
    subSlotIndex: b,
    onDestroy(c) {
      d.push(c);
    }
  });
  ye("$$ms-gr-react-wrapper", y), ge(() => {
    w.set(M(t));
  }), be(() => {
    d.forEach((c) => c());
  });
  function E(c) {
    T[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function V(c) {
    T[c ? "unshift" : "push"](() => {
      o = c, m.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = j(j({}, t), D(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, s = c.$$scope);
  }, t = D(t), [l, o, u, m, a, i, s, e, E, V];
}
class Ce extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, S = window.ms_globals.tree;
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
          }, a = e.parent ?? S;
          return a.nodes = [...a.nodes, s], W({
            createPortal: P,
            node: S
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), W({
              createPortal: P,
              node: S
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
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Ie.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function L(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = L(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
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
      } = L(e);
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
const O = B(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = J(), [s, a] = Y([]);
  return Q(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
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
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: R
        } = L(n);
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
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, r, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), Pe = xe(({
  slots: n,
  children: t,
  ...r
}) => /* @__PURE__ */ p.jsxs(p.Fragment, {
  children: [/* @__PURE__ */ p.jsx(p.Fragment, {
    children: t
  }), /* @__PURE__ */ p.jsx(Z.Item.Meta, {
    ...r,
    avatar: n.avatar ? /* @__PURE__ */ p.jsx(O, {
      slot: n.avatar
    }) : r.avatar,
    description: n.description ? /* @__PURE__ */ p.jsx(O, {
      slot: n.description
    }) : r.description,
    title: n.title ? /* @__PURE__ */ p.jsx(O, {
      slot: n.title
    }) : r.title
  })]
}));
export {
  Pe as ListItemMeta,
  Pe as default
};
