ATE - Automatic Test Equipment Manager - Based on Meteor Technology
===================================================================


Overview
--------
I was asked to design a centralized system for managing hardware testing.
After some research we choose the following technologies:
*Mongodb
*Python/Tornado
*Celery
*Sockjs/ sockjs.tornado
*Angularjs

The system is currently in production. The system works heavily with web-socket.
Learning about Meteor framework I have decided to check how much easier it would be to implement
the same system on this framework.

Usage
-----
to start meteor:

cd viewer

meteor

To start celery 

cd launcher

run celery tasks (celery ...) 



