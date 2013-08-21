Application.addWidget('restaurant_search', function(application) {
	'use strict';

	var $widgetElement;
	var searchUrl = '/show_restaurant_search/';

	function createLoadingOverlay($form_element) {
		// Add overlay + loading gif
	}
	
	function beforeSearch(formData, $form, options) {
		if (!$form.find('.search_query').val() || !$form.find('.search_location').val()) {
			alert('Please enter a restaurant name and a location');
			return false;
		}

		createLoadingOverlay($form);
		return true;
	}

	function searchError(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
		alert('An error occurred: ' + statusText);
	}

	function searchSuccess(responseText, statusText, xhr, $form) {
		context.log(responseText, statusText, xhr, $form);
	}

	return {

		fetchAndDisplayWidget: function(elementIdToReplace, restaurantListElementId) {
			var ajaxService = application.getService('ajax');
			var domService = application.getService('dom');
			var elementSearchUrl = searchUrl;
			var me = this;

			if (restaurantListElementId)
			{
				elementSearchUrl = elementSearchUrl + restaurantListElementId;
			}

			$widgetElement = domService.selectElement('#' + elementIdToReplace);

			ajaxService.getHtmlFromServer(
					elementSearchUrl,
					{},
					function(html) {
						$widgetElement.replaceWith(html);
						me.initWithElement($widgetElement);
					}
			);
		},

		initWithElement: function(element) {
			element.find('search_widget_form').ajaxForm({
				beforeSubmit: beforeSearch,
				error: searchError,
				success: searchSuccess
			});
		}

	};
});
