import { g as G, w as d } from "./Index-BRQcZD6v.js";
const B = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Radio;
var T = {
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
function j(l, t, r) {
  var n, s = {}, e = null, o = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (n in t) H.call(t, n) && !X.hasOwnProperty(n) && (s[n] = t[n]);
  if (l && l.defaultProps) for (n in t = l.defaultProps, t) s[n] === void 0 && (s[n] = t[n]);
  return {
    $$typeof: V,
    type: l,
    key: e,
    ref: o,
    props: s,
    _owner: Q.current
  };
}
b.Fragment = Y;
b.jsx = j;
b.jsxs = j;
T.exports = b;
var Z = T.exports;
const {
  SvelteComponent: $,
  assign: I,
  binding_callbacks: R,
  check_outros: ee,
  children: D,
  claim_element: L,
  claim_space: te,
  component_subscribe: k,
  compute_slots: se,
  create_slot: oe,
  detach: c,
  element: C,
  empty: E,
  exclude_internal_props: S,
  get_all_dirty_from_scope: ne,
  get_slot_changes: re,
  group_outros: le,
  init: ae,
  insert_hydration: p,
  safe_not_equal: ie,
  set_custom_element_data: A,
  space: ce,
  transition_in: m,
  transition_out: g,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: ue,
  getContext: fe,
  onDestroy: de,
  setContext: pe
} = window.__gradio__svelte__internal;
function x(l) {
  let t, r;
  const n = (
    /*#slots*/
    l[7].default
  ), s = oe(
    n,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = C("svelte-slot"), s && s.c(), this.h();
    },
    l(e) {
      t = L(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = D(t);
      s && s.l(o), o.forEach(c), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      p(e, t, o), s && s.m(t, null), l[9](t), r = !0;
    },
    p(e, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && _e(
        s,
        n,
        e,
        /*$$scope*/
        e[6],
        r ? re(
          n,
          /*$$scope*/
          e[6],
          o,
          null
        ) : ne(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (m(s, e), r = !0);
    },
    o(e) {
      g(s, e), r = !1;
    },
    d(e) {
      e && c(t), s && s.d(e), l[9](null);
    }
  };
}
function me(l) {
  let t, r, n, s, e = (
    /*$$slots*/
    l[4].default && x(l)
  );
  return {
    c() {
      t = C("react-portal-target"), r = ce(), e && e.c(), n = E(), this.h();
    },
    l(o) {
      t = L(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(t).forEach(c), r = te(o), e && e.l(o), n = E(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      p(o, t, i), l[8](t), p(o, r, i), e && e.m(o, i), p(o, n, i), s = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = x(o), e.c(), m(e, 1), e.m(n.parentNode, n)) : e && (le(), g(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(o) {
      s || (m(e), s = !0);
    },
    o(o) {
      g(e), s = !1;
    },
    d(o) {
      o && (c(t), c(r), c(n)), l[8](null), e && e.d(o);
    }
  };
}
function O(l) {
  const {
    svelteInit: t,
    ...r
  } = l;
  return r;
}
function be(l, t, r) {
  let n, s, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = se(e);
  let {
    svelteInit: _
  } = t;
  const v = d(O(t)), u = d();
  k(l, u, (a) => r(0, n = a));
  const f = d();
  k(l, f, (a) => r(1, s = a));
  const h = [], N = fe("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = G() || {}, F = _({
    parent: N,
    props: v,
    target: u,
    slot: f,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(a) {
      h.push(a);
    }
  });
  pe("$$ms-gr-react-wrapper", F), ue(() => {
    v.set(O(t));
  }), de(() => {
    h.forEach((a) => a());
  });
  function W(a) {
    R[a ? "unshift" : "push"](() => {
      n = a, u.set(n);
    });
  }
  function z(a) {
    R[a ? "unshift" : "push"](() => {
      s = a, f.set(s);
    });
  }
  return l.$$set = (a) => {
    r(17, t = I(I({}, t), S(a))), "svelteInit" in a && r(5, _ = a.svelteInit), "$$scope" in a && r(6, o = a.$$scope);
  }, t = S(t), [n, s, u, f, i, _, o, e, W, z];
}
class we extends $ {
  constructor(t) {
    super(), ae(this, t, be, me, ie, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function ge(l) {
  function t(r) {
    const n = d(), s = new we({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? w;
          return i.nodes = [...i.nodes, o], P({
            createPortal: y,
            node: w
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((_) => _.svelteInstance !== n), P({
              createPortal: y,
              node: w
            });
          }), o;
        },
        ...r.props
      }
    });
    return n.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const he = ge(({
  onValueChange: l,
  onChange: t,
  elRef: r,
  ...n
}) => /* @__PURE__ */ Z.jsx(J, {
  ...n,
  ref: r,
  onChange: (s) => {
    t == null || t(s), l(s.target.checked);
  }
}));
export {
  he as Radio,
  he as default
};
