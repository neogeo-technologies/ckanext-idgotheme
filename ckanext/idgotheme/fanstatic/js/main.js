// Convert bytes to octets
function toOctetString(value) {
	var len = String(value).length;
	if (len > 6) {
		return (value / 1024 / 1024).toLocaleString('fr-FR') + ' mo';
	} else if (value > 3) {
		return (value / 1024).toLocaleString('fr-FR') + ' ko';
	} else {
		return value + ' octets';
	};
}
$('#dataset-resources .resource-list .resource-item [name="size"]').each(function(){
	var size_bytes = $(this).attr('data-size');
    $(this).children('span[name="size-value"]').html(toOctetString(size_bytes));
});
