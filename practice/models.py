from django.db import models
from django.contrib.auth.models import User

class Phrase(models.Model):
    english = models.CharField(max_length=300)

    def __str__(self):
        return self.english[:20]

class PhraseSet(models.Model):
    title = models.CharField(max_length=300)
    phrases = models.ManyToManyField(Phrase)

    def __str__(self):
        return self.title

class Recording(models.Model):
    user = models.ForeignKey('auth.User')
    phrase = models.ForeignKey('Phrase')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + str(self.phrase)

class Response(models.Model):
    giver = models.ForeignKey('auth.User')
    recording = models.ForeignKey('Recording')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.giver.username + " to " + self.recording.user.username + " for \"" + str(self.recording.phrase) + "\""

class ResponseFeedback(models.Model):
    response = models.ForeignKey('Response')
    positive = models.BooleanField()
    reason = models.CharField(max_length=300,default="")





class Conversation(models.Model):
    title = models.CharField(max_length = 300)
    description = models.CharField(max_length=1000)
    thumbnail = models.ImageField(upload_to='conversation_thumbnails')

    def __str__(self):
        return self.title

class Line(models.Model):
    conversation = models.ForeignKey('conversation')
    order = models.IntegerField()

    interviewer_text = models.CharField(max_length = 1000)
    speaker_text = models.CharField(max_length = 1000)

    def __str__(self):
        return "%s #%s" % (self.conversation.title,self.order)

class Attempt(models.Model):
    conversation = models.ForeignKey('conversation')
    started = models.DateTimeField(auto_now_add = True)
    is_finished = models.BooleanField(default=False)

class LineRecording(models.Model):
    attempt = models.ForeignKey('attempt')
    line = models.ForeignKey('line')

