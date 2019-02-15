$(document).ready(function() {
    $('save').on('click', function(event) {
        $.ajax({
            url: '/add_book',
            contentType: 'application/json;charset=UTF-8',
            data : {
                book : $('book').val(),
            }
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});