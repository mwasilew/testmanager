APP.config(['$routeProvider', function($routeProvider) {

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

}]);

function Index($scope, $window, $routeParams, TestRun) {
	$scope.test_runs = TestRun.query();
}

function Execute($scope, $window, $routeParams, $q, TestRun, TestPlan, Status, TestRunResult, Bug) {
	$q.all([
		Status.query().$promise,
		TestRun.get({id:$routeParams.id}).$promise
	]).then(function(responses) {
		$scope.status_list = responses[0];
		$scope.status_by_id = _.indexBy(responses[0], 'id');
		$scope.test_run = responses[1];
		$scope.test_plan = $scope.test_run.test_plan;
		$scope.active_test_definition = $scope.test_plan.tests_definitions[0];

		tests_results_by_id = _.indexBy(
			$scope.test_run.tests_definitions_results,
			'test_definition'
		);

		_.each($scope.test_run.test_plan.tests_definitions, function(test_definition) {
			test_definition.result = tests_results_by_id[test_definition.id];
		});
	})

	$scope.get_status = function(test_definition) {
		return $scope.status_by_id[test_definition.result.status];
	}

	$scope.set_status = function(status, test_definition) {
		if (status) {
			test_definition.result.status = status.id;
		} else {
			test_definition.result.status = null;
		}
		TestRunResult.update({id: test_definition.result.id}, test_definition.result);
	}

	$scope.load_test_definition = function(test_definition) {
		$scope.active_test_definition = test_definition;
	}

	$scope.add_bug = function(Bug) {
		debugger
		// $scope.active_test_definition = test_definition;
	}

}

function New($scope, $q, $routeParams, $location, TestBuild, TestPlan, TestRun) {

	$q.all([
		TestBuild.get({id: $routeParams.build_id }).$promise,
		TestPlan.query().$promise
	]).then(function(data) {
		$scope.build = data[0];
		$scope.test_plan_list = data[1];
	});

	$scope.submit = function() {
		TestRun.save({
			test_plan: $scope.test_plan,
			build: $scope.build.id
		}, function(data) {
			$location.path('/testrun/' + data.id);
		}, function(response) {
			$scope.error = response.data
		})

	}
}
