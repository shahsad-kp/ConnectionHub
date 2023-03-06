$(document).ready(
    function (){
        const deleteButton = $('.delete-button')

        function deleteData(url, successCallback){
            $.ajax({
                url: url,
                type: 'GET',
                success: successCallback
            })
        }

        function showConfirmation(){
            const confirmation = confirm('Are you sure you want to delete this?');
            const type = $(this).data('type');
            if (confirmation === false){
                return false;
            }
            if (type === 'user'){
                const username = $(this).data('username');
                let url = '/admin/users/' + username + '/delete/'
                deleteData(url, function(){
                    window.location.href = '/admin/';
                });
            }
            else if (type === 'post'){
                const postId = $(this).data('post-id');
                let url = '/admin/post/' + postId + '/delete/'
                deleteData(url, function(){
                    window.location.href = '/admin/';
                });
            }
            else if (type === 'comment'){
                const commentId = $(this).data('comment-id');
                let url = '/admin/post/comment/' + commentId + '/delete/'
                deleteData(url, function(){
                    location.reload();
                });
            }

        }

        deleteButton.click(showConfirmation);

    }
)

