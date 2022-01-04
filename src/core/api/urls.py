from django.urls import path

from core.api import views as core_views

app_name = 'core'

urlpatterns = [
    # register views
    path('register/', core_views.RegisterView.as_view(), name='register'),

    # Version views
    path('create_new_version/<project>/', core_views.CreateNewVersionView.as_view(), name='new_version'),
    path('update_major/<project>/', core_views.UpdateMajorView.as_view(), name='update_major'),
    path('update_minor/<project>/', core_views.UpdateMinorView.as_view(), name='update_minor'),
    path('update_patch/<project>/', core_views.UpdatePatchView.as_view(), name='update_patch'),

    # Project views
    path('projects/', core_views.ProjectListView.as_view(), name='project_list'),
    path('create_project/', core_views.CreateProjectView.as_view(), name='create_project'),
]
