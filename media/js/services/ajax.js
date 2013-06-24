Application.addService('ajax', function(application) {
	'use strict';

	return {
		getHtmlFromServer: function(url, data, callback) {
			// For now, just wrap jQuery
			$.get(url, data, callback, 'html');
		}
	};
});
