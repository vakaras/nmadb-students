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


class StudyRelationInline(admin.TabularInline):
    """ Inline for school information.
    """

    model = models.StudyRelation
    extra = 0


class ParentRelationInline(admin.TabularInline):
    """ Inline for parent information.
    """

    model = models.ParentRelation
    extra = 0


class AlumniInline(admin.StackedInline):
    """ Inline administration for information about alumni.
    """

    model = models.Alumni
    extra = 0


class SocialDisadvantageMarkInline(admin.TabularInline):
    """ Inline administration for social disadvantage mark.
    """

    model = models.SocialDisadvantageMark
    extra = 0


class DisabilityMarkInline(admin.TabularInline):
    """ Inline administration for disability mark.
    """

    model = models.DisabilityMark
    extra = 0


class StudentAdmin(contacts_admin.HumanAdmin):
    """ Administration for student.
    """

    inlines = contacts_admin.HumanAdmin.inlines + [
            StudyRelationInline,
            #ParentRelationInline,   FIXME: Why doesn't work?
            AlumniInline,
            SocialDisadvantageMarkInline,
            DisabilityMarkInline,
            ]


class ParentRelationAdmin(admin.ModelAdmin):
    """ Administration for parent relation.
    """

    list_display = [
            'child',
            'parent',
            'relation_type',
            ]

    search_fields = [
            'child__first_name',
            'child__last_name',
            'child__old_last_name',
            'parent__first_name',
            'parent__last_name',
            'parent__old_last_name',
            ]


admin.site.register(models.School, SchoolAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.ParentRelation, ParentRelationAdmin)
