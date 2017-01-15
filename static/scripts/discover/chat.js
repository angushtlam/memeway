function refreshPage() {
    if ($('#chat-message-field').val() == "") {
       window.location.reload(1);
    }

    setTimeout(refreshPage(), 5000);
}

$(document).ready(function () {
    if (!(document.referrer.includes('/discover/chat'))) {
        $('.user-contacts').addClass('animated slideInDown');
    }

    $('.chat').scrollTop($(".chat")[0].scrollHeight);


    setTimeout(function(){
        refreshPage();
    }, 5000);
});

$('#chat-input-form').submit(function (event) {

    if ($("#talking-to").html() == "memecat") {

        event.preventDefault();

        var chatKey = $('#chat-key').html();

        var data = {
            message: $('#chat-message-field').val(),
            chat_key: chatKey
        };

        $.ajax({
            type: 'POST',
            url: 'https://127.0.0.1:5000',
            data: JSON.stringify(data),
            error: function (xhr, status, errorThrown) {
                alert(errorThrown);
            },
            success: function () {
                location.reload();
            },
            dataType: 'text',
            contentType: 'application/json'
        });

    }
});
