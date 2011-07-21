from django.db import models

class Phrase(models.Model):
    english = models.CharField(max_length=300)

class PhraseSet(models.Model):
    title = models.CharField(max_length=300)
    phrases = models.ManyToManyField(Phrase)


