from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from docencia.models import Universidad, Asignatura, Profesor


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(Universidad, on_delete=models.PROTECT, null=True)
    subjects = models.ManyToManyField(Asignatura)
    teachers = models.ManyToManyField(Profesor)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Perfil Estudiantes"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#    instance.studentprofile.save()
