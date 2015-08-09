(function () {
  "use strict";
  function StationCtrl($meteor) {
    var self = this;
    self.info = {name:'current station'};
    self.fixtures = $meteor.collection(Fixture);
  }
  angular.module('ate')
      .controller('StationCtrl', ['$meteor', StationCtrl]);
}());
