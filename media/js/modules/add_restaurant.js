Application.addModule('add_restaurant', function(context) {
	'use strict';

	var restaurant_added_notification = 'restaurant_added',
		form_validation_service = context.getService('form_validator');

	function validateRestaurant(formData, $form, options) {
		form_validation_service.validate_add_restaurant($form);
	}

	function restaurantAddError(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		alert('Could not add this restaurant. Status was ' + statusText + ' ' + xhr + '. Please retry.');
	}

	function restaurantAddSuccess(responseText, statusText, xhr, $form) {
		var searchLocationElement = $form.find('.searchLocation');
		var searchLocationElementValue = searchLocationElement.val();
		$form.clearForm();
		var $modal = $form.closest('.modal');
		$modal.modal('hide');
		searchLocationElement.val(searchLocationElementValue);
		context.broadcast(restaurant_added_notification , {});
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
