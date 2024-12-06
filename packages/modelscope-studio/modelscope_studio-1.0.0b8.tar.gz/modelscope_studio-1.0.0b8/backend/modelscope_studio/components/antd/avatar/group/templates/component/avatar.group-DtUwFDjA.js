import { g as $, w as E, d as ee, a as w } from "./Index-D0QCgZnm.js";
const h = window.ms_globals.React, z = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, k = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Avatar;
var K = {
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
var ne = h, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) se.call(t, l) && !ae.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: oe,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: le.current
  };
}
C.Fragment = re;
C.jsx = V;
C.jsxs = V;
K.exports = C;
var g = K.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: T,
  check_outros: ce,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: N,
  compute_slots: de,
  create_slot: fe,
  detach: v,
  element: J,
  empty: D,
  exclude_internal_props: G,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: I,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: ve,
  transition_in: S,
  transition_out: A,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function F(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = fe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = J("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = q(t);
      r && r.l(s), s.forEach(v), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      I(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && we(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (S(r, e), o = !0);
    },
    o(e) {
      A(r, e), o = !1;
    },
    d(e) {
      e && v(t), r && r.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = J("react-portal-target"), o = ve(), e && e.c(), l = D(), this.h();
    },
    l(s) {
      t = B(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(v), o = ue(s), e && e.l(s), l = D(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      I(s, t, i), n[8](t), I(s, o, i), e && e.m(s, i), I(s, l, i), r = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && S(e, 1)) : (e = F(s), e.c(), S(e, 1), e.m(l.parentNode, l)) : e && (me(), A(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      r || (S(e), r = !0);
    },
    o(s) {
      A(e), r = !1;
    },
    d(s) {
      s && (v(t), v(o), v(l)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Se(n, t, o) {
  let l, r, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = de(e);
  let {
    svelteInit: a
  } = t;
  const _ = E(M(t)), d = E();
  N(n, d, (u) => o(0, l = u));
  const f = E();
  N(n, f, (u) => o(1, r = u));
  const c = [], p = be("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: R,
    subSlotIndex: x
  } = $() || {}, b = a({
    parent: p,
    props: _,
    target: d,
    slot: f,
    slotKey: m,
    slotIndex: R,
    subSlotIndex: x,
    onDestroy(u) {
      c.push(u);
    }
  });
  Ee("$$ms-gr-react-wrapper", b), xe(() => {
    _.set(M(t));
  }), ye(() => {
    c.forEach((u) => u());
  });
  function y(u) {
    T[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function Q(u) {
    T[u ? "unshift" : "push"](() => {
      r = u, f.set(r);
    });
  }
  return n.$$set = (u) => {
    o(17, t = L(L({}, t), G(u))), "svelteInit" in u && o(5, a = u.svelteInit), "$$scope" in u && o(6, s = u.$$scope);
  }, t = G(t), [l, r, d, f, i, a, s, e, y, Q];
}
class Ce extends ie {
  constructor(t) {
    super(), he(this, t, Se, Ie, ge, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const l = E(), r = new Ce({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? O;
          return i.nodes = [...i.nodes, s], W({
            createPortal: k,
            node: O
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((a) => a.svelteInstance !== l), W({
              createPortal: k,
              node: O
            });
          }), s;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function Oe(n) {
  const [t, o] = U(() => w(n));
  return H(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Pe(n) {
  const t = z(() => ee(n, (o) => o), [n]);
  return Oe(t);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !ke.includes(o) ? t[o] = l + "px" : t[o] = l, t;
  }, {}) : {};
}
function j(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: s,
            children: [...h.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: s,
      type: i,
      useCapture: a
    }) => {
      o.addEventListener(i, s, a);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = j(e);
      t.push(...i), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function je(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const P = X(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = Z(), [s, i] = U([]);
  return H(() => {
    var f;
    if (!e.current || !n)
      return;
    let a = n;
    function _() {
      let c = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (c = a.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), je(r, c), o && c.classList.add(...o.split(" ")), l) {
        const p = Ae(l);
        Object.keys(p).forEach((m) => {
          c.style[m] = p[m];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var x, b, y;
        (x = e.current) != null && x.contains(a) && ((b = e.current) == null || b.removeChild(a));
        const {
          portals: m,
          clonedElement: R
        } = j(n);
        return a = R, i(m), a.style.display = "contents", _(), (y = e.current) == null || y.appendChild(a), m.length > 0;
      };
      c() || (d = new window.MutationObserver(() => {
        c() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", _(), (f = e.current) == null || f.appendChild(a);
    return () => {
      var c, p;
      a.style.display = "", (c = e.current) != null && c.contains(a) && ((p = e.current) == null || p.removeChild(a)), d == null || d.disconnect();
    };
  }, [n, t, o, l, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Le(n, t) {
  const o = z(() => h.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const i = w(e.props.node.slotIndex) || 0, a = w(s.props.node.slotIndex) || 0;
      return i - a === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (w(e.props.node.subSlotIndex) || 0) - (w(s.props.node.subSlotIndex) || 0) : i - a;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Pe(o);
}
const Ne = Re(({
  slots: n,
  children: t,
  ...o
}) => {
  var r, e, s, i, a, _, d, f;
  const l = Le(t);
  return /* @__PURE__ */ g.jsx(g.Fragment, {
    children: /* @__PURE__ */ g.jsxs(te.Group, {
      ...o,
      max: {
        ...o.max,
        count: typeof ((r = o.max) == null ? void 0 : r.count) == "number" ? (
          // children render
          o.max.count + 1
        ) : (e = o.max) == null ? void 0 : e.count,
        popover: n["max.popover.title"] || n["max.popover.content"] ? {
          ...((i = o.max) == null ? void 0 : i.popover) || {},
          title: n["max.popover.title"] ? /* @__PURE__ */ g.jsx(P, {
            slot: n["max.popover.title"]
          }) : (_ = (a = o.max) == null ? void 0 : a.popover) == null ? void 0 : _.title,
          content: n["max.popover.content"] ? /* @__PURE__ */ g.jsx(P, {
            slot: n["max.popover.content"]
          }) : (f = (d = o.max) == null ? void 0 : d.popover) == null ? void 0 : f.content
        } : (s = o.max) == null ? void 0 : s.popover
      },
      children: [/* @__PURE__ */ g.jsx("div", {
        style: {
          display: "none"
        },
        children: t
      }), l.map((c, p) => /* @__PURE__ */ g.jsx(P, {
        slot: c
      }, p))]
    })
  });
});
export {
  Ne as AvatarGroup,
  Ne as default
};
