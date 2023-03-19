$(document).ready(
    function() {
        const notificationButton = $('.notification');

        function showNotification(event){
            let type = $(this).data('type');
            let id = $(this).data('id');
            let arg = $(this).data('arg');
            $.ajax(
                {
                    url:notificationViewUrl.replace('0', id),
                    type: 'GET',
                }
            )
            if (type==='like'){
                let url = postDetailUrl.replace('0', arg);
                location.href = url;
            }
            else if (type==='comment'){
                let url = postDetailUrl.replace('0', arg);
                location.href = url;
            }
            else if (type==='follow'){
                let url = profilePageUrl.replace('-username-', arg);
                location.href = url;
            }
            else{
                let url = updateProfileUrl;
                location.href = url;
            }


        }

        notificationButton.click(showNotification);
    }
)