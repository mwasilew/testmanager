APP.controller('JenkinsBuild', ['$scope', 'Tag', 'Build', function($scope, Tag, Build) {

	$scope.tags = Tag.query();
	$scope.new_tag = function() {
		// debugger
	}

	$scope._tags = {};
	$scope.select_tag = function(tag) {
		Build.get({id:$scope.build_id}, function(build) {
			build.tag = tag;
			Build.update({id:$scope.build_id}, build)
		})
	}

}]);
