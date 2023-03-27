$(document).ready(function () {
    const profileInput = $('#new-profile-picture')
    const profileImage = $('.profile-picture img')
    const fullNameInput = $('#fullname')
    const usernameInput = $('#username')
    const emailInput = $('#email-address')
    const phoneInput = $('#phone-number')
    const bioInput = $('#bio')
    const submitButton = $('#submit-button')
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
    const passwordInput = $('#password')
    const newPasswordInput = $('#new-password')
    const confirmPasswordInput = $('#confirm-password')
    const helpSubjectInput = $('#subject')
    const helpMessageInput = $('#message')
    const accountTypeInput = $('#private-account')
    const errorMessages = {};
    let emailOtpSended = false;
    let emailOtpVerified = false;


    function checkEmpty(element, name) {
        const id = element.attr('id');
        if (element.val() === '') {
            showError('#' + id, name + ' field can not be empty');
            return false;
        } else {
            clearError('#' + id);
            return true;
        }
    }

    function checkEmptyAuto() {
        const element = $(this);
        const name = element.attr('name');
        return checkEmpty(element, name);

    }

    function passwordValidation() {
        const password = passwordInput.val();
        if (password === '') {
            showError('#password', 'Password can not be empty');
            return false;
        }
        clearError('#password');
        return true;
    }

    function newPasswordValidation() {
        const password = newPasswordInput.val();
        if (password === '') {
            showError('#new-password', 'Password can not be empty');
            return false;
        }
        if (password.length < 8) {
            showError('#new-password', 'Password must be at least 8 characters');
            return false;
        }
        if (checkPattern(password) === false) {
            showError('#new-password', 'Password can only contain letters, numbers and underscores');
            return false;
        }
        clearError('#new-password');
        return true;

        function checkPattern(password) {
            const re = /^[a-zA-Z0-9_]+$/;
            return re.test(password);
        }
    }

    function confirmPasswordValidation() {
        const password = newPasswordInput.val();
        const confirmPassword = confirmPasswordInput.val();
        if (password !== confirmPassword) {
            showError('#confirm-password', 'Passwords do not match');
            return false;
        }
        clearError('#confirm-password');
        return true;
    }

    function phoneValidation() {
        const phone = phoneInput.val();
        if (phone === '') {
            clearError('#phone-number');
            return true;
        }
        if (checkPhone(phone) === false) {
            showError('#phone-number', 'Enter your phone number with country code');
            return false;
        }

        function checkPhone(phone) {
            const re = /^\+\d{1,3}\d{6,14}$/;
            return re.test(phone);
        }

        clearError('#phone-number');
        return true;
    }

    function emailValidation() {
        const email = emailInput.val();
        if (email === '') {
            clearError('#email-address');
            return true;
        }
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

        function checkAvailability(email) {
            $.ajax(
                {
                    type: 'GET',
                    url: checkEmailUrl,
                    data: {
                        q: email,
                    },
                    success: function (response) {
                        if (response['available'] === false) {
                            showError('#email-address', 'Email address already in use');
                        }
                    }
                },
            );

        }
    }

    function usernameValidation() {
        const username = usernameInput.val();
        if (username === '') {
            clearError('#username');
            return true;
        }

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
                    success: function (response) {
                        if (response['available'] === false) {
                            showError('#username', 'Username already in use');
                        } else {
                            clearError('#username');
                        }
                    }
                },
            );
        }
    }

    function showError(
        field,
        message
    ) {
        errorMessages[field] = message;
        let errorMessage = '';
        for (let key in errorMessages) {
            errorMessage += ('<div class="error-message-each">' + errorMessages[key] + '</div>');
            $(key).addClass('is-invalid');
        }
        if (errorMessage === '') {
            $('#error').hide();
        } else {
            $('#error').html(errorMessage).show();
        }
    }

    function clearError(
        field
    ) {
        if (field == 'all') {
            for (let key in errorMessages) {
                $(key).removeClass('is-invalid');
            }
            errorMessages = {};
            $('#error').hide();
            return;
        }
        delete errorMessages[field];
        $(field).removeClass('is-invalid');
        let errorMessage = '';
        for (let key in errorMessages) {
            errorMessage += ('<div class="error-message-each">' + errorMessages[key] + '</div>');
            $(key).addClass('is-invalid');
        }
        if (errorMessage === '') {
            $('#error').hide();
        } else {
            $('#error').html(errorMessage).show();
        }
    }

    function updateProfile() {
        if (emailValidation() === false) {
            return;
        }
        if (usernameValidation() === false) {
            return;
        }
        if (phoneValidation() === false) {
            return;
        }
        const form = new FormData();
        form.append('csrfmiddlewaretoken', csrfToken);
        form.append('fullname', fullNameInput.val());
        form.append('username', usernameInput.val());
        form.append('email', emailInput.val());
        form.append('phone', phoneInput.val());
        form.append('bio', bioInput.val());
        form.append('profile-picture', profileInput[0].files[0]);

        if ((emailInput.val() !== '') && (emailOtpSended === false)) {
            submitButton.text('Sending OTP...')
            $.ajax({
                url: sendOtpUrl,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfToken,
                    'email': emailInput.val(),
                },
                success: function (response) {
                    $('#email-otp-field').show()
                    submitButton.text('Submit')
                    emailOtpSended = true;
                    emailInput.prop('readonly', true)
                },
                error: function (error) {
                    submitButton.text('Submit')
                    showError('#undefined', error.responseJSON['error']);
                }
            });
        } else if ((emailInput.val() !== '') && (emailOtpSended === true) && (emailOtpVerified === false)) {
            submitButton.text('Verifying OTP...')
            $.ajax({
                url: verifyOtpUrl,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': csrfToken,
                    'email': emailInput.val(),
                    'otp': $('#email-otp').val(),
                },
                success: function (response) {
                    submitButton.text('Submit')
                    emailOtpVerified = true;
                    updateProfile();
                },
                error: function (error) {
                    submitButton.text('Submit')
                    showError('#email-otp', error.responseJSON['error']);
                }
            });
        } else {
            submitButton.text('Updating Profile...')
            if (emailOtpVerified) {
                form.append('email-otp', $('#email-otp').val());
            }
            $.ajax({
                url: updateProfileUrl,
                type: 'POST',
                data: form,
                processData: false,
                contentType: false,
                success: function (response) {
                    $('#success').text('Your profile was updated successfully..').show();
                    $('#email-otp-field').hide()
                    submitButton.text('Submit')
                    emailInput.prop('readonly', false)
                    emailOtpSended = false;
                    emailOtpVerified = false;
                    $('form').trigger('reset');
                    clearError('all')
                },
                error: function (error) {
                    showError('#undefined', error.responseJSON['error']);
                    submitButton.text('Submit')
                }
            });
        }

    }

    function updatePassword() {
        if (passwordValidation() === false) {
            return;
        }
        if (newPasswordValidation() === false) {
            return;
        }
        if (confirmPasswordValidation() === false) {
            return;
        }
        const form = new FormData();
        form.append('csrfmiddlewaretoken', csrfToken);
        form.append('old-password', passwordInput.val());
        form.append('new-password', newPasswordInput.val());

        $.ajax({
            url: updatePasswordUrl,
            type: 'POST',
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#success').text('Password updated successfully..').show();
            },
            error: function (response) {
                showError('#password', response.responseJSON['error']);
            }
        });
    }

    function sendHelp() {
        if (checkEmpty(helpSubjectInput, 'subject') === false) {
            return;
        }
        if (checkEmpty(helpMessageInput, 'message') === false) {
            return;
        }
        const form = new FormData();
        form.append('csrfmiddlewaretoken', csrfToken);
        form.append('subject', helpSubjectInput.val());
        form.append('message', helpMessageInput.val());

        $.ajax({
            url: helpUrl,
            type: 'POST',
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#success').text('Your message has been sent').show();
                $('form').trigger('reset');
            },
            error: function (error) {
                console.log(error);
            }
        });
    }

    function deleteAccount() {
        if (passwordValidation() === false) {
            return;
        }
        const form = new FormData();
        form.append('csrfmiddlewaretoken', csrfToken);
        form.append('password', passwordInput.val());
        $.ajax({
            url: deleteAccountUrl,
            type: 'POST',
            data: form,
            processData: false,
            contentType: false,
            success: function (response) {
                location.href = '/'
            },
            error: function (response) {
                showError('#password', response.responseJSON['error']);
            }
        });
    }

    function updateAccountType() {
        let turned = this.checked;
        $.ajax(
            {
                url: updateAccTypeUrl,
                data: {
                    'type': turned,
                },
                type: 'GET',
            }
        )
    }

    submitButton.click(
        function (event) {
            event.preventDefault();
            let formType = $(this).data('form-type');
            if (formType === 'profile') {
                updateProfile();
            } else if (formType === 'password') {
                updatePassword();
            } else if (formType === 'help') {
                sendHelp();
            } else if (formType === 'delete') {
                deleteAccount();
            }
        }
    )

    emailInput.on(
        'input',
        emailValidation
    )

    usernameInput.on(
        'input',
        usernameValidation
    )

    phoneInput.on(
        'input',
        phoneValidation
    )

    newPasswordInput.on(
        'input',
        newPasswordValidation
    )

    confirmPasswordInput.on(
        'input',
        confirmPasswordValidation
    )

    passwordInput.on(
        'input',
        passwordValidation
    )

    profileImage.click(function () {
        $('input[type="file"]').click();
    });

    profileInput.change(function () {
        const file = $(this)[0].files[0];
        const reader = new FileReader();
        reader.onload = function (e) {
            $('.profile-picture img').attr('src', e.target.result);
        }
        reader.readAsDataURL(file);
    });

    helpSubjectInput.on(
        'input',
        checkEmptyAuto
    )

    helpMessageInput.on(
        'input',
        checkEmptyAuto
    )

    accountTypeInput.change(
        updateAccountType
    )

    $('#email-otp').on('input', function () {
            if ($(this).val().length === 6) {
                updateProfile();
            } else {
                clearError('#email-otp')
            }
        }
    );
})
