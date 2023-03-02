$(document).ready(
    function() {
        let searchBar = $('#user-search-bar')
        let searchArea = $('#'+searchBar.data('user-search-area'))
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
    }
)