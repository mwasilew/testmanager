APP.config(['$routeProvider', function($routeProvider) {
    $routeProvider
		.when('/', {
			templateUrl: '/static/testreporter/templates/index.html',
			controller: 'Index'
		})
		.when('/:id', {
		templateUrl: '/static/testreporter/templates/report.html',
			controller: 'Report'
		});

  }]);


function Index($scope, $window, $routeParams, Tag) {
	$scope.tags = Tag.query();

	$scope.submit = function() {
		Tag.save($scope.tag, function() {
			$scope.tags = Tag.query();
			$scope.tag = {};
		})
	}
}

function Report($scope, $window, $routeParams, $http, Tag) {
	$http.get('/testreporter/report/'+ $routeParams.id +'/').success(function(data) {
		$scope.data = data;
	});
}
