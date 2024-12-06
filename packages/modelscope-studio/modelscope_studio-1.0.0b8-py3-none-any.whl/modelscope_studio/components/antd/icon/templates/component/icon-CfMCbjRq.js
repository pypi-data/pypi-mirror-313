import { g as J, w as d } from "./Index-sQDf10Kh.js";
const C = window.ms_globals.React, I = window.ms_globals.ReactDOM.createPortal, M = window.ms_globals.antdIcons;
var j = {
  exports: {}
}, g = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var V = C, Y = Symbol.for("react.element"), H = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(r, t, l) {
  var o, n = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) Q.call(t, o) && !Z.hasOwnProperty(o) && (n[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) n[o] === void 0 && (n[o] = t[o]);
  return {
    $$typeof: Y,
    type: r,
    key: e,
    ref: s,
    props: n,
    _owner: X.current
  };
}
g.Fragment = H;
g.jsx = D;
g.jsxs = D;
j.exports = g;
var b = j.exports;
const {
  SvelteComponent: $,
  assign: k,
  binding_callbacks: E,
  check_outros: ee,
  children: L,
  claim_element: A,
  claim_space: te,
  component_subscribe: R,
  compute_slots: se,
  create_slot: oe,
  detach: i,
  element: N,
  empty: x,
  exclude_internal_props: S,
  get_all_dirty_from_scope: ne,
  get_slot_changes: le,
  group_outros: re,
  init: ae,
  insert_hydration: p,
  safe_not_equal: ce,
  set_custom_element_data: q,
  space: ie,
  transition_in: m,
  transition_out: h,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: ue,
  getContext: fe,
  onDestroy: de,
  setContext: pe
} = window.__gradio__svelte__internal;
function O(r) {
  let t, l;
  const o = (
    /*#slots*/
    r[7].default
  ), n = oe(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = N("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = A(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = L(t);
      n && n.l(s), s.forEach(i), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), n && n.m(t, null), r[9](t), l = !0;
    },
    p(e, s) {
      n && n.p && (!l || s & /*$$scope*/
      64) && _e(
        n,
        o,
        e,
        /*$$scope*/
        e[6],
        l ? le(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ne(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      l || (m(n, e), l = !0);
    },
    o(e) {
      h(n, e), l = !1;
    },
    d(e) {
      e && i(t), n && n.d(e), r[9](null);
    }
  };
}
function me(r) {
  let t, l, o, n, e = (
    /*$$slots*/
    r[4].default && O(r)
  );
  return {
    c() {
      t = N("react-portal-target"), l = ie(), e && e.c(), o = x(), this.h();
    },
    l(s) {
      t = A(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), L(t).forEach(i), l = te(s), e && e.l(s), o = x(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      p(s, t, c), r[8](t), p(s, l, c), e && e.m(s, c), p(s, o, c), n = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && m(e, 1)) : (e = O(s), e.c(), m(e, 1), e.m(o.parentNode, o)) : e && (re(), h(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(s) {
      n || (m(e), n = !0);
    },
    o(s) {
      h(e), n = !1;
    },
    d(s) {
      s && (i(t), i(l), i(o)), r[8](null), e && e.d(s);
    }
  };
}
function P(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function ge(r, t, l) {
  let o, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = se(e);
  let {
    svelteInit: _
  } = t;
  const v = d(P(t)), u = d();
  R(r, u, (a) => l(0, o = a));
  const f = d();
  R(r, f, (a) => l(1, n = a));
  const y = [], F = fe("$$ms-gr-react-wrapper"), {
    slotKey: K,
    slotIndex: U,
    subSlotIndex: W
  } = J() || {}, z = _({
    parent: F,
    props: v,
    target: u,
    slot: f,
    slotKey: K,
    slotIndex: U,
    subSlotIndex: W,
    onDestroy(a) {
      y.push(a);
    }
  });
  pe("$$ms-gr-react-wrapper", z), ue(() => {
    v.set(P(t));
  }), de(() => {
    y.forEach((a) => a());
  });
  function B(a) {
    E[a ? "unshift" : "push"](() => {
      o = a, u.set(o);
    });
  }
  function G(a) {
    E[a ? "unshift" : "push"](() => {
      n = a, f.set(n);
    });
  }
  return r.$$set = (a) => {
    l(17, t = k(k({}, t), S(a))), "svelteInit" in a && l(5, _ = a.svelteInit), "$$scope" in a && l(6, s = a.$$scope);
  }, t = S(t), [o, n, u, f, c, _, s, e, B, G];
}
class be extends $ {
  constructor(t) {
    super(), ae(this, t, ge, me, ce, {
      svelteInit: 5
    });
  }
}
const T = window.ms_globals.rerender, w = window.ms_globals.tree;
function we(r) {
  function t(l) {
    const o = d(), n = new be({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? w;
          return c.nodes = [...c.nodes, s], T({
            createPortal: I,
            node: w
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((_) => _.svelteInstance !== o), T({
              createPortal: I,
              node: w
            });
          }), s;
        },
        ...l.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const ve = we(({
  name: r,
  Iconfont: t,
  ...l
}) => {
  const o = M[r];
  return /* @__PURE__ */ b.jsx(b.Fragment, {
    children: o ? C.createElement(o, l) : t ? /* @__PURE__ */ b.jsx(t, {
      type: r,
      ...l
    }) : null
  });
});
export {
  ve as Icon,
  ve as default
};
