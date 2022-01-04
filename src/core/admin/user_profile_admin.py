from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from jet.admin import CompactInline

from core.models import UserProfile

try:
    admin.site.unregister(User)
except NotRegistered:
    pass


class ProfileInline(CompactInline):
    model = UserProfile
    max_num = 1
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    search_fields = ('id', 'profile__uuid', 'username', 'email')
    inlines = (ProfileInline,)
    list_display = (
        'id', 'get_uuid', 'username', 'email', 'first_name', 'last_name', 'get_github',
    )

    def get_uuid(self, obj):
        return obj.profile.uuid.hex

    get_uuid.short_description = _('UUID')

    def get_github(self, obj):
        return obj.profile.github

    get_github.short_description = _('Github')
