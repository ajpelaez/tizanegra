from django.contrib import admin

from .models import Student, University, Degree, Subject, Teacher


class AccountsAdmin(admin.ModelAdmin):
    readonly_fields = ['user']


admin.site.register(Student, AccountsAdmin)
admin.site.register(University)
admin.site.register(Degree)
admin.site.register(Subject)
admin.site.register(Teacher)
