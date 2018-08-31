from django.contrib.auth.models import User
from django.db import models


class University(models.Model):
    acronym = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="static/", null=True, blank=True)
    web = models.CharField(max_length=100)
    email_extension = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"


class Degree(models.Model):
    acronym = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Subject(models.Model):
    acronym = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    degrees = models.ManyToManyField(Degree)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="static/teaching/", null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    anonymity = models.BooleanField()
    date = models.DateField()


class TeacherRating(Rating):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tags = {"Exigente": 0, "Justo": 0, "Pasota": 0, "Simpático": 0}


class SubjectRating(Rating):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    tags = {"Divertida": 0, "Muy práctica": 0, "Actual": 0, "Desfasada": 0, "Muy teórica": 0}


class Comment(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    text = models.TextField()
    positive_score = models.IntegerField(default=0)
    negative_score = models.IntegerField(default=0)

