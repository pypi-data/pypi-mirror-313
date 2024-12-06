import { g as $, w as x } from "./Index-CUKHMizi.js";
const b = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Checkbox;
var W = {
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
var te = b, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(r, t, s) {
  var l, n = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (l in t) oe.call(t, l) && !le.hasOwnProperty(l) && (n[l] = t[l]);
  if (r && r.defaultProps) for (l in t = r.defaultProps, t) n[l] === void 0 && (n[l] = t[l]);
  return {
    $$typeof: ne,
    type: r,
    key: e,
    ref: o,
    props: n,
    _owner: se.current
  };
}
k.Fragment = re;
k.jsx = z;
k.jsxs = z;
W.exports = k;
var E = W.exports;
const {
  SvelteComponent: ie,
  assign: j,
  binding_callbacks: L,
  check_outros: ce,
  children: U,
  claim_element: H,
  claim_space: ae,
  component_subscribe: T,
  compute_slots: ue,
  create_slot: de,
  detach: y,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: B,
  space: ge,
  transition_in: R,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function D(r) {
  let t, s;
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
      C(e, t, o), n && n.m(t, null), r[9](t), s = !0;
    },
    p(e, o) {
      n && n.p && (!s || o & /*$$scope*/
      64) && be(
        n,
        l,
        e,
        /*$$scope*/
        e[6],
        s ? pe(
          l,
          /*$$scope*/
          e[6],
          o,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (R(n, e), s = !0);
    },
    o(e) {
      O(n, e), s = !1;
    },
    d(e) {
      e && y(t), n && n.d(e), r[9](null);
    }
  };
}
function xe(r) {
  let t, s, l, n, e = (
    /*$$slots*/
    r[4].default && D(r)
  );
  return {
    c() {
      t = q("react-portal-target"), s = ge(), e && e.c(), l = N(), this.h();
    },
    l(o) {
      t = H(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(y), s = ae(o), e && e.l(o), l = N(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      C(o, t, i), r[8](t), C(o, s, i), e && e.m(o, i), C(o, l, i), n = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && R(e, 1)) : (e = D(o), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (_e(), O(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(o) {
      n || (R(e), n = !0);
    },
    o(o) {
      O(e), n = !1;
    },
    d(o) {
      o && (y(t), y(s), y(l)), r[8](null), e && e.d(o);
    }
  };
}
function G(r) {
  const {
    svelteInit: t,
    ...s
  } = r;
  return s;
}
function Ce(r, t, s) {
  let l, n, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = ue(e);
  let {
    svelteInit: c
  } = t;
  const m = x(G(t)), u = x();
  T(r, u, (d) => s(0, l = d));
  const f = x();
  T(r, f, (d) => s(1, n = d));
  const a = [], p = Ee("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: h
  } = $() || {}, w = c({
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
  ve("$$ms-gr-react-wrapper", w), we(() => {
    m.set(G(t));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    L[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function J(d) {
    L[d ? "unshift" : "push"](() => {
      n = d, f.set(n);
    });
  }
  return r.$$set = (d) => {
    s(17, t = j(j({}, t), A(d))), "svelteInit" in d && s(5, c = d.svelteInit), "$$scope" in d && s(6, o = d.$$scope);
  }, t = A(t), [l, n, u, f, i, c, o, e, v, J];
}
class Re extends ie {
  constructor(t) {
    super(), he(this, t, Ce, xe, me, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, I = window.ms_globals.tree;
function ke(r) {
  function t(s) {
    const l = x(), n = new Re({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? I;
          return i.nodes = [...i.nodes, o], F({
            createPortal: S,
            node: I
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), F({
              createPortal: S,
              node: I
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
      s(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(r) {
  return r ? Object.keys(r).reduce((t, s) => {
    const l = r[s];
    return typeof l == "number" && !Ie.includes(s) ? t[s] = l + "px" : t[s] = l, t;
  }, {}) : {};
}
function P(r) {
  const t = [], s = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(S(b.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: b.Children.toArray(r._reactElement.props.children).map((n) => {
        if (b.isValidElement(n) && n.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = P(n.props.el);
          return b.cloneElement(n, {
            ...n.props,
            el: o,
            children: [...b.Children.toArray(n.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(r.getEventListeners()).forEach((n) => {
    r.getEventListeners(n).forEach(({
      listener: o,
      type: i,
      useCapture: c
    }) => {
      s.addEventListener(i, o, c);
    });
  });
  const l = Array.from(r.childNodes);
  for (let n = 0; n < l.length; n++) {
    const e = l[n];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: i
      } = P(e);
      t.push(...i), s.appendChild(o);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function Oe(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const M = Y(({
  slot: r,
  clone: t,
  className: s,
  style: l
}, n) => {
  const e = K(), [o, i] = Q([]);
  return X(() => {
    var f;
    if (!e.current || !r)
      return;
    let c = r;
    function m() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(n, a), s && a.classList.add(...s.split(" ")), l) {
        const p = Se(l);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var h, w, v;
        (h = e.current) != null && h.contains(c) && ((w = e.current) == null || w.removeChild(c));
        const {
          portals: _,
          clonedElement: g
        } = P(r);
        return c = g, i(_), c.style.display = "contents", m(), (v = e.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(r, {
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
  }, [r, t, s, l, n]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
});
function V(r, t, s) {
  const l = r.filter(Boolean);
  if (l.length !== 0)
    return l.map((n, e) => {
      var m;
      if (typeof n != "object")
        return n;
      const o = {
        ...n.props,
        key: ((m = n.props) == null ? void 0 : m.key) ?? (s ? `${s}-${e}` : `${e}`)
      };
      let i = o;
      Object.keys(n.slots).forEach((u) => {
        if (!n.slots[u] || !(n.slots[u] instanceof Element) && !n.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((h, w) => {
          i[h] || (i[h] = {}), w !== f.length - 1 && (i = o[h]);
        });
        const a = n.slots[u];
        let p, _, g = !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, g = a.clone ?? g), i[f[f.length - 1]] = p ? _ ? (...h) => (_(f[f.length - 1], h), /* @__PURE__ */ E.jsx(M, {
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
const je = ke(({
  onValueChange: r,
  onChange: t,
  elRef: s,
  optionItems: l,
  options: n,
  children: e,
  ...o
}) => /* @__PURE__ */ E.jsxs(E.Fragment, {
  children: [/* @__PURE__ */ E.jsx("div", {
    style: {
      display: "none"
    },
    children: e
  }), /* @__PURE__ */ E.jsx(ee.Group, {
    ...o,
    ref: s,
    options: Z(() => n || V(l), [l, n]),
    onChange: (i) => {
      t == null || t(i), r(i);
    }
  })]
}));
export {
  je as CheckboxGroup,
  je as default
};
