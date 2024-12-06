import { g as Z, w as v } from "./Index-CUcUY_g0.js";
const p = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.List;
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
var ee = p, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(e, t, r) {
  var s, o = {}, n = null, l = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) re.call(t, s) && !se.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: te,
    type: e,
    key: n,
    ref: l,
    props: o,
    _owner: oe.current
  };
}
x.Fragment = ne;
x.jsx = G;
x.jsxs = G;
z.exports = x;
var w = z.exports;
const {
  SvelteComponent: le,
  assign: j,
  binding_callbacks: T,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ue,
  detach: h,
  element: K,
  empty: A,
  exclude_internal_props: F,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert_hydration: C,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: he,
  transition_in: R,
  transition_out: k,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function M(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), o = ue(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = H(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(t);
      o && o.l(l), l.forEach(h), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      C(n, t, l), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ge(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? fe(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : de(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (R(o, n), r = !0);
    },
    o(n) {
      k(o, n), r = !1;
    },
    d(n) {
      n && h(t), o && o.d(n), e[9](null);
    }
  };
}
function ve(e) {
  let t, r, s, o, n = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      t = K("react-portal-target"), r = he(), n && n.c(), s = A(), this.h();
    },
    l(l) {
      t = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(h), r = ce(l), n && n.l(l), s = A(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      C(l, t, c), e[8](t), C(l, r, c), n && n.m(l, c), C(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && R(n, 1)) : (n = M(l), n.c(), R(n, 1), n.m(s.parentNode, s)) : n && (_e(), k(n, 1, 1, () => {
        n = null;
      }), ie());
    },
    i(l) {
      o || (R(n), o = !0);
    },
    o(l) {
      k(n), o = !1;
    },
    d(l) {
      l && (h(t), h(r), h(s)), e[8](null), n && n.d(l);
    }
  };
}
function W(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ce(e, t, r) {
  let s, o, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const c = ae(n);
  let {
    svelteInit: i
  } = t;
  const g = v(W(t)), d = v();
  N(e, d, (a) => r(0, s = a));
  const m = v();
  N(e, m, (a) => r(1, o = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b
  } = Z() || {}, y = i({
    parent: f,
    props: g,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", y), we(() => {
    g.set(W(t));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function E(a) {
    T[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function V(a) {
    T[a ? "unshift" : "push"](() => {
      o = a, m.set(o);
    });
  }
  return e.$$set = (a) => {
    r(17, t = j(j({}, t), F(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, t = F(t), [s, o, d, m, c, i, l, n, E, V];
}
class Re extends le {
  constructor(t) {
    super(), me(this, t, Ce, ve, pe, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, O = window.ms_globals.tree;
function Se(e) {
  function t(r) {
    const s = v(), o = new Re({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? O;
          return c.nodes = [...c.nodes, l], D({
            createPortal: P,
            node: O
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
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
      r(t);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return typeof s == "number" && !xe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function L(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(P(p.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: p.Children.toArray(e._reactElement.props.children).map((o) => {
        if (p.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = L(o.props.el);
          return p.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...p.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = L(n);
      t.push(...c), r.appendChild(l);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Oe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const S = B(({
  slot: e,
  clone: t,
  className: r,
  style: s
}, o) => {
  const n = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!n.current || !e)
      return;
    let i = e;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(o, u), r && u.classList.add(...r.split(" ")), s) {
        const f = Ie(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var b, y, E;
        (b = n.current) != null && b.contains(i) && ((y = n.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: I
        } = L(e);
        return i = I, c(_), i.style.display = "contents", g(), (E = n.current) == null || E.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (m = n.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = n.current) != null && u.contains(i) && ((f = n.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, t, r, s, o]), p.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ke(e, t = !1) {
  try {
    if (t && !Pe(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Le(e, t) {
  return X(() => ke(e, t), [e, t]);
}
function je(e, t) {
  return e ? /* @__PURE__ */ w.jsx(S, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Te({
  key: e,
  setSlotParams: t,
  slots: r
}, s) {
  return r[e] ? (...o) => (t(e, o), je(r[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const Ae = Se(({
  slots: e,
  renderItem: t,
  setSlotParams: r,
  ...s
}) => {
  const o = Le(t);
  return /* @__PURE__ */ w.jsx($, {
    ...s,
    footer: e.footer ? /* @__PURE__ */ w.jsx(S, {
      slot: e.footer
    }) : s.footer,
    header: e.header ? /* @__PURE__ */ w.jsx(S, {
      slot: e.header
    }) : s.header,
    loadMore: e.loadMore ? /* @__PURE__ */ w.jsx(S, {
      slot: e.loadMore
    }) : s.loadMore,
    renderItem: e.renderItem ? Te({
      slots: e,
      setSlotParams: r,
      key: "renderItem"
    }) : o
  });
});
export {
  Ae as List,
  Ae as default
};
