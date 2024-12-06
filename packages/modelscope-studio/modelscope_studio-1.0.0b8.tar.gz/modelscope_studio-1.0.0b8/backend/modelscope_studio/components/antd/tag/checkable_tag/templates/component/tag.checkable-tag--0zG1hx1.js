import { g as G, w as d } from "./Index-CLJ9Kj5R.js";
const B = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Tag;
var P = {
  exports: {}
}, b = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var M = B, V = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), H = Object.prototype.hasOwnProperty, Q = M.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, X = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(r, t, l) {
  var o, n = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) H.call(t, o) && !X.hasOwnProperty(o) && (n[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) n[o] === void 0 && (n[o] = t[o]);
  return {
    $$typeof: V,
    type: r,
    key: e,
    ref: s,
    props: n,
    _owner: Q.current
  };
}
b.Fragment = Y;
b.jsx = C;
b.jsxs = C;
P.exports = b;
var Z = P.exports;
const {
  SvelteComponent: $,
  assign: k,
  binding_callbacks: I,
  check_outros: ee,
  children: j,
  claim_element: D,
  claim_space: te,
  component_subscribe: E,
  compute_slots: se,
  create_slot: oe,
  detach: c,
  element: L,
  empty: R,
  exclude_internal_props: S,
  get_all_dirty_from_scope: ne,
  get_slot_changes: le,
  group_outros: re,
  init: ae,
  insert_hydration: p,
  safe_not_equal: ie,
  set_custom_element_data: A,
  space: ce,
  transition_in: m,
  transition_out: w,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: ue,
  getContext: fe,
  onDestroy: de,
  setContext: pe
} = window.__gradio__svelte__internal;
function T(r) {
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
      t = L("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = j(t);
      n && n.l(s), s.forEach(c), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
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
      w(n, e), l = !1;
    },
    d(e) {
      e && c(t), n && n.d(e), r[9](null);
    }
  };
}
function me(r) {
  let t, l, o, n, e = (
    /*$$slots*/
    r[4].default && T(r)
  );
  return {
    c() {
      t = L("react-portal-target"), l = ce(), e && e.c(), o = R(), this.h();
    },
    l(s) {
      t = D(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(t).forEach(c), l = te(s), e && e.l(s), o = R(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      p(s, t, i), r[8](t), p(s, l, i), e && e.m(s, i), p(s, o, i), n = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = T(s), e.c(), m(e, 1), e.m(o.parentNode, o)) : e && (re(), w(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(s) {
      n || (m(e), n = !0);
    },
    o(s) {
      w(e), n = !1;
    },
    d(s) {
      s && (c(t), c(l), c(o)), r[8](null), e && e.d(s);
    }
  };
}
function x(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function be(r, t, l) {
  let o, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = se(e);
  let {
    svelteInit: _
  } = t;
  const h = d(x(t)), u = d();
  E(r, u, (a) => l(0, o = a));
  const f = d();
  E(r, f, (a) => l(1, n = a));
  const v = [], N = fe("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = G() || {}, F = _({
    parent: N,
    props: h,
    target: u,
    slot: f,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(a) {
      v.push(a);
    }
  });
  pe("$$ms-gr-react-wrapper", F), ue(() => {
    h.set(x(t));
  }), de(() => {
    v.forEach((a) => a());
  });
  function W(a) {
    I[a ? "unshift" : "push"](() => {
      o = a, u.set(o);
    });
  }
  function z(a) {
    I[a ? "unshift" : "push"](() => {
      n = a, f.set(n);
    });
  }
  return r.$$set = (a) => {
    l(17, t = k(k({}, t), S(a))), "svelteInit" in a && l(5, _ = a.svelteInit), "$$scope" in a && l(6, s = a.$$scope);
  }, t = S(t), [o, n, u, f, i, _, s, e, W, z];
}
class ge extends $ {
  constructor(t) {
    super(), ae(this, t, be, me, ie, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, g = window.ms_globals.tree;
function we(r) {
  function t(l) {
    const o = d(), n = new ge({
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
          }, i = e.parent ?? g;
          return i.nodes = [...i.nodes, s], O({
            createPortal: y,
            node: g
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((_) => _.svelteInstance !== o), O({
              createPortal: y,
              node: g
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
  onChange: r,
  onValueChange: t,
  ...l
}) => /* @__PURE__ */ Z.jsx(J.CheckableTag, {
  ...l,
  onChange: (o) => {
    r == null || r(o), t(o);
  }
}));
export {
  ve as CheckableTag,
  ve as default
};
