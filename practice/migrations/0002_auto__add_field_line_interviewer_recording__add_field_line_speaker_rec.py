# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Line.interviewer_recording'
        db.add_column('practice_line', 'interviewer_recording', self.gf('django.db.models.fields.files.FileField')(default=1, max_length=100, blank=True), keep_default=False)

        # Adding field 'Line.speaker_recording'
        db.add_column('practice_line', 'speaker_recording', self.gf('django.db.models.fields.files.FileField')(default=1, max_length=100, blank=True), keep_default=False)

        # Adding field 'LineRecording.response_recording'
        db.add_column('practice_linerecording', 'response_recording', self.gf('django.db.models.fields.files.FileField')(default=1, max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Line.interviewer_recording'
        db.delete_column('practice_line', 'interviewer_recording')

        # Deleting field 'Line.speaker_recording'
        db.delete_column('practice_line', 'speaker_recording')

        # Deleting field 'LineRecording.response_recording'
        db.delete_column('practice_linerecording', 'response_recording')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'practice.attempt': {
            'Meta': {'object_name': 'Attempt'},
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Conversation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'practice.conversation': {
            'Meta': {'object_name': 'Conversation'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'practice.line': {
            'Meta': {'object_name': 'Line'},
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Conversation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviewer_recording': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'interviewer_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'speaker_recording': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'speaker_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'practice.linerecording': {
            'Meta': {'object_name': 'LineRecording'},
            'attempt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Attempt']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Line']"}),
            'response_recording': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'practice.phrase': {
            'Meta': {'object_name': 'Phrase'},
            'english': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'practice.phraseset': {
            'Meta': {'object_name': 'PhraseSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phrases': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['practice.Phrase']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'practice.recording': {
            'Meta': {'object_name': 'Recording'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phrase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Phrase']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'practice.response': {
            'Meta': {'object_name': 'Response'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recording': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Recording']"})
        },
        'practice.responsefeedback': {
            'Meta': {'object_name': 'ResponseFeedback'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'positive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Response']"})
        }
    }

    complete_apps = ['practice']
