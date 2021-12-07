from django.db.models.signals import post_save
from django.dispatch import receiver

from website.apps.profiles.models import Profile
from .models import User

@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # 注意, 我们在此处检测`created`, 我们期望只在第一次创建用户时创建`Profile`
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)