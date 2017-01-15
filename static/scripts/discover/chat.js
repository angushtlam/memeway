$(document).ready(function () {
	if (!(document.referrer.includes('/discover/chat'))) {
		$('.user-contacts').addClass('animated slideInDown');
	}

	$('.chat').scrollTop($(".chat")[0].scrollHeight);
});
