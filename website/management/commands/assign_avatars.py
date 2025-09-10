from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from website.models import UserProfile, AVATAR_CHOICES
import random


class Command(BaseCommand):
    help = "Assign random avatars to users missing a profile/avatar"

    def handle(self, *args, **options):
        created = 0
        updated = 0
        for u in User.objects.all():
            profile, was_created = UserProfile.objects.get_or_create(user=u)
            if was_created:
                profile.avatar = random.choice(AVATAR_CHOICES)
                profile.save(update_fields=["avatar"])
                created += 1
            elif not profile.avatar:
                profile.avatar = random.choice(AVATAR_CHOICES)
                profile.save(update_fields=["avatar"])
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Profiles created: {created}, avatars set: {created + updated}"))

