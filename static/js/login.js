$(document).ready(function() {
    $('#submit-button').click(
        function(event) {
            event.preventDefault();
            const username = $('#username').val();
            const password = $('#password').val();
            const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax(
                {
                    type: 'POST',
                    url: '/login/',
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
                            $('#login-error').text(xhr.responseJSON['error']).show();
                        }
                    }
                },
            );
        }
    )
});
