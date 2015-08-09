Location = new Mongo.Collection("location");

var location_doc = {
  address:'',
  floor:0,
  map:'', //a visual map of production floor
  positions:[]//a list of {x,y} position where fixture could be placed
};