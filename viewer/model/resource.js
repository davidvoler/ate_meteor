Resource = new Mongo.Collection("resource");

var resource_doc = {
  name:'',
  parent:'',//This resources may be owned by a parent resource.
  type:'',
  exclusive:true, //Only one process/thread can access this
  states:[]// list of states of the resource like on/off
};