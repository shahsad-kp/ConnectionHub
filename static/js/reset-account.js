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
                submitButton.text('Resetting Password...').prop('disabled', true);
                $.ajax(
                    {
                        url: url,
                        data: data,
                        method: 'POST',
                        success: function(response){
                            location.href = ''
                        },
                        error: function(response) {
                            submitButton.text('Reset Password').prop('disabled', false);
                            showError(
                                'otp-invalid',
                                response.responseJSON['error']
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
            submitButton.text('Verifying OTP...').prop('disabled', true);
            $.ajax({
                url: url,
                data: data,
                method: 'POST',
                success: function(response){
                    otpVerified = true;
                    otpInput.hide();
                    submitButton.text('Reset Password').prop('disabled', false);
                    usernameInput.prop("readonly", true);
                    passwordInput.show()
                },
                error: function(response) {
                    submitButton.text('Verify OTP').prop('disabled', false);
                    showError(
                        '#otp-input',
                        response.responseJSON['error']
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
            submitButton.text('Sending OTP...').prop('disabled', true);
            $.ajax({
                url: url,
                data: data,
                method: 'POST',
                success: function(response){
                    otpSended = true;
                    otpInput.show();
                    submitButton.text('Verify OTP').prop('disabled', false);
                    usernameInput.prop("readonly", true);
                },
                error: function(response) {
                    submitButton.text('Send OTP').prop('disabled', false);
                    if(response.status === 404){
                        showError(
                            '#username',
                            'Username is not registered'
                        )
                    }
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

        usernameInput.on(
            'input',
            function () {
                clearError('#username')
            }
        )
    }
)