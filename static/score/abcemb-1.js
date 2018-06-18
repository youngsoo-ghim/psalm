// abc2svg - ABC to SVG translator
// @source: https://github.com/moinejf/abc2svg.git
// Copyright (C) 2014-2017 Jean-Francois Moine - LGPL3+
// abcemb-1.js for abc2svg-1.17.2 (2018-05-18)
window.onerror = function(msg, url, line) {
    if (typeof msg == "string") alert("window error: " + msg + "\nURL: " + url + "\nLine: " + line);
    else if (typeof msg == "object") alert("window error: " + msg.type + " " + msg.target.src);
    else alert("window error: " + msg);
    return false
};
var errtxt = "",
    new_page = "",
    abc, playing, abcplay, playconf = {
        onend: endplay
    },
    page, a_src = [],
    a_pe = [],
    glop, old_gm, jsdir = document.currentScript ? document.currentScript.src.match(/.*\//) : function() {
        var scrs = document.getElementsByTagName("script");
        return scrs[scrs.length - 1].src.match(/.*\//) || ""
    }();
var user = {
    errmsg: function(msg, l, c) {
        errtxt += clean_txt(msg) + "\n"
    },
    img_out: function(str) {
        new_page += str
    },
    page_format: true
};

function clean_txt(txt) {
    return txt.replace(/<|>|&.*?;|&/g, function(c) {
        switch (c) {
            case "<":
                return "&lt;";
            case ">":
                return "&gt;";
            case "&":
                return "&amp;"
        }
        return c
    })
}

function endplay() {
    playing = false
}

function playseq(seq) {
    var outputs;
    if (!abcplay) {
        if (typeof AbcPlay == "undefined") {
            playseq = function() {};
            return
        }
        abcplay = AbcPlay(playconf);
        outputs = abcplay.get_outputs();
        if (outputs.length == 0) {
            playseq = function() {};
            return
        }
    }
    if (playing) {
        abcplay.stop();
        return
    }
    playing = true;
    if (!a_pe[seq]) {
        var abc = new abc2svg.Abc(user);
        abcplay.clear();
        abc.tosvg("play", "%%play");
        try {
            if (glop) abc.tosvg("abcemb", page, glop[0], glop[1]);
            abc.tosvg("abcemb" + seq, page, a_src[seq][0], a_src[seq][1])
        } catch (e) {
            alert(e.message + "\nabc2svg tosvg bug - stack:\n" + e.stack);
            playing = false;
            a_pe[seq] = null;
            return
        }
        a_pe[seq] = abcplay.clear()
    }
    abcplay.play(0, 1e5, a_pe[seq])
}

function dom_loaded() {
    if (typeof abc2svg != "object" || !abc2svg.modules) {
        setTimeout(dom_loaded, 500);
        return
    }
    abc2svg.loadjs = function(fn, relay, onerror) {
        var s = document.createElement("script");
        if (/:\/\//.test(fn)) s.src = fn;
        else s.src = jsdir + fn;
        s.type = "text/javascript";
        if (relay) s.onload = relay;
        s.onerror = onerror || function() {
            alert("error loading " + fn)
        };
        document.head.appendChild(s)
    };

//    var lines;
//    $.get(scoreURL, function(data) {
//        lines = data.split("\r");
//        console.log(data)
//        data = data.replace(/\\r\\n/g, "\n");
//        //$("#notation").text("\n<![CDATA["+data+"]]>");
//        //$("#notation").html("\r"+data);
//        lines = data;
////        $.each(lines, function(n, elem) {
////            $("#notation").text(elem+"\n");
////        })
//    }, 'text');
//    console.log(lines)
//    $("#notation").text("\n"+lines);
    // 악보 body notation 에 쓰기
    //var score = "\n%abc-2.1\n%%leftmargin 0\n%%rightmargin 0\nX:1\nT:만복의 근원 하나님\nC:OLD HUNDERDTH:8,8,8,8,\nC:OLD HUNDERDTH:8,8,8,8\n%%bgcolor white\n%%pagescale 1\n%%pagewidth 20cm\n%%score {(1|2) 3}\n%%barsperstaff 4\nL:1/4\nQ:1/4=92\nM:4/4\nI:linebreak $\nK:Ab\nV:1 treble\nV:2 treble\nV:3 bass\nV:1\n[EA]|[EA][EG][CF][CE]|[CA][EB]H[Ec] [Ec]|[Ec][Ec][EB][CA]|[Fd][Ec]H[EB]|\n[EA]|[EB][Ec][EB][EA]|[DF][DG]H[CA][Ee]| c A [EB][F_d]|c B H[CA]|| [E2A2] [C2A2] |]\nw:만 복 의 근 원 하 나 님 온 백 성 찬 송 드 리 고 저 천 사 여 찬 송 하 세 찬 송 성 부 성 자 성 령 아 멘\nV:2\nx|x4 | x4 | x4 | x3 |x | x4 |x4| E3/2 =D1/2 x2| E3/2 D1/2 x | x4 | %11\nx4 | x4 | %13\nV:3\n[A,C]|[A,C][B,E,][A,F,][G,C,]|[A,F,][G,E,] H[A,,A,][A,C]|A, A, [E,G,][F,A,]|[D,A,][A,,A,]H[E,G,]|\n[A,C]|[B,G,][A,][G,E,][A,C,]|[A,D,][E,B,,]H[E,A,,][CA,]|A, [A,F,][G,E,][A,_D,]|[A,E,][G,E,]H[A,A,,]||[F,2D,2][E,2A,2]|]"
    //var score = "\nX:1\nT:만복의 근원 하나님\nC:OLD HUNDERDTH:8,8,8,8,\nC:OLD HUNDERDTH:8,8,8,8\n%%bgcolor white\n%%pagescale 1\n%%pagewidth 20cm\n%%score {(1|2) 3}\n%%barsperstaff 4\nL:1/4\nQ:1/4=92\nM:4/4\nI:linebreak $\nK:Ab\nV:1 treble\nV:2 treble\nV:3 bass\nV:1\n[EA]|[EA][EG][CF][CE]|[CA][EB]H[Ec] [Ec]|[Ec][Ec][EB][CA]|[Fd][Ec]H[EB]|\n[EA]|[EB][Ec][EB][EA]|[DF][DG]H[CA][Ee]| c A [EB][F_d]|c B H[CA]|| [E2A2] [C2A2] |]\nw:만 복 의 근 원 하 나 님 온 백 성 찬 송 드 리 고 저 천 사 여 찬 송 하 세 찬 송 성 부 성 자 성 령 아 멘\nV:2\nx|x4 | x4 | x4 | x3 |x | x4 |x4| E3/2 =D1/2 x2| E3/2 D1/2 x | x4 | %11\nx4 | x4 | %13\nV:3\n[A,C]|[A,C][B,E,][A,F,][G,C,]|[A,F,][G,E,] H[A,,A,][A,C]|A, A, [E,G,][F,A,]|[D,A,][A,,A,]H[E,G,]|\n[A,C]|[B,G,][A,][G,E,][A,C,]|[A,D,][E,B,,]H[E,A,,][CA,]|A, [A,F,][G,E,][A,_D,]|[A,E,][G,E,]H[A,A,,]||[F,2D,2][E,2A,2]|]"
    //console.log(score)
    //$('#notation').text(score);

    page = document.body.innerHTML;
    if (!abc2svg.modules.load(page, dom_loaded)) return;
    var i = 0,
        j, k, res, src, seq = 0,
        re = /\n%abc|\nX:/g,
        re_stop = /\nX:|\n<|\n%.begin/g,
        select = window.location.hash.slice(1);
    abc = new abc2svg.Abc(user);
    if (select) {
        select = decodeURIComponent(select);
        select = page.indexOf(select);
        if (select < 0) select = 0
    }
    for (;;) {
        res = re.exec(page);
        if (!res) break;
        j = re.lastIndex - res[0].length;
        new_page += page.slice(i, j);
        re_stop.lastIndex = ++j;
        while (1) {
            res = re_stop.exec(page);
            if (!res || res[0][1] != "%") break;
            k = page.indexOf(res[0].replace("begin", "end"), re_stop.lastIndex);
            if (k < 0) break;
            re_stop.lastIndex = k
        }
        if (!res || k < 0) k = page.length;
        else k = re_stop.lastIndex - 2;
        if (!select || page[j] != "X" || select >= j && select < k) {
            if (page[j] == "X") {
                new_page += '<div onclick="playseq(' + a_src.length + ')">\n';
                a_src.push([j, k])
            } else if (!glop) {
                glop = [j, k]
            }
            try {
                abc.tosvg("abcemb", page, j, k)
            } catch (e) {
                alert("abc2svg javascript error: " + e.message + "\nStack:\n" + e.stack)
            }
            if (errtxt) {
                i = page.indexOf("\n", j);
                i = page.indexOf("\n", i + 1);
                alert("Errors in\n" + page.slice(j, i) + "\n...\n\n" + errtxt);
                errtxt = ""
            }
            if (page[j] == "X") new_page += "</div>\n"
        }
        i = k;
        if (i >= page.length) break;
        if (page[i] == "X") i--;
        re.lastIndex = i
    }
    try {
        document.body.innerHTML = new_page + page.slice(i)
    } catch (e) {
        alert("abc2svg bad generated SVG: " + e.message + "\nStack:\n" + e.stack)
    }
    delete user.img_out;
    old_gm = user.get_abcmodel;
    user.get_abcmodel = function(tsfirst, voice_tb, music_types, info) {
        if (old_gm) old_gm(tsfirst, voice_tb, music_types, info);
        abcplay.add(tsfirst, voice_tb)
    }
}
document.addEventListener("DOMContentLoaded", dom_loaded, false);