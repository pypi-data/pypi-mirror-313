import { g as ee, w as C } from "./Index-DHo5mb0G.js";
const w = window.ms_globals.React, G = window.ms_globals.React.useMemo, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Anchor;
var U = {
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
var ne = w, re = Symbol.for("react.element"), se = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(r, e, s) {
  var l, n = {}, t = null, o = null;
  s !== void 0 && (t = "" + s), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (l in e) oe.call(e, l) && !ce.hasOwnProperty(l) && (n[l] = e[l]);
  if (r && r.defaultProps) for (l in e = r.defaultProps, e) n[l] === void 0 && (n[l] = e[l]);
  return {
    $$typeof: re,
    type: r,
    key: t,
    ref: o,
    props: n,
    _owner: le.current
  };
}
S.Fragment = se;
S.jsx = H;
S.jsxs = H;
U.exports = S;
var y = U.exports;
const {
  SvelteComponent: ie,
  assign: j,
  binding_callbacks: A,
  check_outros: ae,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: L,
  compute_slots: fe,
  create_slot: de,
  detach: E,
  element: V,
  empty: F,
  exclude_internal_props: T,
  get_all_dirty_from_scope: _e,
  get_slot_changes: he,
  group_outros: pe,
  init: me,
  insert_hydration: R,
  safe_not_equal: ge,
  set_custom_element_data: J,
  space: we,
  transition_in: x,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function N(r) {
  let e, s;
  const l = (
    /*#slots*/
    r[7].default
  ), n = de(
    l,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      e = V("svelte-slot"), n && n.c(), this.h();
    },
    l(t) {
      e = B(t, "SVELTE-SLOT", {
        class: !0
      });
      var o = q(e);
      n && n.l(o), o.forEach(E), this.h();
    },
    h() {
      J(e, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      R(t, e, o), n && n.m(e, null), r[9](e), s = !0;
    },
    p(t, o) {
      n && n.p && (!s || o & /*$$scope*/
      64) && be(
        n,
        l,
        t,
        /*$$scope*/
        t[6],
        s ? he(
          l,
          /*$$scope*/
          t[6],
          o,
          null
        ) : _e(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      s || (x(n, t), s = !0);
    },
    o(t) {
      O(n, t), s = !1;
    },
    d(t) {
      t && E(e), n && n.d(t), r[9](null);
    }
  };
}
function Re(r) {
  let e, s, l, n, t = (
    /*$$slots*/
    r[4].default && N(r)
  );
  return {
    c() {
      e = V("react-portal-target"), s = we(), t && t.c(), l = F(), this.h();
    },
    l(o) {
      e = B(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(e).forEach(E), s = ue(o), t && t.l(o), l = F(), this.h();
    },
    h() {
      J(e, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      R(o, e, c), r[8](e), R(o, s, c), t && t.m(o, c), R(o, l, c), n = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, c), c & /*$$slots*/
      16 && x(t, 1)) : (t = N(o), t.c(), x(t, 1), t.m(l.parentNode, l)) : t && (pe(), O(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(o) {
      n || (x(t), n = !0);
    },
    o(o) {
      O(t), n = !1;
    },
    d(o) {
      o && (E(e), E(s), E(l)), r[8](null), t && t.d(o);
    }
  };
}
function W(r) {
  const {
    svelteInit: e,
    ...s
  } = r;
  return s;
}
function xe(r, e, s) {
  let l, n, {
    $$slots: t = {},
    $$scope: o
  } = e;
  const c = fe(t);
  let {
    svelteInit: i
  } = e;
  const m = C(W(e)), u = C();
  L(r, u, (f) => s(0, l = f));
  const d = C();
  L(r, d, (f) => s(1, n = f));
  const a = [], _ = ye("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: g,
    subSlotIndex: p
  } = ee() || {}, b = i({
    parent: _,
    props: m,
    target: u,
    slot: d,
    slotKey: h,
    slotIndex: g,
    subSlotIndex: p,
    onDestroy(f) {
      a.push(f);
    }
  });
  Ce("$$ms-gr-react-wrapper", b), Ee(() => {
    m.set(W(e));
  }), ve(() => {
    a.forEach((f) => f());
  });
  function v(f) {
    A[f ? "unshift" : "push"](() => {
      l = f, u.set(l);
    });
  }
  function K(f) {
    A[f ? "unshift" : "push"](() => {
      n = f, d.set(n);
    });
  }
  return r.$$set = (f) => {
    s(17, e = j(j({}, e), T(f))), "svelteInit" in f && s(5, i = f.svelteInit), "$$scope" in f && s(6, o = f.$$scope);
  }, e = T(e), [l, n, u, d, c, i, o, t, v, K];
}
class Se extends ie {
  constructor(e) {
    super(), me(this, e, xe, Re, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, k = window.ms_globals.tree;
function ke(r) {
  function e(s) {
    const l = C(), n = new Se({
      ...s,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? k;
          return c.nodes = [...c.nodes, o], D({
            createPortal: I,
            node: k
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: I,
              node: k
            });
          }), o;
        },
        ...s.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(e);
    });
  });
}
function Ie(r) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(r.trim());
}
function Oe(r, e = !1) {
  try {
    if (e && !Ie(r))
      return;
    if (typeof r == "string") {
      let s = r.trim();
      return s.startsWith(";") && (s = s.slice(1)), s.endsWith(";") && (s = s.slice(0, -1)), new Function(`return (...args) => (${s})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function M(r, e) {
  return G(() => Oe(r, e), [r, e]);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(r) {
  return r ? Object.keys(r).reduce((e, s) => {
    const l = r[s];
    return typeof l == "number" && !Pe.includes(s) ? e[s] = l + "px" : e[s] = l, e;
  }, {}) : {};
}
function P(r) {
  const e = [], s = r.cloneNode(!1);
  if (r._reactElement)
    return e.push(I(w.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: w.Children.toArray(r._reactElement.props.children).map((n) => {
        if (w.isValidElement(n) && n.props.__slot__) {
          const {
            portals: t,
            clonedElement: o
          } = P(n.props.el);
          return w.cloneElement(n, {
            ...n.props,
            el: o,
            children: [...w.Children.toArray(n.props.children), ...t]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: e
    };
  Object.keys(r.getEventListeners()).forEach((n) => {
    r.getEventListeners(n).forEach(({
      listener: o,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, o, i);
    });
  });
  const l = Array.from(r.childNodes);
  for (let n = 0; n < l.length; n++) {
    const t = l[n];
    if (t.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = P(t);
      e.push(...c), s.appendChild(o);
    } else t.nodeType === 3 && s.appendChild(t.cloneNode());
  }
  return {
    clonedElement: s,
    portals: e
  };
}
function Ae(r, e) {
  r && (typeof r == "function" ? r(e) : r.current = e);
}
const z = Q(({
  slot: r,
  clone: e,
  className: s,
  style: l
}, n) => {
  const t = X(), [o, c] = Z([]);
  return $(() => {
    var d;
    if (!t.current || !r)
      return;
    let i = r;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ae(n, a), s && a.classList.add(...s.split(" ")), l) {
        const _ = je(l);
        Object.keys(_).forEach((h) => {
          a.style[h] = _[h];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var p, b, v;
        (p = t.current) != null && p.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: h,
          clonedElement: g
        } = P(r);
        return i = g, c(h), i.style.display = "contents", m(), (v = t.current) == null || v.appendChild(i), h.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (d = t.current) == null || d.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [r, e, s, l, n]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...o);
});
function Y(r, e, s) {
  const l = r.filter(Boolean);
  if (l.length !== 0)
    return l.map((n, t) => {
      var m;
      if (typeof n != "object")
        return e != null && e.fallback ? e.fallback(n) : n;
      const o = {
        ...n.props,
        key: ((m = n.props) == null ? void 0 : m.key) ?? (s ? `${s}-${t}` : `${t}`)
      };
      let c = o;
      Object.keys(n.slots).forEach((u) => {
        if (!n.slots[u] || !(n.slots[u] instanceof Element) && !n.slots[u].el)
          return;
        const d = u.split(".");
        d.forEach((p, b) => {
          c[p] || (c[p] = {}), b !== d.length - 1 && (c = o[p]);
        });
        const a = n.slots[u];
        let _, h, g = (e == null ? void 0 : e.clone) ?? !1;
        a instanceof Element ? _ = a : (_ = a.el, h = a.callback, g = a.clone ?? g), c[d[d.length - 1]] = _ ? h ? (...p) => (h(d[d.length - 1], p), /* @__PURE__ */ y.jsx(z, {
          slot: _,
          clone: g
        })) : /* @__PURE__ */ y.jsx(z, {
          slot: _,
          clone: g
        }) : c[d[d.length - 1]], c = o;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return n[i] && (o[i] = Y(n[i], e, `${t}`)), o;
    });
}
const Fe = ke(({
  getContainer: r,
  getCurrentAnchor: e,
  children: s,
  items: l,
  slotItems: n,
  ...t
}) => {
  const o = M(r), c = M(e);
  return /* @__PURE__ */ y.jsxs(y.Fragment, {
    children: [s, /* @__PURE__ */ y.jsx(te, {
      ...t,
      items: G(() => l || Y(n, {
        clone: !0
      }), [l, n]),
      getContainer: o,
      getCurrentAnchor: c
    })]
  });
});
export {
  Fe as Anchor,
  Fe as default
};
