import { g as Z, w as v } from "./Index-Dkg877lg.js";
const h = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Statistic;
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, e, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) re.call(e, s) && !se.hasOwnProperty(s) && (o[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: te,
    type: n,
    key: t,
    ref: l,
    props: o,
    _owner: oe.current
  };
}
R.Fragment = ne;
R.jsx = G;
R.jsxs = G;
z.exports = R;
var m = z.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: T,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: F,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: K,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert_hydration: x,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: he,
  transition_in: S,
  transition_out: k,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ye,
  onDestroy: be,
  setContext: Ee
} = window.__gradio__svelte__internal;
function W(n) {
  let e, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = ue(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = H(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(e);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      x(t, e, l), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ge(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? fe(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : de(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (S(o, t), r = !0);
    },
    o(t) {
      k(o, t), r = !1;
    },
    d(t) {
      t && g(e), o && o.d(t), n[9](null);
    }
  };
}
function ve(n) {
  let e, r, s, o, t = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      e = K("react-portal-target"), r = he(), t && t.c(), s = N(), this.h();
    },
    l(l) {
      e = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(e).forEach(g), r = ce(l), t && t.l(l), s = N(), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      x(l, e, c), n[8](e), x(l, r, c), t && t.m(l, c), x(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && S(t, 1)) : (t = W(l), t.c(), S(t, 1), t.m(s.parentNode, s)) : t && (_e(), k(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(l) {
      o || (S(t), o = !0);
    },
    o(l) {
      k(t), o = !1;
    },
    d(l) {
      l && (g(e), g(r), g(s)), n[8](null), t && t.d(l);
    }
  };
}
function D(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function xe(n, e, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = ae(t);
  let {
    svelteInit: i
  } = e;
  const w = v(D(e)), d = v();
  F(n, d, (a) => r(0, s = a));
  const p = v();
  F(n, p, (a) => r(1, o = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: I,
    subSlotIndex: y
  } = Z() || {}, b = i({
    parent: f,
    props: w,
    target: d,
    slot: p,
    slotKey: _,
    slotIndex: I,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", b), we(() => {
    w.set(D(e));
  }), be(() => {
    u.forEach((a) => a());
  });
  function E(a) {
    T[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function V(a) {
    T[a ? "unshift" : "push"](() => {
      o = a, p.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, e = L(L({}, e), A(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, e = A(e), [s, o, d, p, c, i, l, t, E, V];
}
class Se extends le {
  constructor(e) {
    super(), me(this, e, xe, ve, pe, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(n) {
  function e(r) {
    const s = v(), o = new Se({
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
          }, c = t.parent ?? O;
          return c.nodes = [...c.nodes, l], M({
            createPortal: P,
            node: O
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), M({
              createPortal: P,
              node: O
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
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const s = n[r];
    return typeof s == "number" && !Re.includes(r) ? e[r] = s + "px" : e[r] = s, e;
  }, {}) : {};
}
function j(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(P(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = j(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...t]
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
      } = j(t);
      e.push(...c), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function Oe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const C = B(({
  slot: n,
  clone: e,
  className: r,
  style: s
}, o) => {
  const t = J(), [l, c] = Y([]);
  return Q(() => {
    var p;
    if (!t.current || !n)
      return;
    let i = n;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(o, u), r && u.classList.add(...r.split(" ")), s) {
        const f = Ie(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var y, b, E;
        (y = t.current) != null && y.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: _,
          clonedElement: I
        } = j(n);
        return i = I, c(_), i.style.display = "contents", w(), (E = t.current) == null || E.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (p = t.current) == null || p.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((f = t.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, e, r, s, o]), h.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function ke(n, e = !1) {
  try {
    if (e && !Pe(n))
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
function je(n, e) {
  return X(() => ke(n, e), [n, e]);
}
function Le(n, e) {
  return n ? /* @__PURE__ */ m.jsx(C, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: e,
  slots: r
}, s) {
  return r[n] ? (...o) => (e(n, o), Le(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Ce(({
  children: n,
  slots: e,
  setSlotParams: r,
  formatter: s,
  ...o
}) => {
  const t = je(s);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ m.jsx($, {
      ...o,
      formatter: e.formatter ? Te({
        slots: e,
        setSlotParams: r,
        key: "formatter"
      }) : t,
      title: e.title ? /* @__PURE__ */ m.jsx(C, {
        slot: e.title
      }) : o.title,
      prefix: e.prefix ? /* @__PURE__ */ m.jsx(C, {
        slot: e.prefix
      }) : o.prefix,
      suffix: e.suffix ? /* @__PURE__ */ m.jsx(C, {
        slot: e.suffix
      }) : o.suffix
    })]
  });
});
export {
  Ne as Statistic,
  Ne as default
};
