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
                alert("hola");
            }
            else{
                $("#register-error-modal").removeClass("hidden");
                $("#register-error-message").html(data.error_message);
                if (typeof data.campo_erroneo !== 'undefined') {
                    $("#" + String(data.campo_erroneo)).addClass("error");
                }

            }
        },
        error: function(error) {
            alert("ERROR");
            alert(error);
            console.log(error);
        }
    });
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function resetFormularioRegistro(){
    $("#register-error-modal").addClass("hidden");
    $(".field").removeClass("error");
}