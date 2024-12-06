import { g as $, w as v } from "./Index-CPzJFWTM.js";
const h = window.ms_globals.React, J = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, Q = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Popconfirm;
var z = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = h, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(t, n, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (l in n) re.call(n, l) && !le.hasOwnProperty(l) && (o[l] = n[l]);
  if (t && t.defaultProps) for (l in n = t.defaultProps, n) o[l] === void 0 && (o[l] = n[l]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: s,
    props: o,
    _owner: se.current
  };
}
R.Fragment = oe;
R.jsx = G;
R.jsxs = G;
z.exports = R;
var m = z.exports;
const {
  SvelteComponent: ie,
  assign: j,
  binding_callbacks: L,
  check_outros: ce,
  children: U,
  claim_element: H,
  claim_space: ae,
  component_subscribe: B,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: K,
  empty: F,
  exclude_internal_props: N,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: P,
  safe_not_equal: he,
  set_custom_element_data: q,
  space: ge,
  transition_in: C,
  transition_out: O,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: xe
} = window.__gradio__svelte__internal;
function A(t) {
  let n, r;
  const l = (
    /*#slots*/
    t[7].default
  ), o = de(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = K("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      n = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(n);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      P(e, n, s), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && we(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? pe(
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
      r || (C(o, e), r = !0);
    },
    o(e) {
      O(o, e), r = !1;
    },
    d(e) {
      e && w(n), o && o.d(e), t[9](null);
    }
  };
}
function ve(t) {
  let n, r, l, o, e = (
    /*$$slots*/
    t[4].default && A(t)
  );
  return {
    c() {
      n = K("react-portal-target"), r = ge(), e && e.c(), l = F(), this.h();
    },
    l(s) {
      n = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(n).forEach(w), r = ae(s), e && e.l(s), l = F(), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      P(s, n, c), t[8](n), P(s, r, c), e && e.m(s, c), P(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = A(s), e.c(), C(e, 1), e.m(l.parentNode, l)) : e && (_e(), O(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (C(e), o = !0);
    },
    o(s) {
      O(e), o = !1;
    },
    d(s) {
      s && (w(n), w(r), w(l)), t[8](null), e && e.d(s);
    }
  };
}
function W(t) {
  const {
    svelteInit: n,
    ...r
  } = t;
  return r;
}
function Pe(t, n, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const c = ue(e);
  let {
    svelteInit: i
  } = n;
  const b = v(W(n)), d = v();
  B(t, d, (a) => r(0, l = a));
  const _ = v();
  B(t, _, (a) => r(1, o = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: k,
    subSlotIndex: y
  } = $() || {}, E = i({
    parent: f,
    props: b,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: k,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  xe("$$ms-gr-react-wrapper", E), be(() => {
    b.set(W(n));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function x(a) {
    L[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function V(a) {
    L[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  return t.$$set = (a) => {
    r(17, n = j(j({}, n), N(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, n = N(n), [l, o, d, _, c, i, s, e, x, V];
}
class Ce extends ie {
  constructor(n) {
    super(), me(this, n, Pe, ve, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, S = window.ms_globals.tree;
function Re(t) {
  function n(r) {
    const l = v(), o = new Ce({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? S;
          return c.nodes = [...c.nodes, s], D({
            createPortal: I,
            node: S
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: I,
              node: S
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
      r(n);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const l = t[r];
    return typeof l == "number" && !ke.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function T(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(I(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = T(o.props.el);
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
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = T(e);
      n.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function Ie(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const g = J(({
  slot: t,
  clone: n,
  className: r,
  style: l
}, o) => {
  const e = Y(), [s, c] = Q([]);
  return X(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function b() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Ie(o, u), r && u.classList.add(...r.split(" ")), l) {
        const f = Se(l);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var y, E, x;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: k
        } = T(t);
        return i = k, c(p), i.style.display = "contents", b(), (x = e.current) == null || x.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", b(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, r, l, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Oe(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Te(t, n = !1) {
  try {
    if (n && !Oe(t))
      return;
    if (typeof t == "string") {
      let r = t.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function M(t, n) {
  return Z(() => Te(t, n), [t, n]);
}
const Le = Re(({
  slots: t,
  afterOpenChange: n,
  getPopupContainer: r,
  children: l,
  ...o
}) => {
  var c, i;
  const e = M(n), s = M(r);
  return /* @__PURE__ */ m.jsx(ee, {
    ...o,
    afterOpenChange: e,
    getPopupContainer: s,
    okText: t.okText ? /* @__PURE__ */ m.jsx(g, {
      slot: t.okText
    }) : o.okText,
    okButtonProps: {
      ...o.okButtonProps || {},
      icon: t["okButtonProps.icon"] ? /* @__PURE__ */ m.jsx(g, {
        slot: t["okButtonProps.icon"]
      }) : (c = o.okButtonProps) == null ? void 0 : c.icon
    },
    cancelText: t.cancelText ? /* @__PURE__ */ m.jsx(g, {
      slot: t.cancelText
    }) : o.cancelText,
    cancelButtonProps: {
      ...o.cancelButtonProps || {},
      icon: t["cancelButtonProps.icon"] ? /* @__PURE__ */ m.jsx(g, {
        slot: t["cancelButtonProps.icon"]
      }) : (i = o.cancelButtonProps) == null ? void 0 : i.icon
    },
    title: t.title ? /* @__PURE__ */ m.jsx(g, {
      slot: t.title
    }) : o.title,
    description: t.description ? /* @__PURE__ */ m.jsx(g, {
      slot: t.description
    }) : o.description,
    children: l
  });
});
export {
  Le as Popconfirm,
  Le as default
};
