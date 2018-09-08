import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login
import re
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Teacher, University, Degree, Subject, SubjectRating, Comment, TeacherRating
from .utils import subject_tags, teacher_tags


def index(request):
    context = {
        "universidades": University.objects.all(),
    }

    return render(request, 'tizanegra/index.html', context)


class UserCreate(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                student_profile = serializer.save()
                if student_profile:
                    token = Token.objects.create(user=student_profile.user)
                    login(request, student_profile.user)
                    return Response({'result': True})
        except Exception as e:
            exception = str(e)

        signup_errors = serializer.errors
        signup_errors['result'] = False
        signup_errors['exception'] = exception
        signup_errors['message'] = 'Ha ocurrido un error con el registro, revisa todos tus datos e inténtalo de nuevo'
        return Response(signup_errors)


@api_view(['GET'])
def check_username_is_valid(request, username):
    if len(username) < 4:
        return Response({'result': False,
                         'message': 'El nombre de usuario debe tener al menos 4 carácteres'})

    if re.match("^[a-zA-Z0-9_.-]+$", username) is None:
        return Response({'result': False,
                         'message': 'El nombre de usuario no puede incluir alguno de los símbolos utilizados'})

    if User.objects.filter(username=username).exists():
        return Response({'result': False,
                         'message': 'Este nombre de usuario ya esta siendo usado'})

    return Response({'result': True})


@api_view(['GET'])
def check_email_is_valid(request, email):
    if User.objects.filter(email=email).exists():
        return Response({'result': False,
                         'message': 'El email introducido ya esta siendo usado'})
    return Response({'result': True})


class UserPanelView(View):

    def get(self, request):
        context = {'test': 'hi'}
        return render(request, 'registration/panel.html', context)


class TeacherDetailView(DetailView):
    model = Teacher

    def get_object(self):
        try:
            teacher_nick = self.kwargs.get("teacher") + "@"
            university_acronym = self.kwargs.get("university").upper()
            university = University.objects.get(acronym=university_acronym)
            teacher_id = Teacher.objects.filter(email__startswith=teacher_nick).get(university=university).id
        except ObjectDoesNotExist:
            teacher_id = 0
        return get_object_or_404(Teacher, pk=teacher_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = teacher_tags.keys
        context['ratings'] = TeacherRating.objects.filter(teacher=context['teacher'])
        return context

    def post(self, request, *args, **kwargs):
        try:
            university = University.objects.get(acronym=(kwargs["university"].upper()))
            teacher = Teacher.objects.filter(email__startswith=kwargs['teacher']).get(university=university)

            rating_comment = request.POST.get("rating_comment")
            anonymity = "anonymous_rating" in request.POST
            teacher_rating = TeacherRating(user=request.user, score=request.POST["rating"], anonymity=anonymity,
                                           date=datetime.date.today(), teacher=teacher)
            teacher_rating.save()

            for tag in teacher_tags.keys():
                if tag in request.POST.keys():
                    teacher_rating.tags.append(tag)

            if rating_comment != "":
                comment = Comment(rating=teacher_rating, text=rating_comment)
                comment.save()

            context = {"teacher": teacher, "tags": teacher_tags.keys,
                       "post_request_result": True, "ratings": TeacherRating.objects.filter(teacher=teacher)}

        except:
            context = {"post_request_result": False}

        return render(request, 'tizanegra/teacher_detail.html', context)


class SubjectDetailView(DetailView):
    model = Subject
    degree = None

    def get_object(self):
        university_acronym = self.kwargs.get("university").upper()
        degree_acronym = self.kwargs.get("degree").upper()
        subject_acronym = self.kwargs.get("subject").upper()

        university = University.objects.get(acronym=university_acronym)
        self.degree = Degree.objects.get(acronym=degree_acronym)
        return get_object_or_404(Subject, university=university, degrees=self.degree, acronym=subject_acronym)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['degree'] = self.degree
        context['tags'] = subject_tags.keys
        context['ratings'] = SubjectRating.objects.filter(subject=context['subject'])
        return context

    def post(self, request, *args, **kwargs):
        try:
            rating_comment = request.POST.get("rating_comment")
            anonymity = "anonymous_rating" in request.POST
            degree = Degree.objects.get(acronym=kwargs.get("degree").upper())
            university = University.objects.get(acronym=kwargs.get("university").upper())
            subject = Subject.objects.get(university=university, acronym=kwargs.get("subject").upper(), degrees=degree)
            subject_rating = SubjectRating(user=request.user, score=request.POST["rating"], anonymity=anonymity,
                                           date=datetime.date.today(), subject=subject)
            subject_rating.save()

            for tag in subject_tags.keys():
                if tag in request.POST.keys():
                    subject_rating.tags.append(tag)

            if rating_comment != "":
                comment = Comment(rating=subject_rating, text=rating_comment)
                comment.save()

            context = {"subject": subject, "tags": subject_tags.keys, "degree": degree,
                       "post_request_result": True, "ratings": SubjectRating.objects.filter(subject=subject)}
        except:
            context = {"post_request_result": False}

        return render(request, 'tizanegra/subject_detail.html', context)
