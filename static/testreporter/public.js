APP.config(['$routeProvider', function($routeProvider) {
    $routeProvider
		.when('/:id', {
			templateUrl: '/static/testreporter/templates/report_public.html',
			controller: 'Report'
		});
  }]);

function Report($scope, $window, $routeParams, $http, Tag) {
	$scope.tag = Tag.get({id:$routeParams.id})
	$http.get('/testreporter/report/'+ $routeParams.id +'/').success(function(data) {
		$scope.data = data;
	});
}
