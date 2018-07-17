from django.db import models


class University(models.Model):
    acronym = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="static/", null=True, blank=True)
    web = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Degrees(models.Model):
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey(University, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre


class Subjects(models.Model):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.PROTECT)
    degrees = models.ManyToManyField(Degrees)

    def __str__(self):
        return self.name


class Teachers(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="static/", null=True, blank=True)
    subjects = models.ManyToManyField(Subjects)
    universities = models.ForeignKey(University, on_delete=models.PROTECT)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name

