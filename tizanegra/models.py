import random

from django.db import models
from django.contrib.auth.models import User
from .utils import subject_tags, teacher_tags


class University(models.Model):
    acronym = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="static/universities_logos", null=True, blank=True)
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
    website = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_url(self):
        return str("/" + self.university.acronym).lower() + "/" + self.degrees.first().acronym.lower() + "/" + \
               self.acronym.lower()

    def get_rating_score(self):
        ratings = SubjectRating.objects.filter(subject=self)
        if ratings:
            from statistics import mean
            return mean([rating.score for rating in ratings])
        else:
            return 0

    # Obtiene las 3 etiquetas más votadas
    def get_tags(self):
        most_repeated_tags = []
        ratings = SubjectRating.objects.filter(subject=self)
        rating_tags = []
        for rating in ratings:
            rating_tags.append(rating.tag1)
            rating_tags.append(rating.tag2)
            rating_tags.append(rating.tag3)

        rating_tags_count = dict(subject_tags)

        for tag in rating_tags:
            if tag:
                rating_tags_count[tag] += 1

        for i in range(0, 3):
            tag = max(rating_tags_count, key=rating_tags_count.get)
            rating_tags_count.pop(tag, None)
            most_repeated_tags.append(tag)

        return most_repeated_tags


class Teacher(models.Model):
    GENDER = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="static/teachers_photos/", null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200)
    gender = models.CharField(max_length=6, choices=GENDER, default='MALE')

    def __str__(self):
        return self.name

    def get_photo(self):
        if self.photo:
            return self.photo
        else:
            if self.gender == 'FEMALE':
                return "static/images/teacher_female.png"
            else:
                return "static/images/teacher_male" + str(random.randint(1, 3)) + ".png"

    def get_nick(self):
        return str(self.email).split("@")[0]

    def get_url(self):
        return str("/" + self.university.acronym).lower() + "/" + self.get_nick() + "/"

    def get_rating_score(self):
        ratings = TeacherRating.objects.filter(teacher=self)
        if ratings:
            from statistics import mean
            return mean([rating.score for rating in ratings])
        else:
            return 0

    # Obtiene las 3 etiquetas más votadas
    def get_tags(self):
        most_repeated_tags = []
        ratings = TeacherRating.objects.filter(teacher=self)

        if not ratings:
            return ["Sin", "etiquetas", ""]

        rating_tags = []
        for rating in ratings:
            rating_tags.append(rating.tag1)
            rating_tags.append(rating.tag2)
            rating_tags.append(rating.tag3)

        rating_tags_count = dict(teacher_tags)

        for tag in rating_tags:
            if tag:
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
    tag1 = models.CharField(max_length=20)
    tag2 = models.CharField(max_length=20)
    tag3 = models.CharField(max_length=20)

    def add_tag(self, tag):
        if self.tag1 == '':
            self.tag1 = tag
        elif self.tag2 == '':
            self.tag2 = tag
        else:
            self.tag3 = tag

    def __str__(self):
        return "#" + str(self.pk) + " " + self.user.username + "'s rating"


class TeacherRating(Rating):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class SubjectRating(Rating):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Comment(models.Model):
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE)
    text = models.TextField()

    def positive_score(self):
        return CommentScore.objects.filter(comment=self, is_positive=True).count()

    def negative_score(self):
        return CommentScore.objects.filter(comment=self, is_positive=False).count()

    def __str__(self):
        return self.text


class CommentScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_positive = models.BooleanField()

    class Meta:
        unique_together = ('user', 'comment')


class Student(models.Model):
    GENDER = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT, null=True)
    photo = models.ImageField(upload_to="static/students_photos/", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER, default='MALE')

    def __str__(self):
        return self.user.username

    def get_photo(self):
        if self.photo:
            return self.photo
        else:
            if self.gender == 'FEMALE':
                return "static/images/student_female.png"
            else:
                return "static/images/student_male.png"

    def get_ratings_count(self):
        return Rating.objects.filter(user=self.user).count()

    def get_ratings(self):
        return Rating.objects.filter(user=self.user)


class Report(models.Model):
    REPORT_STATUS = (
        ('PENDING', 'Pending'),
        ('CHECKED', 'Checked'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=7, choices=REPORT_STATUS, default='PENDING')
    date = models.DateField()

    def __str__(self):
        return self.sender.username + "'s report"

    def rating(self):
        return self.comment.rating
