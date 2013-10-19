Application.addService('ajax', function(application) {
	'use strict';

	function handleValidationError(xhr, status, errorString) {
		alert('Validation Error');
	}

	return {
		getHtmlFromServer: function(url, data, callback) {
			// For now, just wrap jQuery
			$.get(url, data, callback, 'html');
		},

		getJSONFromServer: function(url, data, callback) {
			// For now, just wrap jQuery
			$.ajax(url, {
				data: data,
				dataType: 'json',
				statusCode: {
					200: callback,
					400: handleValidationError
				}
			});
		},

		postToServerReturnJSON: function (url, data, callback) {
			data = data || {};

			// Add csrf token
			var csrfToken = $.cookie('csrftoken');
			data['csrfmiddlewaretoken'] = csrfToken;

			$.ajax(url, {
				type: 'POST',
				data: data,
				dataType: 'json',
				statusCode: {
					200: callback,
					400: handleValidationError
				}
			});
		},

		postToServerReturnHtml: function (url, data, callback) {
			data = data || {};

			// Add csrf token
			var csrfToken = $.cookie('csrftoken');
			data['csrfmiddlewaretoken'] = csrfToken;

			$.ajax(url, {
				type: 'POST',
				data: data,
				dataType: 'html',
				statusCode: {
					200: callback,
					400: handleValidationError
				}
			});
		}
	};
});
