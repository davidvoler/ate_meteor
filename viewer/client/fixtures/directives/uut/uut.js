/**
 * Created by davidl on 7/30/15.
 */
(function () {
  "use strict";
  function myDirective(SerialService) {
    return {
      restrict: 'E',
      templateUrl: '',
      link: function (scope, element, attr) {
        scope.serial = '';
        console.log('uut in link');

      }
    }
  }

  angular.module('ate')
      .directive('myDirective', [myDirective]);

}());