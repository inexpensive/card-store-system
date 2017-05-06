$(document).ready(function () {
    var card_input = $("#card_search_box");
    card_input.autocomplete({
        source: "/inv/autocomplete/",
        minLength: 2,
        select: function (event, ui) {
            $("#card_search_box").val(ui.item.label);
            $("#search_form").submit();
        }
    })
    .autocomplete("instance")._renderItem = function(ul, item) {
        return $("<li>")
            .append("<table><tr><td class=\"fit\" rowspan=\"2\"><img class=\"searchbox\"src=\"/static" + item.image +"\"></td><td>" + item.label + "</td></tr><tr><td>" + item.desc.replace(/\n/g, "<br>") + "</td></tr></table>")
            .appendTo(ul);
    };
});