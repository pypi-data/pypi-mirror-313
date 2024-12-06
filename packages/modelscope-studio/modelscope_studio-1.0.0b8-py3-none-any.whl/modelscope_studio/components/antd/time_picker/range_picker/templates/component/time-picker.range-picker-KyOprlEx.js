import { g as he, w as F } from "./Index-DD5mGIoJ.js";
const I = window.ms_globals.React, fe = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, me = window.ms_globals.React.useState, _e = window.ms_globals.React.useEffect, E = window.ms_globals.React.useMemo, L = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.TimePicker, z = window.ms_globals.dayjs;
var X = {
  exports: {}
}, D = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ge = I, ye = Symbol.for("react.element"), ve = Symbol.for("react.fragment"), xe = Object.prototype.hasOwnProperty, be = ge.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, n, r) {
  var l, o = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) xe.call(n, l) && !Ee.hasOwnProperty(l) && (o[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ye,
    type: e,
    key: t,
    ref: s,
    props: o,
    _owner: be.current
  };
}
D.Fragment = ve;
D.jsx = Z;
D.jsxs = Z;
X.exports = D;
var p = X.exports;
const {
  SvelteComponent: Ie,
  assign: G,
  binding_callbacks: U,
  check_outros: Re,
  children: V,
  claim_element: $,
  claim_space: Se,
  component_subscribe: H,
  compute_slots: Pe,
  create_slot: Ce,
  detach: C,
  element: ee,
  empty: K,
  exclude_internal_props: q,
  get_all_dirty_from_scope: je,
  get_slot_changes: Oe,
  group_outros: Fe,
  init: ke,
  insert_hydration: k,
  safe_not_equal: Te,
  set_custom_element_data: te,
  space: De,
  transition_in: T,
  transition_out: M,
  update_slot_base: Ne
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ae,
  getContext: Le,
  onDestroy: Me,
  setContext: We
} = window.__gradio__svelte__internal;
function B(e) {
  let n, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = Ce(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = ee("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = $(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = V(n);
      o && o.l(s), s.forEach(C), this.h();
    },
    h() {
      te(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      k(t, n, s), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ne(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? Oe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : je(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (T(o, t), r = !0);
    },
    o(t) {
      M(o, t), r = !1;
    },
    d(t) {
      t && C(n), o && o.d(t), e[9](null);
    }
  };
}
function ze(e) {
  let n, r, l, o, t = (
    /*$$slots*/
    e[4].default && B(e)
  );
  return {
    c() {
      n = ee("react-portal-target"), r = De(), t && t.c(), l = K(), this.h();
    },
    l(s) {
      n = $(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), V(n).forEach(C), r = Se(s), t && t.l(s), l = K(), this.h();
    },
    h() {
      te(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      k(s, n, c), e[8](n), k(s, r, c), t && t.m(s, c), k(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && T(t, 1)) : (t = B(s), t.c(), T(t, 1), t.m(l.parentNode, l)) : t && (Fe(), M(t, 1, 1, () => {
        t = null;
      }), Re());
    },
    i(s) {
      o || (T(t), o = !0);
    },
    o(s) {
      M(t), o = !1;
    },
    d(s) {
      s && (C(n), C(r), C(l)), e[8](null), t && t.d(s);
    }
  };
}
function J(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ge(e, n, r) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = Pe(t);
  let {
    svelteInit: i
  } = n;
  const w = F(J(n)), d = F();
  H(e, d, (a) => r(0, l = a));
  const g = F();
  H(e, g, (a) => r(1, o = a));
  const u = [], h = Le("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: x,
    subSlotIndex: R
  } = he() || {}, b = i({
    parent: h,
    props: w,
    target: d,
    slot: g,
    slotKey: m,
    slotIndex: x,
    subSlotIndex: R,
    onDestroy(a) {
      u.push(a);
    }
  });
  We("$$ms-gr-react-wrapper", b), Ae(() => {
    w.set(J(n));
  }), Me(() => {
    u.forEach((a) => a());
  });
  function S(a) {
    U[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function _(a) {
    U[a ? "unshift" : "push"](() => {
      o = a, g.set(o);
    });
  }
  return e.$$set = (a) => {
    r(17, n = G(G({}, n), q(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, n = q(n), [l, o, d, g, c, i, s, t, S, _];
}
class Ue extends Ie {
  constructor(n) {
    super(), ke(this, n, Ge, ze, Te, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, N = window.ms_globals.tree;
function He(e) {
  function n(r) {
    const l = F(), o = new Ue({
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
          }, c = t.parent ?? N;
          return c.nodes = [...c.nodes, s], Y({
            createPortal: L,
            node: N
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), Y({
              createPortal: L,
              node: N
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
const Ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function qe(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !Ke.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function W(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(L(I.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: I.Children.toArray(e._reactElement.props.children).map((o) => {
        if (I.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = W(o.props.el);
          return I.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...I.Children.toArray(o.props.children), ...t]
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
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = W(t);
      n.push(...c), r.appendChild(s);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Be(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const y = fe(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, o) => {
  const t = pe(), [s, c] = me([]);
  return _e(() => {
    var g;
    if (!t.current || !e)
      return;
    let i = e;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Be(o, u), r && u.classList.add(...r.split(" ")), l) {
        const h = qe(l);
        Object.keys(h).forEach((m) => {
          u.style[m] = h[m];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var R, b, S;
        (R = t.current) != null && R.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: m,
          clonedElement: x
        } = W(e);
        return i = x, c(m), i.style.display = "contents", w(), (S = t.current) == null || S.appendChild(i), m.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (g = t.current) == null || g.appendChild(i);
    return () => {
      var u, h;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((h = t.current) == null || h.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, n, r, l, o]), I.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Je(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ye(e, n = !1) {
  try {
    if (n && !Je(e))
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
function O(e, n) {
  return E(() => Ye(e, n), [e, n]);
}
function Qe(e, n) {
  return e ? /* @__PURE__ */ p.jsx(y, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Q({
  key: e,
  setSlotParams: n,
  slots: r
}, l) {
  return r[e] ? (...o) => (n(e, o), Qe(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function v(e) {
  return z(typeof e == "number" ? e * 1e3 : e);
}
function A(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
}
const Ze = He(({
  slots: e,
  disabledDate: n,
  disabledTime: r,
  value: l,
  defaultValue: o,
  defaultPickerValue: t,
  pickerValue: s,
  onChange: c,
  minDate: i,
  maxDate: w,
  cellRender: d,
  panelRender: g,
  getPopupContainer: u,
  onValueChange: h,
  onPanelChange: m,
  onCalendarChange: x,
  children: R,
  setSlotParams: b,
  elRef: S,
  ..._
}) => {
  const a = O(n), ne = O(u), re = O(d), oe = O(g), se = O(r), le = E(() => l == null ? void 0 : l.map((f) => v(f)), [l]), ie = E(() => o == null ? void 0 : o.map((f) => v(f)), [o]), ce = E(() => Array.isArray(t) ? t.map((f) => v(f)) : t ? v(t) : void 0, [t]), ae = E(() => Array.isArray(s) ? s.map((f) => v(f)) : s ? v(s) : void 0, [s]), ue = E(() => i ? v(i) : void 0, [i]), de = E(() => w ? v(w) : void 0, [w]);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: R
    }), /* @__PURE__ */ p.jsx(we.RangePicker, {
      ..._,
      ref: S,
      value: le,
      disabledTime: se,
      defaultValue: ie,
      defaultPickerValue: ce,
      pickerValue: ae,
      minDate: ue,
      maxDate: de,
      disabledDate: a,
      getPopupContainer: ne,
      cellRender: e.cellRender ? Q({
        slots: e,
        setSlotParams: b,
        key: "cellRender"
      }) : re,
      panelRender: e.panelRender ? Q({
        slots: e,
        setSlotParams: b,
        key: "panelRender"
      }) : oe,
      onPanelChange: (f, ...j) => {
        const P = A(f);
        m == null || m(P, ...j);
      },
      onChange: (f, ...j) => {
        const P = A(f);
        c == null || c(P, ...j), h(P);
      },
      onCalendarChange: (f, ...j) => {
        const P = A(f);
        x == null || x(P, ...j);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ p.jsx(y, {
        slot: e.renderExtraFooter
      }) : null : _.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.prevIcon
      }) : _.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.nextIcon
      }) : _.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.suffixIcon
      }) : _.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.superNextIcon
      }) : _.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ p.jsx(y, {
        slot: e.superPrevIcon
      }) : _.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : _.allowClear,
      separator: e.separator ? /* @__PURE__ */ p.jsx(y, {
        slot: e.separator
      }) : _.separator
    })]
  });
});
export {
  Ze as TimeRangePicker,
  Ze as default
};
