// A $( document ).ready() block.
$( document ).ready(function() {

    $("#boton-menu-registro").click(function(){
        resetFormularioRegistro();
        $("#modal-registro").modal('show');
    });

    $("#boton-menu-login").click(function(){
        $("#modal-login").modal('show');
    });

    $('#dropdown-universidades').dropdown();

    $('#formulario-registro').on('submit', function(event){
        event.preventDefault();
        validar_registro();
    });

});

function validar_registro() {
    resetFormularioRegistro();
    var form = $("#formulario-registro");
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        type: "POST",
        url: "/user/register/",
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
            if (data.result) {
                $("#register-success-modal").removeClass("hidden");
                $("#register-success-message").html(data.mensaje_informativo);
            }
            else{
                $("#register-error-modal").removeClass("hidden");
                $("#register-error-message").html(data.mensaje_informativo);
                $.each(data.campos_erroneos, function(index, item){
                    $("#" + String(item)).addClass("error");
                });

            }
        },
        error: function(error) {
            $("#register-error-modal").removeClass("hidden");
            $("#register-error-message").html("Ha ocurrido un error durante tu registro, por favor, inténtalo de nuevo o contacta con el administrador de la plataforma.");

        }
    });
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function resetFormularioRegistro(){
    $("#register-error-modal").addClass("hidden");
    $("#register-success-modal").addClass("hidden");
    $(".field").removeClass("error");
}