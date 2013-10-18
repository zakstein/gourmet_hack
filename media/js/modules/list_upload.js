Application.addModule('list_uploader', function(context) {

	var uploadNotification = 'upload_notification',
		uploadFormElementSelector = '.uploader_form';

	function showLoadingStatus() {
		context.getElement().find('.upload-in-progress').show();
	}

	function cleanupUpload() {
		var element = context.getElement();
		element.find('.upload-in-progress').hide();
		element.find('.file-input').val(null)
	}

	function updateLoadingStatusWithPercent(percent) {
		context.getElement().find('.bar').width(percent + '%');
	}

	function beforeListUpload(formData, $form, options) {
		context.log($form.find('input[type=file]').val());
		var alertString = 'Please select a file to be submitted!';
		var inputValue = $form.find('input[type=file]').val();
		if (!inputValue) {
			alert(alertString);
			return false;
		}
		if (inputValue.indexOf('csv') == -1 && inputValue.indexOf('xls') == -1 && inputValue.indexOf('xlsx') == -1) {
			alert('Could not read that file. Please upload a csv, xls, or xlsx file');
			return false
		}
		showLoadingStatus();
		return true;
	}

	function updateUploadProgress(e, position, total, percentComplete) {
		updateLoadingStatusWithPercent(percentComplete);
	}

	function listUploadError(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		alert('Could not upload your file. Status was ' + statusText + ' ' + xhr + '. Please retry your upload.');
		cleanupUpload();
	}

	function listUploadSuccess(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		context.broadcast(uploadNotification, {});
		cleanupUpload();
	}

	return {
		notifications: [],

		init: function() {
			var element = context.getElement();
			var formElement = element.find(uploadFormElementSelector);
			formElement.ajaxForm();

			// NOTE (zak): Due to browser awesomeness, the change event doesn't propagate from the input element,
			// so we need to attach an event manually
			element.find('.file-input').on('change', function (e) {
				formElement.ajaxSubmit({
					beforeSubmit: beforeListUpload,
					error: listUploadError,
					success: listUploadSuccess,
					uploadProgress: updateUploadProgress
				})
			});
		},

		destroy: function() {
			context.getElement().find('.file-input').off('change');
		},

		onfocus: function(e) {
			var $target = $(e.target);
			if ($target.hasClass('error')) {
				$target.removeClass('error');
				$target.find('help-inline').remove();
			}
		},
	}
});
