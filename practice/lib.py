from models import *
from django.db.models.signals import pre_delete 
from django.dispatch import receiver
from django.core.files.storage import default_storage
import settings

def response_url(response_id):
    return "/uploadedmedia/response" + str(response_id) + ".mp3"

def response_filename(response):
    return "response" + str(response.id) + ".mp3"

def expert_url(phrase_id):
    return "/uploadedmedia/expert" + str(phrase_id) + ".mp3"

def expert_filename(phrase):
    return "expert" + str(phrase.id) + ".mp3"

def recording_url(recording_id):
    return "/uploadedmedia/recording" + str(recording_id) + ".mp3"

def recording_filename(recording):
    return "recording" + str(recording.id) + ".mp3"


@receiver(pre_delete, sender=Phrase)
def my_callback(sender, instance, **kwargs):
    expert_mp3 = expert_filename(instance)
    if default_storage.exists(expert_mp3):
        default_storage.delete(expert_mp3)



