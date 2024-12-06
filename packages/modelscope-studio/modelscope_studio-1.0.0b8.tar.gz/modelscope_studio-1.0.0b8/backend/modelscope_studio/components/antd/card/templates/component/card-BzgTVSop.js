import { g as te, w as I, d as ne, a as v } from "./Index--cFIuHr4.js";
const w = window.ms_globals.React, L = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, $ = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, j = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Card;
var V = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var re = w, oe = Symbol.for("react.element"), se = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, ae = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(r, t, o) {
  var l, n = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) le.call(t, l) && !ce.hasOwnProperty(l) && (n[l] = t[l]);
  if (r && r.defaultProps) for (l in t = r.defaultProps, t) n[l] === void 0 && (n[l] = t[l]);
  return {
    $$typeof: oe,
    type: r,
    key: e,
    ref: s,
    props: n,
    _owner: ae.current
  };
}
O.Fragment = se;
O.jsx = q;
O.jsxs = q;
V.exports = O;
var g = V.exports;
const {
  SvelteComponent: ie,
  assign: N,
  binding_callbacks: B,
  check_outros: ue,
  children: J,
  claim_element: Y,
  claim_space: de,
  component_subscribe: D,
  compute_slots: fe,
  create_slot: pe,
  detach: y,
  element: K,
  empty: G,
  exclude_internal_props: M,
  get_all_dirty_from_scope: _e,
  get_slot_changes: he,
  group_outros: me,
  init: ge,
  insert_hydration: S,
  safe_not_equal: be,
  set_custom_element_data: Q,
  space: we,
  transition_in: R,
  transition_out: P,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: ye,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function W(r) {
  let t, o;
  const l = (
    /*#slots*/
    r[7].default
  ), n = pe(
    l,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = Y(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = J(t);
      n && n.l(s), s.forEach(y), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      S(e, t, s), n && n.m(t, null), r[9](t), o = !0;
    },
    p(e, s) {
      n && n.p && (!o || s & /*$$scope*/
      64) && Ee(
        n,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? he(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : _e(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (R(n, e), o = !0);
    },
    o(e) {
      P(n, e), o = !1;
    },
    d(e) {
      e && y(t), n && n.d(e), r[9](null);
    }
  };
}
function Ie(r) {
  let t, o, l, n, e = (
    /*$$slots*/
    r[4].default && W(r)
  );
  return {
    c() {
      t = K("react-portal-target"), o = we(), e && e.c(), l = G(), this.h();
    },
    l(s) {
      t = Y(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(y), o = de(s), e && e.l(s), l = G(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      S(s, t, a), r[8](t), S(s, o, a), e && e.m(s, a), S(s, l, a), n = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && R(e, 1)) : (e = W(s), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (me(), P(e, 1, 1, () => {
        e = null;
      }), ue());
    },
    i(s) {
      n || (R(e), n = !0);
    },
    o(s) {
      P(e), n = !1;
    },
    d(s) {
      s && (y(t), y(o), y(l)), r[8](null), e && e.d(s);
    }
  };
}
function z(r) {
  const {
    svelteInit: t,
    ...o
  } = r;
  return o;
}
function Se(r, t, o) {
  let l, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = fe(e);
  let {
    svelteInit: c
  } = t;
  const h = I(z(t)), u = I();
  D(r, u, (d) => o(0, l = d));
  const f = I();
  D(r, f, (d) => o(1, n = d));
  const i = [], p = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: m
  } = te() || {}, x = c({
    parent: p,
    props: h,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: m,
    onDestroy(d) {
      i.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", x), xe(() => {
    h.set(z(t));
  }), ve(() => {
    i.forEach((d) => d());
  });
  function C(d) {
    B[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function Z(d) {
    B[d ? "unshift" : "push"](() => {
      n = d, f.set(n);
    });
  }
  return r.$$set = (d) => {
    o(17, t = N(N({}, t), M(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, t = M(t), [l, n, u, f, a, c, s, e, C, Z];
}
class Re extends ie {
  constructor(t) {
    super(), ge(this, t, Se, Ie, be, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, k = window.ms_globals.tree;
function Oe(r) {
  function t(o) {
    const l = I(), n = new Re({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? k;
          return a.nodes = [...a.nodes, s], F({
            createPortal: j,
            node: k
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== l), F({
              createPortal: j,
              node: k
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function ke(r) {
  const [t, o] = U(() => v(r));
  return H(() => {
    let l = !0;
    return r.subscribe((e) => {
      l && (l = !1, e === t) || o(e);
    });
  }, [r]), t;
}
function je(r) {
  const t = L(() => ne(r, (o) => o), [r]);
  return ke(t);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Te(r) {
  return r ? Object.keys(r).reduce((t, o) => {
    const l = r[o];
    return typeof l == "number" && !Pe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function T(r) {
  const t = [], o = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(j(w.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: w.Children.toArray(r._reactElement.props.children).map((n) => {
        if (w.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = T(n.props.el);
          return w.cloneElement(n, {
            ...n.props,
            el: s,
            children: [...w.Children.toArray(n.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(r.getEventListeners()).forEach((n) => {
    r.getEventListeners(n).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      o.addEventListener(a, s, c);
    });
  });
  const l = Array.from(r.childNodes);
  for (let n = 0; n < l.length; n++) {
    const e = l[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = T(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Le(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const E = $(({
  slot: r,
  clone: t,
  className: o,
  style: l
}, n) => {
  const e = ee(), [s, a] = U([]);
  return H(() => {
    var f;
    if (!e.current || !r)
      return;
    let c = r;
    function h() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Le(n, i), o && i.classList.add(...o.split(" ")), l) {
        const p = Te(l);
        Object.keys(p).forEach((_) => {
          i.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var m, x, C;
        (m = e.current) != null && m.contains(c) && ((x = e.current) == null || x.removeChild(c));
        const {
          portals: _,
          clonedElement: b
        } = T(r);
        return c = b, a(_), c.style.display = "contents", h(), (C = e.current) == null || C.appendChild(c), _.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var i, p;
      c.style.display = "", (i = e.current) != null && i.contains(c) && ((p = e.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [r, t, o, l, n]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ae(r, t) {
  const o = L(() => w.Children.toArray(r).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const a = v(e.props.node.slotIndex) || 0, c = v(s.props.node.slotIndex) || 0;
      return a - c === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (v(e.props.node.subSlotIndex) || 0) - (v(s.props.node.subSlotIndex) || 0) : a - c;
    }
    return 0;
  }).map((e) => e.props.node.target), [r, t]);
  return je(o);
}
function X(r, t, o) {
  const l = r.filter(Boolean);
  if (l.length !== 0)
    return l.map((n, e) => {
      var h;
      if (typeof n != "object")
        return n;
      const s = {
        ...n.props,
        key: ((h = n.props) == null ? void 0 : h.key) ?? (o ? `${o}-${e}` : `${e}`)
      };
      let a = s;
      Object.keys(n.slots).forEach((u) => {
        if (!n.slots[u] || !(n.slots[u] instanceof Element) && !n.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((m, x) => {
          a[m] || (a[m] = {}), x !== f.length - 1 && (a = s[m]);
        });
        const i = n.slots[u];
        let p, _, b = !1;
        i instanceof Element ? p = i : (p = i.el, _ = i.callback, b = i.clone ?? b), a[f[f.length - 1]] = p ? _ ? (...m) => (_(f[f.length - 1], m), /* @__PURE__ */ g.jsx(E, {
          slot: p,
          clone: b
        })) : /* @__PURE__ */ g.jsx(E, {
          slot: p,
          clone: b
        }) : a[f[f.length - 1]], a = s;
      });
      const c = "children";
      return n[c] && (s[c] = X(n[c], t, `${e}`)), s;
    });
}
const Be = Oe(({
  children: r,
  containsGrid: t,
  slots: o,
  tabListItems: l,
  tabList: n,
  tabProps: e,
  ...s
}) => {
  const a = Ae(r, "actions");
  return /* @__PURE__ */ g.jsxs(A, {
    ...s,
    tabProps: e,
    tabList: L(() => n || X(l), [n, l]),
    title: o.title ? /* @__PURE__ */ g.jsx(E, {
      slot: o.title
    }) : s.title,
    extra: o.extra ? /* @__PURE__ */ g.jsx(E, {
      slot: o.extra
    }) : s.extra,
    cover: o.cover ? /* @__PURE__ */ g.jsx(E, {
      slot: o.cover
    }) : s.cover,
    tabBarExtraContent: o.tabBarExtraContent ? /* @__PURE__ */ g.jsx(E, {
      slot: o.tabBarExtraContent
    }) : s.tabBarExtraContent,
    actions: a.length > 0 ? a.map((c, h) => /* @__PURE__ */ g.jsx(E, {
      slot: c
    }, h)) : s.actions,
    children: [t ? /* @__PURE__ */ g.jsx(A.Grid, {
      style: {
        display: "none"
      }
    }) : null, r]
  });
});
export {
  Be as Card,
  Be as default
};
