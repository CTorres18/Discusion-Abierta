'use strict';

var LOCALSTORAGE_ACTA_KEY = 'acta';

var app =angular.module('DiscusionAbiertaApp');
app.controller('ActaCtrl', function ($scope, $http, $mdDialog, localStorageService) {

    $scope.datito=''

    $scope.selectedTab = 0;

    $scope.categorias = ['Todos estamos en desacuerdo', 'La mayoría está en desacuerdo', 'No hay acuerdo de mayoría','La mayoría está de acuerdo',  'Todos estamos de acuerdo'];

    $scope.nextTab = function() {
        if ($scope.selectedTab === 4) {
            $scope.selectedTab = 0;
        }
        else {
            $scope.selectedTab++;
        }
    }

    $scope.prevTab = function(){
      if ($scope.selectedTab > 0) {
          $scope.selectedTab--;
        }
    }

    $scope.isSelectedTab = function(thisTab){
     // console.log($scope.selectedTab);
      return $scope.selectedTab === thisTab;
    }


  $scope.agregarParticipante = function () {
    if ($scope.acta.participantes.length < $scope.acta.max_participantes) {
      $scope.acta.participantes.push({nombre: '', apellido: ''});
    }
  };

  $scope.quitarParticipante = function (index) {
    if ($scope.acta.participantes.length <= $scope.acta.min_participantes) {
      return;
    }
    $scope.acta.participantes.splice(index, 1);
  };

  var DialogErroresCtrl = function ($scope, $mdDialog, errores) {
    $scope.errores = errores;

    $scope.close = function () {
      $mdDialog.hide();
    };
  };

  var DialogDisclaimerCtrl = function ($scope, $mdDialog) {

    $scope.aceptamos = false;

    $scope.aceptan = function () {
      $mdDialog.hide();
    };

    $scope.rechazan = function () {
      $mdDialog.cancel();
    };
  };

  var mostrarErrores = function (ev, errores) {
    $mdDialog.show({
      controller: DialogErroresCtrl,
      templateUrl: '/static/html/angular/errors.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose: true,
      locals: {
        errores: errores
      }
    });
  };
    $scope.showInfo = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: '/static/html/angular/get_actas_view.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
           if(answer.length >0) {
             window.location.href = 'http://localhost:8000/actas/bajar/' + answer
           }
    }, function() {
    });
  };
  $scope.getPropuesta = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      templateUrl: '/static/html/angular/get_propuesta_view.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose:true,
      fullscreen: $scope.customFullscreen // Only for -xs, -sm breakpoints.
    })
    .then(function(answer) {
            if(answer.length >0) {
            window.location.href = 'http://localhost:8000/actas/bajarpropuestadocx/'+ answer
          }
    }, function() {
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
  var confirmarActa = function (ev) {
    $mdDialog.show({
      controller: DialogDisclaimerCtrl,
      templateUrl: '/static/html/angular/disclaimer.html',
      parent: angular.element(document.body),
      targetEvent: ev,
      clickOutsideToClose: true,
    }).then(function (result) {
      $http({
        method: 'POST',
        url: '/actas/subir/confirmar',
        data: $scope.acta
      }).then(
        function (response) {
          $mdDialog.show($mdDialog.alert()
            .textContent(response.data.mensajes[0])
            .ariaLabel('Envío del acta')
            .ok('OK')
            .targetEvent(ev));
          $scope.noValidar = false;
        },
        function (response) {
          mostrarErrores(ev, response.data.mensajes);
          $scope.noValidar = false;
        }
      );
    }, function (result) {
      $scope.noValidar = false;
    });
  };
  $scope.validarActa = function (ev) {
    $scope.noValidar = true;

    $http({
      method: 'POST',
      url: '/actas/subir/validar',
      data: $scope.acta
    }).then(
      function (response) {
        confirmarActa(ev);
      },
      function (response) {
        mostrarErrores(ev, response.data.mensajes);
        $scope.noValidar = false;
      }
    );
  };


  //$scope.bajarActa = function (ev) {
  //  console.log($scope.acta)
  //
  //  var docDefinition = {
  //    content: 'propuesta funciona :D'
  //  };
  //  pdfMake.createPdf(docDefinition).download('propuesta.pdf')
    /*$http({
      method: 'POST',
      url: '/actas/bajarpropuestadocx',
      data: $scope.acta
    }).then(
      function (response) {
        document.location = 'data:application/vnd.openxmlformats-officedocument.wordprocessingml.document,' +encodeURIComponent(response);
        console.log(response);
      },
      function (response) {
        console.log('FALLEEE');
        console.log(response);
      }
    );*/
  //};
 /* var filtrarProvincias = function () {
    $scope.provinciasFiltradas = $scope.provincias.filter(function (provincia) {
      if ($scope.acta.geo.region === undefined) {
        return false;
      }
      return provincia.fields.region === $scope.acta.geo.region;
    });
  };

  var filtrarComunas = function () {
    $scope.comunasFiltradas = $scope.comunas.filter(function (comuna) {
      if ($scope.acta.geo.provincia === undefined) {
        return false;
      }
      return comuna.fields.provincia === $scope.acta.geo.provincia;
    });
  };

  var cargarWatchersGeo = function () {
    $scope.$watch('acta.geo.region', function () {
      if ( ! String($scope.acta.geo.provincia).startsWith(String($scope.acta.geo.region))) {
        delete $scope.acta.geo.provincia;
      }
      if ( ! String($scope.acta.geo.comuna).startsWith(String($scope.acta.geo.provincia))) {
        delete $scope.acta.geo.comuna;
      }
      filtrarProvincias();
    });

    $scope.$watch('acta.geo.provincia', function () {
      if ( ! String($scope.acta.geo.comuna).startsWith(String($scope.acta.geo.provincia))) {
        delete $scope.acta.geo.comuna;
      }
      filtrarComunas();
    });
  };
*/
  var cargarWatchersActa = function () {
    $scope.$watch('acta', function () {
      localStorageService.set(LOCALSTORAGE_ACTA_KEY, $scope.acta);
    }, true);
  };



  var cargarDatos = function () {



    if (localStorageService.get(LOCALSTORAGE_ACTA_KEY) !== null) {
      $scope.acta = localStorageService.get(LOCALSTORAGE_ACTA_KEY);
    }

      $http({
        method: 'GET',
        url: '/actas/base/21'
      }).then(function (response) {
        if (!(typeof $scope.acta === "undefined"))
        {
          if (!(typeof $scope.acta.updated_at === "undefined")) {
            var striped_data = response.data.updated_at.substring(0,19);
            var striped_acta = $scope.acta.updated_at.substring(0,19);
            if (!(striped_data === striped_acta)) {
              console.log("changed it!");
                $scope.acta = response.data;
            }
          }
          else{
            console.log("changed it!")
            $scope.acta = response.data;
          }
        }



      });
      //console.log($scope.acta)
    };
    /////////////////
    ////

  $scope.limpiarActa = function (ev) {

    var confirm = $mdDialog.confirm()
      .clickOutsideToClose(true)
      .textContent('¿Estás seguro de que quieres limpiar los datos del acta?')
      .ariaLabel('Limpiar acta')
      .targetEvent(ev)
      .ok('Limpiar')
      .cancel('Cancelar');

    $mdDialog.show(confirm).then(function (result) {
      localStorageService.remove(LOCALSTORAGE_ACTA_KEY);
      cargarDatos();
    });
  };

  $scope.acta = {
    geo: {}
  };
  $scope.toggleView = function(ary, data, index){
    for(var i=0; i<ary.length; i++){
      if(i!=index) { ary[i].expanded=false; }
      else { data.expanded=!data.expanded; }
    }
  }


  //cargarWatchersGeo();
    $scope.options_get = [{"name": "Origenes"},{"name": "Lugares"},{"name": "Encuentros"},{"name": "Estamentos"},{"name": "Respuestas"},{"name": "Temas"},{"name": "Participantes"},{"name": "Tipos_de_Encuentros"}]
    $scope.datito=''
    $scope.to_trusted = function(html_code) {
    return $sce.trustAsHtml(html_code);
}

/*
  $http({
    method: 'GET',
    url: '/static/json/regiones.json'
  }).then(function (response) {
    $scope.regiones = response.data;
  });

  $http({
    method: 'GET',
    url: '/static/json/provincias.json'
  }).then(function (response) {
    $scope.provincias = response.data;
    filtrarProvincias();
  });

  $http({
    method: 'GET',
    url: '/static/json/comunas.json'
  }).then(function (response) {
    $scope.comunas = response.data;
    filtrarComunas();
  });
*/
  cargarWatchersActa();
  cargarDatos();
});

app.filter('html', ['$sce', function ($sce) {
    return function (text) {
        return $sce.trustAsHtml(text);
    };
}])
