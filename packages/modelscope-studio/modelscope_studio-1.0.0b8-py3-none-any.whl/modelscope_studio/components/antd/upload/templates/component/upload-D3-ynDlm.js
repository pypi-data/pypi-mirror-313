import { g as ve, w as j } from "./Index-BG68G0YH.js";
const L = window.ms_globals.React, $ = window.ms_globals.React.useMemo, ye = window.ms_globals.React.forwardRef, ee = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, ne = window.ms_globals.React.useEffect, A = window.ms_globals.ReactDOM.createPortal, be = window.ms_globals.antd.Upload;
function ge() {
}
var oe = {
  exports: {}
}, T = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ee = L, Re = Symbol.for("react.element"), Le = Symbol.for("react.fragment"), xe = Object.prototype.hasOwnProperty, Fe = Ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(e, n, o) {
  var s, r = {}, t = null, i = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (i = n.ref);
  for (s in n) xe.call(n, s) && !Ue.hasOwnProperty(s) && (r[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: Re,
    type: e,
    key: t,
    ref: i,
    props: r,
    _owner: Fe.current
  };
}
T.Fragment = Le;
T.jsx = re;
T.jsxs = re;
oe.exports = T;
var se = oe.exports;
const {
  SvelteComponent: Se,
  assign: K,
  binding_callbacks: B,
  check_outros: ke,
  children: ie,
  claim_element: le,
  claim_space: Oe,
  component_subscribe: J,
  compute_slots: Pe,
  create_slot: je,
  detach: O,
  element: ce,
  empty: Y,
  exclude_internal_props: Q,
  get_all_dirty_from_scope: Ce,
  get_slot_changes: De,
  group_outros: Te,
  init: Ne,
  insert_hydration: C,
  safe_not_equal: Ae,
  set_custom_element_data: ae,
  space: We,
  transition_in: D,
  transition_out: W,
  update_slot_base: ze
} = window.__gradio__svelte__internal, {
  beforeUpdate: Me,
  getContext: qe,
  onDestroy: Ge,
  setContext: He
} = window.__gradio__svelte__internal;
function X(e) {
  let n, o;
  const s = (
    /*#slots*/
    e[7].default
  ), r = je(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = ce("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = le(t, "SVELTE-SLOT", {
        class: !0
      });
      var i = ie(n);
      r && r.l(i), i.forEach(O), this.h();
    },
    h() {
      ae(n, "class", "svelte-1rt0kpf");
    },
    m(t, i) {
      C(t, n, i), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, i) {
      r && r.p && (!o || i & /*$$scope*/
      64) && ze(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        o ? De(
          s,
          /*$$scope*/
          t[6],
          i,
          null
        ) : Ce(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (D(r, t), o = !0);
    },
    o(t) {
      W(r, t), o = !1;
    },
    d(t) {
      t && O(n), r && r.d(t), e[9](null);
    }
  };
}
function Ke(e) {
  let n, o, s, r, t = (
    /*$$slots*/
    e[4].default && X(e)
  );
  return {
    c() {
      n = ce("react-portal-target"), o = We(), t && t.c(), s = Y(), this.h();
    },
    l(i) {
      n = le(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), ie(n).forEach(O), o = Oe(i), t && t.l(i), s = Y(), this.h();
    },
    h() {
      ae(n, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      C(i, n, a), e[8](n), C(i, o, a), t && t.m(i, a), C(i, s, a), r = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? t ? (t.p(i, a), a & /*$$slots*/
      16 && D(t, 1)) : (t = X(i), t.c(), D(t, 1), t.m(s.parentNode, s)) : t && (Te(), W(t, 1, 1, () => {
        t = null;
      }), ke());
    },
    i(i) {
      r || (D(t), r = !0);
    },
    o(i) {
      W(t), r = !1;
    },
    d(i) {
      i && (O(n), O(o), O(s)), e[8](null), t && t.d(i);
    }
  };
}
function Z(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function Be(e, n, o) {
  let s, r, {
    $$slots: t = {},
    $$scope: i
  } = n;
  const a = Pe(t);
  let {
    svelteInit: l
  } = n;
  const b = j(Z(n)), u = j();
  J(e, u, (d) => o(0, s = d));
  const f = j();
  J(e, f, (d) => o(1, r = d));
  const c = [], _ = qe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: g,
    subSlotIndex: h
  } = ve() || {}, x = l({
    parent: _,
    props: b,
    target: u,
    slot: f,
    slotKey: p,
    slotIndex: g,
    subSlotIndex: h,
    onDestroy(d) {
      c.push(d);
    }
  });
  He("$$ms-gr-react-wrapper", x), Me(() => {
    b.set(Z(n));
  }), Ge(() => {
    c.forEach((d) => d());
  });
  function F(d) {
    B[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function w(d) {
    B[d ? "unshift" : "push"](() => {
      r = d, f.set(r);
    });
  }
  return e.$$set = (d) => {
    o(17, n = K(K({}, n), Q(d))), "svelteInit" in d && o(5, l = d.svelteInit), "$$scope" in d && o(6, i = d.$$scope);
  }, n = Q(n), [s, r, u, f, a, l, i, t, F, w];
}
class Je extends Se {
  constructor(n) {
    super(), Ne(this, n, Be, Ke, Ae, {
      svelteInit: 5
    });
  }
}
const V = window.ms_globals.rerender, N = window.ms_globals.tree;
function Ye(e) {
  function n(o) {
    const s = j(), r = new Je({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, a = t.parent ?? N;
          return a.nodes = [...a.nodes, i], V({
            createPortal: A,
            node: N
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((l) => l.svelteInstance !== s), V({
              createPortal: A,
              node: N
            });
          }), i;
        },
        ...o.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
function Qe(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Xe(e, n = !1) {
  try {
    if (n && !Qe(e))
      return;
    if (typeof e == "string") {
      let o = e.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function I(e, n) {
  return $(() => Xe(e, n), [e, n]);
}
const Ze = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ve(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const s = e[o];
    return typeof s == "number" && !Ze.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function z(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(A(L.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: L.Children.toArray(e._reactElement.props.children).map((r) => {
        if (L.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: i
          } = z(r.props.el);
          return L.cloneElement(r, {
            ...r.props,
            el: i,
            children: [...L.Children.toArray(r.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: i,
      type: a,
      useCapture: l
    }) => {
      o.addEventListener(a, i, l);
    });
  });
  const s = Array.from(e.childNodes);
  for (let r = 0; r < s.length; r++) {
    const t = s[r];
    if (t.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = z(t);
      n.push(...a), o.appendChild(i);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function $e(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const et = ye(({
  slot: e,
  clone: n,
  className: o,
  style: s
}, r) => {
  const t = ee(), [i, a] = te([]);
  return ne(() => {
    var f;
    if (!t.current || !e)
      return;
    let l = e;
    function b() {
      let c = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (c = l.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), $e(r, c), o && c.classList.add(...o.split(" ")), s) {
        const _ = Ve(s);
        Object.keys(_).forEach((p) => {
          c.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var h, x, F;
        (h = t.current) != null && h.contains(l) && ((x = t.current) == null || x.removeChild(l));
        const {
          portals: p,
          clonedElement: g
        } = z(e);
        return l = g, a(p), l.style.display = "contents", b(), (F = t.current) == null || F.appendChild(l), p.length > 0;
      };
      c() || (u = new window.MutationObserver(() => {
        c() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      l.style.display = "contents", b(), (f = t.current) == null || f.appendChild(l);
    return () => {
      var c, _;
      l.style.display = "", (c = t.current) != null && c.contains(l) && ((_ = t.current) == null || _.removeChild(l)), u == null || u.disconnect();
    };
  }, [e, n, o, s, r]), L.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...i);
});
function tt(e, n) {
  return e ? /* @__PURE__ */ se.jsx(et, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function k({
  key: e,
  setSlotParams: n,
  slots: o
}, s) {
  return o[e] ? (...r) => (n(e, r), tt(o[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const nt = (e) => !!e.name;
function ot(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const st = Ye(({
  slots: e,
  upload: n,
  showUploadList: o,
  progress: s,
  beforeUpload: r,
  customRequest: t,
  previewFile: i,
  isImageUrl: a,
  itemRender: l,
  iconRender: b,
  data: u,
  onChange: f,
  onValueChange: c,
  onRemove: _,
  maxCount: p,
  fileList: g,
  setSlotParams: h,
  ...x
}) => {
  const F = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof o == "object", w = ot(o), d = I(w.showPreviewIcon), de = I(w.showRemoveIcon), ue = I(w.showDownloadIcon), M = I(r), fe = I(t), pe = I(s == null ? void 0 : s.format), we = I(i), me = I(a), _e = I(l), he = I(b), Ie = I(u), P = ee(!1), [E, q] = te(g);
  ne(() => {
    q(g);
  }, [g]);
  const G = $(() => (E == null ? void 0 : E.map((m) => nt(m) ? m : {
    ...m,
    name: m.orig_name || m.path,
    uid: m.uid || m.url || m.path,
    status: "done"
  })) || [], [E]);
  return /* @__PURE__ */ se.jsx(be, {
    ...x,
    fileList: G,
    data: Ie || u,
    previewFile: we,
    isImageUrl: me,
    maxCount: 1,
    itemRender: e.itemRender ? k({
      slots: e,
      setSlotParams: h,
      key: "itemRender"
    }) : _e,
    iconRender: e.iconRender ? k({
      slots: e,
      setSlotParams: h,
      key: "iconRender"
    }) : he,
    onRemove: (m) => {
      if (P.current)
        return;
      _ == null || _(m);
      const U = G.findIndex((R) => R.uid === m.uid), v = E.slice();
      v.splice(U, 1), c == null || c(v), f == null || f(v.map((R) => R.path));
    },
    customRequest: fe || ge,
    beforeUpload: async (m, U) => {
      if (M && !await M(m, U) || P.current)
        return !1;
      P.current = !0;
      let v = U;
      if (typeof p == "number") {
        const y = p - E.length;
        v = U.slice(0, y < 0 ? 0 : y);
      } else if (p === 1)
        v = U.slice(0, 1);
      else if (v.length === 0)
        return P.current = !1, !1;
      q((y) => [...p === 1 ? [] : y, ...v.map((S) => ({
        ...S,
        size: S.size,
        uid: S.uid,
        name: S.name,
        status: "uploading"
      }))]);
      const R = (await n(v)).filter((y) => y), H = p === 1 ? R : [...E.filter((y) => !R.some((S) => S.uid === y.uid)), ...R];
      return P.current = !1, c == null || c(H), f == null || f(H.map((y) => y.path)), !1;
    },
    progress: s && {
      ...s,
      format: pe
    },
    showUploadList: F ? {
      ...w,
      showDownloadIcon: ue || w.showDownloadIcon,
      showRemoveIcon: de || w.showRemoveIcon,
      showPreviewIcon: d || w.showPreviewIcon,
      downloadIcon: e["showUploadList.downloadIcon"] ? k({
        slots: e,
        setSlotParams: h,
        key: "showUploadList.downloadIcon"
      }) : w.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? k({
        slots: e,
        setSlotParams: h,
        key: "showUploadList.removeIcon"
      }) : w.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? k({
        slots: e,
        setSlotParams: h,
        key: "showUploadList.previewIcon"
      }) : w.previewIcon,
      extra: e["showUploadList.extra"] ? k({
        slots: e,
        setSlotParams: h,
        key: "showUploadList.extra"
      }) : w.extra
    } : o
  });
});
export {
  st as Upload,
  st as default
};
