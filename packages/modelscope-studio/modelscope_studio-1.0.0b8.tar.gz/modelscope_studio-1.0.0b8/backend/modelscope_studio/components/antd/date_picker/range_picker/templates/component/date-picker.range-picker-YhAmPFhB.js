import { g as ve, w as F } from "./Index-CoZcLTKR.js";
const j = window.ms_globals.React, me = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, ge = window.ms_globals.React.useState, we = window.ms_globals.React.useEffect, R = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, xe = window.ms_globals.antd.DatePicker, U = window.ms_globals.dayjs;
var Z = {
  exports: {}
}, L = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ye = j, be = Symbol.for("react.element"), Ee = Symbol.for("react.fragment"), Ie = Object.prototype.hasOwnProperty, Re = ye.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, n, o) {
  var s, r = {}, t = null, l = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) Ie.call(n, s) && !je.hasOwnProperty(s) && (r[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: be,
    type: e,
    key: t,
    ref: l,
    props: r,
    _owner: Re.current
  };
}
L.Fragment = Ee;
L.jsx = V;
L.jsxs = V;
Z.exports = L;
var m = Z.exports;
const {
  SvelteComponent: Se,
  assign: H,
  binding_callbacks: q,
  check_outros: Oe,
  children: $,
  claim_element: ee,
  claim_space: Pe,
  component_subscribe: B,
  compute_slots: ke,
  create_slot: Ce,
  detach: P,
  element: te,
  empty: J,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: De,
  get_slot_changes: Fe,
  group_outros: Ne,
  init: Ae,
  insert_hydration: N,
  safe_not_equal: Le,
  set_custom_element_data: ne,
  space: Te,
  transition_in: A,
  transition_out: z,
  update_slot_base: Me
} = window.__gradio__svelte__internal, {
  beforeUpdate: We,
  getContext: ze,
  onDestroy: Ge,
  setContext: Ue
} = window.__gradio__svelte__internal;
function K(e) {
  let n, o;
  const s = (
    /*#slots*/
    e[7].default
  ), r = Ce(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = te("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = ee(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = $(n);
      r && r.l(l), l.forEach(P), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      N(t, n, l), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && Me(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        o ? Fe(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : De(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (A(r, t), o = !0);
    },
    o(t) {
      z(r, t), o = !1;
    },
    d(t) {
      t && P(n), r && r.d(t), e[9](null);
    }
  };
}
function He(e) {
  let n, o, s, r, t = (
    /*$$slots*/
    e[4].default && K(e)
  );
  return {
    c() {
      n = te("react-portal-target"), o = Te(), t && t.c(), s = J(), this.h();
    },
    l(l) {
      n = ee(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(n).forEach(P), o = Pe(l), t && t.l(l), s = J(), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      N(l, n, i), e[8](n), N(l, o, i), t && t.m(l, i), N(l, s, i), r = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, i), i & /*$$slots*/
      16 && A(t, 1)) : (t = K(l), t.c(), A(t, 1), t.m(s.parentNode, s)) : t && (Ne(), z(t, 1, 1, () => {
        t = null;
      }), Oe());
    },
    i(l) {
      r || (A(t), r = !0);
    },
    o(l) {
      z(t), r = !1;
    },
    d(l) {
      l && (P(n), P(o), P(s)), e[8](null), t && t.d(l);
    }
  };
}
function Q(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function qe(e, n, o) {
  let s, r, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const i = ke(t);
  let {
    svelteInit: c
  } = n;
  const w = F(Q(n)), u = F();
  B(e, u, (f) => o(0, s = f));
  const d = F();
  B(e, d, (f) => o(1, r = f));
  const a = [], _ = ze("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: x,
    subSlotIndex: g
  } = ve() || {}, y = c({
    parent: _,
    props: w,
    target: u,
    slot: d,
    slotKey: h,
    slotIndex: x,
    subSlotIndex: g,
    onDestroy(f) {
      a.push(f);
    }
  });
  Ue("$$ms-gr-react-wrapper", y), We(() => {
    w.set(Q(n));
  }), Ge(() => {
    a.forEach((f) => f());
  });
  function S(f) {
    q[f ? "unshift" : "push"](() => {
      s = f, u.set(s);
    });
  }
  function k(f) {
    q[f ? "unshift" : "push"](() => {
      r = f, d.set(r);
    });
  }
  return e.$$set = (f) => {
    o(17, n = H(H({}, n), Y(f))), "svelteInit" in f && o(5, c = f.svelteInit), "$$scope" in f && o(6, l = f.$$scope);
  }, n = Y(n), [s, r, u, d, i, c, l, t, S, k];
}
class Be extends Se {
  constructor(n) {
    super(), Ae(this, n, qe, He, Le, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, T = window.ms_globals.tree;
function Je(e) {
  function n(o) {
    const s = F(), r = new Be({
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
          }, i = t.parent ?? T;
          return i.nodes = [...i.nodes, l], X({
            createPortal: W,
            node: T
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), X({
              createPortal: W,
              node: T
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
const Ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ke(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const s = e[o];
    return typeof s == "number" && !Ye.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function G(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(W(j.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: j.Children.toArray(e._reactElement.props.children).map((r) => {
        if (j.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = G(r.props.el);
          return j.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...j.Children.toArray(r.props.children), ...t]
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
      } = G(t);
      n.push(...i), o.appendChild(l);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Qe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const v = me(({
  slot: e,
  clone: n,
  className: o,
  style: s
}, r) => {
  const t = he(), [l, i] = ge([]);
  return we(() => {
    var d;
    if (!t.current || !e)
      return;
    let c = e;
    function w() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Qe(r, a), o && a.classList.add(...o.split(" ")), s) {
        const _ = Ke(s);
        Object.keys(_).forEach((h) => {
          a.style[h] = _[h];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var g, y, S;
        (g = t.current) != null && g.contains(c) && ((y = t.current) == null || y.removeChild(c));
        const {
          portals: h,
          clonedElement: x
        } = G(e);
        return c = x, i(h), c.style.display = "contents", w(), (S = t.current) == null || S.appendChild(c), h.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", w(), (d = t.current) == null || d.appendChild(c);
    return () => {
      var a, _;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((_ = t.current) == null || _.removeChild(c)), u == null || u.disconnect();
    };
  }, [e, n, o, s, r]), j.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Xe(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ze(e, n = !1) {
  try {
    if (n && !Xe(e))
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
function C(e, n) {
  return R(() => Ze(e, n), [e, n]);
}
function re(e, n, o) {
  const s = e.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, t) => {
      var w;
      if (typeof r != "object")
        return r;
      const l = {
        ...r.props,
        key: ((w = r.props) == null ? void 0 : w.key) ?? (o ? `${o}-${t}` : `${t}`)
      };
      let i = l;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const d = u.split(".");
        d.forEach((g, y) => {
          i[g] || (i[g] = {}), y !== d.length - 1 && (i = l[g]);
        });
        const a = r.slots[u];
        let _, h, x = !1;
        a instanceof Element ? _ = a : (_ = a.el, h = a.callback, x = a.clone ?? x), i[d[d.length - 1]] = _ ? h ? (...g) => (h(d[d.length - 1], g), /* @__PURE__ */ m.jsx(v, {
          slot: _,
          clone: x
        })) : /* @__PURE__ */ m.jsx(v, {
          slot: _,
          clone: x
        }) : i[d[d.length - 1]], i = l;
      });
      const c = "children";
      return r[c] && (l[c] = re(r[c], n, `${t}`)), l;
    });
}
function Ve(e, n) {
  return e ? /* @__PURE__ */ m.jsx(v, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function M({
  key: e,
  setSlotParams: n,
  slots: o
}, s) {
  return o[e] ? (...r) => (n(e, r), Ve(o[e], {
    clone: !0,
    ...s
  })) : void 0;
}
function I(e) {
  return U(typeof e == "number" ? e * 1e3 : e);
}
function D(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
}
const et = Je(({
  slots: e,
  disabledDate: n,
  value: o,
  defaultValue: s,
  defaultPickerValue: r,
  pickerValue: t,
  presets: l,
  presetItems: i,
  showTime: c,
  onChange: w,
  minDate: u,
  maxDate: d,
  cellRender: a,
  panelRender: _,
  getPopupContainer: h,
  onValueChange: x,
  onPanelChange: g,
  onCalendarChange: y,
  children: S,
  setSlotParams: k,
  elRef: f,
  ...b
}) => {
  const oe = C(n), le = C(h), se = C(a), ce = C(_), ie = R(() => {
    var p;
    return typeof c == "object" ? {
      ...c,
      defaultValue: (p = c.defaultValue) == null ? void 0 : p.map((E) => I(E))
    } : c;
  }, [c]), ae = R(() => o == null ? void 0 : o.map((p) => I(p)), [o]), ue = R(() => s == null ? void 0 : s.map((p) => I(p)), [s]), fe = R(() => Array.isArray(r) ? r.map((p) => I(p)) : r ? I(r) : void 0, [r]), de = R(() => Array.isArray(t) ? t.map((p) => I(p)) : t ? I(t) : void 0, [t]), pe = R(() => u ? I(u) : void 0, [u]), _e = R(() => d ? I(d) : void 0, [d]);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: S
    }), /* @__PURE__ */ m.jsx(xe.RangePicker, {
      ...b,
      ref: f,
      value: ae,
      defaultValue: ue,
      defaultPickerValue: fe,
      pickerValue: de,
      minDate: pe,
      maxDate: _e,
      showTime: ie,
      disabledDate: oe,
      getPopupContainer: le,
      cellRender: e.cellRender ? M({
        slots: e,
        setSlotParams: k,
        key: "cellRender"
      }) : se,
      panelRender: e.panelRender ? M({
        slots: e,
        setSlotParams: k,
        key: "panelRender"
      }) : ce,
      presets: R(() => {
        var p;
        return (p = l || re(i)) == null ? void 0 : p.map((E) => ({
          ...E,
          value: D(E.value)
        }));
      }, [l, i]),
      onPanelChange: (p, ...E) => {
        const O = D(p);
        g == null || g(O, ...E);
      },
      onChange: (p, ...E) => {
        const O = D(p);
        w == null || w(O, ...E), x(O);
      },
      onCalendarChange: (p, ...E) => {
        const O = D(p);
        y == null || y(O, ...E);
      },
      renderExtraFooter: e.renderExtraFooter ? M({
        slots: e,
        setSlotParams: k,
        key: "renderExtraFooter"
      }) : b.renderExtraFooter,
      prefix: e.prefix ? /* @__PURE__ */ m.jsx(v, {
        slot: e.prefix
      }) : b.prefix,
      prevIcon: e.prevIcon ? /* @__PURE__ */ m.jsx(v, {
        slot: e.prevIcon
      }) : b.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ m.jsx(v, {
        slot: e.nextIcon
      }) : b.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(v, {
        slot: e.suffixIcon
      }) : b.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ m.jsx(v, {
        slot: e.superNextIcon
      }) : b.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ m.jsx(v, {
        slot: e.superPrevIcon
      }) : b.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(v, {
          slot: e["allowClear.clearIcon"]
        })
      } : b.allowClear,
      separator: e.separator ? /* @__PURE__ */ m.jsx(v, {
        slot: e.separator,
        clone: !0
      }) : b.separator
    })]
  });
});
export {
  et as DateRangePicker,
  et as default
};
