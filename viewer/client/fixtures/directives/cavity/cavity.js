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
      scope: {info: '='},
      link: function (scope, element, attr) {
        
      }
    }
  }

  angular.module('ate')
      .directive('ateCavity', [ateCavity]);

}());