Application.addModule('restaurant_list', function(context) {
	'use strict';

	var ajaxService = context.getService('ajax'),
		deleteElementURL = '/delete/',
		updateSortURL = '/update_list_sort/';

	function updateHtml(html) {
		context.getElement().html(html);
	}

	function reloadList() {
		ajaxService.getHtmlFromServer('/restaurant_list/', {}, function(html) {
			updateHtml(html)
		});
	}

	function deleteListElement(listDomElement) {
		ajaxService.postToServerReturnJSON(deleteElementURL, {id: listDomElement[0].id}, function(json) {
			listDomElement.remove();
		});
	}

	function extractInfoFromListRow($listRowElement) {
		var data = {formData: {}};
		$listRowElement.find('li').each(function(index, element) {
			var $element = $(element);
			if (element.className) {
				data['formData'][element.className] = $.trim($element.text());
			}
		});

		data['formData']['restaurant_name'] = $listRowElement.find('.restaurant-name').text();
		data['formData']['has_been'] = $listRowElement.hasClass('.has_been');
		data['formData']['restaurant_list_element_id'] = $listRowElement[0].id;

		data['tags'] = {};

		$listRowElement.find('.tag-name').each(function (idx) {
			var $tag = $(this);
			data['tags'][$tag.data('tag-id')] = $tag.text();
		});

		return data;
	}

	function editListElement(listDomElement) {
		var data = extractInfoFromListRow(listDomElement);
		context.broadcast('edit_restaurant', data);
	}

	function sortList(listSortElement) {
		var new_sort_by,
			new_sort_direction = 'asc';

		new_sort_by = listSortElement.data('sort_by');

		if (listSortElement.hasClass('current-sort')) {
			if (listSortElement.data('sort_direction') == 'asc') {
				new_sort_direction = 'desc';
			}
		}

		ajaxService.postToServerReturnHtml(updateSortURL, {sort_by: new_sort_by, sort_direction: new_sort_direction}, function(html) {
			updateHtml(html);
		});
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
				deleteListElement($target.closest('div'));
			} else if ($target.hasClass('edit_restaurant')) {
				editListElement($target.closest('div'));
			} else if ($target.parent().andSelf().hasClass('sort-menu')) {
				sortList($target);
			}
		}
	};
});

