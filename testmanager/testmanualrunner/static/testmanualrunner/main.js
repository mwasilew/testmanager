var URL = "/testmanualrunner/view/";


angular.module('api', ['ngResource'])
	.factory('TestRun', function($resource) {
		return $resource(URL + 'testrun/:id/', {}, {});
	})
	.factory('TestBuild', function($resource) {
		return $resource(URL + 'testrun/:id/', {}, {});
	})
	.factory('Status', function($resource) {
		return $resource(URL + 'status/:id/', {}, {});
	})
	.factory('TestPlan', function($resource) {
		return $resource('/testplanner/view/plan/:id/', {}, {});
	})
	.factory('TestRunResult', function($resource) {
		return $resource(URL + 'testrunresult/:id/', null, {
			update: { method: 'PUT' }
		});
	})



var app = angular.module('app', ['ngRoute', 'api'], function(
	$locationProvider,
	$routeProvider,
	$resourceProvider,
	$httpProvider) {

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$resourceProvider.defaults.stripTrailingSlashes = false;

	$routeProvider
		.when('/testrun/new/:build_id', {
			templateUrl: '/static/testmanualrunner/templates/testrun_form.html',
			controller: 'New'
		})
		.when('/testrun/:id', {
			templateUrl: '/static/testmanualrunner/templates/testrun_execute.html',
			controller: 'Execute'
		})
		.when('/', {
			templateUrl: '/static/testmanualrunner/templates/testrun_form.html',
			controller: 'Index'
		})
});


function Index($scope, $window, $routeParams, TestRun) {
	$scope.test_runs = TestRun.query();
}

function Execute($scope, $window, $routeParams, $q, TestRun, TestPlan, Status, TestRunResult) {
	$q.all([
		Status.query().$promise,
		TestRun.get({id:$routeParams.id}).$promise
	]).then(function(responses) {
		$scope.status_list = responses[0];
		$scope.test_run = responses[1];

		$scope.test_plan = $scope.test_run.test_plan;
		$scope.active_test_definition = $scope.test_plan.tests_definitions[0];

		$scope.tests_definitions_results = _.indexBy(
			$scope.test_run.tests_definitions_results,
			'test_definition'
		);

	})


	$scope.set_status = function(status, test_definition) {
		test_run_result = $scope.tests_definitions_results[test_definition.id];
		$id = test_run_result.id;
		if (status) {
			test_run_result.status = status.id;
		} else {
			test_run_result.status = null;
		}
		TestRunResult.update({id: $id}, test_run_result);
	}


	$scope.load_test_definition = function(test_definition) {
		$scope.active_test_definition = test_definition;
	}

}

function New($http, $scope, $location, $window, $routeParams, TestBuild) {
	var url = URL + 'build/' + $routeParams.build_id + '/';

	$scope.test_plan = {id:null}

	$http.get(url)
		.then(function(response) {
			$scope.build = response.data;
			return $http.get("/testplanner/view/plan/");
		})
		.then(function(response) {
			$scope.test_plan_list = response.data;
		});


	$scope.submit = function() {

		var data = {
			test_plan: $scope.test_plan ? $scope.test_plan.id : null,
			build: $scope.build.id
		};

		$http.post(URL + "view/testrun/", data)
			.success(function(data) {
				$location.path('/testrun/' + data.id);
			}).error(function(error) {
				$scope.error = error;
			});

	}

}
