import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.models.abstract import TimeStampedUUIDModel

logger = logging.getLogger(__name__)


class UserProfile(TimeStampedUUIDModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile'
    )
    github = models.URLField(
        max_length=200,
        null=True, blank=True,
        help_text=_('Github of the user'),
        verbose_name=_('Github')
    )


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance: User, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.save()
    else:
        instance.profile.save()


def get_github(self):
    return f'{self.profile.github}'


User.add_to_class("__str__", get_github)
