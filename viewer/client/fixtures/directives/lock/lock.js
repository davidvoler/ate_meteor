/**
 * Created by davidl on 7/30/15.
 * Cavity directive
 */
(function () {
  "use strict";
  function ateLock() {
    return {
      restrict: 'E',
      templateUrl: 'client/fixtures/directives/lock/lock.ng.html',
      scope: {lock: '='},
      link: function (scope, element, attr) {
        
      }
    }
  }

  angular.module('ate')
      .directive('ateLock', [ateLock]);

}());