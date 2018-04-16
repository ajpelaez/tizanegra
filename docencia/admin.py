from django.contrib import admin

from .models import Universidad, Titulacion, Asignatura, Profesor

admin.site.register(Universidad)
admin.site.register(Titulacion)
admin.site.register(Asignatura)
admin.site.register(Profesor)
