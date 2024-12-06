import { g as V, w as v } from "./Index-CY797iM9.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.message;
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) re.call(t, l) && !se.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: oe.current
  };
}
x.Fragment = ne;
x.jsx = H;
x.jsxs = H;
G.exports = x;
var w = G.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: j,
  check_outros: ie,
  children: U,
  claim_element: K,
  claim_space: ce,
  component_subscribe: T,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: q,
  empty: A,
  exclude_internal_props: F,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert_hydration: C,
  safe_not_equal: pe,
  set_custom_element_data: B,
  space: he,
  transition_in: R,
  transition_out: O,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ye,
  onDestroy: Ee,
  setContext: be
} = window.__gradio__svelte__internal;
function N(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ue(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      o && o.l(s), s.forEach(g), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ge(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? fe(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (R(o, e), r = !0);
    },
    o(e) {
      O(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      t = q("react-portal-target"), r = he(), e && e.c(), l = A(), this.h();
    },
    l(s) {
      t = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(g), r = ce(s), e && e.l(s), l = A(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, t, c), n[8](t), C(s, r, c), e && e.m(s, c), C(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = N(s), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (_e(), O(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      o || (R(e), o = !0);
    },
    o(s) {
      O(e), o = !1;
    },
    d(s) {
      s && (g(t), g(r), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ce(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const m = v(M(t)), d = v();
  T(n, d, (a) => r(0, l = a));
  const p = v();
  T(n, p, (a) => r(1, o = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y
  } = V() || {}, E = i({
    parent: f,
    props: m,
    target: d,
    slot: p,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  be("$$ms-gr-react-wrapper", E), we(() => {
    m.set(M(t));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function b(a) {
    j[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function J(a) {
    j[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = L(L({}, t), F(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = F(t), [l, o, d, p, c, i, s, e, b, J];
}
class Re extends le {
  constructor(t) {
    super(), me(this, t, Ce, ve, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, I = window.ms_globals.tree;
function xe(n) {
  function t(r) {
    const l = v(), o = new Re({
      ...r,
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
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, s], W({
            createPortal: k,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), W({
              createPortal: k,
              node: I
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
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !Se.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function P(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = P(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...h.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = P(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const D = Y(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = Q(), [s, c] = X([]);
  return z(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function m() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(o, u), r && u.classList.add(...r.split(" ")), l) {
        const f = Ie(l);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var y, E, b;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = P(n);
        return i = S, c(_), i.style.display = "contents", m(), (b = e.current) == null || b.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, r, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Oe(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Pe(n, t = !1) {
  try {
    if (t && !Oe(n))
      return;
    if (typeof n == "string") {
      let r = n.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Le(n, t) {
  return Z(() => Pe(n, t), [n, t]);
}
const Te = xe(({
  slots: n,
  children: t,
  visible: r,
  onVisible: l,
  onClose: o,
  getContainer: e,
  ...s
}) => {
  const c = Le(e), [i, m] = $.useMessage({
    ...s,
    getContainer: c
  });
  return z(() => (r ? i.open({
    ...s,
    icon: n.icon ? /* @__PURE__ */ w.jsx(D, {
      slot: n.icon
    }) : s.icon,
    content: n.content ? /* @__PURE__ */ w.jsx(D, {
      slot: n.content
    }) : s.content,
    onClose(...d) {
      l == null || l(!1), o == null || o(...d);
    }
  }) : i.destroy(s.key), () => {
    i.destroy(s.key);
  }), [r]), /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), m]
  });
});
export {
  Te as Message,
  Te as default
};
