import { g as G, w as d } from "./Index-9kukt-yO.js";
const z = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.theme, M = window.ms_globals.antd.Radio;
var T = {
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
var V = z, Y = Symbol.for("react.element"), H = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(r, t, l) {
  var n, o = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) Q.call(t, n) && !Z.hasOwnProperty(n) && (o[n] = t[n]);
  if (r && r.defaultProps) for (n in t = r.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: Y,
    type: r,
    key: e,
    ref: s,
    props: o,
    _owner: X.current
  };
}
w.Fragment = H;
w.jsx = j;
w.jsxs = j;
T.exports = w;
var $ = T.exports;
const {
  SvelteComponent: ee,
  assign: k,
  binding_callbacks: I,
  check_outros: te,
  children: D,
  claim_element: L,
  claim_space: se,
  component_subscribe: R,
  compute_slots: oe,
  create_slot: ne,
  detach: c,
  element: C,
  empty: E,
  exclude_internal_props: x,
  get_all_dirty_from_scope: le,
  get_slot_changes: re,
  group_outros: ie,
  init: ae,
  insert_hydration: m,
  safe_not_equal: ce,
  set_custom_element_data: A,
  space: _e,
  transition_in: p,
  transition_out: g,
  update_slot_base: ue
} = window.__gradio__svelte__internal, {
  beforeUpdate: fe,
  getContext: de,
  onDestroy: me,
  setContext: pe
} = window.__gradio__svelte__internal;
function S(r) {
  let t, l;
  const n = (
    /*#slots*/
    r[7].default
  ), o = ne(
    n,
    r,
    /*$$scope*/
    r[6],
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
      o && o.l(s), s.forEach(c), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      m(e, t, s), o && o.m(t, null), r[9](t), l = !0;
    },
    p(e, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && ue(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        l ? re(
          n,
          /*$$scope*/
          e[6],
          s,
          null
        ) : le(
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
      g(o, e), l = !1;
    },
    d(e) {
      e && c(t), o && o.d(e), r[9](null);
    }
  };
}
function we(r) {
  let t, l, n, o, e = (
    /*$$slots*/
    r[4].default && S(r)
  );
  return {
    c() {
      t = C("react-portal-target"), l = _e(), e && e.c(), n = E(), this.h();
    },
    l(s) {
      t = L(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(t).forEach(c), l = se(s), e && e.l(s), n = E(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      m(s, t, a), r[8](t), m(s, l, a), e && e.m(s, a), m(s, n, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, a), a & /*$$slots*/
      16 && p(e, 1)) : (e = S(s), e.c(), p(e, 1), e.m(n.parentNode, n)) : e && (ie(), g(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(s) {
      o || (p(e), o = !0);
    },
    o(s) {
      g(e), o = !1;
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
  const a = oe(e);
  let {
    svelteInit: _
  } = t;
  const h = d(O(t)), u = d();
  R(r, u, (i) => l(0, n = i));
  const f = d();
  R(r, f, (i) => l(1, o = i));
  const v = [], N = de("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = G() || {}, W = _({
    parent: N,
    props: h,
    target: u,
    slot: f,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(i) {
      v.push(i);
    }
  });
  pe("$$ms-gr-react-wrapper", W), fe(() => {
    h.set(O(t));
  }), me(() => {
    v.forEach((i) => i());
  });
  function B(i) {
    I[i ? "unshift" : "push"](() => {
      n = i, u.set(n);
    });
  }
  function F(i) {
    I[i ? "unshift" : "push"](() => {
      o = i, f.set(o);
    });
  }
  return r.$$set = (i) => {
    l(17, t = k(k({}, t), x(i))), "svelteInit" in i && l(5, _ = i.svelteInit), "$$scope" in i && l(6, s = i.$$scope);
  }, t = x(t), [n, o, u, f, a, _, s, e, B, F];
}
class ge extends ee {
  constructor(t) {
    super(), ae(this, t, be, we, ce, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, b = window.ms_globals.tree;
function he(r) {
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
          }, a = e.parent ?? b;
          return a.nodes = [...a.nodes, s], P({
            createPortal: y,
            node: b
          }), e.onDestroy(() => {
            a.nodes = a.nodes.filter((_) => _.svelteInstance !== n), P({
              createPortal: y,
              node: b
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
const ye = he(({
  onValueChange: r,
  onChange: t,
  elRef: l,
  style: n,
  ...o
}) => {
  const {
    token: e
  } = J.useToken();
  return /* @__PURE__ */ $.jsx(M.Button, {
    ...o,
    style: {
      ...n,
      "--ms-gr-antd-line-width": e.lineWidth + "px"
    },
    ref: l,
    onChange: (s) => {
      t == null || t(s), r(s.target.checked);
    }
  });
});
export {
  ye as Radio,
  ye as default
};
