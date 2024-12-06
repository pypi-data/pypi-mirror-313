import { g as $, w as x, d as ee, a as b } from "./Index-BhOOL6cU.js";
const _ = window.ms_globals.React, G = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Space;
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
var ne = _, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) se.call(t, l) && !ie.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: re,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: le.current
  };
}
C.Fragment = oe;
C.jsx = V;
C.jsxs = V;
K.exports = C;
var h = K.exports;
const {
  SvelteComponent: ae,
  assign: T,
  binding_callbacks: j,
  check_outros: ce,
  children: q,
  claim_element: B,
  claim_space: de,
  component_subscribe: A,
  compute_slots: ue,
  create_slot: fe,
  detach: g,
  element: J,
  empty: N,
  exclude_internal_props: D,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: S,
  safe_not_equal: ge,
  set_custom_element_data: Y,
  space: we,
  transition_in: I,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: Ee,
  onDestroy: ve,
  setContext: xe
} = window.__gradio__svelte__internal;
function F(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = fe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = J("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = B(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = q(t);
      o && o.l(s), s.forEach(g), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      S(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && be(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? _e(
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
      r || (I(o, e), r = !0);
    },
    o(e) {
      k(o, e), r = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function Se(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = J("react-portal-target"), r = we(), e && e.c(), l = N(), this.h();
    },
    l(s) {
      t = B(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(g), r = de(s), e && e.l(s), l = N(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      S(s, t, a), n[8](t), S(s, r, a), e && e.m(s, a), S(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && I(e, 1)) : (e = F(s), e.c(), I(e, 1), e.m(l.parentNode, l)) : e && (me(), k(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      o || (I(e), o = !0);
    },
    o(s) {
      k(e), o = !1;
    },
    d(s) {
      s && (g(t), g(r), g(l)), n[8](null), e && e.d(s);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ie(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = ue(e);
  let {
    svelteInit: i
  } = t;
  const w = x(M(t)), u = x();
  A(n, u, (c) => r(0, l = c));
  const m = x();
  A(n, m, (c) => r(1, o = c));
  const d = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y
  } = $() || {}, E = i({
    parent: f,
    props: w,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y,
    onDestroy(c) {
      d.push(c);
    }
  });
  xe("$$ms-gr-react-wrapper", E), ye(() => {
    w.set(M(t));
  }), ve(() => {
    d.forEach((c) => c());
  });
  function v(c) {
    j[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function Q(c) {
    j[c ? "unshift" : "push"](() => {
      o = c, m.set(o);
    });
  }
  return n.$$set = (c) => {
    r(17, t = T(T({}, t), D(c))), "svelteInit" in c && r(5, i = c.svelteInit), "$$scope" in c && r(6, s = c.$$scope);
  }, t = D(t), [l, o, u, m, a, i, s, e, v, Q];
}
class Ce extends ae {
  constructor(t) {
    super(), he(this, t, Ie, Se, ge, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Re(n) {
  function t(r) {
    const l = x(), o = new Ce({
      ...r,
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
          }, a = e.parent ?? O;
          return a.nodes = [...a.nodes, s], W({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), W({
              createPortal: P,
              node: O
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function Oe(n) {
  const [t, r] = U(() => b(n));
  return H(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Pe(n) {
  const t = G(() => ee(n, (r) => r), [n]);
  return Oe(t);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !ke.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function L(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(P(_.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: _.Children.toArray(n._reactElement.props.children).map((o) => {
        if (_.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = L(o.props.el);
          return _.cloneElement(o, {
            ...o.props,
            el: s,
            children: [..._.Children.toArray(o.props.children), ...e]
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
      listener: s,
      type: a,
      useCapture: i
    }) => {
      r.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = L(e);
      t.push(...a), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Te(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const z = X(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = Z(), [s, a] = U([]);
  return H(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Te(o, d), r && d.classList.add(...r.split(" ")), l) {
        const f = Le(l);
        Object.keys(f).forEach((p) => {
          d.style[p] = f[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let d = function() {
        var y, E, v;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: R
        } = L(n);
        return i = R, a(p), i.style.display = "contents", w(), (v = e.current) == null || v.appendChild(i), p.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, r, l, o]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(n, t) {
  const r = G(() => _.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const a = b(e.props.node.slotIndex) || 0, i = b(s.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (b(e.props.node.subSlotIndex) || 0) - (b(s.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Pe(r);
}
const Ne = Re(({
  slots: n,
  children: t,
  ...r
}) => {
  const l = je(t);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ h.jsx(te, {
      ...r,
      split: n.split ? /* @__PURE__ */ h.jsx(z, {
        slot: n.split,
        clone: !0
      }) : r.split,
      children: l.map((o, e) => /* @__PURE__ */ h.jsx(z, {
        slot: o
      }, e))
    })]
  });
});
export {
  Ne as Space,
  Ne as default
};
