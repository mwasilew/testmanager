APP.config(['$routeProvider', function($routeProvider) {
    $routeProvider
		.when('/:id', {
			templateUrl: '/static/testreporter/templates/report_public.html',
			controller: 'Report'
		});
  }]);

function Report($scope, $window, $routeParams, $http, $sce, $location, Tag) {
    $scope.tag_progress = true;
    $scope.data_progress = true;
    $scope.bugs_progress = false;
	$scope.tag = Tag.get({id:$routeParams.id}, function() {
        $scope.tag_progress = false;
		$scope.description_markup = $sce.trustAsHtml($scope.tag.description_markup);
	})
	$http.get('/testreporter/report/'+ $routeParams.id +'/').success(function(data) {
		$scope.data = data;
        $scope.data_progress = false;
	});
    $http.get('/testreporter/report/'+ $routeParams.id +'/bugs/').success(function(data) {
		$scope.bugs = data.bugs;
        $scope.bugs_progress = false;
	});
	$scope.testRunUrl = function(testrun_id) {
        $window.location.pathname = "/testmanualrunner/#/testrun/" + testrun_id + "/";
    }

}
