import { g as $, w as S } from "./Index-BvZiL_AB.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Slider;
var U = {
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(r, t, e) {
  var l, o = {}, n = null, s = null;
  e !== void 0 && (n = "" + e), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) oe.call(t, l) && !le.hasOwnProperty(l) && (o[l] = t[l]);
  if (r && r.defaultProps) for (l in t = r.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: ne,
    type: r,
    key: n,
    ref: s,
    props: o,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = H;
R.jsxs = H;
U.exports = R;
var g = U.exports;
const {
  SvelteComponent: ie,
  assign: F,
  binding_callbacks: T,
  check_outros: ce,
  children: K,
  claim_element: q,
  claim_space: ae,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: V,
  empty: v,
  exclude_internal_props: A,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: C,
  safe_not_equal: he,
  set_custom_element_data: B,
  space: ge,
  transition_in: x,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: Se
} = window.__gradio__svelte__internal;
function W(r) {
  let t, e;
  const l = (
    /*#slots*/
    r[7].default
  ), o = de(
    l,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = q(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(t);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      C(n, t, s), o && o.m(t, null), r[9](t), e = !0;
    },
    p(n, s) {
      o && o.p && (!e || s & /*$$scope*/
      64) && we(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        e ? _e(
          l,
          /*$$scope*/
          n[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      e || (x(o, n), e = !0);
    },
    o(n) {
      k(o, n), e = !1;
    },
    d(n) {
      n && w(t), o && o.d(n), r[9](null);
    }
  };
}
function Ce(r) {
  let t, e, l, o, n = (
    /*$$slots*/
    r[4].default && W(r)
  );
  return {
    c() {
      t = V("react-portal-target"), e = ge(), n && n.c(), l = v(), this.h();
    },
    l(s) {
      t = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(w), e = ae(s), n && n.l(s), l = v(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, t, c), r[8](t), C(s, e, c), n && n.m(s, c), C(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && x(n, 1)) : (n = W(s), n.c(), x(n, 1), n.m(l.parentNode, l)) : n && (pe(), k(n, 1, 1, () => {
        n = null;
      }), ce());
    },
    i(s) {
      o || (x(n), o = !0);
    },
    o(s) {
      k(n), o = !1;
    },
    d(s) {
      s && (w(t), w(e), w(l)), r[8](null), n && n.d(s);
    }
  };
}
function D(r) {
  const {
    svelteInit: t,
    ...e
  } = r;
  return e;
}
function xe(r, t, e) {
  let l, o, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = ue(n);
  let {
    svelteInit: i
  } = t;
  const m = S(D(t)), d = S();
  N(r, d, (u) => e(0, l = u));
  const p = S();
  N(r, p, (u) => e(1, o = u));
  const a = [], _ = ye("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: P,
    subSlotIndex: b
  } = $() || {}, y = i({
    parent: _,
    props: m,
    target: d,
    slot: p,
    slotKey: f,
    slotIndex: P,
    subSlotIndex: b,
    onDestroy(u) {
      a.push(u);
    }
  });
  Se("$$ms-gr-react-wrapper", y), be(() => {
    m.set(D(t));
  }), Ee(() => {
    a.forEach((u) => u());
  });
  function E(u) {
    T[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function J(u) {
    T[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return r.$$set = (u) => {
    e(17, t = F(F({}, t), A(u))), "svelteInit" in u && e(5, i = u.svelteInit), "$$scope" in u && e(6, s = u.$$scope);
  }, t = A(t), [l, o, d, p, c, i, s, n, E, J];
}
class Re extends ie {
  constructor(t) {
    super(), me(this, t, xe, Ce, he, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, I = window.ms_globals.tree;
function Pe(r) {
  function t(e) {
    const l = S(), o = new Re({
      ...e,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? I;
          return c.nodes = [...c.nodes, s], M({
            createPortal: O,
            node: I
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), M({
              createPortal: O,
              node: I
            });
          }), s;
        },
        ...e.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((e) => {
    window.ms_globals.initializePromise.then(() => {
      e(t);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(r) {
  return r ? Object.keys(r).reduce((t, e) => {
    const l = r[e];
    return typeof l == "number" && !Ie.includes(e) ? t[e] = l + "px" : t[e] = l, t;
  }, {}) : {};
}
function j(r) {
  const t = [], e = r.cloneNode(!1);
  if (r._reactElement)
    return t.push(O(h.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: h.Children.toArray(r._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = j(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...h.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), e)), {
      clonedElement: e,
      portals: t
    };
  Object.keys(r.getEventListeners()).forEach((o) => {
    r.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      e.addEventListener(c, s, i);
    });
  });
  const l = Array.from(r.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(n);
      t.push(...c), e.appendChild(s);
    } else n.nodeType === 3 && e.appendChild(n.cloneNode());
  }
  return {
    clonedElement: e,
    portals: t
  };
}
function ke(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const L = Y(({
  slot: r,
  clone: t,
  className: e,
  style: l
}, o) => {
  const n = Q(), [s, c] = X([]);
  return Z(() => {
    var p;
    if (!n.current || !r)
      return;
    let i = r;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(o, a), e && a.classList.add(...e.split(" ")), l) {
        const _ = Oe(l);
        Object.keys(_).forEach((f) => {
          a.style[f] = _[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b, y, E;
        (b = n.current) != null && b.contains(i) && ((y = n.current) == null || y.removeChild(i));
        const {
          portals: f,
          clonedElement: P
        } = j(r);
        return i = P, c(f), i.style.display = "contents", m(), (E = n.current) == null || E.appendChild(i), f.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (p = n.current) == null || p.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((_ = n.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [r, t, e, l, o]), h.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(r) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(r.trim());
}
function Le(r, t = !1) {
  try {
    if (t && !je(r))
      return;
    if (typeof r == "string") {
      let e = r.trim();
      return e.startsWith(";") && (e = e.slice(1)), e.endsWith(";") && (e = e.slice(0, -1)), new Function(`return (...args) => (${e})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function G(r, t) {
  return z(() => Le(r, t), [r, t]);
}
function Fe(r, t) {
  return r ? /* @__PURE__ */ g.jsx(L, {
    slot: r,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Te({
  key: r,
  setSlotParams: t,
  slots: e
}, l) {
  return e[r] ? (...o) => (t(r, o), Fe(e[r], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ne = (r) => r.reduce((t, e) => {
  const l = e == null ? void 0 : e.props.number;
  return l !== void 0 && (t[l] = (e == null ? void 0 : e.slots.label) instanceof Element ? {
    ...e.props,
    label: /* @__PURE__ */ g.jsx(L, {
      slot: e == null ? void 0 : e.slots.label
    })
  } : (e == null ? void 0 : e.slots.children) instanceof Element ? /* @__PURE__ */ g.jsx(L, {
    slot: e == null ? void 0 : e.slots.children
  }) : {
    ...e == null ? void 0 : e.props
  }), t;
}, {}), Ae = Pe(({
  marks: r,
  markItems: t,
  children: e,
  onValueChange: l,
  onChange: o,
  elRef: n,
  tooltip: s,
  step: c,
  slots: i,
  setSlotParams: m,
  ...d
}) => {
  const p = (f) => {
    o == null || o(f), l(f);
  }, a = G(s == null ? void 0 : s.getPopupContainer), _ = G(s == null ? void 0 : s.formatter);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ g.jsx(ee, {
      ...d,
      tooltip: {
        ...s,
        getPopupContainer: a,
        formatter: i["tooltip.formatter"] ? Te({
          key: "tooltip.formatter",
          setSlotParams: m,
          slots: i
        }) : _
      },
      marks: z(() => r || Ne(t), [t, r]),
      step: c === void 0 ? null : c,
      ref: n,
      onChange: p
    })]
  });
});
export {
  Ae as Slider,
  Ae as default
};
