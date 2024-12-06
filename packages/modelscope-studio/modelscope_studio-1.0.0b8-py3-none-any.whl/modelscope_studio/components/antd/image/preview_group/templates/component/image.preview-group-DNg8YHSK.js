import { g as Z, w as y } from "./Index-DDtAGtmT.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, x = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Image;
var M = {
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
var ee = m, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(t, n, r) {
  var s, o = {}, e = null, l = null;
  r !== void 0 && (e = "" + r), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) re.call(n, s) && !se.hasOwnProperty(s) && (o[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: te,
    type: t,
    key: e,
    ref: l,
    props: o,
    _owner: oe.current
  };
}
I.Fragment = ne;
I.jsx = z;
I.jsxs = z;
M.exports = I;
var S = M.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: j,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: T,
  compute_slots: ae,
  create_slot: ue,
  detach: h,
  element: K,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: pe,
  init: _e,
  insert_hydration: E,
  safe_not_equal: me,
  set_custom_element_data: q,
  space: he,
  transition_in: C,
  transition_out: P,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ve,
  setContext: ye
} = window.__gradio__svelte__internal;
function F(t) {
  let n, r;
  const s = (
    /*#slots*/
    t[7].default
  ), o = ue(
    s,
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
      var l = U(n);
      o && o.l(l), l.forEach(h), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      E(e, n, l), o && o.m(n, null), t[9](n), r = !0;
    },
    p(e, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ge(
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
      r || (C(o, e), r = !0);
    },
    o(e) {
      P(o, e), r = !1;
    },
    d(e) {
      e && h(n), o && o.d(e), t[9](null);
    }
  };
}
function Ee(t) {
  let n, r, s, o, e = (
    /*$$slots*/
    t[4].default && F(t)
  );
  return {
    c() {
      n = K("react-portal-target"), r = he(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      n = H(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(n).forEach(h), r = ce(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      q(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      E(l, n, c), t[8](n), E(l, r, c), e && e.m(l, c), E(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && C(e, 1)) : (e = F(l), e.c(), C(e, 1), e.m(s.parentNode, s)) : e && (pe(), P(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      o || (C(e), o = !0);
    },
    o(l) {
      P(e), o = !1;
    },
    d(l) {
      l && (h(n), h(r), h(s)), t[8](null), e && e.d(l);
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
function Ce(t, n, r) {
  let s, o, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const c = ae(e);
  let {
    svelteInit: i
  } = n;
  const g = y(W(n)), d = y();
  T(t, d, (a) => r(0, s = a));
  const _ = y();
  T(t, _, (a) => r(1, o = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: w
  } = Z() || {}, b = i({
    parent: f,
    props: g,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: w,
    onDestroy(a) {
      u.push(a);
    }
  });
  ye("$$ms-gr-react-wrapper", b), we(() => {
    g.set(W(n));
  }), ve(() => {
    u.forEach((a) => a());
  });
  function v(a) {
    j[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function V(a) {
    j[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  return t.$$set = (a) => {
    r(17, n = L(L({}, n), A(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, n = A(n), [s, o, d, _, c, i, l, e, v, V];
}
class Ie extends le {
  constructor(n) {
    super(), _e(this, n, Ce, Ee, me, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, k = window.ms_globals.tree;
function Re(t) {
  function n(r) {
    const s = y(), o = new Ie({
      ...r,
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
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, l], D({
            createPortal: x,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), D({
              createPortal: x,
              node: k
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
      r(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(t) {
  return t ? Object.keys(t).reduce((n, r) => {
    const s = t[r];
    return typeof s == "number" && !Se.includes(r) ? n[r] = s + "px" : n[r] = s, n;
  }, {}) : {};
}
function O(t) {
  const n = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(x(m.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: m.Children.toArray(t._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = O(o.props.el);
          return m.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...m.Children.toArray(o.props.children), ...e]
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
      listener: l,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let o = 0; o < s.length; o++) {
    const e = s[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = O(e);
      n.push(...c), r.appendChild(l);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function xe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const G = B(({
  slot: t,
  clone: n,
  className: r,
  style: s
}, o) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), xe(o, u), r && u.classList.add(...r.split(" ")), s) {
        const f = ke(s);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var w, b, v;
        (w = e.current) != null && w.contains(i) && ((b = e.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: R
        } = O(t);
        return i = R, c(p), i.style.display = "contents", g(), (v = e.current) == null || v.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, n, r, s, o]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Pe(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Oe(t, n = !1) {
  try {
    if (n && !Pe(t))
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
function Le(t, n) {
  return X(() => Oe(t, n), [t, n]);
}
function je(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const Ne = Re(({
  slots: t,
  preview: n,
  ...r
}) => {
  const s = je(n), o = t["preview.mask"] || t["preview.closeIcon"] || n !== !1, e = Le(s.getContainer);
  return /* @__PURE__ */ S.jsx($.PreviewGroup, {
    ...r,
    preview: o ? {
      ...s,
      getContainer: e,
      ...t["preview.mask"] || Reflect.has(s, "mask") ? {
        mask: t["preview.mask"] ? /* @__PURE__ */ S.jsx(G, {
          slot: t["preview.mask"]
        }) : s.mask
      } : {},
      closeIcon: t["preview.closeIcon"] ? /* @__PURE__ */ S.jsx(G, {
        slot: t["preview.closeIcon"]
      }) : s.closeIcon
    } : !1
  });
});
export {
  Ne as ImagePreviewGroup,
  Ne as default
};
