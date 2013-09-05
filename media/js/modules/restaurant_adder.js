Application.addModule('restaurant_adder', function(context) {
	'use strict';

	function validateRestaurant(formData, $form, options) {
		context.log($form.find('input[type=file]').val());
		var alertString = 'Please select a file to be submitted!';
		if (!$form.find('input[type=file]').val()) {
			alert(alertString);
			return false;
		}

		showLoadingStatus();
		return true;
	}

	function restaurantAddError(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		alert('Could not add this restaurant. Status was ' + statusText + ' ' + xhr + '. Please retry.');
	}

	function restaurantAddSuccess(responseText, statusText, xhr, $form) {
	}

	return {
		notifications: [],

		init: function () {
			context.getElement().ajaxForm({
				beforeSubmit: validateRestaurant,
				error: restaurantAddError,
				success: restaurantAddSuccess
			});
		}
	};
});
