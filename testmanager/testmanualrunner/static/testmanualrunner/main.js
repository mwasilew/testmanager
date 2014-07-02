var URL = "/testmanualrunner/view/";

angular.module('api', ['ngResource'])
	// .factory('Device', function($resource) {
	// 	return $resource(URL + 'device/:id/', {}, {});
	// })
	// .factory('TestPlan', function($resource) {
	// 	return $resource(URL + 'plan/:id/', {}, {});
	// })
	// .factory('Definitions', function($resource) {
	// 	return $resource(URL + 'definitions/:deviceName/', {}, {});
	// });


var app = angular.module('app', ['ngRoute', 'api'], function(
	$locationProvider,
	$routeProvider,
	$resourceProvider,
	$httpProvider) {

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$resourceProvider.defaults.stripTrailingSlashes = false;

	// $routeProvider
	// 	.when('/', {
	// 		templateUrl: '/static/templates/index.html',
	// 		controller: 'Index'
	// 	})
	// 	.when('/new', {
	// 		templateUrl: '/static/templates/new.html',
	// 		controller: 'New'
	// 	})
	// 	.when('/:testPlanId', {
	// 		templateUrl: '/static/templates/new.html',
	// 		controller: 'Edit'
	// 	})
});
