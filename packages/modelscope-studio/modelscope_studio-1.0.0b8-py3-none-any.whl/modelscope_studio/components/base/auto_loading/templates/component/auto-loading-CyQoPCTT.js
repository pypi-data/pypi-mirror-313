import { g as ce, w as T } from "./Index-DYzeyzx_.js";
const x = window.ms_globals.React, se = window.ms_globals.React.forwardRef, W = window.ms_globals.React.useRef, C = window.ms_globals.React.useState, I = window.ms_globals.React.useEffect, ie = window.ms_globals.React.useCallback, D = window.ms_globals.ReactDOM.createPortal, ae = window.ms_globals.antd.theme, ue = window.ms_globals.antd.Spin, de = window.ms_globals.antd.Alert;
var ee = {
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
var fe = x, me = Symbol.for("react.element"), pe = Symbol.for("react.fragment"), _e = Object.prototype.hasOwnProperty, he = fe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ge = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function te(e, t, r) {
  var o, l = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) _e.call(t, o) && !ge.hasOwnProperty(o) && (l[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: me,
    type: e,
    key: n,
    ref: s,
    props: l,
    _owner: he.current
  };
}
j.Fragment = pe;
j.jsx = te;
j.jsxs = te;
ee.exports = j;
var g = ee.exports;
const {
  SvelteComponent: we,
  assign: K,
  binding_callbacks: V,
  check_outros: be,
  children: ne,
  claim_element: re,
  claim_space: ye,
  component_subscribe: J,
  compute_slots: Ee,
  create_slot: xe,
  detach: R,
  element: oe,
  empty: Y,
  exclude_internal_props: Z,
  get_all_dirty_from_scope: ve,
  get_slot_changes: Ce,
  group_outros: ke,
  init: Ie,
  insert_hydration: O,
  safe_not_equal: Re,
  set_custom_element_data: le,
  space: Pe,
  transition_in: L,
  transition_out: M,
  update_slot_base: Te
} = window.__gradio__svelte__internal, {
  beforeUpdate: Oe,
  getContext: Le,
  onDestroy: je,
  setContext: Se
} = window.__gradio__svelte__internal;
function Q(e) {
  let t, r;
  const o = (
    /*#slots*/
    e[7].default
  ), l = xe(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = oe("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = re(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = ne(t);
      l && l.l(s), s.forEach(R), this.h();
    },
    h() {
      le(t, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      O(n, t, s), l && l.m(t, null), e[9](t), r = !0;
    },
    p(n, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && Te(
        l,
        o,
        n,
        /*$$scope*/
        n[6],
        r ? Ce(
          o,
          /*$$scope*/
          n[6],
          s,
          null
        ) : ve(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (L(l, n), r = !0);
    },
    o(n) {
      M(l, n), r = !1;
    },
    d(n) {
      n && R(t), l && l.d(n), e[9](null);
    }
  };
}
function Fe(e) {
  let t, r, o, l, n = (
    /*$$slots*/
    e[4].default && Q(e)
  );
  return {
    c() {
      t = oe("react-portal-target"), r = Pe(), n && n.c(), o = Y(), this.h();
    },
    l(s) {
      t = re(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), ne(t).forEach(R), r = ye(s), n && n.l(s), o = Y(), this.h();
    },
    h() {
      le(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      O(s, t, c), e[8](t), O(s, r, c), n && n.m(s, c), O(s, o, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && L(n, 1)) : (n = Q(s), n.c(), L(n, 1), n.m(o.parentNode, o)) : n && (ke(), M(n, 1, 1, () => {
        n = null;
      }), be());
    },
    i(s) {
      l || (L(n), l = !0);
    },
    o(s) {
      M(n), l = !1;
    },
    d(s) {
      s && (R(t), R(r), R(o)), e[8](null), n && n.d(s);
    }
  };
}
function X(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function ze(e, t, r) {
  let o, l, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const c = Ee(n);
  let {
    svelteInit: i
  } = t;
  const b = T(X(t)), d = T();
  J(e, d, (u) => r(0, o = u));
  const m = T();
  J(e, m, (u) => r(1, l = u));
  const a = [], f = Le("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: w,
    subSlotIndex: _
  } = ce() || {}, y = i({
    parent: f,
    props: b,
    target: d,
    slot: m,
    slotKey: p,
    slotIndex: w,
    subSlotIndex: _,
    onDestroy(u) {
      a.push(u);
    }
  });
  Se("$$ms-gr-react-wrapper", y), Oe(() => {
    b.set(X(t));
  }), je(() => {
    a.forEach((u) => u());
  });
  function h(u) {
    V[u ? "unshift" : "push"](() => {
      o = u, d.set(o);
    });
  }
  function k(u) {
    V[u ? "unshift" : "push"](() => {
      l = u, m.set(l);
    });
  }
  return e.$$set = (u) => {
    r(17, t = K(K({}, t), Z(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = Z(t), [o, l, d, m, c, i, s, n, h, k];
}
class Ae extends we {
  constructor(t) {
    super(), Ie(this, t, ze, Fe, Re, {
      svelteInit: 5
    });
  }
}
const $ = window.ms_globals.rerender, F = window.ms_globals.tree;
function Ne(e) {
  function t(r) {
    const o = T(), l = new Ae({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? F;
          return c.nodes = [...c.nodes, s], $({
            createPortal: D,
            node: F
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== o), $({
              createPortal: D,
              node: F
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const qe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function De(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const o = e[r];
    return typeof o == "number" && !qe.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function G(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(D(x.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: x.Children.toArray(e._reactElement.props.children).map((l) => {
        if (x.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = G(l.props.el);
          return x.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...x.Children.toArray(l.props.children), ...n]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const o = Array.from(e.childNodes);
  for (let l = 0; l < o.length; l++) {
    const n = o[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = G(n);
      t.push(...c), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Me(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Ge = se(({
  slot: e,
  clone: t,
  className: r,
  style: o
}, l) => {
  const n = W(), [s, c] = C([]);
  return I(() => {
    var m;
    if (!n.current || !e)
      return;
    let i = e;
    function b() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Me(l, a), r && a.classList.add(...r.split(" ")), o) {
        const f = De(o);
        Object.keys(f).forEach((p) => {
          a.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var _, y, h;
        (_ = n.current) != null && _.contains(i) && ((y = n.current) == null || y.removeChild(i));
        const {
          portals: p,
          clonedElement: w
        } = G(e);
        return i = w, c(p), i.style.display = "contents", b(), (h = n.current) == null || h.appendChild(i), p.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", b(), (m = n.current) == null || m.appendChild(i);
    return () => {
      var a, f;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((f = n.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [e, t, r, o, l]), x.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function We(e, t) {
  return e ? /* @__PURE__ */ g.jsx(Ge, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function z({
  key: e,
  setSlotParams: t,
  slots: r
}, o) {
  return r[e] ? (...l) => (t(e, l), We(r[e], {
    clone: !0,
    ...o
  })) : void 0;
}
function A(e) {
  const t = W(e);
  return t.current = e, ie((...r) => {
    var o;
    return (o = t.current) == null ? void 0 : o.call(t, ...r);
  }, []);
}
function Be(e) {
  const [t, r] = C((e == null ? void 0 : e.eta) ?? null), {
    status: o,
    progress: l,
    queue_position: n,
    message: s,
    queue_size: c
  } = e || {}, [i, b] = C(0), [d, m] = C(0), [a, f] = C(null), [p, w] = C(null), [_, y] = C(null), h = W(!1), k = A(() => {
    requestAnimationFrame(() => {
      m((performance.now() - i) / 1e3), h.current && k();
    });
  }), u = A(() => {
    r(null), f(null), w(null), b(performance.now()), m(0), h.current = !0, k();
  }), P = A(() => {
    m(0), r(null), f(null), w(null), h.current = !1;
  });
  return I(() => {
    o === "pending" ? u() : P();
  }, [u, o, P]), I(() => {
    r((e == null ? void 0 : e.eta) ?? null);
  }, [e == null ? void 0 : e.eta]), I(() => {
    let E = t;
    E === null && (E = a, r(E)), E !== null && a !== E && (w(((performance.now() - i) / 1e3 + E).toFixed(1)), f(E));
  }, [t, a, i]), I(() => {
    y(d.toFixed(1));
  }, [d]), I(() => () => {
    h.current && P();
  }, []), {
    eta: t,
    formattedEta: p,
    formattedTimer: _,
    progress: l,
    queuePosition: n,
    queueSize: c,
    status: o,
    message: s
  };
}
let N = null;
function q(e) {
  const t = ["", "k", "M", "G", "T", "P", "E", "Z"];
  let r = 0;
  for (; e > 1e3 && r < t.length - 1; )
    e /= 1e3, r++;
  const o = t[r];
  return (Number.isInteger(e) ? e : e.toFixed(1)) + o;
}
const He = Ne(({
  slots: e,
  children: t,
  configType: r,
  loadingStatus: o,
  className: l,
  id: n,
  style: s,
  setSlotParams: c,
  showMask: i,
  showTimer: b,
  loadingText: d
}) => {
  var B, U, H;
  let m = null, a = null;
  const {
    status: f,
    message: p,
    progress: w,
    queuePosition: _,
    queueSize: y,
    eta: h,
    formattedEta: k,
    formattedTimer: u
  } = Be(o), P = f === "pending" || f === "generating", E = e.loadingText || typeof d == "string", {
    token: S
  } = ae.useToken();
  if (P)
    if (e.render)
      m = (B = z({
        setSlotParams: c,
        slots: e,
        key: "render"
      })) == null ? void 0 : B(o);
    else
      switch (r) {
        case "antd":
          m = /* @__PURE__ */ g.jsx(ue, {
            size: "small",
            delay: 200,
            style: {
              zIndex: S.zIndexPopupBase,
              backgroundColor: i ? S.colorBgMask : void 0
            },
            tip: E ? e.loadingText ? (U = z({
              setSlotParams: c,
              slots: e,
              key: "loadingText"
            })) == null ? void 0 : U(o) : d : f === "pending" ? /* @__PURE__ */ g.jsxs("div", {
              style: {
                textShadow: "none"
              },
              children: [w ? w.map((v) => /* @__PURE__ */ g.jsx(x.Fragment, {
                children: v.index != null && /* @__PURE__ */ g.jsxs(g.Fragment, {
                  children: [v.length != null ? `${q(v.index || 0)}/${q(v.length)}` : `${q(v.index || 0)}`, v.unit, " "]
                })
              }, v.index)) : _ !== null && y !== void 0 && typeof _ == "number" && _ >= 0 ? `queue: ${_ + 1}/${y} |` : _ === 0 ? "processing |" : null, " ", b && /* @__PURE__ */ g.jsxs(g.Fragment, {
                children: [u, h ? `/${k}` : "", "s"]
              })]
            }) : null,
            className: "ms-gr-auto-loading-default-antd",
            children: /* @__PURE__ */ g.jsx("div", {})
          });
          break;
      }
  if (f === "error" && !N)
    if (e.errorRender)
      a = (H = z({
        setSlotParams: c,
        slots: e,
        key: "errorRender"
      })) == null ? void 0 : H(o);
    else
      switch (r) {
        case "antd":
          N = a = /* @__PURE__ */ g.jsx(de, {
            closable: !0,
            className: "ms-gr-auto-loading-error-default-antd",
            style: {
              zIndex: S.zIndexPopupBase
            },
            message: "Error",
            description: p,
            type: "error",
            onClose: () => {
              N = null;
            }
          });
          break;
      }
  return /* @__PURE__ */ g.jsxs("div", {
    className: l,
    id: n,
    style: s,
    children: [m, a, t]
  });
});
export {
  He as AutoLoading,
  He as default
};
