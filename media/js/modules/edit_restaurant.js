Application.addModule('edit_restaurant', function (context) {
	'use strict';

	var restaurant_edited_notification = 'restaurant_edited',
		form_validation_service = context.getService('form_validator'),
		$modal; // The modal containing the edit form

	function beforeSubmitCallback(formData, $form, options) {
		var isValid = form_validation_service.validate_edit_restaurant($form);
		if (isValid) {
			addTagsToForm($form);
		}

		return isValid;
	}

	function addTagsToForm($form) {
		var $tag_input = $form.find('.tag-edit');
		$tag_input.val($tag_input.tokenizer('get'));
	}

	function restaurantEditError(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		alert('Could not add this restaurant. Status was ' + statusText + ' ' + xhr + '. Please retry.');
	}

	function populateForm(data, $form) {
		var formData = data['formData'],
			$tag_input = $form.find('.tag-edit');
		for (var key in formData) {
			var datum = formData[key];
			if (key == 'has_been') {
				$($form[0][key]).prop('checked', data[key]);
			} else {
				$($form[0][key]).val(datum);
			}
		}

		$tag_input.tokenizer({
			allowUnknownTags: true,
			numToSuggest: 5,
			source: fetchTagsForSearchTerm,
			placeholder: 'Edit Tags',
		});

		for (var tag in data['tags']) {
			$tag_input.tokenizer('push', tag);
		}
	}

	function restaurantEditSuccess(responseText, statusText, xhr, $form) {
		context.broadcast(restaurant_edited_notification);
		$form.clearForm();
		var $modal = $form.closest('.modal');
		$modal.modal('hide');
	}

	function fetchTagsForSearchTerm(term, populateCallback) {
		var ajaxService = context.getService('ajax'),
			searchUrl = '/get_tags_for_current_user/' + term;

		ajaxService.getJSONFromServer(searchUrl, populateCallback);
	}

	function handleModalHide(e) {
		$(e.target).find('.tag-edit').tokenizer('destroy');
	}

	return {
		notifications: ['edit_restaurant'],
		init: function() {
			context.getElement().ajaxForm({
				beforeSubmit: beforeSubmitCallback,
				error: restaurantEditError,
				success: restaurantEditSuccess
			});

			$modal = context.getElement().closest('.modal');
			$modal.off('hidden.bs.modal').on('hidden.bs.modal', handleModalHide)
		},

		onnotification: function(name, data) {
			if (name == 'edit_restaurant') {
				populateForm(data, context.getElement());
				$modal.modal('show');
			}
		}
	};
});
