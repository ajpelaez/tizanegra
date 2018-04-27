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
    alert("Validar registro is working!");
    var form = $(this).closest("form");
      $.ajax({
        url: form.attr("data-validate-username-url"),
        data: form.serialize(),
        dataType: 'json',
        success: function (data) {
          if (data.is_taken) {
            alert(data.error_message);
          }
        }
      });

}

