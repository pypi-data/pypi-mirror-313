import { g as X, w as E } from "./Index-DYr9PNLu.js";
const m = window.ms_globals.React, q = window.ms_globals.React.useMemo, V = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useState, Y = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.QRCode;
var D = {
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
var $ = m, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(n, e, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) ne.call(e, s) && !oe.hasOwnProperty(s) && (o[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: ee,
    type: n,
    key: t,
    ref: l,
    props: o,
    _owner: re.current
  };
}
C.Fragment = te;
C.jsx = M;
C.jsxs = M;
D.exports = C;
var z = D.exports;
const {
  SvelteComponent: se,
  assign: k,
  binding_callbacks: L,
  check_outros: le,
  children: G,
  claim_element: U,
  claim_space: ie,
  component_subscribe: T,
  compute_slots: ce,
  create_slot: ae,
  detach: h,
  element: H,
  empty: N,
  exclude_internal_props: j,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: _e,
  insert_hydration: v,
  safe_not_equal: pe,
  set_custom_element_data: K,
  space: me,
  transition_in: R,
  transition_out: O,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function A(n) {
  let e, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = ae(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = H("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = U(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = G(e);
      o && o.l(l), l.forEach(h), this.h();
    },
    h() {
      K(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      v(t, e, l), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && he(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? de(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : ue(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (R(o, t), r = !0);
    },
    o(t) {
      O(o, t), r = !1;
    },
    d(t) {
      t && h(e), o && o.d(t), n[9](null);
    }
  };
}
function Ee(n) {
  let e, r, s, o, t = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      e = H("react-portal-target"), r = me(), t && t.c(), s = N(), this.h();
    },
    l(l) {
      e = U(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(e).forEach(h), r = ie(l), t && t.l(l), s = N(), this.h();
    },
    h() {
      K(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, e, c), n[8](e), v(l, r, c), t && t.m(l, c), v(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && R(t, 1)) : (t = A(l), t.c(), R(t, 1), t.m(s.parentNode, s)) : t && (fe(), O(t, 1, 1, () => {
        t = null;
      }), le());
    },
    i(l) {
      o || (R(t), o = !0);
    },
    o(l) {
      O(t), o = !1;
    },
    d(l) {
      l && (h(e), h(r), h(s)), n[8](null), t && t.d(l);
    }
  };
}
function F(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function ve(n, e, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = ce(t);
  let {
    svelteInit: i
  } = e;
  const g = E(F(e)), d = E();
  T(n, d, (a) => r(0, s = a));
  const p = E();
  T(n, p, (a) => r(1, o = a));
  const u = [], f = we("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: w
  } = X() || {}, b = i({
    parent: f,
    props: g,
    target: d,
    slot: p,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: w,
    onDestroy(a) {
      u.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", b), ge(() => {
    g.set(F(e));
  }), be(() => {
    u.forEach((a) => a());
  });
  function y(a) {
    L[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function Q(a) {
    L[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, e = k(k({}, e), j(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, e = j(e), [s, o, d, p, c, i, l, t, y, Q];
}
class Re extends se {
  constructor(e) {
    super(), _e(this, e, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ce(n) {
  function e(r) {
    const s = E(), o = new Re({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? x;
          return c.nodes = [...c.nodes, l], W({
            createPortal: I,
            node: x
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), W({
              createPortal: I,
              node: x
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
function Se(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function xe(n, e = !1) {
  try {
    if (e && !Se(n))
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
function Ie(n, e) {
  return q(() => xe(n, e), [n, e]);
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const s = n[r];
    return typeof s == "number" && !Oe.includes(r) ? e[r] = s + "px" : e[r] = s, e;
  }, {}) : {};
}
function P(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(I(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = P(o.props.el);
          return m.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...m.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = P(t);
      e.push(...c), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function ke(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const Le = V(({
  slot: n,
  clone: e,
  className: r,
  style: s
}, o) => {
  const t = B(), [l, c] = J([]);
  return Y(() => {
    var p;
    if (!t.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(o, u), r && u.classList.add(...r.split(" ")), s) {
        const f = Pe(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var w, b, y;
        (w = t.current) != null && w.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = P(n);
        return i = S, c(_), i.style.display = "contents", g(), (y = t.current) == null || y.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (p = t.current) == null || p.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((f = t.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, e, r, s, o]), m.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Te(n, e) {
  return n ? /* @__PURE__ */ z.jsx(Le, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Ne({
  key: n,
  setSlotParams: e,
  slots: r
}, s) {
  return r[n] ? (...o) => (e(n, o), Te(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ae = Ce(({
  setSlotParams: n,
  slots: e,
  statusRender: r,
  ...s
}) => {
  const o = Ie(r);
  return /* @__PURE__ */ z.jsx(Z, {
    ...s,
    statusRender: e.statusRender ? Ne({
      slots: e,
      setSlotParams: n,
      key: "statusRender"
    }) : o
  });
});
export {
  Ae as QRCode,
  Ae as default
};
