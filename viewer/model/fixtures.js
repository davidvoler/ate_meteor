Fixture = new Mongo.Collection("fixture");

var cavity_doc = {
  enabled: true,
  idx: 0,
  percentage: 0,
  uut:'',
  test:'',
  img:''
};


var fixture_doc = {
  name: '',
  configuration: '',
  cavities: [],
  resources: [],
  location: '',
  position: {x: 0, y: 0},
  station: ''
};