from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Project, TimeStampedUUIDModel


class Version(TimeStampedUUIDModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project_versions', db_index=True
    )
    patch = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_('Patch'),
        help_text=_('Patch updates are interchangeable, meaning consumers can upgrade or downgrade freely.')
    )
    minor = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_('Minor'),
        help_text=_('Minor updates are backwards compatible, meaning consumers can upgrade freely.')
    )
    major = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_('Major'),
        help_text=_(
            'Major updates are non-compatible, meaning consumers can not upgrade without changing their software '
            'where applicable.'
        )
    )
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name='authored_versions', db_index=True
    )

    class Meta:
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')
        unique_together = [('project', 'major', 'minor', 'patch')]

    @property
    def formatted(self):
        return f'{self.major}.{self.minor}.{self.patch}'

    def __str__(self):
        return f'{self.formatted}- {self.author} - {self.uuid.hex}'

    def __repr__(self):
        return str(self)

    def next_version(self, update_type, author: User = None) -> 'Version':
        match update_type:
            case 'major':
                return Version.objects.create(
                    major=self.major + 1,
                    minor=0,
                    patch=0,
                    project=self.project,
                    author=author
                )
            case 'minor':
                return Version.objects.create(
                    major=self.major,
                    minor=self.minor + 1,
                    patch=0,
                    project=self.project,
                    author=author
                )
            case 'patch':
                return Version.objects.create(
                    major=self.major,
                    minor=self.minor,
                    patch=self.patch + 1,
                    project=self.project,
                    author=author
                )
            case _:
                raise ValueError(f'{update_type} is not a valid update type')

    def to_json(self):
        value = {
            'major': self.major,
            'minor': self.minor,
            'patch': self.patch,
            'formatted': self.formatted,
        }
        if self.author:
            value['author'] = {
                'username': self.author.username,
                'github': self.author.profile.github,
            }
        return value
