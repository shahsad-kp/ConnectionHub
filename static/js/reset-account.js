$(document).ready(
    function() {
        const form = $('#reset-form');
        let otpSended = false
        let otpVerified = false
        const usernameInput = $('#username');
        const otpInput = $('#otp-input');
        const submitButton = $('#submit-button');
        const passwordInput = $('#password');
        const csrfTokken = $('input[name="csrfmiddlewaretoken"]').val();
        let errorMessages = {}

        function submitReset(event) {
            event.preventDefault();

            if (!otpSended) {
                sendOtp(event);
                return null;
            }
            else if (!otpVerified){
                verifyOtp(event);
            }
            else{
                const url = $(this).attr('action');
                const data = {
                    'username': usernameInput.val(),
                    'password': passwordInput.val(),
                    'otp': otpInput.val(),
                    'csrfmiddlewaretoken': csrfTokken
                }
                $.ajax(
                    {
                        url: url,
                        data: data,
                        method: 'POST',
                        success: function(response){
                            location.href = ''
                        },
                        error: function(response) {
                            showError(
                                'otp-invalid',
                                response['error']
                            )
                        }
                    }
                )
            }

        }

        function verifyOtp() {
            const url = verifyOtpUrl;
            const data = {
                'username': usernameInput.val(),
                'otp': otpInput.val(),
                'csrfmiddlewaretoken': csrfTokken
            }
            $.ajax({
                url: url,
                data: data,
                method: 'POST',
                success: function(response){
                    otpVerified = true;
                    otpInput.hide();
                    submitButton.html('Reset Password');
                    usernameInput.prop("readonly", true);
                    passwordInput.show()
                },
                error: function(response) {
                    showError(
                        '#otp-input',
                        response['error']
                    )
                }
            })
        }

        function sendOtp() {
            const url = sendOtpUrl;
            const data = {
                'username': usernameInput.val(),
                'csrfmiddlewaretoken': csrfTokken
            }
            $.ajax({
                url: url,
                data: data,
                method: 'POST',
                success: function(response){
                    otpSended = true;
                    otpInput.show();
                    submitButton.html('Verify OTP');
                    usernameInput.prop("readonly", true);
                },
                error: function(response) {
                    console.log(response);
                }
            })
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
                $('#error').hide();
            }
            else {
                $('#error').html(errorMessage).show();
            }
        }

        function clearError(
            field
        ) {
            delete errorMessages[field];
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

        form.submit(submitReset);
        otpInput.focus(
            function () {
                clearError('#otp-input')
            }
        )
        passwordInput.on(
            'input',
            function () {
                if($(this).val().length < 8){
                    showError('#password', 'Password must be atleast 8 characters')
                }
                else{
                    clearError('#password')
                }
            }
        )
    }
)