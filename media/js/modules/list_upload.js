Application.addModule('list_uploader', function(context) {

	var uploadNotification = 'upload_notification';

	function beforeListUpload(formData, $form, options) {
		console.log($form.find('input[type=file]').val());
		var alertString = 'Please select a file to be submitted!';
		if (!$form.find('input[type=file]').val()) {
			alert(alertString);
			return false;
		}

		return true;
	}

	function listUploadError(responseText, statusText, xhr, $form) {
		console.log(responseText, statusText, xhr, $form);
		alert('Could not upload your file. Status was ' + statusText + ' ' + xhr + '. Please retry your upload.');
	}

	function listUploadSuccess(responseText, statusText, xhr, $form) {
		console.log(responseText, statusText, xhr, $form);
		context.broadcast(uploadNotification, {});
	}

	return {
		notifications: [],

		init: function() {
			context.getElement().find('.uploader_form').ajaxForm({
				beforeSubmit: beforeListUpload,
				error: listUploadError,
				success: listUploadSuccess,
			});
		}
	}
});
