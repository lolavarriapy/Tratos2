from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserExtend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primerAcceso = models.BooleanField(default=True)
    
    @receiver(post_save, sender=User)
    def create_user_extend(sender, instance, created, **kwargs):
        if created:
            UserExtend.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_extend(sender, instance, **kwargs):
        instance.userextend.save()