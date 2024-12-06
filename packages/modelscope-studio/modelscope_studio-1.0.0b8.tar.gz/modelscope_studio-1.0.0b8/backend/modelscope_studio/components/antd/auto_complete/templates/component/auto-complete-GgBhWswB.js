import { b as ee, g as te, w as x } from "./Index-C6wsF4KY.js";
const y = window.ms_globals.React, U = window.ms_globals.React.forwardRef, P = window.ms_globals.React.useRef, H = window.ms_globals.React.useState, j = window.ms_globals.React.useEffect, T = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.internalContext.AutoCompleteContext, re = window.ms_globals.antd.AutoComplete;
function le(t, e) {
  return ee(t, e);
}
var B = {
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
var oe = y, se = Symbol.for("react.element"), ce = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function J(t, e, l) {
  var o, r = {}, n = null, s = null;
  l !== void 0 && (n = "" + l), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) ie.call(e, o) && !ue.hasOwnProperty(o) && (r[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) r[o] === void 0 && (r[o] = e[o]);
  return {
    $$typeof: se,
    type: t,
    key: n,
    ref: s,
    props: r,
    _owner: ae.current
  };
}
S.Fragment = ce;
S.jsx = J;
S.jsxs = J;
B.exports = S;
var h = B.exports;
const {
  SvelteComponent: de,
  assign: N,
  binding_callbacks: W,
  check_outros: fe,
  children: Y,
  claim_element: K,
  claim_space: _e,
  component_subscribe: V,
  compute_slots: pe,
  create_slot: he,
  detach: E,
  element: Q,
  empty: D,
  exclude_internal_props: M,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: R,
  safe_not_equal: ye,
  set_custom_element_data: X,
  space: Ce,
  transition_in: I,
  transition_out: A,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: xe,
  onDestroy: Re,
  setContext: Ie
} = window.__gradio__svelte__internal;
function q(t) {
  let e, l;
  const o = (
    /*#slots*/
    t[7].default
  ), r = he(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Q("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      e = K(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(e);
      r && r.l(s), s.forEach(E), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      R(n, e, s), r && r.m(e, null), t[9](e), l = !0;
    },
    p(n, s) {
      r && r.p && (!l || s & /*$$scope*/
      64) && Ee(
        r,
        o,
        n,
        /*$$scope*/
        n[6],
        l ? ge(
          o,
          /*$$scope*/
          n[6],
          s,
          null
        ) : me(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (I(r, n), l = !0);
    },
    o(n) {
      A(r, n), l = !1;
    },
    d(n) {
      n && E(e), r && r.d(n), t[9](null);
    }
  };
}
function Se(t) {
  let e, l, o, r, n = (
    /*$$slots*/
    t[4].default && q(t)
  );
  return {
    c() {
      e = Q("react-portal-target"), l = Ce(), n && n.c(), o = D(), this.h();
    },
    l(s) {
      e = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(e).forEach(E), l = _e(s), n && n.l(s), o = D(), this.h();
    },
    h() {
      X(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      R(s, e, c), t[8](e), R(s, l, c), n && n.m(s, c), R(s, o, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && I(n, 1)) : (n = q(s), n.c(), I(n, 1), n.m(o.parentNode, o)) : n && (we(), A(n, 1, 1, () => {
        n = null;
      }), fe());
    },
    i(s) {
      r || (I(n), r = !0);
    },
    o(s) {
      A(n), r = !1;
    },
    d(s) {
      s && (E(e), E(l), E(o)), t[8](null), n && n.d(s);
    }
  };
}
function z(t) {
  const {
    svelteInit: e,
    ...l
  } = t;
  return l;
}
function Oe(t, e, l) {
  let o, r, {
    $$slots: n = {},
    $$scope: s
  } = e;
  const c = pe(n);
  let {
    svelteInit: i
  } = e;
  const g = x(z(e)), u = x();
  V(t, u, (f) => l(0, o = f));
  const d = x();
  V(t, d, (f) => l(1, r = f));
  const a = [], _ = xe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: w,
    subSlotIndex: m
  } = te() || {}, b = i({
    parent: _,
    props: g,
    target: u,
    slot: d,
    slotKey: p,
    slotIndex: w,
    subSlotIndex: m,
    onDestroy(f) {
      a.push(f);
    }
  });
  Ie("$$ms-gr-react-wrapper", b), ve(() => {
    g.set(z(e));
  }), Re(() => {
    a.forEach((f) => f());
  });
  function C(f) {
    W[f ? "unshift" : "push"](() => {
      o = f, u.set(o);
    });
  }
  function $(f) {
    W[f ? "unshift" : "push"](() => {
      r = f, d.set(r);
    });
  }
  return t.$$set = (f) => {
    l(17, e = N(N({}, e), M(f))), "svelteInit" in f && l(5, i = f.svelteInit), "$$scope" in f && l(6, s = f.$$scope);
  }, e = M(e), [o, r, u, d, c, i, s, n, C, $];
}
class ke extends de {
  constructor(e) {
    super(), be(this, e, Oe, Se, ye, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, O = window.ms_globals.tree;
function Pe(t) {
  function e(l) {
    const o = x(), r = new ke({
      ...l,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? O;
          return c.nodes = [...c.nodes, s], G({
            createPortal: F,
            node: O
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), G({
              createPortal: F,
              node: O
            });
          }), s;
        },
        ...l.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(e);
    });
  });
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(t) {
  return t ? Object.keys(t).reduce((e, l) => {
    const o = t[l];
    return typeof o == "number" && !je.includes(l) ? e[l] = o + "px" : e[l] = o, e;
  }, {}) : {};
}
function L(t) {
  const e = [], l = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(F(y.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: y.Children.toArray(t._reactElement.props.children).map((r) => {
        if (y.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = L(r.props.el);
          return y.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...y.Children.toArray(r.props.children), ...n]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      l.addEventListener(c, s, i);
    });
  });
  const o = Array.from(t.childNodes);
  for (let r = 0; r < o.length; r++) {
    const n = o[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = L(n);
      e.push(...c), l.appendChild(s);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function Ae(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const v = U(({
  slot: t,
  clone: e,
  className: l,
  style: o
}, r) => {
  const n = P(), [s, c] = H([]);
  return j(() => {
    var d;
    if (!n.current || !t)
      return;
    let i = t;
    function g() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ae(r, a), l && a.classList.add(...l.split(" ")), o) {
        const _ = Fe(o);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var m, b, C;
        (m = n.current) != null && m.contains(i) && ((b = n.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: w
        } = L(t);
        return i = w, c(p), i.style.display = "contents", g(), (C = n.current) == null || C.appendChild(i), p.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (d = n.current) == null || d.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((_ = n.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [t, e, l, o, r]), y.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Te(t, e = !1) {
  try {
    if (e && !Le(t))
      return;
    if (typeof t == "string") {
      let l = t.trim();
      return l.startsWith(";") && (l = l.slice(1)), l.endsWith(";") && (l = l.slice(0, -1)), new Function(`return (...args) => (${l})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function k(t, e) {
  return T(() => Te(t, e), [t, e]);
}
function Ne({
  value: t,
  onValueChange: e
}) {
  const [l, o] = H(t), r = P(e);
  r.current = e;
  const n = P(l);
  return n.current = l, j(() => {
    r.current(l);
  }, [l]), j(() => {
    le(t, n.current) || o(t);
  }, [t]), [l, o];
}
function Z(t, e, l) {
  const o = t.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, n) => {
      var g;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const s = {
        ...r.props,
        key: ((g = r.props) == null ? void 0 : g.key) ?? (l ? `${l}-${n}` : `${n}`)
      };
      let c = s;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const d = u.split(".");
        d.forEach((m, b) => {
          c[m] || (c[m] = {}), b !== d.length - 1 && (c = s[m]);
        });
        const a = r.slots[u];
        let _, p, w = (e == null ? void 0 : e.clone) ?? !1;
        a instanceof Element ? _ = a : (_ = a.el, p = a.callback, w = a.clone ?? w), c[d[d.length - 1]] = _ ? p ? (...m) => (p(d[d.length - 1], m), /* @__PURE__ */ h.jsx(v, {
          slot: _,
          clone: w
        })) : /* @__PURE__ */ h.jsx(v, {
          slot: _,
          clone: w
        }) : c[d[d.length - 1]], c = s;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return r[i] && (s[i] = Z(r[i], e, `${n}`)), s;
    });
}
function We(t, e) {
  return t ? /* @__PURE__ */ h.jsx(v, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Ve({
  key: t,
  setSlotParams: e,
  slots: l
}, o) {
  return l[t] ? (...r) => (e(t, r), We(l[t], {
    clone: !0,
    ...o
  })) : void 0;
}
const De = U(({
  children: t,
  ...e
}, l) => /* @__PURE__ */ h.jsx(ne.Provider, {
  value: T(() => ({
    ...e,
    elRef: l
  }), [e, l]),
  children: t
})), qe = Pe(({
  slots: t,
  children: e,
  onValueChange: l,
  filterOption: o,
  onChange: r,
  options: n,
  optionItems: s,
  getPopupContainer: c,
  dropdownRender: i,
  elRef: g,
  setSlotParams: u,
  ...d
}) => {
  const a = k(c), _ = k(o), p = k(i), [w, m] = Ne({
    onValueChange: l,
    value: d.value
  });
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [t.children ? null : /* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ h.jsx(re, {
      ...d,
      value: w,
      ref: g,
      allowClear: t["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(v, {
          slot: t["allowClear.clearIcon"]
        })
      } : d.allowClear,
      options: T(() => n || Z(s, {
        children: "options",
        clone: !0
      }), [s, n]),
      onChange: (b, ...C) => {
        r == null || r(b, ...C), m(b);
      },
      notFoundContent: t.notFoundContent ? /* @__PURE__ */ h.jsx(v, {
        slot: t.notFoundContent
      }) : d.notFoundContent,
      filterOption: _ || o,
      getPopupContainer: a,
      dropdownRender: t.dropdownRender ? Ve({
        slots: t,
        setSlotParams: u,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : p,
      children: t.children ? /* @__PURE__ */ h.jsxs(De, {
        children: [/* @__PURE__ */ h.jsx("div", {
          style: {
            display: "none"
          },
          children: e
        }), /* @__PURE__ */ h.jsx(v, {
          slot: t.children
        })]
      }) : null
    })]
  });
});
export {
  qe as AutoComplete,
  qe as default
};
