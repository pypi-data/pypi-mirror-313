import { g as $, w as x, d as ee, a as w } from "./Index-C5SfNVXo.js";
const _ = window.ms_globals.React, G = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.List;
var K = {
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
var ne = _, oe = Symbol.for("react.element"), re = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(n, t, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ie.hasOwnProperty(s) && (r[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) r[s] === void 0 && (r[s] = t[s]);
  return {
    $$typeof: oe,
    type: n,
    key: e,
    ref: l,
    props: r,
    _owner: le.current
  };
}
S.Fragment = re;
S.jsx = V;
S.jsxs = V;
K.exports = S;
var R = K.exports;
const {
  SvelteComponent: ae,
  assign: T,
  binding_callbacks: A,
  check_outros: ce,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: j,
  compute_slots: de,
  create_slot: fe,
  detach: h,
  element: J,
  empty: N,
  exclude_internal_props: D,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: v,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: we,
  transition_in: I,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: xe,
  setContext: ve
} = window.__gradio__svelte__internal;
function M(n) {
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), r = fe(
    s,
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
      var l = q(t);
      r && r.l(l), l.forEach(h), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      v(e, t, l), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && be(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? _e(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (I(r, e), o = !0);
    },
    o(e) {
      k(r, e), o = !1;
    },
    d(e) {
      e && h(t), r && r.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, o, s, r, e = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      t = J("react-portal-target"), o = we(), e && e.c(), s = N(), this.h();
    },
    l(l) {
      t = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(h), o = ue(l), e && e.l(l), s = N(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      v(l, t, a), n[8](t), v(l, o, a), e && e.m(l, a), v(l, s, a), r = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && I(e, 1)) : (e = M(l), e.c(), I(e, 1), e.m(s.parentNode, s)) : e && (me(), k(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      r || (I(e), r = !0);
    },
    o(l) {
      k(e), r = !1;
    },
    d(l) {
      l && (h(t), h(o), h(s)), n[8](null), e && e.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Se(n, t, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const a = de(e);
  let {
    svelteInit: i
  } = t;
  const g = x(W(t)), d = x();
  j(n, d, (c) => o(0, s = c));
  const m = x();
  j(n, m, (c) => o(1, r = c));
  const u = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: C,
    subSlotIndex: b
  } = $() || {}, y = i({
    parent: f,
    props: g,
    target: d,
    slot: m,
    slotKey: p,
    slotIndex: C,
    subSlotIndex: b,
    onDestroy(c) {
      u.push(c);
    }
  });
  ve("$$ms-gr-react-wrapper", y), ye(() => {
    g.set(W(t));
  }), xe(() => {
    u.forEach((c) => c());
  });
  function E(c) {
    A[c ? "unshift" : "push"](() => {
      s = c, d.set(s);
    });
  }
  function Q(c) {
    A[c ? "unshift" : "push"](() => {
      r = c, m.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = T(T({}, t), D(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, l = c.$$scope);
  }, t = D(t), [s, r, d, m, a, i, l, e, E, Q];
}
class Ce extends ae {
  constructor(t) {
    super(), he(this, t, Se, Ie, ge, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, O = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const s = x(), r = new Ce({
      ...o,
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
          }, a = e.parent ?? O;
          return a.nodes = [...a.nodes, l], z({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), z({
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
      o(t);
    });
  });
}
function Oe(n) {
  const [t, o] = U(() => w(n));
  return H(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Pe(n) {
  const t = G(() => ee(n, (o) => o), [n]);
  return Oe(t);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !ke.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function L(n) {
  const t = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(_.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: _.Children.toArray(n._reactElement.props.children).map((r) => {
        if (_.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = L(r.props.el);
          return _.cloneElement(r, {
            ...r.props,
            el: l,
            children: [..._.Children.toArray(r.props.children), ...e]
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
      listener: l,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, l, i);
    });
  });
  const s = Array.from(n.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = L(e);
      t.push(...a), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Te(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const F = X(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, r) => {
  const e = Z(), [l, a] = U([]);
  return H(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Te(r, u), o && u.classList.add(...o.split(" ")), s) {
        const f = Le(s);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: p,
          clonedElement: C
        } = L(n);
        return i = C, a(p), i.style.display = "contents", g(), (E = e.current) == null || E.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, o, s, r]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(n, t) {
  const o = G(() => _.Children.toArray(n).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const a = w(e.props.node.slotIndex) || 0, i = w(l.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (w(e.props.node.subSlotIndex) || 0) - (w(l.props.node.subSlotIndex) || 0) : a - i;
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
  const s = Ae(t, "actions");
  return /* @__PURE__ */ R.jsx(te.Item, {
    ...o,
    extra: n.extra ? /* @__PURE__ */ R.jsx(F, {
      slot: n.extra
    }) : o.extra,
    actions: s.length > 0 ? s.map((r, e) => /* @__PURE__ */ R.jsx(F, {
      slot: r
    }, e)) : o.actions,
    children: t
  });
});
export {
  Ne as ListItem,
  Ne as default
};
