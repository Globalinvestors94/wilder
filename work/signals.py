from .models import Referal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_user_referal_code(sender, instance, created, *args, **kwargs):
	if created:
		Referal.objects.create(user=instance)
