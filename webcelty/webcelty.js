function wait(pred) {
    function check() {
        if (!pred())
            setTimeout(check, 50);
    }

    check();
}

var webcelty = function webcelty(sock, token) {
    this.sock = sock;
    that = this;

    sock.onopen = function() {
        that.auth_request(sock, token);
    };

    sock.onmessage = function(e) {
        that.dispatch($.parseJSON(e.data));
    };

    sock.onclose = function() {
        that.show_state("not connected", "red");
    };

    webhelmet.submit = function (data) {
        that.command(data.command, data.args);
    };
}

webcelty.prototype = {
    ready: function () {},

    show_state: function (message, color) {
        $("#connection").html(message);
        $("#connection").css("color", color);
    },


    _send: function (data) {
        var json = JSON.stringify(data);
        this.sock.send(json+"\r\n");
    },

    _halt: function (e) {
        console.log("webcelty halt: " + e);
        this.sock.onclose = undefined;
        this.sock.close();
    },

    _jsonlist: function (_list) {
        list = [];

        for (var k in _list) {
            if (_list[k] != undefined)
                list.push(_list[k]);
        }
        return list;
    },

    auth_request: function (sock, token) {
        this.show_state("auth", "yellow");
        this._send({token: token});
    },

    subscribe: function () {
        $("#subscriptions").append("<li id=\""+arguments[0]+"\">" + arguments[0] + "</li>");


        this._send({
            command: "subscribe",
            args: this._jsonlist(arguments),
        });
    },

    unsubscribe: function () {
        $("#subscriptions #" + arguments[0]).remove();

        this._send({
            command: "unsubscribe",
            args: [arguments[0]],
        });
    },

    command: function (cmd, args) {
        this._send({
            command: cmd,
            args: this._jsonlist(args), 
        });
    },

    dispatch: function (r) {
        switch (r.type) {
            case "auth":
                if (r.result == "success") {
                    this.show_state("connected", "green");
                    this.ready();
                } else {
                    this.show_state("auth error: " + r.error, "red");
                    this._halt("auth error");
                }

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
            case "ui":
                webhelmet.renderJSON(r.data, $("#helmet_render"));
                break;
            case "error":
                alert(r.error);
                break;
        }
    }, 
}



$(document).ready(function () {
    c = new webcelty(new SockJS("http://localhost:23589"), "1");
    c.ready = function () {
        this.subscribe("widgets");
        this.command("main");
    };


    $(".celty_command").click(function () {
        c._send({
            command: $(this).attr("data-command"),
            args: $(this).attr("data-args").split(","), 
        });
    });
});
