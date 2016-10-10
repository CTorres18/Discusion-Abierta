'use strict';
var app = angular.module('DiscusionAbiertaApp', ['ngMaterial', 'LocalStorageModule'])
.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  });

app.controller('ListaCtrl', function ($scope, $http, $mdDialog, localStorageService,$mdToast, $location, $anchorScroll) {

  var cargarPropuestas = function () {

    $http({
      method: 'GET',
      url: 'propuestas'
    }).then(function (response) {
      $scope.propuestas = response.data.propuestas;
      console.log($scope.propuestas)
    });
  };
  cargarPropuestas();
});