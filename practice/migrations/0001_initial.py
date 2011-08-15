# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Phrase'
        db.create_table('practice_phrase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('english', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('practice', ['Phrase'])

        # Adding model 'PhraseSet'
        db.create_table('practice_phraseset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('practice', ['PhraseSet'])

        # Adding M2M table for field phrases on 'PhraseSet'
        db.create_table('practice_phraseset_phrases', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('phraseset', models.ForeignKey(orm['practice.phraseset'], null=False)),
            ('phrase', models.ForeignKey(orm['practice.phrase'], null=False))
        ))
        db.create_unique('practice_phraseset_phrases', ['phraseset_id', 'phrase_id'])

        # Adding model 'Recording'
        db.create_table('practice_recording', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('phrase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['practice.Phrase'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('practice', ['Recording'])

        # Adding model 'Response'
        db.create_table('practice_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('giver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('recording', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['practice.Recording'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('practice', ['Response'])

        # Adding model 'ResponseFeedback'
        db.create_table('practice_responsefeedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['practice.Response'])),
            ('positive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reason', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
        ))
        db.send_create_signal('practice', ['ResponseFeedback'])

        # Adding model 'Conversation'
        db.create_table('practice_conversation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('practice', ['Conversation'])

        # Adding model 'Line'
        db.create_table('practice_line', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conversation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['practice.Conversation'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('interviewer_text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('speaker_text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('practice', ['Line'])

        # Adding model 'Attempt'
        db.create_table('practice_attempt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conversation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['practice.Conversation'])),
            ('started', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('practice', ['Attempt'])

        # Adding model 'LineRecording'
        db.create_table('practice_linerecording', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['practice.Attempt'])),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['practice.Line'])),
        ))
        db.send_create_signal('practice', ['LineRecording'])


    def backwards(self, orm):
        
        # Deleting model 'Phrase'
        db.delete_table('practice_phrase')

        # Deleting model 'PhraseSet'
        db.delete_table('practice_phraseset')

        # Removing M2M table for field phrases on 'PhraseSet'
        db.delete_table('practice_phraseset_phrases')

        # Deleting model 'Recording'
        db.delete_table('practice_recording')

        # Deleting model 'Response'
        db.delete_table('practice_response')

        # Deleting model 'ResponseFeedback'
        db.delete_table('practice_responsefeedback')

        # Deleting model 'Conversation'
        db.delete_table('practice_conversation')

        # Deleting model 'Line'
        db.delete_table('practice_line')

        # Deleting model 'Attempt'
        db.delete_table('practice_attempt')

        # Deleting model 'LineRecording'
        db.delete_table('practice_linerecording')


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
            'interviewer_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'speaker_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'practice.linerecording': {
            'Meta': {'object_name': 'LineRecording'},
            'attempt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Attempt']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['practice.Line']"})
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
