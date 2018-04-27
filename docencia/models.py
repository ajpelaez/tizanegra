from django.db import models


class Universidad(models.Model):
    siglas = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="static/", null=True, blank=True)
    web = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Universidades"


class Titulacion(models.Model):
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Titulaciones"


class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)
    titulaciones = models.ManyToManyField(Titulacion)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Asignaturas"


class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="static/", null=True, blank=True)
    asignaturas = models.ManyToManyField(Asignatura)
    universidad = models.ForeignKey(Universidad, on_delete=models.PROTECT)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Profesores"
