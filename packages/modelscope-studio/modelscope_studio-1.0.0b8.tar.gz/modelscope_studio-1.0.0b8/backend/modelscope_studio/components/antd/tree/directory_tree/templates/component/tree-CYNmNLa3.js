import { g as le, w as L } from "./Index-BA4Mzp0j.js";
const v = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, V = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Tree;
var J = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = v, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(e, t, r) {
  var l, o = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ae.call(t, l) && !de.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ce,
    type: e,
    key: n,
    ref: s,
    props: o,
    _owner: ue.current
  };
}
S.Fragment = ie;
S.jsx = Y;
S.jsxs = Y;
J.exports = S;
var b = J.exports;
const {
  SvelteComponent: fe,
  assign: W,
  binding_callbacks: M,
  check_outros: _e,
  children: K,
  claim_element: Q,
  claim_space: he,
  component_subscribe: U,
  compute_slots: me,
  create_slot: ge,
  detach: E,
  element: X,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: we,
  get_slot_changes: pe,
  group_outros: be,
  init: ye,
  insert_hydration: k,
  safe_not_equal: ve,
  set_custom_element_data: Z,
  space: Ee,
  transition_in: j,
  transition_out: N,
  update_slot_base: Ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: Re,
  getContext: xe,
  onDestroy: Ce,
  setContext: Oe
} = window.__gradio__svelte__internal;
function H(e) {
  let t, r;
  const l = (
    /*#slots*/
    e[7].default
  ), o = ge(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = X("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = Q(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(t);
      o && o.l(s), s.forEach(E), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      k(n, t, s), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ie(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? pe(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : we(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (j(o, n), r = !0);
    },
    o(n) {
      N(o, n), r = !1;
    },
    d(n) {
      n && E(t), o && o.d(n), e[9](null);
    }
  };
}
function Le(e) {
  let t, r, l, o, n = (
    /*$$slots*/
    e[4].default && H(e)
  );
  return {
    c() {
      t = X("react-portal-target"), r = Ee(), n && n.c(), l = z(), this.h();
    },
    l(s) {
      t = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(E), r = he(s), n && n.l(s), l = z(), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      k(s, t, c), e[8](t), k(s, r, c), n && n.m(s, c), k(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && j(n, 1)) : (n = H(s), n.c(), j(n, 1), n.m(l.parentNode, l)) : n && (be(), N(n, 1, 1, () => {
        n = null;
      }), _e());
    },
    i(s) {
      o || (j(n), o = !0);
    },
    o(s) {
      N(n), o = !1;
    },
    d(s) {
      s && (E(t), E(r), E(l)), e[8](null), n && n.d(s);
    }
  };
}
function q(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function ke(e, t, r) {
  let l, o, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = me(n);
  let {
    svelteInit: i
  } = t;
  const g = L(q(t)), u = L();
  U(e, u, (f) => r(0, l = f));
  const d = L();
  U(e, d, (f) => r(1, o = f));
  const a = [], h = xe("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: w,
    subSlotIndex: m
  } = le() || {}, p = i({
    parent: h,
    props: g,
    target: u,
    slot: d,
    slotKey: _,
    slotIndex: w,
    subSlotIndex: m,
    onDestroy(f) {
      a.push(f);
    }
  });
  Oe("$$ms-gr-react-wrapper", p), Re(() => {
    g.set(q(t));
  }), Ce(() => {
    a.forEach((f) => f());
  });
  function y(f) {
    M[f ? "unshift" : "push"](() => {
      l = f, u.set(l);
    });
  }
  function P(f) {
    M[f ? "unshift" : "push"](() => {
      o = f, d.set(o);
    });
  }
  return e.$$set = (f) => {
    r(17, t = W(W({}, t), G(f))), "svelteInit" in f && r(5, i = f.svelteInit), "$$scope" in f && r(6, s = f.$$scope);
  }, t = G(t), [l, o, u, d, c, i, s, n, y, P];
}
class je extends fe {
  constructor(t) {
    super(), ye(this, t, ke, Le, ve, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, T = window.ms_globals.tree;
function Se(e) {
  function t(r) {
    const l = L(), o = new je({
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
          }, c = n.parent ?? T;
          return c.nodes = [...c.nodes, s], B({
            createPortal: F,
            node: T
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), B({
              createPortal: F,
              node: T
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
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Te(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const l = e[r];
    return typeof l == "number" && !Pe.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function D(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(F(v.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: v.Children.toArray(e._reactElement.props.children).map((o) => {
        if (v.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = D(o.props.el);
          return v.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...v.Children.toArray(o.props.children), ...n]
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
      } = D(n);
      t.push(...c), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Fe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const C = te(({
  slot: e,
  clone: t,
  className: r,
  style: l
}, o) => {
  const n = ne(), [s, c] = re([]);
  return oe(() => {
    var d;
    if (!n.current || !e)
      return;
    let i = e;
    function g() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Fe(o, a), r && a.classList.add(...r.split(" ")), l) {
        const h = Te(l);
        Object.keys(h).forEach((_) => {
          a.style[_] = h[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var m, p, y;
        (m = n.current) != null && m.contains(i) && ((p = n.current) == null || p.removeChild(i));
        const {
          portals: _,
          clonedElement: w
        } = D(e);
        return i = w, c(_), i.style.display = "contents", g(), (y = n.current) == null || y.appendChild(i), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (d = n.current) == null || d.appendChild(i);
    return () => {
      var a, h;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((h = n.current) == null || h.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, r, l, o]), v.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function De(e, t = !1) {
  try {
    if (t && !Ne(e))
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
function x(e, t) {
  return V(() => De(e, t), [e, t]);
}
function Ae(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function $(e, t, r) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, n) => {
      var g;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const s = {
        ...o.props,
        key: ((g = o.props) == null ? void 0 : g.key) ?? (r ? `${r}-${n}` : `${n}`)
      };
      let c = s;
      Object.keys(o.slots).forEach((u) => {
        if (!o.slots[u] || !(o.slots[u] instanceof Element) && !o.slots[u].el)
          return;
        const d = u.split(".");
        d.forEach((m, p) => {
          c[m] || (c[m] = {}), p !== d.length - 1 && (c = s[m]);
        });
        const a = o.slots[u];
        let h, _, w = (t == null ? void 0 : t.clone) ?? !1;
        a instanceof Element ? h = a : (h = a.el, _ = a.callback, w = a.clone ?? w), c[d[d.length - 1]] = h ? _ ? (...m) => (_(d[d.length - 1], m), /* @__PURE__ */ b.jsx(C, {
          slot: h,
          clone: w
        })) : /* @__PURE__ */ b.jsx(C, {
          slot: h,
          clone: w
        }) : c[d[d.length - 1]], c = s;
      });
      const i = (t == null ? void 0 : t.children) || "children";
      return o[i] && (s[i] = $(o[i], t, `${n}`)), s;
    });
}
function We(e, t) {
  return e ? /* @__PURE__ */ b.jsx(C, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function O({
  key: e,
  setSlotParams: t,
  slots: r
}, l) {
  return r[e] ? (...o) => (t(e, o), We(r[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ue = Se(({
  slots: e,
  filterTreeNode: t,
  treeData: r,
  draggable: l,
  allowDrop: o,
  onCheck: n,
  onSelect: s,
  onExpand: c,
  children: i,
  directory: g,
  slotItems: u,
  setSlotParams: d,
  onLoadData: a,
  titleRender: h,
  ..._
}) => {
  const w = x(t), m = x(l), p = x(h), y = x(typeof l == "object" ? l.nodeDraggable : void 0), P = x(o), f = g ? A.DirectoryTree : A, ee = V(() => ({
    ..._,
    treeData: r || $(u, {
      clone: !0
    }),
    showLine: e["showLine.showLeafIcon"] ? {
      showLeafIcon: O({
        slots: e,
        setSlotParams: d,
        key: "showLine.showLeafIcon"
      })
    } : _.showLine,
    icon: e.icon ? O({
      slots: e,
      setSlotParams: d,
      key: "icon"
    }) : _.icon,
    switcherLoadingIcon: e.switcherLoadingIcon ? /* @__PURE__ */ b.jsx(C, {
      slot: e.switcherLoadingIcon
    }) : _.switcherLoadingIcon,
    switcherIcon: e.switcherIcon ? O({
      slots: e,
      setSlotParams: d,
      key: "switcherIcon"
    }) : _.switcherIcon,
    titleRender: e.titleRender ? O({
      slots: e,
      setSlotParams: d,
      key: "titleRender"
    }) : p,
    draggable: e["draggable.icon"] || y ? {
      icon: e["draggable.icon"] ? /* @__PURE__ */ b.jsx(C, {
        slot: e["draggable.icon"]
      }) : typeof l == "object" ? l.icon : void 0,
      nodeDraggable: y
    } : m || l,
    loadData: a
  }), [_, r, u, e, d, y, l, p, m, a]);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [/* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: i
    }), /* @__PURE__ */ b.jsx(f, {
      ...Ae(ee),
      filterTreeNode: w,
      allowDrop: P,
      onSelect: (I, ...R) => {
        s == null || s(I, ...R);
      },
      onExpand: (I, ...R) => {
        c == null || c(I, ...R);
      },
      onCheck: (I, ...R) => {
        n == null || n(I, ...R);
      }
    })]
  });
});
export {
  Ue as Tree,
  Ue as default
};
