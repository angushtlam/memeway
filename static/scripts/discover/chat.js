$(document).ready(function () {
	if (!(document.referrer.includes('/discover/chat'))) {
		$('.user-contacts').addClass('animated slideInDown');
	}

	$('.chat').scrollTop($(".chat")[0].scrollHeight);
});

$('#chat-input-form').submit(function (event) {
	if ($("#talking-to").html() == "memecat") {
		var formId = this.id,
        form = this;

    event.preventDefault();

    var chatKey = $('#chat-key').html();

    var data = {
    	text: $('#chat-message-field').val(),
    	chat_key: chatKey
    };

    $.ajax({
		  type: 'POST',
		  url: 'http://127.0.0.1:5000',
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