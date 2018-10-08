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
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="static/teaching/", null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200)

    def __str__(self):
        return self.name

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
        return self.user.username + "'s rating"


class TeacherRating(Rating):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class SubjectRating(Rating):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Comment(models.Model):
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE)
    text = models.TextField()
    positive_score = models.IntegerField(default=0)
    negative_score = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT, null=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    teachers = models.ManyToManyField(Teacher, blank=True)

    def __str__(self):
        return self.user.username


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
