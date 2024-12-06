import { g as $, w as x } from "./Index-CKhbJCsB.js";
const w = window.ms_globals.React, z = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Collapse;
var G = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = w, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, e, l) {
  var o, r = {}, t = null, s = null;
  l !== void 0 && (t = "" + l), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) le.call(e, o) && !oe.hasOwnProperty(o) && (r[o] = e[o]);
  if (n && n.defaultProps) for (o in e = n.defaultProps, e) r[o] === void 0 && (r[o] = e[o]);
  return {
    $$typeof: ne,
    type: n,
    key: t,
    ref: s,
    props: r,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = U;
R.jsxs = U;
G.exports = R;
var y = G.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: T,
  check_outros: ie,
  children: H,
  claim_element: q,
  claim_space: ae,
  component_subscribe: F,
  compute_slots: ue,
  create_slot: de,
  detach: E,
  element: B,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: he,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: V,
  space: ge,
  transition_in: I,
  transition_out: O,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function W(n) {
  let e, l;
  const o = (
    /*#slots*/
    n[7].default
  ), r = de(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = B("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = q(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(e);
      r && r.l(s), s.forEach(E), this.h();
    },
    h() {
      V(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      C(t, e, s), r && r.m(e, null), n[9](e), l = !0;
    },
    p(t, s) {
      r && r.p && (!l || s & /*$$scope*/
      64) && we(
        r,
        o,
        t,
        /*$$scope*/
        t[6],
        l ? _e(
          o,
          /*$$scope*/
          t[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      l || (I(r, t), l = !0);
    },
    o(t) {
      O(r, t), l = !1;
    },
    d(t) {
      t && E(e), r && r.d(t), n[9](null);
    }
  };
}
function xe(n) {
  let e, l, o, r, t = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      e = B("react-portal-target"), l = ge(), t && t.c(), o = N(), this.h();
    },
    l(s) {
      e = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(e).forEach(E), l = ae(s), t && t.l(s), o = N(), this.h();
    },
    h() {
      V(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, e, c), n[8](e), C(s, l, c), t && t.m(s, c), C(s, o, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && I(t, 1)) : (t = W(s), t.c(), I(t, 1), t.m(o.parentNode, o)) : t && (pe(), O(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(s) {
      r || (I(t), r = !0);
    },
    o(s) {
      O(t), r = !1;
    },
    d(s) {
      s && (E(e), E(l), E(o)), n[8](null), t && t.d(s);
    }
  };
}
function D(n) {
  const {
    svelteInit: e,
    ...l
  } = n;
  return l;
}
function Ce(n, e, l) {
  let o, r, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = ue(t);
  let {
    svelteInit: i
  } = e;
  const h = x(D(e)), u = x();
  F(n, u, (d) => l(0, o = d));
  const f = x();
  F(n, f, (d) => l(1, r = d));
  const a = [], _ = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: m
  } = $() || {}, b = i({
    parent: _,
    props: h,
    target: u,
    slot: f,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: m,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", b), be(() => {
    h.set(D(e));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    T[d ? "unshift" : "push"](() => {
      o = d, u.set(o);
    });
  }
  function Y(d) {
    T[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return n.$$set = (d) => {
    l(17, e = L(L({}, e), A(d))), "svelteInit" in d && l(5, i = d.svelteInit), "$$scope" in d && l(6, s = d.$$scope);
  }, e = A(e), [o, r, u, f, c, i, s, t, v, Y];
}
class Ie extends ce {
  constructor(e) {
    super(), he(this, e, Ce, xe, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, S = window.ms_globals.tree;
function Re(n) {
  function e(l) {
    const o = x(), r = new Ie({
      ...l,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? S;
          return c.nodes = [...c.nodes, s], M({
            createPortal: k,
            node: S
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), M({
              createPortal: k,
              node: S
            });
          }), s;
        },
        ...l.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(e);
    });
  });
}
function Se(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function ke(n, e = !1) {
  try {
    if (e && !Se(n))
      return;
    if (typeof n == "string") {
      let l = n.trim();
      return l.startsWith(";") && (l = l.slice(1)), l.endsWith(";") && (l = l.slice(0, -1)), new Function(`return (...args) => (${l})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Oe(n, e) {
  return z(() => ke(n, e), [n, e]);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((e, l) => {
    const o = n[l];
    return typeof o == "number" && !Pe.includes(l) ? e[l] = o + "px" : e[l] = o, e;
  }, {}) : {};
}
function P(n) {
  const e = [], l = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(k(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = P(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: s,
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
      listener: s,
      type: c,
      useCapture: i
    }) => {
      l.addEventListener(c, s, i);
    });
  });
  const o = Array.from(n.childNodes);
  for (let r = 0; r < o.length; r++) {
    const t = o[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = P(t);
      e.push(...c), l.appendChild(s);
    } else t.nodeType === 3 && l.appendChild(t.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function Le(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const j = K(({
  slot: n,
  clone: e,
  className: l,
  style: o
}, r) => {
  const t = Q(), [s, c] = X([]);
  return Z(() => {
    var f;
    if (!t.current || !n)
      return;
    let i = n;
    function h() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Le(r, a), l && a.classList.add(...l.split(" ")), o) {
        const _ = je(o);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var m, b, v;
        (m = t.current) != null && m.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: g
        } = P(n);
        return i = g, c(p), i.style.display = "contents", h(), (v = t.current) == null || v.appendChild(i), p.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, e, l, o, r]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function J(n, e, l) {
  const o = n.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, t) => {
      var h;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const s = {
        ...r.props,
        key: ((h = r.props) == null ? void 0 : h.key) ?? (l ? `${l}-${t}` : `${t}`)
      };
      let c = s;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((m, b) => {
          c[m] || (c[m] = {}), b !== f.length - 1 && (c = s[m]);
        });
        const a = r.slots[u];
        let _, p, g = (e == null ? void 0 : e.clone) ?? !1;
        a instanceof Element ? _ = a : (_ = a.el, p = a.callback, g = a.clone ?? g), c[f[f.length - 1]] = _ ? p ? (...m) => (p(f[f.length - 1], m), /* @__PURE__ */ y.jsx(j, {
          slot: _,
          clone: g
        })) : /* @__PURE__ */ y.jsx(j, {
          slot: _,
          clone: g
        }) : c[f[f.length - 1]], c = s;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return r[i] && (s[i] = J(r[i], e, `${t}`)), s;
    });
}
function Te(n, e) {
  return n ? /* @__PURE__ */ y.jsx(j, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Fe({
  key: n,
  setSlotParams: e,
  slots: l
}, o) {
  return l[n] ? (...r) => (e(n, r), Te(l[n], {
    clone: !0,
    ...o
  })) : void 0;
}
const Ae = Re(({
  slots: n,
  items: e,
  slotItems: l,
  children: o,
  onChange: r,
  setSlotParams: t,
  expandIcon: s,
  ...c
}) => {
  const i = Oe(s);
  return /* @__PURE__ */ y.jsxs(y.Fragment, {
    children: [o, /* @__PURE__ */ y.jsx(ee, {
      ...c,
      onChange: (h) => {
        r == null || r(h);
      },
      expandIcon: n.expandIcon ? Fe({
        slots: n,
        setSlotParams: t,
        key: "expandIcon"
      }) : i,
      items: z(() => e || J(l, {
        clone: !0
      }), [e, l])
    })]
  });
});
export {
  Ae as Collapse,
  Ae as default
};
