// Convert bytes to octets
function toOctetString(value) {
	var len = String(value).length;
	if (len > 6) {
		return (Math.round((value / 1024 / 1024)*10)/10).toLocaleString('fr-FR') + ' Mo';
	} else if (value > 3) {
		return (Math.round(value / 1024)).toLocaleString('fr-FR') + ' Ko';
	} else if (value > 0) {
		return Math.round(value) + ' octets';
	} else {
        return '';
    }
}

// Update resource size in resource list (ckan: dataset)
$('#dataset-resources .resource-list .resource-item [name="size"]').each(function(){
	var size_bytes = $(this).attr('data-size');
    $(this).children('span[name="size-value"]').html(toOctetString(size_bytes));
});

// Update resource size in additional info (ckanext-scheming)
var resource_size = $('table tr[name="size"] td').html();
$('table tr[name="size"] td').html(toOctetString(resource_size));

// Modal API GEO
$('body').on('click', '#show-modal-api-geo', function(){
    $('body').append(
        '<div class="modal fade" id="modal-api-geo" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">'+
            '<div class="modal-dialog" role="document">'+
                '<div class="modal-content">'+
                    '<div class="modal-header">'+
                        '<h3 class="modal-title" id="myModalLabel">'+
                            'API de Données Géographiques'+
                            '<button class="close" data-dismiss="modal">×</button>'+
                        '</h3>'+
                    '</div>'+
                    '<div class="modal-body">Bientôt disponible...</div>'+
                '</div>'+
            '</div>'+
        '</div>'
    );

});

