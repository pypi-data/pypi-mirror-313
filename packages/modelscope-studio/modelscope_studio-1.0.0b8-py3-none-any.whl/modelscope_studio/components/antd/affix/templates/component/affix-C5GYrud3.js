import { g as G, w as d } from "./Index-BJCq3ORo.js";
const z = window.ms_globals.React, B = window.ms_globals.React.useMemo, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Affix;
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
var V = z, Y = Symbol.for("react.element"), H = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function T(n, t, s) {
  var l, r = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (l in t) Q.call(t, l) && !Z.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: Y,
    type: n,
    key: e,
    ref: o,
    props: r,
    _owner: X.current
  };
}
g.Fragment = H;
g.jsx = T;
g.jsxs = T;
C.exports = g;
var $ = C.exports;
const {
  SvelteComponent: ee,
  assign: I,
  binding_callbacks: R,
  check_outros: te,
  children: A,
  claim_element: F,
  claim_space: se,
  component_subscribe: x,
  compute_slots: ne,
  create_slot: oe,
  detach: a,
  element: j,
  empty: k,
  exclude_internal_props: S,
  get_all_dirty_from_scope: re,
  get_slot_changes: le,
  group_outros: ie,
  init: ce,
  insert_hydration: m,
  safe_not_equal: ae,
  set_custom_element_data: D,
  space: ue,
  transition_in: p,
  transition_out: b,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: de,
  onDestroy: me,
  setContext: pe
} = window.__gradio__svelte__internal;
function E(n) {
  let t, s;
  const l = (
    /*#slots*/
    n[7].default
  ), r = oe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = j("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = F(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = A(t);
      r && r.l(o), o.forEach(a), this.h();
    },
    h() {
      D(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      m(e, t, o), r && r.m(t, null), n[9](t), s = !0;
    },
    p(e, o) {
      r && r.p && (!s || o & /*$$scope*/
      64) && fe(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        s ? le(
          l,
          /*$$scope*/
          e[6],
          o,
          null
        ) : re(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (p(r, e), s = !0);
    },
    o(e) {
      b(r, e), s = !1;
    },
    d(e) {
      e && a(t), r && r.d(e), n[9](null);
    }
  };
}
function ge(n) {
  let t, s, l, r, e = (
    /*$$slots*/
    n[4].default && E(n)
  );
  return {
    c() {
      t = j("react-portal-target"), s = ue(), e && e.c(), l = k(), this.h();
    },
    l(o) {
      t = F(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), A(t).forEach(a), s = se(o), e && e.l(o), l = k(), this.h();
    },
    h() {
      D(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      m(o, t, c), n[8](t), m(o, s, c), e && e.m(o, c), m(o, l, c), r = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && p(e, 1)) : (e = E(o), e.c(), p(e, 1), e.m(l.parentNode, l)) : e && (ie(), b(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(o) {
      r || (p(e), r = !0);
    },
    o(o) {
      b(e), r = !1;
    },
    d(o) {
      o && (a(t), a(s), a(l)), n[8](null), e && e.d(o);
    }
  };
}
function O(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function we(n, t, s) {
  let l, r, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = ne(e);
  let {
    svelteInit: u
  } = t;
  const h = d(O(t)), f = d();
  x(n, f, (i) => s(0, l = i));
  const _ = d();
  x(n, _, (i) => s(1, r = i));
  const v = [], L = de("$$ms-gr-react-wrapper"), {
    slotKey: N,
    slotIndex: W,
    subSlotIndex: q
  } = G() || {}, K = u({
    parent: L,
    props: h,
    target: f,
    slot: _,
    slotKey: N,
    slotIndex: W,
    subSlotIndex: q,
    onDestroy(i) {
      v.push(i);
    }
  });
  pe("$$ms-gr-react-wrapper", K), _e(() => {
    h.set(O(t));
  }), me(() => {
    v.forEach((i) => i());
  });
  function M(i) {
    R[i ? "unshift" : "push"](() => {
      l = i, f.set(l);
    });
  }
  function U(i) {
    R[i ? "unshift" : "push"](() => {
      r = i, _.set(r);
    });
  }
  return n.$$set = (i) => {
    s(17, t = I(I({}, t), S(i))), "svelteInit" in i && s(5, u = i.svelteInit), "$$scope" in i && s(6, o = i.$$scope);
  }, t = S(t), [l, r, f, _, c, u, o, e, M, U];
}
class be extends ee {
  constructor(t) {
    super(), ce(this, t, we, ge, ae, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function he(n) {
  function t(s) {
    const l = d(), r = new be({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
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
          }, c = e.parent ?? w;
          return c.nodes = [...c.nodes, o], P({
            createPortal: y,
            node: w
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== l), P({
              createPortal: y,
              node: w
            });
          }), o;
        },
        ...s.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
function ve(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function ye(n, t = !1) {
  try {
    if (t && !ve(n))
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
function Ie(n, t) {
  return B(() => ye(n, t), [n, t]);
}
const xe = he(({
  target: n,
  ...t
}) => {
  const s = Ie(n);
  return /* @__PURE__ */ $.jsx(J, {
    ...t,
    target: s
  });
});
export {
  xe as Affix,
  xe as default
};
