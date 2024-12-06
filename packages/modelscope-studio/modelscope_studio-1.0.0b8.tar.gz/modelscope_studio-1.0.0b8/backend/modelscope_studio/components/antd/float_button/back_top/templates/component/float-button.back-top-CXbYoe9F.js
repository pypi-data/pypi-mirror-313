import { g as Z, w as x } from "./Index-DqIRd2ha.js";
const h = window.ms_globals.React, V = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.FloatButton;
var M = {
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(t, n, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) oe.call(n, s) && !se.hasOwnProperty(s) && (r[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: te,
    type: t,
    key: e,
    ref: l,
    props: r,
    _owner: re.current
  };
}
S.Fragment = ne;
S.jsx = z;
S.jsxs = z;
M.exports = S;
var p = M.exports;
const {
  SvelteComponent: le,
  assign: F,
  binding_callbacks: L,
  check_outros: ie,
  children: G,
  claim_element: U,
  claim_space: ce,
  component_subscribe: T,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: H,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: K,
  space: he,
  transition_in: R,
  transition_out: P,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function W(t) {
  let n, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = ue(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = H("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = G(n);
      r && r.l(l), l.forEach(g), this.h();
    },
    h() {
      K(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      C(e, n, l), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ge(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? fe(
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
      o || (R(r, e), o = !0);
    },
    o(e) {
      P(r, e), o = !1;
    },
    d(e) {
      e && g(n), r && r.d(e), t[9](null);
    }
  };
}
function ve(t) {
  let n, o, s, r, e = (
    /*$$slots*/
    t[4].default && W(t)
  );
  return {
    c() {
      n = H("react-portal-target"), o = he(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      n = U(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(n).forEach(g), o = ce(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      K(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      C(l, n, c), t[8](n), C(l, o, c), e && e.m(l, c), C(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = W(l), e.c(), R(e, 1), e.m(s.parentNode, s)) : e && (_e(), P(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      r || (R(e), r = !0);
    },
    o(l) {
      P(e), r = !1;
    },
    d(l) {
      l && (g(n), g(o), g(s)), t[8](null), e && e.d(l);
    }
  };
}
function B(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function xe(t, n, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = ae(e);
  let {
    svelteInit: i
  } = n;
  const w = x(B(n)), d = x();
  T(t, d, (a) => o(0, s = a));
  const m = x();
  T(t, m, (a) => o(1, r = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b
  } = Z() || {}, y = i({
    parent: f,
    props: w,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", y), we(() => {
    w.set(B(n));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function E(a) {
    L[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function q(a) {
    L[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return t.$$set = (a) => {
    o(17, n = F(F({}, n), A(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, n = A(n), [s, r, d, m, c, i, l, e, E, q];
}
class Ce extends le {
  constructor(n) {
    super(), pe(this, n, xe, ve, me, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, k = window.ms_globals.tree;
function Re(t) {
  function n(o) {
    const s = x(), r = new Ce({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, l], D({
            createPortal: O,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: O,
              node: k
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
      o(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const s = t[o];
    return typeof s == "number" && !Se.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function j(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(O(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(r.props.el);
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
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = j(e);
      n.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function ke(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const v = V(({
  slot: t,
  clone: n,
  className: o,
  style: s
}, r) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!e.current || !t)
      return;
    let i = t;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(r, u), o && u.classList.add(...o.split(" ")), s) {
        const f = Ie(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: I
        } = j(t);
        return i = I, c(_), i.style.display = "contents", w(), (E = e.current) == null || E.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, o, s, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Oe(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Pe(t, n = !1) {
  try {
    if (n && !Oe(t))
      return;
    if (typeof t == "string") {
      let o = t.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function je(t, n) {
  return X(() => Pe(t, n), [t, n]);
}
const Le = Re(({
  slots: t,
  children: n,
  target: o,
  ...s
}) => {
  var e;
  const r = je(o);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ p.jsx($.BackTop, {
      ...s,
      target: r,
      icon: t.icon ? /* @__PURE__ */ p.jsx(v, {
        clone: !0,
        slot: t.icon
      }) : s.icon,
      description: t.description ? /* @__PURE__ */ p.jsx(v, {
        clone: !0,
        slot: t.description
      }) : s.description,
      tooltip: t.tooltip ? /* @__PURE__ */ p.jsx(v, {
        clone: !0,
        slot: t.tooltip
      }) : s.tooltip,
      badge: {
        ...s.badge,
        count: t["badge.count"] ? /* @__PURE__ */ p.jsx(v, {
          slot: t["badge.count"]
        }) : (e = s.badge) == null ? void 0 : e.count
      }
    })]
  });
});
export {
  Le as FloatButtonBackTop,
  Le as default
};
