var URL = "/planner/view/";

angular.module('api', ['ngResource']).
	factory('Device', function($resource) {
		return $resource(URL + 'device/:id/', {}, {});
	}).
	factory('TestPlan', function($resource) {
		return $resource(URL + 'plan/:id/', {}, {});
	})


var app = angular.module('app', ['ngRoute', 'api'], function(
	$locationProvider,
	$routeProvider,
	$resourceProvider,
	$httpProvider) {

	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$resourceProvider.defaults.stripTrailingSlashes = false;

	$routeProvider
		.when('/', {
			templateUrl: '/static/templates/index.html',
			controller: 'Index'
		})
		.when('/new', {
			templateUrl: '/static/templates/new.html',
			controller: 'New'
		});
});

function Index($scope, $window, $routeParams, TestPlan) {
	$scope.plans = TestPlan.query();
}

function New($scope, $window, $routeParams, Device, TestPlan) {
	$scope.availableDevices = Device.query();

	$scope.submit = function() {
		var testPlan = new TestPlan();
		testPlan.name = $scope.testPlan.name;
		testPlan.description = $scope.testPlan.description;
		testPlan.device = $scope.testPlan.device.id;
		testPlan.$save();
	}
}


// $(document).ready(function(){

// 	$("#id_device").change(function(aaa){
// 		$deviceId = $(this).val();

// 		$.getJSON( "new/definitions/" + $deviceId, function( data ) {
// 			$('.list-group').html("");
// 			$.each( data, function( _, row ) {
// 				$('.list-group').append(
// 					'<a href="#" class="list-group-item">' + row.name +
// 					'<input class="pull-right" value="' + row.id + '"type="checkbox">' +
// 					'</a>'
// 				)
// 			});
// 		});
// 	});

// 	$(".list-group").on("click", "a", function(e) {
// 		e.stopPropagation();
// 		e.preventDefault();
// 		$(this)
// 			.toggleClass('active')
// 			.find('input').prop("checked", !$(this).find('input').is( ":checked" ));
// 	});

// });
