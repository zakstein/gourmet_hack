/**
 * This service just wraps jQuery for now
 */
Application.addService('dom', function(application) {
	'use strict';

	return {
		selectElement: function(selector) {
			$(selector);
		}
	};
});
