'use strict';

var app = angular.module('DiscusionAbiertaApp', []);

app.controller('ScrollPageCtrl', function($scope, $document, $anchorScroll){
  var section2 = angular.element(document.getElementById('Section2'));
  $scope.toSection2 = function(obj){
    $anchorScroll('Section2');
    //$document.scrollToElementAnimated(section2);

  };

  var section3 = angular.element(document.getElementById('Section3'));
  $scope.toSection3 = function(obj){
    $anchorScroll('Section3');
    //$document.scrollToElementAnimated(section3);
  };
});

app.directive('scroll', function($window){
  return function(scope, element, attrs){
    angular.element($window).bind('scroll', function(){
      //estoy viendo la seccion 1
      if(this.pageYOffset + $window.innerHeight < angular.element(document.querySelector('#header'))[0].offsetHeight){
        scope.in1 = false;
      } else {
        scope.in1 = true;
      }

      //estoy viendo la seccion 2
      if(!(this.pageYOffset + $window.innerHeight < angular.element(document.querySelector('#header'))[0].offsetHeight) && this.pageYOffset + $window.innerHeight < angular.element(document.querySelector('#header'))[0].offsetHeight + angular.element(document.querySelector('#Section2'))[0].offsetHeight){
        scope.in2 = false;
      } else {
        scope.in2 = true;
      }

      scope.$apply();
    });
  };
});
