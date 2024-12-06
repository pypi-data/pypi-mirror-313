import { g as Z, w as C } from "./Index-DDMzxuFO.js";
const p = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Alert;
var z = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = p, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(t, n, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) oe.call(n, s) && !se.hasOwnProperty(s) && (r[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: te,
    type: t,
    key: e,
    ref: l,
    props: r,
    _owner: re.current
  };
}
I.Fragment = ne;
I.jsx = G;
I.jsxs = G;
z.exports = I;
var h = z.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: A,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: T,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: K,
  empty: N,
  exclude_internal_props: F,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert_hydration: x,
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
function W(t) {
  let n, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = ue(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = K("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = U(n);
      r && r.l(l), l.forEach(g), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      x(e, n, l), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && ge(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? fe(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (R(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && g(n), r && r.d(e), t[9](null);
    }
  };
}
function ve(t) {
  let n, o, s, r, e = (
    /*$$slots*/
    t[4].default && W(t)
  );
  return {
    c() {
      n = K("react-portal-target"), o = he(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      n = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(n).forEach(g), o = ce(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      x(l, n, c), t[8](n), x(l, o, c), e && e.m(l, c), x(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = W(l), e.c(), R(e, 1), e.m(s.parentNode, s)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      r || (R(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (g(n), g(o), g(s)), t[8](null), e && e.d(l);
    }
  };
}
function D(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function Ce(t, n, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = ae(e);
  let {
    svelteInit: i
  } = n;
  const w = C(D(n)), d = C();
  T(t, d, (a) => o(0, s = a));
  const m = C();
  T(t, m, (a) => o(1, r = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y
  } = Z() || {}, E = i({
    parent: f,
    props: w,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", E), we(() => {
    w.set(D(n));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function v(a) {
    A[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function V(a) {
    A[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return t.$$set = (a) => {
    o(17, n = L(L({}, n), F(a))), "svelteInit" in a && o(5, i = a.svelteInit), "$$scope" in a && o(6, l = a.$$scope);
  }, n = F(n), [s, r, d, m, c, i, l, e, v, V];
}
class xe extends le {
  constructor(n) {
    super(), me(this, n, Ce, ve, pe, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, O = window.ms_globals.tree;
function Re(t) {
  function n(o) {
    const s = C(), r = new xe({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? O;
          return c.nodes = [...c.nodes, l], M({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), M({
              createPortal: P,
              node: O
            });
          }), l;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const s = t[o];
    return typeof s == "number" && !Ie.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function j(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(P(p.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: p.Children.toArray(t._reactElement.props.children).map((r) => {
        if (p.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(r.props.el);
          return p.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...p.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = j(e);
      n.push(...c), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Oe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const b = B(({
  slot: t,
  clone: n,
  className: o,
  style: s
}, r) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!e.current || !t)
      return;
    let i = t;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(r, u), o && u.classList.add(...o.split(" ")), s) {
        const f = Se(s);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var y, E, v;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = j(t);
        return i = S, c(_), i.style.display = "contents", w(), (v = e.current) == null || v.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, o, s, r]), p.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function ke(t, n = !1) {
  try {
    if (n && !Pe(t))
      return;
    if (typeof t == "string") {
      let o = t.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function je(t, n) {
  return X(() => ke(t, n), [t, n]);
}
const Ae = Re(({
  slots: t,
  afterClose: n,
  ...o
}) => {
  const s = je(n);
  return /* @__PURE__ */ h.jsx($, {
    ...o,
    afterClose: s,
    action: t.action ? /* @__PURE__ */ h.jsx(b, {
      slot: t.action
    }) : o.action,
    closable: t["closable.closeIcon"] ? {
      ...typeof o.closable == "object" ? o.closable : {},
      closeIcon: /* @__PURE__ */ h.jsx(b, {
        slot: t["closable.closeIcon"]
      })
    } : o.closable,
    description: t.description ? /* @__PURE__ */ h.jsx(b, {
      slot: t.description
    }) : o.description,
    icon: t.icon ? /* @__PURE__ */ h.jsx(b, {
      slot: t.icon
    }) : o.icon,
    message: t.message ? /* @__PURE__ */ h.jsx(b, {
      slot: t.message
    }) : o.message
  });
});
export {
  Ae as Alert,
  Ae as default
};
