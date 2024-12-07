const {
  SvelteComponent: y,
  add_iframe_resize_listener: b,
  add_render_callback: m,
  append_hydration: v,
  attr: w,
  binding_callbacks: z,
  children: k,
  claim_element: p,
  claim_text: E,
  detach: o,
  element: S,
  init: q,
  insert_hydration: C,
  noop: u,
  safe_not_equal: D,
  set_data: I,
  text: M,
  toggle_class: r
} = window.__gradio__svelte__internal, { onMount: P } = window.__gradio__svelte__internal;
function V(n) {
  let e, i = (
    /*value*/
    (n[0] ? (
      /*value*/
      n[0]
    ) : "") + ""
  ), a, d;
  return {
    c() {
      e = S("div"), a = M(i), this.h();
    },
    l(t) {
      e = p(t, "DIV", { class: !0 });
      var l = k(e);
      a = E(l, i), l.forEach(o), this.h();
    },
    h() {
      w(e, "class", "svelte-84cxb8"), m(() => (
        /*div_elementresize_handler*/
        n[5].call(e)
      )), r(
        e,
        "table",
        /*type*/
        n[1] === "table"
      ), r(
        e,
        "gallery",
        /*type*/
        n[1] === "gallery"
      ), r(
        e,
        "selected",
        /*selected*/
        n[2]
      );
    },
    m(t, l) {
      C(t, e, l), v(e, a), d = b(
        e,
        /*div_elementresize_handler*/
        n[5].bind(e)
      ), n[6](e);
    },
    p(t, [l]) {
      l & /*value*/
      1 && i !== (i = /*value*/
      (t[0] ? (
        /*value*/
        t[0]
      ) : "") + "") && I(a, i), l & /*type*/
      2 && r(
        e,
        "table",
        /*type*/
        t[1] === "table"
      ), l & /*type*/
      2 && r(
        e,
        "gallery",
        /*type*/
        t[1] === "gallery"
      ), l & /*selected*/
      4 && r(
        e,
        "selected",
        /*selected*/
        t[2]
      );
    },
    i: u,
    o: u,
    d(t) {
      t && o(e), d(), n[6](null);
    }
  };
}
function W(n, e, i) {
  let { value: a } = e, { type: d } = e, { selected: t = !1 } = e, l, _;
  function f(s, c) {
    !s || !c || (_.style.setProperty("--local-text-width", `${c < 150 ? c : 200}px`), i(4, _.style.whiteSpace = "unset", _));
  }
  P(() => {
    f(_, l);
  });
  function h() {
    l = this.clientWidth, i(3, l);
  }
  function g(s) {
    z[s ? "unshift" : "push"](() => {
      _ = s, i(4, _);
    });
  }
  return n.$$set = (s) => {
    "value" in s && i(0, a = s.value), "type" in s && i(1, d = s.type), "selected" in s && i(2, t = s.selected);
  }, [a, d, t, l, _, h, g];
}
class j extends y {
  constructor(e) {
    super(), q(this, e, W, V, D, { value: 0, type: 1, selected: 2 });
  }
}
export {
  j as default
};
