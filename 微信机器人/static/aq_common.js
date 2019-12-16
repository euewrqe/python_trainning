/**
 * Created by nextgo on 2017/10/17 0017.
 */
!function () {
    /**
     *
     * @param n{string} 字符串
     * @param t{object} 键值对
     * @returns {string}
     */
    function n(n, t) {
        for (var e = new Array, o = 0; o < n.length; o++)if ("&" == n.charAt(o)) {
            var r = [3, 4, 5, 9], a = 0;
            for (var c in r) {
                var i = r[c];
                if (o + i <= n.length) {
                    var m = n.substr(o, i).toLowerCase();
                    console.log(m)
                    if (t[m]) {
                        e.push(t[m]), o = o + i - 1, a = 1;
                        break
                    }
                }
            }
            0 == a && e.push(n.charAt(o))
        } else e.push(n.charAt(o));
        return e.join("")
    }

    function t() {
        for (var t = new Object, e = "'\"<>`script:daex/hml;bs64,", o = 0; o < e.length; o++) {
            for (var r = e.charAt(o), a = r.charCodeAt(), c = a, i = a.toString(16), u = 0; u < 7 - a.toString().length; u++)c = "0" + c;
            t["&#" + a + ";"] = r, t["&#" + c] = r, t["&#x" + i] = r
        }
        t["&lt"] = "<", t["&gt"] = ">", t["&quot"] = '"';
        var p = location.href, s = document.referrer;
        p = decodeURIComponent(n(p, t)), s = decodeURIComponent(n(s, t));
        var d = new RegExp("['\"<>`]|script:|data:text/html;base64,");
        if (d.test(p) || d.test(s)) {
            var l = "2", f = h[1], g = new Image;
            if (Math.random() < .1) {
                var q = h[3];
                m(q + "?v=" + l + "&u=" + encodeURIComponent(p) + "&r=" + encodeURIComponent(s))
            }
            g.src = f + "?v=" + l + "&u=" + encodeURIComponent(p) + "&r=" + encodeURIComponent(s), p = p.replace(/['\"<>`]|script:/gi, "M"), p = p.replace(/data:text\/html;base64,/gi, "data:text/plain;base64,"), location.href = encodeURI(p)
        }
    }

    function e(n) {
        return document.createElement(n)
    }

    function o(n, t, o) {
        var r = e("form");
        return r.action = n, r.method = o, r.target = t, r.style.display = "none", r
    }

    function r(n, t) {
        var o = e("input");
        return o.name = n, o.value = t, o
    }

    function a(n) {
        var t = e("iframe");
        return t.name = n, t.src = "javascript:void(0);", t.style.display = "none", t
    }

    function c(n) {
        n && n.parentNode && n.parentNode.removeChild(n)
    }

    function i(n) {
        var t = n.url, e = n.data, i = "aq_form" + 1e17 * Math.random(), m = o(t, i, "post"), u = a(i);
        document.body.appendChild(u), u.contentWindow.name = i;
        for (var p in e)m.appendChild(r(p, e[p]));
        document.body.appendChild(m), m && m.submit(), setTimeout(function () {
            c(m), c(u)
        }, 2e3)
    }

    function m(n) {
        var t = new Image;
        t.src = n
    }

    function u() {
        var n = navigator.plugins, t = "";
        if (n && n.length) {
            t = [];
            for (var e = 0; e < n.length; e++) {
                var o = n[e].name, r = n[e].description;
                t.push(o + "::" + r)
            }
            t = t.join(";")
        }
        return t
    }

    function p() {
        var n = location.protocol, t = "";
        t = n.indexOf("https") >= 0 || n.indexOf("HTTPS") >= 0 ? "https" : n.indexOf("http") >= 0 || n.indexOf("HTTP") >= 0 ? "http" : n, m(h[2] + "?host=" + encodeURIComponent(location.host) + "&p=" + encodeURIComponent(t) + "&hp=0&tk=" + +new Date)
    }

    function s(n) {
        return m(h[2] + "?host=" + encodeURIComponent(location.host) + "&data=" + n + "&hp=1&tk=" + +new Date), !0
    }

    var h = ["https://aq.qq.com/cn2/manage/mbtoken/hijack_sec_js_report", "https://zyjc.sec.qq.com/dom", "https://aq.qq.com/cn2/manage/mbtoken/hijack_pv_report", "https://aq.qq.com/cn2/manage/mbtoken/hijack_xss_report", "https://aq.qq.com/cn2/manage/mbtoken/hijack_mv_js_report"], d = Math.random(), l = .01, f = !1;
    t(), function (n, t, e) {
        function o(o, a, c) {
            var i, m, u = {bid: a, childUrl: "", parentUrl: ""};
            try {
                u.childUrl = e.href
            } catch (s) {
            }
            try {
                u.parentUrl = parent.location.href
            } catch (s) {
            }
            if (1 == c)try {
                m = parent != n && g(parent.document, "datapp", u)
            } catch (s) {
            } else {
                try {
                    i = g(t, "datapt", u), m = parent != n && p(parent.document, "datapp", u)
                } catch (s) {
                }
                try {
                    parent != n && r(u)
                } catch (s) {
                }
            }
        }

        function r(n) {
            if (x(n.parentUrl)) {
                var t = [];
                t.push("beframed::url"), a(t, "beframed", n)
            }
        }

        function a(n, t, e) {
            h[0], new Image;
            if (n.push("childUrl::" + encodeURIComponent(e.childUrl)), n.push("parentUrl::" + encodeURIComponent(e.parentUrl)), !f && d < l && (f = s(n.join("|"))), Math.random() < .9)return !1;
            var o = {id: e.bid, imark: t, data: n.join("|")};
            return Math.random() < .5 && (o.dom = encodeURIComponent(document.documentElement.outerHTML), o.plgs = encodeURIComponent(u())), i({
                data: o,
                url: h[0]
            }), !0
        }

        function c(n, t, e) {
            try {
                var o = location.host;
                if ("m.v.qq.com" != o && "v.qq.com" != o && retrun, Math.random() > .1)return !1;
                m([], t, e)
            } catch (r) {
            }
        }

        function m(n, t, e) {
            try {
                var o = h[4], r = new Image;
                return n.push("childUrl::" + encodeURIComponent(e.childUrl)), n.push("parentUrl::" + encodeURIComponent(e.parentUrl)), r.src = o + "?id=" + e.bid + "&imark=" + t + "&data=" + n.join("|") + "&random=" + Math.random(), !0
            } catch (a) {
            }
        }

        function p(n, t, e) {
            x(e.parentUrl) && g(n, t, e)
        }

        function g(n, t, e) {
            c(n, t, e);
            var o = q(n), r = R(n), i = M(n), m = j(n), u = E(n), p = v(n), s = y(n), h = U(n), d = o.concat(r, i, u, m, p, s, h);
            return !(d.length <= 0) && (d = T(d), void a(d, t, e))
        }

        function q(n) {
            for (var t, e, o, r, a, c = n.getElementsByTagName("script"), i = [], m = 0; m < c.length; m++)t = c[m], (e = t.src) && i.push(e);
            return o = w(i, x), r = I("script"), a = C(o, r)
        }

        function v(n) {
            for (var t, e, o, r, a, c = n.getElementsByTagName("source"), i = [], m = 0; m < c.length; m++)t = c[m], (e = t.src) && i.push(e);
            return o = w(i, x), r = I("source"), a = C(o, r)
        }

        function y(n) {
            for (var t, e, o, r, a, c = n.getElementsByTagName("video"), i = [], m = 0; m < c.length; m++)t = c[m], (e = t.src) && i.push(e);
            return o = w(i, x), r = I("video"), a = C(o, r)
        }

        function U(n) {
            for (var t, e, o, r, a, c = n.getElementsByTagName("object"), i = [], m = 0; m < c.length; m++)t = c[m], (e = t.data) && i.push(e);
            return o = w(i, x), r = I("object"), a = C(o, r)
        }

        function w(n, t) {
            for (var e = [], o = 0; o < n.length; ++o) {
                var r = n[o];
                t(r) && e.push(r)
            }
            return e
        }

        function x(n) {
            var t, e, o, r, a, c = b(n);
            return !!c && (t = /^xui.ptlogin2?\.?$/i, e = /(\.|^)(qq|paipai|soso|wenwen|tenpay|macromedia|gtimg|qstatic|qqmail|paipaiimg|qqgames|pengyou|foxmail|qzoneapp|qzone|qplus|imqq|tqapp|tencent|3366|21mmo|taotao|imrworldwide|idqqimg|17roco|expo2010china|fangqq|tencentmind|tencity|yingkebicheng|zhangzhongxing|expovol|otaworld|gzyunxun|heyyo|himoral|himorale|myrtx|qqwinner|redian|sjkx|rtxonline|nbaso|paipai\.500wan|qqjapan|qq\.salewell|sogou|weiyun|flzhan|wechat|webplat\.ied|qcloud)\.com$/i, o = /(\.|^)(qq\.com|gtimg|gtimg\.com|qlogo|foxmail\.com|gtimg\.com|url|qpic|tencent\.com|expo2010|expo|himorale\.com|nbaso\.com|qqtest\.com|qq\.ucar|rtx\.com|soso\.com|tcimage|taoche)\.cn$/i, r = /(\.|^)(5999|gongyi)\.net$/i, a = /(\.|^)(himorale\.com\.hk|tencent\.com\.hk|qq\.chinacache\.net|qq\.com\.fastcdn\.com|qq\.com\.lxdns\.com|qq\.fastcdn\.com|soso\.com\.lxdns\.com|motu\.pagechoice\.net|ope\.tanx\.com|dap\.gentags\.net|widget\.weibo\.com)$/i, !(t.test(c) || e.test(c) || o.test(c) || r.test(c) || a.test(c)))
        }

        function b(n) {
            var t = /^https?:\/\/([\w\-]+\.[\w\-.]+)/i, e = t.exec(n);
            if (e)return e[1]
        }

        function I(n) {
            return function (t) {
                return n + "::" + encodeURIComponent(t)
            }
        }

        function C(n, t) {
            for (var e, o, r = [], a = 0; a < n.length; ++a)e = n[a], o = t(e), r.push(o);
            return r
        }

        function R(n) {
            var t = "IFRAME", e = function (n) {
                return n.src
            }, o = I("iframe");
            return k(n, t, e, x, o)
        }

        function j(n) {
            var t = "EMBED", e = function (n) {
                return n.src
            }, o = I("embed");
            return k(n, t, e, x, o)
        }

        function k(n, t, e, o, r) {
            var a = n.getElementsByTagName(t), c = C(a, e), i = w(c, o), m = C(i, r);
            return m
        }

        function M(n) {
            var t = "FRAME", e = function (n) {
                return n.src
            }, o = I("frame");
            return k(n, t, e, x, o)
        }

        function E(n) {
            var t = "IMG", e = function (n) {
                return n.src
            }, o = I("img");
            return k(n, t, e, x, o)
        }

        function T(n) {
            var t = n.slice(0), e = [];
            t.sort(), e.push(t[0]);
            for (var o = 1; o < t.length; o += 1)t[o] != t[o - 1] && e.push(t[o]);
            return e
        }

        try {
            setTimeout(function () {
                o(.1, 100, 0)
            }, 5e3)
        } catch (_) {
        }
    }(window, document, location), d < l && p()
}();