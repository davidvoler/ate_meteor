Meteor.publish("fixtures", function () {
  return Fixture.find();
});



Meteor.methods({
  runServerFixture: function (fixtureId) {
    console.log(fixtureId);
    //var fixtureCollection = new Mongo.Collection('fixture');
    fixture = Fixture.findOne({_id:fixtureId});

    console.log(fixture);
    var countTests = 0;

    var interval = Meteor.setInterval(function () {
      if (countTests > 10) {
        Meteor.clearInterval(interval);
        return true;
      } else {
        fixture.cavities[0].status = "test_" + countTests;
        fixture.cavities[1].status = "test_" + countTests;
        fixture.cavities[2].status = "test_" + countTests;
        fixture.cavities[3].status = "test_" + countTests;
        Fixture.update({_id:fixtureId},fixture);
        countTests++;
      }
    }, 1000);
    return true;
  }
});