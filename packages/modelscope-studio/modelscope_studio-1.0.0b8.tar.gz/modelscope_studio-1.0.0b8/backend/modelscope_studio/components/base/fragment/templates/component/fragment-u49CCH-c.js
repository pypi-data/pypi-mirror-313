import { g as J, w as d } from "./Index-BfH6nmOu.js";
const G = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal;
var C = {
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
var M = G, V = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), H = Object.prototype.hasOwnProperty, Q = M.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, X = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(l, t, r) {
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
g.Fragment = Y;
g.jsx = j;
g.jsxs = j;
C.exports = g;
var I = C.exports;
const {
  SvelteComponent: Z,
  assign: k,
  binding_callbacks: E,
  check_outros: $,
  children: D,
  claim_element: L,
  claim_space: ee,
  component_subscribe: R,
  compute_slots: te,
  create_slot: se,
  detach: c,
  element: A,
  empty: S,
  exclude_internal_props: x,
  get_all_dirty_from_scope: oe,
  get_slot_changes: ne,
  group_outros: re,
  init: le,
  insert_hydration: p,
  safe_not_equal: ae,
  set_custom_element_data: F,
  space: ie,
  transition_in: m,
  transition_out: h,
  update_slot_base: ce
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: ue,
  onDestroy: fe,
  setContext: de
} = window.__gradio__svelte__internal;
function O(l) {
  let t, r;
  const n = (
    /*#slots*/
    l[7].default
  ), o = se(
    n,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = A("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = L(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = D(t);
      o && o.l(s), s.forEach(c), this.h();
    },
    h() {
      F(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), o && o.m(t, null), l[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ce(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        r ? ne(
          n,
          /*$$scope*/
          e[6],
          s,
          null
        ) : oe(
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
      h(o, e), r = !1;
    },
    d(e) {
      e && c(t), o && o.d(e), l[9](null);
    }
  };
}
function pe(l) {
  let t, r, n, o, e = (
    /*$$slots*/
    l[4].default && O(l)
  );
  return {
    c() {
      t = A("react-portal-target"), r = ie(), e && e.c(), n = S(), this.h();
    },
    l(s) {
      t = L(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(t).forEach(c), r = ee(s), e && e.l(s), n = S(), this.h();
    },
    h() {
      F(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      p(s, t, i), l[8](t), p(s, r, i), e && e.m(s, i), p(s, n, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = O(s), e.c(), m(e, 1), e.m(n.parentNode, n)) : e && (re(), h(e, 1, 1, () => {
        e = null;
      }), $());
    },
    i(s) {
      o || (m(e), o = !0);
    },
    o(s) {
      h(e), o = !1;
    },
    d(s) {
      s && (c(t), c(r), c(n)), l[8](null), e && e.d(s);
    }
  };
}
function P(l) {
  const {
    svelteInit: t,
    ...r
  } = l;
  return r;
}
function me(l, t, r) {
  let n, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = te(e);
  let {
    svelteInit: _
  } = t;
  const w = d(P(t)), u = d();
  R(l, u, (a) => r(0, n = a));
  const f = d();
  R(l, f, (a) => r(1, o = a));
  const v = [], N = ue("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = J() || {}, W = _({
    parent: N,
    props: w,
    target: u,
    slot: f,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(a) {
      v.push(a);
    }
  });
  de("$$ms-gr-react-wrapper", W), _e(() => {
    w.set(P(t));
  }), fe(() => {
    v.forEach((a) => a());
  });
  function z(a) {
    E[a ? "unshift" : "push"](() => {
      n = a, u.set(n);
    });
  }
  function B(a) {
    E[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  return l.$$set = (a) => {
    r(17, t = k(k({}, t), x(a))), "svelteInit" in a && r(5, _ = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = x(t), [n, o, u, f, i, _, s, e, z, B];
}
class ge extends Z {
  constructor(t) {
    super(), le(this, t, me, pe, ae, {
      svelteInit: 5
    });
  }
}
const T = window.ms_globals.rerender, b = window.ms_globals.tree;
function be(l) {
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
          }, i = e.parent ?? b;
          return i.nodes = [...i.nodes, s], T({
            createPortal: y,
            node: b
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((_) => _.svelteInstance !== n), T({
              createPortal: y,
              node: b
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
const we = be(({
  children: l
}) => /* @__PURE__ */ I.jsx(I.Fragment, {
  children: l
}));
export {
  we as Fragment,
  we as default
};
