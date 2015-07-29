angular.module('ate').controller('StationCtrl', ['$scope','$meteor',
      function($scope, $meteor){
        $scope.newFixture = {};
        $scope.fixtures = $meteor.collection(Fixture);
        $scope.addFixture = function(){
          if (!$scope.newFixture.name){
            return;
          }
          var fixture = {name:$scope.newFixture.name,cavities:[]};
          var numCavities = parseInt($scope.newFixture.noCavities);
          for (i=0; i<numCavities ;i++){
            fixture.cavities.push(i+1);
          }
          $scope.fixtures.push(fixture);
          $scope.newFixture = {};
        };
        $scope.remove = function(fixture){
          $scope.fixtures.splice( $scope.fixtures.indexOf(fixture), 1 );
        };

    }]);

