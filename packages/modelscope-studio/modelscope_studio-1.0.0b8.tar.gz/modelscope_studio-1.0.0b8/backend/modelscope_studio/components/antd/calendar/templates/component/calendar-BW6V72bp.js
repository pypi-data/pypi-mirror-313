import { g as re, w as O } from "./Index-CT2-emui.js";
const w = window.ms_globals.React, x = window.ms_globals.React.useMemo, $ = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, ne = window.ms_globals.React.useEffect, A = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Calendar, N = window.ms_globals.dayjs;
var q = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var le = w, se = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ae = le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ce.call(t, l) && !ue.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: se,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
k.Fragment = ie;
k.jsx = B;
k.jsxs = B;
q.exports = k;
var J = q.exports;
const {
  SvelteComponent: de,
  assign: W,
  binding_callbacks: M,
  check_outros: fe,
  children: Y,
  claim_element: Q,
  claim_space: _e,
  component_subscribe: z,
  compute_slots: pe,
  create_slot: me,
  detach: v,
  element: X,
  empty: G,
  exclude_internal_props: U,
  get_all_dirty_from_scope: he,
  get_slot_changes: we,
  group_outros: ge,
  init: ye,
  insert_hydration: I,
  safe_not_equal: be,
  set_custom_element_data: Z,
  space: ve,
  transition_in: S,
  transition_out: T,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: Re,
  getContext: Ce,
  onDestroy: xe,
  setContext: Oe
} = window.__gradio__svelte__internal;
function V(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = me(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = X("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = Q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(t);
      o && o.l(s), s.forEach(v), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      I(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ee(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? we(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : he(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (S(o, e), r = !0);
    },
    o(e) {
      T(o, e), r = !1;
    },
    d(e) {
      e && v(t), o && o.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && V(n)
  );
  return {
    c() {
      t = X("react-portal-target"), r = ve(), e && e.c(), l = G(), this.h();
    },
    l(s) {
      t = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(t).forEach(v), r = _e(s), e && e.l(s), l = G(), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      I(s, t, a), n[8](t), I(s, r, a), e && e.m(s, a), I(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && S(e, 1)) : (e = V(s), e.c(), S(e, 1), e.m(l.parentNode, l)) : e && (ge(), T(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(s) {
      o || (S(e), o = !0);
    },
    o(s) {
      T(e), o = !1;
    },
    d(s) {
      s && (v(t), v(r), v(l)), n[8](null), e && e.d(s);
    }
  };
}
function H(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Se(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = pe(e);
  let {
    svelteInit: i
  } = t;
  const h = O(H(t)), d = O();
  z(n, d, (u) => r(0, l = u));
  const p = O();
  z(n, p, (u) => r(1, o = u));
  const c = [], f = Ce("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: E,
    subSlotIndex: g
  } = re() || {}, y = i({
    parent: f,
    props: h,
    target: d,
    slot: p,
    slotKey: _,
    slotIndex: E,
    subSlotIndex: g,
    onDestroy(u) {
      c.push(u);
    }
  });
  Oe("$$ms-gr-react-wrapper", y), Re(() => {
    h.set(H(t));
  }), xe(() => {
    c.forEach((u) => u());
  });
  function b(u) {
    M[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function P(u) {
    M[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return n.$$set = (u) => {
    r(17, t = W(W({}, t), U(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = U(t), [l, o, d, p, a, i, s, e, b, P];
}
class ke extends de {
  constructor(t) {
    super(), ye(this, t, Se, Ie, be, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, L = window.ms_globals.tree;
function Pe(n) {
  function t(r) {
    const l = O(), o = new ke({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, a = e.parent ?? L;
          return a.nodes = [...a.nodes, s], K({
            createPortal: A,
            node: L
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), K({
              createPortal: A,
              node: L
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
function Le(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function je(n, t = !1) {
  try {
    if (t && !Le(n))
      return;
    if (typeof n == "string") {
      let r = n.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function C(n, t) {
  return x(() => je(n, t), [n, t]);
}
const Fe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Fe.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function D(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(A(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = D(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...w.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = D(e);
      t.push(...a), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Te(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const De = $(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = ee(), [s, a] = te([]);
  return ne(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function h() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Te(o, c), r && c.classList.add(...r.split(" ")), l) {
        const f = Ae(l);
        Object.keys(f).forEach((_) => {
          c.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var g, y, b;
        (g = e.current) != null && g.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: E
        } = D(n);
        return i = E, a(_), i.style.display = "contents", h(), (b = e.current) == null || b.appendChild(i), _.length > 0;
      };
      c() || (d = new window.MutationObserver(() => {
        c() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var c, f;
      i.style.display = "", (c = e.current) != null && c.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, r, l, o]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(n, t) {
  return n ? /* @__PURE__ */ J.jsx(De, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function j({
  key: n,
  setSlotParams: t,
  slots: r
}, l) {
  return r[n] ? (...o) => (t(n, o), Ne(r[n], {
    clone: !0,
    ...l
  })) : void 0;
}
function F(n) {
  return N(typeof n == "number" ? n * 1e3 : n);
}
const Me = Pe(({
  disabledDate: n,
  value: t,
  defaultValue: r,
  validRange: l,
  onChange: o,
  onPanelChange: e,
  onSelect: s,
  onValueChange: a,
  setSlotParams: i,
  cellRender: h,
  fullCellRender: d,
  headerRender: p,
  slots: c,
  ...f
}) => {
  const _ = C(n), E = C(h), g = C(d), y = C(p), b = x(() => t ? F(t) : void 0, [t]), P = x(() => r ? F(r) : void 0, [r]), u = x(() => Array.isArray(l) ? l.map((m) => F(m)) : void 0, [l]);
  return /* @__PURE__ */ J.jsx(oe, {
    ...f,
    value: b,
    defaultValue: P,
    validRange: u,
    disabledDate: _,
    cellRender: c.cellRender ? j({
      slots: c,
      setSlotParams: i,
      key: "cellRender"
    }) : E,
    fullCellRender: c.fullCellRender ? j({
      slots: c,
      setSlotParams: i,
      key: "fullCellRender"
    }) : g,
    headerRender: c.headerRender ? j({
      slots: c,
      setSlotParams: i,
      key: "headerRender"
    }) : y,
    onChange: (m, ...R) => {
      a(m.valueOf() / 1e3), o == null || o(m.valueOf() / 1e3, ...R);
    },
    onPanelChange: (m, ...R) => {
      e == null || e(m.valueOf() / 1e3, ...R);
    },
    onSelect: (m, ...R) => {
      s == null || s(m.valueOf() / 1e3, ...R);
    }
  });
});
export {
  Me as Calendar,
  Me as default
};
