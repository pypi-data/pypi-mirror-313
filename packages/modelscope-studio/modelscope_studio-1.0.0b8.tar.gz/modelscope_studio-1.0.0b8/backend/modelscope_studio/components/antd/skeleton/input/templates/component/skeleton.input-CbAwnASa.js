import { g as N, w as d } from "./Index-DFmlQv0_.js";
const I = window.ms_globals.ReactDOM.createPortal, U = window.ms_globals.antd.Skeleton, {
  SvelteComponent: V,
  assign: v,
  binding_callbacks: k,
  check_outros: W,
  children: R,
  claim_element: D,
  claim_space: j,
  component_subscribe: y,
  compute_slots: B,
  create_slot: F,
  detach: i,
  element: A,
  empty: S,
  exclude_internal_props: E,
  get_all_dirty_from_scope: H,
  get_slot_changes: J,
  group_outros: Q,
  init: X,
  insert_hydration: m,
  safe_not_equal: Y,
  set_custom_element_data: K,
  space: Z,
  transition_in: p,
  transition_out: b,
  update_slot_base: $
} = window.__gradio__svelte__internal, {
  beforeUpdate: ee,
  getContext: te,
  onDestroy: se,
  setContext: ne
} = window.__gradio__svelte__internal;
function C(l) {
  let s, o;
  const r = (
    /*#slots*/
    l[7].default
  ), n = F(
    r,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      s = A("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      s = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var t = R(s);
      n && n.l(t), t.forEach(i), this.h();
    },
    h() {
      K(s, "class", "svelte-1rt0kpf");
    },
    m(e, t) {
      m(e, s, t), n && n.m(s, null), l[9](s), o = !0;
    },
    p(e, t) {
      n && n.p && (!o || t & /*$$scope*/
      64) && $(
        n,
        r,
        e,
        /*$$scope*/
        e[6],
        o ? J(
          r,
          /*$$scope*/
          e[6],
          t,
          null
        ) : H(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (p(n, e), o = !0);
    },
    o(e) {
      b(n, e), o = !1;
    },
    d(e) {
      e && i(s), n && n.d(e), l[9](null);
    }
  };
}
function oe(l) {
  let s, o, r, n, e = (
    /*$$slots*/
    l[4].default && C(l)
  );
  return {
    c() {
      s = A("react-portal-target"), o = Z(), e && e.c(), r = S(), this.h();
    },
    l(t) {
      s = D(t, "REACT-PORTAL-TARGET", {
        class: !0
      }), R(s).forEach(i), o = j(t), e && e.l(t), r = S(), this.h();
    },
    h() {
      K(s, "class", "svelte-1rt0kpf");
    },
    m(t, c) {
      m(t, s, c), l[8](s), m(t, o, c), e && e.m(t, c), m(t, r, c), n = !0;
    },
    p(t, [c]) {
      /*$$slots*/
      t[4].default ? e ? (e.p(t, c), c & /*$$slots*/
      16 && p(e, 1)) : (e = C(t), e.c(), p(e, 1), e.m(r.parentNode, r)) : e && (Q(), b(e, 1, 1, () => {
        e = null;
      }), W());
    },
    i(t) {
      n || (p(e), n = !0);
    },
    o(t) {
      b(e), n = !1;
    },
    d(t) {
      t && (i(s), i(o), i(r)), l[8](null), e && e.d(t);
    }
  };
}
function P(l) {
  const {
    svelteInit: s,
    ...o
  } = l;
  return o;
}
function le(l, s, o) {
  let r, n, {
    $$slots: e = {},
    $$scope: t
  } = s;
  const c = B(e);
  let {
    svelteInit: u
  } = s;
  const h = d(P(s)), _ = d();
  y(l, _, (a) => o(0, r = a));
  const f = d();
  y(l, f, (a) => o(1, n = a));
  const w = [], L = te("$$ms-gr-react-wrapper"), {
    slotKey: O,
    slotIndex: x,
    subSlotIndex: q
  } = N() || {}, z = u({
    parent: L,
    props: h,
    target: _,
    slot: f,
    slotKey: O,
    slotIndex: x,
    subSlotIndex: q,
    onDestroy(a) {
      w.push(a);
    }
  });
  ne("$$ms-gr-react-wrapper", z), ee(() => {
    h.set(P(s));
  }), se(() => {
    w.forEach((a) => a());
  });
  function G(a) {
    k[a ? "unshift" : "push"](() => {
      r = a, _.set(r);
    });
  }
  function M(a) {
    k[a ? "unshift" : "push"](() => {
      n = a, f.set(n);
    });
  }
  return l.$$set = (a) => {
    o(17, s = v(v({}, s), E(a))), "svelteInit" in a && o(5, u = a.svelteInit), "$$scope" in a && o(6, t = a.$$scope);
  }, s = E(s), [r, n, _, f, c, u, t, e, G, M];
}
class re extends V {
  constructor(s) {
    super(), X(this, s, le, oe, Y, {
      svelteInit: 5
    });
  }
}
const T = window.ms_globals.rerender, g = window.ms_globals.tree;
function ae(l) {
  function s(o) {
    const r = d(), n = new re({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const t = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? g;
          return c.nodes = [...c.nodes, t], T({
            createPortal: I,
            node: g
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== r), T({
              createPortal: I,
              node: g
            });
          }), t;
        },
        ...o.props
      }
    });
    return r.set(n), n;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(s);
    });
  });
}
const ie = ae(U.Input);
export {
  ie as SkeletonInput,
  ie as default
};
