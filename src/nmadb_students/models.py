import datetime

from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from nmadb_contacts.models import Municipality, Human


class School(models.Model):
    """ Information about school.

    School types retrieved from `AIKOS
    <http://www.aikos.smm.lt/aikos/svietimo_ir_mokslo_institucijos.htm>`_
    """

    SCHOOL_TYPES = (
            (1, _(u'primary')),
            (2, _(u'basic')),
            (3, _(u'secondary')),
            (4, _(u'gymnasium')),
            (5, _(u'progymnasium')),
            )

    title = models.CharField(
            max_length=80,
            unique=True,
            verbose_name=_(u'title'),
            )

    school_type = models.PositiveSmallIntegerField(
            choices=SCHOOL_TYPES,
            blank=True,
            null=True,
            verbose_name=_(u'type'),
            )

    email = models.EmailField(
            max_length=128,
            unique=True,
            blank=True,
            null=True,
            verbose_name=_(u'email'),
            )

    municipality = models.ForeignKey(
            Municipality,
            blank=True,
            null=True,
            verbose_name=_(u'municipality'),
            )

    class Meta(object):
        ordering = [u'title',]
        verbose_name=_(u'school')
        verbose_name_plural=_(u'schools')

    def __unicode__(self):
        return unicode(self.title)


class Student(Human):
    """ Information about student.
    """

    school_class = models.PositiveSmallIntegerField(
            validators=[
                validators.MinValueValidator(6),
                validators.MaxValueValidator(12),
                ],
            verbose_name=_(u'class'),
            )

    school_year = models.IntegerField(
            validators=[
                validators.MinValueValidator(2005),
                validators.MaxValueValidator(2015),
                ],
            verbose_name=_(u'class update year'),
            help_text=_(
                u'This field value shows, at which year January 3 day '
                u'student was in school_class.'
                ),
            )

    comment = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'comment'),
            )

    schools = models.ManyToManyField(
            School,
            through='StudyRelation',
            )

    parents = models.ManyToManyField(
            Human,
            through='ParentRelation',
            related_name='children',
            )

    def current_school_class(self):
        """ Returns current school class or 13 if finished.
        """
        today = datetime.date.today()
        school_class = self.school_class + today.year - self.school_year
        if today.month >= 9:
            school_class += 1
        if school_class > 12:
            return 13
        else:
            return school_class
    current_school_class.short_description = _(u'current class')

    def current_school(self):
        """ Returns current school.
        """
        study = StudyRelation.objects.filter(
                student=self).order_by('entered')[0]
        return study.school
    current_school.short_description = _(u'current school')

    def change_school(self, school, date=None):
        """ Marks, that student from ``date`` study in ``school``.

        .. note::
            Automatically saves changes.

        ``date`` defaults to ``today()``. If student already studies in
        some school, than marks, that he had finished it day before
        ``date``.
        """
        if date is None:
            date = datetime.date.today()
        try:
            old_study = StudyRelation.objects.filter(
                    student=self).order_by('entered')[0]
        except IndexError:
            pass
        else:
            if not old_study.finished:
                old_study.finished = date - datetime.timedelta(1)
                old_study.save()
        study = StudyRelation()
        study.student = self
        study.school = school
        study.entered = date
        study.save()

    class Meta(object):
        verbose_name=_(u'student')
        verbose_name_plural=_(u'students')


class StudyRelation(models.Model):
    """ Relationship between student and school.
    """

    student = models.ForeignKey(
            Student,
            verbose_name=_(u'student'),
            )

    school = models.ForeignKey(
            School,
            verbose_name=_(u'school'),
            )

    entered = models.DateField(
            verbose_name=_(u'entered'),
            )

    finished = models.DateField(
            blank=True,
            null=True,
            verbose_name=_(u'finished'),
            )

    class Meta(object):
        ordering = [u'student', u'entered',]
        verbose_name=_(u'study relation')
        verbose_name_plural=_(u'study relations')

    def __unicode__(self):
        return u'{0.school} ({0.entered}; {0.finished})'.format(self)


# FIXME: Diploma should belong to academic, not student.
class Diploma(models.Model):
    """ Information about the diploma that the student has received,
    when he finished, if any.
    """

    DIPLOMA_TYPE = (
            (u'N', _(u'nothing')),
            (u'P', _(u'certificate')),
            (u'D', _(u'diploma')),
            (u'DP', _(u'diploma with honour')),
            )

    student = models.OneToOneField(
            Student,
            verbose_name=_(u'student'),
            )

    tasks_solved = models.PositiveSmallIntegerField(
            blank=True,
            null=True,
            verbose_name=_(u'how many tasks solved'),
            )

    hours = models.DecimalField(
            blank=True,
            null=True,
            max_digits=6,
            decimal_places=2,
            verbose_name=_(u'hours'),
            )

    diploma_type = models.CharField(
            max_length=3,
            choices=DIPLOMA_TYPE,
            verbose_name=_(u'type'),
            )

    number = models.PositiveSmallIntegerField(
            verbose_name=_(u'number'),
            )

    class Meta(object):
        verbose_name=_(u'diploma')
        verbose_name_plural=_(u'diplomas')


class Alumni(models.Model):
    """ Information about alumni.
    """

    INTEREST_LEVEL = (
            # Not tried to contact.
            ( 0, _(u'not tried to contact')),
            # Tried to contact, no response.
            (11, _(u'no response')),
            # Tried to contact, responded.
            (21, _(u'not interested')),
            (22, _(u'friend')),
            (23, _(u'helpmate')),
            (24, _(u'regular helpmate')),
            )

    student = models.OneToOneField(
            Student,
            verbose_name=_(u'student'),
            )

    activity_fields = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'fields'),
            help_text=_(
                u'Alumni reported that he can help in these activity '
                u'fields.'
                ),
            )

    interest_level = models.PositiveSmallIntegerField(
            blank=True,
            null=True,
            choices=INTEREST_LEVEL,
            verbose_name=_(u'interest level'),
            )

    abilities = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'abilities'),
            help_text=_(u'Main abilities and interests.')
            )

    university = models.CharField(
            max_length=128,
            blank=True,
            null=True,
            verbose_name=_(u'university'),
            help_text=_(u'Or work place.'),
            )

    study_field = models.CharField(
            max_length=64,
            blank=True,
            null=True,
            verbose_name=_(u'study field'),
            help_text=_(u'Or employment field.'),
            )

    info_change_year = models.IntegerField(
            blank=True,
            null=True,
            verbose_name=_(u'info change year'),
            help_text=_(
                u'Year when the information about studies '
                u'will become invalid.'
                ),
            )

    notes = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'notes'),
            )

    information_received_timestamp = models.DateTimeField(
            blank=True,
            null=True,
            verbose_name=_(u'information received timestamp'),
            )

    class Meta(object):
        verbose_name=_(u'alumni')
        verbose_name_plural=_(u'alumnis')

    def contactable(self):
        """ If the alumni agreed to receive information.
        """
        return self.interest_level >= 22;


class StudentMark(models.Model):
    """ Mark student with some mark.
    """

    student = models.ForeignKey(
            Student,
            verbose_name=_(u'student'),
            )

    start = models.DateField(
            verbose_name=_(u'start'),
            )

    end = models.DateField(
            blank=True,
            null=True,
            verbose_name=_(u'end'),
            )

    def __unicode__(self):
        return unicode(self.student)

    class Meta(object):
        abstract = True


class SocialDisadvantageMark(StudentMark):
    """ Mark student as socially disadvantaged.
    """

    class Meta(object):
        verbose_name=_(u'social disadvantage mark')
        verbose_name_plural=_(u'social disadvantage marks')


class DisabilityMark(StudentMark):
    """ Mark student as having disability.
    """

    disability = models.CharField(
            max_length=128,
            verbose_name=_(u'disability'),
            )

    class Meta(object):
        verbose_name=_(u'disability mark')
        verbose_name_plural=_(u'disability marks')


class ParentRelation(models.Model):
    """ Relationship between student and his parent.
    """

    RELATION_TYPE = (
            (u'P', _(u'parent')),
            (u'T', _(u'tutor')),
            )

    child = models.ForeignKey(
            Student,
            related_name='+',
            verbose_name=_(u'child'),
            )

    parent = models.ForeignKey(
            Human,
            verbose_name=_(u'parent'),
            )

    relation_type = models.CharField(
            max_length=2,
            choices=RELATION_TYPE,
            verbose_name=_(u'type'),
            )

    def __unicode__(self):
        return u'{0.parent} -> {0.child}'.format(self)

    class Meta(object):
        verbose_name=_(u'parent relation')
        verbose_name_plural=_(u'parent relations')
