import { b as fe, g as he, w as S } from "./Index-CeYzZL1E.js";
const R = window.ms_globals.React, de = window.ms_globals.React.forwardRef, T = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, L = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, N = window.ms_globals.ReactDOM.createPortal, _e = window.ms_globals.antd.Cascader;
function pe(e, t) {
  return fe(e, t);
}
var K = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var me = R, ge = Symbol.for("react.element"), we = Symbol.for("react.fragment"), be = Object.prototype.hasOwnProperty, ye = me.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, xe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(e, t, o) {
  var l, r = {}, n = null, s = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) be.call(t, l) && !xe.hasOwnProperty(l) && (r[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: ge,
    type: e,
    key: n,
    ref: s,
    props: r,
    _owner: ye.current
  };
}
F.Fragment = we;
F.jsx = Q;
F.jsxs = Q;
K.exports = F;
var m = K.exports;
const {
  SvelteComponent: Ee,
  assign: W,
  binding_callbacks: M,
  check_outros: Re,
  children: X,
  claim_element: Z,
  claim_space: Ce,
  component_subscribe: q,
  compute_slots: ve,
  create_slot: Ie,
  detach: v,
  element: $,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Se,
  get_slot_changes: ke,
  group_outros: je,
  init: Fe,
  insert_hydration: k,
  safe_not_equal: Oe,
  set_custom_element_data: ee,
  space: Pe,
  transition_in: j,
  transition_out: A,
  update_slot_base: Te
} = window.__gradio__svelte__internal, {
  beforeUpdate: Le,
  getContext: Ne,
  onDestroy: Ae,
  setContext: De
} = window.__gradio__svelte__internal;
function U(e) {
  let t, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = Ie(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = $("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = Z(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = X(t);
      r && r.l(s), s.forEach(v), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      k(n, t, s), r && r.m(t, null), e[9](t), o = !0;
    },
    p(n, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && Te(
        r,
        l,
        n,
        /*$$scope*/
        n[6],
        o ? ke(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : Se(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (j(r, n), o = !0);
    },
    o(n) {
      A(r, n), o = !1;
    },
    d(n) {
      n && v(t), r && r.d(n), e[9](null);
    }
  };
}
function Ve(e) {
  let t, o, l, r, n = (
    /*$$slots*/
    e[4].default && U(e)
  );
  return {
    c() {
      t = $("react-portal-target"), o = Pe(), n && n.c(), l = z(), this.h();
    },
    l(s) {
      t = Z(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), X(t).forEach(v), o = Ce(s), n && n.l(s), l = z(), this.h();
    },
    h() {
      ee(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      k(s, t, i), e[8](t), k(s, o, i), n && n.m(s, i), k(s, l, i), r = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, i), i & /*$$slots*/
      16 && j(n, 1)) : (n = U(s), n.c(), j(n, 1), n.m(l.parentNode, l)) : n && (je(), A(n, 1, 1, () => {
        n = null;
      }), Re());
    },
    i(s) {
      r || (j(n), r = !0);
    },
    o(s) {
      A(n), r = !1;
    },
    d(s) {
      s && (v(t), v(o), v(l)), e[8](null), n && n.d(s);
    }
  };
}
function H(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function We(e, t, o) {
  let l, r, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const i = ve(n);
  let {
    svelteInit: c
  } = t;
  const g = S(H(t)), u = S();
  q(e, u, (d) => o(0, l = d));
  const f = S();
  q(e, f, (d) => o(1, r = d));
  const a = [], p = Ne("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: w,
    subSlotIndex: h
  } = he() || {}, x = c({
    parent: p,
    props: g,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: w,
    subSlotIndex: h,
    onDestroy(d) {
      a.push(d);
    }
  });
  De("$$ms-gr-react-wrapper", x), Le(() => {
    g.set(H(t));
  }), Ae(() => {
    a.forEach((d) => d());
  });
  function C(d) {
    M[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function O(d) {
    M[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return e.$$set = (d) => {
    o(17, t = W(W({}, t), G(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, t = G(t), [l, r, u, f, i, c, s, n, C, O];
}
class Me extends Ee {
  constructor(t) {
    super(), Fe(this, t, We, Ve, Oe, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, P = window.ms_globals.tree;
function qe(e) {
  function t(o) {
    const l = S(), r = new Me({
      ...o,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, i = n.parent ?? P;
          return i.nodes = [...i.nodes, s], B({
            createPortal: N,
            node: P
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), B({
              createPortal: N,
              node: P
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const ze = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ge(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const l = e[o];
    return typeof l == "number" && !ze.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function D(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(N(R.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: R.Children.toArray(e._reactElement.props.children).map((r) => {
        if (R.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = D(r.props.el);
          return R.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...R.Children.toArray(r.props.children), ...n]
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
      listener: s,
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, s, c);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const n = l[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = D(n);
      t.push(...i), o.appendChild(s);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Ue(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = de(({
  slot: e,
  clone: t,
  className: o,
  style: l
}, r) => {
  const n = T(), [s, i] = J([]);
  return L(() => {
    var f;
    if (!n.current || !e)
      return;
    let c = e;
    function g() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ue(r, a), o && a.classList.add(...o.split(" ")), l) {
        const p = Ge(l);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var h, x, C;
        (h = n.current) != null && h.contains(c) && ((x = n.current) == null || x.removeChild(c));
        const {
          portals: _,
          clonedElement: w
        } = D(e);
        return c = w, i(_), c.style.display = "contents", g(), (C = n.current) == null || C.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", g(), (f = n.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = n.current) != null && a.contains(c) && ((p = n.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [e, t, o, l, r]), R.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function He(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Be(e, t = !1) {
  try {
    if (t && !He(e))
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
function b(e, t) {
  return Y(() => Be(e, t), [e, t]);
}
function Je({
  value: e,
  onValueChange: t
}) {
  const [o, l] = J(e), r = T(t);
  r.current = t;
  const n = T(o);
  return n.current = o, L(() => {
    r.current(o);
  }, [o]), L(() => {
    pe(e, n.current) || l(e);
  }, [e]), [o, l];
}
function te(e, t, o) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((r, n) => {
      var g;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const s = {
        ...r.props,
        key: ((g = r.props) == null ? void 0 : g.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let i = s;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((h, x) => {
          i[h] || (i[h] = {}), x !== f.length - 1 && (i = s[h]);
        });
        const a = r.slots[u];
        let p, _, w = (t == null ? void 0 : t.clone) ?? !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, w = a.clone ?? w), i[f[f.length - 1]] = p ? _ ? (...h) => (_(f[f.length - 1], h), /* @__PURE__ */ m.jsx(y, {
          slot: p,
          clone: w
        })) : /* @__PURE__ */ m.jsx(y, {
          slot: p,
          clone: w
        }) : i[f[f.length - 1]], i = s;
      });
      const c = (t == null ? void 0 : t.children) || "children";
      return r[c] && (s[c] = te(r[c], t, `${n}`)), s;
    });
}
function Ye(e, t) {
  return e ? /* @__PURE__ */ m.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function I({
  key: e,
  setSlotParams: t,
  slots: o
}, l) {
  return o[e] ? (...r) => (t(e, r), Ye(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function Ke(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Xe = qe(({
  slots: e,
  children: t,
  onValueChange: o,
  onChange: l,
  displayRender: r,
  elRef: n,
  getPopupContainer: s,
  tagRender: i,
  maxTagPlaceholder: c,
  dropdownRender: g,
  optionRender: u,
  showSearch: f,
  optionItems: a,
  options: p,
  setSlotParams: _,
  onLoadData: w,
  ...h
}) => {
  const x = b(s), C = b(r), O = b(i), d = b(u), ne = b(g), re = b(c), oe = typeof f == "object" || e["showSearch.render"], E = Ke(f), le = b(E.filter), se = b(E.render), ce = b(E.sort), [ie, ae] = Je({
    onValueChange: o,
    value: h.value
  });
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ m.jsx(_e, {
      ...h,
      ref: n,
      value: ie,
      options: Y(() => p || te(a, {
        clone: !0
      }), [p, a]),
      showSearch: oe ? {
        ...E,
        filter: le || E.filter,
        render: e["showSearch.render"] ? I({
          slots: e,
          setSlotParams: _,
          key: "showSearch.render"
        }) : se || E.render,
        sort: ce || E.sort
      } : f,
      loadData: w,
      optionRender: d,
      getPopupContainer: x,
      prefix: e.prefix ? /* @__PURE__ */ m.jsx(y, {
        slot: e.prefix
      }) : h.prefix,
      dropdownRender: e.dropdownRender ? I({
        slots: e,
        setSlotParams: _,
        key: "dropdownRender"
      }) : ne,
      displayRender: e.displayRender ? I({
        slots: e,
        setSlotParams: _,
        key: "displayRender"
      }) : C,
      tagRender: e.tagRender ? I({
        slots: e,
        setSlotParams: _,
        key: "tagRender"
      }) : O,
      onChange: (V, ...ue) => {
        l == null || l(V, ...ue), ae(V);
      },
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(y, {
        slot: e.suffixIcon
      }) : h.suffixIcon,
      expandIcon: e.expandIcon ? /* @__PURE__ */ m.jsx(y, {
        slot: e.expandIcon
      }) : h.expandIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ m.jsx(y, {
        slot: e.removeIcon
      }) : h.removeIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ m.jsx(y, {
        slot: e.notFoundContent
      }) : h.notFoundContent,
      maxTagPlaceholder: e.maxTagPlaceholder ? I({
        slots: e,
        setSlotParams: _,
        key: "maxTagPlaceholder"
      }) : re || c,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : h.allowClear
    })]
  });
});
export {
  Xe as Cascader,
  Xe as default
};
