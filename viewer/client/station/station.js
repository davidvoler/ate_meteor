(function () {
  "use strict";
  function StationCtrl($meteor,$interval) {
    var self = this;
    self.info = {name:'current station'};
    self.countTests = 0;
    $meteor.subscribe('fixtures');
    self.fixtures = $meteor.collection(Fixture);
    self.runFixture = function (fixtureId){
      var fixture = self.fixtures.find({_id:fixtureId});
      self.countTests = 0;
      console.log(fixture);
      $interval(function(){
        self.countTests++;
        fixture.cavities[0].status = "test_"+self.countTests;
      } , 2, 10);
    }


  }
  angular.module('ate')
      .controller('StationCtrl', ['$meteor', StationCtrl]);
}());
