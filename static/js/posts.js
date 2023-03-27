$(document).ready(
    function () {
        let likedHtml = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">\n' +
            '                        <path d="M8.39062 18.4907V8.33071C8.39062 7.93071 8.51062 7.54071 8.73062 7.21071L11.4606 3.15071C11.8906 2.50071 12.9606 2.04071 13.8706 2.38071C14.8506 2.71071 15.5006 3.81071 15.2906 4.79071L14.7706 8.06071C14.7306 8.36071 14.8106 8.63071 14.9806 8.84071C15.1506 9.03071 15.4006 9.15071 15.6706 9.15071H19.7806C20.5706 9.15071 21.2506 9.47071 21.6506 10.0307C22.0306 10.5707 22.1006 11.2707 21.8506 11.9807L19.3906 19.4707C19.0806 20.7107 17.7306 21.7207 16.3906 21.7207H12.4906C11.8206 21.7207 10.8806 21.4907 10.4506 21.0607L9.17062 20.0707C8.68062 19.7007 8.39062 19.1107 8.39062 18.4907Z" fill="#F8E71C"></path>\n' +
            '                        <path d="M5.21 6.37891H4.18C2.63 6.37891 2 6.97891 2 8.45891V18.5189C2 19.9989 2.63 20.5989 4.18 20.5989H5.21C6.76 20.5989 7.39 19.9989 7.39 18.5189V8.45891C7.39 6.97891 6.76 6.37891 5.21 6.37891Z" fill="#F8E71C"></path>\n' +
            '                    </svg>'
        let normalLikeHtml = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">\n' +
            '                        <path d="M7.47998 18.35L10.58 20.75C10.98 21.15 11.88 21.35 12.48 21.35H16.28C17.48 21.35 18.78 20.45 19.08 19.25L21.48 11.95C21.98 10.55 21.08 9.34997 19.58 9.34997H15.58C14.98 9.34997 14.48 8.84997 14.58 8.14997L15.08 4.94997C15.28 4.04997 14.68 3.04997 13.78 2.74997C12.98 2.44997 11.98 2.84997 11.58 3.44997L7.47998 9.54997" stroke="#F8E71C" stroke-width="1.5" stroke-miterlimit="10"></path>\n' +
            '                        <path d="M2.38 18.35V8.55002C2.38 7.15002 2.98 6.65002 4.38 6.65002H5.38C6.78 6.65002 7.38 7.15002 7.38 8.55002V18.35C7.38 19.75 6.78 20.25 5.38 20.25H4.38C2.98 20.25 2.38 19.75 2.38 18.35Z" stroke="#F8E71C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>\n' +
            '                    </svg>'
        let dislikedHtml = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">\n' +
            '                    <path d="M15.609 5.49953V15.6595C15.609 16.0595 15.489 16.4495 15.269 16.7795L12.539 20.8395C12.109 21.4895 11.039 21.9495 10.129 21.6095C9.14904 21.2795 8.49904 20.1795 8.70904 19.1995L9.22904 15.9295C9.26904 15.6295 9.18904 15.3595 9.01904 15.1495C8.84904 14.9595 8.59904 14.8395 8.32904 14.8395H4.21904C3.42904 14.8395 2.74904 14.5195 2.34904 13.9595C1.96904 13.4195 1.89904 12.7195 2.14904 12.0095L4.60904 4.51953C4.91904 3.27953 6.26904 2.26953 7.60904 2.26953H11.509C12.179 2.26953 13.119 2.49953 13.549 2.92953L14.829 3.91953C15.319 4.29953 15.609 4.87953 15.609 5.49953Z" fill="#F8E71C"></path>\n' +
            '                    <path d="M18.7894 17.6084H19.8194C21.3694 17.6084 21.9994 17.0084 21.9994 15.5284V5.47844C21.9994 3.99844 21.3694 3.39844 19.8194 3.39844H18.7894C17.2394 3.39844 16.6094 3.99844 16.6094 5.47844V15.5384C16.6094 17.0084 17.2394 17.6084 18.7894 17.6084Z" fill="#F8E71C"></path>\n' +
            '                </svg>'
        let normalDislikeHtml = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">\n' +
            '                    <path d="M16.52 5.65002L13.42 3.25002C13.02 2.85002 12.12 2.65002 11.52 2.65002H7.71998C6.51998 2.65002 5.21998 3.55002 4.91998 4.75002L2.51998 12.05C2.01998 13.45 2.91998 14.65 4.41998 14.65H8.41998C9.01998 14.65 9.51998 15.15 9.41998 15.85L8.91998 19.05C8.71998 19.95 9.31998 20.95 10.22 21.25C11.02 21.55 12.02 21.15 12.42 20.55L16.52 14.45" stroke="#F8E71C" stroke-width="1.5" stroke-miterlimit="10"></path>\n' +
            '                    <path d="M21.62 5.65V15.45C21.62 16.85 21.02 17.35 19.62 17.35H18.62C17.22 17.35 16.62 16.85 16.62 15.45V5.65C16.62 4.25 17.22 3.75 18.62 3.75H19.62C21.02 3.75 21.62 4.25 21.62 5.65Z" stroke="#F8E71C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>\n' +
            '                </svg>'

        let savedHtml = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">\n' +
            '                    <path d="M12.89 5.87891H5.11C3.4 5.87891 2 7.27891 2 8.98891V20.3489C2 21.7989 3.04 22.4189 4.31 21.7089L8.24 19.5189C8.66 19.2889 9.34 19.2889 9.75 19.5189L13.68 21.7089C14.96 22.4089 16 21.7989 16 20.3489V8.98891C16 7.27891 14.6 5.87891 12.89 5.87891Z" fill="#F8E71C"></path>\n' +
            '                    <path d="M21.9998 5.11V16.47C21.9998 17.92 20.9598 18.53 19.6898 17.83L17.7598 16.75C17.5998 16.66 17.4998 16.49 17.4998 16.31V8.99C17.4998 6.45 15.4298 4.38 12.8898 4.38H8.81984C8.44984 4.38 8.18984 3.99 8.35984 3.67C8.87984 2.68 9.91984 2 11.1098 2H18.8898C20.5998 2 21.9998 3.4 21.9998 5.11Z" fill="#F8E71C"></path>\n' +
            '                </svg>'
        let normalSaveHtml = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">\n' +
            '                    <path d="M12.89 5.87988H5.10999C3.39999 5.87988 2 7.27987 2 8.98987V20.3499C2 21.7999 3.04 22.4199 4.31 21.7099L8.23999 19.5199C8.65999 19.2899 9.34 19.2899 9.75 19.5199L13.68 21.7099C14.95 22.4199 15.99 21.7999 15.99 20.3499V8.98987C16 7.27987 14.6 5.87988 12.89 5.87988Z" stroke="#F8E71C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>\n' +
            '                    <path d="M16 8.98987V20.3499C16 21.7999 14.96 22.4099 13.69 21.7099L9.76001 19.5199C9.34001 19.2899 8.65999 19.2899 8.23999 19.5199L4.31 21.7099C3.04 22.4099 2 21.7999 2 20.3499V8.98987C2 7.27987 3.39999 5.87988 5.10999 5.87988H12.89C14.6 5.87988 16 7.27987 16 8.98987Z" stroke="#F8E71C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>\n' +
            '                    <path d="M22 5.10999V16.47C22 17.92 20.96 18.53 19.69 17.83L16 15.77V8.98999C16 7.27999 14.6 5.88 12.89 5.88H8V5.10999C8 3.39999 9.39999 2 11.11 2H18.89C20.6 2 22 3.39999 22 5.10999Z" stroke="#F8E71C" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>\n' +
            '                </svg>'

        const commentForm = $('#comment-form');
        const deleteButton = $('.delete-button')

        function likePost() {
            const post_id = $(this).data('post-id');
            let url = likePostUrl.replace('0', post_id)

            likesAjax(
                url,
                post_id,
                function (response) {
                    updateLikesCount(response, post_id);
                }
            );
        }

        function dislikePost() {
            const post_id = $(this).data('post-id');
            let url = dislikePostUrl.replace('0', post_id)
            likesAjax(
                url,
                post_id,
                function (response) {
                    updateLikesCount(response, post_id);
                }
            );
        }

        function savePost() {
            const post_id = $(this).data('post-id');
            let url = savePostUrl.replace('0', post_id);
            likesAjax(
                url,
                post_id,
                function (response) {
                    if (response['success']) {
                        let saved = response['saved'];
                        if (saved) {
                            $('#save-button-' + post_id).html(savedHtml);
                        } else {
                            $('#save-button-' + post_id).html(normalSaveHtml);
                        }
                    }
                }
            );
        }

        function likesAjax(url, post_id, callback) {
            $.ajax({
                url: url,
                type: 'GET',
                success: callback
            });
        }

        function updateLikesCount(response, post_id) {
            if (response['success']) {
                let likes = response['likes'];
                let dislikes = response['dislikes'];
                let liked = response['liked'];
                let disliked = response['disliked'];
                if (liked) {
                    $('#like-button-' + post_id).html(likedHtml);
                } else {
                    $('#like-button-' + post_id).html(normalLikeHtml);
                }
                if (disliked) {
                    $('#dislike-button-' + post_id).html(dislikedHtml);
                } else {
                    $('#dislike-button-' + post_id).html(normalDislikeHtml);
                }

                $('#like-count-' + post_id).text(likes);
                $('#dislike-count-' + post_id).text(dislikes);
            } else {
                alert('Error');
            }
        }

        function sharePost() {
            const post_id = $(this).data('post-id');
            navigator.clipboard.writeText(window.location.href + 'post/' + post_id + '/').then(r => {
                alert('Link copied to clipboard')
            });
        }

        function deletePost() {
            let thisButton = $(this)
            let dataType = thisButton.data('type')
            let url;
            let postId = thisButton.data('post-id')
            if (dataType === 'post') {
                url = deletePostUrl.replace('0', postId)

            } else if (dataType === 'comment') {
                let comment_id = thisButton.data('comment-id')
                url = deleteCommentUrl.replace('0', comment_id)
            }
            $.ajax(
                {
                    url: url,
                    type: 'GET',
                    success: function (response) {
                        if (response['success']) {
                            if (dataType === 'post') {
                                location.href = response['redirect_url']
                            } else {
                                $(thisButton.data('element-id')).remove()
                                $('#comments-count-' + postId).text(response['comment_count'])
                            }
                        }
                    }
                }
            );
        }

        function submitNewComment(event) {
            event.preventDefault();
            const commentText = $('#comment-input').val();
            if (commentText === '') {
                return;
            }
            const url = commentForm.attr('action');
            const data = commentForm.serialize();
            const postId = commentForm.data('post-id');
            $.ajax({
                    url: url,
                    data: data,
                    method: 'POST',
                    success: function (response) {
                        if (response['success']) {
                            $('#post-comments-list').prepend(
                                $(
                                    `<div class="dis-col padding-10 gap-5 position-rel" id="comment-${response['comment']['id']}">
                                        <div class="less-action-button-corner delete-button" id="comment-delete-${response['comment']['id']}" data-type="comment" data-comment-id="${response['comment']['id']}" data-element-id="#comment-${response['comment']['id']}">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                                <path d="M21 5.97998C17.67 5.64998 14.32 5.47998 10.98 5.47998C9 5.47998 7.02 5.57998 5.04 5.77998L3 5.97998" stroke="#FF4136" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                                <path d="M8.5 4.97L8.72 3.66C8.88 2.71 9 2 10.69 2H13.31C15 2 15.13 2.75 15.28 3.67L15.5 4.97" stroke="#FF4136" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                                <path d="M18.85 9.14001L18.2 19.21C18.09 20.78 18 22 15.21 22H8.79002C6.00002 22 5.91002 20.78 5.80002 19.21L5.15002 9.14001" stroke="#FF4136" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                                <path d="M10.33 16.5H13.66" stroke="#FF4136" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                                <path d="M9.5 12.5H14.5" stroke="#FF4136" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                                            </svg>
                                        </div>
                                        <a href="${profilePageUrl.replace('-username-', response['comment']['user']['username'])}">
                                            <div class="dis-row gap-10">
                                                <div class="small-avatar">
                                                    <img class="avatar" src="${response['comment']['user']['profile_picture']}" alt="Avatar">
                                                </div>
                                                <div class="dis-col just-cent">
                                                    <div class="fullname text-color">${response['comment']['user']['fullname']}</div>
                                                    <div class="username text-color">@${response['comment']['user']['username']}</div>
                                                </div>
                                            </div>
                                        </a>
                                        <div class="dis-row text-color comment">${response['comment']['content']}</div>
                                    </div>`
                                )
                            )
                            $('#comments-count-' + postId).text(response['comment_count'])
                            $(`#comment-delete-${response['comment']['id']}`).click(
                                deletePost
                            )
                            commentForm.trigger("reset");
                        }
                    }
                }
            )
        }

        $('.like-button').click(likePost);
        $('.dislike-button').click(dislikePost);
        $('.save-button').click(savePost);
        $('.post-share-button').click(sharePost);
        $('.post-content').dblclick(likePost);
        deleteButton.click(deletePost);
        $('.admin-posts').click(
            function () {
                let postId = $(this).data('post-id');
                let url = adminPostDetailUrl.replace('0', postId);
                location.href = url;
            }
        )
        commentForm.submit(submitNewComment);
    }
)