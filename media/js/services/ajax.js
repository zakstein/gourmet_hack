Application.addService('ajax', function(application) {
	'use strict';

	return {
		getHtmlFromServer: function(url, data, callback) {
			// For now, just wrap jQuery
			$.get(url, data, callback, 'html');
		},

		getJSONFromServer: function(url, data, callback) {
			// For now, just wrap jQuery
			$.get(url, data, callback, 'json');
		},

		postToServerReturnJSON: function (url, data, callback) {
			data = data || {};

			// Add csrf token
			var csrfToken = $.cookie('csrftoken');
			data['csrfmiddlewaretoken'] = csrfToken;

			$.post(url, data, callback, 'json');
		}
	};
});
