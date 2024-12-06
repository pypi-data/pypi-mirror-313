import { g as ee, w as E } from "./Index-BDU4HkVt.js";
const _ = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, $ = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Image;
var G = {
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
var ne = _, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, le = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(e, t, r) {
  var s, o = {}, n = null, l = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) se.call(t, s) && !ie.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: re,
    type: e,
    key: n,
    ref: l,
    props: o,
    _owner: le.current
  };
}
x.Fragment = oe;
x.jsx = H;
x.jsxs = H;
G.exports = x;
var w = G.exports;
const {
  SvelteComponent: ce,
  assign: T,
  binding_callbacks: F,
  check_outros: ae,
  children: K,
  claim_element: q,
  claim_space: ue,
  component_subscribe: N,
  compute_slots: de,
  create_slot: fe,
  detach: h,
  element: V,
  empty: A,
  exclude_internal_props: W,
  get_all_dirty_from_scope: pe,
  get_slot_changes: me,
  group_outros: _e,
  init: he,
  insert_hydration: R,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: we,
  transition_in: C,
  transition_out: j,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: Re
} = window.__gradio__svelte__internal;
function D(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), o = fe(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = q(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = K(t);
      o && o.l(l), l.forEach(h), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      R(n, t, l), o && o.m(t, null), e[9](t), r = !0;
    },
    p(n, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ve(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? me(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (C(o, n), r = !0);
    },
    o(n) {
      j(o, n), r = !1;
    },
    d(n) {
      n && h(t), o && o.d(n), e[9](null);
    }
  };
}
function Ce(e) {
  let t, r, s, o, n = (
    /*$$slots*/
    e[4].default && D(e)
  );
  return {
    c() {
      t = V("react-portal-target"), r = we(), n && n.c(), s = A(), this.h();
    },
    l(l) {
      t = q(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(h), r = ue(l), n && n.l(l), s = A(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      R(l, t, c), e[8](t), R(l, r, c), n && n.m(l, c), R(l, s, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && C(n, 1)) : (n = D(l), n.c(), C(n, 1), n.m(s.parentNode, s)) : n && (_e(), j(n, 1, 1, () => {
        n = null;
      }), ae());
    },
    i(l) {
      o || (C(n), o = !0);
    },
    o(l) {
      j(n), o = !1;
    },
    d(l) {
      l && (h(t), h(r), h(s)), e[8](null), n && n.d(l);
    }
  };
}
function M(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ie(e, t, r) {
  let s, o, {
    $$slots: n = {},
    $$scope: l
  } = t;
  const c = de(n);
  let {
    svelteInit: i
  } = t;
  const g = E(M(t)), d = E();
  N(e, d, (a) => r(0, s = a));
  const m = E();
  N(e, m, (a) => r(1, o = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: S,
    subSlotIndex: v
  } = ee() || {}, b = i({
    parent: f,
    props: g,
    target: d,
    slot: m,
    slotKey: p,
    slotIndex: S,
    subSlotIndex: v,
    onDestroy(a) {
      u.push(a);
    }
  });
  Re("$$ms-gr-react-wrapper", b), be(() => {
    g.set(M(t));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function y(a) {
    F[a ? "unshift" : "push"](() => {
      s = a, d.set(s);
    });
  }
  function J(a) {
    F[a ? "unshift" : "push"](() => {
      o = a, m.set(o);
    });
  }
  return e.$$set = (a) => {
    r(17, t = T(T({}, t), W(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, l = a.$$scope);
  }, t = W(t), [s, o, d, m, c, i, l, n, y, J];
}
class xe extends ce {
  constructor(t) {
    super(), he(this, t, Ie, Ce, ge, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, k = window.ms_globals.tree;
function Se(e) {
  function t(r) {
    const s = E(), o = new xe({
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
          }, c = n.parent ?? k;
          return c.nodes = [...c.nodes, l], U({
            createPortal: P,
            node: k
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), U({
              createPortal: P,
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
      r(t);
    });
  });
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return typeof s == "number" && !ke.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function L(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(P(_.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: _.Children.toArray(e._reactElement.props.children).map((o) => {
        if (_.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: l
          } = L(o.props.el);
          return _.cloneElement(o, {
            ...o.props,
            el: l,
            children: [..._.Children.toArray(o.props.children), ...n]
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
function Pe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const I = Y(({
  slot: e,
  clone: t,
  className: r,
  style: s
}, o) => {
  const n = Q(), [l, c] = X([]);
  return Z(() => {
    var m;
    if (!n.current || !e)
      return;
    let i = e;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Pe(o, u), r && u.classList.add(...r.split(" ")), s) {
        const f = Oe(s);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var v, b, y;
        (v = n.current) != null && v.contains(i) && ((b = n.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: S
        } = L(e);
        return i = S, c(p), i.style.display = "contents", g(), (y = n.current) == null || y.appendChild(i), p.length > 0;
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
  }, [e, t, r, s, o]), _.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...l);
});
function je(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Le(e, t = !1) {
  try {
    if (t && !je(e))
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
function O(e, t) {
  return $(() => Le(e, t), [e, t]);
}
function Te(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function Fe(e, t) {
  return e ? /* @__PURE__ */ w.jsx(I, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function z({
  key: e,
  setSlotParams: t,
  slots: r
}, s) {
  return r[e] ? (...o) => (t(e, o), Fe(r[e], {
    clone: !0,
    ...s
  })) : void 0;
}
function Ne(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const We = Se(({
  slots: e,
  preview: t,
  setSlotParams: r,
  ...s
}) => {
  const o = Ne(t), n = e["preview.mask"] || e["preview.closeIcon"] || e["preview.toolbarRender"] || e["preview.imageRender"] || t !== !1, l = O(o.getContainer), c = O(o.toolbarRender), i = O(o.imageRender);
  return /* @__PURE__ */ w.jsx(te, {
    ...s,
    preview: n ? Te({
      ...o,
      getContainer: l,
      toolbarRender: e["preview.toolbarRender"] ? z({
        slots: e,
        setSlotParams: r,
        key: "preview.toolbarRender"
      }) : c,
      imageRender: e["preview.imageRender"] ? z({
        slots: e,
        setSlotParams: r,
        key: "preview.imageRender"
      }) : i,
      ...e["preview.mask"] || Reflect.has(o, "mask") ? {
        mask: e["preview.mask"] ? /* @__PURE__ */ w.jsx(I, {
          slot: e["preview.mask"]
        }) : o.mask
      } : {},
      closeIcon: e["preview.closeIcon"] ? /* @__PURE__ */ w.jsx(I, {
        slot: e["preview.closeIcon"]
      }) : o.closeIcon
    }) : !1,
    placeholder: e.placeholder ? /* @__PURE__ */ w.jsx(I, {
      slot: e.placeholder
    }) : s.placeholder
  });
});
export {
  We as Image,
  We as default
};
