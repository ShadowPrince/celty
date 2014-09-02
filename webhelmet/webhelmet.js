webhelmet = {
    _label: function (text) {
        return "<span>" + text.replace(/\n/g, "<br />") + "</span>";
    },

    _input: function (name, value) {
        return "<input type=\"text\" id=\"helmet_"+name+"\" value=\""+value+"\" \>";
    },

    _button: function (caption, cmd, grab) {
        return "<input class=\"helmet_submit\" type=\"button\" value=\""+caption+"\" data-cmd=\""+cmd+"\" data-grab=\""+grab+"\" />";
    },

    renderJSON: function(markup, $to) {
        $to.html("");

        webhelmet.elements = {};
        for (var row in markup) {
            var id = "row_" + row;
            var c = "<table><tr>";
            var c = "";

            for (var el in markup[row]) {
                var el = markup[row][el];

                //c += "<td>";
                switch (el.type) {
                    case "label": 
                        c += webhelmet._label(el.text); 
                        break;
                    case "input": 
                        c += webhelmet._input(el.name, el.value);
                        break;
                    case "button":
                        c += webhelmet._button(el.caption, el.command, el.grab);
                        break;
                }
                //c += "</td>";
            }

            //c += "</tr></table>";
            $to.append("<div class=\"helmet_row\" id=\"" + id + "\">"+c+"</div>");
        }

        $(".helmet_submit").click(function () {
            var data = {};

            var attrs = $(this).attr("data-grab").split(",");
            for (var k in attrs) {
                var k = attrs[k];
                data[k] = $("#helmet_" + k).val();
            }

            $("#helmet_title").html($(this).attr("data-cmd"));
            webhelmet.submit({
                command: $(this).attr("data-cmd"),
                args: data,
            });
        });
    },

    updateByJSON: function (json) {
        var data = JSON.parse(json);
        for (var push in data) {
            var push = data[push];
            var $el = $("#helmet_" + push.name);
// b

        }
    }
}
