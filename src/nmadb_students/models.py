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


class Alumni(models.Model):
    """ Information about alumni.
    """

    student = models.OneToOneField(
            Student,
            verbose_name=_(u'student'),
            )

    university = models.CharField(
            max_length=128,
            blank=True,
            null=True,
            verbose_name=_(u'university'),
            )

    study_field = models.CharField(
            max_length=64,
            blank=True,
            null=True,
            verbose_name=_(u'study field'),
            )

    notes = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'notes'),
            )

    class Meta(object):
        verbose_name=_(u'alumni')
        verbose_name_plural=_(u'alumnis')


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
