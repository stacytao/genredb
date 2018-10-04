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
        });
    });
} );

searchForm.submit(function(event) {
    event.preventDefault();
    query = input.val();
    window.location.href = $SCRIPT_ROOT + '/search/' + query;
});