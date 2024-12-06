import { g as he, w as k } from "./Index-Dsf7LUdf.js";
const E = window.ms_globals.React, fe = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, _e = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, b = window.ms_globals.React.useMemo, L = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.TimePicker, z = window.ms_globals.dayjs;
var Q = {
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
var ve = E, ye = Symbol.for("react.element"), ge = Symbol.for("react.fragment"), be = Object.prototype.hasOwnProperty, xe = ve.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function X(e, t, r) {
  var l, o = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) be.call(t, l) && !Ee.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ye,
    type: e,
    key: n,
    ref: s,
    props: o,
    _owner: xe.current
  };
}
D.Fragment = ge;
D.jsx = X;
D.jsxs = X;
Q.exports = D;
var p = Q.exports;
const {
  SvelteComponent: Ie,
  assign: G,
  binding_callbacks: U,
  check_outros: Re,
  children: Z,
  claim_element: $,
  claim_space: Se,
  component_subscribe: H,
  compute_slots: Pe,
  create_slot: Ce,
  detach: P,
  element: ee,
  empty: K,
  exclude_internal_props: V,
  get_all_dirty_from_scope: je,
  get_slot_changes: Oe,
  group_outros: ke,
  init: Fe,
  insert_hydration: F,
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
function q(e) {
  let t, r;
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
      t = ee("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = $(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = Z(t);
      o && o.l(s), s.forEach(P), this.h();
    },
    h() {
      te(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      F(n, t, s), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ne(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? Oe(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : je(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (T(o, n), r = !0);
    },
    o(n) {
      M(o, n), r = !1;
    },
    d(n) {
      n && P(t), o && o.d(n), e[9](null);
    }
  };
}
function ze(e) {
  let t, r, l, o, n = (
    /*$$slots*/
    e[4].default && q(e)
  );
  return {
    c() {
      t = ee("react-portal-target"), r = De(), n && n.c(), l = K(), this.h();
    },
    l(s) {
      t = $(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Z(t).forEach(P), r = Se(s), n && n.l(s), l = K(), this.h();
    },
    h() {
      te(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      F(s, t, c), e[8](t), F(s, r, c), n && n.m(s, c), F(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && T(n, 1)) : (n = q(s), n.c(), T(n, 1), n.m(l.parentNode, l)) : n && (ke(), M(n, 1, 1, () => {
        n = null;
      }), Re());
    },
    i(s) {
      o || (T(n), o = !0);
    },
    o(s) {
      M(n), o = !1;
    },
    d(s) {
      s && (P(t), P(r), P(l)), e[8](null), n && n.d(s);
    }
  };
}
function B(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ge(e, t, r) {
  let l, o, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = Pe(n);
  let {
    svelteInit: i
  } = t;
  const h = k(B(t)), d = k();
  H(e, d, (a) => r(0, l = a));
  const w = k();
  H(e, w, (a) => r(1, o = a));
  const u = [], _ = Le("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: y,
    subSlotIndex: I
  } = he() || {}, g = i({
    parent: _,
    props: h,
    target: d,
    slot: w,
    slotKey: f,
    slotIndex: y,
    subSlotIndex: I,
    onDestroy(a) {
      u.push(a);
    }
  });
  We("$$ms-gr-react-wrapper", g), Ae(() => {
    h.set(B(t));
  }), Me(() => {
    u.forEach((a) => a());
  });
  function R(a) {
    U[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function m(a) {
    U[a ? "unshift" : "push"](() => {
      o = a, w.set(o);
    });
  }
  return e.$$set = (a) => {
    r(17, t = G(G({}, t), V(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = V(t), [l, o, d, w, c, i, s, n, R, m];
}
class Ue extends Ie {
  constructor(t) {
    super(), Fe(this, t, Ge, ze, Te, {
      svelteInit: 5
    });
  }
}
const J = window.ms_globals.rerender, N = window.ms_globals.tree;
function He(e) {
  function t(r) {
    const l = k(), o = new Ue({
      ...r,
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
          }, c = n.parent ?? N;
          return c.nodes = [...c.nodes, s], J({
            createPortal: L,
            node: N
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), J({
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
      r(t);
    });
  });
}
const Ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ve(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const l = e[r];
    return typeof l == "number" && !Ke.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function W(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(L(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = W(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...E.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
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
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = W(n);
      t.push(...c), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function qe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const v = fe(({
  slot: e,
  clone: t,
  className: r,
  style: l
}, o) => {
  const n = pe(), [s, c] = _e([]);
  return me(() => {
    var w;
    if (!n.current || !e)
      return;
    let i = e;
    function h() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), qe(o, u), r && u.classList.add(...r.split(" ")), l) {
        const _ = Ve(l);
        Object.keys(_).forEach((f) => {
          u.style[f] = _[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var I, g, R;
        (I = n.current) != null && I.contains(i) && ((g = n.current) == null || g.removeChild(i));
        const {
          portals: f,
          clonedElement: y
        } = W(e);
        return i = y, c(f), i.style.display = "contents", h(), (R = n.current) == null || R.appendChild(i), f.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (w = n.current) == null || w.appendChild(i);
    return () => {
      var u, _;
      i.style.display = "", (u = n.current) != null && u.contains(i) && ((_ = n.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, t, r, l, o]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Be(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Je(e, t = !1) {
  try {
    if (t && !Be(e))
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
function O(e, t) {
  return b(() => Je(e, t), [e, t]);
}
function Ye(e, t) {
  return e ? /* @__PURE__ */ p.jsx(v, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Y({
  key: e,
  setSlotParams: t,
  slots: r
}, l) {
  return r[e] ? (...o) => (t(e, o), Ye(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
function x(e) {
  return Array.isArray(e) ? e.map((t) => x(t)) : z(typeof e == "number" ? e * 1e3 : e);
}
function A(e) {
  return Array.isArray(e) ? e.map((t) => t ? t.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const Xe = He(({
  slots: e,
  disabledDate: t,
  disabledTime: r,
  value: l,
  defaultValue: o,
  defaultPickerValue: n,
  pickerValue: s,
  onChange: c,
  minDate: i,
  maxDate: h,
  cellRender: d,
  panelRender: w,
  getPopupContainer: u,
  onValueChange: _,
  onPanelChange: f,
  onCalendarChange: y,
  children: I,
  setSlotParams: g,
  elRef: R,
  ...m
}) => {
  const a = O(t), ne = O(r), re = O(u), oe = O(d), le = O(w), se = b(() => l ? x(l) : void 0, [l]), ie = b(() => o ? x(o) : void 0, [o]), ce = b(() => n ? x(n) : void 0, [n]), ae = b(() => s ? x(s) : void 0, [s]), ue = b(() => i ? x(i) : void 0, [i]), de = b(() => h ? x(h) : void 0, [h]);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: I
    }), /* @__PURE__ */ p.jsx(we, {
      ...m,
      ref: R,
      value: se,
      defaultValue: ie,
      defaultPickerValue: ce,
      pickerValue: ae,
      minDate: ue,
      maxDate: de,
      disabledTime: ne,
      disabledDate: a,
      getPopupContainer: re,
      cellRender: e.cellRender ? Y({
        slots: e,
        setSlotParams: g,
        key: "cellRender"
      }) : oe,
      panelRender: e.panelRender ? Y({
        slots: e,
        setSlotParams: g,
        key: "panelRender"
      }) : le,
      onPanelChange: (C, ...j) => {
        const S = A(C);
        f == null || f(S, ...j);
      },
      onChange: (C, ...j) => {
        const S = A(C);
        c == null || c(S, ...j), _(S);
      },
      onCalendarChange: (C, ...j) => {
        const S = A(C);
        y == null || y(S, ...j);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ p.jsx(v, {
        slot: e.renderExtraFooter
      }) : null : m.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ p.jsx(v, {
        slot: e.prevIcon
      }) : m.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ p.jsx(v, {
        slot: e.nextIcon
      }) : m.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ p.jsx(v, {
        slot: e.suffixIcon
      }) : m.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ p.jsx(v, {
        slot: e.superNextIcon
      }) : m.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ p.jsx(v, {
        slot: e.superPrevIcon
      }) : m.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(v, {
          slot: e["allowClear.clearIcon"]
        })
      } : m.allowClear
    })]
  });
});
export {
  Xe as TimePicker,
  Xe as default
};
