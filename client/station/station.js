(function () {
  "use strict";
  function StationCtrl($meteor) {
    var self = this;
    self.info = {name:'current station'};
  }
  angular.module('ate')
      .controller('StationCtrl', ['$meteor', StationCtrl]);
}());
