APP.config(['$routeProvider', function($routeProvider) {

	$routeProvider
		.when('/', {
			templateUrl: '/static/testplanner/templates/index.html',
			controller: 'Index'
		})
		.when('/new', {
			templateUrl: '/static/testplanner/templates/testplan_form.html',
			controller: 'New'
		})
		.when('/:testPlanId', {
			templateUrl: '/static/testplanner/templates/testplan_form.html',
			controller: 'Edit'
		})

  }]);

function Index($scope, $window, $routeParams, TestPlan) {
	$scope.plans = TestPlan.query();

	$scope.remove = function(plan) {
		TestPlan.remove({id:plan.id}, function() {
			$scope.plans = TestPlan.query();
		});
	};

}

function Edit($scope, $location, $window, $routeParams, $q, TestPlan, Device, Definitions) {
	$scope.availableDevices = Device.query();
	$scope.testPlan = TestPlan.get({id:$routeParams.testPlanId}, function(testPlan) {
		$scope.device = Device.get({id:testPlan.device}, function() {
			$scope.testDefinitions = Definitions.query({deviceName:$scope.device.id}, function(tests_definitions) {
				_.each($scope.testPlan.tests_definitions, function(element) {
					_.find(tests_definitions, { 'id': element.id }).active = true;
				})
			});
		});
	});

	$scope.deviceSelected = function() {
		$scope.testDefinitions = Definitions.query({deviceName:$scope.device.id});
	}

	$scope.selectDefinition = function(testDefinition) {
		testDefinition.active = !testDefinition.active;
	}

	$scope.submit = function() {
		$scope.testPlan.device = $scope.device.id;
		$scope.testPlan.tests_definitions = [];

		angular.forEach($scope.testDefinitions, function(value, key) {
			if (value.active) {
				this.push(value.id);
			}
		}, $scope.testPlan.tests_definitions);

		$scope.testPlan.$update({id:$scope.testPlan.id}).then(function() {
			$location.path('/');
		}, function(error) {
			$scope.error = error.data
		})
	}

}

function New($scope, $window, $routeParams, $location, Device, TestPlan, Definitions) {
	$scope.availableDevices = Device.query();

	$scope.testPlan = {
		tests_definitions:[],
	};

	$scope.device = {};

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

	$scope.selectDefinition = function(testDefinition) {
		testDefinition.active = !testDefinition.active;
	}
}
