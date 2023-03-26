$(document).ready(
    function() {
        const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        let errorMessages = {};
        let otpSended = false;
        const submitButton = $('#submit-button');
        const usernameInput = $('#username');
        const emailInput = $('#email-address');
        const passwordInput = $('#password');
        const fullnameInput = $('#fullname');
        const otp_input = $('#otp-input');
        submitButton.click(
            formSubmition
        )
        usernameInput.on(
            'input',
            usernameValidation
        )
        emailInput.on(
            'input',
            emailValidation
        )

        passwordInput.on(
            'input',
            passwordValidation
        )

        fullnameInput.on(
            'input',
            fullnameValidation
        )

        function formSubmition(event) {
                event.preventDefault();
                const fullname = fullnameInput.val();
                const username = usernameInput.val();
                const email = emailInput.val();
                const password = passwordInput.val();

                if (fullnameValidation.call(fullnameInput) === false) {
                    return;
                }
                if (usernameValidation.call(usernameInput) === false) {
                    return;
                }
                if (emailValidation.call(emailInput) === false) {
                    return;
                }
                if (passwordValidation.call(passwordInput) === false) {
                    return;
                }

                if (otpSended === false) {
                    submitButton.text('Sending OTP...').prop('disabled', true)
                    $.ajax(
                        {
                            type: 'POST',
                            url: sendOtpUrl,
                            data: {
                                username: username,
                                email: email,
                                csrfmiddlewaretoken: csrf_token,
                            },
                            success: function(){
                                otpSended = true;
                                otp_input.show();
                                otp_input.removeClass('main-background-disabled');
                                submitButton.text('Verify OTP').prop('disabled', false)
                            },
                            statusCode: {
                                400: function(xhr) {
                                    showError('#otp-input', xhr.responseJSON['error']);
                                    submitButton.text('Send OTP').prop('disabled', false)
                                }
                            },
                            error: function(xhr, status, error) {
                                console.log("Error: " + error);
                            },
                        },
                    );
                    waitForOtp()
                }
                else {
                    submitButton.text('Verifying OTP...').prop('disabled', true)
                    $.ajax(
                        {
                            type: 'POST',
                            url: verifyOtpUrl,
                            data: {
                                otp: otp_input.val(),
                                email: email,
                                csrfmiddlewaretoken: csrf_token,
                            },
                            success: function(_) {
                                submitButton.text('Registering...').prop('disabled', true)
                                $.ajax(
                                    {
                                        type: 'POST',
                                        url: registerUrl,
                                        data: {
                                            username: username,
                                            email: email,
                                            password: password,
                                            fullname: fullname,
                                            csrfmiddlewaretoken: csrf_token,
                                        },
                                        success: function(response) {
                                            const redirectUrl = response['redirect'];
                                            window.location.replace(redirectUrl);
                                        },
                                        statusCode: {
                                            400: function(xhr) {
                                                submitButton.text('Verify OTP').prop('disabled', false)
                                                showError('#otp-input', xhr.responseJSON['error']);
                                            }
                                        },
                                        error: function(xhr, status, error) {
                                            console.log("Error: " + error);
                                        },
                                        complete: function(xhr, status) {
                                            console.log("Request complete with status: " + status);
                                        }
                                    },
                                );
                            },
                            statusCode: {
                                400: function(xhr) {
                                    submitButton.text('Verify OTP').prop('disabled', false)
                                    showError('#otp-input', xhr.responseJSON['error']);
                                }
                            },
                            error: function(xhr, status, error) {
                                console.log("Error: " + error);
                            },
                        },
                    );
                }
            }

        function fullnameValidation() {
            const fullname = $(this).val();
            if (fullname.length < 1) {
                showError('#fullname', 'Name cannot be empty');
                return false;
            }
            clearError('#fullname');
            return true;
        }

        function usernameValidation() {
            const username = $(this).val();
            if (checkPattern(username) === false) {
                showError('#username', 'Username can only contain letters, numbers and underscores');
                return false;
            }
            clearError('#username');
            checkAvailability(username)
            return true;

            function checkPattern(username) {
                const re = /^[a-zA-Z0-9_]+$/;
                return re.test(username);
            }
            function checkAvailability(username) {
                $.ajax(
                    {
                        type: 'GET',
                        url: checkUsernameUrl,
                        data: {
                            q: username,
                        },
                        success: function(response) {
                            if (response['available'] === false) {
                                showError('#username', 'Username already in use');
                            }
                            else {
                                clearError('#username');
                            }
                        }
                    },
                );
            }
        }

        function emailValidation() {
            const email = $(this).val();
            if (checkEmail(email) === false) {
                showError('#email-address', 'Invalid email address');
                return false;
            }
            clearError('#email-address');
            checkAvailability(email)
            return true;

            function checkEmail(email) {
                const re = /\S+@\S+\.\S+/;
                return re.test(email);
            }
            function checkAvailability(email){
                $.ajax(
                    {
                        type: 'GET',
                        url: checkEmailUrl,
                        data: {
                            q: email,
                        },
                        success: function(response) {
                            if (response['available'] === false) {
                                showError('#email-address', 'Email address already in use');
                            }
                        }
                    },
                );

            }
        }

        function passwordValidation() {
            const password = $(this).val();
            if (password.length < 8) {
                showError('#password', 'Password must be at least 8 characters');
                return false;
            }
            else if (password.length > 20) {
                showError('#password', 'Password must be at most 20 characters');
                return false;
            }
            clearError('#password');
            return true;
        }

        function waitForOtp() {
            otpSended = true;
            usernameInput.prop('readonly', true);
            usernameInput.addClass('text-color-disabled')
            emailInput.prop('readonly', true);
            emailInput.addClass('text-color-disabled')
            passwordInput.prop('readonly', true);
            passwordInput.addClass('text-color-disabled')
            fullnameInput.prop('readonly', true);
            fullnameInput.addClass('text-color-disabled')
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
    }
)