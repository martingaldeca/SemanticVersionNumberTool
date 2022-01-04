from django.contrib import admin

from core.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('id', 'uuid', 'name', 'repository')
    list_display = ('id', 'uuid', 'name', 'repository')
