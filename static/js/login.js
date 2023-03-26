$(document).ready(function() {
    const errorMessages = {};
    $('#submit-button').click(
        function(event) {
            event.preventDefault();
            const username = $('#username').val();
            const password = $('#password').val();
            const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            $(this).text('Logging in..').prop('disabled', true);
            $.ajax(
                {
                    type: 'POST',
                    url: loginUrl,
                    data: {
                        username: username,
                        password: password,
                        csrfmiddlewaretoken: csrf_token,
                    },
                    success: function(response) {
                        const redirectUrl = response['redirect'];
                        window.location.replace(redirectUrl);
                    },
                    statusCode: {
                        400: function(xhr, textStatus, errorThrown) {
                            $('#submit-button').text('Login').prop('disabled', false);
                            showError('#password', xhr.responseJSON['error']);
                        }
                    }
                },
            );
        }
    )
    
    $('#password').focus(
        function() {
            clearError('#password');
        }
    )
    
    function showError(
        field,
        message
    ) {
        errorMessages[field] = message;
        let errorMessage = '';
        for (let key in errorMessages) {
            errorMessage += ('<div class="error-message-each">' +  errorMessages[key] + '</div>');
            $(key).addClass('is-invalid');
        }
        if (errorMessage === '') {
            $('#error').hide();
        }
        else {
            $('#error').html(errorMessage).show();
        }
    }

    function clearError(
        field
    ) {
        delete errorMessages[field]
        $(field).removeClass('is-invalid');
        let errorMessage = '';
        for (let key in errorMessages) {
            errorMessage += ('<div class="error-message-each">' +  errorMessages[key] + '</div>');
            $(key).addClass('is-invalid');
        }
        if (errorMessage === '') {
            $('#error').hide();
        }
        else {
            $('#error').html(errorMessage).show();
        }
    }
});
