Station = new Mongo.Collection("station");

var station_doc = {
  name:'',
  hostname:'',
  virtual:false,
  fixtures:[]
};