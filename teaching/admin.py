from django.contrib import admin

from .models import University, Degree, Subject, Teacher

admin.site.register(University)
admin.site.register(Degree)
admin.site.register(Subject)
admin.site.register(Teacher)
