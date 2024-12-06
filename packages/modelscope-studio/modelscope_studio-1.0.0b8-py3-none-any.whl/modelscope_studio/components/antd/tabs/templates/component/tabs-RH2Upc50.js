import { g as ee, w as C } from "./Index-DXdiwmbL.js";
const E = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, M = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tabs;
var U = {
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
var ne = E, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(e, n, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) se.call(n, l) && !ie.hasOwnProperty(l) && (o[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: re,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: le.current
  };
}
R.Fragment = oe;
R.jsx = G;
R.jsxs = G;
U.exports = R;
var h = U.exports;
const {
  SvelteComponent: ae,
  assign: B,
  binding_callbacks: L,
  check_outros: ce,
  children: H,
  claim_element: q,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: x,
  element: V,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: _e,
  get_slot_changes: pe,
  group_outros: he,
  init: me,
  insert_hydration: I,
  safe_not_equal: ge,
  set_custom_element_data: J,
  space: be,
  transition_in: S,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: ye
} = window.__gradio__svelte__internal;
function z(e) {
  let n, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = fe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = V("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = q(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(n);
      o && o.l(s), s.forEach(x), this.h();
    },
    h() {
      J(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      I(t, n, s), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && we(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? pe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : _e(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (S(o, t), r = !0);
    },
    o(t) {
      k(o, t), r = !1;
    },
    d(t) {
      t && x(n), o && o.d(t), e[9](null);
    }
  };
}
function Ce(e) {
  let n, r, l, o, t = (
    /*$$slots*/
    e[4].default && z(e)
  );
  return {
    c() {
      n = V("react-portal-target"), r = be(), t && t.c(), l = N(), this.h();
    },
    l(s) {
      n = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(x), r = ue(s), t && t.l(s), l = N(), this.h();
    },
    h() {
      J(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      I(s, n, i), e[8](n), I(s, r, i), t && t.m(s, i), I(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && S(t, 1)) : (t = z(s), t.c(), S(t, 1), t.m(l.parentNode, l)) : t && (he(), k(t, 1, 1, () => {
        t = null;
      }), ce());
    },
    i(s) {
      o || (S(t), o = !0);
    },
    o(s) {
      k(t), o = !1;
    },
    d(s) {
      s && (x(n), x(r), x(l)), e[8](null), t && t.d(s);
    }
  };
}
function W(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ie(e, n, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const i = de(t);
  let {
    svelteInit: a
  } = n;
  const p = C(W(n)), u = C();
  F(e, u, (d) => r(0, l = d));
  const f = C();
  F(e, f, (d) => r(1, o = d));
  const c = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: g
  } = ee() || {}, v = a({
    parent: _,
    props: p,
    target: u,
    slot: f,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: g,
    onDestroy(d) {
      c.push(d);
    }
  });
  ye("$$ms-gr-react-wrapper", v), Ee(() => {
    p.set(W(n));
  }), xe(() => {
    c.forEach((d) => d());
  });
  function y(d) {
    L[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function K(d) {
    L[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return e.$$set = (d) => {
    r(17, n = B(B({}, n), A(d))), "svelteInit" in d && r(5, a = d.svelteInit), "$$scope" in d && r(6, s = d.$$scope);
  }, n = A(n), [l, o, u, f, i, a, s, t, y, K];
}
class Se extends ae {
  constructor(n) {
    super(), me(this, n, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, P = window.ms_globals.tree;
function Re(e) {
  function n(r) {
    const l = C(), o = new Se({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? P;
          return i.nodes = [...i.nodes, s], D({
            createPortal: j,
            node: P
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((a) => a.svelteInstance !== l), D({
              createPortal: j,
              node: P
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
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !Pe.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function T(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(j(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = T(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...E.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: i,
      useCapture: a
    }) => {
      r.addEventListener(i, s, a);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = T(t);
      n.push(...i), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function je(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = Q(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, o) => {
  const t = X(), [s, i] = Z([]);
  return $(() => {
    var f;
    if (!t.current || !e)
      return;
    let a = e;
    function p() {
      let c = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (c = a.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), je(o, c), r && c.classList.add(...r.split(" ")), l) {
        const _ = Oe(l);
        Object.keys(_).forEach((m) => {
          c.style[m] = _[m];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var g, v, y;
        (g = t.current) != null && g.contains(a) && ((v = t.current) == null || v.removeChild(a));
        const {
          portals: m,
          clonedElement: w
        } = T(e);
        return a = w, i(m), a.style.display = "contents", p(), (y = t.current) == null || y.appendChild(a), m.length > 0;
      };
      c() || (u = new window.MutationObserver(() => {
        c() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", p(), (f = t.current) == null || f.appendChild(a);
    return () => {
      var c, _;
      a.style.display = "", (c = t.current) != null && c.contains(a) && ((_ = t.current) == null || _.removeChild(a)), u == null || u.disconnect();
    };
  }, [e, n, r, l, o]), E.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Te(e, n = !1) {
  try {
    if (n && !ke(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function O(e, n) {
  return M(() => Te(e, n), [e, n]);
}
function Be(e) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (n[r] = e[r]), n), {});
}
function Y(e, n, r) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, t) => {
      var p;
      if (typeof o != "object")
        return o;
      const s = {
        ...o.props,
        key: ((p = o.props) == null ? void 0 : p.key) ?? (r ? `${r}-${t}` : `${t}`)
      };
      let i = s;
      Object.keys(o.slots).forEach((u) => {
        if (!o.slots[u] || !(o.slots[u] instanceof Element) && !o.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((g, v) => {
          i[g] || (i[g] = {}), v !== f.length - 1 && (i = s[g]);
        });
        const c = o.slots[u];
        let _, m, w = !1;
        c instanceof Element ? _ = c : (_ = c.el, m = c.callback, w = c.clone ?? w), i[f[f.length - 1]] = _ ? m ? (...g) => (m(f[f.length - 1], g), /* @__PURE__ */ h.jsx(b, {
          slot: _,
          clone: w
        })) : /* @__PURE__ */ h.jsx(b, {
          slot: _,
          clone: w
        }) : i[f[f.length - 1]], i = s;
      });
      const a = "children";
      return o[a] && (s[a] = Y(o[a], n, `${t}`)), s;
    });
}
function Le(e, n) {
  return e ? /* @__PURE__ */ h.jsx(b, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Fe({
  key: e,
  setSlotParams: n,
  slots: r
}, l) {
  return r[e] ? (...o) => (n(e, o), Le(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ae = Re(({
  slots: e,
  indicator: n,
  items: r,
  onChange: l,
  slotItems: o,
  more: t,
  children: s,
  renderTabBar: i,
  setSlotParams: a,
  ...p
}) => {
  const u = O(n == null ? void 0 : n.size), f = O(t == null ? void 0 : t.getPopupContainer), c = O(i);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ h.jsx(te, {
      ...p,
      indicator: u ? {
        ...n,
        size: u
      } : n,
      renderTabBar: e.renderTabBar ? Fe({
        slots: e,
        setSlotParams: a,
        key: "renderTabBar"
      }) : c,
      items: M(() => r || Y(o), [r, o]),
      more: Be({
        ...t || {},
        getPopupContainer: f || (t == null ? void 0 : t.getPopupContainer),
        icon: e["more.icon"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["more.icon"]
        }) : t == null ? void 0 : t.icon
      }),
      tabBarExtraContent: e.tabBarExtraContent ? /* @__PURE__ */ h.jsx(b, {
        slot: e.tabBarExtraContent
      }) : e["tabBarExtraContent.left"] || e["tabBarExtraContent.right"] ? {
        left: e["tabBarExtraContent.left"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["tabBarExtraContent.left"]
        }) : void 0,
        right: e["tabBarExtraContent.right"] ? /* @__PURE__ */ h.jsx(b, {
          slot: e["tabBarExtraContent.right"]
        }) : void 0
      } : p.tabBarExtraContent,
      addIcon: e.addIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.addIcon
      }) : p.addIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ h.jsx(b, {
        slot: e.removeIcon
      }) : p.removeIcon,
      onChange: (_) => {
        l == null || l(_);
      }
    })]
  });
});
export {
  Ae as Tabs,
  Ae as default
};
