/**
 * Created by davidl on 7/30/15.
 * Cavity directive
 */
(function () {
  "use strict";
  function ateCavity() {
    return {
      restrict: 'E',
      templateUrl: 'client/fixtures/directives/cavity/cavity.ng.html',
      scope:{},
      link: function (scope, element, attr) {
        scope.active=true;
        scope.serial = '';
        scope.status = 'idle'
      }
    }
  }

  angular.module('ate')
      .directive('ateCavity', [ateCavity]);

}());