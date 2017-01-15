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
	});
};

$(document).ready(function () {
	$('.meme').each(function () {
		attachToMemeItem(this);
	});

	$('.fab-continue').click(function () {
		var selectedMemes = $('.meme.selected');
		if (selectedMemes.length < 5) {
			alertify.alert('Pick at least 5!');
		} else {
			var data = [];

			selectedMemes.each(function () {
				var memeId = $(this).data('meme-id');
				data.push({'image_id': memeId});
			});


			$.ajax({
				  type: 'POST',
				  url: '/discover/save-meme',
				  data: JSON.stringify(data),
				  error: function (xhr, status, errorThrown) {
				  	// alert(errorThrown);
				  },
				  success: function () {
						window.location.replace('/discover');
				  },
				  dataType: 'text',
				  contentType: 'application/json'
				});
		}
	});
});
