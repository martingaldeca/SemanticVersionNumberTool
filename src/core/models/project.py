from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedUUIDModel


class Project(TimeStampedUUIDModel):
    name = models.CharField(
        max_length=256, null=False, blank=False,
        verbose_name=_('Name'),
        help_text=_('Name of the project.'),
        db_index=True
    )
    repository = models.URLField(
        max_length=200,
        null=True, blank=True,
        verbose_name=_('Repository'),
        help_text=_('Repository of the project in case of exists'),
    )

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return f'{self.name} - {self.last_version}'

    def __repr__(self):
        return str(self)

    @property
    def last_version(self):
        from core.models import Version
        return Version.objects.filter(project=self).last()


@receiver(post_save, sender=Project)
def create_first_version(sender, instance: Project, created, **kwargs):
    from core.models import Version
    if created:
        Version.objects.create(major=0, minor=0, patch=0, project=instance)
