import { g as ne, w as C, d as re, a as x } from "./Index-sMjhaKXY.js";
const b = window.ms_globals.React, A = window.ms_globals.React.useMemo, q = window.ms_globals.React.useState, B = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, L = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Transfer;
var J = {
  exports: {}
}, P = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = b, le = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ae = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function K(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) ce.call(n, l) && !ue.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: le,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
P.Fragment = ie;
P.jsx = K;
P.jsxs = K;
J.exports = P;
var g = J.exports;
const {
  SvelteComponent: de,
  assign: T,
  binding_callbacks: N,
  check_outros: fe,
  children: Y,
  claim_element: Q,
  claim_space: pe,
  component_subscribe: W,
  compute_slots: _e,
  create_slot: me,
  detach: v,
  element: X,
  empty: D,
  exclude_internal_props: M,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert_hydration: R,
  safe_not_equal: ye,
  set_custom_element_data: Z,
  space: ve,
  transition_in: O,
  transition_out: F,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ie,
  onDestroy: Se,
  setContext: Ce
} = window.__gradio__svelte__internal;
function z(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = me(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = X("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = Q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(n);
      o && o.l(s), s.forEach(v), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      R(e, n, s), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ee(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ge(
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
      r || (O(o, e), r = !0);
    },
    o(e) {
      F(o, e), r = !1;
    },
    d(e) {
      e && v(n), o && o.d(e), t[9](null);
    }
  };
}
function Re(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && z(t)
  );
  return {
    c() {
      n = X("react-portal-target"), r = ve(), e && e.c(), l = D(), this.h();
    },
    l(s) {
      n = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(n).forEach(v), r = pe(s), e && e.l(s), l = D(), this.h();
    },
    h() {
      Z(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      R(s, n, c), t[8](n), R(s, r, c), e && e.m(s, c), R(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && O(e, 1)) : (e = z(s), e.c(), O(e, 1), e.m(l.parentNode, l)) : e && (we(), F(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(s) {
      o || (O(e), o = !0);
    },
    o(s) {
      F(e), o = !1;
    },
    d(s) {
      s && (v(n), v(r), v(l)), t[8](null), e && e.d(s);
    }
  };
}
function G(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function Oe(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = _e(e);
  let {
    svelteInit: i
  } = n;
  const w = C(G(n)), d = C();
  W(t, d, (u) => r(0, l = u));
  const p = C();
  W(t, p, (u) => r(1, o = u));
  const a = [], _ = Ie("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: E,
    subSlotIndex: y
  } = ne() || {}, f = i({
    parent: _,
    props: w,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: E,
    subSlotIndex: y,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", f), xe(() => {
    w.set(G(n));
  }), Se(() => {
    a.forEach((u) => u());
  });
  function h(u) {
    N[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function $(u) {
    N[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return t.$$set = (u) => {
    r(17, n = T(T({}, n), M(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, n = M(n), [l, o, d, p, c, i, s, e, h, $];
}
class Pe extends de {
  constructor(n) {
    super(), be(this, n, Oe, Re, ye, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, k = window.ms_globals.tree;
function ke(t) {
  function n(r) {
    const l = C(), o = new Pe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, s], U({
            createPortal: L,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), U({
              createPortal: L,
              node: k
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
function Le(t) {
  const [n, r] = q(() => x(t));
  return B(() => {
    let l = !0;
    return t.subscribe((e) => {
      l && (l = !1, e === n) || r(e);
    });
  }, [t]), n;
}
function Fe(t) {
  const n = A(() => re(t, (r) => r), [t]);
  return Le(n);
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !je.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function j(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(L(b.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: b.Children.toArray(t._reactElement.props.children).map((o) => {
        if (b.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(o.props.el);
          return b.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...b.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(e);
      n.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Te(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const I = ee(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = te(), [s, c] = q([]);
  return B(() => {
    var p;
    if (!e.current || !t)
      return;
    let i = t;
    function w() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Te(o, a), r && a.classList.add(...r.split(" ")), l) {
        const _ = Ae(l);
        Object.keys(_).forEach((m) => {
          a.style[m] = _[m];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y, f, h;
        (y = e.current) != null && y.contains(i) && ((f = e.current) == null || f.removeChild(i));
        const {
          portals: m,
          clonedElement: E
        } = j(t);
        return i = E, c(m), i.style.display = "contents", w(), (h = e.current) == null || h.appendChild(i), m.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((_ = e.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, r, l, o]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function We(t, n = !1) {
  try {
    if (n && !Ne(t))
      return;
    if (typeof t == "string") {
      let r = t.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function S(t, n) {
  return A(() => We(t, n), [t, n]);
}
function H(t, n) {
  const r = A(() => b.Children.toArray(t).filter((e) => e.props.node && (!n && !e.props.nodeSlotKey || n && n === e.props.nodeSlotKey)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const c = x(e.props.node.slotIndex) || 0, i = x(s.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (x(e.props.node.subSlotIndex) || 0) - (x(s.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [t, n]);
  return Fe(r);
}
function De(t, n) {
  return t ? /* @__PURE__ */ g.jsx(I, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function V({
  key: t,
  setSlotParams: n,
  slots: r
}, l) {
  return r[t] ? (...o) => (n(t, o), De(r[t], {
    clone: !0,
    ...l
  })) : void 0;
}
const ze = ke(({
  slots: t,
  children: n,
  render: r,
  filterOption: l,
  footer: o,
  listStyle: e,
  locale: s,
  onChange: c,
  onValueChange: i,
  setSlotParams: w,
  ...d
}) => {
  const p = H(n, "titles"), a = H(n, "selectAllLabels"), _ = S(r), m = S(e), E = S(o), y = S(l);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ g.jsx(oe, {
      ...d,
      onChange: (f, ...h) => {
        c == null || c(f, ...h), i(f);
      },
      selectionsIcon: t.selectionsIcon ? /* @__PURE__ */ g.jsx(I, {
        slot: t.selectionsIcon
      }) : d.selectionsIcon,
      locale: t["locale.notFoundContent"] ? {
        ...s,
        notFoundContent: /* @__PURE__ */ g.jsx(I, {
          slot: t["locale.notFoundContent"]
        })
      } : s,
      render: t.render ? V({
        slots: t,
        setSlotParams: w,
        key: "render"
      }) : _ || ((f) => ({
        label: f.title || f.label,
        value: f.value || f.title || f.label
      })),
      filterOption: y,
      footer: t.footer ? V({
        slots: t,
        setSlotParams: w,
        key: "footer"
      }) : E || o,
      titles: p.length > 0 ? p.map((f, h) => /* @__PURE__ */ g.jsx(I, {
        slot: f
      }, h)) : d.titles,
      listStyle: m || e,
      selectAllLabels: a.length > 0 ? a.map((f, h) => /* @__PURE__ */ g.jsx(I, {
        slot: f
      }, h)) : d.selectAllLabels
    })]
  });
});
export {
  ze as Transfer,
  ze as default
};
