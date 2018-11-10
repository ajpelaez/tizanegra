import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from django.views import View
from django.contrib.auth import login
import re
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import *
from .utils import subject_tags, teacher_tags


def index(request):

    teachers = Teacher.objects.all()
    best_teachers = []

    for i in range(0, min(len(teachers), 4)):
        teacher = max(teachers, key=lambda t: t.get_rating_score())
        teachers = teachers.exclude(id=teacher.id)
        best_teachers.append(teacher)

    context = {
        "universidades": University.objects.all(),
        "best_teachers": best_teachers
    }

    return render(request, 'tizanegra/index.html', context)


class UserCreate(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                student_profile = serializer.save()
                if student_profile:
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


@api_view(['GET'])
def get_teachers_and_subjects(request, name):

    teachers = Teacher.objects.filter(name__contains=name)
    subjects = Subject.objects.filter(name__contains=name)
    items = []

    for teacher in teachers:
        items.append(
            {"name": teacher.name,
             "email": teacher.email,
             "url": teacher.get_url()})

    for subject in subjects:
        items.append(
            {"name": subject.name,
             "url": subject.get_url()}
        )

    context = {
        "total_count": len(teachers) + len(subjects),
        "items": items,
    }
    return Response(context)


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
        if self.request.user.is_authenticated:
            context['rated'] = TeacherRating.objects.filter(teacher=context['teacher'], user=self.request.user).exists()
        context['ratings'] = TeacherRating.objects.filter(teacher=context['teacher']).order_by('-date', '-pk')
        return context

    def post(self, request, *args, **kwargs):
        try:
            university = University.objects.get(acronym=(kwargs["university"].upper()))
            teacher = Teacher.objects.filter(email__startswith=kwargs['teacher']).get(university=university)

            rating_comment = request.POST.get("rating_comment")
            anonymity = "anonymous_rating" in request.POST
            teacher_rating = TeacherRating(user=request.user, score=request.POST["rating"], anonymity=anonymity,
                                           date=datetime.date.today(), teacher=teacher)

            for tag in teacher_tags.keys():
                if tag in request.POST.keys():
                    teacher_rating.add_tag(tag)

            teacher_rating.save()

            if rating_comment != "":
                comment = Comment(rating=teacher_rating, text=rating_comment)
                comment.save()

            context = {"teacher": teacher, "tags": teacher_tags.keys,
                       "post_request_result": True,
                       "rated": TeacherRating.objects.filter(teacher=teacher, user=self.request.user).exists(),
                       "ratings": TeacherRating.objects.filter(teacher=teacher).order_by('-date', '-pk')}
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
        if self.request.user.is_authenticated:
            context['rated'] = SubjectRating.objects.filter(subject=context['subject'], user=self.request.user).exists()
        context['ratings'] = SubjectRating.objects.filter(subject=context['subject']).order_by('-date', '-pk')
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

            for tag in subject_tags.keys():
                if tag in request.POST.keys():
                    subject_rating.add_tag(tag)

            subject_rating.save()

            if rating_comment != "":
                comment = Comment(rating=subject_rating, text=rating_comment)
                comment.save()

            context = {"subject": subject, "tags": subject_tags.keys, "degree": degree,
                       "post_request_result": True,
                       "rated": SubjectRating.objects.filter(subject=subject, user=self.request.user).exists(),
                       "ratings": SubjectRating.objects.filter(subject=subject).order_by('-date', '-pk')}
        except:
            context = {"post_request_result": False}

        return render(request, 'tizanegra/subject_detail.html', context)


@api_view(['POST'])
def report_comment(request):
    try:
        comment = Comment.objects.get(pk=request.data["comment_id"])
        report = Report(sender=request.user, comment=comment, date=datetime.date.today(),
                        reason=request.data["report_reason"])

        report.save()
        return Response({"message": "Tu reporte se ha enviado corretamente. "
                                    "Será revisado por un moderador lo antes posible."})
    except:
        return Response({"message": "Ha ocurrido un error al enviar tu reporte, intentálo de nuevo o ponte en"
                                    "contacto con el administrador de la plataforma."})


@api_view(['POST'])
def rate_comment(request):
    comment = Comment.objects.get(pk=request.data["comment_id"])
    score = request.data["is_positive"]
    try:
        comment_score = CommentScore.objects.get(comment=comment, user=request.user)

        score_changed = comment_score.is_positive != score
        if score_changed:
            comment_score.is_positive = score
            comment_score.save()
        return Response({"result": True, "created": False, "changed": score_changed})

    except CommentScore.DoesNotExist:
        comment_score = CommentScore(comment=comment, user=request.user, is_positive=score)
        comment_score.save()
        return Response({"result": True, "created": True})

    except:
        return Response({"result": False})
