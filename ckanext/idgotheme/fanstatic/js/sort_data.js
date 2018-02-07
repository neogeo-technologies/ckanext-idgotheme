$('.primary').on('click', '#affich-mode button', function () {
   	var selected_value = $(this).attr('data-affich');
	$('.media-grid').removeClass('affich-grille affich-liste');	
	if (selected_value === 'grille') {
        $('.media-grid').addClass('affich-grille');
    } else if (selected_value === 'liste') {
        $('.media-grid').addClass('affich-liste');
    }
	$('#affich-mode button').removeClass('active');
    $(this).addClass('active');
});
