import { g as G, w as d } from "./Index-VQvu0mGh.js";
const B = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Checkbox;
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
function C(l, t, r) {
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
b.jsx = C;
b.jsxs = C;
T.exports = b;
var Z = T.exports;
const {
  SvelteComponent: $,
  assign: k,
  binding_callbacks: I,
  check_outros: ee,
  children: j,
  claim_element: D,
  claim_space: te,
  component_subscribe: x,
  compute_slots: se,
  create_slot: oe,
  detach: i,
  element: L,
  empty: E,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ne,
  get_slot_changes: re,
  group_outros: le,
  init: ce,
  insert_hydration: p,
  safe_not_equal: ae,
  set_custom_element_data: A,
  space: ie,
  transition_in: m,
  transition_out: g,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: ue,
  getContext: fe,
  onDestroy: de,
  setContext: pe
} = window.__gradio__svelte__internal;
function S(l) {
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
      t = L("svelte-slot"), s && s.c(), this.h();
    },
    l(e) {
      t = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = j(t);
      s && s.l(o), o.forEach(i), this.h();
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
      e && i(t), s && s.d(e), l[9](null);
    }
  };
}
function me(l) {
  let t, r, n, s, e = (
    /*$$slots*/
    l[4].default && S(l)
  );
  return {
    c() {
      t = L("react-portal-target"), r = ie(), e && e.c(), n = E(), this.h();
    },
    l(o) {
      t = D(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(t).forEach(i), r = te(o), e && e.l(o), n = E(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(o, a) {
      p(o, t, a), l[8](t), p(o, r, a), e && e.m(o, a), p(o, n, a), s = !0;
    },
    p(o, [a]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, a), a & /*$$slots*/
      16 && m(e, 1)) : (e = S(o), e.c(), m(e, 1), e.m(n.parentNode, n)) : e && (le(), g(e, 1, 1, () => {
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
      o && (i(t), i(r), i(n)), l[8](null), e && e.d(o);
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
  const a = se(e);
  let {
    svelteInit: _
  } = t;
  const h = d(O(t)), u = d();
  x(l, u, (c) => r(0, n = c));
  const f = d();
  x(l, f, (c) => r(1, s = c));
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
    onDestroy(c) {
      v.push(c);
    }
  });
  pe("$$ms-gr-react-wrapper", F), ue(() => {
    h.set(O(t));
  }), de(() => {
    v.forEach((c) => c());
  });
  function W(c) {
    I[c ? "unshift" : "push"](() => {
      n = c, u.set(n);
    });
  }
  function z(c) {
    I[c ? "unshift" : "push"](() => {
      s = c, f.set(s);
    });
  }
  return l.$$set = (c) => {
    r(17, t = k(k({}, t), R(c))), "svelteInit" in c && r(5, _ = c.svelteInit), "$$scope" in c && r(6, o = c.$$scope);
  }, t = R(t), [n, s, u, f, a, _, o, e, W, z];
}
class we extends $ {
  constructor(t) {
    super(), ce(this, t, be, me, ae, {
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
          }, a = e.parent ?? w;
          return a.nodes = [...a.nodes, o], P({
            createPortal: y,
            node: w
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((_) => _.svelteInstance !== n), P({
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
const ve = ge(({
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
  ve as Checkbox,
  ve as default
};
