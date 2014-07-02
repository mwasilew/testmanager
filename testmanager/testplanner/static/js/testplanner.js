var URL = "/planner/view/";

angular.module('api', ['ngResource'])
	.factory('Device', function($resource) {
		return $resource(URL + 'device/:id/', {}, {});
	})
	.factory('TestPlan', function($resource) {
		return $resource(URL + 'plan/:id/', {}, {});
	})
	.factory('Definitions', function($resource) {
		return $resource(URL + 'definitions/:deviceName/', {}, {});
	});




var app = angular.module('app', ['ngRoute', 'api'], function(
	$locationProvider,
	$routeProvider,
	$resourceProvider,
	$httpProvider) {

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$resourceProvider.defaults.stripTrailingSlashes = false;

	$routeProvider
		.when('/', {
			templateUrl: '/static/templates/index.html',
			controller: 'Index'
		})
		.when('/new', {
			templateUrl: '/static/templates/new.html',
			controller: 'New'
		})
		.when('/:testPlanId', {
			templateUrl: '/static/templates/new.html',
			controller: 'Edit'
		})

});

function Index($scope, $window, $routeParams, TestPlan) {
	$scope.plans = TestPlan.query();
}

function Edit($scope, $window, $routeParams, TestPlan, Device) {
	$scope.availableDevices = Device.query();

	$scope.testPlan = TestPlan.get({id:$routeParams.testPlanId});
	$scope.device = Device.get({id: $scope.testPlan.device.id});
}

function New($scope, $window, $routeParams, $location, Device, TestPlan, Definitions) {
	$scope.availableDevices = Device.query();

	$scope.testPlan = {
		tests_definitions:[],
		device: {}
	};

	$scope.submit = function() {
		var testPlan = new TestPlan($scope.testPlan);
		testPlan.device = $scope.device.id

		angular.forEach($scope.testDefinitions, function(value, key) {
			if (value.active) {
				this.push(value.id);
			}
		}, testPlan.tests_definitions);

		testPlan.$save().then(function() {
			$location.path('/');
		}, function(error) {
			$scope.error = error.data
		})
	}

	$scope.deviceSelected = function() {
		$scope.testDefinitions = Definitions.query({deviceName:$scope.device.id});
	}

	// $scope.selectDefinition = function(testDefinition) {
	// 	testDefinition.active = !testDefinition.active;
	// }
}
