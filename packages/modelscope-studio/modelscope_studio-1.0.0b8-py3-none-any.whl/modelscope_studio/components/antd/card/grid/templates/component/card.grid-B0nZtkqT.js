import { g as N, w as d } from "./Index-CNgZ7iv4.js";
const v = window.ms_globals.ReactDOM.createPortal, U = window.ms_globals.antd.Card, {
  SvelteComponent: V,
  assign: I,
  binding_callbacks: y,
  check_outros: W,
  children: R,
  claim_element: D,
  claim_space: j,
  component_subscribe: k,
  compute_slots: B,
  create_slot: F,
  detach: i,
  element: A,
  empty: C,
  exclude_internal_props: S,
  get_all_dirty_from_scope: H,
  get_slot_changes: J,
  group_outros: Q,
  init: X,
  insert_hydration: m,
  safe_not_equal: Y,
  set_custom_element_data: G,
  space: Z,
  transition_in: p,
  transition_out: b,
  update_slot_base: $
} = window.__gradio__svelte__internal, {
  beforeUpdate: ee,
  getContext: te,
  onDestroy: se,
  setContext: oe
} = window.__gradio__svelte__internal;
function E(l) {
  let s, n;
  const r = (
    /*#slots*/
    l[7].default
  ), o = F(
    r,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      s = A("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      s = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var t = R(s);
      o && o.l(t), t.forEach(i), this.h();
    },
    h() {
      G(s, "class", "svelte-1rt0kpf");
    },
    m(e, t) {
      m(e, s, t), o && o.m(s, null), l[9](s), n = !0;
    },
    p(e, t) {
      o && o.p && (!n || t & /*$$scope*/
      64) && $(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        n ? J(
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
      n || (p(o, e), n = !0);
    },
    o(e) {
      b(o, e), n = !1;
    },
    d(e) {
      e && i(s), o && o.d(e), l[9](null);
    }
  };
}
function ne(l) {
  let s, n, r, o, e = (
    /*$$slots*/
    l[4].default && E(l)
  );
  return {
    c() {
      s = A("react-portal-target"), n = Z(), e && e.c(), r = C(), this.h();
    },
    l(t) {
      s = D(t, "REACT-PORTAL-TARGET", {
        class: !0
      }), R(s).forEach(i), n = j(t), e && e.l(t), r = C(), this.h();
    },
    h() {
      G(s, "class", "svelte-1rt0kpf");
    },
    m(t, c) {
      m(t, s, c), l[8](s), m(t, n, c), e && e.m(t, c), m(t, r, c), o = !0;
    },
    p(t, [c]) {
      /*$$slots*/
      t[4].default ? e ? (e.p(t, c), c & /*$$slots*/
      16 && p(e, 1)) : (e = E(t), e.c(), p(e, 1), e.m(r.parentNode, r)) : e && (Q(), b(e, 1, 1, () => {
        e = null;
      }), W());
    },
    i(t) {
      o || (p(e), o = !0);
    },
    o(t) {
      b(e), o = !1;
    },
    d(t) {
      t && (i(s), i(n), i(r)), l[8](null), e && e.d(t);
    }
  };
}
function P(l) {
  const {
    svelteInit: s,
    ...n
  } = l;
  return n;
}
function le(l, s, n) {
  let r, o, {
    $$slots: e = {},
    $$scope: t
  } = s;
  const c = B(e);
  let {
    svelteInit: _
  } = s;
  const h = d(P(s)), u = d();
  k(l, u, (a) => n(0, r = a));
  const f = d();
  k(l, f, (a) => n(1, o = a));
  const w = [], K = te("$$ms-gr-react-wrapper"), {
    slotKey: L,
    slotIndex: O,
    subSlotIndex: x
  } = N() || {}, q = _({
    parent: K,
    props: h,
    target: u,
    slot: f,
    slotKey: L,
    slotIndex: O,
    subSlotIndex: x,
    onDestroy(a) {
      w.push(a);
    }
  });
  oe("$$ms-gr-react-wrapper", q), ee(() => {
    h.set(P(s));
  }), se(() => {
    w.forEach((a) => a());
  });
  function z(a) {
    y[a ? "unshift" : "push"](() => {
      r = a, u.set(r);
    });
  }
  function M(a) {
    y[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  return l.$$set = (a) => {
    n(17, s = I(I({}, s), S(a))), "svelteInit" in a && n(5, _ = a.svelteInit), "$$scope" in a && n(6, t = a.$$scope);
  }, s = S(s), [r, o, u, f, c, _, t, e, z, M];
}
class re extends V {
  constructor(s) {
    super(), X(this, s, le, ne, Y, {
      svelteInit: 5
    });
  }
}
const T = window.ms_globals.rerender, g = window.ms_globals.tree;
function ae(l) {
  function s(n) {
    const r = d(), o = new re({
      ...n,
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
            createPortal: v,
            node: g
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((_) => _.svelteInstance !== r), T({
              createPortal: v,
              node: g
            });
          }), t;
        },
        ...n.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(s);
    });
  });
}
const ie = ae(U.Grid);
export {
  ie as CardGrid,
  ie as default
};
