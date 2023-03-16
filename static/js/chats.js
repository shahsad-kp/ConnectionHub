$(document).ready(
    function () {
        const endpoint = 'ws://' + window.location.host + window.location.pathname;
        let socket = new WebSocket(endpoint)
        let send_message_form = $('#message-bar')
        let input_message = $('#message-input')
        let message_body = $('#message-body')

        socket.onopen = async function (e) {
            send_message_form.on('submit', function (e) {
                e.preventDefault()
                let message = input_message.val()

                let data = {
                    'message': message,
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

            message_body.append(message_element)
            message_body.scrollTop(message_body[0].scrollHeight);

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

        updateDisplayedTime();
        setInterval(updateDisplayedTime, 1000);
    }
)