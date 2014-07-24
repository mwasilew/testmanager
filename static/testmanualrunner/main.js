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
				 TestRun, Status, TestRunResult, TestRunResultBug,
				 Build, DefinitionYaml, Trackers) {

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
			Build.get({id:$scope.test_run.build}),
			TestRunResult.query({test_run:$scope.test_run.id}).$promise,
		]);

	}).then(function(responses) {
		$scope.build = responses[0];
		$scope.test_run_results = responses[1];

		$scope.test_run_results_by_test_definition = _.indexBy(
			$scope.test_run_results,
			'test_definition'
		);

		if ($scope.test_run_results.length) {
			$scope.set_active_test_result($scope.test_run_results[0]);
		}
	})

	$scope.get_status = function(test_result) {
		if (test_result.status) {
			return $scope.statuses_by_id[test_result.status]
		}
		return {}
	}

	$scope.set_status = function(status, test_result) {
		if (status) {
			test_result.status = status.id;
		} else {
			test_result.status = null;
		}
		TestRunResult.update({id: test_result.id}, test_result);
	}

	$scope.set_active_test_result = function(test_result) {
		$scope.active_test_result = test_result;
		DefinitionYaml.get({id:test_result.test_definition.id}, function(data) {
			//$scope.yaml = jsyaml.load(data.yaml)
			$scope.yaml = data.yaml
		});
	}

	$scope.add_bug = function(alias, tracker, test_result) {
		TestRunResultBug.add(
			{id:test_result.id},
			{alias:alias, tracker:tracker, action:"add"}).$promise
			.then(function(bug) {
				missing = true;
				_.each(test_result.bugs, function(value, i) {
					if (value.id == bug.id) {
						missing = false
					}
				});
				if (missing) {
					test_result.bugs.unshift(bug);
				}
			});
	}

	$scope.remove_bug = function(bug, test_result) {
		TestRunResultBug.remove(
			{id:test_result.id},
			{alias:bug.alias, tracker:bug.tracker, action:"remove"}).$promise
			.then(function(bug) {
				var index = -1;
				_.each(test_result.bugs, function(value, i) {
					if (value.id == bug.id) {
						index = i;
					}
				});
				if (index != -1) {
					test_result.bugs.splice(index, 1);
				}
			});
	}

	$scope.close = function(state) {
		$scope.test_run.closed = state;
		TestRun.update({id: $scope.test_run.id}, $scope.test_run);
	}

}

function New($scope, $q, $routeParams, $location, Build, TestPlan, TestRun) {

	$q.all([
		Build.get({id: $routeParams.build_id }).$promise,
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
