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
			if (data.reload == true) {
				location.reload();
			}
		})

	}
}]);


APP.controller('LavaJobBugsss', ['$scope', 'Trackers', 'LavaJob', 'LavaJobBug', function($scope, Trackers, LavaJob, LavaJobBug) {

	// Mechanism to pass data from Dajgno to Angular.js scope
	$scope.init = function(lavajob_number) {

		$scope.trackers = Trackers.query();
		$scope.lavajob = LavaJob.get({number: lavajob_number});

	};

	$scope.add_bug = function(alias, tracker) {
		number = $scope.lavajob.number;
		lavajob = $scope.lavajob;

		LavaJobBug.add(
			{number:number},
			{alias:alias, tracker:tracker, action:"add"},
			function(bug) {
				missing = true;
				_.each(lavajob.bugs, function(value, i) {
					if (value.id == bug.id) {
						missing = false
					}
				});
				if (missing) {
					lavajob.bugs.unshift(bug);
				}
			}
		);
	}

	$scope.remove_bug = function(bug) {
		number = $scope.lavajob.number;
		lavajob = $scope.lavajob;

		LavaJobBug.remove(
			{number:number},
			{alias:bug.alias, tracker:bug.tracker, action:"remove"})

		var index = -1;
		_.each($scope.lavajob.bugs, function(value, i) {
			if (value.id == bug.id) {
				index = i;
			}
		});
		if (index != -1) {
			$scope.lavajob.bugs.splice(index, 1);
		}
	}

}]);
