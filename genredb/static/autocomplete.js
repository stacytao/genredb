let query = null;
let input = $('#autocomplete');
let searchForm = $('#search-form');

$( function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/autocomplete'
    }).done(function (data) {
        input.autocomplete({
            source: data.json_list,
            minLength: 4,
            select: function(event, ui) {
                input.data('value', ui.item.value);
                query = input.data('value');
            }
        });
    });
} );

searchForm.submit(function(event) {
    event.preventDefault();

    window.location.href = $SCRIPT_ROOT + '/search/' + query;
});