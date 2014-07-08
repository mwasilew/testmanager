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

function Execute($scope, $window, $routeParams, $q, TestRun, TestPlan, Status, TestRunResult, Bug, Build) {
	$q.all([
		Status.query().$promise,
		TestRun.get({id:$routeParams.id}).$promise
	]).then(function(responses) {
		$scope.statuses = responses[0];
		$scope.test_run = responses[1];

		$scope.statuses_by_id = _.indexBy(responses[0], 'id');

		return $q.all([
			TestPlan.get({id:$scope.test_run.test_plan}).$promise,
			Build.get({id:$scope.test_run.test_plan}),
			TestRunResult.query({test_run:$scope.test_run.id}).$promise,
		]);

	}).then(function(responses) {
		$scope.test_plan = responses[0];
		$scope.build = responses[1];
		$scope.test_run_results = responses[2];

		$scope.test_run_results_by_test_definition = _.indexBy(
			$scope.test_run_results,
			'test_definition'
		);

		$scope.active_test_definition = $scope.test_plan.tests_definitions[0];
	})

	$scope.get_status = function(test_definition) {
		var status = $scope.test_run_results_by_test_definition[test_definition.id].status;
		if (status) {
			return $scope.statuses_by_id[status]
		}
		return {}
	}

	$scope.set_status = function(status, test_definition) {
		var test_run_result = $scope.test_run_results_by_test_definition[test_definition.id];
		if (status) {
			test_run_result.status = status.id;
		} else {
			test_run_result.status = null;
		}
		TestRunResult.update({id: test_run_result.id}, test_run_result);
	}

	$scope.set_active_test_definition = function(test_definition) {
		$scope.active_test_definition = test_definition;
	}

	// $scope.add_bug = function(Bug) {
	// 	debugger
	// 	// $scope.active_test_definition = test_definition;
	// }

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