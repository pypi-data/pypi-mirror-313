import { g as te, w as x } from "./Index-DYdY5evZ.js";
const b = window.ms_globals.React, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, $ = window.ms_globals.React.useState, ee = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Dropdown;
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
var re = b, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(n, e, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (l in e) se.call(e, l) && !ie.hasOwnProperty(l) && (r[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) r[l] === void 0 && (r[l] = e[l]);
  return {
    $$typeof: oe,
    type: n,
    key: t,
    ref: s,
    props: r,
    _owner: ce.current
  };
}
S.Fragment = le;
S.jsx = q;
S.jsxs = q;
H.exports = S;
var g = H.exports;
const {
  SvelteComponent: ae,
  assign: L,
  binding_callbacks: F,
  check_outros: ue,
  children: B,
  claim_element: V,
  claim_space: de,
  component_subscribe: N,
  compute_slots: fe,
  create_slot: _e,
  detach: E,
  element: J,
  empty: T,
  exclude_internal_props: A,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: we,
  insert_hydration: I,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: be,
  transition_in: R,
  transition_out: P,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Ie
} = window.__gradio__svelte__internal;
function D(n) {
  let e, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = _e(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = J("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = V(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = B(e);
      r && r.l(s), s.forEach(E), this.h();
    },
    h() {
      Y(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      I(t, e, s), r && r.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && ye(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? pe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : me(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (R(r, t), o = !0);
    },
    o(t) {
      P(r, t), o = !1;
    },
    d(t) {
      t && E(e), r && r.d(t), n[9](null);
    }
  };
}
function Re(n) {
  let e, o, l, r, t = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      e = J("react-portal-target"), o = be(), t && t.c(), l = T(), this.h();
    },
    l(s) {
      e = V(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), B(e).forEach(E), o = de(s), t && t.l(s), l = T(), this.h();
    },
    h() {
      Y(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      I(s, e, c), n[8](e), I(s, o, c), t && t.m(s, c), I(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && R(t, 1)) : (t = D(s), t.c(), R(t, 1), t.m(l.parentNode, l)) : t && (he(), P(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(s) {
      r || (R(t), r = !0);
    },
    o(s) {
      P(t), r = !1;
    },
    d(s) {
      s && (E(e), E(o), E(l)), n[8](null), t && t.d(s);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function Ce(n, e, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = fe(t);
  let {
    svelteInit: i
  } = e;
  const p = x(W(e)), u = x();
  N(n, u, (f) => o(0, l = f));
  const d = x();
  N(n, d, (f) => o(1, r = f));
  const a = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: w,
    subSlotIndex: h
  } = te() || {}, y = i({
    parent: _,
    props: p,
    target: u,
    slot: d,
    slotKey: m,
    slotIndex: w,
    subSlotIndex: h,
    onDestroy(f) {
      a.push(f);
    }
  });
  Ie("$$ms-gr-react-wrapper", y), Ee(() => {
    p.set(W(e));
  }), xe(() => {
    a.forEach((f) => f());
  });
  function v(f) {
    F[f ? "unshift" : "push"](() => {
      l = f, u.set(l);
    });
  }
  function Q(f) {
    F[f ? "unshift" : "push"](() => {
      r = f, d.set(r);
    });
  }
  return n.$$set = (f) => {
    o(17, e = L(L({}, e), A(f))), "svelteInit" in f && o(5, i = f.svelteInit), "$$scope" in f && o(6, s = f.$$scope);
  }, e = A(e), [l, r, u, d, c, i, s, t, v, Q];
}
class Se extends ae {
  constructor(e) {
    super(), we(this, e, Ce, Re, ge, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, k = window.ms_globals.tree;
function ke(n) {
  function e(o) {
    const l = x(), r = new Se({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, c = t.parent ?? k;
          return c.nodes = [...c.nodes, s], M({
            createPortal: O,
            node: k
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), M({
              createPortal: O,
              node: k
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
      o(e);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const l = n[o];
    return typeof l == "number" && !Oe.includes(o) ? e[o] = l + "px" : e[o] = l, e;
  }, {}) : {};
}
function j(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(O(b.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: b.Children.toArray(n._reactElement.props.children).map((r) => {
        if (b.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = j(r.props.el);
          return b.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...b.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
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
    const t = l[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(t);
      e.push(...c), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function je(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const C = X(({
  slot: n,
  clone: e,
  className: o,
  style: l
}, r) => {
  const t = Z(), [s, c] = $([]);
  return ee(() => {
    var d;
    if (!t.current || !n)
      return;
    let i = n;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), je(r, a), o && a.classList.add(...o.split(" ")), l) {
        const _ = Pe(l);
        Object.keys(_).forEach((m) => {
          a.style[m] = _[m];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var h, y, v;
        (h = t.current) != null && h.contains(i) && ((y = t.current) == null || y.removeChild(i));
        const {
          portals: m,
          clonedElement: w
        } = j(n);
        return i = w, c(m), i.style.display = "contents", p(), (v = t.current) == null || v.appendChild(i), m.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (d = t.current) == null || d.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, e, o, l, r]), b.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Fe(n, e = !1) {
  try {
    if (e && !Le(n))
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
function z(n, e) {
  return U(() => Fe(n, e), [n, e]);
}
function K(n, e, o) {
  const l = n.filter(Boolean);
  if (l.length !== 0)
    return l.map((r, t) => {
      var p;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const s = {
        ...r.props,
        key: ((p = r.props) == null ? void 0 : p.key) ?? (o ? `${o}-${t}` : `${t}`)
      };
      let c = s;
      Object.keys(r.slots).forEach((u) => {
        if (!r.slots[u] || !(r.slots[u] instanceof Element) && !r.slots[u].el)
          return;
        const d = u.split(".");
        d.forEach((h, y) => {
          c[h] || (c[h] = {}), y !== d.length - 1 && (c = s[h]);
        });
        const a = r.slots[u];
        let _, m, w = (e == null ? void 0 : e.clone) ?? !1;
        a instanceof Element ? _ = a : (_ = a.el, m = a.callback, w = a.clone ?? w), c[d[d.length - 1]] = _ ? m ? (...h) => (m(d[d.length - 1], h), /* @__PURE__ */ g.jsx(C, {
          slot: _,
          clone: w
        })) : /* @__PURE__ */ g.jsx(C, {
          slot: _,
          clone: w
        }) : c[d[d.length - 1]], c = s;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return r[i] && (s[i] = K(r[i], e, `${t}`)), s;
    });
}
function Ne(n, e) {
  return n ? /* @__PURE__ */ g.jsx(C, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function G({
  key: n,
  setSlotParams: e,
  slots: o
}, l) {
  return o[n] ? (...r) => (e(n, r), Ne(o[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ae = ke(({
  getPopupContainer: n,
  innerStyle: e,
  children: o,
  slots: l,
  menuItems: r,
  dropdownRender: t,
  setSlotParams: s,
  ...c
}) => {
  var u, d, a;
  const i = z(n), p = z(t);
  return /* @__PURE__ */ g.jsx(g.Fragment, {
    children: /* @__PURE__ */ g.jsx(ne, {
      ...c,
      menu: {
        ...c.menu,
        items: U(() => {
          var _;
          return ((_ = c.menu) == null ? void 0 : _.items) || K(r, {
            clone: !0
          });
        }, [r, (u = c.menu) == null ? void 0 : u.items]),
        expandIcon: l["menu.expandIcon"] ? G({
          slots: l,
          setSlotParams: s,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) : (d = c.menu) == null ? void 0 : d.expandIcon,
        overflowedIndicator: l["menu.overflowedIndicator"] ? /* @__PURE__ */ g.jsx(C, {
          slot: l["menu.overflowedIndicator"]
        }) : (a = c.menu) == null ? void 0 : a.overflowedIndicator
      },
      getPopupContainer: i,
      dropdownRender: l.dropdownRender ? G({
        slots: l,
        setSlotParams: s,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : p,
      children: /* @__PURE__ */ g.jsx("div", {
        className: "ms-gr-antd-dropdown-content",
        style: {
          display: "inline-block",
          ...e
        },
        children: o
      })
    })
  });
});
export {
  Ae as Dropdown,
  Ae as default
};
