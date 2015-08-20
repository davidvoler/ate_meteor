var Future = Npm.require('fibers/future');

Meteor.publish("fixtures", function () {
  return Fixture.find();
});


Meteor.methods({
  runServerFixture1: function (fixtureId) {
    //console.log(fixtureId);
    //var fixtureCollection = new Mongo.Collection('fixture');
    fixture = Fixture.findOne({_id: fixtureId});

    //console.log(fixture);
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
        Fixture.update({_id: fixtureId}, fixture);
        countTests++;
      }

    }, 1000);
    return true;

  },
  runServerFixture: function (fixtureId) {


    var uuts = [{'serial': '11101', 'id': 0},
      {'serial': '11102', 'id': 1},
      {'serial': '11103', 'id': 2},
      {'serial': '11104', 'id': 3}];
    var sequence = [
      {
        'name': '',
        'unique_lock': null,
        'wait_lock': null, 'progress': 10
      },
      {
        'name': 'test1',
        'unique_lock': null,
        'wait_lock': null, 'progress': 10
      },
      {
        'name': 'test2',
        'unique_lock': null,
        'wait_lock': null, 'progress': 20
      },
      {
        'name': 'test3',
        'unique_lock': null,
        'wait_lock': null, 'progress': 30
      },
      {
        'name': 'test4',
        'unique_lock': null,
        'wait_lock': null, 'progress': 40
      },
      {
        'name': 'test5',
        'unique_lock': null,
        'wait_lock': null, 'progress': 50
      },
      {
        'name': 'test_on_switch',
        'unique_lock': null,
        'wait_lock': 'on_switch', 'progress': 60
      },
      {
        'name': 'test6_ps',
        'unique_lock': 'ps',
        'wait_lock': null, 'progress': 65
      },
      {
        'name': 'test7',
        'unique_lock': null,
        'wait_lock': null, 'progress': 70
      },
      {
        'name': 'test8',
        'unique_lock': null,
        'wait_lock': null, 'progress': 80
      },
      {
        'name': 'test9',
        'unique_lock': null,
        'wait_lock': null, 'progress': 85
      },
      {
        'name': 'test10',
        'unique_lock': null,
        'wait_lock': null, 'progress': 90
      },
      {
        'name': 'test11',
        'unique_lock': null,
        'wait_lock': null, 'progress': 95
      },
      {
        'name': 'cleanup',
        'unique_lock': null,
        'wait_lock': null, 'progress': 100
      }

    ];

    this.unblock();
    var task = Celery.createTask('tasks.run_sequence');
    //console.log(task);

    try {
      for (i in uuts){
        task.invoke([fixtureId, 12, uuts[i], sequence]);
      }
      //return task.invokeSync([fixtureId, 12, uuts[0], sequence]).wait().result;
    } catch (e) {
      console.error(e.stack);
    }

    return true;
  },


  setCavityStatus: function (fixtureId, cavityId, status, progress) {
    fixture = Fixture.findOne({_id: fixtureId});
    console.log("" + fixtureId + "|" + cavityId + '|' + status + '|' + progress);
    //cid = parseInt(cavityId);
    fixture.cavities[cavityId].status = status;
    fixture.cavities[cavityId].progress = progress;
    var fixture_progress = 0;
    for (var i in fixture.cavities) {
      if (fixture.cavities[i].status == 'fail') {
        fixture_progress = fixture_progress + 100;
      }
      else if (fixture.cavities[i].progress) {
        fixture_progress = fixture_progress + fixture.cavities[i].progress;
      }
    }
    fixture.progress = fixture_progress / fixture.cavities.length;
    if (fixture.progress >= 100){
      fixture.inUse = false;
    }else{
      fixture.inUse = true;

      fixture.inUseDate = new Date();

    }
    Fixture.update({_id: fixtureId}, fixture);
    return true;

  },

  acquireFixture: function (fixtureId) {
    fixture = Fixture.findOne({_id: fixtureId});
    if (fixture.inUse){
      return false;
    }else{
      fixture.inUse = true;
      Fixture.update({_id: fixtureId}, fixture);
      return true;
    }
  }


});