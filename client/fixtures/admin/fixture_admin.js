(function () {
  "use strict";
  function FixtureAdmin($meteor) {
    var self = this;
    self.newFixture = {};
    self.fixtures = $meteor.collection(Fixture);
    self.addFixture = function () {
      if (!self.newFixture.name) {
        return;
      }
      var fixture = {name: self.newFixture.name, cavities: []};
      var numCavities = parseInt(self.newFixture.noCavities);
      for (i = 0; i < numCavities; i++) {
        fixture.cavities.push(i + 1);
      }
      self.fixtures.push(fixture);
      self.newFixture = {};
    };
    self.remove = function (fixture) {
      self.fixtures.splice(self.fixtures.indexOf(fixture), 1);
    };
  }
  angular.module('ate')
      .controller('FixtureAdmin', ['$meteor', FixtureAdmin]);
}());
