from django.db import models
from django.contrib.auth.models import User
from .utils import subject_tags, teacher_tags


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

    def get_rating_score(self):
        from statistics import mean
        ratings = SubjectRating.objects.filter(subject=self)
        rating_scores = [rating.score for rating in ratings]
        return mean(rating_scores)

    # Obtiene las 3 etiquetas más votadas
    def get_tags(self):
        most_repeated_tags = []
        ratings = SubjectRating.objects.filter(subject=self)
        rating_tags = [rating.tags for rating in ratings]
        rating_tags_count = dict(subject_tags)

        for tags in rating_tags:
            for tag in tags:
                rating_tags_count[tag] += 1

        for i in range(0, 3):
            tag = max(rating_tags_count, key=rating_tags_count.get)
            rating_tags_count.pop(tag, None)
            most_repeated_tags.append(tag)

        return most_repeated_tags


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="static/teaching/", null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name

    def get_rating_score(self):
        from statistics import mean
        ratings = TeacherRating.objects.filter(teacher=self)
        rating_scores = [rating.score for rating in ratings]
        return mean(rating_scores)

    # Obtiene las 3 etiquetas más votadas
    def get_tags(self):
        most_repeated_tags = []
        ratings = TeacherRating.objects.filter(teacher=self)
        rating_tags = [rating.tags for rating in ratings]
        rating_tags_count = dict(teacher_tags)

        for tags in rating_tags:
            for tag in tags:
                rating_tags_count[tag] += 1

        for i in range(0, 3):
            tag = max(rating_tags_count, key=rating_tags_count.get)
            rating_tags_count.pop(tag, None)
            most_repeated_tags.append(tag)

        return most_repeated_tags


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    anonymity = models.BooleanField()
    date = models.DateField()


class TeacherRating(Rating):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tags = []


class SubjectRating(Rating):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    tags = []


class Comment(models.Model):
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    text = models.TextField()
    positive_score = models.IntegerField(default=0)
    negative_score = models.IntegerField(default=0)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT, null=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    teachers = models.ManyToManyField(Teacher, blank=True)

    def __str__(self):
        return self.user.username
