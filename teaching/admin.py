from django.contrib import admin

from .models import University, Degrees, Subjects, Teachers

admin.site.register(University)
admin.site.register(Degrees)
admin.site.register(Subjects)
admin.site.register(Teachers)
