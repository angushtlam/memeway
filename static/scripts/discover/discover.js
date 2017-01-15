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