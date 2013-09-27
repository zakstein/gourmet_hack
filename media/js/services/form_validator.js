Application.addService('form_validator', function(application) {
	'use strict';

	function validate_rating_and_has_been_fields($form) {
		var is_valid = true;
		var form = $form[0];
		var rating = form.rating.value;
		if (form.has_been.value && (isNaN(parseInt(rating)) || parseInt(rating) < 1 || parseInt(rating) > 100)) {
			set_error_for_field($(form.rating), 'Incorrect rating. Enter a number between 1 and 100');
			is_valid = false;
		} else if (!form.has_been.value && rating) {
			set_error_for_field($(form.rating), "Can't rate restaurant if you haven't eaten there");
			is_valid = false;
		}

		return is_valid;
	}

	function set_error_for_field($field, message) {
		message = message || '';
		var $controlGroup = $field.closest('.control-group');

		$controlGroup.addClass('error');
		$controlGroup.append('<div class="help-inline">' + message + '</div>');
	}

	return {
		validate_add_restaurant: function($form) {
			var is_valid = true;

			var form = $form[0];

			if (!form.restaurant_id.value) {
				set_error_for_field($(form.restaurant_name), 'Please enter a restaurant to add');
				is_valid = false;
			} else if (!validate_rating_and_has_been_fields($form)) {
				is_valid = false;
			}

			return is_valid;
		},

		validate_edit_restaurant: function($form) {
			return validate_rating_and_has_been_fields($form);
		}
	};
});
