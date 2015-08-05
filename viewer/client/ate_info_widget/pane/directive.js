(function () {
  "use strict";
  function atePane($meteor) {
    return {
      restrict: 'E',
      templateUrl: 'client/ate_info_widget/pane/view.ng.html',
      link: function (scope, element, attr) {
        scope.run_statuss = $meteor.collection(RunStatus);
      }
    }
  }

  angular.module('ate.info.widget')
      .directive('atePane', ['$meteor', atePane]);

}());
