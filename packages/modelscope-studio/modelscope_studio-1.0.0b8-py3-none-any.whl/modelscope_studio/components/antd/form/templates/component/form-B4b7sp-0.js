import { g as $, w as E } from "./Index-FqDom34C.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.useMemo, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, x = window.ms_globals.ReactDOM.createPortal, P = window.ms_globals.antd.Form;
var G = {
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) re.call(t, s) && !se.hasOwnProperty(s) && (o[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: oe.current
  };
}
S.Fragment = ne;
S.jsx = U;
S.jsxs = U;
G.exports = S;
var q = G.exports;
const {
  SvelteComponent: le,
  assign: F,
  binding_callbacks: L,
  check_outros: ie,
  children: H,
  claim_element: K,
  claim_space: ce,
  component_subscribe: T,
  compute_slots: ae,
  create_slot: ue,
  detach: w,
  element: B,
  empty: N,
  exclude_internal_props: j,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: v,
  safe_not_equal: me,
  set_custom_element_data: J,
  space: he,
  transition_in: R,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function A(n) {
  let t, r;
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
      t = B("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(t);
      o && o.l(l), l.forEach(w), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, t, l), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && we(
        o,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? fe(
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
      r || (R(o, e), r = !0);
    },
    o(e) {
      k(o, e), r = !1;
    },
    d(e) {
      e && w(t), o && o.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, r, s, o, e = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      t = B("react-portal-target"), r = he(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(w), r = ce(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      v(l, t, c), n[8](t), v(l, r, c), e && e.m(l, c), v(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = A(l), e.c(), R(e, 1), e.m(s.parentNode, s)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      o || (R(e), o = !0);
    },
    o(l) {
      k(e), o = !1;
    },
    d(l) {
      l && (w(t), w(r), w(s)), n[8](null), e && e.d(l);
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
function Re(n, t, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const m = E(W(t)), d = E();
  T(n, d, (u) => r(0, s = u));
  const f = E();
  T(n, f, (u) => r(1, o = u));
  const a = [], _ = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: C,
    subSlotIndex: g
  } = $() || {}, b = i({
    parent: _,
    props: m,
    target: d,
    slot: f,
    slotKey: p,
    slotIndex: C,
    subSlotIndex: g,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ee("$$ms-gr-react-wrapper", b), ge(() => {
    m.set(W(t));
  }), ye(() => {
    a.forEach((u) => u());
  });
  function y(u) {
    L[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function V(u) {
    L[u ? "unshift" : "push"](() => {
      o = u, f.set(o);
    });
  }
  return n.$$set = (u) => {
    r(17, t = F(F({}, t), j(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, t = j(t), [s, o, d, f, c, i, l, e, y, V];
}
class Se extends le {
  constructor(t) {
    super(), pe(this, t, Re, ve, me, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Ce(n) {
  function t(r) {
    const s = E(), o = new Se({
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
            createPortal: x,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: x,
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
function Ie(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function xe(n, t = !1) {
  try {
    if (t && !Ie(n))
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
function M(n, t) {
  return Y(() => xe(n, t), [n, t]);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !ke.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function O(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(x(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = O(o.props.el);
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
      } = O(e);
      t.push(...c), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Pe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Fe = Q(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, o) => {
  const e = X(), [l, c] = Z([]);
  return z(() => {
    var f;
    if (!e.current || !n)
      return;
    let i = n;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(o, a), r && a.classList.add(...r.split(" ")), s) {
        const _ = Oe(s);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var g, b, y;
        (g = e.current) != null && g.contains(i) && ((b = e.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: C
        } = O(n);
        return i = C, c(p), i.style.display = "contents", m(), (y = e.current) == null || y.appendChild(i), p.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (f = e.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((_ = e.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, r, s, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Le(n, t) {
  return n ? /* @__PURE__ */ q.jsx(Fe, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: t,
  slots: r
}, s) {
  return r[n] ? (...o) => (t(n, o), Le(r[n], {
    clone: !0,
    ...s
  })) : void 0;
}
const je = Ce(({
  value: n,
  onValueChange: t,
  requiredMark: r,
  onValuesChange: s,
  feedbackIcons: o,
  setSlotParams: e,
  slots: l,
  ...c
}) => {
  const [i] = P.useForm(), m = M(o), d = M(r);
  return z(() => {
    i.setFieldsValue(n);
  }, [i, n]), /* @__PURE__ */ q.jsx(P, {
    ...c,
    initialValues: n,
    form: i,
    requiredMark: l.requiredMark ? Te({
      key: "requiredMark",
      setSlotParams: e,
      slots: l
    }) : r === "optional" ? r : d || r,
    feedbackIcons: m,
    onValuesChange: (f, a) => {
      t(a), s == null || s(f, a);
    }
  });
});
export {
  je as Form,
  je as default
};
