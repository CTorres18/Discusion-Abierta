'use strict';

angular.module('DiscusionAbiertaApp', ['ngMaterial', 'LocalStorageModule', 'duScroll', 'monospaced.elastic'])
  .config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  })
  .config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  });
