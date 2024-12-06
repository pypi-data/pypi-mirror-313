import { g as oe, w as k } from "./Index-s6lQgdDx.js";
const E = window.ms_globals.React, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, ne = window.ms_globals.React.useState, re = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, T = window.ms_globals.ReactDOM.createPortal, le = window.ms_globals.antd.TreeSelect;
var B = {
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
var se = E, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, t, o) {
  var s, r = {}, n = null, l = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ae.call(t, s) && !de.hasOwnProperty(s) && (r[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: ce,
    type: e,
    key: n,
    ref: l,
    props: r,
    _owner: ue.current
  };
}
j.Fragment = ie;
j.jsx = V;
j.jsxs = V;
B.exports = j;
var g = B.exports;
const {
  SvelteComponent: fe,
  assign: A,
  binding_callbacks: W,
  check_outros: _e,
  children: J,
  claim_element: Y,
  claim_space: he,
  component_subscribe: D,
  compute_slots: pe,
  create_slot: me,
  detach: R,
  element: K,
  empty: M,
  exclude_internal_props: U,
  get_all_dirty_from_scope: ge,
  get_slot_changes: we,
  group_outros: be,
  init: ye,
  insert_hydration: S,
  safe_not_equal: Ee,
  set_custom_element_data: Q,
  space: xe,
  transition_in: O,
  transition_out: F,
  update_slot_base: Re
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ce,
  onDestroy: Ie,
  setContext: ke
} = window.__gradio__svelte__internal;
function z(e) {
  let t, o;
  const s = (
    /*#slots*/
    e[7].default
  ), r = me(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(t);
      r && r.l(l), l.forEach(R), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      S(n, t, l), r && r.m(t, null), e[9](t), o = !0;
    },
    p(n, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && Re(
        r,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? we(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : ge(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (O(r, n), o = !0);
    },
    o(n) {
      F(r, n), o = !1;
    },
    d(n) {
      n && R(t), r && r.d(n), e[9](null);
    }
  };
}
function Se(e) {
  let t, o, s, r, n = (
    /*$$slots*/
    e[4].default && z(e)
  );
  return {
    c() {
      t = K("react-portal-target"), o = xe(), n && n.c(), s = M(), this.h();
    },
    l(l) {
      t = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(R), o = he(l), n && n.l(l), s = M(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      S(l, t, i), e[8](t), S(l, o, i), n && n.m(l, i), S(l, s, i), r = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, i), i & /*$$slots*/
      16 && O(n, 1)) : (n = z(l), n.c(), O(n, 1), n.m(s.parentNode, s)) : n && (be(), F(n, 1, 1, () => {
        n = null;
      }), _e());
    },
    i(l) {
      r || (O(n), r = !0);
    },
    o(l) {
      F(n), r = !1;
    },
    d(l) {
      l && (R(t), R(o), R(s)), e[8](null), n && n.d(l);
    }
  };
}
function G(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function Oe(e, t, o) {
  let s, r, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const i = pe(n);
  let {
    svelteInit: c
  } = t;
  const w = k(G(t)), u = k();
  D(e, u, (d) => o(0, s = d));
  const _ = k();
  D(e, _, (d) => o(1, r = d));
  const a = [], f = Ce("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: h,
    subSlotIndex: m
  } = oe() || {}, b = c({
    parent: f,
    props: w,
    target: u,
    slot: _,
    slotKey: p,
    slotIndex: h,
    subSlotIndex: m,
    onDestroy(d) {
      a.push(d);
    }
  });
  ke("$$ms-gr-react-wrapper", b), ve(() => {
    w.set(G(t));
  }), Ie(() => {
    a.forEach((d) => d());
  });
  function y(d) {
    W[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function I(d) {
    W[d ? "unshift" : "push"](() => {
      r = d, _.set(r);
    });
  }
  return e.$$set = (d) => {
    o(17, t = A(A({}, t), U(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, l = d.$$scope);
  }, t = U(t), [s, r, u, _, i, c, l, n, y, I];
}
class je extends fe {
  constructor(t) {
    super(), ye(this, t, Oe, Se, Ee, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, P = window.ms_globals.tree;
function Pe(e) {
  function t(o) {
    const s = k(), r = new je({
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
          }, i = n.parent ?? P;
          return i.nodes = [...i.nodes, l], H({
            createPortal: T,
            node: P
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), H({
              createPortal: T,
              node: P
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
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const s = e[o];
    return typeof s == "number" && !Te.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function L(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(T(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((r) => {
        if (E.isValidElement(r) && r.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = L(r.props.el);
          return E.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...E.Children.toArray(r.props.children), ...n]
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
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, l, c);
    });
  });
  const s = Array.from(e.childNodes);
  for (let r = 0; r < s.length; r++) {
    const n = s[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = L(n);
      t.push(...i), o.appendChild(l);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Le(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const x = ee(({
  slot: e,
  clone: t,
  className: o,
  style: s
}, r) => {
  const n = te(), [l, i] = ne([]);
  return re(() => {
    var _;
    if (!n.current || !e)
      return;
    let c = e;
    function w() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Le(r, a), o && a.classList.add(...o.split(" ")), s) {
        const f = Fe(s);
        Object.keys(f).forEach((p) => {
          a.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var m, b, y;
        (m = n.current) != null && m.contains(c) && ((b = n.current) == null || b.removeChild(c));
        const {
          portals: p,
          clonedElement: h
        } = L(e);
        return c = h, i(p), c.style.display = "contents", w(), (y = n.current) == null || y.appendChild(c), p.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", w(), (_ = n.current) == null || _.appendChild(c);
    return () => {
      var a, f;
      c.style.display = "", (a = n.current) != null && a.contains(c) && ((f = n.current) == null || f.removeChild(c)), u == null || u.disconnect();
    };
  }, [e, t, o, s, r]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ne(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Ae(e, t = !1) {
  try {
    if (t && !Ne(e))
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
function v(e, t) {
  return q(() => Ae(e, t), [e, t]);
}
function We(e) {
  return Object.keys(e).reduce((t, o) => (e[o] !== void 0 && (t[o] = e[o]), t), {});
}
function X(e, t, o) {
  const s = e.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, n) => {
      var w;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const l = {
        ...r.props,
        key: ((w = r.props) == null ? void 0 : w.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let i = l;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const _ = u.split(".");
        _.forEach((m, b) => {
          i[m] || (i[m] = {}), b !== _.length - 1 && (i = l[m]);
        });
        const a = r.slots[u];
        let f, p, h = (t == null ? void 0 : t.clone) ?? !1;
        a instanceof Element ? f = a : (f = a.el, p = a.callback, h = a.clone ?? h), i[_[_.length - 1]] = f ? p ? (...m) => (p(_[_.length - 1], m), /* @__PURE__ */ g.jsx(x, {
          slot: f,
          clone: h
        })) : /* @__PURE__ */ g.jsx(x, {
          slot: f,
          clone: h
        }) : i[_[_.length - 1]], i = l;
      });
      const c = (t == null ? void 0 : t.children) || "children";
      return r[c] && (l[c] = X(r[c], t, `${n}`)), l;
    });
}
function De(e, t) {
  return e ? /* @__PURE__ */ g.jsx(x, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function C({
  key: e,
  setSlotParams: t,
  slots: o
}, s) {
  return o[e] ? (...r) => (t(e, r), De(o[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ue = Pe(({
  slots: e,
  filterTreeNode: t,
  getPopupContainer: o,
  dropdownRender: s,
  tagRender: r,
  treeTitleRender: n,
  treeData: l,
  onValueChange: i,
  onChange: c,
  children: w,
  slotItems: u,
  maxTagPlaceholder: _,
  elRef: a,
  setSlotParams: f,
  onLoadData: p,
  ...h
}) => {
  const m = v(t), b = v(o), y = v(r), I = v(s), d = v(n), Z = q(() => ({
    ...h,
    loadData: p,
    treeData: l || X(u, {
      clone: !0
    }),
    dropdownRender: e.dropdownRender ? C({
      slots: e,
      setSlotParams: f,
      key: "dropdownRender"
    }) : I,
    allowClear: e["allowClear.clearIcon"] ? {
      clearIcon: /* @__PURE__ */ g.jsx(x, {
        slot: e["allowClear.clearIcon"]
      })
    } : h.allowClear,
    suffixIcon: e.suffixIcon ? /* @__PURE__ */ g.jsx(x, {
      slot: e.suffixIcon
    }) : h.suffixIcon,
    prefix: e.prefix ? /* @__PURE__ */ g.jsx(x, {
      slot: e.prefix
    }) : h.prefix,
    switcherIcon: e.switcherIcon ? C({
      slots: e,
      setSlotParams: f,
      key: "switcherIcon"
    }) : h.switcherIcon,
    getPopupContainer: b,
    tagRender: e.tagRender ? C({
      slots: e,
      setSlotParams: f,
      key: "tagRender"
    }) : y,
    treeTitleRender: e.treeTitleRender ? C({
      slots: e,
      setSlotParams: f,
      key: "treeTitleRender"
    }) : d,
    filterTreeNode: m || t,
    maxTagPlaceholder: e.maxTagPlaceholder ? C({
      slots: e,
      setSlotParams: f,
      key: "maxTagPlaceholder"
    }) : _,
    notFoundContent: e.notFoundContent ? /* @__PURE__ */ g.jsx(x, {
      slot: e.notFoundContent
    }) : h.notFoundContent
  }), [I, t, m, b, _, p, h, f, u, e, y, l, d]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: w
    }), /* @__PURE__ */ g.jsx(le, {
      ...We(Z),
      ref: a,
      onChange: (N, ...$) => {
        c == null || c(N, ...$), i(N);
      }
    })]
  });
});
export {
  Ue as TreeSelect,
  Ue as default
};
