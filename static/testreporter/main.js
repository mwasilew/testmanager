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
}

function Report($scope, $window, $routeParams, $http, Tag) {
	$http.get('/testreporter/report/'+ $routeParams.id +'/').success(function(data) {
		$scope.data = data;
	});

	// $scope.tag = Tag.get({id:$routeParams.id}, function(tag) {
	// });
}
