'use strict';

var LOCALSTORAGE_ACTA_KEY = 'acta';

var app =angular.module('DiscusionAbiertaApp');
app.controller('ActaCtrl', function ($scope, $http, $mdDialog, localStorageService,$mdToast) {

    $scope.datito=''

    $scope.selectedTab = 0;
    $scope.counter=0;

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
             window.location.href = 'https://discusionabierta.dcc.uchile.cl/actas/bajar/' + answer
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
            window.location.href = 'https://discusionabierta.dcc.uchile.cl/actas/bajarpropuestadocx/'+ answer
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
  /*$scope.validarActa = function (ev) {
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
  };*/

  //valida un RUT
  function Validar_Rut(rut){
    if(rut.length < 5)
      return false;
    if(rut.indexOf('-') < 0)
      return false;

    //separar rut en digitos y digito verificador entregado
    var aux = rut.split('-');
    var digitos = aux[0];
    var digito_ver = aux[1].toLowerCase();

    //calcular digito verificador para compararlo con el entregado
    var suma = 0;
    var multiplicador = 2;
    for (;digitos != "";){
      var dig = digitos.slice(-1);
      suma += dig*multiplicador;
      multiplicador++;
      if(multiplicador>7)
        multiplicador=2;
      digitos = digitos.slice(0,digitos.length-1);
    }
    var digito_ver_calc = suma%11;
    digito_ver_calc = 11-digito_ver_calc

    //11=k, 10=0
    if(digito_ver_calc==11)
      digito_ver_calc='k';
    else if(digito_ver_calc==10)
      digito_ver_calc='0';
    else digito_ver_calc = digito_ver_calc + '';

    //comparacion del digito verificador entregado con digito verificador calculado
    if(digito_ver_calc==digito_ver)
      return true;
    else return false;
  }

  $scope.validarActa = function (ev) {
    $scope.noValidar = true;
    var errores = [];
    if(!$scope.acta.lugar)
      errores.push('Falta el campus.');
    if(!$scope.acta.tipo)
      errores.push('Falta el tipo de encuentro');
    if(!$scope.acta.fechaInicio)
      errores.push('Falta la fecha de inicio');
    if(!$scope.acta.fin)
      errores.push('Falta la fecha de termino');
    if(!$scope.acta.participante_organizador)
      errores.push('Falta la fecha de inicio');
    else{
      if(!$scope.acta.participante_organizador.nombre)
        errores.push('Falta el nombre del organizador');
      if(!$scope.acta.participante_organizador.apellido)
        errores.push('Falta el apellido del organizador');
      if(!$scope.acta.participante_organizador.rut)
        errores.push('Falta el rut del organizador');
      else{
        if(!Validar_Rut($scope.acta.participante_organizador.rut))
          errores.push('Falta el rut inválido del organizador');
      }
      if(!$scope.acta.participante_organizador.email)
        errores.push('Falta el email del organizador');
      if(!$scope.acta.participante_organizador.serie_cedula)
        errores.push('Falta el número de cédula del organizador');
      if(!$scope.acta.participante_organizador.ocupacion)
        errores.push('Falta el ocupación del organizador');
      if(!$scope.acta.participante_organizador.origen)
        errores.push('Falta el origen del organizador');
    }
    if(!$scope.acta.participantes)
      errores.push('Tienes que tener por lo menos' + ($scope.acta.min_participantes+1) + ' participantes');
    else {
      if($scope.acta.participantes.length < $scope.acta.min_participantes)
        errores.push('Tienes que tener por lo menos ' + ($scope.acta.min_participantes +1) + ' participantes ');
      else {
        var par_num = 0;
        for(var i=0;i<$scope.acta.participantes.length;i++){
          par_num++;
          var participante = $scope.acta.participantes[i];
          if(!participante.nombre){
            errores.push('Falta el nombre del participante ' + par_num);
          }
          else if(!participante.apellido){
            errores.push('Falta el apellido del participante ' + par_num);
          }
          else{
            if(!participante.rut){
              errores.push('Falta el rut del participante ' + par_num);
            }
            else{
              if(!Validar_Rut(participante.rut)){
                errores.push('Falta el rut inválido del participante ' + par_num);
              }
              else if(!participante.email){
                errores.push('Falta el email del participante ' + par_num);
              }
              else if(!participante.ocupacion){
                errores.push('Falta el ocupación del participante ' + par_num);
              }
              else if(!participante.origen){
                errores.push('Falta el origen del participante ' + par_num);
              }
            }
          }
        }
      }
    }
    if(errores.length > 0){
      console.log(errores);
      mostrarErrores(ev, errores);
      $scope.noValidar = false;
    }
    else {
      confirmarActa(ev);
    }
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
       $scope.counter +=1;
      if(($scope.counter% 40)==1){
        $scope.showActionToast()

      }
      localStorageService.set(LOCALSTORAGE_ACTA_KEY, $scope.acta);
    }, true);
  };
  var last = {
      bottom: false,
      top: true,
      left: false,
      right: true
    };

  $scope.toastPosition = angular.extend({},last);

  $scope.getToastPosition = function() {
    sanitizePosition();

    return Object.keys($scope.toastPosition)
      .filter(function(pos) { return $scope.toastPosition[pos]; })
      .join(' ');
  };

  function sanitizePosition() {
    var current = $scope.toastPosition;

    if ( current.bottom && last.top ) current.top = false;
    if ( current.top && last.bottom ) current.bottom = false;
    if ( current.right && last.left ) current.left = false;
    if ( current.left && last.right ) current.right = false;

    last = angular.extend({},current);
  }
  $scope.showActionToast = function() {
    var pinTo = $scope.getToastPosition();
    var toast = $mdToast.simple()
      .textContent('Recuerda: La informacion esta siendo guardada en tu navegador!')
      .action('Cerrar')
      .highlightAction(true)
      .highlightClass('md-accent')// Accent is used by default, this just demonstrates the usage.
      .position(pinTo)
        .parent(document.getElementById('ptoast'))
    .hideDelay(0);

    $mdToast.show(toast).then(function(response) {

    });
  };




  var cargarDatos = function () {



    if (localStorageService.get(LOCALSTORAGE_ACTA_KEY) !== null) {
      $scope.acta = localStorageService.get(LOCALSTORAGE_ACTA_KEY);
      //$scope.acta.fechaInicio = new Date();
      $scope.acta.fin = new Date();
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
                //$scope.acta.fechaInicio = new Date();
                $scope.acta.fin = new Date();
            }
          }
          else{
            console.log("changed it!")
            $scope.acta = response.data;
            //$scope.acta.fechaInicio = new Date();
            $scope.acta.fin = new Date();
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
})
.controller('ToastCtrl', function($scope, $mdToast) {
  $scope.closeToast = function() {
    $mdToast.hide();
  };
});

app.filter('html', ['$sce', function ($sce) {

    return function (text) {
        return $sce.trustAsHtml(text);
    };
}])
