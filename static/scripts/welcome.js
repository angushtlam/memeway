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
			alert('Pick at least 5!');
		} else {
			var missingResponses = selectedMemes.length;

			selectedMemes.each(function () {
				var memeId = $(this).attr('meme-id');

				$.ajax({
				  type: 'POST',
				  url: '/discover/save-meme',
				  data: JSON.stringify({
				  	'image-id': 'memeId'
				  }),
				  error: function (xhr, status, errorThrown) {
				  	alert(errorThrown);
				  },
				  success: function () {
				  	missingResponses--;

				  	if (missingResponses < 1) {
							window.location.replace('/discover');
				  	}
				  },
				  dataType: 'json'
				});
			});
		}
	});
});
