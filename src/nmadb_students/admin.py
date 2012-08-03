from django.contrib import admin
from django.utils.translation import ugettext as _

from nmadb_contacts import admin as contacts_admin
from nmadb_students import models
from nmadb_utils import admin as utils


class SchoolAdmin(utils.ModelAdmin):
    """ Administration for school.
    """

    list_display = (
            'id',
            'title',
            'school_type',
            'email',
            )

    list_filter = (
            'school_type',
            )

    search_fields = (
            'id',
            'title',
            'email',
            )

    sheet_mapping = (
            (_(u'ID'), ('id',)),
            (_(u'Title'), ('title',)),
            (_(u'Type'), ('get_school_type_display',)),
            (_(u'Email'), ('email',)),
            (_(u'Municipality'), ('municipality', 'title',)),
            (_(u'Municipality code'), ('municipality', 'code',)),
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

    sheet_mapping = contacts_admin.HumanAdmin.sheet_mapping + (
            (_(u'Class'), ('current_school_class',)),
            (_(u'School'), ('current_school',)),
            )

    inlines = contacts_admin.HumanAdmin.inlines + [
            StudyRelationInline,
            #ParentRelationInline,   FIXME: Why doesn't work?
            AlumniInline,
            SocialDisadvantageMarkInline,
            DisabilityMarkInline,
            ]


class StudyRelationAdmin(utils.ModelAdmin):
    """ Administration for study relations.
    """

    list_display = (
            'id',
            'student',
            'school',
            'entered',
            'finished',
            )

    search_fields = (
            'id',
            'student__first_name',
            'student__last_name',
            'student__old_last_name',
            'school__title',
            )


class AlumniAdmin(utils.ModelAdmin):
    """ Administration for alumnis.
    """

    list_display = (
            'id',
            'student',
            'university',
            'study_field',
            )

    search_fields = (
            'id',
            'student__first_name',
            'student__last_name',
            'student__old_last_name',
            'university',
            'study_field',
            )


class StudentMarkAdmin(utils.ModelAdmin):
    """ Administration for StudentMark.
    """

    list_display = (
            'id',
            'student',
            'start',
            'end',
            )

    list_filter = (
            'school_type',
            )

    search_fields = (
            'id',
            'student__first_name',
            'student__last_name',
            'student__old_last_name',
            )


class ParentRelationAdmin(utils.ModelAdmin):
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
admin.site.register(models.StudyRelation, StudyRelationAdmin)
admin.site.register(models.Alumni, AlumniAdmin)
admin.site.register(models.SocialDisadvantageMark, StudentMarkAdmin)
admin.site.register(models.DisabilityMark, StudentMarkAdmin)
