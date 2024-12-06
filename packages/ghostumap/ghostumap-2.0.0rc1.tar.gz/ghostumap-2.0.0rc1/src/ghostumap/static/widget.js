function Kt(t, e) {
  return t == null || e == null ? NaN : t < e ? -1 : t > e ? 1 : t >= e ? 0 : NaN;
}
function Ni(t, e) {
  return t == null || e == null ? NaN : e < t ? -1 : e > t ? 1 : e >= t ? 0 : NaN;
}
function Rn(t) {
  let e, n, i;
  t.length !== 2 ? (e = Kt, n = (a, u) => Kt(t(a), u), i = (a, u) => t(a) - u) : (e = t === Kt || t === Ni ? t : Ti, n = t, i = t);
  function r(a, u, l = 0, c = a.length) {
    if (l < c) {
      if (e(u, u) !== 0) return c;
      do {
        const h = l + c >>> 1;
        n(a[h], u) < 0 ? l = h + 1 : c = h;
      } while (l < c);
    }
    return l;
  }
  function s(a, u, l = 0, c = a.length) {
    if (l < c) {
      if (e(u, u) !== 0) return c;
      do {
        const h = l + c >>> 1;
        n(a[h], u) <= 0 ? l = h + 1 : c = h;
      } while (l < c);
    }
    return l;
  }
  function o(a, u, l = 0, c = a.length) {
    const h = r(a, u, l, c - 1);
    return h > l && i(a[h - 1], u) > -i(a[h], u) ? h - 1 : h;
  }
  return { left: r, center: o, right: s };
}
function Ti() {
  return 0;
}
function Ci(t) {
  return t === null ? NaN : +t;
}
const zi = Rn(Kt), Ii = zi.right;
Rn(Ci).center;
function Qe(t, e) {
  let n, i;
  if (e === void 0)
    for (const r of t)
      r != null && (n === void 0 ? r >= r && (n = i = r) : (n > r && (n = r), i < r && (i = r)));
  else {
    let r = -1;
    for (let s of t)
      (s = e(s, ++r, t)) != null && (n === void 0 ? s >= s && (n = i = s) : (n > s && (n = s), i < s && (i = s)));
  }
  return [n, i];
}
class Je extends Map {
  constructor(e, n = Pi) {
    if (super(), Object.defineProperties(this, { _intern: { value: /* @__PURE__ */ new Map() }, _key: { value: n } }), e != null) for (const [i, r] of e) this.set(i, r);
  }
  get(e) {
    return super.get(je(this, e));
  }
  has(e) {
    return super.has(je(this, e));
  }
  set(e, n) {
    return super.set(Ri(this, e), n);
  }
  delete(e) {
    return super.delete(Li(this, e));
  }
}
function je({ _intern: t, _key: e }, n) {
  const i = e(n);
  return t.has(i) ? t.get(i) : n;
}
function Ri({ _intern: t, _key: e }, n) {
  const i = e(n);
  return t.has(i) ? t.get(i) : (t.set(i, n), n);
}
function Li({ _intern: t, _key: e }, n) {
  const i = e(n);
  return t.has(i) && (n = t.get(i), t.delete(i)), n;
}
function Pi(t) {
  return t !== null && typeof t == "object" ? t.valueOf() : t;
}
const Hi = Math.sqrt(50), Di = Math.sqrt(10), Ui = Math.sqrt(2);
function te(t, e, n) {
  const i = (e - t) / Math.max(0, n), r = Math.floor(Math.log10(i)), s = i / Math.pow(10, r), o = s >= Hi ? 10 : s >= Di ? 5 : s >= Ui ? 2 : 1;
  let a, u, l;
  return r < 0 ? (l = Math.pow(10, -r) / o, a = Math.round(t * l), u = Math.round(e * l), a / l < t && ++a, u / l > e && --u, l = -l) : (l = Math.pow(10, r) * o, a = Math.round(t / l), u = Math.round(e / l), a * l < t && ++a, u * l > e && --u), u < a && 0.5 <= n && n < 2 ? te(t, e, n * 2) : [a, u, l];
}
function Vi(t, e, n) {
  if (e = +e, t = +t, n = +n, !(n > 0)) return [];
  if (t === e) return [t];
  const i = e < t, [r, s, o] = i ? te(e, t, n) : te(t, e, n);
  if (!(s >= r)) return [];
  const a = s - r + 1, u = new Array(a);
  if (i)
    if (o < 0) for (let l = 0; l < a; ++l) u[l] = (s - l) / -o;
    else for (let l = 0; l < a; ++l) u[l] = (s - l) * o;
  else if (o < 0) for (let l = 0; l < a; ++l) u[l] = (r + l) / -o;
  else for (let l = 0; l < a; ++l) u[l] = (r + l) * o;
  return u;
}
function Ae(t, e, n) {
  return e = +e, t = +t, n = +n, te(t, e, n)[2];
}
function qi(t, e, n) {
  e = +e, t = +t, n = +n;
  const i = e < t, r = i ? Ae(e, t, n) : Ae(t, e, n);
  return (i ? -1 : 1) * (r < 0 ? 1 / -r : r);
}
function Fi(t, e) {
  let n;
  for (const i of t)
    i != null && (n < i || n === void 0 && i >= i) && (n = i);
  return n;
}
function Ln(t, e, n) {
  t = +t, e = +e, n = (r = arguments.length) < 2 ? (e = t, t = 0, 1) : r < 3 ? 1 : +n;
  for (var i = -1, r = Math.max(0, Math.ceil((e - t) / n)) | 0, s = new Array(r); ++i < r; )
    s[i] = t + i * n;
  return s;
}
var Oi = { value: () => {
} };
function Ve() {
  for (var t = 0, e = arguments.length, n = {}, i; t < e; ++t) {
    if (!(i = arguments[t] + "") || i in n || /[\s.]/.test(i)) throw new Error("illegal type: " + i);
    n[i] = [];
  }
  return new Zt(n);
}
function Zt(t) {
  this._ = t;
}
function Xi(t, e) {
  return t.trim().split(/^|\s+/).map(function(n) {
    var i = "", r = n.indexOf(".");
    if (r >= 0 && (i = n.slice(r + 1), n = n.slice(0, r)), n && !e.hasOwnProperty(n)) throw new Error("unknown type: " + n);
    return { type: n, name: i };
  });
}
Zt.prototype = Ve.prototype = {
  constructor: Zt,
  on: function(t, e) {
    var n = this._, i = Xi(t + "", n), r, s = -1, o = i.length;
    if (arguments.length < 2) {
      for (; ++s < o; ) if ((r = (t = i[s]).type) && (r = Bi(n[r], t.name))) return r;
      return;
    }
    if (e != null && typeof e != "function") throw new Error("invalid callback: " + e);
    for (; ++s < o; )
      if (r = (t = i[s]).type) n[r] = tn(n[r], t.name, e);
      else if (e == null) for (r in n) n[r] = tn(n[r], t.name, null);
    return this;
  },
  copy: function() {
    var t = {}, e = this._;
    for (var n in e) t[n] = e[n].slice();
    return new Zt(t);
  },
  call: function(t, e) {
    if ((r = arguments.length - 2) > 0) for (var n = new Array(r), i = 0, r, s; i < r; ++i) n[i] = arguments[i + 2];
    if (!this._.hasOwnProperty(t)) throw new Error("unknown type: " + t);
    for (s = this._[t], i = 0, r = s.length; i < r; ++i) s[i].value.apply(e, n);
  },
  apply: function(t, e, n) {
    if (!this._.hasOwnProperty(t)) throw new Error("unknown type: " + t);
    for (var i = this._[t], r = 0, s = i.length; r < s; ++r) i[r].value.apply(e, n);
  }
};
function Bi(t, e) {
  for (var n = 0, i = t.length, r; n < i; ++n)
    if ((r = t[n]).name === e)
      return r.value;
}
function tn(t, e, n) {
  for (var i = 0, r = t.length; i < r; ++i)
    if (t[i].name === e) {
      t[i] = Oi, t = t.slice(0, i).concat(t.slice(i + 1));
      break;
    }
  return n != null && t.push({ name: e, value: n }), t;
}
var Me = "http://www.w3.org/1999/xhtml";
const en = {
  svg: "http://www.w3.org/2000/svg",
  xhtml: Me,
  xlink: "http://www.w3.org/1999/xlink",
  xml: "http://www.w3.org/XML/1998/namespace",
  xmlns: "http://www.w3.org/2000/xmlns/"
};
function ce(t) {
  var e = t += "", n = e.indexOf(":");
  return n >= 0 && (e = t.slice(0, n)) !== "xmlns" && (t = t.slice(n + 1)), en.hasOwnProperty(e) ? { space: en[e], local: t } : t;
}
function Gi(t) {
  return function() {
    var e = this.ownerDocument, n = this.namespaceURI;
    return n === Me && e.documentElement.namespaceURI === Me ? e.createElement(t) : e.createElementNS(n, t);
  };
}
function Yi(t) {
  return function() {
    return this.ownerDocument.createElementNS(t.space, t.local);
  };
}
function qe(t) {
  var e = ce(t);
  return (e.local ? Yi : Gi)(e);
}
function Wi() {
}
function Fe(t) {
  return t == null ? Wi : function() {
    return this.querySelector(t);
  };
}
function Ki(t) {
  typeof t != "function" && (t = Fe(t));
  for (var e = this._groups, n = e.length, i = new Array(n), r = 0; r < n; ++r)
    for (var s = e[r], o = s.length, a = i[r] = new Array(o), u, l, c = 0; c < o; ++c)
      (u = s[c]) && (l = t.call(u, u.__data__, c, s)) && ("__data__" in u && (l.__data__ = u.__data__), a[c] = l);
  return new L(i, this._parents);
}
function Pn(t) {
  return t == null ? [] : Array.isArray(t) ? t : Array.from(t);
}
function Zi() {
  return [];
}
function Hn(t) {
  return t == null ? Zi : function() {
    return this.querySelectorAll(t);
  };
}
function Qi(t) {
  return function() {
    return Pn(t.apply(this, arguments));
  };
}
function Ji(t) {
  typeof t == "function" ? t = Qi(t) : t = Hn(t);
  for (var e = this._groups, n = e.length, i = [], r = [], s = 0; s < n; ++s)
    for (var o = e[s], a = o.length, u, l = 0; l < a; ++l)
      (u = o[l]) && (i.push(t.call(u, u.__data__, l, o)), r.push(u));
  return new L(i, r);
}
function Dn(t) {
  return function() {
    return this.matches(t);
  };
}
function Un(t) {
  return function(e) {
    return e.matches(t);
  };
}
var ji = Array.prototype.find;
function tr(t) {
  return function() {
    return ji.call(this.children, t);
  };
}
function er() {
  return this.firstElementChild;
}
function nr(t) {
  return this.select(t == null ? er : tr(typeof t == "function" ? t : Un(t)));
}
var ir = Array.prototype.filter;
function rr() {
  return Array.from(this.children);
}
function sr(t) {
  return function() {
    return ir.call(this.children, t);
  };
}
function or(t) {
  return this.selectAll(t == null ? rr : sr(typeof t == "function" ? t : Un(t)));
}
function ar(t) {
  typeof t != "function" && (t = Dn(t));
  for (var e = this._groups, n = e.length, i = new Array(n), r = 0; r < n; ++r)
    for (var s = e[r], o = s.length, a = i[r] = [], u, l = 0; l < o; ++l)
      (u = s[l]) && t.call(u, u.__data__, l, s) && a.push(u);
  return new L(i, this._parents);
}
function Vn(t) {
  return new Array(t.length);
}
function lr() {
  return new L(this._enter || this._groups.map(Vn), this._parents);
}
function ee(t, e) {
  this.ownerDocument = t.ownerDocument, this.namespaceURI = t.namespaceURI, this._next = null, this._parent = t, this.__data__ = e;
}
ee.prototype = {
  constructor: ee,
  appendChild: function(t) {
    return this._parent.insertBefore(t, this._next);
  },
  insertBefore: function(t, e) {
    return this._parent.insertBefore(t, e);
  },
  querySelector: function(t) {
    return this._parent.querySelector(t);
  },
  querySelectorAll: function(t) {
    return this._parent.querySelectorAll(t);
  }
};
function ur(t) {
  return function() {
    return t;
  };
}
function cr(t, e, n, i, r, s) {
  for (var o = 0, a, u = e.length, l = s.length; o < l; ++o)
    (a = e[o]) ? (a.__data__ = s[o], i[o] = a) : n[o] = new ee(t, s[o]);
  for (; o < u; ++o)
    (a = e[o]) && (r[o] = a);
}
function hr(t, e, n, i, r, s, o) {
  var a, u, l = /* @__PURE__ */ new Map(), c = e.length, h = s.length, d = new Array(c), g;
  for (a = 0; a < c; ++a)
    (u = e[a]) && (d[a] = g = o.call(u, u.__data__, a, e) + "", l.has(g) ? r[a] = u : l.set(g, u));
  for (a = 0; a < h; ++a)
    g = o.call(t, s[a], a, s) + "", (u = l.get(g)) ? (i[a] = u, u.__data__ = s[a], l.delete(g)) : n[a] = new ee(t, s[a]);
  for (a = 0; a < c; ++a)
    (u = e[a]) && l.get(d[a]) === u && (r[a] = u);
}
function fr(t) {
  return t.__data__;
}
function dr(t, e) {
  if (!arguments.length) return Array.from(this, fr);
  var n = e ? hr : cr, i = this._parents, r = this._groups;
  typeof t != "function" && (t = ur(t));
  for (var s = r.length, o = new Array(s), a = new Array(s), u = new Array(s), l = 0; l < s; ++l) {
    var c = i[l], h = r[l], d = h.length, g = gr(t.call(c, c && c.__data__, l, i)), m = g.length, x = a[l] = new Array(m), M = o[l] = new Array(m), v = u[l] = new Array(d);
    n(c, h, x, M, v, g, e);
    for (var N = 0, S = 0, I, k; N < m; ++N)
      if (I = x[N]) {
        for (N >= S && (S = N + 1); !(k = M[S]) && ++S < m; ) ;
        I._next = k || null;
      }
  }
  return o = new L(o, i), o._enter = a, o._exit = u, o;
}
function gr(t) {
  return typeof t == "object" && "length" in t ? t : Array.from(t);
}
function pr() {
  return new L(this._exit || this._groups.map(Vn), this._parents);
}
function mr(t, e, n) {
  var i = this.enter(), r = this, s = this.exit();
  return typeof t == "function" ? (i = t(i), i && (i = i.selection())) : i = i.append(t + ""), e != null && (r = e(r), r && (r = r.selection())), n == null ? s.remove() : n(s), i && r ? i.merge(r).order() : r;
}
function yr(t) {
  for (var e = t.selection ? t.selection() : t, n = this._groups, i = e._groups, r = n.length, s = i.length, o = Math.min(r, s), a = new Array(r), u = 0; u < o; ++u)
    for (var l = n[u], c = i[u], h = l.length, d = a[u] = new Array(h), g, m = 0; m < h; ++m)
      (g = l[m] || c[m]) && (d[m] = g);
  for (; u < r; ++u)
    a[u] = n[u];
  return new L(a, this._parents);
}
function _r() {
  for (var t = this._groups, e = -1, n = t.length; ++e < n; )
    for (var i = t[e], r = i.length - 1, s = i[r], o; --r >= 0; )
      (o = i[r]) && (s && o.compareDocumentPosition(s) ^ 4 && s.parentNode.insertBefore(o, s), s = o);
  return this;
}
function vr(t) {
  t || (t = xr);
  function e(h, d) {
    return h && d ? t(h.__data__, d.__data__) : !h - !d;
  }
  for (var n = this._groups, i = n.length, r = new Array(i), s = 0; s < i; ++s) {
    for (var o = n[s], a = o.length, u = r[s] = new Array(a), l, c = 0; c < a; ++c)
      (l = o[c]) && (u[c] = l);
    u.sort(e);
  }
  return new L(r, this._parents).order();
}
function xr(t, e) {
  return t < e ? -1 : t > e ? 1 : t >= e ? 0 : NaN;
}
function wr() {
  var t = arguments[0];
  return arguments[0] = this, t.apply(null, arguments), this;
}
function br() {
  return Array.from(this);
}
function $r() {
  for (var t = this._groups, e = 0, n = t.length; e < n; ++e)
    for (var i = t[e], r = 0, s = i.length; r < s; ++r) {
      var o = i[r];
      if (o) return o;
    }
  return null;
}
function Ar() {
  let t = 0;
  for (const e of this) ++t;
  return t;
}
function Mr() {
  return !this.node();
}
function kr(t) {
  for (var e = this._groups, n = 0, i = e.length; n < i; ++n)
    for (var r = e[n], s = 0, o = r.length, a; s < o; ++s)
      (a = r[s]) && t.call(a, a.__data__, s, r);
  return this;
}
function Er(t) {
  return function() {
    this.removeAttribute(t);
  };
}
function Sr(t) {
  return function() {
    this.removeAttributeNS(t.space, t.local);
  };
}
function Nr(t, e) {
  return function() {
    this.setAttribute(t, e);
  };
}
function Tr(t, e) {
  return function() {
    this.setAttributeNS(t.space, t.local, e);
  };
}
function Cr(t, e) {
  return function() {
    var n = e.apply(this, arguments);
    n == null ? this.removeAttribute(t) : this.setAttribute(t, n);
  };
}
function zr(t, e) {
  return function() {
    var n = e.apply(this, arguments);
    n == null ? this.removeAttributeNS(t.space, t.local) : this.setAttributeNS(t.space, t.local, n);
  };
}
function Ir(t, e) {
  var n = ce(t);
  if (arguments.length < 2) {
    var i = this.node();
    return n.local ? i.getAttributeNS(n.space, n.local) : i.getAttribute(n);
  }
  return this.each((e == null ? n.local ? Sr : Er : typeof e == "function" ? n.local ? zr : Cr : n.local ? Tr : Nr)(n, e));
}
function qn(t) {
  return t.ownerDocument && t.ownerDocument.defaultView || t.document && t || t.defaultView;
}
function Rr(t) {
  return function() {
    this.style.removeProperty(t);
  };
}
function Lr(t, e, n) {
  return function() {
    this.style.setProperty(t, e, n);
  };
}
function Pr(t, e, n) {
  return function() {
    var i = e.apply(this, arguments);
    i == null ? this.style.removeProperty(t) : this.style.setProperty(t, i, n);
  };
}
function Hr(t, e, n) {
  return arguments.length > 1 ? this.each((e == null ? Rr : typeof e == "function" ? Pr : Lr)(t, e, n ?? "")) : wt(this.node(), t);
}
function wt(t, e) {
  return t.style.getPropertyValue(e) || qn(t).getComputedStyle(t, null).getPropertyValue(e);
}
function Dr(t) {
  return function() {
    delete this[t];
  };
}
function Ur(t, e) {
  return function() {
    this[t] = e;
  };
}
function Vr(t, e) {
  return function() {
    var n = e.apply(this, arguments);
    n == null ? delete this[t] : this[t] = n;
  };
}
function qr(t, e) {
  return arguments.length > 1 ? this.each((e == null ? Dr : typeof e == "function" ? Vr : Ur)(t, e)) : this.node()[t];
}
function Fn(t) {
  return t.trim().split(/^|\s+/);
}
function Oe(t) {
  return t.classList || new On(t);
}
function On(t) {
  this._node = t, this._names = Fn(t.getAttribute("class") || "");
}
On.prototype = {
  add: function(t) {
    var e = this._names.indexOf(t);
    e < 0 && (this._names.push(t), this._node.setAttribute("class", this._names.join(" ")));
  },
  remove: function(t) {
    var e = this._names.indexOf(t);
    e >= 0 && (this._names.splice(e, 1), this._node.setAttribute("class", this._names.join(" ")));
  },
  contains: function(t) {
    return this._names.indexOf(t) >= 0;
  }
};
function Xn(t, e) {
  for (var n = Oe(t), i = -1, r = e.length; ++i < r; ) n.add(e[i]);
}
function Bn(t, e) {
  for (var n = Oe(t), i = -1, r = e.length; ++i < r; ) n.remove(e[i]);
}
function Fr(t) {
  return function() {
    Xn(this, t);
  };
}
function Or(t) {
  return function() {
    Bn(this, t);
  };
}
function Xr(t, e) {
  return function() {
    (e.apply(this, arguments) ? Xn : Bn)(this, t);
  };
}
function Br(t, e) {
  var n = Fn(t + "");
  if (arguments.length < 2) {
    for (var i = Oe(this.node()), r = -1, s = n.length; ++r < s; ) if (!i.contains(n[r])) return !1;
    return !0;
  }
  return this.each((typeof e == "function" ? Xr : e ? Fr : Or)(n, e));
}
function Gr() {
  this.textContent = "";
}
function Yr(t) {
  return function() {
    this.textContent = t;
  };
}
function Wr(t) {
  return function() {
    var e = t.apply(this, arguments);
    this.textContent = e ?? "";
  };
}
function Kr(t) {
  return arguments.length ? this.each(t == null ? Gr : (typeof t == "function" ? Wr : Yr)(t)) : this.node().textContent;
}
function Zr() {
  this.innerHTML = "";
}
function Qr(t) {
  return function() {
    this.innerHTML = t;
  };
}
function Jr(t) {
  return function() {
    var e = t.apply(this, arguments);
    this.innerHTML = e ?? "";
  };
}
function jr(t) {
  return arguments.length ? this.each(t == null ? Zr : (typeof t == "function" ? Jr : Qr)(t)) : this.node().innerHTML;
}
function ts() {
  this.nextSibling && this.parentNode.appendChild(this);
}
function es() {
  return this.each(ts);
}
function ns() {
  this.previousSibling && this.parentNode.insertBefore(this, this.parentNode.firstChild);
}
function is() {
  return this.each(ns);
}
function rs(t) {
  var e = typeof t == "function" ? t : qe(t);
  return this.select(function() {
    return this.appendChild(e.apply(this, arguments));
  });
}
function ss() {
  return null;
}
function os(t, e) {
  var n = typeof t == "function" ? t : qe(t), i = e == null ? ss : typeof e == "function" ? e : Fe(e);
  return this.select(function() {
    return this.insertBefore(n.apply(this, arguments), i.apply(this, arguments) || null);
  });
}
function as() {
  var t = this.parentNode;
  t && t.removeChild(this);
}
function ls() {
  return this.each(as);
}
function us() {
  var t = this.cloneNode(!1), e = this.parentNode;
  return e ? e.insertBefore(t, this.nextSibling) : t;
}
function cs() {
  var t = this.cloneNode(!0), e = this.parentNode;
  return e ? e.insertBefore(t, this.nextSibling) : t;
}
function hs(t) {
  return this.select(t ? cs : us);
}
function fs(t) {
  return arguments.length ? this.property("__data__", t) : this.node().__data__;
}
function ds(t) {
  return function(e) {
    t.call(this, e, this.__data__);
  };
}
function gs(t) {
  return t.trim().split(/^|\s+/).map(function(e) {
    var n = "", i = e.indexOf(".");
    return i >= 0 && (n = e.slice(i + 1), e = e.slice(0, i)), { type: e, name: n };
  });
}
function ps(t) {
  return function() {
    var e = this.__on;
    if (e) {
      for (var n = 0, i = -1, r = e.length, s; n < r; ++n)
        s = e[n], (!t.type || s.type === t.type) && s.name === t.name ? this.removeEventListener(s.type, s.listener, s.options) : e[++i] = s;
      ++i ? e.length = i : delete this.__on;
    }
  };
}
function ms(t, e, n) {
  return function() {
    var i = this.__on, r, s = ds(e);
    if (i) {
      for (var o = 0, a = i.length; o < a; ++o)
        if ((r = i[o]).type === t.type && r.name === t.name) {
          this.removeEventListener(r.type, r.listener, r.options), this.addEventListener(r.type, r.listener = s, r.options = n), r.value = e;
          return;
        }
    }
    this.addEventListener(t.type, s, n), r = { type: t.type, name: t.name, value: e, listener: s, options: n }, i ? i.push(r) : this.__on = [r];
  };
}
function ys(t, e, n) {
  var i = gs(t + ""), r, s = i.length, o;
  if (arguments.length < 2) {
    var a = this.node().__on;
    if (a) {
      for (var u = 0, l = a.length, c; u < l; ++u)
        for (r = 0, c = a[u]; r < s; ++r)
          if ((o = i[r]).type === c.type && o.name === c.name)
            return c.value;
    }
    return;
  }
  for (a = e ? ms : ps, r = 0; r < s; ++r) this.each(a(i[r], e, n));
  return this;
}
function Gn(t, e, n) {
  var i = qn(t), r = i.CustomEvent;
  typeof r == "function" ? r = new r(e, n) : (r = i.document.createEvent("Event"), n ? (r.initEvent(e, n.bubbles, n.cancelable), r.detail = n.detail) : r.initEvent(e, !1, !1)), t.dispatchEvent(r);
}
function _s(t, e) {
  return function() {
    return Gn(this, t, e);
  };
}
function vs(t, e) {
  return function() {
    return Gn(this, t, e.apply(this, arguments));
  };
}
function xs(t, e) {
  return this.each((typeof e == "function" ? vs : _s)(t, e));
}
function* ws() {
  for (var t = this._groups, e = 0, n = t.length; e < n; ++e)
    for (var i = t[e], r = 0, s = i.length, o; r < s; ++r)
      (o = i[r]) && (yield o);
}
var Xe = [null];
function L(t, e) {
  this._groups = t, this._parents = e;
}
function Vt() {
  return new L([[document.documentElement]], Xe);
}
function bs() {
  return this;
}
L.prototype = Vt.prototype = {
  constructor: L,
  select: Ki,
  selectAll: Ji,
  selectChild: nr,
  selectChildren: or,
  filter: ar,
  data: dr,
  enter: lr,
  exit: pr,
  join: mr,
  merge: yr,
  selection: bs,
  order: _r,
  sort: vr,
  call: wr,
  nodes: br,
  node: $r,
  size: Ar,
  empty: Mr,
  each: kr,
  attr: Ir,
  style: Hr,
  property: qr,
  classed: Br,
  text: Kr,
  html: jr,
  raise: es,
  lower: is,
  append: rs,
  insert: os,
  remove: ls,
  clone: hs,
  datum: fs,
  on: ys,
  dispatch: xs,
  [Symbol.iterator]: ws
};
function W(t) {
  return typeof t == "string" ? new L([[document.querySelector(t)]], [document.documentElement]) : new L([[t]], Xe);
}
function Yn(t) {
  return W(qe(t).call(document.documentElement));
}
function $s(t) {
  let e;
  for (; e = t.sourceEvent; ) t = e;
  return t;
}
function lt(t, e) {
  if (t = $s(t), e === void 0 && (e = t.currentTarget), e) {
    var n = e.ownerSVGElement || e;
    if (n.createSVGPoint) {
      var i = n.createSVGPoint();
      return i.x = t.clientX, i.y = t.clientY, i = i.matrixTransform(e.getScreenCTM().inverse()), [i.x, i.y];
    }
    if (e.getBoundingClientRect) {
      var r = e.getBoundingClientRect();
      return [t.clientX - r.left - e.clientLeft, t.clientY - r.top - e.clientTop];
    }
  }
  return [t.pageX, t.pageY];
}
function nn(t) {
  return typeof t == "string" ? new L([document.querySelectorAll(t)], [document.documentElement]) : new L([Pn(t)], Xe);
}
const ke = { capture: !0, passive: !1 };
function Ee(t) {
  t.preventDefault(), t.stopImmediatePropagation();
}
function As(t) {
  var e = t.document.documentElement, n = W(t).on("dragstart.drag", Ee, ke);
  "onselectstart" in e ? n.on("selectstart.drag", Ee, ke) : (e.__noselect = e.style.MozUserSelect, e.style.MozUserSelect = "none");
}
function Ms(t, e) {
  var n = t.document.documentElement, i = W(t).on("dragstart.drag", null);
  e && (i.on("click.drag", Ee, ke), setTimeout(function() {
    i.on("click.drag", null);
  }, 0)), "onselectstart" in n ? i.on("selectstart.drag", null) : (n.style.MozUserSelect = n.__noselect, delete n.__noselect);
}
function Be(t, e, n) {
  t.prototype = e.prototype = n, n.constructor = t;
}
function Wn(t, e) {
  var n = Object.create(t.prototype);
  for (var i in e) n[i] = e[i];
  return n;
}
function qt() {
}
var Rt = 0.7, ne = 1 / Rt, xt = "\\s*([+-]?\\d+)\\s*", Lt = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)\\s*", K = "\\s*([+-]?(?:\\d*\\.)?\\d+(?:[eE][+-]?\\d+)?)%\\s*", ks = /^#([0-9a-f]{3,8})$/, Es = new RegExp(`^rgb\\(${xt},${xt},${xt}\\)$`), Ss = new RegExp(`^rgb\\(${K},${K},${K}\\)$`), Ns = new RegExp(`^rgba\\(${xt},${xt},${xt},${Lt}\\)$`), Ts = new RegExp(`^rgba\\(${K},${K},${K},${Lt}\\)$`), Cs = new RegExp(`^hsl\\(${Lt},${K},${K}\\)$`), zs = new RegExp(`^hsla\\(${Lt},${K},${K},${Lt}\\)$`), rn = {
  aliceblue: 15792383,
  antiquewhite: 16444375,
  aqua: 65535,
  aquamarine: 8388564,
  azure: 15794175,
  beige: 16119260,
  bisque: 16770244,
  black: 0,
  blanchedalmond: 16772045,
  blue: 255,
  blueviolet: 9055202,
  brown: 10824234,
  burlywood: 14596231,
  cadetblue: 6266528,
  chartreuse: 8388352,
  chocolate: 13789470,
  coral: 16744272,
  cornflowerblue: 6591981,
  cornsilk: 16775388,
  crimson: 14423100,
  cyan: 65535,
  darkblue: 139,
  darkcyan: 35723,
  darkgoldenrod: 12092939,
  darkgray: 11119017,
  darkgreen: 25600,
  darkgrey: 11119017,
  darkkhaki: 12433259,
  darkmagenta: 9109643,
  darkolivegreen: 5597999,
  darkorange: 16747520,
  darkorchid: 10040012,
  darkred: 9109504,
  darksalmon: 15308410,
  darkseagreen: 9419919,
  darkslateblue: 4734347,
  darkslategray: 3100495,
  darkslategrey: 3100495,
  darkturquoise: 52945,
  darkviolet: 9699539,
  deeppink: 16716947,
  deepskyblue: 49151,
  dimgray: 6908265,
  dimgrey: 6908265,
  dodgerblue: 2003199,
  firebrick: 11674146,
  floralwhite: 16775920,
  forestgreen: 2263842,
  fuchsia: 16711935,
  gainsboro: 14474460,
  ghostwhite: 16316671,
  gold: 16766720,
  goldenrod: 14329120,
  gray: 8421504,
  green: 32768,
  greenyellow: 11403055,
  grey: 8421504,
  honeydew: 15794160,
  hotpink: 16738740,
  indianred: 13458524,
  indigo: 4915330,
  ivory: 16777200,
  khaki: 15787660,
  lavender: 15132410,
  lavenderblush: 16773365,
  lawngreen: 8190976,
  lemonchiffon: 16775885,
  lightblue: 11393254,
  lightcoral: 15761536,
  lightcyan: 14745599,
  lightgoldenrodyellow: 16448210,
  lightgray: 13882323,
  lightgreen: 9498256,
  lightgrey: 13882323,
  lightpink: 16758465,
  lightsalmon: 16752762,
  lightseagreen: 2142890,
  lightskyblue: 8900346,
  lightslategray: 7833753,
  lightslategrey: 7833753,
  lightsteelblue: 11584734,
  lightyellow: 16777184,
  lime: 65280,
  limegreen: 3329330,
  linen: 16445670,
  magenta: 16711935,
  maroon: 8388608,
  mediumaquamarine: 6737322,
  mediumblue: 205,
  mediumorchid: 12211667,
  mediumpurple: 9662683,
  mediumseagreen: 3978097,
  mediumslateblue: 8087790,
  mediumspringgreen: 64154,
  mediumturquoise: 4772300,
  mediumvioletred: 13047173,
  midnightblue: 1644912,
  mintcream: 16121850,
  mistyrose: 16770273,
  moccasin: 16770229,
  navajowhite: 16768685,
  navy: 128,
  oldlace: 16643558,
  olive: 8421376,
  olivedrab: 7048739,
  orange: 16753920,
  orangered: 16729344,
  orchid: 14315734,
  palegoldenrod: 15657130,
  palegreen: 10025880,
  paleturquoise: 11529966,
  palevioletred: 14381203,
  papayawhip: 16773077,
  peachpuff: 16767673,
  peru: 13468991,
  pink: 16761035,
  plum: 14524637,
  powderblue: 11591910,
  purple: 8388736,
  rebeccapurple: 6697881,
  red: 16711680,
  rosybrown: 12357519,
  royalblue: 4286945,
  saddlebrown: 9127187,
  salmon: 16416882,
  sandybrown: 16032864,
  seagreen: 3050327,
  seashell: 16774638,
  sienna: 10506797,
  silver: 12632256,
  skyblue: 8900331,
  slateblue: 6970061,
  slategray: 7372944,
  slategrey: 7372944,
  snow: 16775930,
  springgreen: 65407,
  steelblue: 4620980,
  tan: 13808780,
  teal: 32896,
  thistle: 14204888,
  tomato: 16737095,
  turquoise: 4251856,
  violet: 15631086,
  wheat: 16113331,
  white: 16777215,
  whitesmoke: 16119285,
  yellow: 16776960,
  yellowgreen: 10145074
};
Be(qt, gt, {
  copy(t) {
    return Object.assign(new this.constructor(), this, t);
  },
  displayable() {
    return this.rgb().displayable();
  },
  hex: sn,
  // Deprecated! Use color.formatHex.
  formatHex: sn,
  formatHex8: Is,
  formatHsl: Rs,
  formatRgb: on,
  toString: on
});
function sn() {
  return this.rgb().formatHex();
}
function Is() {
  return this.rgb().formatHex8();
}
function Rs() {
  return Kn(this).formatHsl();
}
function on() {
  return this.rgb().formatRgb();
}
function gt(t) {
  var e, n;
  return t = (t + "").trim().toLowerCase(), (e = ks.exec(t)) ? (n = e[1].length, e = parseInt(e[1], 16), n === 6 ? an(e) : n === 3 ? new H(e >> 8 & 15 | e >> 4 & 240, e >> 4 & 15 | e & 240, (e & 15) << 4 | e & 15, 1) : n === 8 ? Ot(e >> 24 & 255, e >> 16 & 255, e >> 8 & 255, (e & 255) / 255) : n === 4 ? Ot(e >> 12 & 15 | e >> 8 & 240, e >> 8 & 15 | e >> 4 & 240, e >> 4 & 15 | e & 240, ((e & 15) << 4 | e & 15) / 255) : null) : (e = Es.exec(t)) ? new H(e[1], e[2], e[3], 1) : (e = Ss.exec(t)) ? new H(e[1] * 255 / 100, e[2] * 255 / 100, e[3] * 255 / 100, 1) : (e = Ns.exec(t)) ? Ot(e[1], e[2], e[3], e[4]) : (e = Ts.exec(t)) ? Ot(e[1] * 255 / 100, e[2] * 255 / 100, e[3] * 255 / 100, e[4]) : (e = Cs.exec(t)) ? cn(e[1], e[2] / 100, e[3] / 100, 1) : (e = zs.exec(t)) ? cn(e[1], e[2] / 100, e[3] / 100, e[4]) : rn.hasOwnProperty(t) ? an(rn[t]) : t === "transparent" ? new H(NaN, NaN, NaN, 0) : null;
}
function an(t) {
  return new H(t >> 16 & 255, t >> 8 & 255, t & 255, 1);
}
function Ot(t, e, n, i) {
  return i <= 0 && (t = e = n = NaN), new H(t, e, n, i);
}
function Ls(t) {
  return t instanceof qt || (t = gt(t)), t ? (t = t.rgb(), new H(t.r, t.g, t.b, t.opacity)) : new H();
}
function Se(t, e, n, i) {
  return arguments.length === 1 ? Ls(t) : new H(t, e, n, i ?? 1);
}
function H(t, e, n, i) {
  this.r = +t, this.g = +e, this.b = +n, this.opacity = +i;
}
Be(H, Se, Wn(qt, {
  brighter(t) {
    return t = t == null ? ne : Math.pow(ne, t), new H(this.r * t, this.g * t, this.b * t, this.opacity);
  },
  darker(t) {
    return t = t == null ? Rt : Math.pow(Rt, t), new H(this.r * t, this.g * t, this.b * t, this.opacity);
  },
  rgb() {
    return this;
  },
  clamp() {
    return new H(dt(this.r), dt(this.g), dt(this.b), ie(this.opacity));
  },
  displayable() {
    return -0.5 <= this.r && this.r < 255.5 && -0.5 <= this.g && this.g < 255.5 && -0.5 <= this.b && this.b < 255.5 && 0 <= this.opacity && this.opacity <= 1;
  },
  hex: ln,
  // Deprecated! Use color.formatHex.
  formatHex: ln,
  formatHex8: Ps,
  formatRgb: un,
  toString: un
}));
function ln() {
  return `#${ht(this.r)}${ht(this.g)}${ht(this.b)}`;
}
function Ps() {
  return `#${ht(this.r)}${ht(this.g)}${ht(this.b)}${ht((isNaN(this.opacity) ? 1 : this.opacity) * 255)}`;
}
function un() {
  const t = ie(this.opacity);
  return `${t === 1 ? "rgb(" : "rgba("}${dt(this.r)}, ${dt(this.g)}, ${dt(this.b)}${t === 1 ? ")" : `, ${t})`}`;
}
function ie(t) {
  return isNaN(t) ? 1 : Math.max(0, Math.min(1, t));
}
function dt(t) {
  return Math.max(0, Math.min(255, Math.round(t) || 0));
}
function ht(t) {
  return t = dt(t), (t < 16 ? "0" : "") + t.toString(16);
}
function cn(t, e, n, i) {
  return i <= 0 ? t = e = n = NaN : n <= 0 || n >= 1 ? t = e = NaN : e <= 0 && (t = NaN), new X(t, e, n, i);
}
function Kn(t) {
  if (t instanceof X) return new X(t.h, t.s, t.l, t.opacity);
  if (t instanceof qt || (t = gt(t)), !t) return new X();
  if (t instanceof X) return t;
  t = t.rgb();
  var e = t.r / 255, n = t.g / 255, i = t.b / 255, r = Math.min(e, n, i), s = Math.max(e, n, i), o = NaN, a = s - r, u = (s + r) / 2;
  return a ? (e === s ? o = (n - i) / a + (n < i) * 6 : n === s ? o = (i - e) / a + 2 : o = (e - n) / a + 4, a /= u < 0.5 ? s + r : 2 - s - r, o *= 60) : a = u > 0 && u < 1 ? 0 : o, new X(o, a, u, t.opacity);
}
function Hs(t, e, n, i) {
  return arguments.length === 1 ? Kn(t) : new X(t, e, n, i ?? 1);
}
function X(t, e, n, i) {
  this.h = +t, this.s = +e, this.l = +n, this.opacity = +i;
}
Be(X, Hs, Wn(qt, {
  brighter(t) {
    return t = t == null ? ne : Math.pow(ne, t), new X(this.h, this.s, this.l * t, this.opacity);
  },
  darker(t) {
    return t = t == null ? Rt : Math.pow(Rt, t), new X(this.h, this.s, this.l * t, this.opacity);
  },
  rgb() {
    var t = this.h % 360 + (this.h < 0) * 360, e = isNaN(t) || isNaN(this.s) ? 0 : this.s, n = this.l, i = n + (n < 0.5 ? n : 1 - n) * e, r = 2 * n - i;
    return new H(
      ye(t >= 240 ? t - 240 : t + 120, r, i),
      ye(t, r, i),
      ye(t < 120 ? t + 240 : t - 120, r, i),
      this.opacity
    );
  },
  clamp() {
    return new X(hn(this.h), Xt(this.s), Xt(this.l), ie(this.opacity));
  },
  displayable() {
    return (0 <= this.s && this.s <= 1 || isNaN(this.s)) && 0 <= this.l && this.l <= 1 && 0 <= this.opacity && this.opacity <= 1;
  },
  formatHsl() {
    const t = ie(this.opacity);
    return `${t === 1 ? "hsl(" : "hsla("}${hn(this.h)}, ${Xt(this.s) * 100}%, ${Xt(this.l) * 100}%${t === 1 ? ")" : `, ${t})`}`;
  }
}));
function hn(t) {
  return t = (t || 0) % 360, t < 0 ? t + 360 : t;
}
function Xt(t) {
  return Math.max(0, Math.min(1, t || 0));
}
function ye(t, e, n) {
  return (t < 60 ? e + (n - e) * t / 60 : t < 180 ? n : t < 240 ? e + (n - e) * (240 - t) / 60 : e) * 255;
}
const Ge = (t) => () => t;
function Ds(t, e) {
  return function(n) {
    return t + n * e;
  };
}
function Us(t, e, n) {
  return t = Math.pow(t, n), e = Math.pow(e, n) - t, n = 1 / n, function(i) {
    return Math.pow(t + i * e, n);
  };
}
function Vs(t) {
  return (t = +t) == 1 ? Zn : function(e, n) {
    return n - e ? Us(e, n, t) : Ge(isNaN(e) ? n : e);
  };
}
function Zn(t, e) {
  var n = e - t;
  return n ? Ds(t, n) : Ge(isNaN(t) ? e : t);
}
const bt = function t(e) {
  var n = Vs(e);
  function i(r, s) {
    var o = n((r = Se(r)).r, (s = Se(s)).r), a = n(r.g, s.g), u = n(r.b, s.b), l = Zn(r.opacity, s.opacity);
    return function(c) {
      return r.r = o(c), r.g = a(c), r.b = u(c), r.opacity = l(c), r + "";
    };
  }
  return i.gamma = t, i;
}(1);
function qs(t, e) {
  e || (e = []);
  var n = t ? Math.min(e.length, t.length) : 0, i = e.slice(), r;
  return function(s) {
    for (r = 0; r < n; ++r) i[r] = t[r] * (1 - s) + e[r] * s;
    return i;
  };
}
function Fs(t) {
  return ArrayBuffer.isView(t) && !(t instanceof DataView);
}
function Os(t, e) {
  var n = e ? e.length : 0, i = t ? Math.min(n, t.length) : 0, r = new Array(i), s = new Array(n), o;
  for (o = 0; o < i; ++o) r[o] = he(t[o], e[o]);
  for (; o < n; ++o) s[o] = e[o];
  return function(a) {
    for (o = 0; o < i; ++o) s[o] = r[o](a);
    return s;
  };
}
function Xs(t, e) {
  var n = /* @__PURE__ */ new Date();
  return t = +t, e = +e, function(i) {
    return n.setTime(t * (1 - i) + e * i), n;
  };
}
function O(t, e) {
  return t = +t, e = +e, function(n) {
    return t * (1 - n) + e * n;
  };
}
function Bs(t, e) {
  var n = {}, i = {}, r;
  (t === null || typeof t != "object") && (t = {}), (e === null || typeof e != "object") && (e = {});
  for (r in e)
    r in t ? n[r] = he(t[r], e[r]) : i[r] = e[r];
  return function(s) {
    for (r in n) i[r] = n[r](s);
    return i;
  };
}
var Ne = /[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?/g, _e = new RegExp(Ne.source, "g");
function Gs(t) {
  return function() {
    return t;
  };
}
function Ys(t) {
  return function(e) {
    return t(e) + "";
  };
}
function Qn(t, e) {
  var n = Ne.lastIndex = _e.lastIndex = 0, i, r, s, o = -1, a = [], u = [];
  for (t = t + "", e = e + ""; (i = Ne.exec(t)) && (r = _e.exec(e)); )
    (s = r.index) > n && (s = e.slice(n, s), a[o] ? a[o] += s : a[++o] = s), (i = i[0]) === (r = r[0]) ? a[o] ? a[o] += r : a[++o] = r : (a[++o] = null, u.push({ i: o, x: O(i, r) })), n = _e.lastIndex;
  return n < e.length && (s = e.slice(n), a[o] ? a[o] += s : a[++o] = s), a.length < 2 ? u[0] ? Ys(u[0].x) : Gs(e) : (e = u.length, function(l) {
    for (var c = 0, h; c < e; ++c) a[(h = u[c]).i] = h.x(l);
    return a.join("");
  });
}
function he(t, e) {
  var n = typeof e, i;
  return e == null || n === "boolean" ? Ge(e) : (n === "number" ? O : n === "string" ? (i = gt(e)) ? (e = i, bt) : Qn : e instanceof gt ? bt : e instanceof Date ? Xs : Fs(e) ? qs : Array.isArray(e) ? Os : typeof e.valueOf != "function" && typeof e.toString != "function" || isNaN(e) ? Bs : O)(t, e);
}
function Jn(t, e) {
  return t = +t, e = +e, function(n) {
    return Math.round(t * (1 - n) + e * n);
  };
}
var fn = 180 / Math.PI, Te = {
  translateX: 0,
  translateY: 0,
  rotate: 0,
  skewX: 0,
  scaleX: 1,
  scaleY: 1
};
function jn(t, e, n, i, r, s) {
  var o, a, u;
  return (o = Math.sqrt(t * t + e * e)) && (t /= o, e /= o), (u = t * n + e * i) && (n -= t * u, i -= e * u), (a = Math.sqrt(n * n + i * i)) && (n /= a, i /= a, u /= a), t * i < e * n && (t = -t, e = -e, u = -u, o = -o), {
    translateX: r,
    translateY: s,
    rotate: Math.atan2(e, t) * fn,
    skewX: Math.atan(u) * fn,
    scaleX: o,
    scaleY: a
  };
}
var Bt;
function Ws(t) {
  const e = new (typeof DOMMatrix == "function" ? DOMMatrix : WebKitCSSMatrix)(t + "");
  return e.isIdentity ? Te : jn(e.a, e.b, e.c, e.d, e.e, e.f);
}
function Ks(t) {
  return t == null || (Bt || (Bt = document.createElementNS("http://www.w3.org/2000/svg", "g")), Bt.setAttribute("transform", t), !(t = Bt.transform.baseVal.consolidate())) ? Te : (t = t.matrix, jn(t.a, t.b, t.c, t.d, t.e, t.f));
}
function ti(t, e, n, i) {
  function r(l) {
    return l.length ? l.pop() + " " : "";
  }
  function s(l, c, h, d, g, m) {
    if (l !== h || c !== d) {
      var x = g.push("translate(", null, e, null, n);
      m.push({ i: x - 4, x: O(l, h) }, { i: x - 2, x: O(c, d) });
    } else (h || d) && g.push("translate(" + h + e + d + n);
  }
  function o(l, c, h, d) {
    l !== c ? (l - c > 180 ? c += 360 : c - l > 180 && (l += 360), d.push({ i: h.push(r(h) + "rotate(", null, i) - 2, x: O(l, c) })) : c && h.push(r(h) + "rotate(" + c + i);
  }
  function a(l, c, h, d) {
    l !== c ? d.push({ i: h.push(r(h) + "skewX(", null, i) - 2, x: O(l, c) }) : c && h.push(r(h) + "skewX(" + c + i);
  }
  function u(l, c, h, d, g, m) {
    if (l !== h || c !== d) {
      var x = g.push(r(g) + "scale(", null, ",", null, ")");
      m.push({ i: x - 4, x: O(l, h) }, { i: x - 2, x: O(c, d) });
    } else (h !== 1 || d !== 1) && g.push(r(g) + "scale(" + h + "," + d + ")");
  }
  return function(l, c) {
    var h = [], d = [];
    return l = t(l), c = t(c), s(l.translateX, l.translateY, c.translateX, c.translateY, h, d), o(l.rotate, c.rotate, h, d), a(l.skewX, c.skewX, h, d), u(l.scaleX, l.scaleY, c.scaleX, c.scaleY, h, d), l = c = null, function(g) {
      for (var m = -1, x = d.length, M; ++m < x; ) h[(M = d[m]).i] = M.x(g);
      return h.join("");
    };
  };
}
var Zs = ti(Ws, "px, ", "px)", "deg)"), Qs = ti(Ks, ", ", ")", ")"), Js = 1e-12;
function dn(t) {
  return ((t = Math.exp(t)) + 1 / t) / 2;
}
function js(t) {
  return ((t = Math.exp(t)) - 1 / t) / 2;
}
function to(t) {
  return ((t = Math.exp(2 * t)) - 1) / (t + 1);
}
const eo = function t(e, n, i) {
  function r(s, o) {
    var a = s[0], u = s[1], l = s[2], c = o[0], h = o[1], d = o[2], g = c - a, m = h - u, x = g * g + m * m, M, v;
    if (x < Js)
      v = Math.log(d / l) / e, M = function(G) {
        return [
          a + G * g,
          u + G * m,
          l * Math.exp(e * G * v)
        ];
      };
    else {
      var N = Math.sqrt(x), S = (d * d - l * l + i * x) / (2 * l * n * N), I = (d * d - l * l - i * x) / (2 * d * n * N), k = Math.log(Math.sqrt(S * S + 1) - S), D = Math.log(Math.sqrt(I * I + 1) - I);
      v = (D - k) / e, M = function(G) {
        var ot = G * v, _t = dn(k), at = l / (n * N) * (_t * to(e * ot + k) - js(k));
        return [
          a + at * g,
          u + at * m,
          l * _t / dn(e * ot + k)
        ];
      };
    }
    return M.duration = v * 1e3 * e / Math.SQRT2, M;
  }
  return r.rho = function(s) {
    var o = Math.max(1e-3, +s), a = o * o, u = a * a;
    return t(o, a, u);
  }, r;
}(Math.SQRT2, 2, 4);
var $t = 0, Ct = 0, St = 0, ei = 1e3, re, zt, se = 0, pt = 0, fe = 0, Pt = typeof performance == "object" && performance.now ? performance : Date, ni = typeof window == "object" && window.requestAnimationFrame ? window.requestAnimationFrame.bind(window) : function(t) {
  setTimeout(t, 17);
};
function Ye() {
  return pt || (ni(no), pt = Pt.now() + fe);
}
function no() {
  pt = 0;
}
function oe() {
  this._call = this._time = this._next = null;
}
oe.prototype = ii.prototype = {
  constructor: oe,
  restart: function(t, e, n) {
    if (typeof t != "function") throw new TypeError("callback is not a function");
    n = (n == null ? Ye() : +n) + (e == null ? 0 : +e), !this._next && zt !== this && (zt ? zt._next = this : re = this, zt = this), this._call = t, this._time = n, Ce();
  },
  stop: function() {
    this._call && (this._call = null, this._time = 1 / 0, Ce());
  }
};
function ii(t, e, n) {
  var i = new oe();
  return i.restart(t, e, n), i;
}
function io() {
  Ye(), ++$t;
  for (var t = re, e; t; )
    (e = pt - t._time) >= 0 && t._call.call(void 0, e), t = t._next;
  --$t;
}
function gn() {
  pt = (se = Pt.now()) + fe, $t = Ct = 0;
  try {
    io();
  } finally {
    $t = 0, so(), pt = 0;
  }
}
function ro() {
  var t = Pt.now(), e = t - se;
  e > ei && (fe -= e, se = t);
}
function so() {
  for (var t, e = re, n, i = 1 / 0; e; )
    e._call ? (i > e._time && (i = e._time), t = e, e = e._next) : (n = e._next, e._next = null, e = t ? t._next = n : re = n);
  zt = t, Ce(i);
}
function Ce(t) {
  if (!$t) {
    Ct && (Ct = clearTimeout(Ct));
    var e = t - pt;
    e > 24 ? (t < 1 / 0 && (Ct = setTimeout(gn, t - Pt.now() - fe)), St && (St = clearInterval(St))) : (St || (se = Pt.now(), St = setInterval(ro, ei)), $t = 1, ni(gn));
  }
}
function pn(t, e, n) {
  var i = new oe();
  return e = e == null ? 0 : +e, i.restart((r) => {
    i.stop(), t(r + e);
  }, e, n), i;
}
var oo = Ve("start", "end", "cancel", "interrupt"), ao = [], ri = 0, mn = 1, ze = 2, Qt = 3, yn = 4, Ie = 5, Jt = 6;
function de(t, e, n, i, r, s) {
  var o = t.__transition;
  if (!o) t.__transition = {};
  else if (n in o) return;
  lo(t, n, {
    name: e,
    index: i,
    // For context during callback.
    group: r,
    // For context during callback.
    on: oo,
    tween: ao,
    time: s.time,
    delay: s.delay,
    duration: s.duration,
    ease: s.ease,
    timer: null,
    state: ri
  });
}
function We(t, e) {
  var n = B(t, e);
  if (n.state > ri) throw new Error("too late; already scheduled");
  return n;
}
function Q(t, e) {
  var n = B(t, e);
  if (n.state > Qt) throw new Error("too late; already running");
  return n;
}
function B(t, e) {
  var n = t.__transition;
  if (!n || !(n = n[e])) throw new Error("transition not found");
  return n;
}
function lo(t, e, n) {
  var i = t.__transition, r;
  i[e] = n, n.timer = ii(s, 0, n.time);
  function s(l) {
    n.state = mn, n.timer.restart(o, n.delay, n.time), n.delay <= l && o(l - n.delay);
  }
  function o(l) {
    var c, h, d, g;
    if (n.state !== mn) return u();
    for (c in i)
      if (g = i[c], g.name === n.name) {
        if (g.state === Qt) return pn(o);
        g.state === yn ? (g.state = Jt, g.timer.stop(), g.on.call("interrupt", t, t.__data__, g.index, g.group), delete i[c]) : +c < e && (g.state = Jt, g.timer.stop(), g.on.call("cancel", t, t.__data__, g.index, g.group), delete i[c]);
      }
    if (pn(function() {
      n.state === Qt && (n.state = yn, n.timer.restart(a, n.delay, n.time), a(l));
    }), n.state = ze, n.on.call("start", t, t.__data__, n.index, n.group), n.state === ze) {
      for (n.state = Qt, r = new Array(d = n.tween.length), c = 0, h = -1; c < d; ++c)
        (g = n.tween[c].value.call(t, t.__data__, n.index, n.group)) && (r[++h] = g);
      r.length = h + 1;
    }
  }
  function a(l) {
    for (var c = l < n.duration ? n.ease.call(null, l / n.duration) : (n.timer.restart(u), n.state = Ie, 1), h = -1, d = r.length; ++h < d; )
      r[h].call(t, c);
    n.state === Ie && (n.on.call("end", t, t.__data__, n.index, n.group), u());
  }
  function u() {
    n.state = Jt, n.timer.stop(), delete i[e];
    for (var l in i) return;
    delete t.__transition;
  }
}
function jt(t, e) {
  var n = t.__transition, i, r, s = !0, o;
  if (n) {
    e = e == null ? null : e + "";
    for (o in n) {
      if ((i = n[o]).name !== e) {
        s = !1;
        continue;
      }
      r = i.state > ze && i.state < Ie, i.state = Jt, i.timer.stop(), i.on.call(r ? "interrupt" : "cancel", t, t.__data__, i.index, i.group), delete n[o];
    }
    s && delete t.__transition;
  }
}
function uo(t) {
  return this.each(function() {
    jt(this, t);
  });
}
function co(t, e) {
  var n, i;
  return function() {
    var r = Q(this, t), s = r.tween;
    if (s !== n) {
      i = n = s;
      for (var o = 0, a = i.length; o < a; ++o)
        if (i[o].name === e) {
          i = i.slice(), i.splice(o, 1);
          break;
        }
    }
    r.tween = i;
  };
}
function ho(t, e, n) {
  var i, r;
  if (typeof n != "function") throw new Error();
  return function() {
    var s = Q(this, t), o = s.tween;
    if (o !== i) {
      r = (i = o).slice();
      for (var a = { name: e, value: n }, u = 0, l = r.length; u < l; ++u)
        if (r[u].name === e) {
          r[u] = a;
          break;
        }
      u === l && r.push(a);
    }
    s.tween = r;
  };
}
function fo(t, e) {
  var n = this._id;
  if (t += "", arguments.length < 2) {
    for (var i = B(this.node(), n).tween, r = 0, s = i.length, o; r < s; ++r)
      if ((o = i[r]).name === t)
        return o.value;
    return null;
  }
  return this.each((e == null ? co : ho)(n, t, e));
}
function Ke(t, e, n) {
  var i = t._id;
  return t.each(function() {
    var r = Q(this, i);
    (r.value || (r.value = {}))[e] = n.apply(this, arguments);
  }), function(r) {
    return B(r, i).value[e];
  };
}
function si(t, e) {
  var n;
  return (typeof e == "number" ? O : e instanceof gt ? bt : (n = gt(e)) ? (e = n, bt) : Qn)(t, e);
}
function go(t) {
  return function() {
    this.removeAttribute(t);
  };
}
function po(t) {
  return function() {
    this.removeAttributeNS(t.space, t.local);
  };
}
function mo(t, e, n) {
  var i, r = n + "", s;
  return function() {
    var o = this.getAttribute(t);
    return o === r ? null : o === i ? s : s = e(i = o, n);
  };
}
function yo(t, e, n) {
  var i, r = n + "", s;
  return function() {
    var o = this.getAttributeNS(t.space, t.local);
    return o === r ? null : o === i ? s : s = e(i = o, n);
  };
}
function _o(t, e, n) {
  var i, r, s;
  return function() {
    var o, a = n(this), u;
    return a == null ? void this.removeAttribute(t) : (o = this.getAttribute(t), u = a + "", o === u ? null : o === i && u === r ? s : (r = u, s = e(i = o, a)));
  };
}
function vo(t, e, n) {
  var i, r, s;
  return function() {
    var o, a = n(this), u;
    return a == null ? void this.removeAttributeNS(t.space, t.local) : (o = this.getAttributeNS(t.space, t.local), u = a + "", o === u ? null : o === i && u === r ? s : (r = u, s = e(i = o, a)));
  };
}
function xo(t, e) {
  var n = ce(t), i = n === "transform" ? Qs : si;
  return this.attrTween(t, typeof e == "function" ? (n.local ? vo : _o)(n, i, Ke(this, "attr." + t, e)) : e == null ? (n.local ? po : go)(n) : (n.local ? yo : mo)(n, i, e));
}
function wo(t, e) {
  return function(n) {
    this.setAttribute(t, e.call(this, n));
  };
}
function bo(t, e) {
  return function(n) {
    this.setAttributeNS(t.space, t.local, e.call(this, n));
  };
}
function $o(t, e) {
  var n, i;
  function r() {
    var s = e.apply(this, arguments);
    return s !== i && (n = (i = s) && bo(t, s)), n;
  }
  return r._value = e, r;
}
function Ao(t, e) {
  var n, i;
  function r() {
    var s = e.apply(this, arguments);
    return s !== i && (n = (i = s) && wo(t, s)), n;
  }
  return r._value = e, r;
}
function Mo(t, e) {
  var n = "attr." + t;
  if (arguments.length < 2) return (n = this.tween(n)) && n._value;
  if (e == null) return this.tween(n, null);
  if (typeof e != "function") throw new Error();
  var i = ce(t);
  return this.tween(n, (i.local ? $o : Ao)(i, e));
}
function ko(t, e) {
  return function() {
    We(this, t).delay = +e.apply(this, arguments);
  };
}
function Eo(t, e) {
  return e = +e, function() {
    We(this, t).delay = e;
  };
}
function So(t) {
  var e = this._id;
  return arguments.length ? this.each((typeof t == "function" ? ko : Eo)(e, t)) : B(this.node(), e).delay;
}
function No(t, e) {
  return function() {
    Q(this, t).duration = +e.apply(this, arguments);
  };
}
function To(t, e) {
  return e = +e, function() {
    Q(this, t).duration = e;
  };
}
function Co(t) {
  var e = this._id;
  return arguments.length ? this.each((typeof t == "function" ? No : To)(e, t)) : B(this.node(), e).duration;
}
function zo(t, e) {
  if (typeof e != "function") throw new Error();
  return function() {
    Q(this, t).ease = e;
  };
}
function Io(t) {
  var e = this._id;
  return arguments.length ? this.each(zo(e, t)) : B(this.node(), e).ease;
}
function Ro(t, e) {
  return function() {
    var n = e.apply(this, arguments);
    if (typeof n != "function") throw new Error();
    Q(this, t).ease = n;
  };
}
function Lo(t) {
  if (typeof t != "function") throw new Error();
  return this.each(Ro(this._id, t));
}
function Po(t) {
  typeof t != "function" && (t = Dn(t));
  for (var e = this._groups, n = e.length, i = new Array(n), r = 0; r < n; ++r)
    for (var s = e[r], o = s.length, a = i[r] = [], u, l = 0; l < o; ++l)
      (u = s[l]) && t.call(u, u.__data__, l, s) && a.push(u);
  return new it(i, this._parents, this._name, this._id);
}
function Ho(t) {
  if (t._id !== this._id) throw new Error();
  for (var e = this._groups, n = t._groups, i = e.length, r = n.length, s = Math.min(i, r), o = new Array(i), a = 0; a < s; ++a)
    for (var u = e[a], l = n[a], c = u.length, h = o[a] = new Array(c), d, g = 0; g < c; ++g)
      (d = u[g] || l[g]) && (h[g] = d);
  for (; a < i; ++a)
    o[a] = e[a];
  return new it(o, this._parents, this._name, this._id);
}
function Do(t) {
  return (t + "").trim().split(/^|\s+/).every(function(e) {
    var n = e.indexOf(".");
    return n >= 0 && (e = e.slice(0, n)), !e || e === "start";
  });
}
function Uo(t, e, n) {
  var i, r, s = Do(e) ? We : Q;
  return function() {
    var o = s(this, t), a = o.on;
    a !== i && (r = (i = a).copy()).on(e, n), o.on = r;
  };
}
function Vo(t, e) {
  var n = this._id;
  return arguments.length < 2 ? B(this.node(), n).on.on(t) : this.each(Uo(n, t, e));
}
function qo(t) {
  return function() {
    var e = this.parentNode;
    for (var n in this.__transition) if (+n !== t) return;
    e && e.removeChild(this);
  };
}
function Fo() {
  return this.on("end.remove", qo(this._id));
}
function Oo(t) {
  var e = this._name, n = this._id;
  typeof t != "function" && (t = Fe(t));
  for (var i = this._groups, r = i.length, s = new Array(r), o = 0; o < r; ++o)
    for (var a = i[o], u = a.length, l = s[o] = new Array(u), c, h, d = 0; d < u; ++d)
      (c = a[d]) && (h = t.call(c, c.__data__, d, a)) && ("__data__" in c && (h.__data__ = c.__data__), l[d] = h, de(l[d], e, n, d, l, B(c, n)));
  return new it(s, this._parents, e, n);
}
function Xo(t) {
  var e = this._name, n = this._id;
  typeof t != "function" && (t = Hn(t));
  for (var i = this._groups, r = i.length, s = [], o = [], a = 0; a < r; ++a)
    for (var u = i[a], l = u.length, c, h = 0; h < l; ++h)
      if (c = u[h]) {
        for (var d = t.call(c, c.__data__, h, u), g, m = B(c, n), x = 0, M = d.length; x < M; ++x)
          (g = d[x]) && de(g, e, n, x, d, m);
        s.push(d), o.push(c);
      }
  return new it(s, o, e, n);
}
var Bo = Vt.prototype.constructor;
function Go() {
  return new Bo(this._groups, this._parents);
}
function Yo(t, e) {
  var n, i, r;
  return function() {
    var s = wt(this, t), o = (this.style.removeProperty(t), wt(this, t));
    return s === o ? null : s === n && o === i ? r : r = e(n = s, i = o);
  };
}
function oi(t) {
  return function() {
    this.style.removeProperty(t);
  };
}
function Wo(t, e, n) {
  var i, r = n + "", s;
  return function() {
    var o = wt(this, t);
    return o === r ? null : o === i ? s : s = e(i = o, n);
  };
}
function Ko(t, e, n) {
  var i, r, s;
  return function() {
    var o = wt(this, t), a = n(this), u = a + "";
    return a == null && (u = a = (this.style.removeProperty(t), wt(this, t))), o === u ? null : o === i && u === r ? s : (r = u, s = e(i = o, a));
  };
}
function Zo(t, e) {
  var n, i, r, s = "style." + e, o = "end." + s, a;
  return function() {
    var u = Q(this, t), l = u.on, c = u.value[s] == null ? a || (a = oi(e)) : void 0;
    (l !== n || r !== c) && (i = (n = l).copy()).on(o, r = c), u.on = i;
  };
}
function Qo(t, e, n) {
  var i = (t += "") == "transform" ? Zs : si;
  return e == null ? this.styleTween(t, Yo(t, i)).on("end.style." + t, oi(t)) : typeof e == "function" ? this.styleTween(t, Ko(t, i, Ke(this, "style." + t, e))).each(Zo(this._id, t)) : this.styleTween(t, Wo(t, i, e), n).on("end.style." + t, null);
}
function Jo(t, e, n) {
  return function(i) {
    this.style.setProperty(t, e.call(this, i), n);
  };
}
function jo(t, e, n) {
  var i, r;
  function s() {
    var o = e.apply(this, arguments);
    return o !== r && (i = (r = o) && Jo(t, o, n)), i;
  }
  return s._value = e, s;
}
function ta(t, e, n) {
  var i = "style." + (t += "");
  if (arguments.length < 2) return (i = this.tween(i)) && i._value;
  if (e == null) return this.tween(i, null);
  if (typeof e != "function") throw new Error();
  return this.tween(i, jo(t, e, n ?? ""));
}
function ea(t) {
  return function() {
    this.textContent = t;
  };
}
function na(t) {
  return function() {
    var e = t(this);
    this.textContent = e ?? "";
  };
}
function ia(t) {
  return this.tween("text", typeof t == "function" ? na(Ke(this, "text", t)) : ea(t == null ? "" : t + ""));
}
function ra(t) {
  return function(e) {
    this.textContent = t.call(this, e);
  };
}
function sa(t) {
  var e, n;
  function i() {
    var r = t.apply(this, arguments);
    return r !== n && (e = (n = r) && ra(r)), e;
  }
  return i._value = t, i;
}
function oa(t) {
  var e = "text";
  if (arguments.length < 1) return (e = this.tween(e)) && e._value;
  if (t == null) return this.tween(e, null);
  if (typeof t != "function") throw new Error();
  return this.tween(e, sa(t));
}
function aa() {
  for (var t = this._name, e = this._id, n = ai(), i = this._groups, r = i.length, s = 0; s < r; ++s)
    for (var o = i[s], a = o.length, u, l = 0; l < a; ++l)
      if (u = o[l]) {
        var c = B(u, e);
        de(u, t, n, l, o, {
          time: c.time + c.delay + c.duration,
          delay: 0,
          duration: c.duration,
          ease: c.ease
        });
      }
  return new it(i, this._parents, t, n);
}
function la() {
  var t, e, n = this, i = n._id, r = n.size();
  return new Promise(function(s, o) {
    var a = { value: o }, u = { value: function() {
      --r === 0 && s();
    } };
    n.each(function() {
      var l = Q(this, i), c = l.on;
      c !== t && (e = (t = c).copy(), e._.cancel.push(a), e._.interrupt.push(a), e._.end.push(u)), l.on = e;
    }), r === 0 && s();
  });
}
var ua = 0;
function it(t, e, n, i) {
  this._groups = t, this._parents = e, this._name = n, this._id = i;
}
function ai() {
  return ++ua;
}
var et = Vt.prototype;
it.prototype = {
  constructor: it,
  select: Oo,
  selectAll: Xo,
  selectChild: et.selectChild,
  selectChildren: et.selectChildren,
  filter: Po,
  merge: Ho,
  selection: Go,
  transition: aa,
  call: et.call,
  nodes: et.nodes,
  node: et.node,
  size: et.size,
  empty: et.empty,
  each: et.each,
  on: Vo,
  attr: xo,
  attrTween: Mo,
  style: Qo,
  styleTween: ta,
  text: ia,
  textTween: oa,
  remove: Fo,
  tween: fo,
  delay: So,
  duration: Co,
  ease: Io,
  easeVarying: Lo,
  end: la,
  [Symbol.iterator]: et[Symbol.iterator]
};
function ca(t) {
  return ((t *= 2) <= 1 ? t * t * t : (t -= 2) * t * t + 2) / 2;
}
var ha = {
  time: null,
  // Set on use.
  delay: 0,
  duration: 250,
  ease: ca
};
function fa(t, e) {
  for (var n; !(n = t.__transition) || !(n = n[e]); )
    if (!(t = t.parentNode))
      throw new Error(`transition ${e} not found`);
  return n;
}
function da(t) {
  var e, n;
  t instanceof it ? (e = t._id, t = t._name) : (e = ai(), (n = ha).time = Ye(), t = t == null ? null : t + "");
  for (var i = this._groups, r = i.length, s = 0; s < r; ++s)
    for (var o = i[s], a = o.length, u, l = 0; l < a; ++l)
      (u = o[l]) && de(u, t, e, l, o, n || fa(u, e));
  return new it(i, this._parents, t, e);
}
Vt.prototype.interrupt = uo;
Vt.prototype.transition = da;
const Re = Math.PI, Le = 2 * Re, ct = 1e-6, ga = Le - ct;
function li(t) {
  this._ += t[0];
  for (let e = 1, n = t.length; e < n; ++e)
    this._ += arguments[e] + t[e];
}
function pa(t) {
  let e = Math.floor(t);
  if (!(e >= 0)) throw new Error(`invalid digits: ${t}`);
  if (e > 15) return li;
  const n = 10 ** e;
  return function(i) {
    this._ += i[0];
    for (let r = 1, s = i.length; r < s; ++r)
      this._ += Math.round(arguments[r] * n) / n + i[r];
  };
}
class ma {
  constructor(e) {
    this._x0 = this._y0 = // start of current subpath
    this._x1 = this._y1 = null, this._ = "", this._append = e == null ? li : pa(e);
  }
  moveTo(e, n) {
    this._append`M${this._x0 = this._x1 = +e},${this._y0 = this._y1 = +n}`;
  }
  closePath() {
    this._x1 !== null && (this._x1 = this._x0, this._y1 = this._y0, this._append`Z`);
  }
  lineTo(e, n) {
    this._append`L${this._x1 = +e},${this._y1 = +n}`;
  }
  quadraticCurveTo(e, n, i, r) {
    this._append`Q${+e},${+n},${this._x1 = +i},${this._y1 = +r}`;
  }
  bezierCurveTo(e, n, i, r, s, o) {
    this._append`C${+e},${+n},${+i},${+r},${this._x1 = +s},${this._y1 = +o}`;
  }
  arcTo(e, n, i, r, s) {
    if (e = +e, n = +n, i = +i, r = +r, s = +s, s < 0) throw new Error(`negative radius: ${s}`);
    let o = this._x1, a = this._y1, u = i - e, l = r - n, c = o - e, h = a - n, d = c * c + h * h;
    if (this._x1 === null)
      this._append`M${this._x1 = e},${this._y1 = n}`;
    else if (d > ct) if (!(Math.abs(h * u - l * c) > ct) || !s)
      this._append`L${this._x1 = e},${this._y1 = n}`;
    else {
      let g = i - o, m = r - a, x = u * u + l * l, M = g * g + m * m, v = Math.sqrt(x), N = Math.sqrt(d), S = s * Math.tan((Re - Math.acos((x + d - M) / (2 * v * N))) / 2), I = S / N, k = S / v;
      Math.abs(I - 1) > ct && this._append`L${e + I * c},${n + I * h}`, this._append`A${s},${s},0,0,${+(h * g > c * m)},${this._x1 = e + k * u},${this._y1 = n + k * l}`;
    }
  }
  arc(e, n, i, r, s, o) {
    if (e = +e, n = +n, i = +i, o = !!o, i < 0) throw new Error(`negative radius: ${i}`);
    let a = i * Math.cos(r), u = i * Math.sin(r), l = e + a, c = n + u, h = 1 ^ o, d = o ? r - s : s - r;
    this._x1 === null ? this._append`M${l},${c}` : (Math.abs(this._x1 - l) > ct || Math.abs(this._y1 - c) > ct) && this._append`L${l},${c}`, i && (d < 0 && (d = d % Le + Le), d > ga ? this._append`A${i},${i},0,1,${h},${e - a},${n - u}A${i},${i},0,1,${h},${this._x1 = l},${this._y1 = c}` : d > ct && this._append`A${i},${i},0,${+(d >= Re)},${h},${this._x1 = e + i * Math.cos(s)},${this._y1 = n + i * Math.sin(s)}`);
  }
  rect(e, n, i, r) {
    this._append`M${this._x0 = this._x1 = +e},${this._y0 = this._y1 = +n}h${i = +i}v${+r}h${-i}Z`;
  }
  toString() {
    return this._;
  }
}
function ya(t) {
  return Math.abs(t = Math.round(t)) >= 1e21 ? t.toLocaleString("en").replace(/,/g, "") : t.toString(10);
}
function ae(t, e) {
  if ((n = (t = e ? t.toExponential(e - 1) : t.toExponential()).indexOf("e")) < 0) return null;
  var n, i = t.slice(0, n);
  return [
    i.length > 1 ? i[0] + i.slice(2) : i,
    +t.slice(n + 1)
  ];
}
function At(t) {
  return t = ae(Math.abs(t)), t ? t[1] : NaN;
}
function _a(t, e) {
  return function(n, i) {
    for (var r = n.length, s = [], o = 0, a = t[0], u = 0; r > 0 && a > 0 && (u + a + 1 > i && (a = Math.max(1, i - u)), s.push(n.substring(r -= a, r + a)), !((u += a + 1) > i)); )
      a = t[o = (o + 1) % t.length];
    return s.reverse().join(e);
  };
}
function va(t) {
  return function(e) {
    return e.replace(/[0-9]/g, function(n) {
      return t[+n];
    });
  };
}
var xa = /^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$/i;
function le(t) {
  if (!(e = xa.exec(t))) throw new Error("invalid format: " + t);
  var e;
  return new Ze({
    fill: e[1],
    align: e[2],
    sign: e[3],
    symbol: e[4],
    zero: e[5],
    width: e[6],
    comma: e[7],
    precision: e[8] && e[8].slice(1),
    trim: e[9],
    type: e[10]
  });
}
le.prototype = Ze.prototype;
function Ze(t) {
  this.fill = t.fill === void 0 ? " " : t.fill + "", this.align = t.align === void 0 ? ">" : t.align + "", this.sign = t.sign === void 0 ? "-" : t.sign + "", this.symbol = t.symbol === void 0 ? "" : t.symbol + "", this.zero = !!t.zero, this.width = t.width === void 0 ? void 0 : +t.width, this.comma = !!t.comma, this.precision = t.precision === void 0 ? void 0 : +t.precision, this.trim = !!t.trim, this.type = t.type === void 0 ? "" : t.type + "";
}
Ze.prototype.toString = function() {
  return this.fill + this.align + this.sign + this.symbol + (this.zero ? "0" : "") + (this.width === void 0 ? "" : Math.max(1, this.width | 0)) + (this.comma ? "," : "") + (this.precision === void 0 ? "" : "." + Math.max(0, this.precision | 0)) + (this.trim ? "~" : "") + this.type;
};
function wa(t) {
  t: for (var e = t.length, n = 1, i = -1, r; n < e; ++n)
    switch (t[n]) {
      case ".":
        i = r = n;
        break;
      case "0":
        i === 0 && (i = n), r = n;
        break;
      default:
        if (!+t[n]) break t;
        i > 0 && (i = 0);
        break;
    }
  return i > 0 ? t.slice(0, i) + t.slice(r + 1) : t;
}
var ui;
function ba(t, e) {
  var n = ae(t, e);
  if (!n) return t + "";
  var i = n[0], r = n[1], s = r - (ui = Math.max(-8, Math.min(8, Math.floor(r / 3))) * 3) + 1, o = i.length;
  return s === o ? i : s > o ? i + new Array(s - o + 1).join("0") : s > 0 ? i.slice(0, s) + "." + i.slice(s) : "0." + new Array(1 - s).join("0") + ae(t, Math.max(0, e + s - 1))[0];
}
function _n(t, e) {
  var n = ae(t, e);
  if (!n) return t + "";
  var i = n[0], r = n[1];
  return r < 0 ? "0." + new Array(-r).join("0") + i : i.length > r + 1 ? i.slice(0, r + 1) + "." + i.slice(r + 1) : i + new Array(r - i.length + 2).join("0");
}
const vn = {
  "%": (t, e) => (t * 100).toFixed(e),
  b: (t) => Math.round(t).toString(2),
  c: (t) => t + "",
  d: ya,
  e: (t, e) => t.toExponential(e),
  f: (t, e) => t.toFixed(e),
  g: (t, e) => t.toPrecision(e),
  o: (t) => Math.round(t).toString(8),
  p: (t, e) => _n(t * 100, e),
  r: _n,
  s: ba,
  X: (t) => Math.round(t).toString(16).toUpperCase(),
  x: (t) => Math.round(t).toString(16)
};
function xn(t) {
  return t;
}
var wn = Array.prototype.map, bn = ["y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"];
function $a(t) {
  var e = t.grouping === void 0 || t.thousands === void 0 ? xn : _a(wn.call(t.grouping, Number), t.thousands + ""), n = t.currency === void 0 ? "" : t.currency[0] + "", i = t.currency === void 0 ? "" : t.currency[1] + "", r = t.decimal === void 0 ? "." : t.decimal + "", s = t.numerals === void 0 ? xn : va(wn.call(t.numerals, String)), o = t.percent === void 0 ? "%" : t.percent + "", a = t.minus === void 0 ? "−" : t.minus + "", u = t.nan === void 0 ? "NaN" : t.nan + "";
  function l(h) {
    h = le(h);
    var d = h.fill, g = h.align, m = h.sign, x = h.symbol, M = h.zero, v = h.width, N = h.comma, S = h.precision, I = h.trim, k = h.type;
    k === "n" ? (N = !0, k = "g") : vn[k] || (S === void 0 && (S = 12), I = !0, k = "g"), (M || d === "0" && g === "=") && (M = !0, d = "0", g = "=");
    var D = x === "$" ? n : x === "#" && /[boxX]/.test(k) ? "0" + k.toLowerCase() : "", G = x === "$" ? i : /[%p]/.test(k) ? o : "", ot = vn[k], _t = /[defgprs%]/.test(k);
    S = S === void 0 ? 6 : /[gprs]/.test(k) ? Math.max(1, Math.min(21, S)) : Math.max(0, Math.min(20, S));
    function at(A) {
      var J = D, P = G, f, y, p;
      if (k === "c")
        P = ot(A) + P, A = "";
      else {
        A = +A;
        var _ = A < 0 || 1 / A < 0;
        if (A = isNaN(A) ? u : ot(Math.abs(A), S), I && (A = wa(A)), _ && +A == 0 && m !== "+" && (_ = !1), J = (_ ? m === "(" ? m : a : m === "-" || m === "(" ? "" : m) + J, P = (k === "s" ? bn[8 + ui / 3] : "") + P + (_ && m === "(" ? ")" : ""), _t) {
          for (f = -1, y = A.length; ++f < y; )
            if (p = A.charCodeAt(f), 48 > p || p > 57) {
              P = (p === 46 ? r + A.slice(f + 1) : A.slice(f)) + P, A = A.slice(0, f);
              break;
            }
        }
      }
      N && !M && (A = e(A, 1 / 0));
      var b = J.length + A.length + P.length, w = b < v ? new Array(v - b + 1).join(d) : "";
      switch (N && M && (A = e(w + A, w.length ? v - P.length : 1 / 0), w = ""), g) {
        case "<":
          A = J + A + P + w;
          break;
        case "=":
          A = J + w + A + P;
          break;
        case "^":
          A = w.slice(0, b = w.length >> 1) + J + A + P + w.slice(b);
          break;
        default:
          A = w + J + A + P;
          break;
      }
      return s(A);
    }
    return at.toString = function() {
      return h + "";
    }, at;
  }
  function c(h, d) {
    var g = l((h = le(h), h.type = "f", h)), m = Math.max(-8, Math.min(8, Math.floor(At(d) / 3))) * 3, x = Math.pow(10, -m), M = bn[8 + m / 3];
    return function(v) {
      return g(x * v) + M;
    };
  }
  return {
    format: l,
    formatPrefix: c
  };
}
var Gt, ci, hi;
Aa({
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});
function Aa(t) {
  return Gt = $a(t), ci = Gt.format, hi = Gt.formatPrefix, Gt;
}
function Ma(t) {
  return Math.max(0, -At(Math.abs(t)));
}
function ka(t, e) {
  return Math.max(0, Math.max(-8, Math.min(8, Math.floor(At(e) / 3))) * 3 - At(Math.abs(t)));
}
function Ea(t, e) {
  return t = Math.abs(t), e = Math.abs(e) - t, Math.max(0, At(e) - At(t)) + 1;
}
function fi(t, e) {
  switch (arguments.length) {
    case 0:
      break;
    case 1:
      this.range(t);
      break;
    default:
      this.range(e).domain(t);
      break;
  }
  return this;
}
function Sa(t, e) {
  switch (arguments.length) {
    case 0:
      break;
    case 1: {
      typeof t == "function" ? this.interpolator(t) : this.range(t);
      break;
    }
    default: {
      this.domain(t), typeof e == "function" ? this.interpolator(e) : this.range(e);
      break;
    }
  }
  return this;
}
const $n = Symbol("implicit");
function di() {
  var t = new Je(), e = [], n = [], i = $n;
  function r(s) {
    let o = t.get(s);
    if (o === void 0) {
      if (i !== $n) return i;
      t.set(s, o = e.push(s) - 1);
    }
    return n[o % n.length];
  }
  return r.domain = function(s) {
    if (!arguments.length) return e.slice();
    e = [], t = new Je();
    for (const o of s)
      t.has(o) || t.set(o, e.push(o) - 1);
    return r;
  }, r.range = function(s) {
    return arguments.length ? (n = Array.from(s), r) : n.slice();
  }, r.unknown = function(s) {
    return arguments.length ? (i = s, r) : i;
  }, r.copy = function() {
    return di(e, n).unknown(i);
  }, fi.apply(r, arguments), r;
}
function Na(t) {
  return function() {
    return t;
  };
}
function Ta(t) {
  return +t;
}
var An = [0, 1];
function st(t) {
  return t;
}
function Pe(t, e) {
  return (e -= t = +t) ? function(n) {
    return (n - t) / e;
  } : Na(isNaN(e) ? NaN : 0.5);
}
function Ca(t, e) {
  var n;
  return t > e && (n = t, t = e, e = n), function(i) {
    return Math.max(t, Math.min(e, i));
  };
}
function za(t, e, n) {
  var i = t[0], r = t[1], s = e[0], o = e[1];
  return r < i ? (i = Pe(r, i), s = n(o, s)) : (i = Pe(i, r), s = n(s, o)), function(a) {
    return s(i(a));
  };
}
function Ia(t, e, n) {
  var i = Math.min(t.length, e.length) - 1, r = new Array(i), s = new Array(i), o = -1;
  for (t[i] < t[0] && (t = t.slice().reverse(), e = e.slice().reverse()); ++o < i; )
    r[o] = Pe(t[o], t[o + 1]), s[o] = n(e[o], e[o + 1]);
  return function(a) {
    var u = Ii(t, a, 1, i) - 1;
    return s[u](r[u](a));
  };
}
function Ra(t, e) {
  return e.domain(t.domain()).range(t.range()).interpolate(t.interpolate()).clamp(t.clamp()).unknown(t.unknown());
}
function La() {
  var t = An, e = An, n = he, i, r, s, o = st, a, u, l;
  function c() {
    var d = Math.min(t.length, e.length);
    return o !== st && (o = Ca(t[0], t[d - 1])), a = d > 2 ? Ia : za, u = l = null, h;
  }
  function h(d) {
    return d == null || isNaN(d = +d) ? s : (u || (u = a(t.map(i), e, n)))(i(o(d)));
  }
  return h.invert = function(d) {
    return o(r((l || (l = a(e, t.map(i), O)))(d)));
  }, h.domain = function(d) {
    return arguments.length ? (t = Array.from(d, Ta), c()) : t.slice();
  }, h.range = function(d) {
    return arguments.length ? (e = Array.from(d), c()) : e.slice();
  }, h.rangeRound = function(d) {
    return e = Array.from(d), n = Jn, c();
  }, h.clamp = function(d) {
    return arguments.length ? (o = d ? !0 : st, c()) : o !== st;
  }, h.interpolate = function(d) {
    return arguments.length ? (n = d, c()) : n;
  }, h.unknown = function(d) {
    return arguments.length ? (s = d, h) : s;
  }, function(d, g) {
    return i = d, r = g, c();
  };
}
function Pa() {
  return La()(st, st);
}
function Ha(t, e, n, i) {
  var r = qi(t, e, n), s;
  switch (i = le(i ?? ",f"), i.type) {
    case "s": {
      var o = Math.max(Math.abs(t), Math.abs(e));
      return i.precision == null && !isNaN(s = ka(r, o)) && (i.precision = s), hi(i, o);
    }
    case "":
    case "e":
    case "g":
    case "p":
    case "r": {
      i.precision == null && !isNaN(s = Ea(r, Math.max(Math.abs(t), Math.abs(e)))) && (i.precision = s - (i.type === "e"));
      break;
    }
    case "f":
    case "%": {
      i.precision == null && !isNaN(s = Ma(r)) && (i.precision = s - (i.type === "%") * 2);
      break;
    }
  }
  return ci(i);
}
function gi(t) {
  var e = t.domain;
  return t.ticks = function(n) {
    var i = e();
    return Vi(i[0], i[i.length - 1], n ?? 10);
  }, t.tickFormat = function(n, i) {
    var r = e();
    return Ha(r[0], r[r.length - 1], n ?? 10, i);
  }, t.nice = function(n) {
    n == null && (n = 10);
    var i = e(), r = 0, s = i.length - 1, o = i[r], a = i[s], u, l, c = 10;
    for (a < o && (l = o, o = a, a = l, l = r, r = s, s = l); c-- > 0; ) {
      if (l = Ae(o, a, n), l === u)
        return i[r] = o, i[s] = a, e(i);
      if (l > 0)
        o = Math.floor(o / l) * l, a = Math.ceil(a / l) * l;
      else if (l < 0)
        o = Math.ceil(o * l) / l, a = Math.floor(a * l) / l;
      else
        break;
      u = l;
    }
    return t;
  }, t;
}
function He() {
  var t = Pa();
  return t.copy = function() {
    return Ra(t, He());
  }, fi.apply(t, arguments), gi(t);
}
function Da() {
  var t = 0, e = 1, n, i, r, s, o = st, a = !1, u;
  function l(h) {
    return h == null || isNaN(h = +h) ? u : o(r === 0 ? 0.5 : (h = (s(h) - n) * r, a ? Math.max(0, Math.min(1, h)) : h));
  }
  l.domain = function(h) {
    return arguments.length ? ([t, e] = h, n = s(t = +t), i = s(e = +e), r = n === i ? 0 : 1 / (i - n), l) : [t, e];
  }, l.clamp = function(h) {
    return arguments.length ? (a = !!h, l) : a;
  }, l.interpolator = function(h) {
    return arguments.length ? (o = h, l) : o;
  };
  function c(h) {
    return function(d) {
      var g, m;
      return arguments.length ? ([g, m] = d, o = h(g, m), l) : [o(0), o(1)];
    };
  }
  return l.range = c(he), l.rangeRound = c(Jn), l.unknown = function(h) {
    return arguments.length ? (u = h, l) : u;
  }, function(h) {
    return s = h, n = h(t), i = h(e), r = n === i ? 0 : 1 / (i - n), l;
  };
}
function Ua(t, e) {
  return e.domain(t.domain()).interpolator(t.interpolator()).clamp(t.clamp()).unknown(t.unknown());
}
function pi() {
  var t = gi(Da()(st));
  return t.copy = function() {
    return Ua(t, pi());
  }, Sa.apply(t, arguments);
}
function Va(t) {
  for (var e = t.length / 6 | 0, n = new Array(e), i = 0; i < e; ) n[i] = "#" + t.slice(i * 6, ++i * 6);
  return n;
}
const mi = Va("4e79a7f28e2ce1575976b7b259a14fedc949af7aa1ff9da79c755fbab0ab");
function Yt(t) {
  return function() {
    return t;
  };
}
const yt = Math.sqrt, yi = Math.PI, qa = 2 * yi;
function Fa(t) {
  let e = 3;
  return t.digits = function(n) {
    if (!arguments.length) return e;
    if (n == null)
      e = null;
    else {
      const i = Math.floor(n);
      if (!(i >= 0)) throw new RangeError(`invalid digits: ${n}`);
      e = i;
    }
    return t;
  }, () => new ma(e);
}
const Oa = {
  draw(t, e) {
    const n = yt(e / yi);
    t.moveTo(n, 0), t.arc(0, 0, n, 0, qa);
  }
}, _i = {
  draw(t, e) {
    const n = yt(e / 5) / 2;
    t.moveTo(-3 * n, -n), t.lineTo(-n, -n), t.lineTo(-n, -3 * n), t.lineTo(n, -3 * n), t.lineTo(n, -n), t.lineTo(3 * n, -n), t.lineTo(3 * n, n), t.lineTo(n, n), t.lineTo(n, 3 * n), t.lineTo(-n, 3 * n), t.lineTo(-n, n), t.lineTo(-3 * n, n), t.closePath();
  }
}, ve = yt(3), vi = {
  draw(t, e) {
    const n = -yt(e / (ve * 3));
    t.moveTo(0, n * 2), t.lineTo(-ve * n, -n), t.lineTo(ve * n, -n), t.closePath();
  }
}, U = -0.5, V = yt(3) / 2, De = 1 / yt(12), Xa = (De / 2 + 1) * 3, xi = {
  draw(t, e) {
    const n = yt(e / Xa), i = n / 2, r = n * De, s = i, o = n * De + n, a = -s, u = o;
    t.moveTo(i, r), t.lineTo(s, o), t.lineTo(a, u), t.lineTo(U * i - V * r, V * i + U * r), t.lineTo(U * s - V * o, V * s + U * o), t.lineTo(U * a - V * u, V * a + U * u), t.lineTo(U * i + V * r, U * r - V * i), t.lineTo(U * s + V * o, U * o - V * s), t.lineTo(U * a + V * u, U * u - V * a), t.closePath();
  }
};
function ge(t, e) {
  let n = null, i = Fa(r);
  t = typeof t == "function" ? t : Yt(t || Oa), e = typeof e == "function" ? e : Yt(e === void 0 ? 64 : +e);
  function r() {
    let s;
    if (n || (n = s = i()), t.apply(this, arguments).draw(n, +e.apply(this, arguments)), s) return n = null, s + "" || null;
  }
  return r.type = function(s) {
    return arguments.length ? (t = typeof s == "function" ? s : Yt(s), r) : t;
  }, r.size = function(s) {
    return arguments.length ? (e = typeof s == "function" ? s : Yt(+s), r) : e;
  }, r.context = function(s) {
    return arguments.length ? (n = s ?? null, r) : n;
  }, r;
}
const Wt = (t) => () => t;
function Ba(t, {
  sourceEvent: e,
  target: n,
  transform: i,
  dispatch: r
}) {
  Object.defineProperties(this, {
    type: { value: t, enumerable: !0, configurable: !0 },
    sourceEvent: { value: e, enumerable: !0, configurable: !0 },
    target: { value: n, enumerable: !0, configurable: !0 },
    transform: { value: i, enumerable: !0, configurable: !0 },
    _: { value: r }
  });
}
function nt(t, e, n) {
  this.k = t, this.x = e, this.y = n;
}
nt.prototype = {
  constructor: nt,
  scale: function(t) {
    return t === 1 ? this : new nt(this.k * t, this.x, this.y);
  },
  translate: function(t, e) {
    return t === 0 & e === 0 ? this : new nt(this.k, this.x + this.k * t, this.y + this.k * e);
  },
  apply: function(t) {
    return [t[0] * this.k + this.x, t[1] * this.k + this.y];
  },
  applyX: function(t) {
    return t * this.k + this.x;
  },
  applyY: function(t) {
    return t * this.k + this.y;
  },
  invert: function(t) {
    return [(t[0] - this.x) / this.k, (t[1] - this.y) / this.k];
  },
  invertX: function(t) {
    return (t - this.x) / this.k;
  },
  invertY: function(t) {
    return (t - this.y) / this.k;
  },
  rescaleX: function(t) {
    return t.copy().domain(t.range().map(this.invertX, this).map(t.invert, t));
  },
  rescaleY: function(t) {
    return t.copy().domain(t.range().map(this.invertY, this).map(t.invert, t));
  },
  toString: function() {
    return "translate(" + this.x + "," + this.y + ") scale(" + this.k + ")";
  }
};
var wi = new nt(1, 0, 0);
nt.prototype;
function xe(t) {
  t.stopImmediatePropagation();
}
function Nt(t) {
  t.preventDefault(), t.stopImmediatePropagation();
}
function Ga(t) {
  return (!t.ctrlKey || t.type === "wheel") && !t.button;
}
function Ya() {
  var t = this;
  return t instanceof SVGElement ? (t = t.ownerSVGElement || t, t.hasAttribute("viewBox") ? (t = t.viewBox.baseVal, [[t.x, t.y], [t.x + t.width, t.y + t.height]]) : [[0, 0], [t.width.baseVal.value, t.height.baseVal.value]]) : [[0, 0], [t.clientWidth, t.clientHeight]];
}
function Mn() {
  return this.__zoom || wi;
}
function Wa(t) {
  return -t.deltaY * (t.deltaMode === 1 ? 0.05 : t.deltaMode ? 1 : 2e-3) * (t.ctrlKey ? 10 : 1);
}
function Ka() {
  return navigator.maxTouchPoints || "ontouchstart" in this;
}
function Za(t, e, n) {
  var i = t.invertX(e[0][0]) - n[0][0], r = t.invertX(e[1][0]) - n[1][0], s = t.invertY(e[0][1]) - n[0][1], o = t.invertY(e[1][1]) - n[1][1];
  return t.translate(
    r > i ? (i + r) / 2 : Math.min(0, i) || Math.max(0, r),
    o > s ? (s + o) / 2 : Math.min(0, s) || Math.max(0, o)
  );
}
function Qa() {
  var t = Ga, e = Ya, n = Za, i = Wa, r = Ka, s = [0, 1 / 0], o = [[-1 / 0, -1 / 0], [1 / 0, 1 / 0]], a = 250, u = eo, l = Ve("start", "zoom", "end"), c, h, d, g = 500, m = 150, x = 0, M = 10;
  function v(f) {
    f.property("__zoom", Mn).on("wheel.zoom", ot, { passive: !1 }).on("mousedown.zoom", _t).on("dblclick.zoom", at).filter(r).on("touchstart.zoom", A).on("touchmove.zoom", J).on("touchend.zoom touchcancel.zoom", P).style("-webkit-tap-highlight-color", "rgba(0,0,0,0)");
  }
  v.transform = function(f, y, p, _) {
    var b = f.selection ? f.selection() : f;
    b.property("__zoom", Mn), f !== b ? k(f, y, p, _) : b.interrupt().each(function() {
      D(this, arguments).event(_).start().zoom(null, typeof y == "function" ? y.apply(this, arguments) : y).end();
    });
  }, v.scaleBy = function(f, y, p, _) {
    v.scaleTo(f, function() {
      var b = this.__zoom.k, w = typeof y == "function" ? y.apply(this, arguments) : y;
      return b * w;
    }, p, _);
  }, v.scaleTo = function(f, y, p, _) {
    v.transform(f, function() {
      var b = e.apply(this, arguments), w = this.__zoom, $ = p == null ? I(b) : typeof p == "function" ? p.apply(this, arguments) : p, E = w.invert($), T = typeof y == "function" ? y.apply(this, arguments) : y;
      return n(S(N(w, T), $, E), b, o);
    }, p, _);
  }, v.translateBy = function(f, y, p, _) {
    v.transform(f, function() {
      return n(this.__zoom.translate(
        typeof y == "function" ? y.apply(this, arguments) : y,
        typeof p == "function" ? p.apply(this, arguments) : p
      ), e.apply(this, arguments), o);
    }, null, _);
  }, v.translateTo = function(f, y, p, _, b) {
    v.transform(f, function() {
      var w = e.apply(this, arguments), $ = this.__zoom, E = _ == null ? I(w) : typeof _ == "function" ? _.apply(this, arguments) : _;
      return n(wi.translate(E[0], E[1]).scale($.k).translate(
        typeof y == "function" ? -y.apply(this, arguments) : -y,
        typeof p == "function" ? -p.apply(this, arguments) : -p
      ), w, o);
    }, _, b);
  };
  function N(f, y) {
    return y = Math.max(s[0], Math.min(s[1], y)), y === f.k ? f : new nt(y, f.x, f.y);
  }
  function S(f, y, p) {
    var _ = y[0] - p[0] * f.k, b = y[1] - p[1] * f.k;
    return _ === f.x && b === f.y ? f : new nt(f.k, _, b);
  }
  function I(f) {
    return [(+f[0][0] + +f[1][0]) / 2, (+f[0][1] + +f[1][1]) / 2];
  }
  function k(f, y, p, _) {
    f.on("start.zoom", function() {
      D(this, arguments).event(_).start();
    }).on("interrupt.zoom end.zoom", function() {
      D(this, arguments).event(_).end();
    }).tween("zoom", function() {
      var b = this, w = arguments, $ = D(b, w).event(_), E = e.apply(b, w), T = p == null ? I(E) : typeof p == "function" ? p.apply(b, w) : p, Y = Math.max(E[1][0] - E[0][0], E[1][1] - E[0][1]), R = b.__zoom, q = typeof y == "function" ? y.apply(b, w) : y, j = u(R.invert(T).concat(Y / R.k), q.invert(T).concat(Y / q.k));
      return function(F) {
        if (F === 1) F = q;
        else {
          var tt = j(F), me = Y / tt[2];
          F = new nt(me, T[0] - tt[0] * me, T[1] - tt[1] * me);
        }
        $.zoom(null, F);
      };
    });
  }
  function D(f, y, p) {
    return !p && f.__zooming || new G(f, y);
  }
  function G(f, y) {
    this.that = f, this.args = y, this.active = 0, this.sourceEvent = null, this.extent = e.apply(f, y), this.taps = 0;
  }
  G.prototype = {
    event: function(f) {
      return f && (this.sourceEvent = f), this;
    },
    start: function() {
      return ++this.active === 1 && (this.that.__zooming = this, this.emit("start")), this;
    },
    zoom: function(f, y) {
      return this.mouse && f !== "mouse" && (this.mouse[1] = y.invert(this.mouse[0])), this.touch0 && f !== "touch" && (this.touch0[1] = y.invert(this.touch0[0])), this.touch1 && f !== "touch" && (this.touch1[1] = y.invert(this.touch1[0])), this.that.__zoom = y, this.emit("zoom"), this;
    },
    end: function() {
      return --this.active === 0 && (delete this.that.__zooming, this.emit("end")), this;
    },
    emit: function(f) {
      var y = W(this.that).datum();
      l.call(
        f,
        this.that,
        new Ba(f, {
          sourceEvent: this.sourceEvent,
          target: v,
          type: f,
          transform: this.that.__zoom,
          dispatch: l
        }),
        y
      );
    }
  };
  function ot(f, ...y) {
    if (!t.apply(this, arguments)) return;
    var p = D(this, y).event(f), _ = this.__zoom, b = Math.max(s[0], Math.min(s[1], _.k * Math.pow(2, i.apply(this, arguments)))), w = lt(f);
    if (p.wheel)
      (p.mouse[0][0] !== w[0] || p.mouse[0][1] !== w[1]) && (p.mouse[1] = _.invert(p.mouse[0] = w)), clearTimeout(p.wheel);
    else {
      if (_.k === b) return;
      p.mouse = [w, _.invert(w)], jt(this), p.start();
    }
    Nt(f), p.wheel = setTimeout($, m), p.zoom("mouse", n(S(N(_, b), p.mouse[0], p.mouse[1]), p.extent, o));
    function $() {
      p.wheel = null, p.end();
    }
  }
  function _t(f, ...y) {
    if (d || !t.apply(this, arguments)) return;
    var p = f.currentTarget, _ = D(this, y, !0).event(f), b = W(f.view).on("mousemove.zoom", T, !0).on("mouseup.zoom", Y, !0), w = lt(f, p), $ = f.clientX, E = f.clientY;
    As(f.view), xe(f), _.mouse = [w, this.__zoom.invert(w)], jt(this), _.start();
    function T(R) {
      if (Nt(R), !_.moved) {
        var q = R.clientX - $, j = R.clientY - E;
        _.moved = q * q + j * j > x;
      }
      _.event(R).zoom("mouse", n(S(_.that.__zoom, _.mouse[0] = lt(R, p), _.mouse[1]), _.extent, o));
    }
    function Y(R) {
      b.on("mousemove.zoom mouseup.zoom", null), Ms(R.view, _.moved), Nt(R), _.event(R).end();
    }
  }
  function at(f, ...y) {
    if (t.apply(this, arguments)) {
      var p = this.__zoom, _ = lt(f.changedTouches ? f.changedTouches[0] : f, this), b = p.invert(_), w = p.k * (f.shiftKey ? 0.5 : 2), $ = n(S(N(p, w), _, b), e.apply(this, y), o);
      Nt(f), a > 0 ? W(this).transition().duration(a).call(k, $, _, f) : W(this).call(v.transform, $, _, f);
    }
  }
  function A(f, ...y) {
    if (t.apply(this, arguments)) {
      var p = f.touches, _ = p.length, b = D(this, y, f.changedTouches.length === _).event(f), w, $, E, T;
      for (xe(f), $ = 0; $ < _; ++$)
        E = p[$], T = lt(E, this), T = [T, this.__zoom.invert(T), E.identifier], b.touch0 ? !b.touch1 && b.touch0[2] !== T[2] && (b.touch1 = T, b.taps = 0) : (b.touch0 = T, w = !0, b.taps = 1 + !!c);
      c && (c = clearTimeout(c)), w && (b.taps < 2 && (h = T[0], c = setTimeout(function() {
        c = null;
      }, g)), jt(this), b.start());
    }
  }
  function J(f, ...y) {
    if (this.__zooming) {
      var p = D(this, y).event(f), _ = f.changedTouches, b = _.length, w, $, E, T;
      for (Nt(f), w = 0; w < b; ++w)
        $ = _[w], E = lt($, this), p.touch0 && p.touch0[2] === $.identifier ? p.touch0[0] = E : p.touch1 && p.touch1[2] === $.identifier && (p.touch1[0] = E);
      if ($ = p.that.__zoom, p.touch1) {
        var Y = p.touch0[0], R = p.touch0[1], q = p.touch1[0], j = p.touch1[1], F = (F = q[0] - Y[0]) * F + (F = q[1] - Y[1]) * F, tt = (tt = j[0] - R[0]) * tt + (tt = j[1] - R[1]) * tt;
        $ = N($, Math.sqrt(F / tt)), E = [(Y[0] + q[0]) / 2, (Y[1] + q[1]) / 2], T = [(R[0] + j[0]) / 2, (R[1] + j[1]) / 2];
      } else if (p.touch0) E = p.touch0[0], T = p.touch0[1];
      else return;
      p.zoom("touch", n(S($, E, T), p.extent, o));
    }
  }
  function P(f, ...y) {
    if (this.__zooming) {
      var p = D(this, y).event(f), _ = f.changedTouches, b = _.length, w, $;
      for (xe(f), d && clearTimeout(d), d = setTimeout(function() {
        d = null;
      }, g), w = 0; w < b; ++w)
        $ = _[w], p.touch0 && p.touch0[2] === $.identifier ? delete p.touch0 : p.touch1 && p.touch1[2] === $.identifier && delete p.touch1;
      if (p.touch1 && !p.touch0 && (p.touch0 = p.touch1, delete p.touch1), p.touch0) p.touch0[1] = this.__zoom.invert(p.touch0[0]);
      else if (p.end(), p.taps === 2 && ($ = lt($, this), Math.hypot(h[0] - $[0], h[1] - $[1]) < M)) {
        var E = W(this).on("dblclick.zoom");
        E && E.apply(this, arguments);
      }
    }
  }
  return v.wheelDelta = function(f) {
    return arguments.length ? (i = typeof f == "function" ? f : Wt(+f), v) : i;
  }, v.filter = function(f) {
    return arguments.length ? (t = typeof f == "function" ? f : Wt(!!f), v) : t;
  }, v.touchable = function(f) {
    return arguments.length ? (r = typeof f == "function" ? f : Wt(!!f), v) : r;
  }, v.extent = function(f) {
    return arguments.length ? (e = typeof f == "function" ? f : Wt([[+f[0][0], +f[0][1]], [+f[1][0], +f[1][1]]]), v) : e;
  }, v.scaleExtent = function(f) {
    return arguments.length ? (s[0] = +f[0], s[1] = +f[1], v) : [s[0], s[1]];
  }, v.translateExtent = function(f) {
    return arguments.length ? (o[0][0] = +f[0][0], o[1][0] = +f[1][0], o[0][1] = +f[0][1], o[1][1] = +f[1][1], v) : [[o[0][0], o[0][1]], [o[1][0], o[1][1]]];
  }, v.constrain = function(f) {
    return arguments.length ? (n = f, v) : n;
  }, v.duration = function(f) {
    return arguments.length ? (a = +f, v) : a;
  }, v.interpolate = function(f) {
    return arguments.length ? (u = f, v) : u;
  }, v.on = function() {
    var f = l.on.apply(l, arguments);
    return f === l ? v : f;
  }, v.clickDistance = function(f) {
    return arguments.length ? (x = (f = +f) * f, v) : Math.sqrt(x);
  }, v.tapDistance = function(f) {
    return arguments.length ? (M = +f, v) : M;
  }, v;
}
class Ja {
  constructor(e) {
    this.showUnst = !0, this.group = e.append("g").attr("class", "originalEmbedding");
  }
  render(e, n) {
    this.group.selectAll("circle").data(e).join("circle").attr("id", (i) => `circle-${i.id.toString()}`).attr("cx", (i) => n.xScale(i.x)).attr("cy", (i) => n.yScale(i.y)).attr("r", 0.6).attr("fill", (i) => n.colorScale(i.label)).attr("id", (i) => `circle-${i.id.toString()}`);
  }
  setVisibility(e, n) {
    if (this.showUnst = e, this.showUnst) {
      this.group.selectAll("circle").attr("visibility", "visible");
      return;
    }
    n.forEach((i) => {
      this.group.selectAll(`circle[id="circle-${i.id.toString()}"]`).attr("visibility", "hidden");
    });
  }
  updateUnstEmbedding(e) {
    this.group.selectAll("circle").attr("visibility", "visible"), this.showUnst || e.forEach((n) => {
      this.group.selectAll(`circle[id="circle-${n.toString()}"]`).attr("visibility", "hidden");
    });
  }
}
const ja = (t, e, n, i, r, s) => {
  const [o, a] = Qe(t, (x) => x.x), [u, l] = Qe(t, (x) => x.y), c = He().domain([o * 1.1, a * 1.1]).range([0, e]), h = He().domain([u * 1.1, l * 1.1]).range([n, 0]);
  console.log(i);
  let d = di().domain(Ln(i.length).map(String)).range(mi);
  return { xScale: c, yScale: h, colorScale: d, range: {
    xMin: o,
    xMax: a,
    yMin: u,
    yMax: l
  }, ghostColorScale: (x) => {
    const M = r[x] || d(x);
    return (v) => {
      const N = v / s;
      return bt(M, "#ffffff")(1 - N);
    };
  } };
}, vt = (t) => {
  const e = t.get("embedding_id"), [n, i] = [t.get("width"), t.get("height")], {
    original_embedding: r,
    ghost_embedding: s,
    n_ghosts: o,
    r: a,
    legend: u,
    colors: l
  } = t.get("embedding_set")[e], c = ja(r, n, i, u, l, a), h = c.range, d = t.get("distance"), g = t.get("sensitivity"), m = Math.floor(g * (o - 1));
  console.log("ghostEmb", s);
  const x = d * Fi([h.xMax - h.xMin, h.yMax - h.yMin]);
  console.log(m, x);
  const M = r.filter((v) => v.radii[m] > x);
  return {
    origEmb: r,
    ghostEmb: s,
    radius: a,
    unstEmb: M,
    scales: c,
    range: h,
    scaledDist: x,
    scaledSens: m,
    legend: u,
    colors: l
  };
}, Ue = (t, e, n) => {
  const i = { ...t.get("unstableInfo") };
  return i.unstableEmb = e, i.numUnstables = e.length, i.percentUnstables = e.length / n * 100, t.set("unstableInfo", i), t.save_changes(), i;
}, bi = (t, e) => {
  const n = e.filter(
    (r) => !t.includes(r)
  ), i = t.filter(
    (r) => !e.includes(r)
  );
  return [n, i];
};
class tl {
  constructor(e) {
    this.unstableList = [], this.group = e.append("g").attr("class", "ghostEmbedding");
  }
  renderGhosts(e, n, i) {
    const r = n.find((a) => a.id === e), s = (r == null ? void 0 : r.coords) || [], o = (r == null ? void 0 : r.label) || "0";
    this.group.append("g").selectAll("path").data(s).join("path").attr("pointer-events", "none").attr("stroke-width", 3).attr("d", ge(vi).size(260)).attr("fill", (a) => i.ghostColorScale(o)(a.r)).attr(
      "transform",
      (a) => `translate(${i.xScale(a.x)},${i.yScale(a.y)})`
    ).attr("stroke", "black");
  }
  removeGhosts(e) {
    this.group.selectAll(`#ghost-${e}`).remove();
  }
  reset() {
    this.group.selectAll("g").remove(), this.unstableList = [];
  }
  setVisibility(e) {
    this.group.attr("visibility", e ? "visible" : "hidden");
  }
  render(e, n, i) {
    const [r, s] = bi(this.unstableList, i);
    r.forEach((o) => this.renderGhosts(o, e, n)), s.forEach((o) => this.removeGhosts(o)), this.unstableList = i;
  }
}
class el {
  constructor(e) {
    this.show = !0, this.group = e.append("g").attr("class", "unstableEmbedding");
  }
  render(e, n, i) {
    const { xScale: r, yScale: s, colorScale: o } = n;
    this.group.selectAll("path").data(e).join("path").attr("transform", (a) => `translate(${r(a.x)},${s(a.y)})`).attr("fill", (a) => o(a.label)).attr("pointer-events", "all").attr("stroke", "black").attr("d", ge(_i).size(300)).attr("stroke-width", 1.2).attr("visibility", this.show ? "visible" : "hidden").attr("id", (a) => `unstPoint-${a.id.toString()}`).on("click", (a, u) => {
      a.stopPropagation(), i(u.id);
    });
  }
  setVisibility(e) {
    this.show = e, this.show ? this.group.selectAll("path").attr("visibility", "visible").attr("pointer-events", "all") : this.group.selectAll("path").attr("visibility", "hidden").attr("pointer-events", "none");
  }
}
class nl {
  constructor(e) {
    this.unstableList = [], this.group = e.append("g").attr("class", "neighborEmbedding").attr("visibility", "hidden");
  }
  renderNeighbors(e, n, i) {
    const { xScale: r, yScale: s, colorScale: o } = i, a = n[e].neighbors.map((u) => n[u]);
    this.group.append("g").attr("id", `neighbor-${e}`).selectAll("path").data(a).join("path").attr("pointer-events", "none").attr("stroke-width", 2).attr("d", ge(xi).size(250)).attr("transform", (u) => `translate(${r(u.x)},${s(u.y)})`).attr("fill", (u) => o(u.label)).attr("stroke", "black");
  }
  removeNeighbors(e) {
    this.group.selectAll(`#neighbor-${e}`).remove();
  }
  reset() {
    this.group.selectAll("g").remove(), this.unstableList = [];
  }
  setVisibility(e) {
    this.group.attr("visibility", e ? "visible" : "hidden");
  }
  render(e, n, i) {
    const [r, s] = bi(this.unstableList, i);
    r.forEach((o) => this.renderNeighbors(o, e, n)), s.forEach((o) => this.removeNeighbors(o)), this.unstableList = i;
  }
}
class il {
  constructor(e, n) {
    this.width = e, this.height = n, this.svg = this.createSVG(), this.groupContainer = this.svg.append("g"), this.originalEmbedding = new Ja(this.groupContainer), this.neighborEmbedding = new nl(this.groupContainer), this.ghostEmbedding = new tl(this.groupContainer), this.unstableEmbedding = new el(this.groupContainer);
  }
  createSVG() {
    return Yn("svg").attr("class", "scatterplot").attr("width", `${this.width}px`).attr("height", `${this.height}px`).on("contextmenu", (e) => {
      e.preventDefault(), this.resetViewPoint();
    });
  }
  resetViewPoint() {
    this.groupContainer.transition().duration(750).attr("transform", "translate(0,0) scale(1)");
  }
  updateEmbedding(e, n, i, r) {
    this.originalEmbedding.render(e, i), this.unstableEmbedding.render(n, i, (s) => {
      r([s]);
    });
  }
  render(e, n, i, r) {
    this.updateEmbedding(e, n, i, r), this.svg.on("click", () => r([]));
    const s = Qa().scaleExtent([1, 20]).filter((o) => o.type === "wheel").on("zoom", (o) => {
      o.transform.k <= 1 && (o.transform.k = 1, o.transform.x = 0, o.transform.y = 0), this.groupContainer.transition().delay(10).attr("transform", o.transform);
    });
    return this.svg.call(s), this.svg.node();
  }
  updateUnstEmbedding(e, n, i) {
    this.unstableEmbedding.render(e, n, (r) => {
      i([r]);
    }), this.originalEmbedding.updateUnstEmbedding(e);
  }
  setVisibility(e, n, i = []) {
    switch (e) {
      case "neighbors":
        this.neighborEmbedding.setVisibility(n);
        break;
      case "ghosts":
        this.ghostEmbedding.setVisibility(n);
        break;
      case "unstables":
        this.originalEmbedding.setVisibility(n, i), this.unstableEmbedding.setVisibility(n);
        break;
    }
  }
  updateDetail(e, n, i, r) {
    this.ghostEmbedding.render(n, i, r), this.neighborEmbedding.render(e, i, r), this.unstableEmbedding.render(
      e.filter((s) => r.includes(s.id)),
      i,
      (s) => {
      }
    );
  }
  resetDetail(e, n, i) {
    this.ghostEmbedding.reset(), this.neighborEmbedding.reset(), this.unstableEmbedding.render(e, n, (r) => {
      i([r]);
    });
  }
}
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const It = globalThis, ue = It.trustedTypes, kn = ue ? ue.createPolicy("lit-html", { createHTML: (t) => t }) : void 0, $i = "$lit$", rt = `lit$${Math.random().toFixed(9).slice(2)}$`, Ai = "?" + rt, rl = `<${Ai}>`, mt = document, Ht = () => mt.createComment(""), Dt = (t) => t === null || typeof t != "object" && typeof t != "function", Mi = Array.isArray, sl = (t) => Mi(t) || typeof (t == null ? void 0 : t[Symbol.iterator]) == "function", we = `[ 	
\f\r]`, Tt = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, En = /-->/g, Sn = />/g, ut = RegExp(`>|${we}(?:([^\\s"'>=/]+)(${we}*=${we}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), Nn = /'/g, Tn = /"/g, ki = /^(?:script|style|textarea|title)$/i, ol = (t) => (e, ...n) => ({ _$litType$: t, strings: e, values: n }), Z = ol(1), Mt = Symbol.for("lit-noChange"), z = Symbol.for("lit-nothing"), Cn = /* @__PURE__ */ new WeakMap(), ft = mt.createTreeWalker(mt, 129);
function Ei(t, e) {
  if (!Array.isArray(t) || !t.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return kn !== void 0 ? kn.createHTML(e) : e;
}
const al = (t, e) => {
  const n = t.length - 1, i = [];
  let r, s = e === 2 ? "<svg>" : "", o = Tt;
  for (let a = 0; a < n; a++) {
    const u = t[a];
    let l, c, h = -1, d = 0;
    for (; d < u.length && (o.lastIndex = d, c = o.exec(u), c !== null); ) d = o.lastIndex, o === Tt ? c[1] === "!--" ? o = En : c[1] !== void 0 ? o = Sn : c[2] !== void 0 ? (ki.test(c[2]) && (r = RegExp("</" + c[2], "g")), o = ut) : c[3] !== void 0 && (o = ut) : o === ut ? c[0] === ">" ? (o = r ?? Tt, h = -1) : c[1] === void 0 ? h = -2 : (h = o.lastIndex - c[2].length, l = c[1], o = c[3] === void 0 ? ut : c[3] === '"' ? Tn : Nn) : o === Tn || o === Nn ? o = ut : o === En || o === Sn ? o = Tt : (o = ut, r = void 0);
    const g = o === ut && t[a + 1].startsWith("/>") ? " " : "";
    s += o === Tt ? u + rl : h >= 0 ? (i.push(l), u.slice(0, h) + $i + u.slice(h) + rt + g) : u + rt + (h === -2 ? a : g);
  }
  return [Ei(t, s + (t[n] || "<?>") + (e === 2 ? "</svg>" : "")), i];
};
class Ut {
  constructor({ strings: e, _$litType$: n }, i) {
    let r;
    this.parts = [];
    let s = 0, o = 0;
    const a = e.length - 1, u = this.parts, [l, c] = al(e, n);
    if (this.el = Ut.createElement(l, i), ft.currentNode = this.el.content, n === 2) {
      const h = this.el.content.firstChild;
      h.replaceWith(...h.childNodes);
    }
    for (; (r = ft.nextNode()) !== null && u.length < a; ) {
      if (r.nodeType === 1) {
        if (r.hasAttributes()) for (const h of r.getAttributeNames()) if (h.endsWith($i)) {
          const d = c[o++], g = r.getAttribute(h).split(rt), m = /([.?@])?(.*)/.exec(d);
          u.push({ type: 1, index: s, name: m[2], strings: g, ctor: m[1] === "." ? ul : m[1] === "?" ? cl : m[1] === "@" ? hl : pe }), r.removeAttribute(h);
        } else h.startsWith(rt) && (u.push({ type: 6, index: s }), r.removeAttribute(h));
        if (ki.test(r.tagName)) {
          const h = r.textContent.split(rt), d = h.length - 1;
          if (d > 0) {
            r.textContent = ue ? ue.emptyScript : "";
            for (let g = 0; g < d; g++) r.append(h[g], Ht()), ft.nextNode(), u.push({ type: 2, index: ++s });
            r.append(h[d], Ht());
          }
        }
      } else if (r.nodeType === 8) if (r.data === Ai) u.push({ type: 2, index: s });
      else {
        let h = -1;
        for (; (h = r.data.indexOf(rt, h + 1)) !== -1; ) u.push({ type: 7, index: s }), h += rt.length - 1;
      }
      s++;
    }
  }
  static createElement(e, n) {
    const i = mt.createElement("template");
    return i.innerHTML = e, i;
  }
}
function kt(t, e, n = t, i) {
  var o, a;
  if (e === Mt) return e;
  let r = i !== void 0 ? (o = n._$Co) == null ? void 0 : o[i] : n._$Cl;
  const s = Dt(e) ? void 0 : e._$litDirective$;
  return (r == null ? void 0 : r.constructor) !== s && ((a = r == null ? void 0 : r._$AO) == null || a.call(r, !1), s === void 0 ? r = void 0 : (r = new s(t), r._$AT(t, n, i)), i !== void 0 ? (n._$Co ?? (n._$Co = []))[i] = r : n._$Cl = r), r !== void 0 && (e = kt(t, r._$AS(t, e.values), r, i)), e;
}
class ll {
  constructor(e, n) {
    this._$AV = [], this._$AN = void 0, this._$AD = e, this._$AM = n;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(e) {
    const { el: { content: n }, parts: i } = this._$AD, r = ((e == null ? void 0 : e.creationScope) ?? mt).importNode(n, !0);
    ft.currentNode = r;
    let s = ft.nextNode(), o = 0, a = 0, u = i[0];
    for (; u !== void 0; ) {
      if (o === u.index) {
        let l;
        u.type === 2 ? l = new Ft(s, s.nextSibling, this, e) : u.type === 1 ? l = new u.ctor(s, u.name, u.strings, this, e) : u.type === 6 && (l = new fl(s, this, e)), this._$AV.push(l), u = i[++a];
      }
      o !== (u == null ? void 0 : u.index) && (s = ft.nextNode(), o++);
    }
    return ft.currentNode = mt, r;
  }
  p(e) {
    let n = 0;
    for (const i of this._$AV) i !== void 0 && (i.strings !== void 0 ? (i._$AI(e, i, n), n += i.strings.length - 2) : i._$AI(e[n])), n++;
  }
}
class Ft {
  get _$AU() {
    var e;
    return ((e = this._$AM) == null ? void 0 : e._$AU) ?? this._$Cv;
  }
  constructor(e, n, i, r) {
    this.type = 2, this._$AH = z, this._$AN = void 0, this._$AA = e, this._$AB = n, this._$AM = i, this.options = r, this._$Cv = (r == null ? void 0 : r.isConnected) ?? !0;
  }
  get parentNode() {
    let e = this._$AA.parentNode;
    const n = this._$AM;
    return n !== void 0 && (e == null ? void 0 : e.nodeType) === 11 && (e = n.parentNode), e;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(e, n = this) {
    e = kt(this, e, n), Dt(e) ? e === z || e == null || e === "" ? (this._$AH !== z && this._$AR(), this._$AH = z) : e !== this._$AH && e !== Mt && this._(e) : e._$litType$ !== void 0 ? this.$(e) : e.nodeType !== void 0 ? this.T(e) : sl(e) ? this.k(e) : this._(e);
  }
  S(e) {
    return this._$AA.parentNode.insertBefore(e, this._$AB);
  }
  T(e) {
    this._$AH !== e && (this._$AR(), this._$AH = this.S(e));
  }
  _(e) {
    this._$AH !== z && Dt(this._$AH) ? this._$AA.nextSibling.data = e : this.T(mt.createTextNode(e)), this._$AH = e;
  }
  $(e) {
    var s;
    const { values: n, _$litType$: i } = e, r = typeof i == "number" ? this._$AC(e) : (i.el === void 0 && (i.el = Ut.createElement(Ei(i.h, i.h[0]), this.options)), i);
    if (((s = this._$AH) == null ? void 0 : s._$AD) === r) this._$AH.p(n);
    else {
      const o = new ll(r, this), a = o.u(this.options);
      o.p(n), this.T(a), this._$AH = o;
    }
  }
  _$AC(e) {
    let n = Cn.get(e.strings);
    return n === void 0 && Cn.set(e.strings, n = new Ut(e)), n;
  }
  k(e) {
    Mi(this._$AH) || (this._$AH = [], this._$AR());
    const n = this._$AH;
    let i, r = 0;
    for (const s of e) r === n.length ? n.push(i = new Ft(this.S(Ht()), this.S(Ht()), this, this.options)) : i = n[r], i._$AI(s), r++;
    r < n.length && (this._$AR(i && i._$AB.nextSibling, r), n.length = r);
  }
  _$AR(e = this._$AA.nextSibling, n) {
    var i;
    for ((i = this._$AP) == null ? void 0 : i.call(this, !1, !0, n); e && e !== this._$AB; ) {
      const r = e.nextSibling;
      e.remove(), e = r;
    }
  }
  setConnected(e) {
    var n;
    this._$AM === void 0 && (this._$Cv = e, (n = this._$AP) == null || n.call(this, e));
  }
}
class pe {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(e, n, i, r, s) {
    this.type = 1, this._$AH = z, this._$AN = void 0, this.element = e, this.name = n, this._$AM = r, this.options = s, i.length > 2 || i[0] !== "" || i[1] !== "" ? (this._$AH = Array(i.length - 1).fill(new String()), this.strings = i) : this._$AH = z;
  }
  _$AI(e, n = this, i, r) {
    const s = this.strings;
    let o = !1;
    if (s === void 0) e = kt(this, e, n, 0), o = !Dt(e) || e !== this._$AH && e !== Mt, o && (this._$AH = e);
    else {
      const a = e;
      let u, l;
      for (e = s[0], u = 0; u < s.length - 1; u++) l = kt(this, a[i + u], n, u), l === Mt && (l = this._$AH[u]), o || (o = !Dt(l) || l !== this._$AH[u]), l === z ? e = z : e !== z && (e += (l ?? "") + s[u + 1]), this._$AH[u] = l;
    }
    o && !r && this.j(e);
  }
  j(e) {
    e === z ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, e ?? "");
  }
}
class ul extends pe {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(e) {
    this.element[this.name] = e === z ? void 0 : e;
  }
}
class cl extends pe {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(e) {
    this.element.toggleAttribute(this.name, !!e && e !== z);
  }
}
class hl extends pe {
  constructor(e, n, i, r, s) {
    super(e, n, i, r, s), this.type = 5;
  }
  _$AI(e, n = this) {
    if ((e = kt(this, e, n, 0) ?? z) === Mt) return;
    const i = this._$AH, r = e === z && i !== z || e.capture !== i.capture || e.once !== i.once || e.passive !== i.passive, s = e !== z && (i === z || r);
    r && this.element.removeEventListener(this.name, this, i), s && this.element.addEventListener(this.name, this, e), this._$AH = e;
  }
  handleEvent(e) {
    var n;
    typeof this._$AH == "function" ? this._$AH.call(((n = this.options) == null ? void 0 : n.host) ?? this.element, e) : this._$AH.handleEvent(e);
  }
}
class fl {
  constructor(e, n, i) {
    this.element = e, this.type = 6, this._$AN = void 0, this._$AM = n, this.options = i;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(e) {
    kt(this, e);
  }
}
const be = It.litHtmlPolyfillSupport;
be == null || be(Ut, Ft), (It.litHtmlVersions ?? (It.litHtmlVersions = [])).push("3.1.4");
const Et = (t, e, n) => {
  const i = e;
  let r = i._$litPart$;
  return r === void 0 && (i._$litPart$ = r = new Ft(e.insertBefore(Ht(), null), null, void 0, {})), r._$AI(t), r;
};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const dl = { ATTRIBUTE: 1, CHILD: 2, PROPERTY: 3, BOOLEAN_ATTRIBUTE: 4, EVENT: 5, ELEMENT: 6 }, gl = (t) => (...e) => ({ _$litDirective$: t, values: e });
let pl = class {
  constructor(e) {
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AT(e, n, i) {
    this._$Ct = e, this._$AM = n, this._$Ci = i;
  }
  _$AS(e, n) {
    return this.update(e, n);
  }
  update(e, n) {
    return this.render(...n);
  }
};
/**
 * @license
 * Copyright 2018 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const Si = "important", ml = " !" + Si, C = gl(class extends pl {
  constructor(t) {
    var e;
    if (super(t), t.type !== dl.ATTRIBUTE || t.name !== "style" || ((e = t.strings) == null ? void 0 : e.length) > 2) throw Error("The `styleMap` directive must be used in the `style` attribute and must be the only part in the attribute.");
  }
  render(t) {
    return Object.keys(t).reduce((e, n) => {
      const i = t[n];
      return i == null ? e : e + `${n = n.includes("-") ? n : n.replace(/(?:^(webkit|moz|ms|o)|)(?=[A-Z])/g, "-$&").toLowerCase()}:${i};`;
    }, "");
  }
  update(t, [e]) {
    const { style: n } = t.element;
    if (this.ft === void 0) return this.ft = new Set(Object.keys(e)), this.render(e);
    for (const i of this.ft) e[i] == null && (this.ft.delete(i), i.includes("-") ? n.removeProperty(i) : n[i] = null);
    for (const i in e) {
      const r = e[i];
      if (r != null) {
        this.ft.add(i);
        const s = typeof r == "string" && r.endsWith(ml);
        i.includes("-") || s ? n.setProperty(i, s ? r.slice(0, -11) : r, s ? Si : "") : n[i] = r;
      }
    }
    return Mt;
  }
}), yl = {
  maxWidth: "250px",
  width: "100%"
}, _l = {
  display: "flex",
  "flex-direction": "column",
  "margin-bottom": "10px",
  maxWidth: "300px",
  "font-size": "16px"
  // 추가된 기본 폰트 크기
}, vl = {
  "font-size": "18px",
  // label 폰트 크기
  "margin-bottom": "5px"
}, zn = {
  "font-size": "16px"
  // min/max 값 폰트 크기
};
class xl {
  constructor(e, n, i, r, s) {
    this.id = e, this.label = n, this.min = i, this.max = r, this.step = s, this.component = document.createElement("div");
  }
  render(e) {
    const n = e.get(this.id), i = typeof n == "number" ? n.toFixed(2) : "N/A", r = Z`
      <div class="slider-container" style=${C(_l)}>
        <label
          for="${this.id}"
          id="${this.id}-label"
          style=${C(vl)}
          >${this.label}: ${i}</label
        >

        <div style="display: flex; justify-content: space-between;">
          <span style=${C(zn)}>0</span>
          <input
            type="range"
            id="${this.id}"
            min="${this.min}"
            max="${this.max}"
            step="${this.step}"
            style=${C(yl)}
            .value="${typeof n == "number" ? n : 0}"
            @change="${(s) => {
      e.set(this.id, +s.target.value), e.save_changes();
    }}"
          />
          <span style=${C(zn)}>1</span>
        </div>
      </div>
    `;
    return Et(r, this.component), this.component;
  }
  update(e) {
    console.log("update", e);
    const n = e.toFixed(2), i = this.component.querySelector("label"), r = this.component.querySelector("input"), s = document.getElementById("rd-title");
    console.log(i, r), i && (i.textContent = `${this.label}: ${n}`), r && (r.value = e.toString()), console.log(s), s && s.textContent && (s.textContent = `${s.textContent.split(",")[0]}, ${e})-Stable Projection`);
  }
}
class $e {
  constructor(e, n) {
    this.id = e, this.label = n;
  }
  render(e) {
    return Z`
      <label style="font-size: 18px;">
        <input
          type="checkbox"
          id="${this.id}"
          .checked="${e.get(this.id)}"
          width="100%"
          @change="${(n) => {
      e.set(this.id, n.target.checked), e.save_changes();
    }}"
        />
        ${this.label}
      </label>
    `;
  }
}
const wl = {
  maxWidth: "350px",
  width: "300px"
}, bl = {
  "font-size": "2.5em",
  "font-weight": "bold",
  "margin-bottom": "10px"
}, $l = {
  display: "flex",
  "flex-direction": "row",
  "justify-content": "space-between",
  "align-items": "center",
  "margin-bottom": "10px",
  maxWidth: "300px",
  width: "100%"
}, Al = {
  display: "flex",
  "flex-direction": "column",
  "margin-bottom": "10px",
  maxWidth: "300px",
  width: "100%"
};
class Ml {
  constructor() {
    this.container = document.createElement("div"), this.sliders = [
      new xl("distance", "Distance", 0.01, 1, 0.01)
      // new Slider("sensitivity", "Sensitivity", 0.01, 1, 0.01),
    ], this.checkboxes = [
      new $e("show_unstables", "Unstables"),
      new $e("show_neighbors", "Neighbors"),
      new $e("show_ghosts", "Ghosts")
    ];
  }
  update(e, n) {
    var r;
    ["distance", "sensitivity"].includes(e) && typeof n == "number" && ((r = this.sliders.find((s) => s.id === e)) == null || r.update(n), console.log(this.sliders.find((s) => s.id === e))), ["show_neighbors", "show_ghosts", "show_unstables"].includes(e) && W("#" + e).attr("checked", n);
  }
  render(e) {
    const n = Z`
      <div class="settings-container" style=${C(wl)}>
        <div style=${C(bl)}>Settings</div>
        <div style=${C($l)}>
          ${this.checkboxes.map((i) => i.render(e))}
        </div>
        <div style=${C(Al)}>
          ${this.sliders.map(
      (i) => Z` <div>${i.render(e)}</div> `
    )}
        </div>
      </div>
    `;
    return Et(n, this.container), this.container;
  }
}
class kl {
  constructor() {
    this.container = document.createElement("div");
  }
  update(e, n) {
    const i = Z`
      <div id="unstableInfo">
        Number of Unstables: ${e || 0}
        (${(n == null ? void 0 : n.toFixed(4)) || 0}%)
      </div>
    `;
    Et(i, this.container);
  }
  render(e, n) {
    return this.update(e, n), this.container;
  }
}
const El = {
  height: "100%",
  maxHeight: "360px",
  "max-width": "250px",
  "overflow-y": "auto",
  border: "1px solid #ccc",
  padding: "5px",
  "margin-top": "5px",
  "font-size": "0.9em",
  color: "#555"
}, Sl = {
  display: "flex",
  "align-items": "center",
  "margin-bottom": "2px"
};
class Nl {
  constructor() {
    this.container = document.createElement("div");
  }
  onClick(e, n, i, r) {
    const s = i();
    r(
      n ? [...s, e] : s.filter((o) => o !== e)
    );
  }
  updateCheckbox(e) {
    console.log("updateCheckbox", e), nn(".unstable-list input").property("checked", !1), e.forEach((n) => {
      W(`#unstable-${n}`).property("checked", !0);
    });
  }
  reset() {
    nn(".unstable-list input").property("checked", !1);
  }
  update(e, n, i) {
    const r = e.sort((o, a) => a.instability - o.instability), s = Z`
      <div class="unstable-list" style=${C(El)}>
        ${r.length ? r.map(
      (o) => Z`
                <div style=${C(Sl)}>
                  <input
                    type="checkbox"
                    id="unstable-${o.id}"
                    name="unstable-${o.id}"
                    @click=${(a) => this.onClick(
        o.id,
        a.target.checked,
        n,
        i
      )}
                  />
                  <label for="unstable-${o.id}" style="margin-left: 5px;"
                    >${o.id}
                  </label>
                </div>
              `
    ) : Z`<div>None</div>`}
      </div>
    `;
    Et(s, this.container);
  }
  render(e, n, i) {
    return this.update(e, n, i), this.container;
  }
}
const In = {
  "margin-top": "10px",
  "font-size": "18px"
}, Tl = {
  "font-size": "2.5em",
  "font-weight": "bold"
}, Cl = {
  maxWidth: "300px",
  width: "300px"
};
class zl {
  constructor() {
    this.container = document.createElement("div"), this.unstableCounter = new kl(), this.unstableIDList = new Nl();
  }
  update(e, n, i, r, s) {
    this.unstableCounter.update(n, i), this.unstableIDList.update(e, r, s);
  }
  updateCheckbox(e) {
    this.unstableIDList.updateCheckbox(e);
  }
  render(e, n, i, r, s) {
    const o = Z`
      <div style=${C(Cl)}>
        <div style=${C(Tl)}>Unstable Points</div>
        <div style=${C(In)}>
          ${this.unstableCounter.render(n, i)}
        </div>
        <div style=${C(In)}>
          ${this.unstableIDList.render(e, r, s)}
        </div>
      </div>
    `;
    return Et(o, this.container), this.container;
  }
}
class Il {
  constructor(e, n) {
    this.width = e, this.height = n, this.svg = this.createSVG(), this.symbolLegend = this.svg.append("g"), this.labelLegend = this.svg.append("g"), this.ghostColorLegend = this.svg.append("g");
  }
  createSVG() {
    return Yn("svg").attr("class", "legend").attr("width", `${this.width}px`).attr("height", `${this.height}px`);
  }
  renderSymbolLegend() {
    const e = [
      { label: "Unstable", symbol: _i },
      { label: "Ghost", symbol: vi },
      { label: "Neighbor", symbol: xi }
    ];
    this.symbolLegend.attr("transform", "translate(20, 150)"), this.symbolLegend.selectAll("path").data(e).join("path").attr(
      "d",
      ge().type((n) => n.symbol).size(200)
    ).attr("transform", (n, i) => `translate(0, ${20 + i * 28})`).attr("fill", "none").attr("stroke", "black").attr("stroke-width", 1), this.symbolLegend.selectAll("text").data(e).join("text").text((n) => n.label).attr("x", 20).attr("y", (n, i) => 22 + i * 28).attr("alignment-baseline", "middle").attr("font-size", "18px");
  }
  renderLabelLegend(e, n, i) {
    e.length === 0 && Object.keys(n).length === 0 || (this.labelLegend.attr("transform", "translate(20, 260)"), e.length ? n = e.reduce((r, s, o) => (r[s] = mi[o % 10], r), {}) : e = Object.keys(n), this.labelLegend.selectAll("circle").data(e).join("circle").attr("cx", 0).attr("cy", (r, s) => 10 + s * 23).attr("r", 7).attr("fill", (r, s) => i.colorScale(s.toString())), this.labelLegend.selectAll("text").data(e).join("text").text((r) => r).attr("x", 15).attr("y", (r, s) => 11 + s * 23).attr("alignment-baseline", "middle").attr("font-size", "18px"));
  }
  renderGhostLegend(e) {
    const n = pi(bt("#000000", "#ffffff")).domain([0, 1]);
    this.ghostColorLegend.attr("transform", "translate(10, 80)"), this.svg.append("defs").append("linearGradient").attr("id", "ghost-gradient").attr("x1", "0%").attr("x2", "100%").attr("y1", "0%").attr("y2", "0%").selectAll("stop").data(Ln(0, 1.01, 0.01)).enter().append("stop").attr("offset", (r) => `${r * 100}%`).attr("stop-color", (r) => n(r)), this.ghostColorLegend.append("rect").attr("x", 0).attr("y", 20).attr("width", 150).attr("height", 20).style("fill", "url(#ghost-gradient)"), this.ghostColorLegend.append("text").attr("x", 0).attr("y", 10).attr("alignment-baseline", "middle").attr("font-size", "18px").text("Ghost Color Scale"), this.ghostColorLegend.append("text").attr("x", 0).attr("y", 50).attr("alignment-baseline", "middle").attr("font-size", "16px").text("0"), this.ghostColorLegend.append("text").attr("x", 160).attr("y", 50).attr("alignment-baseline", "middle").attr("font-size", "16px").attr("text-anchor", "middle").text(`${e.toString()} (r)`);
  }
  render(e, n, i, r) {
    return this.renderSymbolLegend(), this.renderLabelLegend(e, n, r), this.renderGhostLegend(i), this.svg.node();
  }
  update(e, n, i) {
    this.renderLabelLegend(e, n, i);
  }
}
const Rl = {
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between",
  height: "100%",
  "padding-right": "30px"
}, Ll = {
  display: "flex",
  flexDirection: "row"
}, Pl = {
  display: "flex",
  flexDirection: "row",
  justifyContent: "center",
  alignItems: "center",
  border: "none",
  width: "100%",
  margin: 0,
  padding: 0,
  backgroundColor: "#fff",
  color: "#333"
}, Hl = {
  width: "100%",
  padding: "5px"
}, Dl = {
  padding: "5px"
};
function Ul(t, e, n, i, r, s) {
  const o = () => {
    const { origEmb: l, unstEmb: c, scales: h, legend: d, colors: g } = vt(t);
    s([]);
    const m = Ue(t, c, l.length);
    e.updateEmbedding(l, c, h, s), n.update(d, g, h), i.update("distance", t.get("distance")), r.update(
      c,
      m.numUnstables,
      m.percentUnstables,
      () => t.get("checkedUnstables"),
      s
    );
  }, a = (l) => {
    const { origEmb: c, unstEmb: h, scales: d } = vt(t), { numUnstables: g, percentUnstables: m } = Ue(
      t,
      h,
      c.length
    );
    s([]), e.updateUnstEmbedding(h, d, s), i.update(l, t.get(l)), r.update(
      h,
      g,
      m,
      () => t.get("checkedUnstables"),
      s
    );
  }, u = (l) => {
    const { unstEmb: c } = vt(t), h = `show_${l}`;
    e.setVisibility(l, t.get(h), c), i.update(h, t.get(h));
  };
  t.on("change:embedding_id", o), t.on("change:distance", () => a("distance")), t.on("change:sensitivity", () => a("sensitivity")), t.on("change:show_unstables", () => u("unstables")), t.on("change:show_neighbors", () => u("neighbors")), t.on("change:show_ghosts", () => u("ghosts")), t.on("change:unstableInfo", () => {
    const { unstEmb: l } = vt(t), c = t.get("unstableInfo");
    r.update(
      l,
      c.numUnstables,
      c.percentUnstables,
      () => t.get("checkedUnstables"),
      s
    );
  }), t.on("change:checkedUnstables", () => {
    const { origEmb: l, unstEmb: c, ghostEmb: h, scales: d } = vt(t), g = t.get("checkedUnstables");
    console.log("checkedUnstables", g), g.length === 0 ? e.resetDetail(c, d, s) : e.updateDetail(l, h, d, g), r.updateCheckbox(g);
  });
}
function Vl({ model: t, el: e }) {
  const n = document.createElement("div");
  console.log(t.get("embedding_id"), t.get("embedding_set"));
  const i = new il(
    t.get("width"),
    t.get("height")
  ), r = new Il(
    t.get("legend_width"),
    t.get("legend_height")
  ), s = new Ml(), o = new zl(), a = (x) => {
    t.set("checkedUnstables", x), t.save_changes();
  }, { origEmb: u, unstEmb: l, scales: c, legend: h, colors: d, radius: g } = vt(t), m = Ue(t, l, u.length);
  Et(
    Z` <div
      id="widget-container"
      class="container"
      style=${C(Pl)}
    >
      <div
        class="row"
        style="width:100%;display:flex;flex-direction:row; margin: 20px;"
      >
        <div class="col-md-3 left" style=${C(Rl)}>
          <div class="toolbar">${s.render(t)}</div>
          <div class="unstable-container">
            ${o.render(
      l,
      m.numUnstables,
      m.percentUnstables,
      () => t.get("checkedUnstables"),
      a
    )}
          </div>
        </div>
        <div class="col-md-9 scatterplot" style=${C(Ll)}>
          <div style="display: flex; flex-direction: column; ">
            <div
              style="font-size: 2.5em; font-weight: bold; margin-bottom: 10px;"
              id="rd-title"
            >
              (${g}, ${t.get("distance")})-Stable Projection
            </div>

            <div
              style="display: flex; flex-direction: row; justify-content: space-between;"
            >
              <div class="projection" style=${C(Hl)}>
                ${i.render(
      u,
      l,
      c,
      a
    )}
              </div>
              <div class="legend" style=${C(Dl)}>
                ${r.render(h, d, g, c)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>`,
    n
  ), Ul(
    t,
    i,
    r,
    s,
    o,
    a
  ), e.appendChild(n);
}
const Fl = { render: Vl };
export {
  Fl as default
};
