from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Teacher, University, Degree, Subject


class TeacherDetailView(DetailView):

    def get_object(self):
        try:
            teacher_nick = self.kwargs.get("teacher") + "@"
            university_acronym = self.kwargs.get("university").upper()
            university = University.objects.get(acronym=university_acronym)
            teacher_id = Teacher.objects.filter(email__startswith=teacher_nick).get(university=university).id
        except ObjectDoesNotExist:
            teacher_id = 0
        return get_object_or_404(Teacher, pk=teacher_id)


class SubjectDetailView(DetailView):
    degree = None

    def get_object(self):
        university_acronym = self.kwargs.get("university").upper()
        degree_acronym = self.kwargs.get("degree").upper()
        subject_acronym = self.kwargs.get("subject").upper()

        university = University.objects.get(acronym=university_acronym)
        self.degree = Degree.objects.get(acronym=degree_acronym)
        return get_object_or_404(Subject, university=university, degrees=self.degree , acronym=subject_acronym)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['degree'] = self.degree
        return context
