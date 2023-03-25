$(document).ready(
    function () {
        const searchBar = $('#user-search-bar');
        const searchArea = $('#' + searchBar.data('user-search-area'));
        const followButton = $('.follow-button');
        const blockButton = $('.block-button');
        const reportButton = $('.report-button');
        const sendRequestButton = $('.request-button');
        const acceptRequestButton = $('.request-accept');
        const rejectRequestButton = $('.request-reject');

        $('#' + searchBar.data('results-id')).hide()

        function searchUsers() {
            const search_results = $(this).data('results-id');
            const text = $(this).val();
            if (text.length > 0) {
                $.ajax({
                    url: searchUsersUrl,
                    type: 'GET',
                    data: {
                        'q': text
                    },
                    success: function (response) {
                        let htmlText = '';
                        let results = response['results'];
                        if (results.length === 0) {
                            htmlText = '<div class="search-result">\n' +
                                '            <div class="right-bar-content-text">\n' +
                                '                <div class="right-bar-content-text-name text-color">No results found</div>\n' +
                                '            </div>\n' +
                                '        </div>'
                        }

                        for (let i = 0; i < results.length; i++) {
                            let result = results[i];
                            let profileUrl = profilePageUrl.replace('-username-', result['username']);
                            htmlText += '<a href="' + profileUrl + '">' +
                                '   <div class="dis-row gap-10"> \n' +
                                '       <div class="small-avatar"> \n' +
                                '           <img class="avatar" src="' + result['profile_picture'] + '" alt="Avatar">' +
                                '        </div>' +
                                '        <div class="dis-col">' +
                                '            <div class="fullname text-color">' + result['fullname'] + '</div>' +
                                '            <div class="username text-color">@' + result['username'] + '</div>' +
                                '        </div>' +
                                '    </div>' +
                                '</a>'
                        }
                        $('#' + search_results).html(htmlText).show();

                    }
                });
            } else {
                $('#' + search_results).hide();
            }
        }

        function followUser() {
            let thisButton = $(this)
            let username = thisButton.data('username');
            let following = thisButton.hasClass('following');
            let url;
            if (following === false) {
                url = followUserUrl.replace('-username-', username);
            } else {
                url = unfollowUserUrl.replace('-username-', username);
            }
            $.ajax({
                url: url,
                type: 'GET',
                success: function (response) {
                    if (response['success']) {
                        $(thisButton.data('remove-data')).remove()
                        let followButton = $(`#follow-button-${username}`)
                        if (response['followed']) {
                            followButton.addClass('following')
                            followButton.html('Unfollow')
                            followButton.removeAttr('data-remove-data')
                        }
                        else {
                            if (response['private_account']){
                                location.reload()
                                return
                            }
                            followButton.removeClass('following')
                            followButton.html('Follow')
                            followButton.attr(
                                'data-remove-data',
                                `.follow-remover-${username}`
                            )
                        }
                        $(`#followers-count-${username}`).html(`${response['followers']} Followers`)
                        $(`#followings-count${username}`).html(`${response['followings']} Followings`)
                        refreshSideBar()
                    }
                }
            });
        }

        function sendRequest() {
            let username = $(this).data('username');
            let thisButton = $(this)
            let url
            let requested = thisButton.hasClass('requested')
            if (requested === true) {
                url = cancelFollowRequestUrl.replace('-username-', username);
            } else {
                url = sendFollowRequestUrl.replace('-username-', username);
            }
            $.ajax({
                url: url,
                type: 'GET',
                success: function (response) {
                    if (response['success']) {
                        $(thisButton.data('remove-data')).remove()
                        if (response['requested']) {
                            thisButton.addClass('requested')
                            thisButton.html('Cancel Request')
                            thisButton.removeAttr('remove-data')
                        } else {
                            thisButton.removeClass('requested')
                            thisButton.html('Send Request')
                            thisButton.attr(
                                'data-remove-data',
                                `.follow-remover-${username}`
                            )
                        }
                        refreshSideBar()
                    }
                }
            });
        }


        function refreshSideBar() {
            if ($('#suggestions-list').children().length === 0) {
                $('#suggestion-area').remove()
            }
            if ($('#following-list').children().length === 0) {
                $('#following-area').remove()
            }
        }

        function reportUser() {
            let reason = prompt("Why you are reporting this user?");
            if (reason !== null) {
                let username = $(this).data('username');
                let csrftoken = $('input[name=csrfmiddlewaretoken]').val()
                let url = reportUserUrl.replace('-username-', username)
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrftoken,
                        'reason': reason
                    },
                    success: function (response) {
                        if (response['success']) {
                            alert('User reported successfully');
                        }
                    }
                });
            }

        }

        function blockUser() {
            let thisButton = $(this)
            let username = thisButton.data('username');
            let blocked = thisButton.hasClass('blocked');
            let url;
            if (blocked === false) {
                url = blockUserUrl.replace('-username-', username);
            } else {
                url = unblockUserUrl.replace('-username-', username);
            }
            $.ajax({
                url: url,
                type: 'GET',
                success: function (response) {
                    if (response['success']) {
                        if (response['blocked']) {
                            thisButton.addClass('blocked')
                            thisButton.html('Unblock')
                            $('#follow-button-div').replaceWith(
                                $('<div id="blocked-text" class="danger-text-color">You blocked this user..</div>')
                            )
                        } else {
                            thisButton.removeClass('blocked')
                            thisButton.html('Block')
                            $('#blocked-text').replaceWith(
                                $(
                                    `<div id="follow-button-div">
                                        <button class="follow-button accent-two-bg text-color" data-username="${username}"
                                         data-remove-data=".follow-remover-${username}">
                                            Follow
                                        </button>
                                    </div>`
                                )
                            )
                        }
                    }
                }
            });
        }

        function respondRequest() {
            let thisButton = $(this)
            let username = thisButton.data('username');
            let accept = thisButton.hasClass('request-accept');
            let url = respondFollowRequestUrl.replace('-username-', username);
            if (accept === true) {
                url = url.replace('-action-', 'accept');
            } else {
                url = url.replace('-action-', 'reject');
            }
            $.ajax({
                url: url,
                type: 'GET',
                success: function (response) {
                    if (response['success']) {
                        $(thisButton.data('remove-data')).remove()
                        if ($('#follow-requests-list').children().length === 0){
                            $('#follow-requests-area').remove()
                        }
                    }
                }
            });
        }

        searchBar.on(
            'input',
            searchUsers
        )

        searchArea.focusout(
            function () {
                const search_results = $(this).data('results-id');
                $('#' + search_results).hide();
            }
        )

        followButton.click(
            followUser
        )

        reportButton.click(
            reportUser
        )

        blockButton.click(
            blockUser
        )

        sendRequestButton.click(
            sendRequest
        )

        acceptRequestButton.click(
            respondRequest
        )

        rejectRequestButton.click(
            respondRequest
        )
    }
)