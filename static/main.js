angular.module('api', ['ngResource'])
	.factory('TestRun', function($resource) {
		return $resource('testmanualrunner/view/testrun/:id/', {}, {
			update: { method: 'PUT' }
		});
	})
	.factory('Status', function($resource) {
		return $resource('testmanualrunner/view/status/:id/', {}, {});
	})
	.factory('Device', function($resource) {
		return $resource('/testplanner/view/device/:id/', {}, {});
	})
	.factory('TestPlan', function($resource) {
		return $resource('/testplanner/view/plan/:id/', {}, {
			update: { method: 'PUT' }
		});
	})
	.factory('Definitions', function($resource) {
		return $resource('/testplanner/view/definitions/:deviceName/', {}, {});
	})
	.factory('DefinitionYaml', function($resource) {
		return $resource('/testplanner/view/definition-yaml/:id/', {}, {});
	})
	.factory('TestRunResult', function($resource) {
		return $resource('/testmanualrunner/view/testrunresult/:id/', null, {
			update: { method: 'PUT' }
		});
	})
	.factory('TestRunResultBug', function($resource) {
		return $resource('/testmanualrunner/view/testrunresult/:id/bug/', null, {
			add: { method: 'POST' },
			remove: { method: 'POST' },
		});
	})
	.factory('Trackers', function($resource) {
		return $resource('/testrunner/trackers/', null, {});
	})
	.factory('Tag', function($resource) {
		return $resource('/testrunner/tag/:id/', null, {
			update: { method: 'PUT' }
		});
	})
	.factory('Build', function($resource) {
		return $resource('/testrunner/build/:id/', null, {
			'update': {method:'PUT'},
		});
	})



var APP = angular.module('app', ['ngRoute', 'api'], function(
	$locationProvider,
	$routeProvider,
	$resourceProvider,
	$httpProvider,
	$interpolateProvider) {

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$resourceProvider.defaults.stripTrailingSlashes = false;

	$interpolateProvider.startSymbol('//');
	$interpolateProvider.endSymbol('//');
});
