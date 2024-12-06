import { g as be, w as F } from "./Index-Cg3aPQhv.js";
const I = window.ms_globals.React, he = window.ms_globals.React.forwardRef, ve = window.ms_globals.React.useRef, ge = window.ms_globals.React.useState, we = window.ms_globals.React.useEffect, x = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, ye = window.ms_globals.antd.DatePicker, z = window.ms_globals.dayjs;
var X = {
  exports: {}
}, A = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var xe = I, Ee = Symbol.for("react.element"), Ie = Symbol.for("react.fragment"), Re = Object.prototype.hasOwnProperty, Ce = xe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, t, o) {
  var s, r = {}, n = null, l = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) Re.call(t, s) && !je.hasOwnProperty(s) && (r[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: Ee,
    type: e,
    key: n,
    ref: l,
    props: r,
    _owner: Ce.current
  };
}
A.Fragment = Ie;
A.jsx = Z;
A.jsxs = Z;
X.exports = A;
var m = X.exports;
const {
  SvelteComponent: Se,
  assign: G,
  binding_callbacks: U,
  check_outros: ke,
  children: $,
  claim_element: ee,
  claim_space: Oe,
  component_subscribe: H,
  compute_slots: Pe,
  create_slot: Fe,
  detach: S,
  element: te,
  empty: q,
  exclude_internal_props: B,
  get_all_dirty_from_scope: De,
  get_slot_changes: Ne,
  group_outros: Ae,
  init: Le,
  insert_hydration: D,
  safe_not_equal: Te,
  set_custom_element_data: ne,
  space: Me,
  transition_in: N,
  transition_out: W,
  update_slot_base: We
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ve,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function J(e) {
  let t, o;
  const s = (
    /*#slots*/
    e[7].default
  ), r = Fe(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = te("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = ee(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = $(t);
      r && r.l(l), l.forEach(S), this.h();
    },
    h() {
      ne(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      D(n, t, l), r && r.m(t, null), e[9](t), o = !0;
    },
    p(n, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && We(
        r,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? Ne(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : De(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (N(r, n), o = !0);
    },
    o(n) {
      W(r, n), o = !1;
    },
    d(n) {
      n && S(t), r && r.d(n), e[9](null);
    }
  };
}
function He(e) {
  let t, o, s, r, n = (
    /*$$slots*/
    e[4].default && J(e)
  );
  return {
    c() {
      t = te("react-portal-target"), o = Me(), n && n.c(), s = q(), this.h();
    },
    l(l) {
      t = ee(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(t).forEach(S), o = Oe(l), n && n.l(l), s = q(), this.h();
    },
    h() {
      ne(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      D(l, t, c), e[8](t), D(l, o, c), n && n.m(l, c), D(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && N(n, 1)) : (n = J(l), n.c(), N(n, 1), n.m(s.parentNode, s)) : n && (Ae(), W(n, 1, 1, () => {
        n = null;
      }), ke());
    },
    i(l) {
      r || (N(n), r = !0);
    },
    o(l) {
      W(n), r = !1;
    },
    d(l) {
      l && (S(t), S(o), S(s)), e[8](null), n && n.d(l);
    }
  };
}
function Y(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function qe(e, t, o) {
  let s, r, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const c = Pe(n);
  let {
    svelteInit: i
  } = t;
  const v = F(Y(t)), u = F();
  H(e, u, (d) => o(0, s = d));
  const f = F();
  H(e, f, (d) => o(1, r = d));
  const a = [], p = ze("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: h
  } = be() || {}, w = i({
    parent: p,
    props: v,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: g,
    subSlotIndex: h,
    onDestroy(d) {
      a.push(d);
    }
  });
  Ue("$$ms-gr-react-wrapper", w), Ve(() => {
    v.set(Y(t));
  }), Ge(() => {
    a.forEach((d) => d());
  });
  function R(d) {
    U[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function k(d) {
    U[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return e.$$set = (d) => {
    o(17, t = G(G({}, t), B(d))), "svelteInit" in d && o(5, i = d.svelteInit), "$$scope" in d && o(6, l = d.$$scope);
  }, t = B(t), [s, r, u, f, c, i, l, n, R, k];
}
class Be extends Se {
  constructor(t) {
    super(), Le(this, t, qe, He, Te, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, L = window.ms_globals.tree;
function Je(e) {
  function t(o) {
    const s = F(), r = new Be({
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
          }, c = n.parent ?? L;
          return c.nodes = [...c.nodes, l], K({
            createPortal: M,
            node: L
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), K({
              createPortal: M,
              node: L
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
const Ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ke(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const s = e[o];
    return typeof s == "number" && !Ye.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function V(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(M(I.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: I.Children.toArray(e._reactElement.props.children).map((r) => {
        if (I.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = V(r.props.el);
          return I.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...I.Children.toArray(r.props.children), ...n]
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
      } = V(n);
      t.push(...c), o.appendChild(l);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Qe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const b = he(({
  slot: e,
  clone: t,
  className: o,
  style: s
}, r) => {
  const n = ve(), [l, c] = ge([]);
  return we(() => {
    var f;
    if (!n.current || !e)
      return;
    let i = e;
    function v() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Qe(r, a), o && a.classList.add(...o.split(" ")), s) {
        const p = Ke(s);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var h, w, R;
        (h = n.current) != null && h.contains(i) && ((w = n.current) == null || w.removeChild(i));
        const {
          portals: _,
          clonedElement: g
        } = V(e);
        return i = g, c(_), i.style.display = "contents", v(), (R = n.current) == null || R.appendChild(i), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", v(), (f = n.current) == null || f.appendChild(i);
    return () => {
      var a, p;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((p = n.current) == null || p.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, o, s, r]), I.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Xe(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ze(e, t = !1) {
  try {
    if (t && !Xe(e))
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
function O(e, t) {
  return x(() => Ze(e, t), [e, t]);
}
function re(e, t, o) {
  const s = e.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, n) => {
      var v;
      if (typeof r != "object")
        return r;
      const l = {
        ...r.props,
        key: ((v = r.props) == null ? void 0 : v.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let c = l;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((h, w) => {
          c[h] || (c[h] = {}), w !== f.length - 1 && (c = l[h]);
        });
        const a = r.slots[u];
        let p, _, g = !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, g = a.clone ?? g), c[f[f.length - 1]] = p ? _ ? (...h) => (_(f[f.length - 1], h), /* @__PURE__ */ m.jsx(b, {
          slot: p,
          clone: g
        })) : /* @__PURE__ */ m.jsx(b, {
          slot: p,
          clone: g
        }) : c[f[f.length - 1]], c = l;
      });
      const i = "children";
      return r[i] && (l[i] = re(r[i], t, `${n}`)), l;
    });
}
function $e(e, t) {
  return e ? /* @__PURE__ */ m.jsx(b, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function T({
  key: e,
  setSlotParams: t,
  slots: o
}, s) {
  return o[e] ? (...r) => (t(e, r), $e(o[e], {
    clone: !0,
    ...s
  })) : void 0;
}
function E(e) {
  return Array.isArray(e) ? e.map((t) => E(t)) : z(typeof e == "number" ? e * 1e3 : e);
}
function Q(e) {
  return Array.isArray(e) ? e.map((t) => t ? t.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const tt = Je(({
  slots: e,
  disabledDate: t,
  disabledTime: o,
  value: s,
  defaultValue: r,
  defaultPickerValue: n,
  pickerValue: l,
  showTime: c,
  presets: i,
  presetItems: v,
  onChange: u,
  minDate: f,
  maxDate: a,
  cellRender: p,
  panelRender: _,
  getPopupContainer: g,
  onValueChange: h,
  onPanelChange: w,
  children: R,
  setSlotParams: k,
  elRef: d,
  ...y
}) => {
  const oe = O(t), le = O(o), se = O(g), ce = O(p), ie = O(_), ae = x(() => typeof c == "object" ? {
    ...c,
    defaultValue: c.defaultValue ? E(c.defaultValue) : void 0
  } : c, [c]), ue = x(() => s ? E(s) : void 0, [s]), de = x(() => r ? E(r) : void 0, [r]), fe = x(() => n ? E(n) : void 0, [n]), pe = x(() => l ? E(l) : void 0, [l]), _e = x(() => f ? E(f) : void 0, [f]), me = x(() => a ? E(a) : void 0, [a]);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: R
    }), /* @__PURE__ */ m.jsx(ye, {
      ...y,
      ref: d,
      value: ue,
      defaultValue: de,
      defaultPickerValue: fe,
      pickerValue: pe,
      minDate: _e,
      maxDate: me,
      showTime: ae,
      disabledDate: oe,
      disabledTime: le,
      getPopupContainer: se,
      cellRender: e.cellRender ? T({
        slots: e,
        setSlotParams: k,
        key: "cellRender"
      }) : ce,
      panelRender: e.panelRender ? T({
        slots: e,
        setSlotParams: k,
        key: "panelRender"
      }) : ie,
      presets: x(() => {
        var C;
        return (C = i || re(v)) == null ? void 0 : C.map((j) => ({
          ...j,
          value: E(j.value)
        }));
      }, [i, v]),
      onPanelChange: (C, ...j) => {
        const P = Q(C);
        w == null || w(P, ...j);
      },
      onChange: (C, ...j) => {
        const P = Q(C);
        u == null || u(P, ...j), h(P);
      },
      renderExtraFooter: e.renderExtraFooter ? T({
        slots: e,
        setSlotParams: k,
        key: "renderExtraFooter"
      }) : y.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.prevIcon
      }) : y.prevIcon,
      prefix: e.prefix ? /* @__PURE__ */ m.jsx(b, {
        slot: e.prefix
      }) : y.prefix,
      nextIcon: e.nextIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.nextIcon
      }) : y.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.suffixIcon
      }) : y.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.superNextIcon
      }) : y.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.superPrevIcon
      }) : y.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : y.allowClear
    })]
  });
});
export {
  tt as DatePicker,
  tt as default
};
