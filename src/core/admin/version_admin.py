from django.contrib import admin

from core.models import Version


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    search_fields = ('id', 'uuid', 'project', 'major', 'minor', 'patch', 'author')
    list_display = ('id', 'uuid', 'project', 'major', 'minor', 'patch', 'author')
    raw_id_fields = ('author', 'project')
