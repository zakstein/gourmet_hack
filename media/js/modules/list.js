Application.addModule('restaurant_list', function(context) {
	'use strict';

	var ajaxService = context.getService('ajax'),
		deleteElementURL = '/delete/';

	function reloadList() {
		ajaxService.getHtmlFromServer('/restaurant_list/', {}, function(html) {
			context.getElement().find('table').replaceWith(html);
		});
	}

	function deleteListElement(listDomElement) {
		ajaxService.postToServerReturnJSON(deleteElementURL, {id: listDomElement[0].id}, function(json) {
			listDomElement.remove();
		});
	}

	function extractDataFromTableRow($tableRowElement) {
		var data = {};
		$tableRowElement.find('td').each(function(index, element) {
			var $element = $(element);
			if (element.className) {
				if ($element.hasClass('has_been')) {
					data['has_been'] = $element.hasClass('been') ? true : false;
				} else {
					data[element.className] = $.trim($element.text());
				}
			}
		});

		data['restaurant_list_element_id'] = $tableRowElement[0].id;

		return data;
	}

	function editListElement(listDomElement) {
		var data = extractDataFromTableRow(listDomElement);
		context.broadcast('edit_restaurant', data);
	}

	return {
		notifications: ['upload_notification', 'restaurant_added', 'restaurant_edited'],

		onnotification: function(name, data) {
			// We don't care what notification we get, we just reload the list
			reloadList();
		},

		onclick: function(e) {
			var $target = $(e.target);
			if ($target.hasClass('delete_restaurant')) {
				deleteListElement($target.closest('tr'));
			} else if ($target.hasClass('edit_restaurant')) {
				editListElement($target.closest('tr'));
			}
		}
	};
});

