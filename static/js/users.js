$(document).ready(
    function() {
        const searchBar = $('#user-search-bar');
        const searchArea = $('#'+searchBar.data('user-search-area'));
        const followButton = $('.follow-button');
        const reportButton = $('.report-button');

        $('#'+searchBar.data('results-id')).hide()
        function searchUsers() {
            const search_results = $(this).data('results-id');
            const text = $(this).val();
            if (text.length > 0) {
                $.ajax({
                    url: '/users/search',
                    type: 'GET',
                    data: {
                        'q': text
                    },
                    success: function(response) {
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
                            htmlText += '<a href="/users/'+ result['username'] +'">' +
                                '<li class="search-result">\n' +
                        '            <div class="small-avatar">\n' +
                        '                <img class="avatar" src="' + result['profile_picture'] + '" alt="@' + result['username'] + '">' +
                        '            </div>\n' +
                        '            <div class="right-bar-content-text">\n' +
                        '                <div class="right-bar-content-text-name text-color">'+ result['fullname'] +'</div>\n' +
                        '                <div class="right-bar-content-text-username text-color">@' + result['username'] + '</div>\n' +
                        '            </div>\n' +
                        '        </li>' +
                                '</a>'
                        }
                        $('#' + search_results).html(htmlText).show();

                    }
                });
            }
            else {
                $('#' + search_results).hide();
            }
        }

        function followUser() {
            let username = $(this).data('username');
            let following = !!$(this).hasClass('following');
            let url;
            if (following) {
                url = '/users/' + username + '/unfollow/';
            }
            else {
                url = '/users/' + username + '/follow/';
            }
            $.ajax({
                url: url,
                type: 'GET',
                success: function(response) {
                    if (response['success']) {
                        location.reload()
                    }
                }
            });
        }

        function reportUser() {
            let reason = prompt("Why you are reporting this user?");
            if (reason !== null) {
                let username = $(this).data('username');
                let csrftoken = $('input[name=csrfmiddlewaretoken]').val()
                let url = '/users/' + username + '/report/';
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrftoken,
                        'reason': reason
                    },
                    success: function(response) {
                        if (response['success']) {
                            alert('User reported successfully');
                        }
                    }
                });
            }

        }

        searchBar.on(
            'input',
            searchUsers
        )

        searchArea.focusout(
            function() {
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
    }
)