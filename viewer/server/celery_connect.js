/*
Meteor.startup(function(){
  // Creates a new client 'meteor`
  this.celery_client = new CeleryClient('meteor');
  this.celery_client.connect({
    "BROKER_URL": "amqp://ate:crow2012@192.168.1.124:5672//",
    "RESULT_BACKEND": "amqp",
    "SEND_TASK_SENT_EVENT": true
  });
  console.log('creating celery client');

});
*/