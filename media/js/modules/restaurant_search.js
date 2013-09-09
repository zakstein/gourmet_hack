Application.addModule('restaurant_search', function(context) {
	'use strict';

	var searchTermInputElement,
		searchTermRestaurantIdElement,
		searchLocationInputElement,
		autocompleteSourceUrl = '/restaurant_search/',
		ajaxService = context.getService('ajax');

	function autocompleteSourceFetch(request, response) {
		var location = searchLocationInputElement.val();

		ajaxService.getJSONFromServer(autocompleteSourceUrl, {term: request.term, location: location}, function(json) {
			response(json);
		});
	}

	function autocompleteSelect(event, ui) {
		searchTermInputElement.val(ui.item.label);
		searchTermRestaurantIdElement.val(ui.item.value);
		return false;
	}

	return {
		notifications: [],

		init: function () {
			console.log("HAI");
			searchTermInputElement = context.getElement().find('.searchTerm');
			searchTermRestaurantIdElement = context.getElement().find('.searchTermRestaurantId');
			searchLocationInputElement = context.getElement().find('.searchLocation');
			searchTermInputElement.autocomplete({
				delay: 100,
				minLength: 2,
				source: autocompleteSourceFetch,
				select: autocompleteSelect
			});
		},
	};
});
