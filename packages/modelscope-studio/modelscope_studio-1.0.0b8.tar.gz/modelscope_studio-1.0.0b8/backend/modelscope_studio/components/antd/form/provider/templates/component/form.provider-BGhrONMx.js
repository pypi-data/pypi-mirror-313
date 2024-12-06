import { g as G, w as d } from "./Index-DltofxAr.js";
const B = window.ms_globals.React, h = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Form;
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
var M = B, Y = Symbol.for("react.element"), H = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = M.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(n, t, l) {
  var r, o = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) Q.call(t, r) && !Z.hasOwnProperty(r) && (o[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Y,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: X.current
  };
}
b.Fragment = H;
b.jsx = j;
b.jsxs = j;
T.exports = b;
var F = T.exports;
const {
  SvelteComponent: $,
  assign: k,
  binding_callbacks: I,
  check_outros: ee,
  children: D,
  claim_element: L,
  claim_space: te,
  component_subscribe: E,
  compute_slots: se,
  create_slot: oe,
  detach: i,
  element: C,
  empty: R,
  exclude_internal_props: O,
  get_all_dirty_from_scope: re,
  get_slot_changes: le,
  group_outros: ne,
  init: ae,
  insert_hydration: m,
  safe_not_equal: ce,
  set_custom_element_data: A,
  space: ie,
  transition_in: p,
  transition_out: w,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: ue,
  getContext: fe,
  onDestroy: de,
  setContext: me
} = window.__gradio__svelte__internal;
function S(n) {
  let t, l;
  const r = (
    /*#slots*/
    n[7].default
  ), o = oe(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = C("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = L(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = D(t);
      o && o.l(s), s.forEach(i), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      m(e, t, s), o && o.m(t, null), n[9](t), l = !0;
    },
    p(e, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && _e(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        l ? le(
          r,
          /*$$scope*/
          e[6],
          s,
          null
        ) : re(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      l || (p(o, e), l = !0);
    },
    o(e) {
      w(o, e), l = !1;
    },
    d(e) {
      e && i(t), o && o.d(e), n[9](null);
    }
  };
}
function pe(n) {
  let t, l, r, o, e = (
    /*$$slots*/
    n[4].default && S(n)
  );
  return {
    c() {
      t = C("react-portal-target"), l = ie(), e && e.c(), r = R(), this.h();
    },
    l(s) {
      t = L(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(t).forEach(i), l = te(s), e && e.l(s), r = R(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      m(s, t, c), n[8](t), m(s, l, c), e && e.m(s, c), m(s, r, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && p(e, 1)) : (e = S(s), e.c(), p(e, 1), e.m(r.parentNode, r)) : e && (ne(), w(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(s) {
      o || (p(e), o = !0);
    },
    o(s) {
      w(e), o = !1;
    },
    d(s) {
      s && (i(t), i(l), i(r)), n[8](null), e && e.d(s);
    }
  };
}
function x(n) {
  const {
    svelteInit: t,
    ...l
  } = n;
  return l;
}
function be(n, t, l) {
  let r, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = se(e);
  let {
    svelteInit: _
  } = t;
  const v = d(x(t)), u = d();
  E(n, u, (a) => l(0, r = a));
  const f = d();
  E(n, f, (a) => l(1, o = a));
  const y = [], N = fe("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = G() || {}, V = _({
    parent: N,
    props: v,
    target: u,
    slot: f,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(a) {
      y.push(a);
    }
  });
  me("$$ms-gr-react-wrapper", V), ue(() => {
    v.set(x(t));
  }), de(() => {
    y.forEach((a) => a());
  });
  function W(a) {
    I[a ? "unshift" : "push"](() => {
      r = a, u.set(r);
    });
  }
  function z(a) {
    I[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  return n.$$set = (a) => {
    l(17, t = k(k({}, t), O(a))), "svelteInit" in a && l(5, _ = a.svelteInit), "$$scope" in a && l(6, s = a.$$scope);
  }, t = O(t), [r, o, u, f, c, _, s, e, W, z];
}
class ge extends $ {
  constructor(t) {
    super(), ae(this, t, be, pe, ce, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, g = window.ms_globals.tree;
function we(n) {
  function t(l) {
    const r = d(), o = new ge({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? g;
          return c.nodes = [...c.nodes, s], P({
            createPortal: h,
            node: g
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((_) => _.svelteInstance !== r), P({
              createPortal: h,
              node: g
            });
          }), s;
        },
        ...l.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const ye = we(({
  onFormChange: n,
  onFormFinish: t,
  ...l
}) => /* @__PURE__ */ F.jsx(J.Provider, {
  ...l,
  onFormChange: (r, o) => {
    n == null || n(r, {
      ...o,
      forms: Object.keys(o.forms).reduce((e, s) => ({
        ...e,
        [s]: o.forms[s].getFieldsValue()
      }), {})
    });
  },
  onFormFinish: (r, o) => {
    t == null || t(r, {
      ...o,
      forms: Object.keys(o.forms).reduce((e, s) => ({
        ...e,
        [s]: o.forms[s].getFieldsValue()
      }), {})
    });
  }
}));
export {
  ye as FormProvider,
  ye as default
};
