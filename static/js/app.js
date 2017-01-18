

// 'use strict';
 
///////////////////////////////////////////////////////
// Confuguration and the Modules required are loaded //
//////////////////////////////////////////////////////


var app1 = angular.module("myapp1", ['ui.bootstrap','ngCookies','ui.router'], function ($interpolateProvider,$locationProvider) {
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
//  app1.config(function($locationProvider) {
//     $locationProvider.html5Mode({
//   		enabled: true,
//   		requireBase: false
// 	});
// });
app1.run(['$state', '$stateParams',
function($state, $stateParams) {
//this solves page refresh and getting back to state
}]);
// app1.run(['$state', '$stateParams',
// function($state, $stateParams) {
// //this solves page refresh and getting back to state
// }]);

///////////////////////////////////////////////////////
// Routes of the User interface or Front end         //
//////////////////////////////////////////////////////$routeProvider

app1.config(function ($stateProvider,$urlRouterProvider,$locationProvider) {
    $locationProvider.html5Mode({
       enabled: true,
       requireBase: false
   });
    // $urlRouterProvider.otherwise("/");
    //  var base = {
    //         name: 'home',
    //         url:'/appoint/',
    //         // controller: 'ntroller',
    //         templateUrl: '/static/pages/tenant_new.html',
    //        abstract: true,
    //         // pageTitle: ''
    //     },
    //     signup =
    //     	{
    //   		url:"singup",
    //     templateUrl: '/static/pages/tenant_new.html',
    //     controller: 'tenantNewController'
    //   },
    //   login={
    //   	url:"login",
    //   	templateurl:'/static/pages/login.html',
    //  	controller:'DatepickerDemoCtrl'
    //   }

        $stateProvider.state('appoint',{
        	 url:'/appoint',
            controller: '',
            templateUrl: '/static/js/base.html',
           abstract: true,

           })
        .state('signup',{

        	url:"/appoint/singup",
        	templateUrl: '/static/js/tenant_new.html',
        	controller: 'tenantNewController'
        })
        .state('login',{
     	   url:"/appoint/login",
      	templateUrl:' /static/js/login_html.html',
        controller:'DatepickerDemoCtrl'
    
     }).state('work',{
        url:"/appoint/work",
        templateUrl:'/static/js/proccess.html',
        controller:'tenantCounterController'
     })
     .state('home',{
        url:"/appoint/home",
        templateUrl:'/static/js/userRequest.html'
     })
     .state('user',{
        url:"/appoint/user",
        templateUrl:'/static/js/userDashboard.html'
     })
     .state('usersignup',{
        url:"/appoint/usersignup",
        templateUrl:'/static/js/usersignup.html'

     });

      $urlRouterProvider.otherwise("/appoint/");
      
});


//factory method for sending the request to api or endpoint 
// contains two one for the get and another for post gets and requests the JSON objects 
// for api can see the django urls


////////////////////////////////////////////////////////////////////////////
// Factory method to which send the request to endpoints or api  		 //
// supports : GET and POST 												//	
/////////////////////////////////////////////////////////////////////////
app1.factory('countries', function($http,$q,$state){
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


app1.controller("tenantlistController",function($scope,$http,countries){

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

$scope.searchServices=function(branch_name){
  $scope.selectedTenantbranch=branch_name;
  countries.request_get("http://172.27.30.119:8000/appoint/api/services/"+$scope.selectedTenant+"/"+$scope.selectedTenantbranch)
    .then(function(data,status){
      $scope.services_list=data.services;
      console.log($scope.services_list)
    });
}
$scope.bookslot=function(branch_name){

}

});



app1.controller("tenantController",function($scope,$http,$state,countries){
  $scope.firtname = "Rahul";
  $scope.lastname = "Kuntala";
  // $scope.tenants = '';
  $scope.newtenant = {
      tenant_name :"",
      email: "",
      org_name: "",
      branch_name: "",
      services_list:[]
  }
  $scope.user = {
  	username:"",
  	password:""
  }

  $scope.login = function() {
        alert($scope.user.username)
        countries.request_get().then(function(response){
        	$scope.tenants=response;
        	console.log(response)
        	console.log($scope.tenants)
    });
    	// $scope.tenants=countries.list(){
    	// 	$scope.tenants = response;
    	// 	console.log($scope.tenants)	

    	// });

    };

  

  });



//controller create sthe new tenant 
//initial requirements or parameters are the 
// name,username,doamin name, emailid,branch office 
// another phase fro creating the 
app1.controller("tenantNewController",function($scope,countries,$http){
	  $scope.firtname = "Rahul";
	  $scope.newtenant = {
      	tenant_name :"",
      	email: "",
      	org_name: "",
      	branch_name:"",
      	//services_list:[]
  		}
	$scope.createTenant = function (){
		// new tenant details and services_list kept empty to  for generic and later added 
		console.log($scope.newtenant)
		// data = $scope.newtenant

		countries.request_post('http://172.27.30.119:8000/appoint/api/edit/tenant/',$scope.newtenant).then(function(data,status){
			// $scope.tt = responbody
			$scope.status = console.log(data)
			// console.log($scope.status)
		});		

	}
 


});

app1.controller('timerController',function($scope,$timeout,$interval,$filter){
      $scope.presentii = $filter('date')(new Date(),'HH:mm:ss');
      $scope.present = new Date('HH:mm:ss');


});

// app1.factory('apiService', function(){
     
//     var fac = {};
//      apiService.users function(){
//     	fac.users = ['John', 'James', 'Jake']; 	
//      }
     
     
//     return fac;
 
// });
app1.filter('formatTimer', function() {
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
app1.controller('DatepickerDemoCtrl', function ($scope,$filter,$timeout) {
  $scope.presentii =moment().format(' h:mm:ss a');
  $scope.startTime=moment($scope.presentii, "HH:mm:ss a");
  $scope.endTime=moment("4:30:00 pm", "HH:mm:ss a");
  $scope.duration = moment.duration($scope.endTime.diff($scope.startTime));
  $scope.hours = parseInt($scope.duration.asHours());
  $scope.minutes = parseInt($scope.duration.asMinutes())-$scope.hours*60;
  $scope.seconds = parseInt($scope.duration.asSeconds())-$scope.hours*60*60-$scope.minutes*60;

  $scope.seconds1 = parseInt($scope.duration.asSeconds());
  // $scope.presentii = $filter('date')(new Date(),'HH:mm:ss');
  // var duration = moment.duration( * 1000, 'milliseconds');
// $scope.duration1 =  moment.duration($scope.duration*1000, 'milliseconds'); 
// var interval = 1000;
// $scope.countdown =function(){
//     $timeout($scope.seconds-1,1000);

// };
// $timeout($scope.countdown,1000);
// // $timeout(, 1000)

// $scope.counter = $scope.hours*60*60+$scope.minutes*60+$scope.seconds;
$scope.counter=$scope.seconds1;
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
    $scope.presentii =moment().format(' h:mm:ss a');
      $scope.present = new Date('HH:mm:ss');
// +++++++++++++++++++++++++++++++++++++++++++++++===
  $scope.today = function() {
    $scope.dt = new Date();
  };
  $scope.today();

  $scope.clear = function() {
    $scope.dt = null;
  };

  $scope.options = {
    customClass: getDayClass,
    minDate: new Date(),
    showWeeks: true
  };

  // Disable weekend selection
  function disabled(data) {
    var date = data.date,
      mode = data.mode;
    return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
  }

  $scope.toggleMin = function() {
    $scope.options.minDate = $scope.options.minDate ? null : new Date();
  };

  $scope.toggleMin();

  $scope.setDate = function(year, month, day) {
    $scope.dt = new Date(year, month, day);
  };

  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var afterTomorrow = new Date(tomorrow);
  afterTomorrow.setDate(tomorrow.getDate() + 1);
  $scope.events = [
    {
      date: tomorrow,
      status: 'full'
    },
    {
      date: afterTomorrow,
      status: 'partially'
    }
  ];

  function getDayClass(data) {
    var date = data.date,
      mode = data.mode;
    if (mode === 'day') {
      var dayToCheck = new Date(date).setHours(0,0,0,0);

      for (var i = 0; i < $scope.events.length; i++) {
        var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return $scope.events[i].status;
        }
      }
    }

    return '';
  }
   $scope.status = {
    isFirstOpen: true,
    isFirstDisabled: false
  };
});
// app1.directive('countdowntimer',function(){
//   return {
//     restrict:'EA',
//     replace:false,
//     scope:{
//       interval: '=interval',
//       startTimeAttr: '=startTime',
//       endTimeAttr: '=endTime',
//       countdownTimeAttr: '=countdownTime'
      
//     },
//     controller:['$scope','$element','$timeout',function($scope,$timeout,$element){
//         $scope.startTime=null;
//         $scope.endTime=null;
//         $scope.countdownTime=;
//         $scope.isRunning =false;
//         $scope.presentTime=;

//         $scope.$watch('startTimeAttr',function(newValue,oldValue){
//             if (newValue!==oldValue&&$scope.isRunning)
//                 $scope.start();
//         }); 

//         $scope.start()
//     }]
//   }

// });

//#########################################################################################################
//# accessing the counter through this controller ,connected to end point /api/tenants/bankName/BranchName/
//#########################################################################################################
app1.controller('tenantCounterController',function($scope,countries){
    $scope.counter1 = [];
    $scope.counter2 = [];
    $scope.counter3 =[];
    $scope.current={};
    $scope.index=0;
    $scope.count=0;
    $scope.counters = countries.request_get("http://172.27.30.119:8000/appoint/api/tenant/SBH/asifnagar/").then(function(data,status){
      // console.log(data)
      $scope.data = data;
      $scope.count_counter = $scope.data.counters_count;
      $scope.counters = $scope.data.counters;
      // return data.value;
      $scope.counter1 = $scope.counters[0];
      $scope.counter2 = $scope.counters[1];
      $scope.counter3 = $scope.counters[2];
      $scope.count = $scope.counter1.length;
      
      $scope.current = $scope.counter1[$scope.index];
      // $scope.counter1.splice($scope.index,1);
      // while($scope.counter1.length){
      // $scope.current = $scope.counter1[index];
      
      // }

    });


    $scope.process_complete = function(){
      
      if($scope.index < $scope.count){
          $scope.index++;
      // console.log($scope.index)
      // console.log($scope.counter1)

      countries.request_post('http://172.27.30.119:8000/appoint/api/tenant/SBH/asifnagar/request',$scope.current).then(
        function(data,status){
          

        });
      $scope.current = $scope.counter1[$scope.index];
      alert( ($scope.index)+" = it is "+ $scope.current.full_name )
      // $scope.counter1.splice($scope.index,);

      //alert("")
      //console.log("hello")
      //console.log($scope.current)
      }
    }

    // $scope.count_counter = $scope.counters.counters_count;
    // console.log($scope.counters)

});

///////////////////////////////////////
// 
//////////////////////////////////////
app1.controller('userNewController',function($scope,countries){
  $scope.user={
    "full_name":"",
    "email":"",
    // "password":"",
    "mobile":"",
    // "dpassword":""
}
  $scope.rr="Hello"
  $scope.reply=""
   $scope.createNewuser = function(){
    alert("sure")
    countries.request_post('http://172.27.30.119:8000/appoint/api/newuser/',$scope.user).then(
      function(data,status){
      $scope.reply=data.message
      alert("SUccess")
          });
   }
});