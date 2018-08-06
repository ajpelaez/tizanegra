from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Teacher, University


class TeacherDetailView(DetailView):
    slug_field = 'email'

    def get_object(self):
        teacher_nick = self.kwargs.get("teacher_nick") + "@"
        university_acronym = self.kwargs.get("university").upper()
        university = University.objects.get(acronym=university_acronym)
        teacher_id = Teacher.objects.filter(email__startswith=teacher_nick).get(university=university).id
        return get_object_or_404(Teacher, pk=teacher_id)