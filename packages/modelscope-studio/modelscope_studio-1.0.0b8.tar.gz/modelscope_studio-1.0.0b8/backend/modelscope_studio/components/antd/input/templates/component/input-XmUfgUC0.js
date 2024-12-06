import { b as $, g as ee, w as I } from "./Index-FohUJ0Is.js";
const g = window.ms_globals.React, Z = window.ms_globals.React.forwardRef, j = window.ms_globals.React.useRef, q = window.ms_globals.React.useState, k = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Input;
function ne(e, n) {
  return $(e, n);
}
var G = {
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
var re = g, oe = Symbol.for("react.element"), se = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, ie = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(e, n, t) {
  var s, o = {}, r = null, l = null;
  t !== void 0 && (r = "" + t), n.key !== void 0 && (r = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) le.call(n, s) && !ae.hasOwnProperty(s) && (o[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: oe,
    type: e,
    key: r,
    ref: l,
    props: o,
    _owner: ie.current
  };
}
O.Fragment = se;
O.jsx = H;
O.jsxs = H;
G.exports = O;
var p = G.exports;
const {
  SvelteComponent: ce,
  assign: T,
  binding_callbacks: N,
  check_outros: ue,
  children: K,
  claim_element: J,
  claim_space: de,
  component_subscribe: V,
  compute_slots: fe,
  create_slot: _e,
  detach: y,
  element: Y,
  empty: W,
  exclude_internal_props: D,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: ge,
  insert_hydration: R,
  safe_not_equal: we,
  set_custom_element_data: Q,
  space: be,
  transition_in: S,
  transition_out: A,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: xe,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function M(e) {
  let n, t;
  const s = (
    /*#slots*/
    e[7].default
  ), o = _e(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = Y("svelte-slot"), o && o.c(), this.h();
    },
    l(r) {
      n = J(r, "SVELTE-SLOT", {
        class: !0
      });
      var l = K(n);
      o && o.l(l), l.forEach(y), this.h();
    },
    h() {
      Q(n, "class", "svelte-1rt0kpf");
    },
    m(r, l) {
      R(r, n, l), o && o.m(n, null), e[9](n), t = !0;
    },
    p(r, l) {
      o && o.p && (!t || l & /*$$scope*/
      64) && ye(
        o,
        s,
        r,
        /*$$scope*/
        r[6],
        t ? pe(
          s,
          /*$$scope*/
          r[6],
          l,
          null
        ) : me(
          /*$$scope*/
          r[6]
        ),
        null
      );
    },
    i(r) {
      t || (S(o, r), t = !0);
    },
    o(r) {
      A(o, r), t = !1;
    },
    d(r) {
      r && y(n), o && o.d(r), e[9](null);
    }
  };
}
function Ie(e) {
  let n, t, s, o, r = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      n = Y("react-portal-target"), t = be(), r && r.c(), s = W(), this.h();
    },
    l(l) {
      n = J(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(n).forEach(y), t = de(l), r && r.l(l), s = W(), this.h();
    },
    h() {
      Q(n, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      R(l, n, a), e[8](n), R(l, t, a), r && r.m(l, a), R(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? r ? (r.p(l, a), a & /*$$slots*/
      16 && S(r, 1)) : (r = M(l), r.c(), S(r, 1), r.m(s.parentNode, s)) : r && (he(), A(r, 1, 1, () => {
        r = null;
      }), ue());
    },
    i(l) {
      o || (S(r), o = !0);
    },
    o(l) {
      A(r), o = !1;
    },
    d(l) {
      l && (y(n), y(t), y(s)), e[8](null), r && r.d(l);
    }
  };
}
function B(e) {
  const {
    svelteInit: n,
    ...t
  } = e;
  return t;
}
function Re(e, n, t) {
  let s, o, {
    $$slots: r = {},
    $$scope: l
  } = n;
  const a = fe(r);
  let {
    svelteInit: i
  } = n;
  const h = I(B(n)), d = I();
  V(e, d, (u) => t(0, s = u));
  const f = I();
  V(e, f, (u) => t(1, o = u));
  const c = [], _ = xe("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: E
  } = ee() || {}, x = i({
    parent: _,
    props: h,
    target: d,
    slot: f,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: E,
    onDestroy(u) {
      c.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", x), Ee(() => {
    h.set(B(n));
  }), ve(() => {
    c.forEach((u) => u());
  });
  function v(u) {
    N[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function X(u) {
    N[u ? "unshift" : "push"](() => {
      o = u, f.set(o);
    });
  }
  return e.$$set = (u) => {
    t(17, n = T(T({}, n), D(u))), "svelteInit" in u && t(5, i = u.svelteInit), "$$scope" in u && t(6, l = u.$$scope);
  }, n = D(n), [s, o, d, f, a, i, l, r, v, X];
}
class Se extends ce {
  constructor(n) {
    super(), ge(this, n, Re, Ie, we, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, P = window.ms_globals.tree;
function Oe(e) {
  function n(t) {
    const s = I(), o = new Se({
      ...t,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? P;
          return a.nodes = [...a.nodes, l], U({
            createPortal: F,
            node: P
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), U({
              createPortal: F,
              node: P
            });
          }), l;
        },
        ...t.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((t) => {
    window.ms_globals.initializePromise.then(() => {
      t(n);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(e) {
  return e ? Object.keys(e).reduce((n, t) => {
    const s = e[t];
    return typeof s == "number" && !Pe.includes(t) ? n[t] = s + "px" : n[t] = s, n;
  }, {}) : {};
}
function L(e) {
  const n = [], t = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(F(g.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: g.Children.toArray(e._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: r,
            clonedElement: l
          } = L(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...g.Children.toArray(o.props.children), ...r]
          });
        }
        return null;
      })
    }), t)), {
      clonedElement: t,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      t.addEventListener(a, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const r = s[o];
    if (r.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = L(r);
      n.push(...a), t.appendChild(l);
    } else r.nodeType === 3 && t.appendChild(r.cloneNode());
  }
  return {
    clonedElement: t,
    portals: n
  };
}
function ke(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = Z(({
  slot: e,
  clone: n,
  className: t,
  style: s
}, o) => {
  const r = j(), [l, a] = q([]);
  return k(() => {
    var f;
    if (!r.current || !e)
      return;
    let i = e;
    function h() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ke(o, c), t && c.classList.add(...t.split(" ")), s) {
        const _ = je(s);
        Object.keys(_).forEach((m) => {
          c.style[m] = _[m];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var E, x, v;
        (E = r.current) != null && E.contains(i) && ((x = r.current) == null || x.removeChild(i));
        const {
          portals: m,
          clonedElement: w
        } = L(e);
        return i = w, a(m), i.style.display = "contents", h(), (v = r.current) == null || v.appendChild(i), m.length > 0;
      };
      c() || (d = new window.MutationObserver(() => {
        c() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (f = r.current) == null || f.appendChild(i);
    return () => {
      var c, _;
      i.style.display = "", (c = r.current) != null && c.contains(i) && ((_ = r.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, n, t, s, o]), g.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Fe(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ae(e, n = !1) {
  try {
    if (n && !Fe(e))
      return;
    if (typeof e == "string") {
      let t = e.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function C(e, n) {
  return z(() => Ae(e, n), [e, n]);
}
function Le({
  value: e,
  onValueChange: n
}) {
  const [t, s] = q(e), o = j(n);
  o.current = n;
  const r = j(t);
  return r.current = t, k(() => {
    o.current(t);
  }, [t]), k(() => {
    ne(e, r.current) || s(e);
  }, [e]), [t, s];
}
function Te(e) {
  return Object.keys(e).reduce((n, t) => (e[t] !== void 0 && (n[t] = e[t]), n), {});
}
function Ne(e, n) {
  return e ? /* @__PURE__ */ p.jsx(b, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Ve({
  key: e,
  setSlotParams: n,
  slots: t
}, s) {
  return t[e] ? (...o) => (n(e, o), Ne(t[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const De = Oe(({
  slots: e,
  children: n,
  count: t,
  showCount: s,
  onValueChange: o,
  onChange: r,
  setSlotParams: l,
  elRef: a,
  ...i
}) => {
  const h = C(t == null ? void 0 : t.strategy), d = C(t == null ? void 0 : t.exceedFormatter), f = C(t == null ? void 0 : t.show), c = C(typeof s == "object" ? s.formatter : void 0), [_, m] = Le({
    onValueChange: o,
    value: i.value
  });
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ p.jsx(te, {
      ...i,
      value: _,
      ref: a,
      onChange: (w) => {
        r == null || r(w), m(w.target.value);
      },
      showCount: e["showCount.formatter"] ? {
        formatter: Ve({
          slots: e,
          setSlotParams: l,
          key: "showCount.formatter"
        })
      } : typeof s == "object" && c ? {
        ...s,
        formatter: c
      } : s,
      count: z(() => Te({
        ...t,
        exceedFormatter: d,
        strategy: h,
        show: f || (t == null ? void 0 : t.show)
      }), [t, d, h, f]),
      addonAfter: e.addonAfter ? /* @__PURE__ */ p.jsx(b, {
        slot: e.addonAfter
      }) : i.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ p.jsx(b, {
        slot: e.addonBefore
      }) : i.addonBefore,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : i.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ p.jsx(b, {
        slot: e.prefix
      }) : i.prefix,
      suffix: e.suffix ? /* @__PURE__ */ p.jsx(b, {
        slot: e.suffix
      }) : i.suffix
    })]
  });
});
export {
  De as Input,
  De as default
};
