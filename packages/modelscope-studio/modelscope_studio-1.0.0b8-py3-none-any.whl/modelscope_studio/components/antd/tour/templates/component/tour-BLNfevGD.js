import { g as ee, w as R } from "./Index-BxQtsfIM.js";
const b = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, G = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tour;
var U = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = b, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) se.call(t, l) && !ie.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: le.current
  };
}
C.Fragment = oe;
C.jsx = H;
C.jsxs = H;
U.exports = C;
var w = U.exports;
const {
  SvelteComponent: ce,
  assign: T,
  binding_callbacks: L,
  check_outros: ae,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: E,
  element: V,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: he,
  init: me,
  insert_hydration: x,
  safe_not_equal: ge,
  set_custom_element_data: J,
  space: we,
  transition_in: I,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ve,
  setContext: Re
} = window.__gradio__svelte__internal;
function W(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = fe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = q(t);
      r && r.l(s), s.forEach(E), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      x(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && be(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (I(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && E(t), r && r.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      t = V("react-portal-target"), o = we(), e && e.c(), l = N(), this.h();
    },
    l(s) {
      t = B(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(E), o = ue(s), e && e.l(s), l = N(), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      x(s, t, i), n[8](t), x(s, o, i), e && e.m(s, i), x(s, l, i), r = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && I(e, 1)) : (e = W(s), e.c(), I(e, 1), e.m(l.parentNode, l)) : e && (he(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(s) {
      r || (I(e), r = !0);
    },
    o(s) {
      k(e), r = !1;
    },
    d(s) {
      s && (E(t), E(o), E(l)), n[8](null), e && e.d(s);
    }
  };
}
function D(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Ie(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = de(e);
  let {
    svelteInit: c
  } = t;
  const h = R(D(t)), u = R();
  F(n, u, (d) => o(0, l = d));
  const f = R();
  F(n, f, (d) => o(1, r = d));
  const a = [], p = Ee("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: m
  } = ee() || {}, y = c({
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
  Re("$$ms-gr-react-wrapper", y), ye(() => {
    h.set(D(t));
  }), ve(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    L[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function K(d) {
    L[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return n.$$set = (d) => {
    o(17, t = T(T({}, t), A(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, t = A(t), [l, r, u, f, i, c, s, e, v, K];
}
class Se extends ce {
  constructor(t) {
    super(), me(this, t, Ie, xe, ge, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const l = R(), r = new Se({
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
          }, i = e.parent ?? O;
          return i.nodes = [...i.nodes, s], M({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), M({
              createPortal: P,
              node: O
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
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Oe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function j(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(b.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: b.Children.toArray(n._reactElement.props.children).map((r) => {
        if (b.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(r.props.el);
          return b.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...b.Children.toArray(r.props.children), ...e]
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
      } = j(e);
      t.push(...i), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const S = Q(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = X(), [s, i] = Z([]);
  return $(() => {
    var f;
    if (!e.current || !n)
      return;
    let c = n;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(r, a), o && a.classList.add(...o.split(" ")), l) {
        const p = Pe(l);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var m, y, v;
        (m = e.current) != null && m.contains(c) && ((y = e.current) == null || y.removeChild(c));
        const {
          portals: _,
          clonedElement: g
        } = j(n);
        return c = g, i(_), c.style.display = "contents", h(), (v = e.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
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
  }, [n, t, o, l, r]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Te(n, t = !1) {
  try {
    if (t && !je(n))
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
  return G(() => Te(n, t), [n, t]);
}
function Y(n, t, o) {
  const l = n.filter(Boolean);
  if (l.length !== 0)
    return l.map((r, e) => {
      var h;
      if (typeof r != "object")
        return r;
      const s = {
        ...r.props,
        key: ((h = r.props) == null ? void 0 : h.key) ?? (o ? `${o}-${e}` : `${e}`)
      };
      let i = s;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const f = u.split(".");
        f.forEach((m, y) => {
          i[m] || (i[m] = {}), y !== f.length - 1 && (i = s[m]);
        });
        const a = r.slots[u];
        let p, _, g = !1;
        a instanceof Element ? p = a : (p = a.el, _ = a.callback, g = a.clone ?? g), i[f[f.length - 1]] = p ? _ ? (...m) => (_(f[f.length - 1], m), /* @__PURE__ */ w.jsx(S, {
          slot: p,
          clone: g
        })) : /* @__PURE__ */ w.jsx(S, {
          slot: p,
          clone: g
        }) : i[f[f.length - 1]], i = s;
      });
      const c = "children";
      return r[c] && (s[c] = Y(r[c], t, `${e}`)), s;
    });
}
function Le(n, t) {
  return n ? /* @__PURE__ */ w.jsx(S, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Fe({
  key: n,
  setSlotParams: t,
  slots: o
}, l) {
  return o[n] ? (...r) => (t(n, r), Le(o[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ae = Ce(({
  slots: n,
  steps: t,
  slotItems: o,
  children: l,
  onChange: r,
  onClose: e,
  getPopupContainer: s,
  setSlotParams: i,
  indicatorsRender: c,
  ...h
}) => {
  const u = z(s), f = z(c);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: l
    }), /* @__PURE__ */ w.jsx(te, {
      ...h,
      steps: G(() => t || Y(o), [t, o]),
      onChange: (a) => {
        r == null || r(a);
      },
      closeIcon: n.closeIcon ? /* @__PURE__ */ w.jsx(S, {
        slot: n.closeIcon
      }) : h.closeIcon,
      indicatorsRender: n.indicatorsRender ? Fe({
        slots: n,
        setSlotParams: i,
        key: "indicatorsRender"
      }) : f,
      getPopupContainer: u,
      onClose: (a, ...p) => {
        e == null || e(a, ...p);
      }
    })]
  });
});
export {
  Ae as Tour,
  Ae as default
};
