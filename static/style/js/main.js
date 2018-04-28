// A $( document ).ready() block.
$( document ).ready(function() {

    $("#boton-menu-registro").click(function(){
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
    alert("Validar registro is working! ");
    var form = $(this).closest("form");
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
                alert(data.error_message);
            }
            else{
                alert(data.error_message);
            }
        },
        error: function(error) {
            alert(error);
            console.log(error);
        }
    });
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}