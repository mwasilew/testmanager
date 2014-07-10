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
