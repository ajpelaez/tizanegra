from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Teacher


class TeacherDetailView(DetailView):
    model = Teacher