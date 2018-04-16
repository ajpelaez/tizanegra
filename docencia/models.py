from django.db import models


class Universidad(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    logo = models.ImageField(upload_to="static/", null=True, blank=True)
    web = models.CharField(max_length=200)


class Titulacion(models.Model):
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)


class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)
    titulacion = models.ForeignKey(Titulacion, on_delete=models.PROTECT)


class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="static/", null=True, blank=True)
    asignaturas = models.ForeignKey(Asignatura, on_delete=models.SET_NULL, null=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)
    email = models.EmailField(max_length=200)
