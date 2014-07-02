var URL = "/testmanualrunner/view/";

angular.module('api', ['ngResource'])
	.factory('TestRun', function($resource) {
		return $resource(URL + 'testrun/:id/', {}, {});
	})
	.factory('TestBuild', function($resource) {
		return $resource(URL + 'testrun/:id/', {}, {});
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
		.when('/', {
			templateUrl: '/static/testmanualrunner/templates/testrun_form.html',
			controller: 'Index'
		})
});


function Index($scope, $window, $routeParams, TestRun) {
	$scope.test_runs = TestRun.query();
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
