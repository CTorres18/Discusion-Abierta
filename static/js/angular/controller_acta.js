'use strict';

var LOCALSTORAGE_ACTA_KEY = 'acta';

var app =angular.module('DiscusionAbiertaApp', ['ngMaterial', 'LocalStorageModule', 'monospaced.elastic'])
  .config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  })
  .config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  })
  .config(['msdElasticConfig', function(msdElasticConfig) { 
    msdElasticConfig.append = '\n'; 
  }]);

app.controller('ActaCtrl', function ($scope, $http, $mdDialog, localStorageService,$mdToast, $location, $anchorScroll) {
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

    $scope.datito=''

    $scope.selectedTab = 0;
    $scope.counter=0;

    $scope.categorias = ['Todos estamos en desacuerdo', 'La mayoría está en desacuerdo', 'No hay acuerdo de mayoría','La mayoría está de acuerdo',  'Todos estamos de acuerdo'];

    $scope.gotoTop = function(){
      // set the location.hash to the id of
      // the element 8you wish to scroll to.
      $location.hash(('tab' +$scope.selectedTab));

      // call $anchorScroll()
      $anchorScroll();
    }

    $scope.nextTab = function() {
        if ($scope.selectedTab === 4) {
            $scope.selectedTab = 0;
        }
        else {
            $scope.selectedTab++;
        }
        //angular.element(('#tab' +$scope.selectedTab)).triggerHandler('click');
        $scope.gotoTop();
    }

    $scope.prevTab = function(){
      if ($scope.selectedTab > 0) {
          $scope.selectedTab--;
        }
      //angular.element(('#tab' +$scope.selectedTab)).triggerHandler('click');
      $scope.gotoTop();
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

  $scope.quitarParticipante = function (index, ev) {
    if ($scope.acta.participantes.length <= $scope.acta.min_participantes) {
      return;
    }else{
      var confirm = $mdDialog.confirm()
            .title('¿Estás seguro de eliminar al participante ' + (index + 1) + ' ( ' + $scope.acta.participantes[index].nombre + ' ' + $scope.acta.participantes[index].apellido + ' ) ?')
            .textContent()
            .ariaLabel('Lucky day')
            .targetEvent(ev)
            .ok('Eliminar')
            .cancel('Mantener');

      $mdDialog.show(confirm).then(function() {
        $scope.acta.participantes.splice(index, 1);
      }, function() {
        //Do nothing
      });
    }
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
      templateUrl: '/static/html/angular/not_get_actas_view.html',
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
      templateUrl: '/static/html/angular/get_propuesta_view_subir.html',
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
      digito_ver_calc='0';
    else if(digito_ver_calc==10)
      digito_ver_calc='k';
    else digito_ver_calc = digito_ver_calc + '';

    //comparacion del digito verificador entregado con digito verificador calculado
    if(digito_ver_calc==digito_ver)
      return true;
    else return false;
  }

  $scope.buscarErrores = function(ev){
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
    return errores;
  }

  $scope.validarParticipantes = function(ev){
    $scope.noValidar = true;
    var errores = $scope.buscarErrores(ev);
    if(errores.length > 0){
      console.log(errores);
      mostrarErrores(ev, errores);
      $scope.noValidar = false;
    }

  };

  $scope.validarActa = function (ev) {
    $scope.noValidar = true;
    var errores = $scope.buscarErrores(ev);
    if(errores.length > 0){
      console.log(errores);
      mostrarErrores(ev, errores);
      $scope.noValidar = false;
    }
    else {
      confirmarActa(ev);
    }
  };
  
  var cargarWatchersActa = function () {
    $scope.$watch('acta', function () {
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
    $http({
        method: 'POST',
        url: '/actas/enviarprepropuesta',
        data: $scope.acta
      }).then(
        function (response) {
          console.log("test ok")
        },
        function (response) {
           console.log("test fail")
        }
      );
    var pinTo = $scope.getToastPosition();
    var toast = $mdToast.simple()
      .textContent('¡Guardado! \n La información ha sido guardada, pero solo en su computador.\n Recuerde "Subir Propuesta" en la pestaña de igual nombre en el punto 4 cuando termine de editar su propuesta.')
      .action('Entendido')
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
      console.log('changed it!')
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
        $scope.acta.tipo = "Encuentro autoconvocado";
      });
      console.log($scope.acta)
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
