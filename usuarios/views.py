from django.http import JsonResponse
from docencia.models import Universidad
from django.shortcuts import render


def registro(request):
    if request.method == 'POST':
        campos_obligatorios = ["nombre", "apellidos", "universidad", "email", "password", "repeated_password"]
        for campo in campos_obligatorios:
            if request.POST.get(campo) is None or request.POST.get(campo) == "":
                context = {
                    "result": False,
                    "error": "Falta algun campo por rellenar.",
                    "campo_vacio": campo
                }
                return JsonResponse(context)

        email = request.POST.get("email")
        universidad = Universidad.objects.get(name=request.POST.get("universidad"))



