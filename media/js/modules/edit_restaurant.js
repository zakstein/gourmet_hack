Application.addModule('edit_restaurant', function (context) {
	'use strict';

	var restaurant_edited_notification = 'restaurant_edited',
		form_validation_service = context.getService('form_validator'),
		$modal; // The modal containing the edit form

	function validateRestaurant(formData, $form, options) {
		form_validation_service.validate_edit_restaurant($form);
	}

	function restaurantEditError(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		alert('Could not add this restaurant. Status was ' + statusText + ' ' + xhr + '. Please retry.');
	}

	function populateForm(data, $form) {
		for (var key in data) {
			var datum = data[key];
			if (key == 'has_been') {
				$($form[0][key]).prop('checked', data[key]);
			} else {
				$($form[0][key]).val(datum);
			}
		}
	}

	function restaurantEditSuccess(responseText, statusText, xhr, $form) {
		context.broadcast(restaurant_edited_notification);
		$form.clearForm();
		var $modal = $form.closest('.modal');
		$modal.modal('hide');
	}

	return {
		notifications: ['edit_restaurant'],
		init: function() {
			context.getElement().ajaxForm({
				beforeSubmit: validateRestaurant,
				error: restaurantEditError,
				success: restaurantEditSuccess
			});

			$modal = context.getElement().closest('.modal');
		},

		onnotification: function(name, data) {
			if (name == 'edit_restaurant') {
				populateForm(data, context.getElement());
				$modal.modal('show');
			}
		}
	};
});
