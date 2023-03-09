$(document).ready(
    function () {
        const submitButton = $('#submit-button')
        const usernameInput = $('#username')
        const passwordInput = $('#password')
        const errorField = $('#error')
        const errorMessages = {};

        function submitForm(event) {
            event.preventDefault();
            if (!checkEmpty(usernameInput)) {
                return;
            }
            if (!checkEmpty(passwordInput)) {
                return;
            }
            const username = usernameInput.val();
            const password = passwordInput.val();
            const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax(
                {
                    type: 'POST',
                    url: adminLoginUrl,
                    data: {
                        username: username,
                        password: password,
                        csrfmiddlewaretoken: csrf_token,
                    },
                    success: function(response) {
                        const redirectUrl = response['redirect'];
                        window.location.replace(redirectUrl);
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        showError('#password', xhr.responseJSON['error']);
                    },
                }
            )
        }

        function checkEmpty(element){
            const id = element.attr('id');
            const value = element.val();
            if (value === '') {
                showError('#' + id,  id + ' field is required');
                return false;
            }
            clearError('#' + id);
            return true;
        }

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
                errorField.hide();
            }
            else {
                errorField.html(errorMessage).show();
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
                errorField.hide();
            }
            else {
                errorField.html(errorMessage).show();
            }
        }

        usernameInput.change(
            function() {
                checkEmpty($(this));
            }
        )

        passwordInput.change(
            function() {
                checkEmpty($(this));
            }
        )

        submitButton.click(
            submitForm
        )
    }
)