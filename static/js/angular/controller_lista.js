'use strict';
var urlBase = "https://dabierta-dev.dcc.uchile.cl";

var app = angular.module('DiscusionAbiertaApp', ['ngMaterial', 'LocalStorageModule'])
.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  });

app.controller('ListaCtrl', function ($scope, $http, $mdDialog, localStorageService,$mdToast, $location, $anchorScroll) {
  $scope.datito=''
  $scope.options_get = [{"name": "Origenes"},{"name": "Lugares"},{"name": "Encuentros"},{"name": "Estamentos"},{"name": "Respuestas"},{"name": "Temas"},{"name": "Participantes"},{"name": "Tipos_de_Encuentros"}]
  

  var cargarPropuestas = function () {
    $http({
      method: 'GET',
      url: 'propuestas'
    }).then(function (response) {
      $scope.propuestas = response.data.propuestas;
      console.log($scope.propuestas)
    });
  };

  function DialogController($scope, $mdDialog) {
    $scope.hide = function() {
      $mdDialog.hide();
    };

    $scope.cancel = function() {
      $mdDialog.cancel();
    };

    $scope.answer = function(answer) {
      $mdDialog.hide(answer);
    };
  }

  $scope.showInfo = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: '/static/html/angular/get_actas_view_lista.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
           if(answer.length >0) {
             window.location.href = urlBase + '/actas/bajar/' + answer
           }
    }, function() {
    });
  };
  $scope.getPropuesta = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: '/static/html/angular/get_propuesta_view_lista.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
            if(answer.length >0) {
            window.location.href = urlBase + '/actas/bajarpropuestadocx/' + answer
          }
    }, function() {
    });
  };

  cargarPropuestas();
});