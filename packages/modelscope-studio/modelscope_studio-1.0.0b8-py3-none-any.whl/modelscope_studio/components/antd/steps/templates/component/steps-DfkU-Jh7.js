import { g as $, w as S } from "./Index-DyIbxa4-.js";
const w = window.ms_globals.React, z = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Steps;
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
var te = w, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) oe.call(t, l) && !le.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = U;
R.jsxs = U;
G.exports = R;
var b = G.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: T,
  check_outros: ce,
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
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: V,
  space: ge,
  transition_in: x,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function D(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = de(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = B("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(t);
      r && r.l(s), s.forEach(E), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && we(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? pe(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (x(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && E(t), r && r.d(e), n[9](null);
    }
  };
}
function Se(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = B("react-portal-target"), o = ge(), e && e.c(), l = N(), this.h();
    },
    l(s) {
      t = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(E), o = ae(s), e && e.l(s), l = N(), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      C(s, t, i), n[8](t), C(s, o, i), e && e.m(s, i), C(s, l, i), r = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && x(e, 1)) : (e = D(s), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      r || (x(e), r = !0);
    },
    o(s) {
      k(e), r = !1;
    },
    d(s) {
      s && (E(t), E(o), E(l)), n[8](null), e && e.d(s);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ce(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = ue(e);
  let {
    svelteInit: c
  } = t;
  const m = S(W(t)), u = S();
  F(n, u, (d) => o(0, l = d));
  const f = S();
  F(n, f, (d) => o(1, r = d));
  const a = [], p = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: h
  } = $() || {}, y = c({
    parent: p,
    props: m,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: g,
    subSlotIndex: h,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", y), be(() => {
    m.set(W(t));
  }), Ee(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    T[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function Y(d) {
    T[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return n.$$set = (d) => {
    o(17, t = L(L({}, t), A(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, t = A(t), [l, r, u, f, i, c, s, e, v, Y];
}
class xe extends ie {
  constructor(t) {
    super(), he(this, t, Ce, Se, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const l = S(), r = new xe({
      ...o,
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
          }, i = e.parent ?? I;
          return i.nodes = [...i.nodes, s], M({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), M({
              createPortal: O,
              node: I
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function Ie(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Oe(n, t = !1) {
  try {
    if (t && !Ie(n))
      return;
    if (typeof n == "string") {
      let o = n.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function ke(n, t) {
  return z(() => Oe(n, t), [n, t]);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Pe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function P(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = P(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...w.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      o.addEventListener(i, s, c);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = P(e);
      t.push(...i), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Le(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const j = K(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = Q(), [s, i] = X([]);
  return Z(() => {
    var f;
    if (!e.current || !n)
      return;
    let c = n;
    function m() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Le(r, a), o && a.classList.add(...o.split(" ")), l) {
        const p = je(l);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var h, y, v;
        (h = e.current) != null && h.contains(c) && ((y = e.current) == null || y.removeChild(c));
        const {
          portals: _,
          clonedElement: g
        } = P(n);
        return c = g, i(_), c.style.display = "contents", m(), (v = e.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", m(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((p = e.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [n, t, o, l, r]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function J(n, t, o) {
  const l = n.filter(Boolean);
  if (l.length !== 0)
    return l.map((r, e) => {
      var m;
      if (typeof r != "object")
        return r;
      const s = {
        ...r.props,
        key: ((m = r.props) == null ? void 0 : m.key) ?? (o ? `${o}-${e}` : `${e}`)
      };
      let i = s;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((h, y) => {
          i[h] || (i[h] = {}), y !== f.length - 1 && (i = s[h]);
        });
        const a = r.slots[u];
        let p, _, g = !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, g = a.clone ?? g), i[f[f.length - 1]] = p ? _ ? (...h) => (_(f[f.length - 1], h), /* @__PURE__ */ b.jsx(j, {
          slot: p,
          clone: g
        })) : /* @__PURE__ */ b.jsx(j, {
          slot: p,
          clone: g
        }) : i[f[f.length - 1]], i = s;
      });
      const c = "children";
      return r[c] && (s[c] = J(r[c], t, `${e}`)), s;
    });
}
function Te(n, t) {
  return n ? /* @__PURE__ */ b.jsx(j, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Fe({
  key: n,
  setSlotParams: t,
  slots: o
}, l) {
  return o[n] ? (...r) => (t(n, r), Te(o[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ae = Re(({
  slots: n,
  items: t,
  slotItems: o,
  setSlotParams: l,
  children: r,
  progressDot: e,
  ...s
}) => {
  const i = ke(e);
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [/* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ b.jsx(ee, {
      ...s,
      items: z(() => t || J(o), [t, o]),
      progressDot: n.progressDot ? Fe({
        slots: n,
        setSlotParams: l,
        key: "progressDot"
      }, {
        clone: !0
      }) : i || e
    })]
  });
});
export {
  Ae as Steps,
  Ae as default
};
