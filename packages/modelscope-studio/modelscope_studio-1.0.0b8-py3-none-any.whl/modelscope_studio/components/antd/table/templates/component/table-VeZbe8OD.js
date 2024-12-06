import { g as Oe, w as L } from "./Index-KJgNJooW.js";
const E = window.ms_globals.React, Ce = window.ms_globals.React.forwardRef, be = window.ms_globals.React.useRef, ye = window.ms_globals.React.useState, Ee = window.ms_globals.React.useEffect, I = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, k = window.ms_globals.antd.Table;
var Z = {
  exports: {}
}, M = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ve = E, Re = Symbol.for("react.element"), Se = Symbol.for("react.fragment"), ke = Object.prototype.hasOwnProperty, xe = ve.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(t, e, r) {
  var i, o = {}, n = null, l = null;
  r !== void 0 && (n = "" + r), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (i in e) ke.call(e, i) && !Ne.hasOwnProperty(i) && (o[i] = e[i]);
  if (t && t.defaultProps) for (i in e = t.defaultProps, e) o[i] === void 0 && (o[i] = e[i]);
  return {
    $$typeof: Re,
    type: t,
    key: n,
    ref: l,
    props: o,
    _owner: xe.current
  };
}
M.Fragment = Se;
M.jsx = $;
M.jsxs = $;
Z.exports = M;
var w = Z.exports;
const {
  SvelteComponent: Pe,
  assign: H,
  binding_callbacks: Q,
  check_outros: Te,
  children: ee,
  claim_element: te,
  claim_space: Ie,
  component_subscribe: z,
  compute_slots: Le,
  create_slot: je,
  detach: S,
  element: ne,
  empty: X,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Fe,
  get_slot_changes: Ae,
  group_outros: Me,
  init: Ue,
  insert_hydration: j,
  safe_not_equal: De,
  set_custom_element_data: re,
  space: We,
  transition_in: F,
  transition_out: B,
  update_slot_base: Be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ge,
  getContext: Je,
  onDestroy: He,
  setContext: Qe
} = window.__gradio__svelte__internal;
function V(t) {
  let e, r;
  const i = (
    /*#slots*/
    t[7].default
  ), o = je(
    i,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = ne("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = te(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = ee(e);
      o && o.l(l), l.forEach(S), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      j(n, e, l), o && o.m(e, null), t[9](e), r = !0;
    },
    p(n, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && Be(
        o,
        i,
        n,
        /*$$scope*/
        n[6],
        r ? Ae(
          i,
          /*$$scope*/
          n[6],
          l,
          null
        ) : Fe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (F(o, n), r = !0);
    },
    o(n) {
      B(o, n), r = !1;
    },
    d(n) {
      n && S(e), o && o.d(n), t[9](null);
    }
  };
}
function ze(t) {
  let e, r, i, o, n = (
    /*$$slots*/
    t[4].default && V(t)
  );
  return {
    c() {
      e = ne("react-portal-target"), r = We(), n && n.c(), i = X(), this.h();
    },
    l(l) {
      e = te(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), ee(e).forEach(S), r = Ie(l), n && n.l(l), i = X(), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(l, s) {
      j(l, e, s), t[8](e), j(l, r, s), n && n.m(l, s), j(l, i, s), o = !0;
    },
    p(l, [s]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, s), s & /*$$slots*/
      16 && F(n, 1)) : (n = V(l), n.c(), F(n, 1), n.m(i.parentNode, i)) : n && (Me(), B(n, 1, 1, () => {
        n = null;
      }), Te());
    },
    i(l) {
      o || (F(n), o = !0);
    },
    o(l) {
      B(n), o = !1;
    },
    d(l) {
      l && (S(e), S(r), S(i)), t[8](null), n && n.d(l);
    }
  };
}
function K(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function Xe(t, e, r) {
  let i, o, {
    $$slots: n = {},
    $$scope: l
  } = e;
  const s = Le(n);
  let {
    svelteInit: c
  } = e;
  const C = L(K(e)), u = L();
  z(t, u, (f) => r(0, i = f));
  const d = L();
  z(t, d, (f) => r(1, o = f));
  const a = [], p = Je("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: b,
    subSlotIndex: g
  } = Oe() || {}, y = c({
    parent: p,
    props: C,
    target: u,
    slot: d,
    slotKey: _,
    slotIndex: b,
    subSlotIndex: g,
    onDestroy(f) {
      a.push(f);
    }
  });
  Qe("$$ms-gr-react-wrapper", y), Ge(() => {
    C.set(K(e));
  }), He(() => {
    a.forEach((f) => f());
  });
  function v(f) {
    Q[f ? "unshift" : "push"](() => {
      i = f, u.set(i);
    });
  }
  function R(f) {
    Q[f ? "unshift" : "push"](() => {
      o = f, d.set(o);
    });
  }
  return t.$$set = (f) => {
    r(17, e = H(H({}, e), q(f))), "svelteInit" in f && r(5, c = f.svelteInit), "$$scope" in f && r(6, l = f.$$scope);
  }, e = q(e), [i, o, u, d, s, c, l, n, v, R];
}
class qe extends Pe {
  constructor(e) {
    super(), Ue(this, e, Xe, ze, De, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, D = window.ms_globals.tree;
function Ve(t) {
  function e(r) {
    const i = L(), o = new qe({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: i,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, s = n.parent ?? D;
          return s.nodes = [...s.nodes, l], Y({
            createPortal: W,
            node: D
          }), n.onDestroy(() => {
            s.nodes = s.nodes.filter((c) => c.svelteInstance !== i), Y({
              createPortal: W,
              node: D
            });
          }), l;
        },
        ...r.props
      }
    });
    return i.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const Ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ye(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const i = t[r];
    return typeof i == "number" && !Ke.includes(r) ? e[r] = i + "px" : e[r] = i, e;
  }, {}) : {};
}
function G(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(W(E.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: E.Children.toArray(t._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = G(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...E.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: l,
      type: s,
      useCapture: c
    }) => {
      r.addEventListener(s, l, c);
    });
  });
  const i = Array.from(t.childNodes);
  for (let o = 0; o < i.length; o++) {
    const n = i[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: s
      } = G(n);
      e.push(...s), r.appendChild(l);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Ze(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const O = Ce(({
  slot: t,
  clone: e,
  className: r,
  style: i
}, o) => {
  const n = be(), [l, s] = ye([]);
  return Ee(() => {
    var d;
    if (!n.current || !t)
      return;
    let c = t;
    function C() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ze(o, a), r && a.classList.add(...r.split(" ")), i) {
        const p = Ye(i);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var g, y, v;
        (g = n.current) != null && g.contains(c) && ((y = n.current) == null || y.removeChild(c));
        const {
          portals: _,
          clonedElement: b
        } = G(t);
        return c = b, s(_), c.style.display = "contents", C(), (v = n.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", C(), (d = n.current) == null || d.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = n.current) != null && a.contains(c) && ((p = n.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [t, e, r, i, o]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function $e(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function et(t, e = !1) {
  try {
    if (e && !$e(t))
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
function m(t, e) {
  return I(() => et(t, e), [t, e]);
}
function tt(t) {
  return Object.keys(t).reduce((e, r) => (t[r] !== void 0 && (e[r] = t[r]), e), {});
}
function A(t, e, r) {
  const i = t.filter(Boolean);
  if (i.length !== 0)
    return i.map((o, n) => {
      var C;
      if (typeof o != "object")
        return e != null && e.fallback ? e.fallback(o) : o;
      const l = {
        ...o.props,
        key: ((C = o.props) == null ? void 0 : C.key) ?? (r ? `${r}-${n}` : `${n}`)
      };
      let s = l;
      Object.keys(o.slots).forEach((u) => {
        if (!o.slots[u] || !(o.slots[u] instanceof Element) && !o.slots[u].el)
          return;
        const d = u.split(".");
        d.forEach((g, y) => {
          s[g] || (s[g] = {}), y !== d.length - 1 && (s = l[g]);
        });
        const a = o.slots[u];
        let p, _, b = (e == null ? void 0 : e.clone) ?? !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, b = a.clone ?? b), s[d[d.length - 1]] = p ? _ ? (...g) => (_(d[d.length - 1], g), /* @__PURE__ */ w.jsx(O, {
          slot: p,
          clone: b
        })) : /* @__PURE__ */ w.jsx(O, {
          slot: p,
          clone: b
        }) : s[d[d.length - 1]], s = l;
      });
      const c = (e == null ? void 0 : e.children) || "children";
      return o[c] && (l[c] = A(o[c], e, `${n}`)), l;
    });
}
function nt(t, e) {
  return t ? /* @__PURE__ */ w.jsx(O, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function P({
  key: t,
  setSlotParams: e,
  slots: r
}, i) {
  return r[t] ? (...o) => (e(t, o), nt(r[t], {
    clone: !0,
    ...i
  })) : void 0;
}
function T(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const ot = Ve(({
  children: t,
  slots: e,
  columnItems: r,
  columns: i,
  getPopupContainer: o,
  pagination: n,
  loading: l,
  rowKey: s,
  rowClassName: c,
  summary: C,
  rowSelection: u,
  rowSelectionItems: d,
  expandableItems: a,
  expandable: p,
  sticky: _,
  footer: b,
  showSorterTooltip: g,
  onRow: y,
  onHeaderRow: v,
  setSlotParams: R,
  ...f
}) => {
  const oe = m(o), le = e["loading.tip"] || e["loading.indicator"], U = T(l), ie = e["pagination.showQuickJumper.goButton"] || e["pagination.itemRender"], x = T(n), se = m(x.showTotal), ce = m(c), ae = m(s), ue = e["showSorterTooltip.title"] || typeof g == "object", N = T(g), fe = m(N.afterOpenChange), de = m(N.getPopupContainer), pe = typeof _ == "object", J = T(_), _e = m(J.getContainer), ge = m(y), he = m(v), me = m(C), we = m(b);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ w.jsx(k, {
      ...f,
      columns: I(() => (i == null ? void 0 : i.map((h) => h === "EXPAND_COLUMN" ? k.EXPAND_COLUMN : h === "SELECTION_COLUMN" ? k.SELECTION_COLUMN : h)) || A(r, {
        fallback: (h) => h === "EXPAND_COLUMN" ? k.EXPAND_COLUMN : h === "SELECTION_COLUMN" ? k.SELECTION_COLUMN : h
      }), [r, i]),
      onRow: ge,
      onHeaderRow: he,
      summary: e.summary ? P({
        slots: e,
        setSlotParams: R,
        key: "summary"
      }) : me,
      rowSelection: I(() => {
        var h;
        return u || ((h = A(d)) == null ? void 0 : h[0]);
      }, [u, d]),
      expandable: I(() => {
        var h;
        return p || ((h = A(a)) == null ? void 0 : h[0]);
      }, [p, a]),
      rowClassName: ce,
      rowKey: ae || s,
      sticky: pe ? {
        ...J,
        getContainer: _e
      } : _,
      showSorterTooltip: ue ? {
        ...N,
        afterOpenChange: fe,
        getPopupContainer: de,
        title: e["showSorterTooltip.title"] ? /* @__PURE__ */ w.jsx(O, {
          slot: e["showSorterTooltip.title"]
        }) : N.title
      } : g,
      pagination: ie ? tt({
        ...x,
        showTotal: se,
        showQuickJumper: e["pagination.showQuickJumper.goButton"] ? {
          goButton: /* @__PURE__ */ w.jsx(O, {
            slot: e["pagination.showQuickJumper.goButton"]
          })
        } : x.showQuickJumper,
        itemRender: e["pagination.itemRender"] ? P({
          slots: e,
          setSlotParams: R,
          key: "pagination.itemRender"
        }) : x.itemRender
      }) : n,
      getPopupContainer: oe,
      loading: le ? {
        ...U,
        tip: e["loading.tip"] ? /* @__PURE__ */ w.jsx(O, {
          slot: e["loading.tip"]
        }) : U.tip,
        indicator: e["loading.indicator"] ? /* @__PURE__ */ w.jsx(O, {
          slot: e["loading.indicator"]
        }) : U.indicator
      } : l,
      footer: e.footer ? P({
        slots: e,
        setSlotParams: R,
        key: "footer"
      }) : we,
      title: e.title ? P({
        slots: e,
        setSlotParams: R,
        key: "title"
      }) : f.title
    })]
  });
});
export {
  ot as Table,
  ot as default
};
