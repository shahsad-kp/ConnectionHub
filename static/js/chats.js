$(document).ready(
    function () {
        let send_message_form = $('#message-bar')
        let input_message = $('#message-input')
        let message_body = $('#message-body')
        const endpoint = 'ws://' + window.location.host + '/chat/';
        let socket = new WebSocket(endpoint)

        socket.onopen = async function (e) {
            send_message_form.on('submit', function (e) {
                e.preventDefault()
                let message = input_message.val()
                let username = $(this).data('username')

                let data = {
                    'message': message,
                    'username': username
                }
                data = JSON.stringify(data)
                socket.send(data)
                $(this)[0].reset()
            })
        }

        socket.onmessage = async function (e) {
            console.log('message', e)
            let data = JSON.parse(e.data)
            newMessage(data)
        }

        socket.onerror = async function (e) {
            console.log('error', e)
        }

        socket.onclose = async function (e) {
            console.log('close', e)
        }

        function newMessage(data) {
            let message_element;
            let ownUsername = $('#msgs-section').data('own-username')
            let otherUsername = send_message_form.data('username')
            let senderUsername = data['sender']['username']
            let receiverUsername = data['receiver']['username']
            if (data['is_sender'] === true) {
                message_element = "<div class=\"msg right-msg\">\n" +
                    "        <div\n" +
                    "                class=\"msg-img\"\n" +
                    "                style=\"background-image: url("+ data['sender']['avatar'] +")\"\n" +
                    "        ></div>\n" +
                    "\n" +
                    "        <div class=\"msg-bubble secondary-background\">\n" +
                    "            <div class=\"msg-info\">\n" +
                    "                <div class=\"msg-info-name\">You</div>\n" +
                    "                <div class=\"msg-info-time time\" data-time=\""+ data['timestamp'] +"\"></div>\n" +
                    "            </div>\n" +
                    "\n" +
                    "            <div class=\"msg-text\">"+ data["message"] +"</div>\n" +
                    "        </div>\n" +
                    "    </div>"
            }
            else {
                message_element = "<div class=\"msg left-msg\">\n" +
                    "        <div\n" +
                    "                class=\"msg-img\"\n" +
                    "                style=\"background-image: url("+ data['sender']['avatar'] +")\"\n" +
                    "        ></div>\n" +
                    "\n" +
                    "        <div class=\"msg-bubble accent-three-bg\">\n" +
                    "            <div class=\"msg-info\">\n" +
                    "                <div class=\"msg-info-name\">@" + data["sender"]["username"] + "</div>\n" +
                    "                <div class=\"msg-info-time time\" data-time=\""+ data['timestamp'] +"\"></div>\n" +
                    "            </div>\n" +
                    "\n" +
                    "            <div class=\"msg-text\">"+ data["message"] +"</div>\n" +
                    "        </div>\n" +
                    "    </div>"
            }
            if (
                (otherUsername===senderUsername&&ownUsername===receiverUsername) ||
                (otherUsername===receiverUsername&&ownUsername===senderUsername)
            ){
                message_body.append(message_element)
                $('#no-chat').remove()
                message_body.scrollTop(message_body[0].scrollHeight);
            }

            updateUserToFront(data)
        }

        function updateUserToFront(data) {
            let ownUsername = $('#msgs-section').data('own-username')
            let senderUsername = data['sender']['username']
            let userdata = data['sender']
            if (senderUsername === ownUsername){
                userdata = data['receiver']
            }
            let username = userdata['username']
            let userData = $('#chat-user-' + username)

            if (userData.length === 0) {
                userData = '<a href="/chat/'+ username +'/" id="chat-user-'+ username +'">\n' +
                    '    <div class="dis-row gap-10" style="align-items: center">\n' +
                    '        <div class="small-avatar">\n' +
                    '            <img class="avatar" src="'+ userdata['avatar'] +'" alt="Avatar">\n' +
                    '        </div>\n' +
                    '        <div class="dis-col just-cent">\n' +
                    '            <div class="fullname text-color">'+ userdata['fullname'] +'</div>\n' +
                    '            <div class="username text-color">@' + userdata['username'] + '</div>' +
                    '        </div>\n' +
                    '        <span class="badge accent-one-bg ' + (senderUsername !== ownUsername? 'showing-badge': '') + '" id="badge-' + userdata['username'] + '"></span>\n' +
                    '    </div>\n' +
                    '</a>'
                $('#chat-users-list').prepend(userData)
                $('.no-chats-available').remove()
            }
            else{
                userData.prependTo('#chat-users-list')
                let badge = $('#badge-' + senderUsername)
                if (!badge.hasClass('showing-badge')){
                    badge.addClass('showing-badge')
                }
            }

        }

        function updateTimeSince(timeString) {
            let time;
            const then = new Date(timeString);
            const now = new Date();
            const secondsPast = (now.getTime() - then.getTime()) / 1000;
            const minutesPast = Math.floor(secondsPast / 60);
            const hoursPast = Math.floor(minutesPast / 60);
            const daysPast = Math.floor(hoursPast / 24);

            if (daysPast > 6) {
                const year = then.getFullYear() === now.getFullYear() ? '' : ' ' + then.getFullYear();
                const month = then.toLocaleString('default', {month: 'short'});
                const day = then.getDate();
                time = then.toLocaleTimeString([], {hour: 'numeric', minute: '2-digit'});
                return month + ' ' + day + year + ', ' + time;
            } else if (daysPast > 0) {
                const days = daysPast === 1 ? "1 day" : daysPast + " days";
                time = then.toLocaleTimeString([], {hour: 'numeric', minute: '2-digit'});
                return days + " ago, " + time;
            } else if (hoursPast > 0) {
                return hoursPast + " hours ago";
            } else if (minutesPast > 0) {
                return minutesPast + " minutes ago";
            } else {
                return "just now";
            }
        }

        function updateDisplayedTime() {
            $('.time').each(function () {
                const timeString = $(this).data('time');
                const timeSince = updateTimeSince(timeString);
                $(this).text(timeSince);
            });
        }
        if (message_body){
            message_body.scrollTop(message_body[0].scrollHeight);
        }
        updateDisplayedTime();
        setInterval(updateDisplayedTime, 1000);
    }
)