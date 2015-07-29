(function () {
  "use strict";
  function StationAdminCtrl($meteor) {
    var self = this;
    self.newStation = {};
    self.stations = $meteor.collection(Station);
    self.add = function () {
      if (!self.newStation.name) {
        return;
      }
      var station = {name: self.newStation.name, hostname: self.newStation.hostname};

      self.stations.push(station);
      self.newStation = {};
    };
    self.remove = function (station) {
      self.stations.splice(self.fixtures.indexOf(station), 1);
    };
  }

  angular.module('ate')
      .controller('StationAdminCtrl', ['$meteor', StationAdminCtrl]);
}());

