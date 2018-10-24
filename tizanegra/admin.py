from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import *


class AccountsAdmin(admin.ModelAdmin):
    readonly_fields = ['user']


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ['sender', 'comment', 'reason', 'date', 'rating']
    list_display = ('sender', 'reason', 'comment_text', 'rating_link', 'date', 'status')

    def rating_link(self, obj):
        link = reverse("admin:tizanegra_rating_change", args=[obj.comment.rating.pk])
        return format_html('<a href="{}">View rating and comment</a>', link)

    def rating(self, obj):
        link = reverse("admin:tizanegra_rating_change", args=[obj.comment.rating.pk])
        return format_html('<a href="{}">View Rating</a>', link)

    def comment_text(self, obj):
        return obj.comment.text


class ReportInline(admin.TabularInline):
    model = Report
    readonly_fields = ['sender', 'reason', 'date']


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['rating_link']
    exclude = ['rating']
    inlines = [ReportInline]

    def rating_link(self, obj):
        link = reverse("admin:tizanegra_rating_change", args=[obj.rating.pk])
        return format_html('<a href="{}">View Rating</a>', link)


class CommentInline(admin.TabularInline):
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
admin.site.register(Comment, CommentAdmin)

