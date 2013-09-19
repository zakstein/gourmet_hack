Application.addModule('list_uploader', function(context) {

	var uploadNotification = 'upload_notification',
		uploadFormElementSelector = '.uploader_form';

	function showLoadingStatus() {
		context.getElement().find('.upload-in-progress').show();
	}

	function hideLoadingStatus() {
		context.getElement().find('.upload-in-progress').hide();
	}

	function beforeListUpload(formData, $form, options) {
		context.log($form.find('input[type=file]').val());
		var alertString = 'Please select a file to be submitted!';
		if (!$form.find('input[type=file]').val()) {
			alert(alertString);
			return false;
		}

		showLoadingStatus();
		return true;
	}

	function listUploadError(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		alert('Could not upload your file. Status was ' + statusText + ' ' + xhr + '. Please retry your upload.');
	}

	function listUploadSuccess(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		context.broadcast(uploadNotification, {});
		hideLoadingStatus();
	}

	return {
		notifications: [],

		init: function() {
			context.getElement().find(uploadFormElementSelector).ajaxForm({
				beforeSubmit: beforeListUpload,
				error: listUploadError,
				success: listUploadSuccess
				// upload_process: processUpload
			});
		},

		onfocus: function(e) {
			var $e = $(e);
			if ($e.hasClass('error')) {
				$e.removeClass('error');
				$e.find('help-inline').remove();
			}
		}
	}
});
