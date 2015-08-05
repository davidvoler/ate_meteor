(function () {

    function HomeController() {
        var self = this;
        self.msg = 'Home controller';
        console.log('HomeController');
    }

    angular.module('ate.launcher')
        .controller('HomeController', [HomeController]);
}());
