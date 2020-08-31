let csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
// like and comment notification
let formNotificationSocket = new ReconnectingWebSocket(
    'ws://' + window.location.host +
    '/ws/notification/');


function fetchNotifications() {
    formNotificationSocket.send(JSON.stringify({'command': 'fetch_form_notifications'}));
}

function createFormNotification(notification) {
    let single = `<li>
                        <a href="#" title="">
                            <div class="mesg-meta">
                                <span>Nortication test</span>
                                <i>2 min ago</i>
                            </div>
                        </a>
                    </li>`;
    $('#form-menu').prepend(single);
}
formNotificationSocket.onopen = function (e) {
    fetchNotifications();
};
formNotificationSocket.onmessage = function (event) {
    let data = JSON.parse(event.data);
    if (data['command'] === 'notifications') {
        let notifications = JSON.parse(data['notifications']);
        $('#form-notifications').text(notifications.length);
        for (let i = 0; i < notifications.length; i++) {
            createFormNotification(notifications[i]);
        }
    } else if (data['command'] === 'new_form_notification') {
        let notification = $('#form-notifications');
        notification.text(parseInt(notification.text()) + 1);
        createLikeCommentNotification(JSON.parse(data['notification']));
    }
};

$('#notifications-as-read').click(function () {

    let url = $(this).data('url');

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        }
    });

    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        success: function (res) {
            console.log(res);
            if (res.status === false) {
            }
            if (res.status === true) {}

        },
        error: function (err) {
            console.log(err);
        }
    });
});
