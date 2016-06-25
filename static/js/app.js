var mozioapp = angular.module('mozio', ['ngCookies',]);

mozioapp.run(function($http,$cookies) {

  $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
  $http.defaults.headers.put['X-CSRFToken'] = $cookies.get('csrftoken');
  
});


mozioapp.controller('signupcontroller',function($scope, $http, $window){

  signupData = {}
  //signup service provider
  $scope.signup = function()
  {
      signupData = {'email':$scope.inputemail, 'name':$scope.inputname, 
      'currency':$scope.inputcurrency, 'language':$scope.inputlanguage,
      'phone_number':$scope.inputphone}
      console.log(signupData)
      $http.post("../provider/", signupData).then(function(response)
      {
        console.log(response);
        if(response.status===201)
        {
          window.location.href="/";
        }
        
      },
      function(response)
      {
        console.log(response)
        if(response.status===403)
        {
          alert("Email already exists")
        }
        else
        {
          alert("Error. Try again.")          
        }
      });
  }
});


mozioapp.controller('loginaccesscontroller', function($scope, $http, $cookies)
{
  $scope.get_access = function()
  {
    accessData = {}
    accessData = {'email':$scope.inputemail, 'phone_number':$scope.inputphone}
    $http.post("get_access/", accessData).then(function(response)
    {
      if(response.status===200)
      {
        // setting cookies to do CRUD operations
        $scope.currency = response.data['currency']
        $scope.provider_name = response.data['name']
        $cookies.put('email',$scope.inputemail,{path:'/'});
        $cookies.put('phone',$scope.inputphone,{path:'/'});
        $cookies.put('currency',$scope.currency,{path:'/'});
        $cookies.put('name',$scope.provider_name,{path:'/'});
        window.location.href="/define_service";
      }
    },
    function(err)
    {
      if(err.status===404)
      {
        alert("Access code doesnt match.")
      }
      else
      {
        alert("Error occurred.Try again.")
      }
    })

  }
});

mozioapp.controller('defineservicecontroller', function($scope, $http, $cookies, $window)
{
  $scope.currency = $cookies.get('currency')
  $scope.provider_name = $cookies.get('name')
  $scope.inputname = $window.areaname;
  $scope.inputprice = parseInt($window.price)
  $scope.savearea = function()
  {
      geojson = angular.element(document.querySelector("#inputGeojson")).val()
      data = {'geojson':geojson,'name':$scope.inputname, 'price':$scope.inputprice,
              'email':$cookies.get('email'), 'phone_number':$cookies.get('phone')}
    if(geojson && $scope.inputname && $scope.inputprice)
      {

        $http.post("../service/", data).then(function(response)
        {
          alert("Service Area added. Add more service")
           $window.location.reload()

        },function(err)
        {
          alert("Error occurred.")
        })
      }
      else
      {
        alert("Please fill all the fields and chose area.")
      }


  }


  $scope.updatearea = function(id)
  {

      geojson = angular.element(document.querySelector("#inputGeojson")).val()
      data = {'geojson':geojson,'name':$scope.inputname, 'price':$scope.inputprice,
              'email':$cookies.get('email'), 'phone_number':$cookies.get('phone'),
              'service_id':id}
      if(geojson && $scope.inputname && $scope.inputprice)
      {

        $http.put("../../service/"+id+"/update_service/", data).then(function(response)
        {
          alert("Service Area updated. Add more service")
           $window.location.reload()

        },function(err)
        {
          alert("Error occurred.")
        })
        }
      else
      {
        alert("Please fill all the fields and chose area.")
      }
  }

});

mozioapp.controller('servicecontroller', function($scope, $http, $cookies)
{
  $scope.get_services = function()
  {
      $scope.serviceareas = null
      data = {'lat':$scope.inputlat, 'long':$scope.inputlong}
      $http.get("../service/valid_areas/",{params:data}).then(function(response)
      {
        $scope.serviceareas = response.data

      },function(err)
      {
        alert("Error occurred.")
      })
  }

});


mozioapp.controller('areascontroller', function($scope, $http, $cookies)
{
  $scope.get_services = function()
  {
      $scope.serviceareas = null
      data = {'email':$cookies.get('email'), 'phone_number':$cookies.get('phone')}
      $http.get("../service/get_areas_of_provider/",{params:data}).then(function(response)
      {
        $scope.serviceareas = response.data

      },function(err)
      {
        alert("Error occurred.")
      })
  }

  $scope.delete_area = function(id)
  {
    data = {'email':$cookies.get('email'), 'phone_number':$cookies.get('phone'), 'id':id}
    $http.put("../service/"+id+"/delete_service/",data).then(function(response)
    {
      alert("Deleted")
      $scope.get_services()
    },
    function(err)
    {
      alert("Error occurred.")
    })
  }

});


mozioapp.controller('basecontroller', function($scope, $http, $cookies)
{
  $scope.is_accessed = function()
  {
      email = $cookies.get('email')
      phone = $cookies.get('phone')
      if(email !=null && phone !=null)
      {
        return true
      }
      return false
  }
  $scope.clearcookies = function()
  {
    var cookies = $cookies.getAll();
    angular.forEach(cookies, function (v, k) {
      console.log(k)
      $cookies.remove(k,{path:'/'});
    });
    window.location.href="/";
  }

});

