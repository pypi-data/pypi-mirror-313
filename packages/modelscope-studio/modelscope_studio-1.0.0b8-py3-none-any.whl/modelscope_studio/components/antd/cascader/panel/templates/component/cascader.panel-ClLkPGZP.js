import { b as $, g as ee, w as C } from "./Index-D-rkf9zY.js";
const w = window.ms_globals.React, X = window.ms_globals.React.forwardRef, O = window.ms_globals.React.useRef, z = window.ms_globals.React.useState, P = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Cascader;
function ne(r, t) {
  return $(r, t);
}
var G = {
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
var re = w, le = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(r, t, l) {
  var s, n = {}, e = null, o = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) se.call(t, s) && !ae.hasOwnProperty(s) && (n[s] = t[s]);
  if (r && r.defaultProps) for (s in t = r.defaultProps, t) n[s] === void 0 && (n[s] = t[s]);
  return {
    $$typeof: le,
    type: r,
    key: e,
    ref: o,
    props: n,
    _owner: ce.current
  };
}
k.Fragment = oe;
k.jsx = U;
k.jsxs = U;
G.exports = k;
var b = G.exports;
const {
  SvelteComponent: ie,
  assign: N,
  binding_callbacks: A,
  check_outros: ue,
  children: H,
  claim_element: B,
  claim_space: de,
  component_subscribe: F,
  compute_slots: fe,
  create_slot: _e,
  detach: y,
  element: J,
  empty: D,
  exclude_internal_props: V,
  get_all_dirty_from_scope: pe,
  get_slot_changes: he,
  group_outros: me,
  init: ge,
  insert_hydration: x,
  safe_not_equal: be,
  set_custom_element_data: Y,
  space: we,
  transition_in: I,
  transition_out: L,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: ve,
  onDestroy: Ce,
  setContext: xe
} = window.__gradio__svelte__internal;
function M(r) {
  let t, l;
  const s = (
    /*#slots*/
    r[7].default
  ), n = _e(
    s,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = J("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = H(t);
      n && n.l(o), o.forEach(y), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      x(e, t, o), n && n.m(t, null), r[9](t), l = !0;
    },
    p(e, o) {
      n && n.p && (!l || o & /*$$scope*/
      64) && Ee(
        n,
        s,
        e,
        /*$$scope*/
        e[6],
        l ? he(
          s,
          /*$$scope*/
          e[6],
          o,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      l || (I(n, e), l = !0);
    },
    o(e) {
      L(n, e), l = !1;
    },
    d(e) {
      e && y(t), n && n.d(e), r[9](null);
    }
  };
}
function Ie(r) {
  let t, l, s, n, e = (
    /*$$slots*/
    r[4].default && M(r)
  );
  return {
    c() {
      t = J("react-portal-target"), l = we(), e && e.c(), s = D(), this.h();
    },
    l(o) {
      t = B(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(y), l = de(o), e && e.l(o), s = D(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      x(o, t, c), r[8](t), x(o, l, c), e && e.m(o, c), x(o, s, c), n = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && I(e, 1)) : (e = M(o), e.c(), I(e, 1), e.m(s.parentNode, s)) : e && (me(), L(e, 1, 1, () => {
        e = null;
      }), ue());
    },
    i(o) {
      n || (I(e), n = !0);
    },
    o(o) {
      L(e), n = !1;
    },
    d(o) {
      o && (y(t), y(l), y(s)), r[8](null), e && e.d(o);
    }
  };
}
function W(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function Re(r, t, l) {
  let s, n, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = fe(e);
  let {
    svelteInit: a
  } = t;
  const h = C(W(t)), u = C();
  F(r, u, (d) => l(0, s = d));
  const f = C();
  F(r, f, (d) => l(1, n = d));
  const i = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: m
  } = ee() || {}, E = a({
    parent: _,
    props: h,
    target: u,
    slot: f,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: m,
    onDestroy(d) {
      i.push(d);
    }
  });
  xe("$$ms-gr-react-wrapper", E), ye(() => {
    h.set(W(t));
  }), Ce(() => {
    i.forEach((d) => d());
  });
  function v(d) {
    A[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function Q(d) {
    A[d ? "unshift" : "push"](() => {
      n = d, f.set(n);
    });
  }
  return r.$$set = (d) => {
    l(17, t = N(N({}, t), V(d))), "svelteInit" in d && l(5, a = d.svelteInit), "$$scope" in d && l(6, o = d.$$scope);
  }, t = V(t), [s, n, u, f, c, a, o, e, v, Q];
}
class ke extends ie {
  constructor(t) {
    super(), ge(this, t, Re, Ie, be, {
      svelteInit: 5
    });
  }
}
const q = window.ms_globals.rerender, S = window.ms_globals.tree;
function Se(r) {
  function t(l) {
    const s = C(), n = new ke({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, o], q({
            createPortal: j,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== s), q({
              createPortal: j,
              node: S
            });
          }), o;
        },
        ...l.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(r) {
  return r ? Object.keys(r).reduce((t, l) => {
    const s = r[l];
    return typeof s == "number" && !Oe.includes(l) ? t[l] = s + "px" : t[l] = s, t;
  }, {}) : {};
}
function T(r) {
  const t = [], l = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(j(w.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: w.Children.toArray(r._reactElement.props.children).map((n) => {
        if (w.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = T(n.props.el);
          return w.cloneElement(n, {
            ...n.props,
            el: o,
            children: [...w.Children.toArray(n.props.children), ...e]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: t
    };
  Object.keys(r.getEventListeners()).forEach((n) => {
    r.getEventListeners(n).forEach(({
      listener: o,
      type: c,
      useCapture: a
    }) => {
      l.addEventListener(c, o, a);
    });
  });
  const s = Array.from(r.childNodes);
  for (let n = 0; n < s.length; n++) {
    const e = s[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = T(e);
      t.push(...c), l.appendChild(o);
    } else e.nodeType === 3 && l.appendChild(e.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function je(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const R = X(({
  slot: r,
  clone: t,
  className: l,
  style: s
}, n) => {
  const e = O(), [o, c] = z([]);
  return P(() => {
    var f;
    if (!e.current || !r)
      return;
    let a = r;
    function h() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), je(n, i), l && i.classList.add(...l.split(" ")), s) {
        const _ = Pe(s);
        Object.keys(_).forEach((p) => {
          i.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var m, E, v;
        (m = e.current) != null && m.contains(a) && ((E = e.current) == null || E.removeChild(a));
        const {
          portals: p,
          clonedElement: g
        } = T(r);
        return a = g, c(p), a.style.display = "contents", h(), (v = e.current) == null || v.appendChild(a), p.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", h(), (f = e.current) == null || f.appendChild(a);
    return () => {
      var i, _;
      a.style.display = "", (i = e.current) != null && i.contains(a) && ((_ = e.current) == null || _.removeChild(a)), u == null || u.disconnect();
    };
  }, [r, t, l, s, n]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
});
function Le({
  value: r,
  onValueChange: t
}) {
  const [l, s] = z(r), n = O(t);
  n.current = t;
  const e = O(l);
  return e.current = l, P(() => {
    n.current(l);
  }, [l]), P(() => {
    ne(r, e.current) || s(r);
  }, [r]), [l, s];
}
function K(r, t, l) {
  const s = r.filter(Boolean);
  if (s.length !== 0)
    return s.map((n, e) => {
      var h;
      if (typeof n != "object")
        return t != null && t.fallback ? t.fallback(n) : n;
      const o = {
        ...n.props,
        key: ((h = n.props) == null ? void 0 : h.key) ?? (l ? `${l}-${e}` : `${e}`)
      };
      let c = o;
      Object.keys(n.slots).forEach((u) => {
        if (!n.slots[u] || !(n.slots[u] instanceof Element) && !n.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((m, E) => {
          c[m] || (c[m] = {}), E !== f.length - 1 && (c = o[m]);
        });
        const i = n.slots[u];
        let _, p, g = (t == null ? void 0 : t.clone) ?? !1;
        i instanceof Element ? _ = i : (_ = i.el, p = i.callback, g = i.clone ?? g), c[f[f.length - 1]] = _ ? p ? (...m) => (p(f[f.length - 1], m), /* @__PURE__ */ b.jsx(R, {
          slot: _,
          clone: g
        })) : /* @__PURE__ */ b.jsx(R, {
          slot: _,
          clone: g
        }) : c[f[f.length - 1]], c = o;
      });
      const a = (t == null ? void 0 : t.children) || "children";
      return n[a] && (o[a] = K(n[a], t, `${e}`)), o;
    });
}
const Ne = Se(({
  slots: r,
  children: t,
  onValueChange: l,
  onChange: s,
  onLoadData: n,
  optionItems: e,
  options: o,
  ...c
}) => {
  const [a, h] = Le({
    onValueChange: l,
    value: c.value
  });
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [/* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ b.jsx(te.Panel, {
      ...c,
      value: a,
      options: Z(() => o || K(e, {
        clone: !0
      }), [o, e]),
      loadData: n,
      onChange: (u, ...f) => {
        s == null || s(u, ...f), h(u);
      },
      expandIcon: r.expandIcon ? /* @__PURE__ */ b.jsx(R, {
        slot: r.expandIcon
      }) : c.expandIcon,
      notFoundContent: r.notFoundContent ? /* @__PURE__ */ b.jsx(R, {
        slot: r.notFoundContent
      }) : c.notFoundContent
    })]
  });
});
export {
  Ne as CascaderPanel,
  Ne as default
};
