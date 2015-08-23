(function () {

  function routes($routeProvider) {
    $routeProvider
        .when('/station', {
          templateUrl: 'client/station/station.ng.html',
          controller: 'StationCtrl',
          controllerAs: 'station'
        })
        .when('/admin/stations', {
          templateUrl: 'client/station/admin/station_admin.ng.html',
          controller: 'StationAdminCtrl',
          controllerAs: 'admin'
        })
        .when('/admin/fixtures', {
          templateUrl: 'client/fixtures/admin/fixture_admin.ng.html',
          controller: 'FixtureAdmin',
          controllerAs: 'admin'
        })
        .when('/admin/fixture/:fixtureId', {
          templateUrl: 'client/fixtures/admin/fixture_admin.ng.html',
          controller: 'FixtureAdmin',
          controllerAs: 'admin'
        })
        .otherwise({redirectTo: '/station'});
  }

  angular.module('ate')
      .config(['$routeProvider', routes]);
}());

