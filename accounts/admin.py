from django.contrib import admin

from .models import StudentProfile


class AccountsAdmin(admin.ModelAdmin):
    readonly_fields = ['user']


admin.site.register(StudentProfile, AccountsAdmin)