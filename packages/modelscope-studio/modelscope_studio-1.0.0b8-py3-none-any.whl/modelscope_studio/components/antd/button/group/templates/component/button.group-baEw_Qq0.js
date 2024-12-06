import { g as z, w as d } from "./Index-vTvwdVDM.js";
const F = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.theme, M = window.ms_globals.antd.Button;
var T = {
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
var V = F, Y = Symbol.for("react.element"), H = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(r, t, n) {
  var l, o = {}, e = null, s = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) Q.call(t, l) && !Z.hasOwnProperty(l) && (o[l] = t[l]);
  if (r && r.defaultProps) for (l in t = r.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: Y,
    type: r,
    key: e,
    ref: s,
    props: o,
    _owner: X.current
  };
}
g.Fragment = H;
g.jsx = C;
g.jsxs = C;
T.exports = g;
var $ = T.exports;
const {
  SvelteComponent: ee,
  assign: k,
  binding_callbacks: I,
  check_outros: te,
  children: j,
  claim_element: D,
  claim_space: se,
  component_subscribe: E,
  compute_slots: oe,
  create_slot: ne,
  detach: c,
  element: L,
  empty: R,
  exclude_internal_props: x,
  get_all_dirty_from_scope: le,
  get_slot_changes: re,
  group_outros: ae,
  init: ie,
  insert_hydration: p,
  safe_not_equal: ce,
  set_custom_element_data: A,
  space: _e,
  transition_in: m,
  transition_out: b,
  update_slot_base: ue
} = window.__gradio__svelte__internal, {
  beforeUpdate: fe,
  getContext: de,
  onDestroy: pe,
  setContext: me
} = window.__gradio__svelte__internal;
function S(r) {
  let t, n;
  const l = (
    /*#slots*/
    r[7].default
  ), o = ne(
    l,
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
      A(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), o && o.m(t, null), r[9](t), n = !0;
    },
    p(e, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && ue(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        n ? re(
          l,
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
      n || (m(o, e), n = !0);
    },
    o(e) {
      b(o, e), n = !1;
    },
    d(e) {
      e && c(t), o && o.d(e), r[9](null);
    }
  };
}
function ge(r) {
  let t, n, l, o, e = (
    /*$$slots*/
    r[4].default && S(r)
  );
  return {
    c() {
      t = L("react-portal-target"), n = _e(), e && e.c(), l = R(), this.h();
    },
    l(s) {
      t = D(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(t).forEach(c), n = se(s), e && e.l(s), l = R(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      p(s, t, i), r[8](t), p(s, n, i), e && e.m(s, i), p(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && m(e, 1)) : (e = S(s), e.c(), m(e, 1), e.m(l.parentNode, l)) : e && (ae(), b(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(s) {
      o || (m(e), o = !0);
    },
    o(s) {
      b(e), o = !1;
    },
    d(s) {
      s && (c(t), c(n), c(l)), r[8](null), e && e.d(s);
    }
  };
}
function O(r) {
  const {
    svelteInit: t,
    ...n
  } = r;
  return n;
}
function we(r, t, n) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = oe(e);
  let {
    svelteInit: _
  } = t;
  const h = d(O(t)), u = d();
  E(r, u, (a) => n(0, l = a));
  const f = d();
  E(r, f, (a) => n(1, o = a));
  const v = [], B = de("$$ms-gr-react-wrapper"), {
    slotKey: N,
    slotIndex: q,
    subSlotIndex: G
  } = z() || {}, K = _({
    parent: B,
    props: h,
    target: u,
    slot: f,
    slotKey: N,
    slotIndex: q,
    subSlotIndex: G,
    onDestroy(a) {
      v.push(a);
    }
  });
  me("$$ms-gr-react-wrapper", K), fe(() => {
    h.set(O(t));
  }), pe(() => {
    v.forEach((a) => a());
  });
  function U(a) {
    I[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  function W(a) {
    I[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  return r.$$set = (a) => {
    n(17, t = k(k({}, t), x(a))), "svelteInit" in a && n(5, _ = a.svelteInit), "$$scope" in a && n(6, s = a.$$scope);
  }, t = x(t), [l, o, u, f, i, _, s, e, U, W];
}
class be extends ee {
  constructor(t) {
    super(), ie(this, t, we, ge, ce, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function he(r) {
  function t(n) {
    const l = d(), o = new be({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? w;
          return i.nodes = [...i.nodes, s], P({
            createPortal: y,
            node: w
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((_) => _.svelteInstance !== l), P({
              createPortal: y,
              node: w
            });
          }), s;
        },
        ...n.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const ye = he(({
  style: r,
  ...t
}) => {
  const {
    token: n
  } = J.useToken();
  return /* @__PURE__ */ $.jsx(M.Group, {
    ...t,
    style: {
      ...r,
      "--ms-gr-antd-line-width": n.lineWidth + "px"
    }
  });
});
export {
  ye as ButtonGroup,
  ye as default
};
