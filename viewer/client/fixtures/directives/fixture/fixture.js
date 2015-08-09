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
  function ateFixture($meteor) {
    return {
      restrict: 'E',
      templateUrl: 'client/fixtures/directives/fixture/fixture.ng.html',
      scope: {key: '='},
      link: function (scope, element, attr) {
        scope.fixture = $meteor.object(Fixture, scope.key);
      }
    }
  }

  angular.module('ate')
      .directive('ateFixture', ['$meteor', ateFixture]);

}());