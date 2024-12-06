import { g as $, w as v } from "./Index-D-nn0PwO.js";
const h = window.ms_globals.React, q = window.ms_globals.React.forwardRef, V = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, X = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Pagination;
var z = {
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(n, e, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) oe.call(e, s) && !le.hasOwnProperty(s) && (o[s] = e[s]);
  if (n && n.defaultProps) for (s in e = n.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: ne,
    type: n,
    key: t,
    ref: l,
    props: o,
    _owner: se.current
  };
}
x.Fragment = re;
x.jsx = B;
x.jsxs = B;
z.exports = x;
var g = z.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: j,
  check_outros: ce,
  children: G,
  claim_element: J,
  claim_space: ae,
  component_subscribe: T,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: U,
  empty: F,
  exclude_internal_props: N,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: me,
  insert_hydration: R,
  safe_not_equal: he,
  set_custom_element_data: H,
  space: ge,
  transition_in: S,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: be,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function A(n) {
  let e, r;
  const s = (
    /*#slots*/
    n[7].default
  ), o = de(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = U("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = J(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = G(e);
      o && o.l(l), l.forEach(w), this.h();
    },
    h() {
      H(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      R(t, e, l), o && o.m(e, null), n[9](e), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && we(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? _e(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : fe(
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
      t && w(e), o && o.d(t), n[9](null);
    }
  };
}
function Re(n) {
  let e, r, s, o, t = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      e = U("react-portal-target"), r = ge(), t && t.c(), s = F(), this.h();
    },
    l(l) {
      e = J(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(e).forEach(w), r = ae(l), t && t.l(l), s = F(), this.h();
    },
    h() {
      H(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      R(l, e, c), n[8](e), R(l, r, c), t && t.m(l, c), R(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && S(t, 1)) : (t = A(l), t.c(), S(t, 1), t.m(s.parentNode, s)) : t && (pe(), k(t, 1, 1, () => {
        t = null;
      }), ce());
    },
    i(l) {
      o || (S(t), o = !0);
    },
    o(l) {
      k(t), o = !1;
    },
    d(l) {
      l && (w(e), w(r), w(s)), n[8](null), t && t.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function Se(n, e, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = ue(t);
  let {
    svelteInit: i
  } = e;
  const m = v(W(e)), d = v();
  T(n, d, (a) => r(0, s = a));
  const f = v();
  T(n, f, (a) => r(1, o = a));
  const u = [], _ = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: C,
    subSlotIndex: y
  } = $() || {}, b = i({
    parent: _,
    props: m,
    target: d,
    slot: f,
    slotKey: p,
    slotIndex: C,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  ve("$$ms-gr-react-wrapper", b), ye(() => {
    m.set(W(e));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function E(a) {
    j[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function Q(a) {
    j[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, e = L(L({}, e), N(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, e = N(e), [s, o, d, f, c, i, l, t, E, Q];
}
class xe extends ie {
  constructor(e) {
    super(), me(this, e, Se, Re, he, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Ce(n) {
  function e(r) {
    const s = v(), o = new xe({
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
          }, c = t.parent ?? I;
          return c.nodes = [...c.nodes, l], D({
            createPortal: P,
            node: I
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: P,
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
      r(e);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const s = n[r];
    return typeof s == "number" && !Ie.includes(r) ? e[r] = s + "px" : e[r] = s, e;
  }, {}) : {};
}
function O(n) {
  const e = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(P(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = O(o.props.el);
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
      } = O(t);
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
const K = q(({
  slot: n,
  clone: e,
  className: r,
  style: s
}, o) => {
  const t = V(), [l, c] = Y([]);
  return X(() => {
    var f;
    if (!t.current || !n)
      return;
    let i = n;
    function m() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(o, u), r && u.classList.add(...r.split(" ")), s) {
        const _ = Pe(s);
        Object.keys(_).forEach((p) => {
          u.style[p] = _[p];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var y, b, E;
        (y = t.current) != null && y.contains(i) && ((b = t.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: C
        } = O(n);
        return i = C, c(p), i.style.display = "contents", m(), (E = t.current) == null || E.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var u, _;
      i.style.display = "", (u = t.current) != null && u.contains(i) && ((_ = t.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, e, r, s, o]), h.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Oe(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Le(n, e = !1) {
  try {
    if (e && !Oe(n))
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
function M(n, e) {
  return Z(() => Le(n, e), [n, e]);
}
function je(n, e) {
  return n ? /* @__PURE__ */ g.jsx(K, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: e,
  slots: r
}, s) {
  return r[n] ? (...o) => (e(n, o), je(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ne = Ce(({
  slots: n,
  showTotal: e,
  showQuickJumper: r,
  onChange: s,
  children: o,
  itemRender: t,
  setSlotParams: l,
  ...c
}) => {
  const i = M(t), m = M(e);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: o
    }), /* @__PURE__ */ g.jsx(ee, {
      ...c,
      showTotal: e ? m : void 0,
      itemRender: n.itemRender ? Te({
        slots: n,
        setSlotParams: l,
        key: "itemRender"
      }, {
        clone: !0
      }) : i,
      onChange: (d, f) => {
        s == null || s(d, f);
      },
      showQuickJumper: n["showQuickJumper.goButton"] ? {
        goButton: /* @__PURE__ */ g.jsx(K, {
          slot: n["showQuickJumper.goButton"]
        })
      } : r
    })]
  });
});
export {
  Ne as Pagination,
  Ne as default
};
