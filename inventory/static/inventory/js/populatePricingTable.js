$(document).ready(function () {
    $("button").click(function () {
        $.getJSON("/inv/pricing/",
        {
            name: $('#card_search_box').val()
        },
        function (data, status) {
            var names = [];
            var sets = {};
            for (var i = 0; i < data.length; i++) {
                var card = data[i];
                var name = card.name;
                var set = card.set;
                if ($.inArray(name, names) === -1) {
                    sets[name] = [];
                    names.push(name);
                }
                if ($.inArray(set, sets[name]) === -1) {
                    sets[name].push(set);
                }
            }
            var $table = $('<table class="table table-striped table-bordered table-sm table-nonfluid"/>');
            for (var j = 0; j < names.length; j++) {
                name = names[j];
                set = sets[name];
                var colspan = 1 + 2 * set.length;
                $table.append('<tr><th colspan="' + colspan +'">' + name +'</th></tr>');
                var set_row = '<tr><th>Set</th>';
                $.each(set, function (i) {
                    var set_name = set[i];
                    set_row += '<td colspan="2">' + set_name + '</td>'
                });
                set_row += '</tr>';
                $table.append(set_row);
                var conditions = ['NM', 'SP', 'MP', 'HP'];
                $.each(conditions, function (i) {
                    var condition = conditions[i];
                    var price_row = '<tr><td>'+ condition +'</td>';
                    var num_of_sets = sets[name].length;
                    for(var k = 0; k < num_of_sets; k++) {
                        var non_foil_price = data[i * num_of_sets * 2 + 2 * k].price;
                        var foil_price = data[i * num_of_sets * 2 + 2 * k + 1].price;
                        if (non_foil_price === -1) {
                            non_foil_price = 'N/A';
                        }
                        else {
                            non_foil_price = '$' + non_foil_price;
                        }
                        if (foil_price === -1) {
                            foil_price = '(N/A)';
                        }
                        else {
                            foil_price = '($' + foil_price + ')';
                        }
                        price_row += '<td>' + non_foil_price + '</td><td>' + foil_price + '</td>';
                    }
                    price_row +='</tr>';
                    $table.append(price_row);
                })
            }
            $('#test-table').html($table);
        });
    })
});
