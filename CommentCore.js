function AcfunParser(t) {
    function e(t) {
        for (; t.length < 6;) t = "0" + t;
        return t
    }
    var o = [];
    try {
        var i = JSON.parse(t)
    } catch (s) {
        return console.log("Error: Could not parse json list!"), []
    }
    for (var r = 0; r < i.length; r++) {
        var a = {},
            n = i[r].c.split(",");
        if (n.length > 0) {
            if (a.stime = 1e3 * parseFloat(n[0]), a.color = "#" + e(parseInt(n[1]).toString(16)), a.mode = parseInt(n[2]), a.size = parseInt(n[3]), a.hash = n[4], a.date = parseInt(n[5]), a.position = "relative", 7 != a.mode ? (a.text = i[r].m.replace(/(\/n|\\n|\n|\r\n|\\r)/g, "\n"), a.text = a.text.replace(/\r/g, "\n"), a.text = a.text.replace(/\s/g, " ")) : a.text = i[r].m, 7 == a.mode) {
                try {
                    var l = JSON.parse(a.text)
                } catch (s) {
                    console.log("[Err] Error parsing internal data for comment"), console.log("[Dbg] " + a.text);
                    continue
                }
                a.text = l.n, a.text = a.text.replace(/\ /g, " "), console.log(a.text), null != l.p ? (a.x = l.p.x / 1e3, a.y = l.p.y / 1e3) : (a.x = 0, a.y = 0), a.shadow = l.b, a.duration = 4e3, null != l.l && (a.moveDelay = 1e3 * l.l), null != l.z && l.z.length > 0 && (a.movable = !0, a.toX = l.z[0].x / 1e3, a.toY = l.z[0].y / 1e3, a.alphaTo = l.z[0].t, a.colorTo = l.z[0].c, a.moveDuration = null != l.z[0].l ? 1e3 * l.z[0].l : 500, a.duration = a.moveDelay + a.moveDuration), null != l.r && null != l.k && (a.rX = l.r, a.rY = l.k), l.a && (a.alphaFrom = l.a)
            }
            o.push(a)
        }
    }
    return o
}

function BilibiliParser(t, e) {
    function o(t) {
        for (; t.length < 6;) t = "0" + t;
        return t
    }

    function i(t) {
        return t.replace(/\t/, "\\t")
    }
    if (null !== t) var s = t.getElementsByTagName("d");
    else {
        var r = document.createElement("div");
        r.innerHTML = e;
        var s = r.getElementsByTagName("d")
    }
    for (var a = [], n = 0; n < s.length; n++)
        if (null != s[n].getAttribute("p")) {
            var l = s[n].getAttribute("p").split(",");
            if (!s[n].childNodes[0]) continue;
            var e = s[n].childNodes[0].nodeValue,
                h = {};
            if (h.stime = Math.round(parseFloat(1e3 * l[0])), h.size = parseInt(l[2]), h.color = "#" + o(parseInt(l[3]).toString(16)), h.mode = parseInt(l[1]), h.date = parseInt(l[4]), h.pool = parseInt(l[5]), h.position = "absolute", null != l[7] && (h.dbid = parseInt(l[7])), h.hash = l[6], h.border = !1, h.mode < 7) h.text = e.replace(/(\/n|\\n|\n|\r\n)/g, "\n");
            else if (7 == h.mode) try {
                adv = JSON.parse(i(e)), h.shadow = !0, h.x = parseInt(adv[0]), h.y = parseInt(adv[1]), h.text = adv[4].replace(/(\/n|\\n|\n|\r\n)/g, "\n"), h.rZ = 0, h.rY = 0, adv.length >= 7 && (h.rZ = parseInt(adv[5]), h.rY = parseInt(adv[6])), h.movable = !1, adv.length >= 11 && (h.movable = !0, h.toX = adv[7], h.toY = adv[8], h.moveDuration = 500, h.moveDelay = 0, "" != adv[9] && (h.moveDuration = adv[9]), "" != adv[10] && (h.moveDelay = adv[10]), adv.length > 11 && (h.shadow = adv[11], "true" === h.shadow && (h.shadow = !0), "false" === h.shadow && (h.shadow = !1), null != adv[12] && (h.font = adv[12]))), h.duration = 2500, adv[3] < 12 && (h.duration = 1e3 * adv[3]), h.alphaFrom = 1, h.alphaTo = 1;
                var r = adv[2].split("-");
                null != r && r.length > 1 && (h.alphaFrom = parseFloat(r[0]), h.alphaTo = parseFloat(r[1]))
            } catch (d) {
                console.log("[Err] Error occurred in JSON parsing"), console.log("[Dbg] " + e)
            } else 8 == h.mode && (h.code = e);
            null != h.text && (h.text = h.text.replace(/\u25a0/g, "█")), a.push(h)
        }
    return a
}

function CommentFilter() {
    this.rulebook = {
        all: []
    }, this.modifiers = [], this.runtime = null, this.allowTypes = {
        1: !0,
        4: !0,
        5: !0,
        6: !0,
        7: !0,
        8: !0,
        17: !0
    }, this.doModify = function (t) {
        for (var e = 0; e < this.modifiers.length; e++) t = this.modifiers[e](t);
        return t
    }, this.isMatchRule = function (t, e) {
        switch (e.operator) {
        case "==":
            if (t[e.subject] == e.value) return !1;
            break;
        case ">":
            if (t[e.subject] > e.value) return !1;
            break;
        case "<":
            if (t[e.subject] < e.value) return !1;
            break;
        case "range":
            if (t[e.subject] > e.value.min && t[e.subject] < e.value.max) return !1;
            break;
        case "!=":
            if (t[e.subject] != e.value) return !1;
            break;
        case "~":
            if (new RegExp(e.value).test(t[e[subject]])) return !1;
            break;
        case "!~":
            if (!new RegExp(e.value).test(t[e[subject]])) return !1
        }
        return !0
    }, this.beforeSend = function (t) {
        var e = t.data.mode;
        if (null != this.rulebook[e]) {
            for (var o = 0; o < this.rulebook[e].length; o++)
                if ("width" == this.rulebook[e][o].subject || "height" == this.rulebook[e][o].subject)
                    if ("width" == this.rulebook[e][o].subject) switch (this.rulebook[e][o].operator) {
                    case ">":
                        if (this.rulebook[e][o].value < t.offsetWidth) return !1;
                        break;
                    case "<":
                        if (this.rulebook[e][o].value > t.offsetWidth) return !1;
                        break;
                    case "range":
                        if (this.rulebook[e][o].value.max > t.offsetWidth && this.rulebook[e][o].min < t.offsetWidth) return !1;
                        break;
                    case "==":
                        if (this.rulebook[e][o].value == t.offsetWidth) return !1
                    } else switch (this.rulebook[e][o].operator) {
                    case ">":
                        if (this.rulebook[e][o].value < t.offsetHeight) return !1;
                        break;
                    case "<":
                        if (this.rulebook[e][o].value > t.offsetHeight) return !1;
                        break;
                    case "range":
                        if (this.rulebook[e][o].value.max > t.offsetHeight && this.rulebook[e][o].min < t.offsetHeight) return !1;
                        break;
                    case "==":
                        if (this.rulebook[e][o].value == t.offsetHeight) return !1
                    }
                    return !0
        }
        return !0
    }, this.doValidate = function (t) {
        if (!this.allowTypes[t.mode]) return !1;
        var e = {
            text: t.text,
            mode: t.mode,
            color: t.color,
            size: t.size,
            stime: t.stime,
            hash: t.hash
        };
        if (null != this.rulebook[t.mode] && this.rulebook[t.mode].length > 0)
            for (var o = 0; o < this.rulebook[t.mode]; o++)
                if (!this.isMatchRule(e, this.rulebook[t.mode][o])) return !1;
        for (var o = 0; o < this.rulebook[t.mode]; o++)
            if (!this.isMatchRule(e, this.rulebook[t.mode][o])) return !1;
        return !0
    }, this.addRule = function (t) {
        switch (null == this.rulebook[t.mode + ""] && (this.rulebook[t.mode + ""] = []), t.operator) {
        case "eq":
        case "equals":
        case "=":
            t.operator = "==";
            break;
        case "ineq":
            t.operator = "!=";
            break;
        case "regex":
        case "matches":
            t.operator = "~";
            break;
        case "notmatch":
        case "iregex":
            t.operator = "!~"
        }
        return this.rulebook[t.mode].push(t), this.rulebook[t.mode].length - 1
    }, this.addModifier = function (t) {
        this.modifiers.push(t)
    }, this.runtimeFilter = function (t) {
        return null == this.runtime ? t : this.runtime(t)
    }, this.setRuntimeFilter = function (t) {
        this.runtime = t
    }
}

function CommentSpaceAllocator(t, e) {
    this.width = t, this.height = e, this.dur = 4e3, this.pools = [
        []
    ], this.pool = this.pools[0], this.setBounds = function (t, e) {
        this.width = t, this.height = e
    }, this.add = function (t) {
        t.height >= this.height ? (t.cindex = this.pools.indexOf(this.pool), t.style.top = "0px") : (t.cindex = this.pools.indexOf(this.pool), t.style.top = this.setY(t) + "px")
    }, this.remove = function (t) {
        var e = this.pools[t.cindex];
        e.remove(t)
    }, this.validateCmt = function (t) {
        return t.bottom = t.offsetTop + t.offsetHeight, t.y = t.offsetTop, t.x = t.offsetLeft, t.right = t.offsetLeft + t.offsetWidth, t.w && t.h ? (t.width = t.w, t.height = t.h) : (t.height = t.offsetHeight, t.width = t.offsetWidth), t.top = t.offsetTop, t.left = t.offsetLeft, t
    }, this.setY = function (t, e) {
        if (!e) var e = 0;
        if (t = this.validateCmt(t), this.pools.length <= e && this.pools.push([]), this.pool = this.pools[e], 0 == this.pool.length) return this.pool.push(t), 0;
        if (this.vCheck(0, t)) return this.pool.binsert(t, function (t, e) {
            return t.bottom < e.bottom ? -1 : t.bottom == e.bottom ? 0 : 1
        }), t.y;
        for (var o = 0, i = 0; i < this.pool.length && (o = this.pool[i].bottom + 1, !(o + t.offsetHeight > this.height)); i++)
            if (this.vCheck(o, t)) return this.pool.binsert(t, function (t, e) {
                return t.bottom < e.bottom ? -1 : t.bottom == e.bottom ? 0 : 1
            }), t.y;
        this.setY(t, e + 1)
    }, this.vCheck = function (t, e) {
        var o = t + e.height,
            i = e.x + e.width;
        this.validateCmt(e);
        for (var s = 0; s < this.pool.length; s++)
            if (this.pool[s] = this.validateCmt(this.pool[s]), !(this.pool[s].y > o || this.pool[s].bottom < t)) {
                if (this.pool[s].right < e.x || this.pool[s].x > i) {
                    if (this.getEnd(this.pool[s]) < this.getMiddle(e)) continue;
                    return !1
                }
                return !1
            }
        return e.y = t, e.bottom = e.height + t, !0
    }, this.getEnd = function (t) {
        return t.stime + t.ttl
    }, this.getMiddle = function (t) {
        return t.stime + t.ttl / 2
    }
}

function TopCommentSpaceAllocator(t, e) {
    var o = new CommentSpaceAllocator(t, e);
    o.add = function (t) {
        o.validateCmt(t), t.style.left = (o.width - t.width) / 2 + "px", t.height >= o.height ? (t.cindex = o.pools.indexOf(o.pool), t.style.top = "0px") : (t.cindex = o.pools.indexOf(o.pool), t.style.top = o.setY(t) + "px")
    }, o.vCheck = function (t, e) {
        for (var i = t + e.height, s = 0; s < o.pool.length; s++) {
            var r = o.validateCmt(o.pool[s]);
            if (!(r.y > i || r.bottom < t)) return !1
        }
        return e.y = t, e.bottom = e.bottom + t, !0
    }, this.setBounds = function (t, e) {
        o.setBounds(t, e)
    }, this.add = function (t) {
        o.add(t)
    }, this.remove = function (t) {
        o.remove(t)
    }
}

function BottomCommentSpaceAllocator(t, e) {
    var o = new CommentSpaceAllocator(t, e);
    o.add = function (t) {
        t.style.top = "", t.style.bottom = "0px", o.validateCmt(t), t.style.left = (o.width - t.width) / 2 + "px", t.height >= o.height ? (t.cindex = o.pools.indexOf(o.pool), t.style.bottom = "0px") : (t.cindex = o.pools.indexOf(o.pool), t.style.bottom = o.setY(t) + "px")
    }, o.validateCmt = function (t) {
        return t.y = o.height - (t.offsetTop + t.offsetHeight), t.bottom = t.y + t.offsetHeight, t.x = t.offsetLeft, t.right = t.offsetLeft + t.offsetWidth, t.height = t.offsetHeight, t.width = t.offsetWidth, t.top = t.y, t.left = t.offsetLeft, t
    }, o.vCheck = function (t, e) {
        for (var i = t + e.height, s = 0; s < o.pool.length; s++) {
            var r = o.validateCmt(o.pool[s]);
            if (!(r.y > i || r.bottom < t)) return !1
        }
        return e.y = t, e.bottom = e.bottom + t, !0
    }, this.setBounds = function (t, e) {
        o.setBounds(t, e)
    }, this.add = function (t) {
        o.add(t)
    }, this.remove = function (t) {
        o.remove(t)
    }
}

function ReverseCommentSpaceAllocator(t, e) {
    var o = new CommentSpaceAllocator(t, e);
    o.vCheck = function (t, e) {
        var o = t + e.height,
            i = e.x + e.width;
        this.validateCmt(e);
        for (var s = 0; s < this.pool.length; s++) {
            var r = this.validateCmt(this.pool[s]);
            if (!(r.y > o || r.bottom < t)) {
                if (r.x > i || r.right < e.x) {
                    if (this.getEnd(r) < this.getMiddle(e)) continue;
                    return !1
                }
                return !1
            }
        }
        return e.y = t, e.bottom = e.height + t, !0
    }, this.setBounds = function (t, e) {
        o.setBounds(t, e)
    }, this.add = function (t) {
        o.add(t)
    }, this.remove = function (t) {
        o.remove(t)
    }
}

function BottomScrollCommentSpaceAllocator(t, e) {
    var o = new CommentSpaceAllocator(t, e);
    o.validateCmt = function (t) {
        return t.y = o.height - (t.offsetTop + t.offsetHeight), t.bottom = t.y + t.offsetHeight, t.x = t.offsetLeft, t.right = t.offsetLeft + t.offsetWidth, t.height = t.offsetHeight, t.width = t.offsetWidth, t.top = t.y, t.left = t.offsetLeft, t
    }, o.add = function (t) {
        t.style.top = "", t.style.bottom = "0px", o.validateCmt(t), t.style.left = o.width + "px", t.height >= o.height ? (t.cindex = o.pools.indexOf(o.pool), t.style.bottom = "0px") : (t.cindex = o.pools.indexOf(o.pool), t.style.bottom = o.setY(t) + "px")
    }, this.setBounds = function (t, e) {
        o.setBounds(t, e)
    }, this.add = function (t) {
        o.add(t)
    }, this.remove = function (t) {
        o.remove(t)
    }
}

function CommentManager(t) {
    var e = 0;
    this.stage = t, this.def = {
        opacity: 1,
        globalScale: 1,
        scrollScale: 3
    }, this.timeline = [], this.runline = [], this.position = 0, this.limiter = 0, this.filter = null, this.csa = {
        scroll: new CommentSpaceAllocator(0, 0),
        top: new TopCommentSpaceAllocator(0, 0),
        bottom: new BottomCommentSpaceAllocator(0, 0),
        reverse: new ReverseCommentSpaceAllocator(0, 0),
        scrollbtm: new BottomScrollCommentSpaceAllocator(0, 0)
    }, this.stage.width = this.stage.offsetWidth, this.stage.height = this.stage.offsetHeight, this.initCmt = function (t, e) {
        return t.className = "cmt", t.stime = e.stime, t.mode = e.mode, t.data = e, 17 === t.mode || (t.appendChild(document.createTextNode(e.text)), t.innerText = e.text, t.style.fontSize = e.size + "px"), null != e.font && "" != e.font && (t.style.fontFamily = e.font), e.shadow === !1 && (t.className = "cmt noshadow"), "#000000" != e.color || !e.shadow && null != e.shadow || (t.className += " rshadow"), null != e.margin && (t.style.margin = e.margin), null != e.color && (t.style.color = e.color), 1 != this.def.opacity && 1 == e.mode && (t.style.opacity = this.def.opacity), null != e.alphaFrom && (t.style.opacity = e.alphaFrom), e.border && (t.style.border = "1px solid #00ffff"), t.ttl = Math.round(4e3 * this.def.globalScale), t.dur = t.ttl, (1 === t.mode || 6 === t.mode || 2 === t.mode) && (t.ttl *= this.def.scrollScale, t.dur = t.ttl), t
    }, this.startTimer = function () {
        if (!(e > 0)) {
            var t = (new Date).getTime(),
                o = this;
            e = window.setInterval(function () {
                var e = (new Date).getTime() - t;
                t = (new Date).getTime(), o.onTimerEvent(e, o)
            }, 10)
        }
    }, this.stopTimer = function () {
        window.clearInterval(e), e = 0
    }
}
Array.prototype.remove = function (t) {
    for (var e = 0; e < this.length; e++)
        if (this[e] == t) {
            this.splice(e, 1);
            break
        }
}, Array.prototype.bsearch = function (t, e) {
    if (0 == this.length) return 0;
    if (e(t, this[0]) < 0) return 0;
    if (e(t, this[this.length - 1]) >= 0) return this.length;
    for (var o = 0, i = 0, s = 0, r = this.length - 1; r >= o;) {
        if (i = Math.floor((r + o + 1) / 2), s++, e(t, this[i - 1]) >= 0 && e(t, this[i]) < 0) return i;
        e(t, this[i - 1]) < 0 ? r = i - 1 : e(t, this[i]) >= 0 ? o = i : console.error("Program Error"), s > 1500 && console.error("Too many run cycles.")
    }
    return -1
}, Array.prototype.binsert = function (t, e) {
    this.splice(this.bsearch(t, e), 0, t)
}, CommentManager.prototype.seek = function (t) {
    this.position = this.timeline.bsearch(t, function (t, e) {
        return t < e.stime ? -1 : t > e.stime ? 1 : 0
    })
}, CommentManager.prototype.validate = function (t) {
    return null == t ? !1 : this.filter.doValidate(t)
}, CommentManager.prototype.load = function (t) {
    this.timeline = t, this.timeline.sort(function (t, e) {
        return t.stime > e.stime ? 2 : t.stime < e.stime ? -2 : t.date > e.date ? 1 : t.date < e.date ? -1 : null != t.dbid && null != e.dbid ? t.dbid > e.dbid ? 1 : t.dbid < e.dbid ? -1 : 0 : 0
    })
}, CommentManager.prototype.clear = function () {
    for (var t = 0; t < this.runline.length; t++) this.finish(this.runline[t]), this.stage.removeChild(this.runline[t]);
    this.runline = []
}, CommentManager.prototype.setBounds = function () {
    for (var t in this.csa) this.csa[t].setBounds(this.stage.offsetWidth, this.stage.offsetHeight);
    this.stage.width = this.stage.offsetWidth, this.stage.height = this.stage.offsetHeight, this.stage.style.perspective = this.stage.width * Math.tan(40 * Math.PI / 180) / 2 + "px", this.stage.style.webkitPerspective = this.stage.width * Math.tan(40 * Math.PI / 180) / 2 + "px"
}, CommentManager.prototype.init = function () {
    this.setBounds(), null == this.filter && (this.filter = new CommentFilter)
}, CommentManager.prototype.time = function (t) {
    if (t -= 1, this.position >= this.timeline.length || Math.abs(this.lastPos - t) >= 2e3) {
        if (this.seek(t), this.lastPos = t, this.timeline.length <= this.position) return
    } else this.lastPos = t;
    for (; this.position < this.timeline.length && !(this.limiter > 0 && this.runline.length > this.limiter) && (this.validate(this.timeline[this.position]) && this.timeline[this.position].stime <= t); this.position++) this.sendComment(this.timeline[this.position])
}, CommentManager.prototype.rescale = function () {
    for (var t = 0; t < this.runline.length; t++) this.runline[t].dur = Math.round(this.runline[t].dur * this.def.globalScale), this.runline[t].ttl = Math.round(this.runline[t].ttl * this.def.globalScale)
}, CommentManager.prototype.sendComment = function (t) {
    if (8 === t.mode) return console.log(t), void(this.scripting && console.log(this.scripting.eval(t.code)));
    var e = document.createElement("div");
    if (null == this.filter || (t = this.filter.doModify(t), null != t)) {
        if (e = this.initCmt(e, t), this.stage.appendChild(e), e.width = e.offsetWidth, e.height = e.offsetHeight, e.style.width = e.w + 1 + "px", e.style.height = e.h - 3 + "px", e.style.left = this.stage.width + "px", null != this.filter && !this.filter.beforeSend(e)) return this.stage.removeChild(e), void(e = null);
        switch (e.mode) {
            default:
            case 1:
                this.csa.scroll.add(e);
            break;
        case 2:
            this.csa.scrollbtm.add(e);
            break;
        case 4:
            this.csa.bottom.add(e);
            break;
        case 5:
            this.csa.top.add(e);
            break;
        case 6:
            this.csa.reverse.add(e);
            break;
        case 17:
        case 7:
            if ("relative" !== e.data.position ? (e.style.top = e.data.y + "px", e.style.left = e.data.x + "px") : (e.style.top = e.data.y * this.stage.height + "px", e.style.left = e.data.x * this.stage.width + "px"), e.ttl = Math.round(t.duration * this.def.globalScale), e.dur = Math.round(t.duration * this.def.globalScale), 0 !== t.rY || 0 !== t.rZ) {
                var o = function (t, e) {
                    for (var o = Math.PI / 180, i = t * o, s = e * o, r = Math.cos, a = Math.sin, n = [r(i) * r(s), r(i) * a(s), a(i), 0, -a(s), r(s), 0, 0, -a(i) * r(s), -a(i) * a(s), r(i), 0, 0, 0, 0, 1], l = 0; l < n.length; l++) Math.abs(n[l]) < 1e-6 && (n[l] = 0);
                    return "matrix3d(" + n.join(",") + ")"
                };
                e.style.transformOrigin = "0% 0%", e.style.webkitTransformOrigin = "0% 0%", e.style.OTransformOrigin = "0% 0%", e.style.MozTransformOrigin = "0% 0%", e.style.MSTransformOrigin = "0% 0%", e.style.transform = o(t.rY, t.rZ), e.style.webkitTransform = o(t.rY, t.rZ), e.style.OTransform = o(t.rY, t.rZ), e.style.MozTransform = o(t.rY, t.rZ), e.style.MSTransform = o(t.rY, t.rZ)
            }
        }
        this.runline.push(e)
    }
}, CommentManager.prototype.finish = function (t) {
    switch (t.mode) {
        default:
        case 1:
            this.csa.scroll.remove(t);
        break;
    case 2:
        this.csa.scrollbtm.remove(t);
        break;
    case 4:
        this.csa.bottom.remove(t);
        break;
    case 5:
        this.csa.top.remove(t);
        break;
    case 6:
        this.csa.reverse.remove(t);
        break;
    case 7:
    }
}, CommentManager.prototype.onTimerEvent = function (t, e) {
    for (var o = 0; o < e.runline.length; o++) {
        var i = e.runline[o];
        if (!i.hold) {
            if (i.ttl -= t, 1 == i.mode || 2 == i.mode) i.style.left = i.ttl / i.dur * (e.stage.width + i.width) - i.width + "px";
            else if (6 == i.mode) i.style.left = (1 - i.ttl / i.dur) * (e.stage.width + i.width) - i.width + "px";
            else if ((4 == i.mode || 5 == i.mode || i.mode >= 7) && (null == i.dur && (i.dur = 4e3), null != i.data.alphaFrom && null != i.data.alphaTo && (i.style.opacity = (i.data.alphaFrom - i.data.alphaTo) * (i.ttl / i.dur) + i.data.alphaTo), 7 == i.mode && i.data.movable)) {
                var s = Math.min(Math.max(i.dur - i.data.moveDelay - i.ttl, 0), i.data.moveDuration) / i.data.moveDuration;
                "relative" !== i.data.position ? (i.style.top = (i.data.toY - i.data.y) * s + i.data.y + "px", i.style.left = (i.data.toX - i.data.x) * s + i.data.x + "px") : (i.style.top = ((i.data.toY - i.data.y) * s + i.data.y) * e.stage.height + "px", i.style.left = ((i.data.toX - i.data.x) * s + i.data.x) * e.stage.width + "px")
            }
            null != e.filter && (i = e.filter.runtimeFilter(i)), i.ttl <= 0 && (e.stage.removeChild(i), e.runline.splice(o, 1), e.finish(i))
        }
    }
};