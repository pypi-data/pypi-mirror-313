import { g as X, w as v } from "./Index-V4f3oCjq.js";
const h = window.ms_globals.React, V = window.ms_globals.React.useMemo, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Rate;
var M = {
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
var $ = h, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ne.call(t, s) && !oe.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: re.current
  };
}
x.Fragment = te;
x.jsx = z;
x.jsxs = z;
M.exports = x;
var w = M.exports;
const {
  SvelteComponent: se,
  assign: L,
  binding_callbacks: j,
  check_outros: le,
  children: G,
  claim_element: U,
  claim_space: ie,
  component_subscribe: T,
  compute_slots: ce,
  create_slot: ae,
  detach: g,
  element: H,
  empty: F,
  exclude_internal_props: N,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: _e,
  insert_hydration: R,
  safe_not_equal: pe,
  set_custom_element_data: K,
  space: me,
  transition_in: S,
  transition_out: P,
  update_slot_base: he
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: ye,
  setContext: be
} = window.__gradio__svelte__internal;
function A(n) {
  let t, r;
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
      t = H("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = G(t);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      R(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && he(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? de(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ue(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (S(o, e), r = !0);
    },
    o(e) {
      P(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Ee(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      t = H("react-portal-target"), r = me(), e && e.c(), s = F(), this.h();
    },
    l(l) {
      t = U(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(t).forEach(g), r = ie(l), e && e.l(l), s = F(), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      R(l, t, c), n[8](t), R(l, r, c), e && e.m(l, c), R(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && S(e, 1)) : (e = A(l), e.c(), S(e, 1), e.m(s.parentNode, s)) : e && (fe(), P(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(l) {
      o || (S(e), o = !0);
    },
    o(l) {
      P(e), o = !1;
    },
    d(l) {
      l && (g(t), g(r), g(s)), n[8](null), e && e.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function ve(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ce(e);
  let {
    svelteInit: i
  } = t;
  const f = v(W(t)), d = v();
  T(n, d, (a) => r(0, s = a));
  const m = v();
  T(n, m, (a) => r(1, o = a));
  const u = [], _ = we("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: C,
    subSlotIndex: y
  } = X() || {}, b = i({
    parent: _,
    props: f,
    target: d,
    slot: m,
    slotKey: p,
    slotIndex: C,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  be("$$ms-gr-react-wrapper", b), ge(() => {
    f.set(W(t));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function E(a) {
    j[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function q(a) {
    j[a ? "unshift" : "push"](() => {
      o = a, m.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = L(L({}, t), N(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, t = N(t), [s, o, d, m, c, i, l, e, E, q];
}
class Re extends se {
  constructor(t) {
    super(), _e(this, t, ve, Ee, pe, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(n) {
  function t(r) {
    const s = v(), o = new Re({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, l], D({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: O,
              node: I
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
      r(t);
    });
  });
}
function xe(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Ce(n, t = !1) {
  try {
    if (t && !xe(n))
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
function Ie(n, t) {
  return V(() => Ce(n, t), [n, t]);
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Oe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function k(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = k(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
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
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = k(e);
      t.push(...c), r.appendChild(l);
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
const Le = B(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function f() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(o, u), r && u.classList.add(...r.split(" ")), s) {
        const _ = Pe(s);
        Object.keys(_).forEach((p) => {
          u.style[p] = _[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var y, b, E;
        (y = e.current) != null && y.contains(i) && ((b = e.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: C
        } = k(n);
        return i = C, c(p), i.style.display = "contents", f(), (E = e.current) == null || E.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", f(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, _;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((_ = e.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, r, s, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(n, t) {
  return n ? /* @__PURE__ */ w.jsx(Le, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: t,
  slots: r
}, s) {
  return r[n] ? (...o) => (t(n, o), je(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Se(({
  slots: n,
  children: t,
  onValueChange: r,
  character: s,
  onChange: o,
  setSlotParams: e,
  elRef: l,
  ...c
}) => {
  const i = Ie(s, !0);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ w.jsx(Z, {
      ...c,
      ref: l,
      onChange: (f) => {
        o == null || o(f), r(f);
      },
      character: n.character ? Te({
        slots: n,
        setSlotParams: e,
        key: "character"
      }) : i || s
    })]
  });
});
export {
  Ne as Rate,
  Ne as default
};
