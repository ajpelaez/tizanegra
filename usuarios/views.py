from django.http import JsonResponse
from docencia.models import Universidad
from django.shortcuts import render


def registro(request):
    if request.method == 'POST':
        campos_obligatorios = ["nombre", "apellidos", "universidad", "email", "password", "repeated_password"]
        for campo in campos_obligatorios:
            if request.POST.get(campo) is None or request.POST.get(campo) == "":
                data = {
                    "result": False,
                    "error_message": "Falta algun campo por rellenar.",
                    "error_code": 1,
                    "campo_vacio": campo
                }
                return JsonResponse(data)

        email = request.POST.get("email")
        universidad = Universidad.objects.get(name=request.POST.get("universidad"))

        if universidad == "ugr":
            if not str(email).endswith(".ugr.es"):
                data = {
                    "result": False,
                    "error_message":
                        "Para registrarte como alumno de la Universidad de Granada tu email debe acabar en .ugr.es",
                    "error_code": 2
                }
                return JsonResponse(data)
        else:
            data = {
                "result": False,
                "error_message": "La universidad elegida no existe.",
                "error_code": 3
            }
            return JsonResponse(data)




