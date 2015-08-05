(function () {
  "use strict";
  function ateInfoYield() {
    return {
      restrict: 'E',
      /*
      template: '<md-whiteframe style="width: 150px;min-height: 150px;" ' +
      'class="md-whiteframe-z1" layout layout-align="center center">' +
      '<span>I am yield directive</span>' +
      '</md-whiteframe>',
      */
      templateUrl:'client/ate_info_widget/yield/view.ng.html',
      link: function (scope, element, attr) {
      }
    }
  }

  angular.module('ate.info.widget')
      .directive('ateInfoYield', [ateInfoYield]);

}());
