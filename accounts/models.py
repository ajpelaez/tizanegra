from django.db import models
from django.contrib.auth.models import User
from teaching.models import University, Subject, Teacher, Degree
from django.db.models.signals import post_save
from django.dispatch import receiver


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True)
    degree = models.ForeignKey(Degree, on_delete=models.PROTECT, null=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    teachers = models.ManyToManyField(Teacher, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.studentprofile.save()