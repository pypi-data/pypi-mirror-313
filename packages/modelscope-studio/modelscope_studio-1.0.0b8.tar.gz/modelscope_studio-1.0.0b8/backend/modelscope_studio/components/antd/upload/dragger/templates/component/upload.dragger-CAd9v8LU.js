import { g as pe, w as U } from "./Index-BU1daTs7.js";
const b = window.ms_globals.React, J = window.ms_globals.React.useMemo, ae = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, D = window.ms_globals.ReactDOM.createPortal, we = window.ms_globals.antd.Upload;
var Y = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var me = b, _e = Symbol.for("react.element"), he = Symbol.for("react.fragment"), ve = Object.prototype.hasOwnProperty, Ie = me.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ye = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Q(e, n, o) {
  var s, r = {}, t = null, i = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (i = n.ref);
  for (s in n) ve.call(n, s) && !ye.hasOwnProperty(s) && (r[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) r[s] === void 0 && (r[s] = n[s]);
  return {
    $$typeof: _e,
    type: e,
    key: t,
    ref: i,
    props: r,
    _owner: Ie.current
  };
}
k.Fragment = he;
k.jsx = Q;
k.jsxs = Q;
Y.exports = k;
var X = Y.exports;
const {
  SvelteComponent: be,
  assign: W,
  binding_callbacks: M,
  check_outros: ge,
  children: Z,
  claim_element: V,
  claim_space: Ee,
  component_subscribe: q,
  compute_slots: Re,
  create_slot: xe,
  detach: S,
  element: $,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Se,
  get_slot_changes: Ue,
  group_outros: Le,
  init: Fe,
  insert_hydration: L,
  safe_not_equal: ke,
  set_custom_element_data: ee,
  space: Oe,
  transition_in: F,
  transition_out: j,
  update_slot_base: Pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ce,
  getContext: De,
  onDestroy: je,
  setContext: Te
} = window.__gradio__svelte__internal;
function H(e) {
  let n, o;
  const s = (
    /*#slots*/
    e[7].default
  ), r = xe(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = $("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      n = V(t, "SVELTE-SLOT", {
        class: !0
      });
      var i = Z(n);
      r && r.l(i), i.forEach(S), this.h();
    },
    h() {
      ee(n, "class", "svelte-1rt0kpf");
    },
    m(t, i) {
      L(t, n, i), r && r.m(n, null), e[9](n), o = !0;
    },
    p(t, i) {
      r && r.p && (!o || i & /*$$scope*/
      64) && Pe(
        r,
        s,
        t,
        /*$$scope*/
        t[6],
        o ? Ue(
          s,
          /*$$scope*/
          t[6],
          i,
          null
        ) : Se(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (F(r, t), o = !0);
    },
    o(t) {
      j(r, t), o = !1;
    },
    d(t) {
      t && S(n), r && r.d(t), e[9](null);
    }
  };
}
function Ne(e) {
  let n, o, s, r, t = (
    /*$$slots*/
    e[4].default && H(e)
  );
  return {
    c() {
      n = $("react-portal-target"), o = Oe(), t && t.c(), s = z(), this.h();
    },
    l(i) {
      n = V(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), Z(n).forEach(S), o = Ee(i), t && t.l(i), s = z(), this.h();
    },
    h() {
      ee(n, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      L(i, n, a), e[8](n), L(i, o, a), t && t.m(i, a), L(i, s, a), r = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? t ? (t.p(i, a), a & /*$$slots*/
      16 && F(t, 1)) : (t = H(i), t.c(), F(t, 1), t.m(s.parentNode, s)) : t && (Le(), j(t, 1, 1, () => {
        t = null;
      }), ge());
    },
    i(i) {
      r || (F(t), r = !0);
    },
    o(i) {
      j(t), r = !1;
    },
    d(i) {
      i && (S(n), S(o), S(s)), e[8](null), t && t.d(i);
    }
  };
}
function K(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function Ae(e, n, o) {
  let s, r, {
    $$slots: t = {},
    $$scope: i
  } = n;
  const a = Re(t);
  let {
    svelteInit: l
  } = n;
  const y = U(K(n)), u = U();
  q(e, u, (d) => o(0, s = d));
  const w = U();
  q(e, w, (d) => o(1, r = d));
  const c = [], m = De("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: v,
    subSlotIndex: g
  } = pe() || {}, E = l({
    parent: m,
    props: y,
    target: u,
    slot: w,
    slotKey: f,
    slotIndex: v,
    subSlotIndex: g,
    onDestroy(d) {
      c.push(d);
    }
  });
  Te("$$ms-gr-react-wrapper", E), Ce(() => {
    y.set(K(n));
  }), je(() => {
    c.forEach((d) => d());
  });
  function p(d) {
    M[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function O(d) {
    M[d ? "unshift" : "push"](() => {
      r = d, w.set(r);
    });
  }
  return e.$$set = (d) => {
    o(17, n = W(W({}, n), G(d))), "svelteInit" in d && o(5, l = d.svelteInit), "$$scope" in d && o(6, i = d.$$scope);
  }, n = G(n), [s, r, u, w, a, l, i, t, p, O];
}
class We extends be {
  constructor(n) {
    super(), Fe(this, n, Ae, Ne, ke, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, C = window.ms_globals.tree;
function Me(e) {
  function n(o) {
    const s = U(), r = new We({
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
          }, a = t.parent ?? C;
          return a.nodes = [...a.nodes, i], B({
            createPortal: D,
            node: C
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((l) => l.svelteInstance !== s), B({
              createPortal: D,
              node: C
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
function qe(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ze(e, n = !1) {
  try {
    if (n && !qe(e))
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
function h(e, n) {
  return J(() => ze(e, n), [e, n]);
}
const Ge = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function He(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const s = e[o];
    return typeof s == "number" && !Ge.includes(o) ? n[o] = s + "px" : n[o] = s, n;
  }, {}) : {};
}
function T(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(D(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: b.Children.toArray(e._reactElement.props.children).map((r) => {
        if (b.isValidElement(r) && r.props.__slot__) {
          const {
            portals: t,
            clonedElement: i
          } = T(r.props.el);
          return b.cloneElement(r, {
            ...r.props,
            el: i,
            children: [...b.Children.toArray(r.props.children), ...t]
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
      } = T(t);
      n.push(...a), o.appendChild(i);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function Ke(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const Be = ae(({
  slot: e,
  clone: n,
  className: o,
  style: s
}, r) => {
  const t = de(), [i, a] = ue([]);
  return fe(() => {
    var w;
    if (!t.current || !e)
      return;
    let l = e;
    function y() {
      let c = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (c = l.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ke(r, c), o && c.classList.add(...o.split(" ")), s) {
        const m = He(s);
        Object.keys(m).forEach((f) => {
          c.style[f] = m[f];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var g, E, p;
        (g = t.current) != null && g.contains(l) && ((E = t.current) == null || E.removeChild(l));
        const {
          portals: f,
          clonedElement: v
        } = T(e);
        return l = v, a(f), l.style.display = "contents", y(), (p = t.current) == null || p.appendChild(l), f.length > 0;
      };
      c() || (u = new window.MutationObserver(() => {
        c() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      l.style.display = "contents", y(), (w = t.current) == null || w.appendChild(l);
    return () => {
      var c, m;
      l.style.display = "", (c = t.current) != null && c.contains(l) && ((m = t.current) == null || m.removeChild(l)), u == null || u.disconnect();
    };
  }, [e, n, o, s, r]), b.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...i);
});
function Je(e, n) {
  return e ? /* @__PURE__ */ X.jsx(Be, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function x({
  key: e,
  setSlotParams: n,
  slots: o
}, s) {
  return o[e] ? (...r) => (n(e, r), Je(o[e], {
    clone: !0,
    ...s
  })) : void 0;
}
function Ye(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Xe = Me(({
  slots: e,
  upload: n,
  showUploadList: o,
  progress: s,
  beforeUpload: r,
  customRequest: t,
  previewFile: i,
  isImageUrl: a,
  itemRender: l,
  iconRender: y,
  data: u,
  onChange: w,
  onValueChange: c,
  onRemove: m,
  fileList: f,
  setSlotParams: v,
  ...g
}) => {
  const E = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof o == "object", p = Ye(o), O = h(p.showPreviewIcon), d = h(p.showRemoveIcon), te = h(p.showDownloadIcon), N = h(r), ne = h(t), oe = h(s == null ? void 0 : s.format), re = h(i), se = h(a), ie = h(l), le = h(y), ce = h(u), A = J(() => (f == null ? void 0 : f.map((_) => ({
    ..._,
    name: _.orig_name || _.path,
    uid: _.url || _.path,
    status: "done"
  }))) || [], [f]);
  return /* @__PURE__ */ X.jsx(we.Dragger, {
    ...g,
    fileList: A,
    data: ce || u,
    previewFile: re,
    isImageUrl: se,
    itemRender: e.itemRender ? x({
      slots: e,
      setSlotParams: v,
      key: "itemRender"
    }) : ie,
    iconRender: e.iconRender ? x({
      slots: e,
      setSlotParams: v,
      key: "iconRender"
    }) : le,
    onRemove: (_) => {
      m == null || m(_);
      const P = A.findIndex((I) => I.uid === _.uid), R = f.slice();
      R.splice(P, 1), c == null || c(R), w == null || w(R.map((I) => I.path));
    },
    beforeUpload: async (_, P) => {
      if (N && !await N(_, P))
        return !1;
      const R = (await n([_])).filter((I) => I);
      return c == null || c([...f, ...R]), w == null || w([...f.map((I) => I.path), ...R.map((I) => I.path)]), !1;
    },
    customRequest: ne,
    progress: s && {
      ...s,
      format: oe
    },
    showUploadList: E ? {
      ...p,
      showDownloadIcon: te || p.showDownloadIcon,
      showRemoveIcon: d || p.showRemoveIcon,
      showPreviewIcon: O || p.showPreviewIcon,
      downloadIcon: e["showUploadList.downloadIcon"] ? x({
        slots: e,
        setSlotParams: v,
        key: "showUploadList.downloadIcon"
      }) : p.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? x({
        slots: e,
        setSlotParams: v,
        key: "showUploadList.removeIcon"
      }) : p.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? x({
        slots: e,
        setSlotParams: v,
        key: "showUploadList.previewIcon"
      }) : p.previewIcon,
      extra: e["showUploadList.extra"] ? x({
        slots: e,
        setSlotParams: v,
        key: "showUploadList.extra"
      }) : p.extra
    } : o
  });
});
export {
  Xe as UploadDragger,
  Xe as default
};
