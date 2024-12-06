import { g as $, w as v } from "./Index-D0SDhsEv.js";
const m = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Popover;
var G = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = m, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) re.call(t, l) && !le.hasOwnProperty(l) && (r[l] = t[l]);
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
x.Fragment = oe;
x.jsx = U;
x.jsxs = U;
G.exports = x;
var w = G.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: j,
  check_outros: ce,
  children: H,
  claim_element: K,
  claim_space: ae,
  component_subscribe: F,
  compute_slots: ue,
  create_slot: de,
  detach: h,
  element: q,
  empty: T,
  exclude_internal_props: N,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: C,
  safe_not_equal: he,
  set_custom_element_data: V,
  space: ge,
  transition_in: R,
  transition_out: O,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function A(n) {
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
      t = q("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(t);
      r && r.l(s), s.forEach(h), this.h();
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
      o || (R(r, e), o = !0);
    },
    o(e) {
      O(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function Ce(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      t = q("react-portal-target"), o = ge(), e && e.c(), l = T(), this.h();
    },
    l(s) {
      t = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(h), o = ae(s), e && e.l(s), l = T(), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, t, c), n[8](t), C(s, o, c), e && e.m(s, c), C(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = A(s), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (_e(), O(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      r || (R(e), r = !0);
    },
    o(s) {
      O(e), r = !1;
    },
    d(s) {
      s && (h(t), h(o), h(l)), n[8](null), e && e.d(s);
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
function Re(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ue(e);
  let {
    svelteInit: i
  } = t;
  const g = v(W(t)), d = v();
  F(n, d, (a) => o(0, l = a));
  const _ = v();
  F(n, _, (a) => o(1, r = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: S,
    subSlotIndex: b
  } = $() || {}, y = i({
    parent: f,
    props: g,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: S,
    subSlotIndex: b,
    onDestroy(a) {
      u.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", y), be(() => {
    g.set(W(t));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function E(a) {
    j[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function B(a) {
    j[a ? "unshift" : "push"](() => {
      r = a, _.set(r);
    });
  }
  return n.$$set = (a) => {
    o(17, t = L(L({}, t), N(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, t = N(t), [l, r, d, _, c, i, s, e, E, B];
}
class xe extends ie {
  constructor(t) {
    super(), me(this, t, Re, Ce, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, P = window.ms_globals.tree;
function Se(n) {
  function t(o) {
    const l = v(), r = new xe({
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
          }, c = e.parent ?? P;
          return c.nodes = [...c.nodes, s], D({
            createPortal: I,
            node: P
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: I,
              node: P
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
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Pe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function k(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(I(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((r) => {
        if (m.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(r.props.el);
          return m.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...m.Children.toArray(r.props.children), ...e]
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
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = k(e);
      t.push(...c), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const M = J(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = Y(), [s, c] = Q([]);
  return X(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(r, u), o && u.classList.add(...o.split(" ")), l) {
        const f = Ie(l);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: p,
          clonedElement: S
        } = k(n);
        return i = S, c(p), i.style.display = "contents", g(), (E = e.current) == null || E.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, o, l, r]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Le(n, t = !1) {
  try {
    if (t && !ke(n))
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
function z(n, t) {
  return Z(() => Le(n, t), [n, t]);
}
const Fe = Se(({
  slots: n,
  afterOpenChange: t,
  getPopupContainer: o,
  children: l,
  ...r
}) => {
  const e = z(t), s = z(o);
  return /* @__PURE__ */ w.jsx(w.Fragment, {
    children: /* @__PURE__ */ w.jsx(ee, {
      ...r,
      afterOpenChange: e,
      getPopupContainer: s,
      title: n.title ? /* @__PURE__ */ w.jsx(M, {
        slot: n.title
      }) : r.title,
      content: n.content ? /* @__PURE__ */ w.jsx(M, {
        slot: n.content
      }) : r.content,
      children: l
    })
  });
});
export {
  Fe as Popover,
  Fe as default
};
