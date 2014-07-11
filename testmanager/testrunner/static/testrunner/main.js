APP.controller('JenkinsBuild', ['$scope', 'Tag', 'Build', function($scope, Tag, Build) {

	$scope.tags = Tag.query();
	$scope._tags = {};

	$scope.save_tags = function(tags, build_id) {
		Build.get({id:build_id}, function(build) {
			build.tags = _.map(tags, function(val, key) { return val ? key : null });
			Build.update({id:build_id}, build)
		})
	}
}]);


APP.controller('FetchLavaJob', ['$scope', 'FetchLavaJob', function($scope, FetchLavaJob) {

	$scope.fetch = function(build_id) {

		FetchLavaJob.get({
			build_id:build_id,
			lavajob_id: $scope.lavajob_id
		}, function(data) {
			$scope.lavajob_fetch_error = data.error;
			if (data.reload) {
				location.reload();
			}
		})

	}
}]);
