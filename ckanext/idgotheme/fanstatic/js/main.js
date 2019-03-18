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

// Init Bootstrap Tooltips
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

// Update resource size in resource list (ckan: dataset)
$('#dataset-resources .resource-list .resource-item [name="size"]').each(function(){
  var size_bytes = $(this).attr('data-size');
  $(this).children('span[name="size-value"]').html(toOctetString(size_bytes));
});

// Update resource size in additional info (ckanext-scheming)
var resource_size = $('table tr[name="size"] td').html();
$('table tr[name="size"] td').html(toOctetString(resource_size));

// Modal resource download
$(document).on("click", ".open-download-modal", function () {
  var resourceID = $(this).data('id');
  var resourceName = $(this).data('name');
  var resourceURL = $(this).data('url');
  // TODO: AJAX request to get modal text -> $("#download-modal-res-list .modal-custom-content")
  $("#download-modal-res-list .resource-name").html(resourceName);
  $("#download-modal-res-list .download-button-resource").attr("href", resourceURL);
});
