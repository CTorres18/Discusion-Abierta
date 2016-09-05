'use strict';

var app =angular.module('DiscusionAbiertaApp');
app.controller('ScrollPageCtrl', function ($scope, $document) {
    $scope.toTheTop = function() {
      $document.scrollTopAnimated(0, 5000).then(function() {
        console && console.log('You just scrolled to the top!');
      });
    }
    var section2 = angular.element(document.getElementById('Section2'));
    $scope.toSection2 = function(obj) {
      $document.scrollToElementAnimated(section2);
    }
    var section3 = angular.element(document.getElementById('Section3'));
    $scope.toSection3 = function(obj) {
      $document.scrollToElementAnimated(section3);
    }


  }

  ).value('duScrollOffset', 0);