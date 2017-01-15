var grid = $('.meme-grid');

grid.masonry({
  itemSelector: '.meme',
  columnWidth: '.grid-sizer',
	transitionDuration: 0,
  gutter: 15
});

grid.imagesLoaded().progress(function() {
  grid.masonry('layout');
});

function attachToMemeItem(jqueryObj) {
	$(jqueryObj).click(function () {
		$(this).toggleClass('selected');

		var selectedMemes = $('.meme.selected');

		if (selectedMemes.length > 0) {
			$('.fab-continue').removeClass('disabled');
		} else {
			$('.fab-continue').addClass('disabled');
		}
	});
};

$(document).ready(function () {
	$('.meme').each(function () {
		attachToMemeItem(this);
	});

	$('.fab-continue').click(function () {
		var selectedMemes = $('.meme.selected');
		if (selectedMemes.length < 1) {
			alert('You did not select any memes!');
		} else {
			var data = [];

			selectedMemes.each(function () {
				var memeId = $(this).data('meme-id');
				data.push({'image_id': memeId});
			});


			$.ajax({
				  type: 'POST',
				  url: '/discover/delete-meme',
				  data: JSON.stringify(data),
				  error: function (xhr, status, errorThrown) {
				  	// alert(errorThrown);
				  },
				  success: function () {	
						var selectedMemes = $('.meme.selected');		
						selectedMemes.each(function () {
							$(this).remove();
						});					

						alert('You have removed the selected memes from your profile.');
						$('.fab-continue').addClass('disabled');
						grid.masonry('layout');
				  },
				  dataType: 'text',
				  contentType: 'application/json'
				});
		}
	});
});


function submitForm() {
	$('#account-form').submit();
}