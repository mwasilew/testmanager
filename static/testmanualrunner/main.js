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

function Execute($scope, $window, $routeParams, $q,
				 TestRun, TestPlan, Status, TestRunResult, TestRunResultBug, Build, Trackers) {
	$q.all([
		Status.query().$promise,
		TestRun.get({id:$routeParams.id}).$promise,
		Trackers.query().$promise
	]).then(function(responses) {
		$scope.statuses = responses[0];
		$scope.test_run = responses[1];
		$scope.trackers = responses[2];

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

	$scope.add_bug = function(alias, tracker, test_definition) {
		var test_run_result = $scope.test_run_results_by_test_definition[test_definition.id];
		TestRunResultBug.add(
			{id:test_run_result.id},
			{alias:alias, tracker:tracker, action:"add"}).$promise
			.then(function(bug) {
				missing = true;
				_.each(test_run_result.bugs, function(value, i) {
					if (value.id == bug.id) {
						missing = false
					}
				});
				if (missing) {
					test_run_result.bugs.unshift(bug);
				}
			});
	}

	$scope.remove_bug = function(bug, test_definition) {
		var test_run_result = $scope.test_run_results_by_test_definition[test_definition.id];
		TestRunResultBug.remove(
			{id:test_run_result.id},
			{alias:bug.alias, tracker:bug.tracker, action:"remove"}).$promise
			.then(function(bug) {
				var index = null;
				_.each(test_run_result.bugs, function(value, i) {
					if (value.id == bug.id) {
						index = i;
					}
				});
				if (index) {
					test_run_result.bugs.splice(index, 1);
				}
			});
	}

	$scope.get_test_run_results = function(test_definition) {
		return $scope.test_run_results_by_test_definition[test_definition.id];
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
