webhelmet = function webhelmet () {

}

webhelmet.prototype = {
    _label: function (name, text) {
        if (name != undefined) 
            var id = "id=\"helmet_" + name + "\"";
        else
            var id = "";
        return "<span "+id+">" + text.replace(/\n/g, "<br />") + "</span>";
    },

    _input: function (name, value) {
        return "<input type=\"text\" id=\"helmet_"+name+"\" value=\""+value+"\" \>";
    },

    _button: function (name, caption, cmd, grab) {
        if (name != undefined) 
            var id = "id=\"helmet_" + name + "\"";
        else
            var id = "";
        return "<input class=\"helmet_submit\" "+id+" type=\"button\" value=\""+caption+"\" data-cmd=\""+cmd+"\" data-grab=\""+grab+"\" />";
    },

    renderJSON: function(markup, $to) {
        $to.html("");

        this.elements = {};
        for (var row in markup) {
            var id = "row_" + row;
            var c = "<table><tr>";
            var c = "";

            for (var el in markup[row]) {
                var el = markup[row][el];

                if (el.name) 
                    this.elements[el.name] = el;
                        
                //c += "<td>";
                switch (el.type) {
                    case "label": 
                        c += this._label(el.name, el.text); 
                        break;
                    case "input": 
                        c += this._input(el.name, el.value);
                        break;
                    case "button":
                        c += this._button(el.name, el.caption, el.command, el.grab);
                        break;
                }
                //c += "</td>";
            }

            //c += "</tr></table>";
            $to.append("<div class=\"helmet_row\" id=\"" + id + "\">"+c+"</div>");
        }

        var that = this;
        $(".helmet_submit").click(function () {
            var data = {};

            var attrs = $(this).attr("data-grab").split(",");
            for (var k in attrs) {
                var k = attrs[k];
                data[k] = $("#helmet_" + k).val();
            }

            $("#helmet_title").html($(this).attr("data-cmd"));

            that.submit({
                command: $(this).attr("data-cmd"),
                args: data,
            });
        });
    },

    updateByJSON: function (data) {
        for (var name in data) {
            var el = this.elements[name];
            var $el = $("#helmet_" + el.name);
            for (var k in data[name]) {
                var value = data[name][k];
                switch (el.type) {
                    case "input":
                        switch (k) {
                            case "value": $el.val(value); break;
                            default: $el.attr(k, value); break;
                        }
                        break;
                    case "button":
                        $el.attr(k, value);
                        break;
                    case "label": 
                        switch (k) {
                            case "text": 
                                if (data[name]["__method"] == "append") {
                                    $el.append(value); 

                                    text = $el.html().split("\n");
                                    if (el.max_lines && text.length > el.max_lines) {
                                        diff = text.length - el.max_lines;
                                        text = text.slice(diff - 1);
                                        $el.html(text.join("\n"));
                                    }
                                } else {
                                    $el.html(value); 
                                }

                                break;

                        }
                        break;

                }

            }
        }
    }
}
