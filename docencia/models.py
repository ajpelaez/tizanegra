from django.db import models


class Universidad(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    logo = models.ImageField(upload_to="static/", null=True, blank=True)
    web = models.SlugField(max_length=200)

    class Meta:
        verbose_name_plural = "Universidades"


class Titulacion(models.Model):
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Titulaciones"


class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)
    titulacion = models.ForeignKey(Titulacion, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Asignaturas"


class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="static/", null=True, blank=True)
    asignaturas = models.ManyToManyField(Asignatura, null=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)
    email = models.EmailField(max_length=200)

    class Meta:
        verbose_name_plural = "Profesores"
