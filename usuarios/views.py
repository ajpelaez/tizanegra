from django.contrib.auth.models import User
from django.http import JsonResponse
from docencia.models import Universidad
from django.views import View


class Registro(View):
    result = True
    mensaje_informativo = ""
    campos_erroneos = []

    def post(self, request):
        self.check_campos_rellenos(request)
        if not self.result:
            return JsonResponse(self.get_data_dictionary())

        self.check_email(request)
        if not self.result:
            return JsonResponse(self.get_data_dictionary())

        self.check_password(request)
        if not self.result:
            return JsonResponse(self.get_data_dictionary())

        self.check_usuario_no_registrado(request)
        if not self.result:
            return JsonResponse(self.get_data_dictionary())

        self.registrar_usuario(request)
        return JsonResponse(self.get_data_dictionary())

    def check_campos_rellenos(self, request):
        campos_obligatorios = ["nombre", "apellidos", "universidad", "email", "password", "repeated-password"]
        for campo in campos_obligatorios:
            if request.POST.get(campo) is None or request.POST.get(campo) == "":
                self.result = False
                self.mensaje_informativo = "Falta algun campo por rellenar."
                self.campos_erroneos.append("field-" + str(campo))

    def check_email(self, request):
        email = request.POST.get("email")
        universidad = Universidad.objects.get(siglas=request.POST.get("universidad"))

        if universidad.siglas == "ugr":
            if not str(email).endswith("ugr.es"):
                self.result = False
                self.campos_erroneos.append("field-email")
                self.mensaje_informativo = \
                    "Para registrarte como alumno de la Universidad de Granada tu email debe acabar en ugr.es"
        else:
            self.result = False
            self.campo_erroneo = "field-universidad",
            self.mensaje_informativo = "La universidad elegida no existe."

    def check_password(self, request):
        password = request.POST.get("password")
        repeated_password = request.POST.get("repeated-password")
        if password != repeated_password:
            self.result = False
            self.campos_erroneos.append("field-password")
            self.campos_erroneos.append("field-repeated-password")
            self.mensaje_informativo = "Las contraseñas introducidas no coinciden."

    def check_usuario_no_registrado(self, request):
        email = request.POST.get("email")
        if User.objects.filter(username=email).exists():
            self.result = False
            self.campos_erroneos.append("field-email")
            self.mensaje_informativo = "El email introducido ya esta siendo utilizado."

    def get_data_dictionary(self):
        return {
            "result": self.result,
            "mensaje_informativo": self.mensaje_informativo,
            "campos_erroneos": self.campos_erroneos
        }

    def registrar_usuario(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        universidad = Universidad.objects.get(siglas=request.POST.get("universidad"))

        user = User.objects.create_user(username=email, password=password)
        user.perfilestudiante.universidad = universidad
        user.perfilestudiante.save()
        self.mensaje_informativo = \
            "Te has registrado correctamente, revisa tu dirección de correo electrónico para confirmar tu email."
