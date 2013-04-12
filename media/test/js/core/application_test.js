module('init');
test('init should call startAll with document.body', function() {
	this.mock(Application).expects('startAll').once().withExactArgs(document.body);
	Application.init();
});

module('destroy');
test('destroy should call stopAll', function() {
	this.mock(Application).expects('stopAll').once();
	Application.destroy();
});

module('startAll');
test('startAll should find and start all module elements', function() {
	var $fixture = $('#qunit-fixture');
	$fixture.append('<div class="module"></div>');
	$fixture.append('<div class="module"></div>');
	
	this.mock(Application).expects('start').twice();

	Application.startAll(document.body);
});

module('tests that require a module', {
	setup: function() {
		this.initStub = sinon.stub();
		this.destroyStub = sinon.stub();
		$('#qunit-fixture').append('<div class="module" data-module="testModule"></div>');
		var me = this;

		Application.addModule('testModule', function(context) {
			return {
				init: me.initStub,
				destroy: me.destroyStub
			};
		});

		Application.start($('.module').get(0));
	},
	teardown: function() {
		Application.destroy();
	}
});

test('start should call init on module', function() {

	equal(1, this.initStub.called);

});

test('stopAll should call stop for each instance', function() {
	this.mock(Application).expects('stop').once();
	Application.stopAll();
});

test('stop should call destroy on the module isntance', function() {
	Application.stop($('.module').get(0));
	equal(1, this.destroyStub.called);
});

test('isStarted should be true after a module is started', function() {
	ok(Application.isStarted($('.module').get(0)));
});

module('service tests', {
	setup: function() {
		this.serviceCreator = sinon.stub();
		Application.addService('testService', this.serviceCreator);
	}
});

test('getService should only call the service creator once', function() {
	var service = Application.getService('testService');
	equal(1, this.serviceCreator.called);
	var same_service = Application.getService('testService');
	equal(1, this.serviceCreator.called);
	equal(service, same_service);
});

