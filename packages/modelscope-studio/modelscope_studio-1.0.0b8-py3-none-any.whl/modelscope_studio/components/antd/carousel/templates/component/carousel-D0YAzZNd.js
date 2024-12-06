import { g as $, w as C, d as ee, a as b } from "./Index-BlaIr913.js";
const _ = window.ms_globals.React, T = window.ms_globals.React.useMemo, U = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Carousel;
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
S.Fragment = oe;
S.jsx = V;
S.jsxs = V;
K.exports = S;
var w = K.exports;
const {
  SvelteComponent: ce,
  assign: j,
  binding_callbacks: A,
  check_outros: ae,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: h,
  element: J,
  empty: N,
  exclude_internal_props: W,
  get_all_dirty_from_scope: pe,
  get_slot_changes: _e,
  group_outros: me,
  init: he,
  insert_hydration: x,
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
  setContext: Ce
} = window.__gradio__svelte__internal;
function D(n) {
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
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      x(e, t, s), o && o.m(t, null), n[9](t), r = !0;
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
      e && h(t), o && o.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      t = J("react-portal-target"), r = we(), e && e.c(), l = N(), this.h();
    },
    l(s) {
      t = B(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(t).forEach(h), r = ue(s), e && e.l(s), l = N(), this.h();
    },
    h() {
      Y(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      x(s, t, c), n[8](t), x(s, r, c), e && e.m(s, c), x(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && I(e, 1)) : (e = D(s), e.c(), I(e, 1), e.m(l.parentNode, l)) : e && (me(), k(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(s) {
      o || (I(e), o = !0);
    },
    o(s) {
      k(e), o = !1;
    },
    d(s) {
      s && (h(t), h(r), h(l)), n[8](null), e && e.d(s);
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
  const c = de(e);
  let {
    svelteInit: i
  } = t;
  const g = C(M(t)), d = C();
  F(n, d, (a) => r(0, l = a));
  const m = C();
  F(n, m, (a) => r(1, o = a));
  const u = [], f = Ee("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y
  } = $() || {}, E = i({
    parent: f,
    props: g,
    target: d,
    slot: m,
    slotKey: p,
    slotIndex: R,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ce("$$ms-gr-react-wrapper", E), ye(() => {
    g.set(M(t));
  }), ve(() => {
    u.forEach((a) => a());
  });
  function v(a) {
    A[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function Q(a) {
    A[a ? "unshift" : "push"](() => {
      o = a, m.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = j(j({}, t), W(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = W(t), [l, o, d, m, c, i, s, e, v, Q];
}
class Se extends ce {
  constructor(t) {
    super(), he(this, t, Ie, xe, ge, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, O = window.ms_globals.tree;
function Re(n) {
  function t(r) {
    const l = C(), o = new Se({
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
          }, c = e.parent ?? O;
          return c.nodes = [...c.nodes, s], z({
            createPortal: P,
            node: O
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), z({
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
  const t = T(() => ee(n, (r) => r), [n]);
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
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = L(e);
      t.push(...c), r.appendChild(s);
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
const je = X(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = Z(), [s, c] = U([]);
  return H(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Te(o, u), r && u.classList.add(...r.split(" ")), l) {
        const f = Le(l);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var y, E, v;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: R
        } = L(n);
        return i = R, c(p), i.style.display = "contents", g(), (v = e.current) == null || v.appendChild(i), p.length > 0;
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
  }, [n, t, r, l, o]), _.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ae(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Fe(n, t = !1) {
  try {
    if (t && !Ae(n))
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
function G(n, t) {
  return T(() => Fe(n, t), [n, t]);
}
function Ne(n, t) {
  const r = T(() => _.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const c = b(e.props.node.slotIndex) || 0, i = b(s.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (b(e.props.node.subSlotIndex) || 0) - (b(s.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Pe(r);
}
const De = Re(({
  afterChange: n,
  beforeChange: t,
  children: r,
  ...l
}) => {
  const o = G(n), e = G(t), s = Ne(r);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ w.jsx(te, {
      ...l,
      afterChange: o,
      beforeChange: e,
      children: s.map((c, i) => /* @__PURE__ */ w.jsx(je, {
        clone: !0,
        slot: c
      }, i))
    })]
  });
});
export {
  De as Carousel,
  De as default
};
