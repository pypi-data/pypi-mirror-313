import { g as G, w as d } from "./Index-DmMtsTAV.js";
const B = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Divider;
var D = {
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
function T(l, t, r) {
  var n, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) H.call(t, n) && !X.hasOwnProperty(n) && (o[n] = t[n]);
  if (l && l.defaultProps) for (n in t = l.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: V,
    type: l,
    key: e,
    ref: s,
    props: o,
    _owner: Q.current
  };
}
b.Fragment = Y;
b.jsx = T;
b.jsxs = T;
D.exports = b;
var Z = D.exports;
const {
  SvelteComponent: $,
  assign: I,
  binding_callbacks: k,
  check_outros: ee,
  children: C,
  claim_element: j,
  claim_space: te,
  component_subscribe: E,
  compute_slots: se,
  create_slot: oe,
  detach: c,
  element: L,
  empty: R,
  exclude_internal_props: S,
  get_all_dirty_from_scope: ne,
  get_slot_changes: re,
  group_outros: le,
  init: ie,
  insert_hydration: p,
  safe_not_equal: ae,
  set_custom_element_data: A,
  space: ce,
  transition_in: m,
  transition_out: v,
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
  ), o = oe(
    n,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = L("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = j(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = C(t);
      o && o.l(s), s.forEach(c), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), o && o.m(t, null), l[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && _e(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        r ? re(
          n,
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
      r || (m(o, e), r = !0);
    },
    o(e) {
      v(o, e), r = !1;
    },
    d(e) {
      e && c(t), o && o.d(e), l[9](null);
    }
  };
}
function me(l) {
  let t, r, n, o, e = (
    /*$$slots*/
    l[4].default && x(l)
  );
  return {
    c() {
      t = L("react-portal-target"), r = ce(), e && e.c(), n = R(), this.h();
    },
    l(s) {
      t = j(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), C(t).forEach(c), r = te(s), e && e.l(s), n = R(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      p(s, t, a), l[8](t), p(s, r, a), e && e.m(s, a), p(s, n, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && m(e, 1)) : (e = x(s), e.c(), m(e, 1), e.m(n.parentNode, n)) : e && (le(), v(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(s) {
      o || (m(e), o = !0);
    },
    o(s) {
      v(e), o = !1;
    },
    d(s) {
      s && (c(t), c(r), c(n)), l[8](null), e && e.d(s);
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
  let n, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const a = se(e);
  let {
    svelteInit: _
  } = t;
  const w = d(O(t)), u = d();
  E(l, u, (i) => r(0, n = i));
  const f = d();
  E(l, f, (i) => r(1, o = i));
  const h = [], N = fe("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = G() || {}, F = _({
    parent: N,
    props: w,
    target: u,
    slot: f,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(i) {
      h.push(i);
    }
  });
  pe("$$ms-gr-react-wrapper", F), ue(() => {
    w.set(O(t));
  }), de(() => {
    h.forEach((i) => i());
  });
  function W(i) {
    k[i ? "unshift" : "push"](() => {
      n = i, u.set(n);
    });
  }
  function z(i) {
    k[i ? "unshift" : "push"](() => {
      o = i, f.set(o);
    });
  }
  return l.$$set = (i) => {
    r(17, t = I(I({}, t), S(i))), "svelteInit" in i && r(5, _ = i.svelteInit), "$$scope" in i && r(6, s = i.$$scope);
  }, t = S(t), [n, o, u, f, a, _, s, e, W, z];
}
class ge extends $ {
  constructor(t) {
    super(), ie(this, t, be, me, ae, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, g = window.ms_globals.tree;
function ve(l) {
  function t(r) {
    const n = d(), o = new ge({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, a = e.parent ?? g;
          return a.nodes = [...a.nodes, s], P({
            createPortal: y,
            node: g
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((_) => _.svelteInstance !== n), P({
              createPortal: y,
              node: g
            });
          }), s;
        },
        ...r.props
      }
    });
    return n.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const he = ve(({
  ...l
}) => /* @__PURE__ */ Z.jsx(J, {
  ...l
}));
export {
  he as Divider,
  he as default
};
