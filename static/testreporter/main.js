APP.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/static/testreporter/templates/index.html',
            controller: 'Index'
        })
        .when('/new', {
            templateUrl: '/static/testreporter/templates/tag_form.html',
            controller: 'New'
        })
        .when('/:id', {
            templateUrl: '/static/testreporter/templates/report_private.html',
            controller: 'Report'
        });
  }]);


function Index($scope, $window, $routeParams, Tag){ 
    $scope.tags_progress = true;
    $scope.tags = Tag.query(function(){
       $scope.tags_progress = false; 
    });
    //$scope.tags_progress = false;

    $scope.remove = function(tag) {
        Tag.remove({id:tag.id}, function() {
            $scope.tags = Tag.query();
        });
    };
}

function Report($scope, $window, $routeParams, $http, $sce, Tag) {
    $scope.tag_progress = true;
    $scope.data_progress = true;
    $scope.bugs_progress = true;
    $scope.tag = Tag.get({id:$routeParams.id}, function() {
        $scope.description_markup = $sce.trustAsHtml($scope.tag.description_markup);
        $scope.tag_progress = false;
    })

    $scope.testRunUrl = function(testrun_id) {
        $window.location.pathname = "/testmanualrunner/#/testrun/" + testrun_id + "/";
    }

    $http.get('/testreporter/report/'+ $routeParams.id +'/').success(function(data) {
        $scope.data = data;
        $scope.data_progress = false;
    });

    $http.get('/testreporter/report/'+ $routeParams.id +'/bugs/').success(function(data) {
        $scope.bugs = data.bugs;
        $scope.bugs_progress = false;
    });

    $scope.submit = function() {
        Tag.update(
            {id:$scope.tag.id},
            $scope.tag,
            function(success) {
            },
            function(error) {
                debugger
                $scope.error = error.data
            }
        )
    }

}

function New($scope, $window, $routeParams, $location, Tag) {
    $scope.tag = {};
    $scope.submit = function() {
        Tag.save(
            $scope.tag,
            function() {
                $location.path('/');
            },
            function(error) {
                $scope.error = error.data
            }
        )
    }
}
