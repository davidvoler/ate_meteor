Meteor.startup(function () {


  if (Fixture.find().count() === 0) {

    var fixtures = [
      {
        'name': 'Fixture 1',
        'cavities': [1, 2, 3, 4]
      },
      {
        'name': 'Fixture 2',
        'cavities': [1, 2, 3, 4]
      },
      {
        'name': 'Fixture 3',
        'cavities': [1, 2, 3, 4]
      }
    ];

    for (var i = 0; i < fixtures.length; i++)
      Fixture.insert(fixtures[i]);

  }
  if (RunStatus.find().count() === 0) {

    var statuses = [
      {
        'info': 'Yield is .....',
        'type':'Yield',
        'status':'ok'
      },
      {
        'info': 'Performanse is ',
        'type':'Performanse',
        'status':'ok'
      },
      {
        'info': 'Methods are ',
        'type':'Methods',
        'status':'ok'
      }

    ];

    for (var i = 0; i < statuses.length; i++)
      RunStatus.insert(statuses[i]);
  }
  if (Station.find().count() <20) {

    var stations = [];
    for (var i = 0; i<20; i++){
       Station.insert({name:'name'+i,hostname:'1.1.2.'+i});
    }

  }

});

