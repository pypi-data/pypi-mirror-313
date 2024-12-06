import { g as $, w as R } from "./Index-CXe4hEvO.js";
const w = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Breadcrumb;
var W = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = w, re = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, e, l) {
  var s, r = {}, t = null, o = null;
  l !== void 0 && (t = "" + l), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (s in e) le.call(e, s) && !se.hasOwnProperty(s) && (r[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) r[s] === void 0 && (r[s] = e[s]);
  return {
    $$typeof: re,
    type: n,
    key: t,
    ref: o,
    props: r,
    _owner: oe.current
  };
}
I.Fragment = ne;
I.jsx = z;
I.jsxs = z;
W.exports = I;
var b = W.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: T,
  check_outros: ae,
  children: G,
  claim_element: U,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: de,
  detach: y,
  element: H,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: C,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: ge,
  transition_in: x,
  transition_out: P,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function B(n) {
  let e, l;
  const s = (
    /*#slots*/
    n[7].default
  ), r = de(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = H("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = U(t, "SVELTE-SLOT", {
        class: !0
      });
      var o = G(e);
      r && r.l(o), o.forEach(y), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      C(t, e, o), r && r.m(e, null), n[9](e), l = !0;
    },
    p(t, o) {
      r && r.p && (!l || o & /*$$scope*/
      64) && be(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        l ? _e(
          s,
          /*$$scope*/
          t[6],
          o,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      l || (x(r, t), l = !0);
    },
    o(t) {
      P(r, t), l = !1;
    },
    d(t) {
      t && y(e), r && r.d(t), n[9](null);
    }
  };
}
function Re(n) {
  let e, l, s, r, t = (
    /*$$slots*/
    n[4].default && B(n)
  );
  return {
    c() {
      e = H("react-portal-target"), l = ge(), t && t.c(), s = A(), this.h();
    },
    l(o) {
      e = U(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(e).forEach(y), l = ie(o), t && t.l(o), s = A(), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      C(o, e, c), n[8](e), C(o, l, c), t && t.m(o, c), C(o, s, c), r = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, c), c & /*$$slots*/
      16 && x(t, 1)) : (t = B(o), t.c(), x(t, 1), t.m(s.parentNode, s)) : t && (me(), P(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(o) {
      r || (x(t), r = !0);
    },
    o(o) {
      P(t), r = !1;
    },
    d(o) {
      o && (y(e), y(l), y(s)), n[8](null), t && t.d(o);
    }
  };
}
function F(n) {
  const {
    svelteInit: e,
    ...l
  } = n;
  return l;
}
function Ce(n, e, l) {
  let s, r, {
    $$slots: t = {},
    $$scope: o
  } = e;
  const c = ue(t);
  let {
    svelteInit: a
  } = e;
  const p = R(F(e)), u = R();
  N(n, u, (d) => l(0, s = d));
  const f = R();
  N(n, f, (d) => l(1, r = d));
  const i = [], _ = Ee("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: h
  } = $() || {}, E = a({
    parent: _,
    props: p,
    target: u,
    slot: f,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: h,
    onDestroy(d) {
      i.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", E), we(() => {
    p.set(F(e));
  }), ye(() => {
    i.forEach((d) => d());
  });
  function v(d) {
    T[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function J(d) {
    T[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return n.$$set = (d) => {
    l(17, e = L(L({}, e), D(d))), "svelteInit" in d && l(5, a = d.svelteInit), "$$scope" in d && l(6, o = d.$$scope);
  }, e = D(e), [s, r, u, f, c, a, o, t, v, J];
}
class xe extends ce {
  constructor(e) {
    super(), he(this, e, Ce, Re, pe, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, k = window.ms_globals.tree;
function Se(n) {
  function e(l) {
    const s = R(), r = new xe({
      ...l,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? k;
          return c.nodes = [...c.nodes, o], M({
            createPortal: O,
            node: k
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((a) => a.svelteInstance !== s), M({
              createPortal: O,
              node: k
            });
          }), o;
        },
        ...l.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(e);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((e, l) => {
    const s = n[l];
    return typeof s == "number" && !Ie.includes(l) ? e[l] = s + "px" : e[l] = s, e;
  }, {}) : {};
}
function j(n) {
  const e = [], l = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(O(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: o
          } = j(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: o,
            children: [...w.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: o,
      type: c,
      useCapture: a
    }) => {
      l.addEventListener(c, o, a);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const t = s[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = j(t);
      e.push(...c), l.appendChild(o);
    } else t.nodeType === 3 && l.appendChild(t.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function Oe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const S = Y(({
  slot: n,
  clone: e,
  className: l,
  style: s
}, r) => {
  const t = K(), [o, c] = Q([]);
  return X(() => {
    var f;
    if (!t.current || !n)
      return;
    let a = n;
    function p() {
      let i = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (i = a.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(r, i), l && i.classList.add(...l.split(" ")), s) {
        const _ = ke(s);
        Object.keys(_).forEach((m) => {
          i.style[m] = _[m];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var h, E, v;
        (h = t.current) != null && h.contains(a) && ((E = t.current) == null || E.removeChild(a));
        const {
          portals: m,
          clonedElement: g
        } = j(n);
        return a = g, c(m), a.style.display = "contents", p(), (v = t.current) == null || v.appendChild(a), m.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", p(), (f = t.current) == null || f.appendChild(a);
    return () => {
      var i, _;
      a.style.display = "", (i = t.current) != null && i.contains(a) && ((_ = t.current) == null || _.removeChild(a)), u == null || u.disconnect();
    };
  }, [n, e, l, s, r]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...o);
});
function V(n, e, l) {
  const s = n.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, t) => {
      var p;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const o = {
        ...r.props,
        key: ((p = r.props) == null ? void 0 : p.key) ?? (l ? `${l}-${t}` : `${t}`)
      };
      let c = o;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((h, E) => {
          c[h] || (c[h] = {}), E !== f.length - 1 && (c = o[h]);
        });
        const i = r.slots[u];
        let _, m, g = (e == null ? void 0 : e.clone) ?? !1;
        i instanceof Element ? _ = i : (_ = i.el, m = i.callback, g = i.clone ?? g), c[f[f.length - 1]] = _ ? m ? (...h) => (m(f[f.length - 1], h), /* @__PURE__ */ b.jsx(S, {
          slot: _,
          clone: g
        })) : /* @__PURE__ */ b.jsx(S, {
          slot: _,
          clone: g
        }) : c[f[f.length - 1]], c = o;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return r[a] && (o[a] = V(r[a], e, `${t}`)), o;
    });
}
function Pe(n, e) {
  return n ? /* @__PURE__ */ b.jsx(S, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function je({
  key: n,
  setSlotParams: e,
  slots: l
}, s) {
  return l[n] ? (...r) => (e(n, r), Pe(l[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Te = Se(({
  slots: n,
  items: e,
  slotItems: l,
  setSlotParams: s,
  children: r,
  ...t
}) => /* @__PURE__ */ b.jsxs(b.Fragment, {
  children: [/* @__PURE__ */ b.jsx("div", {
    style: {
      display: "none"
    },
    children: r
  }), /* @__PURE__ */ b.jsx(ee, {
    ...t,
    itemRender: n.itemRender ? je({
      setSlotParams: s,
      slots: n,
      key: "itemRender"
    }, {
      clone: !0
    }) : t.itemRender,
    items: Z(() => e || V(l, {
      clone: !0
    }), [e, l]),
    separator: n.separator ? /* @__PURE__ */ b.jsx(S, {
      slot: n.separator,
      clone: !0
    }) : t.separator
  })]
}));
export {
  Te as Breadcrumb,
  Te as default
};
