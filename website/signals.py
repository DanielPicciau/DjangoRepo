import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, AVATAR_CHOICES


@receiver(post_save, sender=User)
def ensure_profile_with_avatar(sender, instance: User, created, **kwargs):
    # Create a profile on user creation and assign a random avatar
    if created:
        avatar = random.choice(AVATAR_CHOICES)
        UserProfile.objects.create(user=instance, avatar=avatar)
    else:
        # Ensure a profile exists for older users
        try:
            profile = instance.profile
            if not profile.avatar:
                profile.avatar = random.choice(AVATAR_CHOICES)
                profile.save(update_fields=["avatar"])
        except UserProfile.DoesNotExist:
            avatar = random.choice(AVATAR_CHOICES)
            UserProfile.objects.create(user=instance, avatar=avatar)

