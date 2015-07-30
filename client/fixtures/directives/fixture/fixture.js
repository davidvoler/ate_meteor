/**
 * Created by davidl on 7/30/15.
 */
/**
 * Created by davidl on 7/30/15.
 * Cavity directive
 */
(function () {
  "use strict";
  function ateFixture() {
    return {
      restrict: 'E',
      templateUrl: 'client/fixtures/directives/fixture/fixture.ng.html',
      scope:{},
      link: function (scope, element, attr) {
      }
    }
  }

  angular.module('ate')
      .directive('ateFixture', [ateFixture]);

}());