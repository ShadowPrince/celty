var webcelty = function webcelty(url, token) {
    this.sock = new SockJS(url);
    this.token = token;
    this.url = url;
    this.connect_attempt = 1;

    $(".state #addr").html(url);

    this._register_handlers();
    this.helmet = new webhelmet();

    var that = this;
    this.helmet.submit = function (data) {
        that.command(data.command, data.args);
    };
};

webcelty.prototype = {
    ready: function () {},

    _register_handlers: function () {
        var that = this;
        this.sock.onopen = function() {
            that.auth_request(that.token);
            that.connect_attempt = 1;
        };

        this.sock.onmessage = function(e) {
            that.dispatch($.parseJSON(e.data));
        };

        this.sock.onclose = function() {
            that.show_state("not connected (attempt "+that.connect_attempt+")", "red");
            setTimeout(function () {
                that.connect_attempt++;
                that.sock = new SockJS(that.url);
                that._register_handlers();
            }, 1000);
        };
    },

    _send: function (data) {
        var json = JSON.stringify(data);

        this.sock.send(json+"\r\n");
    },

    _halt: function (e) {
        console.log("webcelty halt: " + e);
        this.sock.onclose = undefined;
        this.sock.onmessage = undefined;
        this.sock.onopen = undefined;
        this.sock.close();
        this.sock = undefined;
    },

    _jsonlist: function (_list) {
        list = [];

        for (var k in _list) {
            if (_list[k] != undefined)
                list.push(_list[k]);
        }
        return list;
    },

    show_state: function (message, color) {
        $("#connection").html(message);
        $("#connection").css("color", color);
        $("#connection").css("border-color", color);
    },

    auth_request: function (token) {
        this.show_state("authenticating...", "yellow");
        this._send({token: token});
    },

    subscribe: function () {
        console.log("webcelty: subscribed to " + arguments[0]);

        this._send({
            command: "celty:subscribe",
            args: this._jsonlist(arguments),
        });
    },

    unsubscribe: function () {
        console.log("webcelty: unsubscribed from " + arguments[0]);

        this._send({
            command: "celty:unsubscribe",
            args: [arguments[0]],
        });
    },

    command: function (cmd, args) {
        this._send({
            command: cmd,
            args: args,
        });
    },

    dispatch: function (r) {
        switch (r.type) {
            case "auth":
                if (r.result == "success") {
                    this.show_state("connected", "green");
                    this.ready();
                } else {
                    this.show_state("celty halted -> auth error: " + r.error, "red");
                    this._halt("auth error");
                }

                break;
            case "widgets":
                for (var key in r.data) {
                    text = r.data[key].join("\n");
                    html_key = key.replace(/:/g, "_");
                    if ($("#" + html_key).length) {
                        $("#" + html_key).html(text);
                    } else {
                        $("#widgets").append('<div class="widget"><div class="title">'+key+'</div><pre id="' + html_key + '">'+text+'</pre></div>');
                    }
                }
                break;
            case "ui":
                if (this.ui_sub) {
                    this.unsubscribe(this.ui_sub);
                    this.ui_sub = undefined;
                }

                if (r.subscribe) {
                    this.ui_sub = r.subscribe;
                    this.subscribe(this.ui_sub);
                }

                this.helmet.renderJSON(r.data, $("#helmet_render"));
                break;
            case "ui_update":
                this.helmet.updateByJSON(r.data);
                break;
            case "error":
                alert(r.error);
                break;
        }
    }, 
}



$(document).ready(function () {
    c = new webcelty("http://127.0.0.1:23589", "1");
    c.ready = function () {
        this.subscribe("celty:widgets");
        this.command("celty:main");
    };


    $("#back_command").click(function () {
        $("#helmet_title").html("&nbsp;");
    });

    $(".celty_command").click(function () {
        args = $(this).attr("data-args");
        if (args != undefined)
            args = args.split(",");

        c._send({
            command: $(this).attr("data-command"),
            args: args,
        });
    });
});
