/**
 * Created by davidl on 7/30/15.
 */
/**
 * Created by davidl on 7/30/15.
 * Fixture directive
 *
 */
(function () {
  "use strict";
  function ateFixture($meteor, $interval) {
    return {
      restrict: 'E',
      templateUrl: 'client/fixtures/directives/fixture/fixture.ng.html',
      scope: {key: '='},
      link: function (scope, element, attr) {
        scope.fixture = $meteor.object(Fixture, scope.key, false);
        scope.countTests = 0;
        scope.runFixture = function () {
          scope.countTests = 0;
          $interval(function () {
            scope.countTests++;
            scope.fixture.cavities[0].status = "test_" + scope.countTests;
            scope.fixture.cavities[1].status = "test_" + scope.countTests;
            scope.fixture.cavities[2].status = "test_" + scope.countTests;
            scope.fixture.cavities[3].status = "test_" + scope.countTests;
          }, 1000, 10);
        };

        scope.runFixture = function () {
          $meteor.call('runServerFixture', scope.key).then(function(res){
            console.log(res);
          });
        };
        scope.stopFixture = function(){
          $meteor.call('stopServerFixture', scope.key).then(function(res){
            console.log(res);
          });
        };
        scope.clear = function(){
          for (var i in scope.fixture.cavities){
            scope.fixture.cavities[i].serial = '';
          }
          scope.fixture.save();
        }
      }
    }
  }

  angular.module('ate')
      .directive('ateFixture', ['$meteor', '$interval', ateFixture]);

}());