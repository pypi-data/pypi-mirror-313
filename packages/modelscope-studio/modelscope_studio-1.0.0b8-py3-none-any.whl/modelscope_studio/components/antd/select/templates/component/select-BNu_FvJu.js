import { g as le, w as C } from "./Index-hc9MuAsH.js";
const E = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, se = window.ms_globals.antd.Select;
var B = {
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
var ce = E, ie = Symbol.for("react.element"), ae = Symbol.for("react.fragment"), ue = Object.prototype.hasOwnProperty, de = ce.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, fe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, o) {
  var s, r = {}, n = null, l = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ue.call(t, s) && !fe.hasOwnProperty(s) && (r[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ie,
    type: e,
    key: n,
    ref: l,
    props: r,
    _owner: de.current
  };
}
O.Fragment = ae;
O.jsx = V;
O.jsxs = V;
B.exports = O;
var p = B.exports;
const {
  SvelteComponent: _e,
  assign: A,
  binding_callbacks: W,
  check_outros: me,
  children: J,
  claim_element: Y,
  claim_space: he,
  component_subscribe: D,
  compute_slots: pe,
  create_slot: ge,
  detach: I,
  element: K,
  empty: M,
  exclude_internal_props: z,
  get_all_dirty_from_scope: we,
  get_slot_changes: be,
  group_outros: ye,
  init: xe,
  insert_hydration: S,
  safe_not_equal: Ee,
  set_custom_element_data: Q,
  space: Re,
  transition_in: k,
  transition_out: T,
  update_slot_base: Ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ce,
  onDestroy: Se,
  setContext: ke
} = window.__gradio__svelte__internal;
function G(e) {
  let t, o;
  const s = (
    /*#slots*/
    e[7].default
  ), r = ge(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(t);
      r && r.l(l), l.forEach(I), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      S(n, t, l), r && r.m(t, null), e[9](t), o = !0;
    },
    p(n, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && Ie(
        r,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? be(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : we(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (k(r, n), o = !0);
    },
    o(n) {
      T(r, n), o = !1;
    },
    d(n) {
      n && I(t), r && r.d(n), e[9](null);
    }
  };
}
function Oe(e) {
  let t, o, s, r, n = (
    /*$$slots*/
    e[4].default && G(e)
  );
  return {
    c() {
      t = K("react-portal-target"), o = Re(), n && n.c(), s = M(), this.h();
    },
    l(l) {
      t = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(I), o = he(l), n && n.l(l), s = M(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      S(l, t, c), e[8](t), S(l, o, c), n && n.m(l, c), S(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && k(n, 1)) : (n = G(l), n.c(), k(n, 1), n.m(s.parentNode, s)) : n && (ye(), T(n, 1, 1, () => {
        n = null;
      }), me());
    },
    i(l) {
      r || (k(n), r = !0);
    },
    o(l) {
      T(n), r = !1;
    },
    d(l) {
      l && (I(t), I(o), I(s)), e[8](null), n && n.d(l);
    }
  };
}
function U(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function je(e, t, o) {
  let s, r, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const c = pe(n);
  let {
    svelteInit: i
  } = t;
  const w = C(U(t)), u = C();
  D(e, u, (d) => o(0, s = d));
  const f = C();
  D(e, f, (d) => o(1, r = d));
  const a = [], h = Ce("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: m,
    subSlotIndex: g
  } = le() || {}, y = i({
    parent: h,
    props: w,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: m,
    subSlotIndex: g,
    onDestroy(d) {
      a.push(d);
    }
  });
  ke("$$ms-gr-react-wrapper", y), ve(() => {
    w.set(U(t));
  }), Se(() => {
    a.forEach((d) => d());
  });
  function R(d) {
    W[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function j(d) {
    W[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return e.$$set = (d) => {
    o(17, t = A(A({}, t), z(d))), "svelteInit" in d && o(5, i = d.svelteInit), "$$scope" in d && o(6, l = d.$$scope);
  }, t = z(t), [s, r, u, f, c, i, l, n, R, j];
}
class Pe extends _e {
  constructor(t) {
    super(), xe(this, t, je, Oe, Ee, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, P = window.ms_globals.tree;
function Fe(e) {
  function t(o) {
    const s = C(), r = new Pe({
      ...o,
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
          }, c = n.parent ?? P;
          return c.nodes = [...c.nodes, l], H({
            createPortal: F,
            node: P
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), H({
              createPortal: F,
              node: P
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
      o(t);
    });
  });
}
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const s = e[o];
    return typeof s == "number" && !Te.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function L(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(F(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((r) => {
        if (E.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = L(r.props.el);
          return E.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...E.Children.toArray(r.props.children), ...n]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let r = 0; r < s.length; r++) {
    const n = s[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = L(n);
      t.push(...c), o.appendChild(l);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Ne(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const b = te(({
  slot: e,
  clone: t,
  className: o,
  style: s
}, r) => {
  const n = ne(), [l, c] = re([]);
  return oe(() => {
    var f;
    if (!n.current || !e)
      return;
    let i = e;
    function w() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ne(r, a), o && a.classList.add(...o.split(" ")), s) {
        const h = Le(s);
        Object.keys(h).forEach((_) => {
          a.style[_] = h[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var g, y, R;
        (g = n.current) != null && g.contains(i) && ((y = n.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: m
        } = L(e);
        return i = m, c(_), i.style.display = "contents", w(), (R = n.current) == null || R.appendChild(i), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (f = n.current) == null || f.appendChild(i);
    return () => {
      var a, h;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((h = n.current) == null || h.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, o, s, r]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function We(e, t = !1) {
  try {
    if (t && !Ae(e))
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
function x(e, t) {
  return q(() => We(e, t), [e, t]);
}
function X(e, t, o) {
  const s = e.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, n) => {
      var w;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const l = {
        ...r.props,
        key: ((w = r.props) == null ? void 0 : w.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let c = l;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((g, y) => {
          c[g] || (c[g] = {}), y !== f.length - 1 && (c = l[g]);
        });
        const a = r.slots[u];
        let h, _, m = (t == null ? void 0 : t.clone) ?? !1;
        a instanceof Element ? h = a : (h = a.el, _ = a.callback, m = a.clone ?? m), c[f[f.length - 1]] = h ? _ ? (...g) => (_(f[f.length - 1], g), /* @__PURE__ */ p.jsx(b, {
          slot: h,
          clone: m
        })) : /* @__PURE__ */ p.jsx(b, {
          slot: h,
          clone: m
        }) : c[f[f.length - 1]], c = l;
      });
      const i = (t == null ? void 0 : t.children) || "children";
      return r[i] && (l[i] = X(r[i], t, `${n}`)), l;
    });
}
function De(e, t) {
  return e ? /* @__PURE__ */ p.jsx(b, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function v({
  key: e,
  setSlotParams: t,
  slots: o
}, s) {
  return o[e] ? (...r) => (t(e, r), De(o[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const ze = Fe(({
  slots: e,
  children: t,
  onValueChange: o,
  filterOption: s,
  onChange: r,
  options: n,
  optionItems: l,
  getPopupContainer: c,
  dropdownRender: i,
  optionRender: w,
  tagRender: u,
  labelRender: f,
  filterSort: a,
  elRef: h,
  setSlotParams: _,
  ...m
}) => {
  const g = x(c), y = x(s), R = x(i), j = x(a), d = x(w), Z = x(u), $ = x(f);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ p.jsx(se, {
      ...m,
      ref: h,
      options: q(() => n || X(l, {
        children: "options",
        clone: !0
      }), [l, n]),
      onChange: (N, ...ee) => {
        r == null || r(N, ...ee), o(N);
      },
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : m.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ p.jsx(b, {
        slot: e.prefix
      }) : m.prefix,
      removeIcon: e.removeIcon ? /* @__PURE__ */ p.jsx(b, {
        slot: e.removeIcon
      }) : m.removeIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ p.jsx(b, {
        slot: e.suffixIcon
      }) : m.suffixIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ p.jsx(b, {
        slot: e.notFoundContent
      }) : m.notFoundContent,
      menuItemSelectedIcon: e.menuItemSelectedIcon ? /* @__PURE__ */ p.jsx(b, {
        slot: e.menuItemSelectedIcon
      }) : m.menuItemSelectedIcon,
      filterOption: y || s,
      maxTagPlaceholder: e.maxTagPlaceholder ? v({
        slots: e,
        setSlotParams: _,
        key: "maxTagPlaceholder"
      }) : m.maxTagPlaceholder,
      getPopupContainer: g,
      dropdownRender: e.dropdownRender ? v({
        slots: e,
        setSlotParams: _,
        key: "dropdownRender"
      }) : R,
      optionRender: e.optionRender ? v({
        slots: e,
        setSlotParams: _,
        key: "optionRender"
      }) : d,
      tagRender: e.tagRender ? v({
        slots: e,
        setSlotParams: _,
        key: "tagRender"
      }) : Z,
      labelRender: e.labelRender ? v({
        slots: e,
        setSlotParams: _,
        key: "labelRender"
      }) : $,
      filterSort: j
    })]
  });
});
export {
  ze as Select,
  ze as default
};
