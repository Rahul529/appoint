// "use strict";
var userApp = angular.module("userApp", ['ui.bootstrap','ngCookies','ui.router'], function ($interpolateProvider,$locationProvider) {
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
userApp.config(function ($stateProvider,$urlRouterProvider,$locationProvider) {
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
        .state('newRequest',{

            url:"/newrequest",
            templateUrl: '/static/js/newUserRequest.html',
            controller: 'tenantlistController'
        }).state('home',{
          url:"/home",
          templateUrl:'/static/js/userHome.html',
          // controller:''
        })
        // .state('newRequest',{

        //     url:"/newrequest",
        //     templateUrl: '/static/js/newUserRequest.html',
        //     controller: 'tenantlistController'
        // })
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

userApp.factory('countries', function($http,$q,$state){
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

userApp.service('Bankutils',function(countries) {
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
    x.bookSlot = function(tenant,branch,service,username,email){
      data={"email":email,
        "full_name":username,
        "bank_name":tenant,
        "branch_name":branch,
        "service_name":service,
        "processed":"NO"
      };
      console.log(data)
      return countries.request_post('http://172.27.30.119:8000/appoint/api/services/book/',data)
    }
    x.getRequests=function(username){
      return countries.request_get('http://172.27.30.119:8000/appoint/api/user/'+username+'/requests/')
    }

    x.getRequestId=function(username,request_id){
      return countries.request_get('http://172.27.30.119:8000/appoint/api/user/'+username+'/request/'+request_id)
          
      }
    
    return x;
  
});


userApp.controller("tenantlistController",function($scope,$http,countries,Bankutils,$filter,$timeout){
$scope.username=document.getElementById("username").innerHTML
$scope.userEmail=document.getElementById("userEmail").innerHTML
$scope.tenants=null;
$scope.services_list=null;
countries.request_get('http://172.27.30.119:8000/appoint/api/tenants/').then(function(data,status){
    $scope.tenants=data.tenants;
})
$scope.branches=null;
$scope.selectedTenant=null;
$scope.searchbranchs=function(org_name){
  $scope.selectedTenant=org_name
  alert(org_name)
  countries.request_get("http://172.27.30.119:8000/appoint/api/branch/"+org_name).then(function(data,status){
      $scope.branches=data.branches;
      alert($scope.branches)
      console.log($scope.branches)

  });

}
$scope.requests=null
$scope.searchServices=function(branch_name){
  $scope.selectedTenantbranch=branch_name;
  countries.request_get("http://172.27.30.119:8000/appoint/api/services/"+$scope.selectedTenant+"/"+$scope.selectedTenantbranch)
    .then(function(data,status){
      $scope.services_list=data.services;
      console.log($scope.services_list)
    });
}
$scope.bookSlot=function(selected_Service){
  Bankutils.bookSlot($scope.selectedTenant,$scope.selectedTenantbranch,$scope.selectedService,$scope.username,$scope.userEmail).then(function(data,status){
    console.log(data)
    alert(data.message)
  });


}
$scope.requests=Bankutils.getRequests($scope.username).then(function(data,status){
    // $scope.request=data.user_requests
    $scope.requests=data.user_requests

    console.log($scope.requests[0])
    // return $scope.requests
  });
// $scope.requests.then(function(data,status){console.log(data)})
// console.log($scope.requests[0])
// $scope.index=0
// console.log($scope.requests[$scope.index])
$scope.dada=""
var saa="1a832c2a-82d5-4197-b595-10386c4d30e8"
$scope.getRequestData=function(id){

Bankutils.getRequestId($scope.username,id).then(function(data,status){
  $scope.requestHome=data.request
  $scope.dada = data.request
  console.log($scope.requestHome)

$scope.presentii =moment().format(' HH:mm:ss a');
$scope.startTime=moment($scope.presentii, "HH:mm:ss a");
// $scope.counter=$scope.seconds1;
$scope.endtime=$scope.requestHome.timep

$scope.endTime=moment($scope.endtime, "HH:mm:ss a");
// alert($scope.startTime)
// alert(document.getElementById("Endtime").innerHTML)
$scope.duration = moment.duration($scope.endTime.diff($scope.startTime));
// alert($scope.duration)
$scope.hours = parseInt($scope.duration.asHours());
$scope.minutes = parseInt($scope.duration.asMinutes())-$scope.hours*60;
$scope.seconds = parseInt($scope.duration.asSeconds())-$scope.hours*60*60-$scope.minutes*60;

  $scope.counter = parseInt($scope.duration.asSeconds());
   $scope.onTimeout = function(){
        if($scope.counter==0){
          $scope.stopCounter();
        }
        else{
        $scope.counter--;
         
         mytimeout = $timeout($scope.onTimeout,1000);
       }
    }
    var mytimeout = $timeout($scope.onTimeout,1000);

    $scope.stopCounter=function(){
      $timeout.cancel(mytimeout);
    }
});


}

Bankutils.getRequestId($scope.username,saa).then(function(data,status){
  $scope.requestHome=data.request
  $scope.dada = data.request
  console.log($scope.requestHome)

$scope.presentii =moment().format(' HH:mm:ss a');
$scope.startTime=moment($scope.presentii, "HH:mm:ss a");
// $scope.counter=$scope.seconds1;
$scope.endtime=$scope.requestHome.timep

$scope.endTime=moment($scope.endtime, "HH:mm:ss a");
// alert($scope.startTime)
// alert(document.getElementById("Endtime").innerHTML)
$scope.duration = moment.duration($scope.endTime.diff($scope.startTime));
// alert($scope.duration)
$scope.hours = parseInt($scope.duration.asHours());
$scope.minutes = parseInt($scope.duration.asMinutes())-$scope.hours*60;
$scope.seconds = parseInt($scope.duration.asSeconds())-$scope.hours*60*60-$scope.minutes*60;

  $scope.counter = parseInt($scope.duration.asSeconds());
   $scope.onTimeout = function(){
        if($scope.counter==0){
          $scope.stopCounter();
        }
        else{
        $scope.counter--;
         
         mytimeout = $timeout($scope.onTimeout,1000);
       }
    }
    var mytimeout = $timeout($scope.onTimeout,1000);

    $scope.stopCounter=function(){
      $timeout.cancel(mytimeout);
    }
});
// console.log($scope.dada)


    // $scope.presentii =moment().format(' h:mm:ss a');
      // $scope.present = new Date('HH:mm:ss');

});

userApp.filter('formatTimer', function() {
  return function(input)
    {
        function z(n) {return (n<10? '0' : '') + n;}
        
        // var seconds = input % 60;
        // var minutes = Math.floor(input / 60);
        var hours = Math.floor(input / 3600);
        var minutes=Math.floor((input - (hours * 3600)) / 60);
        var seconds = input - (hours * 3600) - (minutes * 60);

        return (z(hours) +':'+z(minutes)+':'+z(seconds));
    };
});