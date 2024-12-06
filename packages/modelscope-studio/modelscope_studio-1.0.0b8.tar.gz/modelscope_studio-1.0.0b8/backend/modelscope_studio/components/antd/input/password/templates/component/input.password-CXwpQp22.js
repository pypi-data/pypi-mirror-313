import { b as ee, g as te, w as C } from "./Index-vrCGYh2Y.js";
const g = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, j = window.ms_globals.React.useRef, z = window.ms_globals.React.useState, k = window.ms_globals.React.useEffect, G = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Input;
function re(e, n) {
  return ee(e, n);
}
var H = {
  exports: {}
}, P = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = g, se = Symbol.for("react.element"), le = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function K(e, n, t) {
  var s, o = {}, r = null, l = null;
  t !== void 0 && (r = "" + t), n.key !== void 0 && (r = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) ie.call(n, s) && !ce.hasOwnProperty(s) && (o[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: se,
    type: e,
    key: r,
    ref: l,
    props: o,
    _owner: ae.current
  };
}
P.Fragment = le;
P.jsx = K;
P.jsxs = K;
H.exports = P;
var h = H.exports;
const {
  SvelteComponent: de,
  assign: T,
  binding_callbacks: N,
  check_outros: ue,
  children: J,
  claim_element: Y,
  claim_space: fe,
  component_subscribe: V,
  compute_slots: _e,
  create_slot: me,
  detach: E,
  element: Q,
  empty: W,
  exclude_internal_props: D,
  get_all_dirty_from_scope: pe,
  get_slot_changes: he,
  group_outros: we,
  init: ge,
  insert_hydration: I,
  safe_not_equal: ye,
  set_custom_element_data: X,
  space: be,
  transition_in: S,
  transition_out: A,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: ve,
  onDestroy: Re,
  setContext: Ce
} = window.__gradio__svelte__internal;
function M(e) {
  let n, t;
  const s = (
    /*#slots*/
    e[7].default
  ), o = me(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = Q("svelte-slot"), o && o.c(), this.h();
    },
    l(r) {
      n = Y(r, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(n);
      o && o.l(l), l.forEach(E), this.h();
    },
    h() {
      X(n, "class", "svelte-1rt0kpf");
    },
    m(r, l) {
      I(r, n, l), o && o.m(n, null), e[9](n), t = !0;
    },
    p(r, l) {
      o && o.p && (!t || l & /*$$scope*/
      64) && Ee(
        o,
        s,
        r,
        /*$$scope*/
        r[6],
        t ? he(
          s,
          /*$$scope*/
          r[6],
          l,
          null
        ) : pe(
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
      r && E(n), o && o.d(r), e[9](null);
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
      n = Q("react-portal-target"), t = be(), r && r.c(), s = W(), this.h();
    },
    l(l) {
      n = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(n).forEach(E), t = fe(l), r && r.l(l), s = W(), this.h();
    },
    h() {
      X(n, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      I(l, n, a), e[8](n), I(l, t, a), r && r.m(l, a), I(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? r ? (r.p(l, a), a & /*$$slots*/
      16 && S(r, 1)) : (r = M(l), r.c(), S(r, 1), r.m(s.parentNode, s)) : r && (we(), A(r, 1, 1, () => {
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
      l && (E(n), E(t), E(s)), e[8](null), r && r.d(l);
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
function Se(e, n, t) {
  let s, o, {
    $$slots: r = {},
    $$scope: l
  } = n;
  const a = _e(r);
  let {
    svelteInit: i
  } = n;
  const f = C(B(n)), u = C();
  V(e, u, (d) => t(0, s = d));
  const m = C();
  V(e, m, (d) => t(1, o = d));
  const c = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: x,
    subSlotIndex: y
  } = te() || {}, w = i({
    parent: _,
    props: f,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: x,
    subSlotIndex: y,
    onDestroy(d) {
      c.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", w), xe(() => {
    f.set(B(n));
  }), Re(() => {
    c.forEach((d) => d());
  });
  function R(d) {
    N[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function Z(d) {
    N[d ? "unshift" : "push"](() => {
      o = d, m.set(o);
    });
  }
  return e.$$set = (d) => {
    t(17, n = T(T({}, n), D(d))), "svelteInit" in d && t(5, i = d.svelteInit), "$$scope" in d && t(6, l = d.$$scope);
  }, n = D(n), [s, o, u, m, a, i, l, r, R, Z];
}
class Pe extends de {
  constructor(n) {
    super(), ge(this, n, Se, Ie, ye, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, O = window.ms_globals.tree;
function Oe(e) {
  function n(t) {
    const s = C(), o = new Pe({
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
          }, a = r.parent ?? O;
          return a.nodes = [...a.nodes, l], U({
            createPortal: F,
            node: O
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), U({
              createPortal: F,
              node: O
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
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(e) {
  return e ? Object.keys(e).reduce((n, t) => {
    const s = e[t];
    return typeof s == "number" && !je.includes(t) ? n[t] = s + "px" : n[t] = s, n;
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
function Fe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = $(({
  slot: e,
  clone: n,
  className: t,
  style: s
}, o) => {
  const r = j(), [l, a] = z([]);
  return k(() => {
    var m;
    if (!r.current || !e)
      return;
    let i = e;
    function f() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Fe(o, c), t && c.classList.add(...t.split(" ")), s) {
        const _ = ke(s);
        Object.keys(_).forEach((p) => {
          c.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var y, w, R;
        (y = r.current) != null && y.contains(i) && ((w = r.current) == null || w.removeChild(i));
        const {
          portals: p,
          clonedElement: x
        } = L(e);
        return i = x, a(p), i.style.display = "contents", f(), (R = r.current) == null || R.appendChild(i), p.length > 0;
      };
      c() || (u = new window.MutationObserver(() => {
        c() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", f(), (m = r.current) == null || m.appendChild(i);
    return () => {
      var c, _;
      i.style.display = "", (c = r.current) != null && c.contains(i) && ((_ = r.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, n, t, s, o]), g.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Le(e, n = !1) {
  try {
    if (n && !Ae(e))
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
function v(e, n) {
  return G(() => Le(e, n), [e, n]);
}
function Te({
  value: e,
  onValueChange: n
}) {
  const [t, s] = z(e), o = j(n);
  o.current = n;
  const r = j(t);
  return r.current = t, k(() => {
    o.current(t);
  }, [t]), k(() => {
    re(e, r.current) || s(e);
  }, [e]), [t, s];
}
function Ne(e) {
  return Object.keys(e).reduce((n, t) => (e[t] !== void 0 && (n[t] = e[t]), n), {});
}
function Ve(e, n) {
  return e ? /* @__PURE__ */ h.jsx(b, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function q({
  key: e,
  setSlotParams: n,
  slots: t
}, s) {
  return t[e] ? (...o) => (n(e, o), Ve(t[e], {
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
  iconRender: l,
  elRef: a,
  setSlotParams: i,
  ...f
}) => {
  const u = v(t == null ? void 0 : t.strategy), m = v(t == null ? void 0 : t.exceedFormatter), c = v(t == null ? void 0 : t.show), _ = v(typeof s == "object" ? s.formatter : void 0), p = v(l), [x, y] = Te({
    onValueChange: o,
    value: f.value
  });
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ h.jsx(ne.Password, {
      ...f,
      value: x,
      ref: a,
      onChange: (w) => {
        r == null || r(w), y(w.target.value);
      },
      iconRender: e.iconRender ? q({
        slots: e,
        setSlotParams: i,
        key: "iconRender"
      }) : p,
      showCount: e["showCount.formatter"] ? {
        formatter: q({
          slots: e,
          setSlotParams: i,
          key: "showCount.formatter"
        })
      } : typeof s == "object" && _ ? {
        ...s,
        formatter: _
      } : s,
      count: G(() => Ne({
        ...t,
        exceedFormatter: m,
        strategy: u,
        show: c || (t == null ? void 0 : t.show)
      }), [t, m, u, c]),
      addonAfter: e.addonAfter ? /* @__PURE__ */ h.jsx(b, {
        slot: e.addonAfter
      }) : f.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ h.jsx(b, {
        slot: e.addonBefore
      }) : f.addonBefore,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : f.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ h.jsx(b, {
        slot: e.prefix
      }) : f.prefix,
      suffix: e.suffix ? /* @__PURE__ */ h.jsx(b, {
        slot: e.suffix
      }) : f.suffix
    })]
  });
});
export {
  De as InputPassword,
  De as default
};
