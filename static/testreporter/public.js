APP.config(['$routeProvider', function($routeProvider) {
    $routeProvider
		.when('/:id', {
			templateUrl: '/static/testreporter/templates/report_public.html',
			controller: 'Report'
		});
  }]);

function Report($scope, $window, $routeParams, $http, $sce, $location, Tag) {
	$scope.tag = Tag.get({id:$routeParams.id}, function() {
		$scope.description_markup = $sce.trustAsHtml($scope.tag.description_markup);
	})
	$http.get('/testreporter/report/'+ $routeParams.id +'/').success(function(data) {
		$scope.data = data;
	});
	$scope.testRunUrl = function(testrun_id) {
        $window.location.pathname = "/testmanualrunner/#/testrun/" + testrun_id + "/";
    }

}
