from django.contrib import admin
from django.utils.translation import ugettext as _

from django_db_utils import utils
from nmadb_contacts import admin as contacts_admin
from nmadb_students import models


class SchoolAdmin(admin.ModelAdmin):
    """ Administration for school.
    """

    list_display = (
            'id',
            'title',
            'school_type',
            'email',
            'municipality',
            )

    list_filter = (
            'school_type',
            )

    search_fields = (
            'id',
            'title',
            'email',
            )


class StudentAdmin(contacts_admin.HumanAdmin):
    """ Administration for student.
    """


admin.site.register(models.School, SchoolAdmin)
admin.site.register(models.Student, StudentAdmin)
