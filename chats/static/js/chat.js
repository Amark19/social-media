let input_msg = $('#input-message')
let msg_body = $('.msg_card_body');
let cur_user_id = $('#loggedIn-user').val();
msg_body.scrollTop(msg_body.prop("scrollHeight"));

let loc = window.location;
let wsStart = 'ws://';

if (loc.protocol == 'https:') {
    wsStart = 'wss://';
}

let endpoint = wsStart + loc.host + loc.pathname;

const socket = new WebSocket(endpoint);

socket.onopen = async function (e) { //called when socket connection is opened,so js inside of it can run line by line as normal js till connection is open
    console.log("Socket opened");
    $('#send-message-form').submit(function (e) {
        e.preventDefault();
        let msg = input_msg.val();
        let data = {
            'message': msg,
            'sent_by': cur_user_id,
            'sent_to': get_active_other_user_id(),
            'thread_id': get_active_chat_id(),
        }
        data = JSON.stringify(data);
        socket.send(data);//send data to server/consumer
    });
}

socket.onmessage = async function (e) { // called when socket receives a message from server/consumer
    console.log("Socket message", e.data);
    let data = JSON.parse(e.data);
    let msg = data['message'], sent_by_id = data['sent_by'], thread = JSON.parse(data['thread']);
    newMessage(msg, sent_by_id, thread.thread_id, thread.user1, thread.user2, thread.profile1, thread.profile2)
}

socket.onclose = async function (e) {
    console.log("Socket closed");
}

socket.onerror = async function (e) {
    console.log("Socket error", e);
}

function getCurrentTime() {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    const currentDate = new Date();
    const currentMonth = months[currentDate.getMonth()];
    const currentDay = currentDate.getDate();
    const currentHour = currentDate.getHours();
    const currentMinute = currentDate.getMinutes();

    const formattedTime = `${currentDay < 10 ? '0' : ''}${currentDay} ${currentMonth}, ${currentHour < 10 ? '0' : ''}${currentHour}:${currentMinute < 10 ? '0' : ''}${currentMinute}`;

    return formattedTime;

}

function newMessage(message, sent_by_id, thread_id, thread_user1_id, thread_user2_id, profile1, profile2) {
    if ($.trim(message) === '') {
        return false;
    }

    let message_element, imgElement;
    let chat_id = 'chat_' + thread_id;
    if (sent_by_id == cur_user_id) {
        if (thread_user1_id == cur_user_id) {
            imgElement = `<img src="${profile1}" class="rounded-circle user_img_msg">`;
        }
        else {
            imgElement = `<img src="${profile2}" class="rounded-circle user_img_msg">`;
        }
        message_element = `
            <div class="d-flex mb-4 replied">
                <div class="msg_cotainer_send">
                    ${message}
                    <span class="msg_time_send">${getCurrentTime()}</span>
                </div>
                <div class="img_cont_msg">
                    ${imgElement}
                </div>
            </div>
        `
    }

    else {
        if (thread_user2_id == cur_user_id) {
            imgElement = `<img src="${profile1}" class="rounded-circle user_img_msg">`;
        }
        else {
            imgElement = `<img src="${profile2}" class="rounded-circle user_img_msg">`;
        }
        message_element = `
            <div class="d-flex mb-4 received">
                <div class="img_cont_msg">
                    ${imgElement}
                </div>
                <div class="msg_cotainer">
                        ${message}
                        <span class="msg_time">${getCurrentTime()}</span>
                </div>
            </div>
        `
    }
    let msg_body = $(`.messages-wrapper[chat-id="${chat_id}"] .msg_card_body`);
    msg_body.append($(message_element))
    msg_body.animate({
        scrollTop: $(document).height()
    }, 100);
    input_msg.val(null);
}

$('.contact-li').click(function (e) {
    $('.contact-li').removeClass('active');
    $(this).addClass('active');
    //msg wrapper
    let chat_id = $(this).attr('chat-id');
    $('.messages-wrapper.is_active').removeClass('is_active');
    $(`.messages-wrapper[chat-id="${chat_id}"]`).addClass('is_active');
})


function get_active_other_user_id() {
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id');
    return other_user_id;
}

function get_active_chat_id() {
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id');
    let thread_id = chat_id.replace('chat_', '')
    return thread_id;
}