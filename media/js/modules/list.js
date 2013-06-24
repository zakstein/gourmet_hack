Application.addModule('restaurant_list', function(context) {
	'use strict';

	function reloadList() {
		var ajaxService = context.getService('ajax');
		ajaxService.getHtmlFromServer('/restaurant_list/', {}, function(html) {
			context.getElement().replaceWith(html);
		});
	}

	return {
		notifications: ['upload_notification'],

		onnotification: function(name, data) {
			reloadList();
		}
	};
});

