window.Application = (function() {
	'use strict';

	var debug,
		modules = {}, // Information about modules by moduleName
		services = {}, // Information about services by serviceName
		widgets = {}, // Information about widgets by widgetName
		instances = {}, // Module instances that have been instantiated
		eventTypes = ['click', 'mouseout', 'mouseover', 'focus', 'blur']; // Event types used for event listeners

	function getModuleName(element) {
		var moduleDeclaration = $(element).data('module');

		if (moduleDeclaration) {
			return moduleDeclaration.split('-')[0];
		}
		
		return '';
	}

	function config(params) {
		debug = params.debug || false;
	}

	function log() {
		if (window.console && console.log) {
			console.log.apply(console, arguments);
		}
	}

	function callModuleMethod(obj, method) {
		if (typeof obj[method] === 'function') {
			obj[method].apply(obj, Array.prototype.slice.call(arguments, 2));
		}
	}

	function getInstanceByElement(element) {
		return instances[element.id];
	}

	function initModuleInstance(moduleName, moduleElement, application) {
		var moduleData = modules[moduleName],
			module,
			instance,
			context;

		moduleElement.id = 'mod-' + moduleName + '-' + moduleData.counter;
		moduleData.counter++;

		context = new Context(application, moduleName, moduleElement.id);

		module = moduleData.creator(context);

		instance = {
			moduleName: moduleName,
			module: module,
			context: context,
			element: moduleElement,
			eventHandlers: {}
		};

		bindEventListeners(instance);

		instances[moduleElement.id] = instance;

		callModuleMethod(instance.module, 'init');
		if (debug) log(moduleName + ' init()');
	}

	function getWidget(widgetName, application) {
		var widgetData = widgets[widgetName],
				widget;

		return widgetData.creator(application);
	}

	function bindEventListeners(instanceData) {
		var eventType,
			eventHandlerName,
			moduleInstance = instanceData.module,
			moduleElement = instanceData.element;

		for (var i in eventTypes) {
			eventType = eventTypes[i];

			eventHandlerName = 'on' + eventType;

			if (moduleInstance[eventHandlerName]) {
				$(moduleElement).on(eventType, moduleInstance[eventHandlerName]);
			}
		}
	}

	return {

		/**
		 * Called on page initialization. Currently, it creats all modules
		 * @param params Currently only accepts debug
		 */
		init: function(params) {
			params = params || {};
			config(params);
			this.startAll(document.body);
		},

		/**
		 * Called when we are tearing down a page
		 */
		destroy: function() {
			this.stopAll();

			modules = {};
			services = {};
		},

		/**
		 * Starts all modules that have been added
		 */
		startAll: function(root_element) {
			var me = this;

			$(root_element).find('.module').each(function(idx, element) {
				me.start(element);
			});
		},

		/**
		 * Starts a module associated with the given element
		 */
		start: function(element) {
			var moduleName = getModuleName(element);

			if (!this.isStarted(element)) {
				initModuleInstance(moduleName, element, this);
			}
		},

		/**
		 * Stops all modules
		 */
		stopAll: function() {
			for (var id in instances)
			{
				this.stop(instances[id].element);
			}
		},

		/**
		 * Calls destroy on a module and deletes its instance(s)
		 */
		stop: function(element) {
			var instance = getInstanceByElement(element),
				moduleName = instance.moduleName,
				moduleData = modules[moduleName];

			if (instance) {
				if (debug) log(moduleName + ' destroy()');

				callModuleMethod(instance.module, 'destroy');

				delete instances[element.id];
			}
		},

		/**
		 * Determines whether an instance of a module exists
		 */
		isStarted: function(element) {
			return !!getInstanceByElement(element);
		},

		/**
		 * Registers a new module. This is required to start the module
		 */
		addModule: function(moduleName, creatorFunction) {
			modules[moduleName] = {
				creator: creatorFunction,
				counter: 1
			};
		},

		addWidget: function(widgetName, creatorFunction) {
			widgets[widgetName] = {
				creator: creatorFunction,
				counter: 1
			};
		},

		getWidget: function(widgetName) {
			return getWidget(widgetName, this);
		},

		/**
		 * Broadcasts a notification to any modules listening for the given notification name
		 * @param notificationName
		 * @param notificationData
		 */
		broadcast: function(notificationName, notificationData) {
			var id,
					notificationsAcceptedByModule,
					instanceData;
			for (var id in instances) {
				instanceData = instances[id];
				notificationsAcceptedByModule = instanceData.module.notifications || [];

				if ($.inArray(notificationName, notificationsAcceptedByModule) != -1) {
					callModuleMethod(instanceData.module, 'onnotification', notificationName, notificationData);
				}

			}
		},

		/**
		 * Adds a service to the application
		 */
		addService: function(serviceName, creator) {
			services[serviceName] = {
				creator: creator,
				instance: null
			};
		},

		/**
		 * Gets a service that has been registered with the application
		 */
		getService: function(serviceName) {
			var serviceData = services[serviceName];

			if (serviceData) {
				if (!serviceData.instance) {
					serviceData.instance = serviceData.creator(this);
				}

				return serviceData.instance;
			}
			
			return null;
		}
	};
})();
