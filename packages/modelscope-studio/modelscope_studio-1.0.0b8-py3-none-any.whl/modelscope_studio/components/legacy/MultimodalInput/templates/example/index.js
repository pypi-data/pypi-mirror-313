const {
  SvelteComponent: F,
  append_hydration: q,
  attr: f,
  children: b,
  claim_svg_element: E,
  detach: v,
  init: H,
  insert_hydration: W,
  noop: j,
  safe_not_equal: x,
  svg_element: S
} = window.__gradio__svelte__internal;
function G(r) {
  let e, l, i;
  return {
    c() {
      e = S("svg"), l = S("path"), i = S("polyline"), this.h();
    },
    l(c) {
      e = E(c, "svg", {
        xmlns: !0,
        width: !0,
        height: !0,
        viewBox: !0,
        fill: !0,
        stroke: !0,
        "stroke-width": !0,
        "stroke-linecap": !0,
        "stroke-linejoin": !0,
        class: !0
      });
      var o = b(e);
      l = E(o, "path", {
        d: !0
      }), b(l).forEach(v), i = E(o, "polyline", {
        points: !0
      }), b(i).forEach(v), o.forEach(v), this.h();
    },
    h() {
      f(l, "d", "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"), f(i, "points", "13 2 13 9 20 9"), f(e, "xmlns", "http://www.w3.org/2000/svg"), f(e, "width", "100%"), f(e, "height", "100%"), f(e, "viewBox", "0 0 24 24"), f(e, "fill", "none"), f(e, "stroke", "currentColor"), f(e, "stroke-width", "1.5"), f(e, "stroke-linecap", "round"), f(e, "stroke-linejoin", "round"), f(e, "class", "feather feather-file");
    },
    m(c, o) {
      W(c, e, o), q(e, l), q(e, i);
    },
    p: j,
    i: j,
    o: j,
    d(c) {
      c && v(e);
    }
  };
}
class J extends F {
  constructor(e) {
    super(), H(this, e, null, G, x, {});
  }
}
const {
  SvelteComponent: K,
  add_iframe_resize_listener: L,
  add_render_callback: O,
  append_hydration: p,
  attr: z,
  binding_callbacks: Q,
  check_outros: R,
  children: w,
  claim_component: T,
  claim_element: y,
  claim_space: B,
  claim_text: I,
  create_component: U,
  destroy_component: X,
  detach: m,
  element: k,
  group_outros: Y,
  init: Z,
  insert_hydration: M,
  mount_component: $,
  safe_not_equal: ee,
  set_data: N,
  space: V,
  text: D,
  toggle_class: d,
  transition_in: g,
  transition_out: C
} = window.__gradio__svelte__internal, {
  onMount: te
} = window.__gradio__svelte__internal;
function P(r) {
  let e, l, i, c, o = (
    /*value*/
    r[0].files.map(A).join(", ") + ""
  ), _, s;
  return i = new J({}), {
    c() {
      e = k("span"), l = k("i"), U(i.$$.fragment), c = V(), _ = D(o), this.h();
    },
    l(t) {
      e = y(t, "SPAN", {
        class: !0
      });
      var u = w(e);
      l = y(u, "I", {
        class: !0
      });
      var a = w(l);
      T(i.$$.fragment, a), a.forEach(m), c = B(u), _ = I(u, o), u.forEach(m), this.h();
    },
    h() {
      z(l, "class", "svelte-1j28ovu"), z(e, "class", "files svelte-1j28ovu");
    },
    m(t, u) {
      M(t, e, u), p(e, l), $(i, l, null), p(e, c), p(e, _), s = !0;
    },
    p(t, u) {
      (!s || u & /*value*/
      1) && o !== (o = /*value*/
      t[0].files.map(A).join(", ") + "") && N(_, o);
    },
    i(t) {
      s || (g(i.$$.fragment, t), s = !0);
    },
    o(t) {
      C(i.$$.fragment, t), s = !1;
    },
    d(t) {
      t && m(e), X(i);
    }
  };
}
function le(r) {
  var u;
  let e, l, i = (
    /*value*/
    r[0].text + ""
  ), c, o, _, s, t = (
    /*value*/
    ((u = r[0].files) == null ? void 0 : u.length) > 0 && P(r)
  );
  return {
    c() {
      e = k("div"), l = k("span"), c = D(i), o = V(), t && t.c(), this.h();
    },
    l(a) {
      e = y(a, "DIV", {
        class: !0
      });
      var n = w(e);
      l = y(n, "SPAN", {});
      var h = w(l);
      c = I(h, i), h.forEach(m), o = B(n), t && t.l(n), n.forEach(m), this.h();
    },
    h() {
      z(e, "class", "svelte-1j28ovu"), O(() => (
        /*div_elementresize_handler*/
        r[5].call(e)
      )), d(
        e,
        "table",
        /*type*/
        r[1] === "table"
      ), d(
        e,
        "gallery",
        /*type*/
        r[1] === "gallery"
      ), d(
        e,
        "selected",
        /*selected*/
        r[2]
      );
    },
    m(a, n) {
      M(a, e, n), p(e, l), p(l, c), p(e, o), t && t.m(e, null), _ = L(
        e,
        /*div_elementresize_handler*/
        r[5].bind(e)
      ), r[6](e), s = !0;
    },
    p(a, [n]) {
      var h;
      (!s || n & /*value*/
      1) && i !== (i = /*value*/
      a[0].text + "") && N(c, i), /*value*/
      ((h = a[0].files) == null ? void 0 : h.length) > 0 ? t ? (t.p(a, n), n & /*value*/
      1 && g(t, 1)) : (t = P(a), t.c(), g(t, 1), t.m(e, null)) : t && (Y(), C(t, 1, 1, () => {
        t = null;
      }), R()), (!s || n & /*type*/
      2) && d(
        e,
        "table",
        /*type*/
        a[1] === "table"
      ), (!s || n & /*type*/
      2) && d(
        e,
        "gallery",
        /*type*/
        a[1] === "gallery"
      ), (!s || n & /*selected*/
      4) && d(
        e,
        "selected",
        /*selected*/
        a[2]
      );
    },
    i(a) {
      s || (g(t), s = !0);
    },
    o(a) {
      C(t), s = !1;
    },
    d(a) {
      a && m(e), t && t.d(), _(), r[6](null);
    }
  };
}
const A = (r) => r.orig_name;
function ne(r, e, l) {
  let {
    value: i
  } = e, {
    type: c
  } = e, {
    selected: o = !1
  } = e, _, s;
  function t(n, h) {
    !n || !h || (s.style.setProperty("--local-text-width", `${h < 150 ? h : 200}px`), l(4, s.style.whiteSpace = "unset", s));
  }
  te(() => {
    t(s, _);
  });
  function u() {
    _ = this.clientWidth, l(3, _);
  }
  function a(n) {
    Q[n ? "unshift" : "push"](() => {
      s = n, l(4, s);
    });
  }
  return r.$$set = (n) => {
    "value" in n && l(0, i = n.value), "type" in n && l(1, c = n.type), "selected" in n && l(2, o = n.selected);
  }, [i, c, o, _, s, u, a];
}
class ie extends K {
  constructor(e) {
    super(), Z(this, e, ne, le, ee, {
      value: 0,
      type: 1,
      selected: 2
    });
  }
}
export {
  ie as default
};
