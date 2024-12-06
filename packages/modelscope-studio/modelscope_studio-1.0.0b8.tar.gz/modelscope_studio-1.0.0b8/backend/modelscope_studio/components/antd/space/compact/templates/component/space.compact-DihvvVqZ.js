import { g as Z, w as x, d as $, a as b } from "./Index-Cdzq6Vqf.js";
const _ = window.ms_globals.React, z = window.ms_globals.React.useMemo, G = window.ms_globals.React.useState, U = window.ms_globals.React.useEffect, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Space;
var H = {
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
var te = _, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function K(n, t, o) {
  var l, r = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) re.call(t, l) && !le.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: s,
    props: r,
    _owner: se.current
  };
}
C.Fragment = oe;
C.jsx = K;
C.jsxs = K;
H.exports = C;
var w = H.exports;
const {
  SvelteComponent: ie,
  assign: T,
  binding_callbacks: j,
  check_outros: ae,
  children: V,
  claim_element: q,
  claim_space: ce,
  component_subscribe: A,
  compute_slots: de,
  create_slot: ue,
  detach: h,
  element: B,
  empty: N,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: S,
  safe_not_equal: he,
  set_custom_element_data: J,
  space: ge,
  transition_in: I,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: ve
} = window.__gradio__svelte__internal;
function F(n) {
  let t, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = ue(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = B("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = V(t);
      r && r.l(s), s.forEach(h), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      S(e, t, s), r && r.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && we(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        o ? pe(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : fe(
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
function xe(n) {
  let t, o, l, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = B("react-portal-target"), o = ge(), e && e.c(), l = N(), this.h();
    },
    l(s) {
      t = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), V(t).forEach(h), o = ce(s), e && e.l(s), l = N(), this.h();
    },
    h() {
      J(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      S(s, t, a), n[8](t), S(s, o, a), e && e.m(s, a), S(s, l, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && I(e, 1)) : (e = F(s), e.c(), I(e, 1), e.m(l.parentNode, l)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(s) {
      r || (I(e), r = !0);
    },
    o(s) {
      k(e), r = !1;
    },
    d(s) {
      s && (h(t), h(o), h(l)), n[8](null), e && e.d(s);
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
  const a = de(e);
  let {
    svelteInit: i
  } = t;
  const g = x(M(t)), u = x();
  A(n, u, (c) => o(0, l = c));
  const m = x();
  A(n, m, (c) => o(1, r = c));
  const d = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y
  } = Z() || {}, E = i({
    parent: f,
    props: g,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y,
    onDestroy(c) {
      d.push(c);
    }
  });
  ve("$$ms-gr-react-wrapper", E), be(() => {
    g.set(M(t));
  }), Ee(() => {
    d.forEach((c) => c());
  });
  function v(c) {
    j[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  function Y(c) {
    j[c ? "unshift" : "push"](() => {
      r = c, m.set(r);
    });
  }
  return n.$$set = (c) => {
    o(17, t = T(T({}, t), D(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = D(t), [l, r, u, m, a, i, s, e, v, Y];
}
class Ie extends ie {
  constructor(t) {
    super(), me(this, t, Se, xe, he, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const l = x(), r = new Ie({
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
function Re(n) {
  const [t, o] = G(() => b(n));
  return U(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Oe(n) {
  const t = z(() => $(n, (o) => o), [n]);
  return Re(t);
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const l = n[o];
    return typeof l == "number" && !Pe.includes(o) ? t[o] = l + "px" : t[o] = l, t;
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
            clonedElement: s
          } = L(r.props.el);
          return _.cloneElement(r, {
            ...r.props,
            el: s,
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
      listener: s,
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = L(e);
      t.push(...a), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function Le(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Te = Q(({
  slot: n,
  clone: t,
  className: o,
  style: l
}, r) => {
  const e = X(), [s, a] = G([]);
  return U(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Le(r, d), o && d.classList.add(...o.split(" ")), l) {
        const f = ke(l);
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
        return i = R, a(p), i.style.display = "contents", g(), (v = e.current) == null || v.appendChild(i), p.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((f = e.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, t, o, l, r]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(n, t) {
  const o = z(() => _.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const a = b(e.props.node.slotIndex) || 0, i = b(s.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (b(e.props.node.subSlotIndex) || 0) - (b(s.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Oe(o);
}
const Ne = Ce(({
  children: n,
  ...t
}) => {
  const o = je(n);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ w.jsx(ee.Compact, {
      ...t,
      children: o.map((l, r) => /* @__PURE__ */ w.jsx(Te, {
        slot: l
      }, r))
    })]
  });
});
export {
  Ne as Space,
  Ne as default
};
