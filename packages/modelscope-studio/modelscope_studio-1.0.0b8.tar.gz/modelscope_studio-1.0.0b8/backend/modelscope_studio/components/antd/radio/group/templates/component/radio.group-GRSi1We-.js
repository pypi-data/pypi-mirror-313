import { g as $, w as x } from "./Index-Db395FKl.js";
const w = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.internalContext.FormItemContext, te = window.ms_globals.antd.Radio;
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
var ne = w, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(r, t, l) {
  var s, n = {}, e = null, o = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) le.call(t, s) && !ie.hasOwnProperty(s) && (n[s] = t[s]);
  if (r && r.defaultProps) for (s in t = r.defaultProps, t) n[s] === void 0 && (n[s] = t[s]);
  return {
    $$typeof: re,
    type: r,
    key: e,
    ref: o,
    props: n,
    _owner: se.current
  };
}
I.Fragment = oe;
I.jsx = z;
I.jsxs = z;
W.exports = I;
var E = W.exports;
const {
  SvelteComponent: ce,
  assign: j,
  binding_callbacks: L,
  check_outros: ae,
  children: U,
  claim_element: H,
  claim_space: ue,
  component_subscribe: T,
  compute_slots: de,
  create_slot: fe,
  detach: y,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: C,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: we,
  transition_in: R,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function F(r) {
  let t, l;
  const s = (
    /*#slots*/
    r[7].default
  ), n = fe(
    s,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = U(t);
      n && n.l(o), o.forEach(y), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      C(e, t, o), n && n.m(t, null), r[9](t), l = !0;
    },
    p(e, o) {
      n && n.p && (!l || o & /*$$scope*/
      64) && be(
        n,
        s,
        e,
        /*$$scope*/
        e[6],
        l ? _e(
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
      l || (R(n, e), l = !0);
    },
    o(e) {
      k(n, e), l = !1;
    },
    d(e) {
      e && y(t), n && n.d(e), r[9](null);
    }
  };
}
function Ce(r) {
  let t, l, s, n, e = (
    /*$$slots*/
    r[4].default && F(r)
  );
  return {
    c() {
      t = q("react-portal-target"), l = we(), e && e.c(), s = N(), this.h();
    },
    l(o) {
      t = H(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(y), l = ue(o), e && e.l(o), s = N(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      C(o, t, i), r[8](t), C(o, l, i), e && e.m(o, i), C(o, s, i), n = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && R(e, 1)) : (e = F(o), e.c(), R(e, 1), e.m(s.parentNode, s)) : e && (me(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(o) {
      n || (R(e), n = !0);
    },
    o(o) {
      k(e), n = !1;
    },
    d(o) {
      o && (y(t), y(l), y(s)), r[8](null), e && e.d(o);
    }
  };
}
function D(r) {
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
  const i = de(e);
  let {
    svelteInit: c
  } = t;
  const h = x(D(t)), u = x();
  T(r, u, (d) => l(0, s = d));
  const f = x();
  T(r, f, (d) => l(1, n = d));
  const a = [], p = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: m
  } = $() || {}, b = c({
    parent: p,
    props: h,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: g,
    subSlotIndex: m,
    onDestroy(d) {
      a.push(d);
    }
  });
  xe("$$ms-gr-react-wrapper", b), Ee(() => {
    h.set(D(t));
  }), ve(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    L[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function J(d) {
    L[d ? "unshift" : "push"](() => {
      n = d, f.set(n);
    });
  }
  return r.$$set = (d) => {
    l(17, t = j(j({}, t), A(d))), "svelteInit" in d && l(5, c = d.svelteInit), "$$scope" in d && l(6, o = d.$$scope);
  }, t = A(t), [s, n, u, f, i, c, o, e, v, J];
}
class Ie extends ce {
  constructor(t) {
    super(), he(this, t, Re, Ce, ge, {
      svelteInit: 5
    });
  }
}
const G = window.ms_globals.rerender, S = window.ms_globals.tree;
function Se(r) {
  function t(l) {
    const s = x(), n = new Ie({
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
          }, i = e.parent ?? S;
          return i.nodes = [...i.nodes, o], G({
            createPortal: O,
            node: S
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), G({
              createPortal: O,
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
function ke(r) {
  return r ? Object.keys(r).reduce((t, l) => {
    const s = r[l];
    return typeof s == "number" && !Oe.includes(l) ? t[l] = s + "px" : t[l] = s, t;
  }, {}) : {};
}
function P(r) {
  const t = [], l = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(O(w.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: w.Children.toArray(r._reactElement.props.children).map((n) => {
        if (w.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = P(n.props.el);
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
      type: i,
      useCapture: c
    }) => {
      l.addEventListener(i, o, c);
    });
  });
  const s = Array.from(r.childNodes);
  for (let n = 0; n < s.length; n++) {
    const e = s[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: i
      } = P(e);
      t.push(...i), l.appendChild(o);
    } else e.nodeType === 3 && l.appendChild(e.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function Pe(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const M = Y(({
  slot: r,
  clone: t,
  className: l,
  style: s
}, n) => {
  const e = K(), [o, i] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !r)
      return;
    let c = r;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(n, a), l && a.classList.add(...l.split(" ")), s) {
        const p = ke(s);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var m, b, v;
        (m = e.current) != null && m.contains(c) && ((b = e.current) == null || b.removeChild(c));
        const {
          portals: _,
          clonedElement: g
        } = P(r);
        return c = g, i(_), c.style.display = "contents", h(), (v = e.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((p = e.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [r, t, l, s, n]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
});
function V(r, t, l) {
  const s = r.filter(Boolean);
  if (s.length !== 0)
    return s.map((n, e) => {
      var h;
      if (typeof n != "object")
        return n;
      const o = {
        ...n.props,
        key: ((h = n.props) == null ? void 0 : h.key) ?? (l ? `${l}-${e}` : `${e}`)
      };
      let i = o;
      Object.keys(n.slots).forEach((u) => {
        if (!n.slots[u] || !(n.slots[u] instanceof Element) && !n.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((m, b) => {
          i[m] || (i[m] = {}), b !== f.length - 1 && (i = o[m]);
        });
        const a = n.slots[u];
        let p, _, g = !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, g = a.clone ?? g), i[f[f.length - 1]] = p ? _ ? (...m) => (_(f[f.length - 1], m), /* @__PURE__ */ E.jsx(M, {
          slot: p,
          clone: g
        })) : /* @__PURE__ */ E.jsx(M, {
          slot: p,
          clone: g
        }) : i[f[f.length - 1]], i = o;
      });
      const c = "children";
      return n[c] && (o[c] = V(n[c], t, `${e}`)), o;
    });
}
const Le = Se(({
  onValueChange: r,
  onChange: t,
  elRef: l,
  optionItems: s,
  options: n,
  children: e,
  ...o
}) => /* @__PURE__ */ E.jsx(E.Fragment, {
  children: /* @__PURE__ */ E.jsx(te.Group, {
    ...o,
    ref: l,
    options: Z(() => n || V(s), [s, n]),
    onChange: (i) => {
      t == null || t(i), r(i.target.value);
    },
    children: /* @__PURE__ */ E.jsx(ee.Provider, {
      value: null,
      children: e
    })
  })
}));
export {
  Le as RadioGroup,
  Le as default
};
