import { b as $, g as ee, w as C } from "./Index-DD6FD9vS.js";
const h = window.ms_globals.React, Z = window.ms_globals.React.forwardRef, P = window.ms_globals.React.useRef, q = window.ms_globals.React.useState, k = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Input;
function re(e, r) {
  return $(e, r);
}
var G = {
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
var ne = h, oe = Symbol.for("react.element"), se = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, ie = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(e, r, t) {
  var s, o = {}, n = null, l = null;
  t !== void 0 && (n = "" + t), r.key !== void 0 && (n = "" + r.key), r.ref !== void 0 && (l = r.ref);
  for (s in r) le.call(r, s) && !ae.hasOwnProperty(s) && (o[s] = r[s]);
  if (e && e.defaultProps) for (s in r = e.defaultProps, r) o[s] === void 0 && (o[s] = r[s]);
  return {
    $$typeof: oe,
    type: e,
    key: n,
    ref: l,
    props: o,
    _owner: ie.current
  };
}
S.Fragment = se;
S.jsx = H;
S.jsxs = H;
G.exports = S;
var w = G.exports;
const {
  SvelteComponent: ce,
  assign: T,
  binding_callbacks: A,
  check_outros: ue,
  children: K,
  claim_element: B,
  claim_space: de,
  component_subscribe: N,
  compute_slots: fe,
  create_slot: _e,
  detach: b,
  element: J,
  empty: V,
  exclude_internal_props: W,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: ge,
  insert_hydration: I,
  safe_not_equal: we,
  set_custom_element_data: Y,
  space: be,
  transition_in: R,
  transition_out: j,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Ce
} = window.__gradio__svelte__internal;
function D(e) {
  let r, t;
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
      r = J("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      r = B(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = K(r);
      o && o.l(l), l.forEach(b), this.h();
    },
    h() {
      Y(r, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      I(n, r, l), o && o.m(r, null), e[9](r), t = !0;
    },
    p(n, l) {
      o && o.p && (!t || l & /*$$scope*/
      64) && ye(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        t ? pe(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : me(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      t || (R(o, n), t = !0);
    },
    o(n) {
      j(o, n), t = !1;
    },
    d(n) {
      n && b(r), o && o.d(n), e[9](null);
    }
  };
}
function Ie(e) {
  let r, t, s, o, n = (
    /*$$slots*/
    e[4].default && D(e)
  );
  return {
    c() {
      r = J("react-portal-target"), t = be(), n && n.c(), s = V(), this.h();
    },
    l(l) {
      r = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(r).forEach(b), t = de(l), n && n.l(l), s = V(), this.h();
    },
    h() {
      Y(r, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      I(l, r, a), e[8](r), I(l, t, a), n && n.m(l, a), I(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, a), a & /*$$slots*/
      16 && R(n, 1)) : (n = D(l), n.c(), R(n, 1), n.m(s.parentNode, s)) : n && (he(), j(n, 1, 1, () => {
        n = null;
      }), ue());
    },
    i(l) {
      o || (R(n), o = !0);
    },
    o(l) {
      j(n), o = !1;
    },
    d(l) {
      l && (b(r), b(t), b(s)), e[8](null), n && n.d(l);
    }
  };
}
function M(e) {
  const {
    svelteInit: r,
    ...t
  } = e;
  return t;
}
function Re(e, r, t) {
  let s, o, {
    $$slots: n = {},
    $$scope: l
  } = r;
  const a = fe(n);
  let {
    svelteInit: i
  } = r;
  const p = C(M(r)), d = C();
  N(e, d, (u) => t(0, s = u));
  const f = C();
  N(e, f, (u) => t(1, o = u));
  const c = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: y
  } = ee() || {}, E = i({
    parent: _,
    props: p,
    target: d,
    slot: f,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: y,
    onDestroy(u) {
      c.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", E), Ee(() => {
    p.set(M(r));
  }), xe(() => {
    c.forEach((u) => u());
  });
  function v(u) {
    A[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function X(u) {
    A[u ? "unshift" : "push"](() => {
      o = u, f.set(o);
    });
  }
  return e.$$set = (u) => {
    t(17, r = T(T({}, r), W(u))), "svelteInit" in u && t(5, i = u.svelteInit), "$$scope" in u && t(6, l = u.$$scope);
  }, r = W(r), [s, o, d, f, a, i, l, n, v, X];
}
class Se extends ce {
  constructor(r) {
    super(), ge(this, r, Re, Ie, we, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, O = window.ms_globals.tree;
function Oe(e) {
  function r(t) {
    const s = C(), o = new Se({
      ...t,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, a = n.parent ?? O;
          return a.nodes = [...a.nodes, l], U({
            createPortal: F,
            node: O
          }), n.onDestroy(() => {
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
      t(r);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(e) {
  return e ? Object.keys(e).reduce((r, t) => {
    const s = e[t];
    return typeof s == "number" && !Pe.includes(t) ? r[t] = s + "px" : r[t] = s, r;
  }, {}) : {};
}
function L(e) {
  const r = [], t = e.cloneNode(!1);
  if (e._reactElement)
    return r.push(F(h.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: h.Children.toArray(e._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = L(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), t)), {
      clonedElement: t,
      portals: r
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
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = L(n);
      r.push(...a), t.appendChild(l);
    } else n.nodeType === 3 && t.appendChild(n.cloneNode());
  }
  return {
    clonedElement: t,
    portals: r
  };
}
function Fe(e, r) {
  e && (typeof e == "function" ? e(r) : e.current = r);
}
const Q = Z(({
  slot: e,
  clone: r,
  className: t,
  style: s
}, o) => {
  const n = P(), [l, a] = q([]);
  return k(() => {
    var f;
    if (!n.current || !e)
      return;
    let i = e;
    function p() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Fe(o, c), t && c.classList.add(...t.split(" ")), s) {
        const _ = ke(s);
        Object.keys(_).forEach((m) => {
          c.style[m] = _[m];
        });
      }
    }
    let d = null;
    if (r && window.MutationObserver) {
      let c = function() {
        var y, E, v;
        (y = n.current) != null && y.contains(i) && ((E = n.current) == null || E.removeChild(i));
        const {
          portals: m,
          clonedElement: g
        } = L(e);
        return i = g, a(m), i.style.display = "contents", p(), (v = n.current) == null || v.appendChild(i), m.length > 0;
      };
      c() || (d = new window.MutationObserver(() => {
        c() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (f = n.current) == null || f.appendChild(i);
    return () => {
      var c, _;
      i.style.display = "", (c = n.current) != null && c.contains(i) && ((_ = n.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, r, t, s, o]), h.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Le(e, r = !1) {
  try {
    if (r && !je(e))
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
function x(e, r) {
  return z(() => Le(e, r), [e, r]);
}
function Te({
  value: e,
  onValueChange: r
}) {
  const [t, s] = q(e), o = P(r);
  o.current = r;
  const n = P(t);
  return n.current = t, k(() => {
    o.current(t);
  }, [t]), k(() => {
    re(e, n.current) || s(e);
  }, [e]), [t, s];
}
function Ae(e) {
  return Object.keys(e).reduce((r, t) => (e[t] !== void 0 && (r[t] = e[t]), r), {});
}
function Ne(e, r) {
  return e ? /* @__PURE__ */ w.jsx(Q, {
    slot: e,
    clone: r == null ? void 0 : r.clone
  }) : null;
}
function Ve({
  key: e,
  setSlotParams: r,
  slots: t
}, s) {
  return t[e] ? (...o) => (r(e, o), Ne(t[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const De = Oe(({
  slots: e,
  children: r,
  count: t,
  showCount: s,
  onValueChange: o,
  onChange: n,
  elRef: l,
  setSlotParams: a,
  ...i
}) => {
  const p = x(t == null ? void 0 : t.strategy), d = x(t == null ? void 0 : t.exceedFormatter), f = x(t == null ? void 0 : t.show), c = x(typeof s == "object" ? s.formatter : void 0), [_, m] = Te({
    onValueChange: o,
    value: i.value
  });
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ w.jsx(te.TextArea, {
      ...i,
      ref: l,
      value: _,
      onChange: (g) => {
        n == null || n(g), m(g.target.value);
      },
      showCount: e["showCount.formatter"] ? {
        formatter: Ve({
          slots: e,
          setSlotParams: a,
          key: "showCount.formatter"
        })
      } : typeof s == "object" && c ? {
        ...s,
        formatter: c
      } : s,
      count: z(() => Ae({
        ...t,
        exceedFormatter: d,
        strategy: p,
        show: f || (t == null ? void 0 : t.show)
      }), [t, d, p, f]),
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ w.jsx(Q, {
          slot: e["allowClear.clearIcon"]
        })
      } : i.allowClear
    })]
  });
});
export {
  De as InputTextarea,
  De as default
};
