APP.controller('JenkinsBuild', ['$scope', 'Tag', 'Build', function($scope, Tag, Build) {

	$scope.tags = Tag.query();
	$scope._tags = {};
	
	$scope.select_tag = function(tag, build_id) {
		Build.get({id:build_id}, function(build) {
			build.tags = tag;
			Build.update({id:build_id}, build)
		})
	}

}]);
