/*
UUT - Unit Under Test
 */
Uut = new Mongo.Collection("uut");

var uut_doc = {
  product:'',
  serial:'',//unit serial number
  status:'',//This resources may be owned by a parent resource.
  tests:[]//a list of tests and results
};