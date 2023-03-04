$(document).ready(
    function() {
        const commentForm = $('#comment-form');

        function submitNewComment(event){
            event.preventDefault();
            const commentText = $('#comment-input').val();
            if (commentText === ''){
                return;
            }
            const url = commentForm.attr('action');
            const data = commentForm.serialize();
            $.ajax({
                url: url,
                data: data,
                method: 'POST',
                success: function(response){
                    location.reload();
                }
            }
            )
        }

        commentForm.submit(submitNewComment);
    }
)