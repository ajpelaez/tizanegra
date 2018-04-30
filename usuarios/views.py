from django.http import JsonResponse
from docencia.models import Universidad
from django.views import View


class Registro(View):
    def post(self, request):
        campos_obligatorios = ["nombre", "apellidos", "universidad", "email", "password", "repeated-password"]
        for campo in campos_obligatorios:
            if request.POST.get(campo) is None or request.POST.get(campo) == "":
                data = {
                    "result": False,
                    "error_message": "Falta algun campo por rellenar.",
                    "campo_erroneo": "field-" + str(campo)
                }
                return JsonResponse(data)

        email = request.POST.get("email")
        universidad = Universidad.objects.get(siglas=request.POST.get("universidad"))

        if universidad.siglas == "ugr":
            if not str(email).endswith(".ugr.es"):
                data = {
                    "result": False,
                    "campo_erroneo": "field-email",
                    "error_message":
                        "Para registrarte como alumno de la Universidad de Granada tu email debe acabar en .ugr.es"
                }
                return JsonResponse(data)
        else:
            data = {
                "result": False,
                "campo_erroneo": "field-universidad",
                "error_message": "La universidad elegida no existe."
            }
            return JsonResponse(data)

