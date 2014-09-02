waitings = {}

function wait(key) {
    waitings[key] = false;

    function w(key) {
        if (waitings[key] == false)
            setTimeout(w, 30);
    }
    w(key);
}

function release(key) {
    waitings[key] = true;
}

webcelty.prototype= {
    constructor: function (sock) {
        this.sock = sock;
    }

    state: function (message, color) {
        $("#connection").html(message);
        $("#connection").css("color", color);
    },


    send: function (data) {
        this.sock.send(JSON.stringify(data)+"\r\n");
    },


    auth: function (sock, token) {
        this.state("auth", "yellow");
        this.send({token: token});
    },



    dispatch: function (r) {
    switch (r.type) {
        case "auth":
            release("auth");
            state("connected", "green");
            break;
        case "widgets":
            for (var key in r.data) {
                text = r.data[key].join("<br />");
                if ($("#" + key).length) {
                    $("#" + key).html(text);
                } else {
                    $("#widgets").append('<div class="block">'+key+':<div id="' + key + '">'+text+'</div></div>');
                }
            }
            break;
        case "commands":
            for (var key in r.list) {
                name = r.list[key];
                $("#commands").append('<span id="command" data-attribute="'+name+'">'+name+'</span>');
            }
            $("#command").onclick(function () {
                
            });
            break;
        case "ui":
            console.log(r);
            webhelmet.renderJSON(r.data, $("#helmet_render"));
            break;
    }
}, 
    }


$(document).ready(function () {
    var sock = new SockJS('http://localhost:23589');

    sock.onopen = function() {
        auth(sock, "1");
    };

    sock.onmessage = function(e) {
        dispatch($.parseJSON(e.data));
    };

    sock.onclose = function() {
        state("not connected", "red");
    };

    webhelmet.submit = function (data) {
        send(sock, data);
    };

    $(".celty_command").click(function () {
        console.log($(this).attr("data-args").split(","))
        send(sock, {
            command: $(this).attr("data-command"),
            args: $(this).attr("data-args").split(","), 
        });
    });
});
