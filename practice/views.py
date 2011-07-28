from models import *
from django.shortcuts import render
from django import http
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
import logging
import pprint
import settings
import urllib


def response_url(response_id):
    return "/uploadedmedia/response" + str(response_id) + ".mp3"

def expert_url(phrase_id):
    return "/uploadedmedia/expert" + str(phrase_id) + ".mp3"

@login_required
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

    # Additional params we want passed through to uploading
    upload_params = "phrase_id=" + str(phrase.id)
    upload_params_encoded = urllib.quote_plus(upload_params)

    next_url = '?num=' + str(num + 1)
    return render(request,'practice.html',{
        'phrase_set':phrase_set,
        'last_one':last_one,
        'phrase':phrase,
        'next_url':next_url,
        'upload_params_encoded':upload_params_encoded,
        'expert_url':expert_url(phrase.id),
        'phrase_num':num,
        'phrases_in_set':len(phrases),
    })

@login_required
def sets(request):
    phrase_sets = PhraseSet.objects.all()

    phrase_set_objs = []
    for phrase_set in phrase_sets:
        recordings = Recording.objects.filter(
            user = request.user,
            phrase__phraseset = phrase_set)
        responses = Response.objects.filter(recording__in = recordings)

        status = 'untaken'
        if len(recordings) > 0:
            status = 'taken'
        if len(responses) > 0:
            status = 'responses'

        phrase_set_objs.append((phrase_set, recordings, responses,status))

    return render(request,'sets.html',{
        'phrase_sets':phrase_sets,
        'phrase_set_objs':phrase_set_objs,
    })

@login_required
def review(request):
    recordings = Recording.objects.filter(user = request.user)

    phrase_set = None
    if request.GET.get('set_id'):
        set_id = int(request.GET.get('set_id'))
        phrase_set = PhraseSet.objects.get(id=set_id)
        phrases = list(phrase_set.phrases.all())
        recordings = recordings.filter(phrase__in = phrases)


    recordingObjs = []
    for recording in recordings:
        media_url = settings.MEDIA_URL + "recording" + str(recording.id) + ".mp3"
        media_url_encoded = urllib.quote_plus(media_url)
        responses = Response.objects.filter(recording=recording).order_by('-created')
        responseObjs = [(response,response_url(response.id)) for response in responses]
        recordingObjs.append((
            recording,
            media_url_encoded,
            responseObjs,
            expert_url(recording.phrase.id),
        ))

    return render(request,'review.html',{
        'recordingObjs':recordingObjs,
        'phrase_set':phrase_set,
    })

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

        if request.GET.get('type',None) == "response":
                recording_id = request.GET.get('recording_id',None)
                if not recording_id:
                    raise Exception('No recording id')
                recording = Recording.objects.get(id=int(recording_id))

                response = Response(
                    giver=request.user,
                    recording=recording,
                )
                response.save()

                filename = "response" + str(response.id) + ".mp3"
                default_storage.save(filename,request.FILES['fileupload'])
        else:
            # Validate phrase exists
            phrase_id = request.GET.get('phrase_id')
            if not phrase_id:
                raise Exception('no phrase id')

            try:
                phrase = Phrase.objects.get(id=int(phrase_id))
            except Phrase.DoesNotExist:
                raise Exception('phrase with id does not exist: ' + str(phrase_id))

            if request.GET.get('type',None) == "expert":
                filename = "expert" + str(phrase.id) + ".mp3"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
                default_storage.save(filename,request.FILES['fileupload'])
            else:
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

def expert_recording(request,phrase_id):
    try:
        phrase = Phrase.objects.get(id=int(phrase_id))
    except Phrase.DoesNotExist:
        raise Exception('phrase with id does not exist: ' + str(phrase_id))

    upload_params = "phrase_id=" + str(phrase.id) + "&type=expert"
    upload_params_encoded = urllib.quote_plus(upload_params)


    # Expert info
    filename = "expert" + str(phrase.id) + ".mp3"
    exists = default_storage.exists(filename)
    created_time = None
    size = None
    if exists:
        created_time = default_storage.created_time(filename)
        size = default_storage.size(filename)

    return render(request,'expert_recording.html',{
        'phrase':phrase,
        'upload_params_encoded':upload_params_encoded,
        'expert_url':expert_url(phrase_id),

        'filename':filename,
        'exists':exists,
        'created_time':created_time,
        'size':size,
    })

@login_required
def give_response(request):
    recordings = Recording.objects.order_by('-created')

    recordingObjs = []
    for recording in recordings:
        media_url = settings.MEDIA_URL + "recording" + str(recording.id) + ".mp3"
        media_url_encoded = urllib.quote_plus(media_url)
        responses = Response.objects.filter(recording=recording)
        responseObjs = [(response,response_url(response.id)) for response in responses]

        # Additional params we want passed through to uploading
        upload_params = "type=response&recording_id=" + str(recording.id)
        upload_params_encoded = urllib.quote_plus(upload_params)

        recordingObjs.append((
            recording,
            media_url_encoded,
            responseObjs,
            expert_url(recording.phrase.id),
            upload_params_encoded,
        ))



    return render(request,'give_response.html',{
        'recordingObjs':recordingObjs,
    })
