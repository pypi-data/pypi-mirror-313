import { g as G, w as d } from "./Index-BPNAK77I.js";
const B = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Flex;
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
function C(r, t, l) {
  var n, o = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) H.call(t, n) && !X.hasOwnProperty(n) && (o[n] = t[n]);
  if (r && r.defaultProps) for (n in t = r.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: V,
    type: r,
    key: e,
    ref: s,
    props: o,
    _owner: Q.current
  };
}
b.Fragment = Y;
b.jsx = C;
b.jsxs = C;
T.exports = b;
var Z = T.exports;
const {
  SvelteComponent: $,
  assign: I,
  binding_callbacks: k,
  check_outros: ee,
  children: j,
  claim_element: D,
  claim_space: te,
  component_subscribe: x,
  compute_slots: se,
  create_slot: oe,
  detach: c,
  element: L,
  empty: E,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ne,
  get_slot_changes: le,
  group_outros: re,
  init: ae,
  insert_hydration: p,
  safe_not_equal: ie,
  set_custom_element_data: F,
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
function S(r) {
  let t, l;
  const n = (
    /*#slots*/
    r[7].default
  ), o = oe(
    n,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = L("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = j(t);
      o && o.l(s), s.forEach(c), this.h();
    },
    h() {
      F(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), o && o.m(t, null), r[9](t), l = !0;
    },
    p(e, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && _e(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        l ? le(
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
      l || (m(o, e), l = !0);
    },
    o(e) {
      w(o, e), l = !1;
    },
    d(e) {
      e && c(t), o && o.d(e), r[9](null);
    }
  };
}
function me(r) {
  let t, l, n, o, e = (
    /*$$slots*/
    r[4].default && S(r)
  );
  return {
    c() {
      t = L("react-portal-target"), l = ce(), e && e.c(), n = E(), this.h();
    },
    l(s) {
      t = D(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(t).forEach(c), l = te(s), e && e.l(s), n = E(), this.h();
    },
    h() {
      F(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      p(s, t, i), r[8](t), p(s, l, i), e && e.m(s, i), p(s, n, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = S(s), e.c(), m(e, 1), e.m(n.parentNode, n)) : e && (re(), w(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(s) {
      o || (m(e), o = !0);
    },
    o(s) {
      w(e), o = !1;
    },
    d(s) {
      s && (c(t), c(l), c(n)), r[8](null), e && e.d(s);
    }
  };
}
function O(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function be(r, t, l) {
  let n, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = se(e);
  let {
    svelteInit: _
  } = t;
  const h = d(O(t)), u = d();
  x(r, u, (a) => l(0, n = a));
  const f = d();
  x(r, f, (a) => l(1, o = a));
  const v = [], A = fe("$$ms-gr-react-wrapper"), {
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K
  } = G() || {}, U = _({
    parent: A,
    props: h,
    target: u,
    slot: f,
    slotKey: N,
    slotIndex: q,
    subSlotIndex: K,
    onDestroy(a) {
      v.push(a);
    }
  });
  pe("$$ms-gr-react-wrapper", U), ue(() => {
    h.set(O(t));
  }), de(() => {
    v.forEach((a) => a());
  });
  function W(a) {
    k[a ? "unshift" : "push"](() => {
      n = a, u.set(n);
    });
  }
  function z(a) {
    k[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  return r.$$set = (a) => {
    l(17, t = I(I({}, t), R(a))), "svelteInit" in a && l(5, _ = a.svelteInit), "$$scope" in a && l(6, s = a.$$scope);
  }, t = R(t), [n, o, u, f, i, _, s, e, W, z];
}
class ge extends $ {
  constructor(t) {
    super(), ae(this, t, be, me, ie, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, g = window.ms_globals.tree;
function we(r) {
  function t(l) {
    const n = d(), o = new ge({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? g;
          return i.nodes = [...i.nodes, s], P({
            createPortal: y,
            node: g
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((_) => _.svelteInstance !== n), P({
              createPortal: y,
              node: g
            });
          }), s;
        },
        ...l.props
      }
    });
    return n.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const ve = we(({
  children: r,
  ...t
}) => /* @__PURE__ */ Z.jsx(J, {
  ...t,
  children: r
}));
export {
  ve as Flex,
  ve as default
};
