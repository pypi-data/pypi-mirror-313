import { g as Z, w as x } from "./Index-s8v41nBW.js";
const g = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, G = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.notification;
var H = {
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
var $ = g, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, oe = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ne.call(n, l) && !re.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ee,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: oe.current
  };
}
R.Fragment = te;
R.jsx = U;
R.jsxs = U;
H.exports = R;
var h = H.exports;
const {
  SvelteComponent: se,
  assign: L,
  binding_callbacks: N,
  check_outros: le,
  children: K,
  claim_element: M,
  claim_space: ie,
  component_subscribe: T,
  compute_slots: ce,
  create_slot: ae,
  detach: w,
  element: q,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: de,
  get_slot_changes: ue,
  group_outros: fe,
  init: _e,
  insert_hydration: I,
  safe_not_equal: pe,
  set_custom_element_data: B,
  space: me,
  transition_in: C,
  transition_out: P,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: ye,
  setContext: be
} = window.__gradio__svelte__internal;
function F(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = ae(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = q("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = M(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(n);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      B(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      I(e, n, s), o && o.m(n, null), t[9](n), r = !0;
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
      r || (C(o, e), r = !0);
    },
    o(e) {
      P(o, e), r = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), t[9](null);
    }
  };
}
function Ee(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && F(t)
  );
  return {
    c() {
      n = q("react-portal-target"), r = me(), e && e.c(), l = A(), this.h();
    },
    l(s) {
      n = M(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(n).forEach(w), r = ie(s), e && e.l(s), l = A(), this.h();
    },
    h() {
      B(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      I(s, n, c), t[8](n), I(s, r, c), e && e.m(s, c), I(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = F(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (fe(), P(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      o || (C(e), o = !0);
    },
    o(s) {
      P(e), o = !1;
    },
    d(s) {
      s && (w(n), w(r), w(l)), t[8](null), e && e.d(s);
    }
  };
}
function W(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function ve(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = ce(e);
  let {
    svelteInit: i
  } = n;
  const f = x(W(n)), u = x();
  T(t, u, (d) => r(0, l = d));
  const _ = x();
  T(t, _, (d) => r(1, o = d));
  const a = [], p = we("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: S,
    subSlotIndex: b
  } = Z() || {}, E = i({
    parent: p,
    props: f,
    target: u,
    slot: _,
    slotKey: m,
    slotIndex: S,
    subSlotIndex: b,
    onDestroy(d) {
      a.push(d);
    }
  });
  be("$$ms-gr-react-wrapper", E), ge(() => {
    f.set(W(n));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    N[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function J(d) {
    N[d ? "unshift" : "push"](() => {
      o = d, _.set(o);
    });
  }
  return t.$$set = (d) => {
    r(17, n = L(L({}, n), D(d))), "svelteInit" in d && r(5, i = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, n = D(n), [l, o, u, _, c, i, s, e, v, J];
}
class xe extends se {
  constructor(n) {
    super(), _e(this, n, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, k = window.ms_globals.tree;
function Ie(t) {
  function n(r) {
    const l = x(), o = new xe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, s], z({
            createPortal: O,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), z({
              createPortal: O,
              node: k
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
      r(n);
    });
  });
}
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !Ce.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function j(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(O(g.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: g.Children.toArray(t._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...g.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(e);
      n.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Se(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const y = Y(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = Q(), [s, c] = X([]);
  return G(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function f() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Se(o, a), r && a.classList.add(...r.split(" ")), l) {
        const p = Re(l);
        Object.keys(p).forEach((m) => {
          a.style[m] = p[m];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var b, E, v;
        (b = e.current) != null && b.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: m,
          clonedElement: S
        } = j(t);
        return i = S, c(m), i.style.display = "contents", f(), (v = e.current) == null || v.appendChild(i), m.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", f(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var a, p;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((p = e.current) == null || p.removeChild(i)), u == null || u.disconnect();
    };
  }, [t, n, r, l, o]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
}), Oe = Ie(({
  slots: t,
  bottom: n,
  rtl: r,
  stack: l,
  top: o,
  children: e,
  visible: s,
  onClose: c,
  onVisible: i,
  ...f
}) => {
  const [u, _] = V.useNotification({
    bottom: n,
    rtl: r,
    stack: l,
    top: o
  });
  return G(() => (s ? u.open({
    ...f,
    btn: t.btn ? /* @__PURE__ */ h.jsx(y, {
      slot: t.btn
    }) : f.btn,
    closeIcon: t.closeIcon ? /* @__PURE__ */ h.jsx(y, {
      slot: t.closeIcon
    }) : f.closeIcon,
    description: t.description ? /* @__PURE__ */ h.jsx(y, {
      slot: t.description
    }) : f.description,
    message: t.message ? /* @__PURE__ */ h.jsx(y, {
      slot: t.message
    }) : f.message,
    icon: t.icon ? /* @__PURE__ */ h.jsx(y, {
      slot: t.icon
    }) : f.icon,
    onClose(...a) {
      i == null || i(!1), c == null || c(...a);
    }
  }) : u.destroy(f.key), () => {
    u.destroy(f.key);
  }), [s]), /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [e, _]
  });
});
export {
  Oe as Notification,
  Oe as default
};
