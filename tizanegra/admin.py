from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class AccountsAdmin(admin.ModelAdmin):
    readonly_fields = ['user']


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ['sender', 'comment', 'reason', 'date']
    list_display = ('sender', 'reason', 'comment', 'rating_link', 'date')

    def rating_link(self, obj):
        link = reverse("admin:tizanegra_rating_change", args=[obj.comment.rating.pk])
        return format_html('<a href="{}">View rating</a>', link)


class CommentInline(admin.StackedInline):
    model = Comment


class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'score', 'anonymity', 'date', 'tag1', 'tag2', 'tag3']
    inlines = [CommentInline]


admin.site.register(Student, AccountsAdmin)
admin.site.register(University)
admin.site.register(Degree)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Report, ReportAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Comment)

