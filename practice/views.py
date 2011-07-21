from models import *
from django.shortcuts import render
from django import http
from django.core.files.storage import default_storage
import logging
import pprint


def practice(request,phrase_set_id):
    phrase_set = PhraseSet.objects.get(id=int(phrase_set_id))
    phrases = phrase_set.phrases.all()

    # Post-quiz
    num = int(request.GET.get('num',1))
    if num > len(phrases):
        raise Exception('finished')

    last_one = num == len(phrases)

    # Grab relevant phrase
    phrase = phrases[num - 1]

    next_url = '?num=' + str(num + 1)
    return render(request,'practice.html',{
        'phrase_set':phrase_set,
        'last_one':last_one,
        'phrase':phrase,
        'next_url':next_url,
    })

def sets(request):
    phrase_sets = PhraseSet.objects.all()
    return render(request,'sets.html',{
        'phrase_sets':phrase_sets,
    })

def review(request):
    return render(request,'review.html',{})

def testrecording(request):
    return render(request,'testrecording.html',{})

def submit_recording(request):
    if request.method == 'POST':
        # Debug output
        logging.warn('user authenticated: ' + str(request.user.is_authenticated()))
        pprint.pprint(request.POST)
        logging.warn('encoding: ' + str(request.encoding))
        logging.warn('number files: ' + str(len(request.FILES)))
        pprint.pprint(request.FILES)
        logging.warn('has fileupload: ' + str("fileupload" in request.FILES))

        # Validation
        if "fileupload" not in request.FILES:
            raise Exception("Server Error: not file upload")
        phrase_id = request.POST.get('phrase_id')
        if not phrase_id:
            raise Exception('no phrase id')

        try:
            phrase = Phrase.objects.get(id=int(phrase_id))
        except Phrase.DoesNotExist:
            raise Exception('phrase with id does not exist: ' + str(phrase_id))

        # Create the DB object
        recording = Recording(
            user = request.user,
            phrase = phrase
        )
        recording.save()

        # Save the file to the uploaded folder
        filename = "recording" + str(recording.id) + ".mp3"
        default_storage.save(filename,request.FILES['fileupload'])

    else:
        pass
    return http.HttpResponse("<html><body><form method='POST' enctype='multipart/form-data'><input name='phrase_id'><input type='file' name='fileupload'><input type='submit' name='submit'></form></body></html>")

