// "use strict";
var bankapp1 = angular.module("bmyapp1", ['ui.bootstrap','ngCookies','ui.router'], function ($interpolateProvider,$locationProvider) {
         $interpolateProvider.startSymbol("{[");
         $interpolateProvider.endSymbol("]}");
            // $httpProvider.interceptors.push('myHttpRequestInterceptor'); 
                }
).run([
    '$http', 
    '$cookies', 
    function($http, $cookies) {
        // $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.xsrfCookieName = 'csrftoken';
        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        // $http.defaults.headers.post['Content-Type'] = 'application/JSON';

    }]);
bankapp1.config(function ($stateProvider,$urlRouterProvider,$locationProvider) {
   //  $locationProvider.html5Mode({
   //     enabled: true,
   //     requireBase: false
   // });
          $stateProvider.state('dashboard',{
             url:'/dashboard/',
            templateUrl: '/static/js/dashboard_user.html',
           abstract: true,
           controller:'bankDetailsController',

           })
        .state('newUser',{

            url:"/newUser",
            templateUrl: '/static/js/tenant_new.html',
            controller: ''
        })
        .state('service',{
           url:"/service",
        templateUrl:' /static/js/bankServices.html',
        controller:'bankDetailsController'})
        .state('addUser',{
           url:"/addUser",
            templateUrl:' /static/js/bankemployees_add.html',
            controller:'bankDetailsController'})
        .state('counters',{
            url:"/counter",
            templateUrl:'/static/js/add_counters.html',
            controller:''});

    
     

      $urlRouterProvider.otherwise("");
      
});

bankapp1.factory('countries', function($http,$q,$state){
        var fact={};
          fact.request_get = function(url){
            var dede =$q.defer();
            var promise = $http.get(url).success(function(data,status){
              return dede.resolve(data)
            }).error(function(msg){
              console.error('Unable to fetch item. Reason: ' + msg);
            }); 
          return dede.promise
        }
        fact.request_post = function(url,data){
          var deffered = $q.defer();
          var nurl= url 
          var promise = $http.post(url,data).success(function(data,status){
              console.log(data);
              return deffered.resolve(data)
              }).error(function(msg){
              console.error('Unable to fetch item. Reason: ' + msg);
            }); 
          return deffered.promise  
        }
      
      return fact;
});
// bankapp1.controller('bankDetailsController',['Bankutils',function($scope,$rootscope,Bankutils){
//   // $rootscope.tenant={}
//   $scope.services={};
//   // console.log('hekllojuh')
//   // $scope.as=Bankutils.getServices();

// }]);

bankapp1.service('Bankutils',function(countries) {
    var x ={}
    x.getServices = function(tenant,branch) {
      console.log('hello')
      return countries.request_get('http://172.27.30.119:8000/appoint/api/services/'+tenant+'/'+branch+'/')
      // .then(function(data,status){
      // console.log(data)
      // var data1 = data;     
      }
      // return services;
    x.getStaff = function(tenant,branch) {
      console.log('hello')
      return countries.request_get('http://172.27.30.119:8000/appoint/api/staff/'+tenant+'/'+branch+'/')
      // .then(function(data,status){
      // console.log(data)
      // var data1 = data;     
      }
    
    // getUsers  : function(){
    //   console.log('in getUsers')
    //   return null;
    // }

    x.getCounters = function(tenant,branch){
      return countries.request_get('http://172.27.30.119:8000/appoint/api/counters/'+tenant+'/'+branch+'/')
    }

    x.newCounter = function(tenant,branch,data){
      return countries.request_post('http://172.27.30.119:8000/appoint/api/counter/'+tenant+'/'+branch+'/new/',data)
    }

    return x;
  
});


bankapp1.controller('bankDetailsController',function($scope,Bankutils){
  // $rootscope.tenant=null
  // $rootscope.tenant=null
  $scope.tenant={'org_name':'SBH','branch_name':'AsifNagar'}
  $scope.services=null
  $scope.services1=Bankutils.getServices($scope.tenant.org_name,$scope.tenant.branch_name).then(function(data,status){
    $scope.data1=data;
    $scope.services=data.services
  
    return $scope.data1
  });
  Bankutils.getStaff($scope.tenant.org_name,$scope.tenant.branch_name).then(function(data,status){
    $scope.staff1=data.staff
    // return $scope.staff1
  });
  console.log($scope.services)
  $scope.bankStaff=function(tenant,branch){
    Bankutils.getStaff(tenant,branch).then(function(data,status){
    $scope.staff1=data.staff
    return $scope.staff1
    });

    Bankutils.getStaff($scope.tenant.org_name,$scope.tenant.branch_name).then(function(data,status){
      $scope.staff=data.staff
    });
  }


  $scope.addUser=function(){
    // Bankutils.createStaff($scope.tenant.org_name,$scope.tenant.branch_name,{}).then(function(data,status){
    //   $scope.services=data.staffusers
    // });
    $scope.staff1=$scope.bankstaff()
  }
  $scope.addcounter={"counter_name":"","service":"","staff_name":""}

  $scope.addCounter1=function(){
    $scope.addcounter.counter_name=$scope.counter_name
    $scope.addcounter.service=$scope.selectedService
    $scope.addcounter.staff_name=$scope.selectedStaff.username
    console.log($scope.addcounter)
    alert("addcounter1")
    Bankutils.newCounter($scope.tenant.org_name,$scope.tenant.branch_name,$scope.addcounter).then(function(data,status){
      alert(data.message)

    });

  }

});