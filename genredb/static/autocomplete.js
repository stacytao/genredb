$( function() {
    $.ajax({
        url: $SCRIPT_ROOT + '/autocomplete'
    }).done(function (data) {
        $('#autocomplete').autocomplete({
            source: data.json_list,
            minLength: 4
        });
    });
} );