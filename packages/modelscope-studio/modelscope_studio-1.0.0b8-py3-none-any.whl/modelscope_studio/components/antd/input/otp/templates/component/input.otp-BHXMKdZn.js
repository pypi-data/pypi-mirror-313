import { b as Y, g as H, w as d } from "./Index-kraw3AN-.js";
const B = window.ms_globals.React, G = window.ms_globals.React.useMemo, J = window.ms_globals.React.useState, y = window.ms_globals.React.useRef, R = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Input;
function X(n, t) {
  return Y(n, t);
}
var j = {
  exports: {}
}, w = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Z = B, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, se = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(n, t, s) {
  var l, o = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (l in t) te.call(t, l) && !ne.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: r,
    props: o,
    _owner: se.current
  };
}
w.Fragment = ee;
w.jsx = C;
w.jsxs = C;
j.exports = w;
var oe = j.exports;
const {
  SvelteComponent: re,
  assign: E,
  binding_callbacks: S,
  check_outros: le,
  children: D,
  claim_element: L,
  claim_space: ue,
  component_subscribe: k,
  compute_slots: ie,
  create_slot: ce,
  detach: a,
  element: V,
  empty: x,
  exclude_internal_props: O,
  get_all_dirty_from_scope: ae,
  get_slot_changes: fe,
  group_outros: _e,
  init: de,
  insert_hydration: m,
  safe_not_equal: me,
  set_custom_element_data: q,
  space: pe,
  transition_in: p,
  transition_out: b,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: be,
  onDestroy: he,
  setContext: ve
} = window.__gradio__svelte__internal;
function P(n) {
  let t, s;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ce(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = V("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = L(e, "SVELTE-SLOT", {
        class: !0
      });
      var r = D(t);
      o && o.l(r), r.forEach(a), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      m(e, t, r), o && o.m(t, null), n[9](t), s = !0;
    },
    p(e, r) {
      o && o.p && (!s || r & /*$$scope*/
      64) && we(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        s ? fe(
          l,
          /*$$scope*/
          e[6],
          r,
          null
        ) : ae(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (p(o, e), s = !0);
    },
    o(e) {
      b(o, e), s = !1;
    },
    d(e) {
      e && a(t), o && o.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, s, l, o, e = (
    /*$$slots*/
    n[4].default && P(n)
  );
  return {
    c() {
      t = V("react-portal-target"), s = pe(), e && e.c(), l = x(), this.h();
    },
    l(r) {
      t = L(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(t).forEach(a), s = ue(r), e && e.l(r), l = x(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      m(r, t, i), n[8](t), m(r, s, i), e && e.m(r, i), m(r, l, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && p(e, 1)) : (e = P(r), e.c(), p(e, 1), e.m(l.parentNode, l)) : e && (_e(), b(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(r) {
      o || (p(e), o = !0);
    },
    o(r) {
      b(e), o = !1;
    },
    d(r) {
      r && (a(t), a(s), a(l)), n[8](null), e && e.d(r);
    }
  };
}
function T(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function Re(n, t, s) {
  let l, o, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = ie(e);
  let {
    svelteInit: c
  } = t;
  const h = d(T(t)), f = d();
  k(n, f, (u) => s(0, l = u));
  const _ = d();
  k(n, _, (u) => s(1, o = u));
  const v = [], A = be("$$ms-gr-react-wrapper"), {
    slotKey: M,
    slotIndex: N,
    subSlotIndex: W
  } = H() || {}, K = c({
    parent: A,
    props: h,
    target: f,
    slot: _,
    slotKey: M,
    slotIndex: N,
    subSlotIndex: W,
    onDestroy(u) {
      v.push(u);
    }
  });
  ve("$$ms-gr-react-wrapper", K), ge(() => {
    h.set(T(t));
  }), he(() => {
    v.forEach((u) => u());
  });
  function U(u) {
    S[u ? "unshift" : "push"](() => {
      l = u, f.set(l);
    });
  }
  function z(u) {
    S[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return n.$$set = (u) => {
    s(17, t = E(E({}, t), O(u))), "svelteInit" in u && s(5, c = u.svelteInit), "$$scope" in u && s(6, r = u.$$scope);
  }, t = O(t), [l, o, f, _, i, c, r, e, U, z];
}
class Ie extends re {
  constructor(t) {
    super(), de(this, t, Re, ye, me, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, g = window.ms_globals.tree;
function Ee(n) {
  function t(s) {
    const l = d(), o = new Ie({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? g;
          return i.nodes = [...i.nodes, r], F({
            createPortal: I,
            node: g
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== l), F({
              createPortal: I,
              node: g
            });
          }), r;
        },
        ...s.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
function Se(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function ke(n, t = !1) {
  try {
    if (t && !Se(n))
      return;
    if (typeof n == "string") {
      let s = n.trim();
      return s.startsWith(";") && (s = s.slice(1)), s.endsWith(";") && (s = s.slice(0, -1)), new Function(`return (...args) => (${s})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function xe(n, t) {
  return G(() => ke(n, t), [n, t]);
}
function Oe({
  value: n,
  onValueChange: t
}) {
  const [s, l] = J(n), o = y(t);
  o.current = t;
  const e = y(s);
  return e.current = s, R(() => {
    o.current(s);
  }, [s]), R(() => {
    X(n, e.current) || l(n);
  }, [n]), [s, l];
}
const Te = Ee(({
  formatter: n,
  onValueChange: t,
  onChange: s,
  elRef: l,
  ...o
}) => {
  const e = xe(n), [r, i] = Oe({
    onValueChange: t,
    value: o.value
  });
  return /* @__PURE__ */ oe.jsx(Q.OTP, {
    ...o,
    value: r,
    ref: l,
    formatter: e,
    onChange: (c) => {
      s == null || s(c), i(c);
    }
  });
});
export {
  Te as InputOTP,
  Te as default
};
