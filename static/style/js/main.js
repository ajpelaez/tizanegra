// A $( document ).ready() block.
$( document ).ready(function() {

    $("#boton-menu-registro").click(function(){
        $("#modal-registro").modal('show');
    });
    $("#boton-menu-login").click(function(){
        $("#modal-login").modal('show');
    });

    $('.dropdown').dropdown();
});


