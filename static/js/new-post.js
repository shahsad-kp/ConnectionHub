$(document).ready(
    function(){
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
            const form = new FormData();
            form.append('image', fileInput[0].files[0]);
            form.append('caption', caption.val());
            form.append('tags', tags.val());
            form.append('location', location.val());
            form.append('csrfmiddlewaretoken', csrfTokken);

            $.ajax({
                url: '/post/new/',
                type: 'POST',
                data: form,
                processData: false,
                contentType: false,
                success: function(response) {
                    window.location.href = response.redirect;
                },
                error: function(response) {
                    console.log(response);
                }
            });
        }

        function displayImage(file) {
            if (file.type.match('image.*')) {
                const reader = new FileReader();

                reader.onload = function(event) {
                    imagePreview.attr('src', event.target.result);
                };

                reader.readAsDataURL(file);
            }
        }

        fileInput.change(function() {
            displayImage(this.files[0]);
        });

        imagePreview.on('dragover', function(event) {
            event.preventDefault();
        });

        imagePreview.on('drop', function(event) {
            event.preventDefault();
            displayImage(event.originalEvent.dataTransfer.files[0]);
        });

        submitButton.click(submitPost);
    }
)