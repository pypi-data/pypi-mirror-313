import { g as $, w as x } from "./Index-DbPJn-HQ.js";
const p = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Drawer;
var G = {
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
var te = p, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(e, n, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) oe.call(n, s) && !le.hasOwnProperty(s) && (o[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: ne,
    type: e,
    key: t,
    ref: l,
    props: o,
    _owner: se.current
  };
}
S.Fragment = re;
S.jsx = U;
S.jsxs = U;
G.exports = S;
var h = G.exports;
const {
  SvelteComponent: ie,
  assign: F,
  binding_callbacks: T,
  check_outros: ce,
  children: H,
  claim_element: K,
  claim_space: ae,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: q,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: me,
  init: pe,
  insert_hydration: R,
  safe_not_equal: he,
  set_custom_element_data: V,
  space: we,
  transition_in: C,
  transition_out: j,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function W(e) {
  let n, r;
  const s = (
    /*#slots*/
    e[7].default
  ), o = de(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = q("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(n);
      o && o.l(l), l.forEach(w), this.h();
    },
    h() {
      V(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      R(t, n, l), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ge(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? _e(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (C(o, t), r = !0);
    },
    o(t) {
      j(o, t), r = !1;
    },
    d(t) {
      t && w(n), o && o.d(t), e[9](null);
    }
  };
}
function xe(e) {
  let n, r, s, o, t = (
    /*$$slots*/
    e[4].default && W(e)
  );
  return {
    c() {
      n = q("react-portal-target"), r = we(), t && t.c(), s = A(), this.h();
    },
    l(l) {
      n = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(w), r = ae(l), t && t.l(l), s = A(), this.h();
    },
    h() {
      V(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      R(l, n, c), e[8](n), R(l, r, c), t && t.m(l, c), R(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && C(t, 1)) : (t = W(l), t.c(), C(t, 1), t.m(s.parentNode, s)) : t && (me(), j(t, 1, 1, () => {
        t = null;
      }), ce());
    },
    i(l) {
      o || (C(t), o = !0);
    },
    o(l) {
      j(t), o = !1;
    },
    d(l) {
      l && (w(n), w(r), w(s)), e[8](null), t && t.d(l);
    }
  };
}
function M(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Re(e, n, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const c = ue(t);
  let {
    svelteInit: i
  } = n;
  const g = x(M(n)), d = x();
  N(e, d, (a) => r(0, s = a));
  const m = x();
  N(e, m, (a) => r(1, o = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: I,
    subSlotIndex: y
  } = $() || {}, E = i({
    parent: f,
    props: g,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: I,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", E), be(() => {
    g.set(M(n));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function v(a) {
    T[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function B(a) {
    T[a ? "unshift" : "push"](() => {
      o = a, m.set(o);
    });
  }
  return e.$$set = (a) => {
    r(17, n = F(F({}, n), D(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, n = D(n), [s, o, d, m, c, i, l, t, v, B];
}
class Ce extends ie {
  constructor(n) {
    super(), pe(this, n, Re, xe, he, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, O = window.ms_globals.tree;
function Se(e) {
  function n(r) {
    const s = x(), o = new Ce({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? O;
          return c.nodes = [...c.nodes, l], z({
            createPortal: k,
            node: O
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), z({
              createPortal: k,
              node: O
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const s = e[r];
    return typeof s == "number" && !Ie.includes(r) ? n[r] = s + "px" : n[r] = s, n;
  }, {}) : {};
}
function L(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(k(p.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: p.Children.toArray(e._reactElement.props.children).map((o) => {
        if (p.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = L(o.props.el);
          return p.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...p.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = L(t);
      n.push(...c), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Pe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = J(({
  slot: e,
  clone: n,
  className: r,
  style: s
}, o) => {
  const t = Y(), [l, c] = Q([]);
  return X(() => {
    var m;
    if (!t.current || !e)
      return;
    let i = e;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Pe(o, u), r && u.classList.add(...r.split(" ")), s) {
        const f = Oe(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var y, E, v;
        (y = t.current) != null && y.contains(i) && ((E = t.current) == null || E.removeChild(i));
        const {
          portals: _,
          clonedElement: I
        } = L(e);
        return i = I, c(_), i.style.display = "contents", g(), (v = t.current) == null || v.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (m = t.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((f = t.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, n, r, s, o]), p.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function ke(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function je(e, n = !1) {
  try {
    if (n && !ke(e))
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
function P(e, n) {
  return Z(() => je(e, n), [e, n]);
}
function Le(e, n) {
  return e ? /* @__PURE__ */ h.jsx(b, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Fe({
  key: e,
  setSlotParams: n,
  slots: r
}, s) {
  return r[e] ? (...o) => (n(e, o), Le(r[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Se(({
  slots: e,
  afterOpenChange: n,
  getContainer: r,
  drawerRender: s,
  setSlotParams: o,
  ...t
}) => {
  const l = P(n), c = P(r), i = P(s);
  return /* @__PURE__ */ h.jsx(ee, {
    ...t,
    afterOpenChange: l,
    closeIcon: e.closeIcon ? /* @__PURE__ */ h.jsx(b, {
      slot: e.closeIcon
    }) : t.closeIcon,
    extra: e.extra ? /* @__PURE__ */ h.jsx(b, {
      slot: e.extra
    }) : t.extra,
    footer: e.footer ? /* @__PURE__ */ h.jsx(b, {
      slot: e.footer
    }) : t.footer,
    title: e.title ? /* @__PURE__ */ h.jsx(b, {
      slot: e.title
    }) : t.title,
    drawerRender: e.drawerRender ? Fe({
      slots: e,
      setSlotParams: o,
      key: "drawerRender"
    }) : i,
    getContainer: typeof r == "string" ? c : r
  });
});
export {
  Ne as Drawer,
  Ne as default
};
