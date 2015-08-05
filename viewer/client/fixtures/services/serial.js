/**
 * Serial number validation service
 * Created by davidl on 7/30/15.
 */
(function () {
  "use strict";
  function SerialService($http) {
    var service = {};
    service.validateSerial = function(serial){
      if(serial.length > 4) {
        return true;
      }
      return false;
    };
    return service;
  }

  angular.module('ate')
      .service('SerialService', ['$http',SerialService]);

}());