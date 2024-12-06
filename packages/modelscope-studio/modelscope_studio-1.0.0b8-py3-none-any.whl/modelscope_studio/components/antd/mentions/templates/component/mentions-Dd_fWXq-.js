import { b as ee, g as te, w as C } from "./Index-HR2C9qZn.js";
const b = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, O = window.ms_globals.React.useRef, G = window.ms_globals.React.useState, P = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Mentions;
function re(n, e) {
  return ee(n, e);
}
var H = {
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
var se = b, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ie = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(n, e, s) {
  var l, r = {}, t = null, o = null;
  s !== void 0 && (t = "" + s), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (l in e) ce.call(e, l) && !ae.hasOwnProperty(l) && (r[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) r[l] === void 0 && (r[l] = e[l]);
  return {
    $$typeof: oe,
    type: n,
    key: t,
    ref: o,
    props: r,
    _owner: ie.current
  };
}
S.Fragment = le;
S.jsx = B;
S.jsxs = B;
H.exports = S;
var E = H.exports;
const {
  SvelteComponent: ue,
  assign: N,
  binding_callbacks: A,
  check_outros: de,
  children: J,
  claim_element: Y,
  claim_space: fe,
  component_subscribe: M,
  compute_slots: _e,
  create_slot: pe,
  detach: y,
  element: K,
  empty: V,
  exclude_internal_props: W,
  get_all_dirty_from_scope: he,
  get_slot_changes: me,
  group_outros: ge,
  init: we,
  insert_hydration: R,
  safe_not_equal: be,
  set_custom_element_data: Q,
  space: Ee,
  transition_in: x,
  transition_out: F,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: Ce,
  onDestroy: Re,
  setContext: xe
} = window.__gradio__svelte__internal;
function D(n) {
  let e, s;
  const l = (
    /*#slots*/
    n[7].default
  ), r = pe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = Y(t, "SVELTE-SLOT", {
        class: !0
      });
      var o = J(e);
      r && r.l(o), o.forEach(y), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      R(t, e, o), r && r.m(e, null), n[9](e), s = !0;
    },
    p(t, o) {
      r && r.p && (!s || o & /*$$scope*/
      64) && ye(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        s ? me(
          l,
          /*$$scope*/
          t[6],
          o,
          null
        ) : he(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      s || (x(r, t), s = !0);
    },
    o(t) {
      F(r, t), s = !1;
    },
    d(t) {
      t && y(e), r && r.d(t), n[9](null);
    }
  };
}
function Se(n) {
  let e, s, l, r, t = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      e = K("react-portal-target"), s = Ee(), t && t.c(), l = V(), this.h();
    },
    l(o) {
      e = Y(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(e).forEach(y), s = fe(o), t && t.l(o), l = V(), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      R(o, e, c), n[8](e), R(o, s, c), t && t.m(o, c), R(o, l, c), r = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, c), c & /*$$slots*/
      16 && x(t, 1)) : (t = D(o), t.c(), x(t, 1), t.m(l.parentNode, l)) : t && (ge(), F(t, 1, 1, () => {
        t = null;
      }), de());
    },
    i(o) {
      r || (x(t), r = !0);
    },
    o(o) {
      F(t), r = !1;
    },
    d(o) {
      o && (y(e), y(s), y(l)), n[8](null), t && t.d(o);
    }
  };
}
function q(n) {
  const {
    svelteInit: e,
    ...s
  } = n;
  return s;
}
function Ie(n, e, s) {
  let l, r, {
    $$slots: t = {},
    $$scope: o
  } = e;
  const c = _e(t);
  let {
    svelteInit: i
  } = e;
  const m = C(q(e)), u = C();
  M(n, u, (d) => s(0, l = d));
  const f = C();
  M(n, f, (d) => s(1, r = d));
  const a = [], _ = Ce("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: h
  } = te() || {}, w = i({
    parent: _,
    props: m,
    target: u,
    slot: f,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: h,
    onDestroy(d) {
      a.push(d);
    }
  });
  xe("$$ms-gr-react-wrapper", w), ve(() => {
    m.set(q(e));
  }), Re(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    A[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function Z(d) {
    A[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return n.$$set = (d) => {
    s(17, e = N(N({}, e), W(d))), "svelteInit" in d && s(5, i = d.svelteInit), "$$scope" in d && s(6, o = d.$$scope);
  }, e = W(e), [l, r, u, f, c, i, o, t, v, Z];
}
class ke extends ue {
  constructor(e) {
    super(), we(this, e, Ie, Se, be, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, I = window.ms_globals.tree;
function Oe(n) {
  function e(s) {
    const l = C(), r = new ke({
      ...s,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? I;
          return c.nodes = [...c.nodes, o], z({
            createPortal: j,
            node: I
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), z({
              createPortal: j,
              node: I
            });
          }), o;
        },
        ...s.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(e);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((e, s) => {
    const l = n[s];
    return typeof l == "number" && !Pe.includes(s) ? e[s] = l + "px" : e[s] = l, e;
  }, {}) : {};
}
function L(n) {
  const e = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(j(b.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: b.Children.toArray(n._reactElement.props.children).map((r) => {
        if (b.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: o
          } = L(r.props.el);
          return b.cloneElement(r, {
            ...r.props,
            el: o,
            children: [...b.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: o,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, o, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const t = l[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = L(t);
      e.push(...c), s.appendChild(o);
    } else t.nodeType === 3 && s.appendChild(t.cloneNode());
  }
  return {
    clonedElement: s,
    portals: e
  };
}
function Fe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const T = $(({
  slot: n,
  clone: e,
  className: s,
  style: l
}, r) => {
  const t = O(), [o, c] = G([]);
  return P(() => {
    var f;
    if (!t.current || !n)
      return;
    let i = n;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Fe(r, a), s && a.classList.add(...s.split(" ")), l) {
        const _ = je(l);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var h, w, v;
        (h = t.current) != null && h.contains(i) && ((w = t.current) == null || w.removeChild(i));
        const {
          portals: p,
          clonedElement: g
        } = L(n);
        return i = g, c(p), i.style.display = "contents", m(), (v = t.current) == null || v.appendChild(i), p.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, e, s, l, r]), b.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...o);
});
function Le(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Te(n, e = !1) {
  try {
    if (e && !Le(n))
      return;
    if (typeof n == "string") {
      let s = n.trim();
      return s.startsWith(";") && (s = s.slice(1)), s.endsWith(";") && (s = s.slice(0, -1)), new Function(`return (...args) => (${s})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function k(n, e) {
  return U(() => Te(n, e), [n, e]);
}
function Ne({
  value: n,
  onValueChange: e
}) {
  const [s, l] = G(n), r = O(e);
  r.current = e;
  const t = O(s);
  return t.current = s, P(() => {
    r.current(s);
  }, [s]), P(() => {
    re(n, t.current) || l(n);
  }, [n]), [s, l];
}
function X(n, e, s) {
  const l = n.filter(Boolean);
  if (l.length !== 0)
    return l.map((r, t) => {
      var m;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const o = {
        ...r.props,
        key: ((m = r.props) == null ? void 0 : m.key) ?? (s ? `${s}-${t}` : `${t}`)
      };
      let c = o;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((h, w) => {
          c[h] || (c[h] = {}), w !== f.length - 1 && (c = o[h]);
        });
        const a = r.slots[u];
        let _, p, g = (e == null ? void 0 : e.clone) ?? !1;
        a instanceof Element ? _ = a : (_ = a.el, p = a.callback, g = a.clone ?? g), c[f[f.length - 1]] = _ ? p ? (...h) => (p(f[f.length - 1], h), /* @__PURE__ */ E.jsx(T, {
          slot: _,
          clone: g
        })) : /* @__PURE__ */ E.jsx(T, {
          slot: _,
          clone: g
        }) : c[f[f.length - 1]], c = o;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return r[i] && (o[i] = X(r[i], e, `${t}`)), o;
    });
}
const Me = Oe(({
  slots: n,
  children: e,
  onValueChange: s,
  filterOption: l,
  onChange: r,
  options: t,
  validateSearch: o,
  optionItems: c,
  getPopupContainer: i,
  elRef: m,
  ...u
}) => {
  const f = k(i), a = k(l), _ = k(o), [p, g] = Ne({
    onValueChange: s,
    value: u.value
  });
  return /* @__PURE__ */ E.jsxs(E.Fragment, {
    children: [/* @__PURE__ */ E.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ E.jsx(ne, {
      ...u,
      ref: m,
      value: p,
      options: U(() => t || X(c, {
        clone: !0
      }), [c, t]),
      onChange: (h, ...w) => {
        r == null || r(h, ...w), g(h);
      },
      validateSearch: _,
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ E.jsx(T, {
        slot: n.notFoundContent
      }) : u.notFoundContent,
      filterOption: a || l,
      getPopupContainer: f
    })]
  });
});
export {
  Me as Mentions,
  Me as default
};
