from django.contrib import admin

from backend.settings import PRODUCTION
from . import project_admin
from . import user_profile_admin
from . import version_admin

if PRODUCTION:
    # Disable delete_selected action globally
    admin.site.disable_action('delete_selected')
