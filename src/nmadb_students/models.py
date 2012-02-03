import datetime

from django.db import models
from django.core import validators
from django.utils.translation import ugettext as _

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
            )

    school_type = models.PositiveSmallIntegerField(
            choices=SCHOOL_TYPES,
            blank=True,
            null=True,
            )

    email = models.EmailField(
            max_length=128,
            unique=True,
            blank=True,
            null=True,
            )

    municipality = models.ForeignKey(
            Municipality,
            blank=True,
            null=True,
            )

    class Meta(object):
        ordering = [u'title',]

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


class StudyRelation(models.Model):
    """ Relationship between student and school.
    """

    student = models.ForeignKey(
            Student,
            )

    school = models.ForeignKey(
            School,
            )

    entered = models.DateField(
            )

    finished = models.DateField(
            blank=True,
            null=True,
            )

    class Meta(object):
        ordering = [u'student', u'entered',]

    def __unicode__(self):
        return u'{0.school} ({0.entered}; {0.finished})'.format(self)


class Alumni(Student):
    """ Information about alumni.
    """

    university = models.CharField(
            max_length=128,
            blank=True,
            null=True,
            )

    study_field = models.CharField(
            max_length=64,
            blank=True,
            null=True,
            )

    notes = models.TextField(
            blank=True,
            null=True,
            )


class StudentMark(models.Model):
    """ Mark student with some mark.
    """

    student = models.ForeignKey(
            Student,
            )

    start = models.DateField()

    end = models.DateField(
            blank=True,
            null=True,
            )

    def __unicode__(self):
        return unicode(self.student)

    class Meta(object):
        abstract = True


class SocialDisadvantageMark(StudentMark):
    """ Mark student as socially disadvantaged.
    """


class DisabilityMark(StudentMark):
    """ Mark student as having disability.
    """

    disability = models.CharField(
            max_length=128,
            )


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
            )

    parent = models.ForeignKey(
            Human,
            )

    relation_type = models.CharField(
            max_length=2,
            choices=RELATION_TYPE,
            )

    def __unicode__(self):
        return u'{0.parent} -> {0.student}'.format(self)
