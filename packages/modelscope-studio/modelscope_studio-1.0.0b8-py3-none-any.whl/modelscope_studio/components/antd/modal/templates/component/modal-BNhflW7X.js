import { g as ee, w as C } from "./Index-BFgMncMU.js";
const w = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, $ = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Modal;
var G = {
  exports: {}
}, P = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = w, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(e, n, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) le.call(n, l) && !ce.hasOwnProperty(l) && (r[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) r[l] === void 0 && (r[l] = n[l]);
  return {
    $$typeof: oe,
    type: e,
    key: t,
    ref: s,
    props: r,
    _owner: se.current
  };
}
P.Fragment = re;
P.jsx = U;
P.jsxs = U;
G.exports = P;
var m = G.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: F,
  check_outros: ae,
  children: H,
  claim_element: K,
  claim_space: ue,
  component_subscribe: B,
  compute_slots: de,
  create_slot: fe,
  detach: b,
  element: q,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: _e,
  get_slot_changes: me,
  group_outros: pe,
  init: he,
  insert_hydration: R,
  safe_not_equal: ge,
  set_custom_element_data: V,
  space: we,
  transition_in: I,
  transition_out: T,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: xe,
  setContext: ve
} = window.__gradio__svelte__internal;
function M(e) {
  let n, o;
  const l = (
    /*#slots*/
    e[7].default
  ), r = fe(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = q("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(n);
      r && r.l(s), s.forEach(b), this.h();
    },
    h() {
      V(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      R(t, n, s), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && be(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? me(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : _e(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (I(r, t), o = !0);
    },
    o(t) {
      T(r, t), o = !1;
    },
    d(t) {
      t && b(n), r && r.d(t), e[9](null);
    }
  };
}
function Ce(e) {
  let n, o, l, r, t = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      n = q("react-portal-target"), o = we(), t && t.c(), l = N(), this.h();
    },
    l(s) {
      n = K(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(b), o = ue(s), t && t.l(s), l = N(), this.h();
    },
    h() {
      V(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      R(s, n, c), e[8](n), R(s, o, c), t && t.m(s, c), R(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && I(t, 1)) : (t = M(s), t.c(), I(t, 1), t.m(l.parentNode, l)) : t && (pe(), T(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(s) {
      r || (I(t), r = !0);
    },
    o(s) {
      T(t), r = !1;
    },
    d(s) {
      s && (b(n), b(o), b(l)), e[8](null), t && t.d(s);
    }
  };
}
function W(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function Re(e, n, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const c = de(t);
  let {
    svelteInit: i
  } = n;
  const g = C(W(n)), d = C();
  B(e, d, (u) => o(0, l = u));
  const _ = C();
  B(e, _, (u) => o(1, r = u));
  const a = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: k,
    subSlotIndex: y
  } = ee() || {}, E = i({
    parent: f,
    props: g,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: k,
    subSlotIndex: y,
    onDestroy(u) {
      a.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", E), ye(() => {
    g.set(W(n));
  }), xe(() => {
    a.forEach((u) => u());
  });
  function x(u) {
    F[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function J(u) {
    F[u ? "unshift" : "push"](() => {
      r = u, _.set(r);
    });
  }
  return e.$$set = (u) => {
    o(17, n = L(L({}, n), A(u))), "svelteInit" in u && o(5, i = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, n = A(n), [l, r, d, _, c, i, s, t, x, J];
}
class Ie extends ie {
  constructor(n) {
    super(), he(this, n, Re, Ce, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, S = window.ms_globals.tree;
function Pe(e) {
  function n(o) {
    const l = C(), r = new Ie({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? S;
          return c.nodes = [...c.nodes, s], D({
            createPortal: O,
            node: S
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: O,
              node: S
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
      o(n);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !ke.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function j(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(O(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((r) => {
        if (w.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = j(r.props.el);
          return w.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...w.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const t = l[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(t);
      n.push(...c), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Oe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const h = Y(({
  slot: e,
  clone: n,
  className: o,
  style: l
}, r) => {
  const t = Q(), [s, c] = X([]);
  return Z(() => {
    var _;
    if (!t.current || !e)
      return;
    let i = e;
    function g() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(r, a), o && a.classList.add(...o.split(" ")), l) {
        const f = Se(l);
        Object.keys(f).forEach((p) => {
          a.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y, E, x;
        (y = t.current) != null && y.contains(i) && ((E = t.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: k
        } = j(e);
        return i = k, c(p), i.style.display = "contents", g(), (x = t.current) == null || x.appendChild(i), p.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (_ = t.current) == null || _.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((f = t.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, n, o, l, r]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Te(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function je(e, n = !1) {
  try {
    if (n && !Te(e))
      return;
    if (typeof e == "string") {
      let o = e.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function v(e, n) {
  return $(() => je(e, n), [e, n]);
}
function Le(e, n) {
  return e ? /* @__PURE__ */ m.jsx(h, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function z({
  key: e,
  setSlotParams: n,
  slots: o
}, l) {
  return o[e] ? (...r) => (n(e, r), Le(o[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Be = Pe(({
  slots: e,
  afterClose: n,
  afterOpenChange: o,
  getContainer: l,
  children: r,
  modalRender: t,
  setSlotParams: s,
  ...c
}) => {
  var a, f;
  const i = v(o), g = v(n), d = v(l), _ = v(t);
  return /* @__PURE__ */ m.jsx(te, {
    ...c,
    afterOpenChange: i,
    afterClose: g,
    okText: e.okText ? /* @__PURE__ */ m.jsx(h, {
      slot: e.okText
    }) : c.okText,
    okButtonProps: {
      ...c.okButtonProps || {},
      icon: e["okButtonProps.icon"] ? /* @__PURE__ */ m.jsx(h, {
        slot: e["okButtonProps.icon"]
      }) : (a = c.okButtonProps) == null ? void 0 : a.icon
    },
    cancelText: e.cancelText ? /* @__PURE__ */ m.jsx(h, {
      slot: e.cancelText
    }) : c.cancelText,
    cancelButtonProps: {
      ...c.cancelButtonProps || {},
      icon: e["cancelButtonProps.icon"] ? /* @__PURE__ */ m.jsx(h, {
        slot: e["cancelButtonProps.icon"]
      }) : (f = c.cancelButtonProps) == null ? void 0 : f.icon
    },
    closable: e["closable.closeIcon"] ? {
      ...typeof c.closable == "object" ? c.closable : {},
      closeIcon: /* @__PURE__ */ m.jsx(h, {
        slot: e["closable.closeIcon"]
      })
    } : c.closable,
    closeIcon: e.closeIcon ? /* @__PURE__ */ m.jsx(h, {
      slot: e.closeIcon
    }) : c.closeIcon,
    footer: e.footer ? z({
      slots: e,
      setSlotParams: s,
      key: "footer"
    }) : c.footer,
    title: e.title ? /* @__PURE__ */ m.jsx(h, {
      slot: e.title
    }) : c.title,
    modalRender: e.modalRender ? z({
      slots: e,
      setSlotParams: s,
      key: "modalRender"
    }) : _,
    getContainer: typeof l == "string" ? d : l,
    children: r
  });
});
export {
  Be as Modal,
  Be as default
};
