$(document).ready(
    function (){
        const deleteButton = $('.delete-button')
        const banButton = $('.ban-button')

        function banUser(){
            let username = $(this).data('username');
            let url;
            if ($(this).hasClass('banned')){
                url = adminUserUnbanUrl.replace('-username-', username);
            }
            else{
                url = adminUserBanUrl.replace('-username-', username);
            }
            $.ajax({
                url: url,
                type: 'GET',
                success: function (){
                    location.reload();
                }
            })
        }

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
                let url = adminUserDeleteUrl.replace('-username-', username);
                deleteData(url, function(){
                    window.location.href = adminHomeUrl;
                });
            }
            else if (type === 'post'){
                const postId = $(this).data('post-id');
                let url = adminPostDeleteUrl.replace('0', postId)
                deleteData(url, function(){
                    window.location.href = adminHomeUrl;
                });
            }
            else if (type === 'comment'){
                const commentId = $(this).data('comment-id');
                let url = adminCommentDeleteUrl.replace('0', commentId)
                deleteData(url, function(){
                    location.reload();
                });
            }

        }

        deleteButton.click(showConfirmation);
        banButton.click(banUser);

    }
)

