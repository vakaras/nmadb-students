# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Diploma.hours'
        db.alter_column('nmadb_students_diploma', 'hours', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2))

        # Changing field 'Diploma.tasks_solved'
        db.alter_column('nmadb_students_diploma', 'tasks_solved', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Diploma.hours'
        raise RuntimeError("Cannot reverse this migration. 'Diploma.hours' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Diploma.tasks_solved'
        raise RuntimeError("Cannot reverse this migration. 'Diploma.tasks_solved' and its values cannot be restored.")

    models = {
        'nmadb_contacts.address': {
            'Meta': {'ordering': "[u'municipality']", 'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'human': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_contacts.Human']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_contacts.Municipality']", 'null': 'True', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'nmadb_contacts.human': {
            'Meta': {'ordering': "[u'last_name', u'first_name']", 'object_name': 'Human'},
            'academic_degree': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django_db_utils.models.FirstNameField', [], {'max_length': '45'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_code': ('django_db_utils.models.IdentityCodeField', [], {'max_length': '11', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django_db_utils.models.LastNameField', [], {'max_length': '45'}),
            'main_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['nmadb_contacts.Address']"}),
            'old_last_name': ('django_db_utils.models.LastNameField', [], {'max_length': '45', 'blank': 'True'})
        },
        'nmadb_contacts.municipality': {
            'Meta': {'ordering': "[u'town', u'municipality_type']", 'object_name': 'Municipality'},
            'code': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'nmadb_students.alumni': {
            'Meta': {'object_name': 'Alumni'},
            'abilities': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'activity_fields': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_change_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'information_received_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'interest_level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nmadb_students.Student']", 'unique': 'True'}),
            'study_field': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'nmadb_students.diploma': {
            'Meta': {'object_name': 'Diploma'},
            'diploma_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'student': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nmadb_students.Student']", 'unique': 'True'}),
            'tasks_solved': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'nmadb_students.disabilitymark': {
            'Meta': {'object_name': 'DisabilityMark'},
            'disability': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_students.Student']"})
        },
        'nmadb_students.parentrelation': {
            'Meta': {'object_name': 'ParentRelation'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['nmadb_students.Student']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_contacts.Human']"}),
            'relation_type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'nmadb_students.school': {
            'Meta': {'ordering': "[u'title']", 'object_name': 'School'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_contacts.Municipality']", 'null': 'True', 'blank': 'True'}),
            'school_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'nmadb_students.socialdisadvantagemark': {
            'Meta': {'object_name': 'SocialDisadvantageMark'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_students.Student']"})
        },
        'nmadb_students.student': {
            'Meta': {'ordering': "[u'last_name', u'first_name']", 'object_name': 'Student', '_ormbases': ['nmadb_contacts.Human']},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'human_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['nmadb_contacts.Human']", 'unique': 'True', 'primary_key': 'True'}),
            'parents': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'children'", 'symmetrical': 'False', 'through': "orm['nmadb_students.ParentRelation']", 'to': "orm['nmadb_contacts.Human']"}),
            'school_class': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'school_year': ('django.db.models.fields.IntegerField', [], {}),
            'schools': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['nmadb_students.School']", 'through': "orm['nmadb_students.StudyRelation']", 'symmetrical': 'False'})
        },
        'nmadb_students.studyrelation': {
            'Meta': {'ordering': "[u'student', u'entered']", 'object_name': 'StudyRelation'},
            'entered': ('django.db.models.fields.DateField', [], {}),
            'finished': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_students.School']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_students.Student']"})
        }
    }

    complete_apps = ['nmadb_students']