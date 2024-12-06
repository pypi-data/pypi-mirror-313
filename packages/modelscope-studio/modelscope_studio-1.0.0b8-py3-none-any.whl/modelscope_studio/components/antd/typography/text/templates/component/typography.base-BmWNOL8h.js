import { g as se, w as R, d as le, a as v, c as ie } from "./Index-Cgg6ubPB.js";
const b = window.ms_globals.React, O = window.ms_globals.React.useMemo, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, oe = window.ms_globals.React.forwardRef, re = window.ms_globals.React.useRef, D = window.ms_globals.ReactDOM.createPortal, I = window.ms_globals.antd.Typography;
var X = {
  exports: {}
}, j = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ae = b, ce = Symbol.for("react.element"), de = Symbol.for("react.fragment"), ue = Object.prototype.hasOwnProperty, pe = ae.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, fe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(t, n, o) {
  var s, r = {}, e = null, l = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) ue.call(n, s) && !fe.hasOwnProperty(s) && (r[s] = n[s]);
  if (t && t.defaultProps) for (s in n = t.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: ce,
    type: t,
    key: e,
    ref: l,
    props: r,
    _owner: pe.current
  };
}
j.Fragment = de;
j.jsx = Z;
j.jsxs = Z;
X.exports = j;
var p = X.exports;
const {
  SvelteComponent: _e,
  assign: W,
  binding_callbacks: z,
  check_outros: me,
  children: $,
  claim_element: ee,
  claim_space: he,
  component_subscribe: G,
  compute_slots: ge,
  create_slot: be,
  detach: C,
  element: te,
  empty: B,
  exclude_internal_props: H,
  get_all_dirty_from_scope: ye,
  get_slot_changes: we,
  group_outros: xe,
  init: Ee,
  insert_hydration: P,
  safe_not_equal: Ce,
  set_custom_element_data: ne,
  space: ve,
  transition_in: T,
  transition_out: F,
  update_slot_base: Ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: Se,
  getContext: Re,
  onDestroy: Pe,
  setContext: Te
} = window.__gradio__svelte__internal;
function K(t) {
  let n, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = be(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = te("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      n = ee(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = $(n);
      r && r.l(l), l.forEach(C), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      P(e, n, l), r && r.m(n, null), t[9](n), o = !0;
    },
    p(e, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && Ie(
        r,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? we(
          s,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ye(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (T(r, e), o = !0);
    },
    o(e) {
      F(r, e), o = !1;
    },
    d(e) {
      e && C(n), r && r.d(e), t[9](null);
    }
  };
}
function Oe(t) {
  let n, o, s, r, e = (
    /*$$slots*/
    t[4].default && K(t)
  );
  return {
    c() {
      n = te("react-portal-target"), o = ve(), e && e.c(), s = B(), this.h();
    },
    l(l) {
      n = ee(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(n).forEach(C), o = he(l), e && e.l(l), s = B(), this.h();
    },
    h() {
      ne(n, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      P(l, n, a), t[8](n), P(l, o, a), e && e.m(l, a), P(l, s, a), r = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, a), a & /*$$slots*/
      16 && T(e, 1)) : (e = K(l), e.c(), T(e, 1), e.m(s.parentNode, s)) : e && (xe(), F(e, 1, 1, () => {
        e = null;
      }), me());
    },
    i(l) {
      r || (T(e), r = !0);
    },
    o(l) {
      F(e), r = !1;
    },
    d(l) {
      l && (C(n), C(o), C(s)), t[8](null), e && e.d(l);
    }
  };
}
function V(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function je(t, n, o) {
  let s, r, {
    $$slots: e = {},
    $$scope: l
  } = n;
  const a = ge(e);
  let {
    svelteInit: i
  } = n;
  const w = R(V(n)), u = R();
  G(t, u, (c) => o(0, s = c));
  const _ = R();
  G(t, _, (c) => o(1, r = c));
  const d = [], m = Re("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: x,
    subSlotIndex: h
  } = se() || {}, g = i({
    parent: m,
    props: w,
    target: u,
    slot: _,
    slotKey: f,
    slotIndex: x,
    subSlotIndex: h,
    onDestroy(c) {
      d.push(c);
    }
  });
  Te("$$ms-gr-react-wrapper", g), Se(() => {
    w.set(V(n));
  }), Pe(() => {
    d.forEach((c) => c());
  });
  function E(c) {
    z[c ? "unshift" : "push"](() => {
      s = c, u.set(s);
    });
  }
  function k(c) {
    z[c ? "unshift" : "push"](() => {
      r = c, _.set(r);
    });
  }
  return t.$$set = (c) => {
    o(17, n = W(W({}, n), H(c))), "svelteInit" in c && o(5, i = c.svelteInit), "$$scope" in c && o(6, l = c.$$scope);
  }, n = H(n), [s, r, u, _, a, i, l, e, E, k];
}
class ke extends _e {
  constructor(n) {
    super(), Ee(this, n, je, Oe, Ce, {
      svelteInit: 5
    });
  }
}
const q = window.ms_globals.rerender, N = window.ms_globals.tree;
function Le(t) {
  function n(o) {
    const s = R(), r = new ke({
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
          }, a = e.parent ?? N;
          return a.nodes = [...a.nodes, l], q({
            createPortal: D,
            node: N
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), q({
              createPortal: D,
              node: N
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
function Ae(t) {
  const [n, o] = Y(() => v(t));
  return Q(() => {
    let s = !0;
    return t.subscribe((e) => {
      s && (s = !1, e === n) || o(e);
    });
  }, [t]), n;
}
function Ne(t) {
  const n = O(() => le(t, (o) => o), [t]);
  return Ae(n);
}
const De = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const s = t[o];
    return typeof s == "number" && !De.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function M(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(D(b.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: b.Children.toArray(t._reactElement.props.children).map((r) => {
        if (b.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = M(r.props.el);
          return b.cloneElement(r, {
            ...r.props,
            el: l,
            children: [...b.Children.toArray(r.props.children), ...e]
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
      type: a,
      useCapture: i
    }) => {
      o.addEventListener(a, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const e = s[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = M(e);
      n.push(...a), o.appendChild(l);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Me(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const y = oe(({
  slot: t,
  clone: n,
  className: o,
  style: s
}, r) => {
  const e = re(), [l, a] = Y([]);
  return Q(() => {
    var _;
    if (!e.current || !t)
      return;
    let i = t;
    function w() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Me(r, d), o && d.classList.add(...o.split(" ")), s) {
        const m = Fe(s);
        Object.keys(m).forEach((f) => {
          d.style[f] = m[f];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let d = function() {
        var h, g, E;
        (h = e.current) != null && h.contains(i) && ((g = e.current) == null || g.removeChild(i));
        const {
          portals: f,
          clonedElement: x
        } = M(t);
        return i = x, a(f), i.style.display = "contents", w(), (E = e.current) == null || E.appendChild(i), f.length > 0;
      };
      d() || (u = new window.MutationObserver(() => {
        d() && (u == null || u.disconnect());
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var d, m;
      i.style.display = "", (d = e.current) != null && d.contains(i) && ((m = e.current) == null || m.removeChild(i)), u == null || u.disconnect();
    };
  }, [t, n, o, s, r]), b.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ue(t) {
  return O(() => {
    const n = b.Children.toArray(t), o = [], s = [];
    return n.forEach((r) => {
      r.props.node && r.props.nodeSlotKey ? o.push(r) : s.push(r);
    }), [o, s];
  }, [t]);
}
function We(t) {
  return Object.keys(t).reduce((n, o) => (t[o] !== void 0 && (n[o] = t[o]), n), {});
}
function ze(t, n) {
  return t ? /* @__PURE__ */ p.jsx(y, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Ge({
  key: t,
  setSlotParams: n,
  slots: o
}, s) {
  return o[t] ? (...r) => (n(t, r), ze(o[t], {
    clone: !0,
    ...s
  })) : void 0;
}
function J(t, n) {
  const o = O(() => b.Children.toArray(t).filter((e) => e.props.node && (!n && !e.props.nodeSlotKey || n && n === e.props.nodeSlotKey)).sort((e, l) => {
    if (e.props.node.slotIndex && l.props.node.slotIndex) {
      const a = v(e.props.node.slotIndex) || 0, i = v(l.props.node.slotIndex) || 0;
      return a - i === 0 && e.props.node.subSlotIndex && l.props.node.subSlotIndex ? (v(e.props.node.subSlotIndex) || 0) - (v(l.props.node.subSlotIndex) || 0) : a - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [t, n]);
  return Ne(o);
}
function S(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const He = Le(({
  component: t,
  className: n,
  slots: o,
  children: s,
  copyable: r,
  editable: e,
  ellipsis: l,
  setSlotParams: a,
  value: i,
  ...w
}) => {
  var U;
  const u = J(s, "copyable.tooltips"), _ = J(s, "copyable.icon"), d = o["copyable.icon"] || u.length > 0 || r, m = o["editable.icon"] || o["editable.tooltip"] || o["editable.enterIcon"] || e, f = o["ellipsis.symbol"] || o["ellipsis.tooltip"] || o["ellipsis.tooltip.title"] || l, x = S(r), h = S(e), g = S(l), E = O(() => {
    switch (t) {
      case "title":
        return I.Title;
      case "paragraph":
        return I.Paragraph;
      case "text":
        return I.Text;
      case "link":
        return I.Link;
    }
  }, [t]), [k, c] = Ue(s);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: k
    }), /* @__PURE__ */ p.jsx(E, {
      ...w,
      className: ie(n, `ms-gr-antd-typography-${t}`),
      copyable: d ? We({
        text: i,
        ...S(r),
        tooltips: u.length > 0 ? u.map((L, A) => /* @__PURE__ */ p.jsx(y, {
          slot: L
        }, A)) : x.tooltips,
        icon: _.length > 0 ? _.map((L, A) => /* @__PURE__ */ p.jsx(y, {
          slot: L
        }, A)) : x.icon
      }) : void 0,
      editable: m ? {
        ...h,
        icon: o["editable.icon"] ? /* @__PURE__ */ p.jsx(y, {
          slot: o["editable.icon"]
        }) : h.icon,
        tooltip: o["editable.tooltip"] ? /* @__PURE__ */ p.jsx(y, {
          slot: o["editable.tooltip"]
        }) : h.tooltip,
        enterIcon: o["editable.enterIcon"] ? /* @__PURE__ */ p.jsx(y, {
          slot: o["editable.enterIcon"]
        }) : h.enterIcon
      } : void 0,
      ellipsis: t === "link" ? !!f : f ? {
        ...g,
        symbol: o["ellipsis.symbol"] ? Ge({
          key: "ellipsis.symbol",
          setSlotParams: a,
          slots: o
        }, {
          clone: !0
        }) : g.symbol,
        tooltip: o["ellipsis.tooltip"] ? /* @__PURE__ */ p.jsx(y, {
          slot: o["ellipsis.tooltip"]
        }) : {
          ...g.tooltip,
          title: o["ellipsis.tooltip.title"] ? /* @__PURE__ */ p.jsx(y, {
            slot: o["ellipsis.tooltip.title"]
          }) : (U = g.tooltip) == null ? void 0 : U.title
        }
      } : void 0,
      children: c
    })]
  });
});
export {
  He as TypographyBase,
  He as default
};
