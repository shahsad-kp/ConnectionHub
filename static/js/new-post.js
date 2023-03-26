$(document).ready(
    function () {
        const fileInput = $('#file-input');
        const imagePreview = $('#image-preview');
        const submitButton = $('#submit-button');
        const caption = $('#caption');
        const tags = $('#tags');
        const location = $('#location');
        const csrfTokken = $('input[name="csrfmiddlewaretoken"]').val();

        function submitPost(event) {
            event.preventDefault();
            if (fileInput[0].files.length === 0) {
                alert('Please select an image');
                return;
            }
            if (!validateTags()) {
                return alert('Please correct the hashtags');
            }
            const form = new FormData();
            form.append('image', fileInput[0].files[0]);
            form.append('caption', caption.val());
            form.append('tags', tags.val());
            form.append('location', location.val());
            form.append('csrfmiddlewaretoken', csrfTokken);
            submitButton.text('Uploading...').prop('disabled', true);
            $.ajax({
                url: newPostUrl,
                type: 'POST',
                data: form,
                processData: false,
                contentType: false,
                success: function (response) {
                    window.location.href = response.redirect;
                },
                error: function (response) {
                    submitButton.text('Submit').prop('disabled', false);
                    console.log(response);
                }
            });
        }

        function displayImage(file) {
            if (file.type.match('image.*')) {
                const reader = new FileReader();

                reader.onload = function (event) {
                    imagePreview.attr('src', event.target.result);
                };

                reader.readAsDataURL(file);
            }
        }

        function validateTags() {
            if (tags.val().length > 0) {
                let pattern = /^#[a-zA-Z0-9]+(\s+#[a-zA-Z0-9]+)*$/;
                if (tags.val().replace(/^\s+|\s+$/g, '').match(pattern)) {
                    $('#error-message').hide()
                    return true;
                } else {
                    $('#error-message').text('Hashtags must be separated by spaces, start with #, and contain only letters and numbers.').css('color', 'red').show();
                    return false;
                }
            }
            else{
                $('#error-message').hide()
                return true;
            }
        }

        fileInput.change(function () {
            displayImage(this.files[0]);
        });

        imagePreview.on('dragover', function (event) {
            event.preventDefault();
        });

        imagePreview.on('drop', function (event) {
            event.preventDefault();
            displayImage(event.originalEvent.dataTransfer.files[0]);
        });

        submitButton.click(submitPost);
        tags.on(
            'input',
            validateTags
        )
    }
)