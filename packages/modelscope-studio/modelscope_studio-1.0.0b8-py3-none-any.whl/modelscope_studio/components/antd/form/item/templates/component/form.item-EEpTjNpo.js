import { g as le, w as I } from "./Index-CNzMEl_N.js";
const C = window.ms_globals.React, ne = window.ms_globals.React.forwardRef, oe = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, se = window.ms_globals.React.useEffect, A = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ie = window.ms_globals.internalContext.FormItemContext, ce = window.ms_globals.antd.Form;
var J = {
  exports: {}
}, j = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ae = C, ue = Symbol.for("react.element"), fe = Symbol.for("react.fragment"), de = Object.prototype.hasOwnProperty, pe = ae.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, me = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(e, n, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) de.call(n, l) && !me.hasOwnProperty(l) && (o[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ue,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: pe.current
  };
}
j.Fragment = fe;
j.jsx = Y;
j.jsxs = Y;
J.exports = j;
var g = J.exports;
const {
  SvelteComponent: _e,
  assign: W,
  binding_callbacks: z,
  check_outros: he,
  children: K,
  claim_element: Q,
  claim_space: ge,
  component_subscribe: D,
  compute_slots: we,
  create_slot: be,
  detach: R,
  element: X,
  empty: V,
  exclude_internal_props: G,
  get_all_dirty_from_scope: ye,
  get_slot_changes: Ee,
  group_outros: xe,
  init: ve,
  insert_hydration: F,
  safe_not_equal: Ce,
  set_custom_element_data: Z,
  space: Re,
  transition_in: O,
  transition_out: L,
  update_slot_base: Ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: Fe,
  getContext: Oe,
  onDestroy: Se,
  setContext: je
} = window.__gradio__svelte__internal;
function M(e) {
  let n, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = be(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = X("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = Q(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(n);
      o && o.l(s), s.forEach(R), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      F(t, n, s), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ie(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? Ee(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : ye(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (O(o, t), r = !0);
    },
    o(t) {
      L(o, t), r = !1;
    },
    d(t) {
      t && R(n), o && o.d(t), e[9](null);
    }
  };
}
function Pe(e) {
  let n, r, l, o, t = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      n = X("react-portal-target"), r = Re(), t && t.c(), l = V(), this.h();
    },
    l(s) {
      n = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(n).forEach(R), r = ge(s), t && t.l(s), l = V(), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      F(s, n, i), e[8](n), F(s, r, i), t && t.m(s, i), F(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && O(t, 1)) : (t = M(s), t.c(), O(t, 1), t.m(l.parentNode, l)) : t && (xe(), L(t, 1, 1, () => {
        t = null;
      }), he());
    },
    i(s) {
      o || (O(t), o = !0);
    },
    o(s) {
      L(t), o = !1;
    },
    d(s) {
      s && (R(n), R(r), R(l)), e[8](null), t && t.d(s);
    }
  };
}
function H(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function ke(e, n, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const i = we(t);
  let {
    svelteInit: c
  } = n;
  const _ = I(H(n)), u = I();
  D(e, u, (f) => r(0, l = f));
  const d = I();
  D(e, d, (f) => r(1, o = f));
  const a = [], p = Oe("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: h
  } = le() || {}, b = c({
    parent: p,
    props: _,
    target: u,
    slot: d,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: h,
    onDestroy(f) {
      a.push(f);
    }
  });
  je("$$ms-gr-react-wrapper", b), Fe(() => {
    _.set(H(n));
  }), Se(() => {
    a.forEach((f) => f());
  });
  function E(f) {
    z[f ? "unshift" : "push"](() => {
      l = f, u.set(l);
    });
  }
  function x(f) {
    z[f ? "unshift" : "push"](() => {
      o = f, d.set(o);
    });
  }
  return e.$$set = (f) => {
    r(17, n = W(W({}, n), G(f))), "svelteInit" in f && r(5, c = f.svelteInit), "$$scope" in f && r(6, s = f.$$scope);
  }, n = G(n), [l, o, u, d, i, c, s, t, E, x];
}
class Le extends _e {
  constructor(n) {
    super(), ve(this, n, ke, Pe, Ce, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, P = window.ms_globals.tree;
function Te(e) {
  function n(r) {
    const l = I(), o = new Le({
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
          return i.nodes = [...i.nodes, s], U({
            createPortal: k,
            node: P
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), U({
              createPortal: k,
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
const Ae = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ne(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !Ae.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function T(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(k(C.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: C.Children.toArray(e._reactElement.props.children).map((o) => {
        if (C.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = T(o.props.el);
          return C.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...C.Children.toArray(o.props.children), ...t]
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
      useCapture: c
    }) => {
      r.addEventListener(i, s, c);
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
function We(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const y = ne(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, o) => {
  const t = oe(), [s, i] = re([]);
  return se(() => {
    var d;
    if (!t.current || !e)
      return;
    let c = e;
    function _() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), We(o, a), r && a.classList.add(...r.split(" ")), l) {
        const p = Ne(l);
        Object.keys(p).forEach((m) => {
          a.style[m] = p[m];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var h, b, E;
        (h = t.current) != null && h.contains(c) && ((b = t.current) == null || b.removeChild(c));
        const {
          portals: m,
          clonedElement: w
        } = T(e);
        return c = w, i(m), c.style.display = "contents", _(), (E = t.current) == null || E.appendChild(c), m.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", _(), (d = t.current) == null || d.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((p = t.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [e, n, r, l, o]), C.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ze(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function S(e, n = !1) {
  try {
    if (n && !ze(e))
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
function v(e, n) {
  return A(() => S(e, n), [e, n]);
}
function $(e, n, r) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, t) => {
      var _;
      if (typeof o != "object")
        return o;
      const s = {
        ...o.props,
        key: ((_ = o.props) == null ? void 0 : _.key) ?? (r ? `${r}-${t}` : `${t}`)
      };
      let i = s;
      Object.keys(o.slots).forEach((u) => {
        if (!o.slots[u] || !(o.slots[u] instanceof Element) && !o.slots[u].el)
          return;
        const d = u.split(".");
        d.forEach((h, b) => {
          i[h] || (i[h] = {}), b !== d.length - 1 && (i = s[h]);
        });
        const a = o.slots[u];
        let p, m, w = !1;
        a instanceof Element ? p = a : (p = a.el, m = a.callback, w = a.clone ?? w), i[d[d.length - 1]] = p ? m ? (...h) => (m(d[d.length - 1], h), /* @__PURE__ */ g.jsx(y, {
          slot: p,
          clone: w
        })) : /* @__PURE__ */ g.jsx(y, {
          slot: p,
          clone: w
        }) : i[d[d.length - 1]], i = s;
      });
      const c = "children";
      return o[c] && (s[c] = $(o[c], n, `${t}`)), s;
    });
}
function De(e) {
  const n = e.pattern;
  return {
    ...e,
    pattern: (() => {
      if (typeof n == "string" && n.startsWith("/")) {
        const r = n.match(/^\/(.+)\/([gimuy]*)$/);
        if (r) {
          const [, l, o] = r;
          return new RegExp(l, o);
        }
      }
      return typeof n == "string" ? new RegExp(n) : void 0;
    })() ? new RegExp(n) : void 0,
    defaultField: S(e.defaultField) || e.defaultField,
    transform: S(e.transform),
    validator: S(e.validator)
  };
}
function q(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const B = ({
  children: e,
  ...n
}) => /* @__PURE__ */ g.jsx(ie.Provider, {
  value: A(() => n, [n]),
  children: e
}), Ge = Te(({
  slots: e,
  getValueFromEvent: n,
  getValueProps: r,
  normalize: l,
  shouldUpdate: o,
  tooltip: t,
  ruleItems: s,
  rules: i,
  children: c,
  hasFeedback: _,
  ...u
}) => {
  const d = e["tooltip.icon"] || e["tooltip.title"] || typeof t == "object", a = typeof _ == "object", p = q(_), m = v(p.icons), w = v(n), h = v(r), b = v(l), E = v(o), x = q(t), f = v(x.afterOpenChange), ee = v(x.getPopupContainer);
  return /* @__PURE__ */ g.jsx(ce.Item, {
    ...u,
    hasFeedback: a ? {
      ...p,
      icons: m || p.icons
    } : _,
    getValueFromEvent: w,
    getValueProps: h,
    normalize: b,
    shouldUpdate: E || o,
    rules: A(() => {
      var N;
      return (N = i || $(s)) == null ? void 0 : N.map((te) => De(te));
    }, [s, i]),
    tooltip: e.tooltip ? /* @__PURE__ */ g.jsx(y, {
      slot: e.tooltip
    }) : d ? {
      ...x,
      afterOpenChange: f,
      getPopupContainer: ee,
      icon: e["tooltip.icon"] ? /* @__PURE__ */ g.jsx(y, {
        slot: e["tooltip.icon"]
      }) : x.icon,
      title: e["tooltip.title"] ? /* @__PURE__ */ g.jsx(y, {
        slot: e["tooltip.title"]
      }) : x.title
    } : t,
    extra: e.extra ? /* @__PURE__ */ g.jsx(y, {
      slot: e.extra
    }) : u.extra,
    help: e.help ? /* @__PURE__ */ g.jsx(y, {
      slot: e.help
    }) : u.help,
    label: e.label ? /* @__PURE__ */ g.jsx(y, {
      slot: e.label
    }) : u.label,
    children: E || o ? () => /* @__PURE__ */ g.jsx(B, {
      children: c
    }) : /* @__PURE__ */ g.jsx(B, {
      children: c
    })
  });
});
export {
  Ge as FormItem,
  Ge as default
};
