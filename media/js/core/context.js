Context = function(application, moduleName, moduleId) {
	'use strict';

	this.broadcast = function(name, data) {
		application.broadcast(name, data);
	};

	this.getService = function(serviceName) {
		return application.getService(serviceName);
	};

	this.getElement = function() {
		return $('#' + moduleId);
	}
};
