import { b as $, g as ee, w as v } from "./Index-C1-zmsAv.js";
const w = window.ms_globals.React, X = window.ms_globals.React.forwardRef, P = window.ms_globals.React.useRef, z = window.ms_globals.React.useState, j = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.InputNumber;
function ne(e, n) {
  return $(e, n);
}
var G = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = w, re = Symbol.for("react.element"), se = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, ie = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(e, n, o) {
  var s, r = {}, t = null, l = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) le.call(n, s) && !ce.hasOwnProperty(s) && (r[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: re,
    type: e,
    key: t,
    ref: l,
    props: r,
    _owner: ie.current
  };
}
C.Fragment = se;
C.jsx = U;
C.jsxs = U;
G.exports = C;
var f = G.exports;
const {
  SvelteComponent: ae,
  assign: N,
  binding_callbacks: F,
  check_outros: ue,
  children: H,
  claim_element: K,
  claim_space: de,
  component_subscribe: T,
  compute_slots: fe,
  create_slot: _e,
  detach: b,
  element: J,
  empty: V,
  exclude_internal_props: W,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: we,
  insert_hydration: I,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: be,
  transition_in: R,
  transition_out: A,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: xe,
  onDestroy: ve,
  setContext: Ie
} = window.__gradio__svelte__internal;
function D(e) {
  let n, o;
  const s = (
    /*#slots*/
    e[7].default
  ), r = _e(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = J("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(n);
      r && r.l(l), l.forEach(b), this.h();
    },
    h() {
      Y(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      I(t, n, l), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ye(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        o ? pe(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : me(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (R(r, t), o = !0);
    },
    o(t) {
      A(r, t), o = !1;
    },
    d(t) {
      t && b(n), r && r.d(t), e[9](null);
    }
  };
}
function Re(e) {
  let n, o, s, r, t = (
    /*$$slots*/
    e[4].default && D(e)
  );
  return {
    c() {
      n = J("react-portal-target"), o = be(), t && t.c(), s = V(), this.h();
    },
    l(l) {
      n = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(b), o = de(l), t && t.l(l), s = V(), this.h();
    },
    h() {
      Y(n, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      I(l, n, i), e[8](n), I(l, o, i), t && t.m(l, i), I(l, s, i), r = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, i), i & /*$$slots*/
      16 && R(t, 1)) : (t = D(l), t.c(), R(t, 1), t.m(s.parentNode, s)) : t && (he(), A(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(l) {
      r || (R(t), r = !0);
    },
    o(l) {
      A(t), r = !1;
    },
    d(l) {
      l && (b(n), b(o), b(s)), e[8](null), t && t.d(l);
    }
  };
}
function M(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function Ce(e, n, o) {
  let s, r, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const i = fe(t);
  let {
    svelteInit: c
  } = n;
  const h = v(M(n)), d = v();
  T(e, d, (u) => o(0, s = u));
  const _ = v();
  T(e, _, (u) => o(1, r = u));
  const a = [], m = xe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: S,
    subSlotIndex: y
  } = ee() || {}, E = c({
    parent: m,
    props: h,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ie("$$ms-gr-react-wrapper", E), Ee(() => {
    h.set(M(n));
  }), ve(() => {
    a.forEach((u) => u());
  });
  function x(u) {
    F[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function Q(u) {
    F[u ? "unshift" : "push"](() => {
      r = u, _.set(r);
    });
  }
  return e.$$set = (u) => {
    o(17, n = N(N({}, n), W(u))), "svelteInit" in u && o(5, c = u.svelteInit), "$$scope" in u && o(6, l = u.$$scope);
  }, n = W(n), [s, r, d, _, i, c, l, t, x, Q];
}
class Se extends ae {
  constructor(n) {
    super(), we(this, n, Ce, Re, ge, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, O = window.ms_globals.tree;
function Oe(e) {
  function n(o) {
    const s = v(), r = new Se({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? O;
          return i.nodes = [...i.nodes, l], B({
            createPortal: k,
            node: O
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), B({
              createPortal: k,
              node: O
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
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const s = e[o];
    return typeof s == "number" && !Pe.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function L(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(k(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = L(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...w.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, l, c);
    });
  });
  const s = Array.from(e.childNodes);
  for (let r = 0; r < s.length; r++) {
    const t = s[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = L(t);
      n.push(...i), o.appendChild(l);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function ke(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const g = X(({
  slot: e,
  clone: n,
  className: o,
  style: s
}, r) => {
  const t = P(), [l, i] = z([]);
  return j(() => {
    var _;
    if (!t.current || !e)
      return;
    let c = e;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(r, a), o && a.classList.add(...o.split(" ")), s) {
        const m = je(s);
        Object.keys(m).forEach((p) => {
          a.style[p] = m[p];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y, E, x;
        (y = t.current) != null && y.contains(c) && ((E = t.current) == null || E.removeChild(c));
        const {
          portals: p,
          clonedElement: S
        } = L(e);
        return c = S, i(p), c.style.display = "contents", h(), (x = t.current) == null || x.appendChild(c), p.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (_ = t.current) == null || _.appendChild(c);
    return () => {
      var a, m;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((m = t.current) == null || m.removeChild(c)), d == null || d.disconnect();
    };
  }, [e, n, o, s, r]), w.createElement("react-child", {
    ref: t,
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
      let o = e.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function q(e, n) {
  return Z(() => Le(e, n), [e, n]);
}
function Ne({
  value: e,
  onValueChange: n
}) {
  const [o, s] = z(e), r = P(n);
  r.current = n;
  const t = P(o);
  return t.current = o, j(() => {
    r.current(o);
  }, [o]), j(() => {
    ne(e, t.current) || s(e);
  }, [e]), [o, s];
}
const Te = Oe(({
  slots: e,
  children: n,
  onValueChange: o,
  onChange: s,
  formatter: r,
  parser: t,
  elRef: l,
  ...i
}) => {
  const c = q(r), h = q(t), [d, _] = Ne({
    onValueChange: o,
    value: i.value
  });
  return /* @__PURE__ */ f.jsxs(f.Fragment, {
    children: [/* @__PURE__ */ f.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ f.jsx(te, {
      ...i,
      ref: l,
      value: d,
      onChange: (a) => {
        s == null || s(a), _(a);
      },
      parser: h,
      formatter: c,
      controls: e["controls.upIcon"] || e["controls.downIcon"] ? {
        upIcon: e["controls.upIcon"] ? /* @__PURE__ */ f.jsx(g, {
          slot: e["controls.upIcon"]
        }) : typeof i.controls == "object" ? i.controls.upIcon : void 0,
        downIcon: e["controls.downIcon"] ? /* @__PURE__ */ f.jsx(g, {
          slot: e["controls.downIcon"]
        }) : typeof i.controls == "object" ? i.controls.downIcon : void 0
      } : i.controls,
      addonAfter: e.addonAfter ? /* @__PURE__ */ f.jsx(g, {
        slot: e.addonAfter
      }) : i.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ f.jsx(g, {
        slot: e.addonBefore
      }) : i.addonBefore,
      prefix: e.prefix ? /* @__PURE__ */ f.jsx(g, {
        slot: e.prefix
      }) : i.prefix,
      suffix: e.suffix ? /* @__PURE__ */ f.jsx(g, {
        slot: e.suffix
      }) : i.suffix
    })]
  });
});
export {
  Te as InputNumber,
  Te as default
};
