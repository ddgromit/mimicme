from models import *
from django.shortcuts import render
from django import http
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
import logging
import pprint
import settings
import urllib
from practice import lib


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

    # Precent bar
    phrase_percent = max(float(num - 1) / len(phrases)*100,2)

    next_url = '?num=' + str(num + 1)
    return render(request,'practice.html',{
        'phrase_set':phrase_set,
        'last_one':last_one,
        'phrase':phrase,
        'next_url':next_url,
        'upload_params_encoded':upload_params_encoded,
        'expert_url':lib.expert_url(phrase.id),
        'phrase_num':num,
        'phrases_in_set':len(phrases),
        'phrase_percent':phrase_percent,
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
        media_url = lib.recording_url(recording.id)
        media_url_encoded = urllib.quote_plus(media_url)
        responses = Response.objects.filter(recording=recording).order_by('-created')
        responseObjs = [(response,lib.response_url(response.id)) for response in responses]

        # Additional params we want passed through to uploading
        upload_params = "phrase_id=" + str(recording.phrase.id)
        upload_params_encoded = urllib.quote_plus(upload_params)

        recordingObjs.append((
            recording,
            media_url_encoded,
            responseObjs,
            lib.expert_url(recording.phrase.id),
            upload_params_encoded,
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
        elif request.GET.get('type',None) == 'line_interviewer':
            line_id = request.GET.get('line_id',None)
            line = Line.objects.get(id=int(line_id))
            line.interviewer_recording = request.FILES['fileupload']
            line.save()
        elif request.GET.get('type',None) == 'line_speaker':
            line_id = request.GET.get('line_id',None)
            line = Line.objects.get(id=int(line_id))
            line.speaker_recording = request.FILES['fileupload']
            line.save()
        elif request.GET.get('type',None) == 'line_response':
            line_id = request.GET.get('line_id',None)
            line = Line.objects.get(id=int(line_id))
            attempt_id = request.GET.get('attempt_id',None)
            attempt = Attempt.objects.get(id=int(attempt_id))
            
            line_recording = LineRecording(
                line=line,
                attempt=attempt,
                response_recording = request.FILES['fileupload'],
            )
            line_recording.save()
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
        'expert_url':lib.expert_url(phrase_id),

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
        media_url = lib.recording_url(recording.id)
        media_url_encoded = urllib.quote_plus(media_url)
        responses = Response.objects.filter(recording=recording)
        responseObjs = [(response,lib.response_url(response.id)) for response in responses]

        # Additional params we want passed through to uploading
        upload_params = "type=response&recording_id=" + str(recording.id)
        upload_params_encoded = urllib.quote_plus(upload_params)

        recordingObjs.append((
            recording,
            media_url_encoded,
            responseObjs,
            lib.expert_url(recording.phrase.id),
            upload_params_encoded,
        ))



    return render(request,'give_response.html',{
        'recordingObjs':recordingObjs,
    })


def finished(request):
    return render(request,'finished.html', {
        'set_id':request.GET.get('set_id','unknown')
    })


def response_feedback_handler(request):
    response_id = int(request.POST.get('response_id'))
    positive = bool(int(request.POST.get('positive')))
    reason = request.POST.get('reason','')

    response = Response.objects.get(id=response_id)

    response_feedback = lib.give_response_feedback(
        response = response,
        positive = positive,
        reason = reason,
    )

    return http.HttpResponse("ok " + str(response_feedback.id))




@login_required
def conversations_handler(request):
    conversations = Conversation.objects.all()
    attempts = Attempt.objects.all().order_by('-started')

    return render(request,'convosets.html',{
        'conversations':conversations,
        'attempts':attempts,
    })

@login_required
def start_conversation_handler(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)

    # Create an attempt to track progress
    attempt = Attempt(
        conversation = conversation,
        user = request.user,
    )
    attempt.save()

    # Build the starting url
    next_url = "/practicing/%s/1/" % attempt.id

    # Go there
    return http.HttpResponseRedirect(next_url)

@login_required
def practicing_handler(request,attempt_id,order):
    order = int(order)
    attempt = Attempt.objects.get(id=attempt_id)

    try:
        line = Line.objects.get(
            conversation = attempt.conversation,
            order = order,
        )
    except Line.DoesNotExist:
        # Finished
        attempt.is_finished = True
        attempt.save()
        return render(request,'convo_finished.html',{
            'conversation':attempt.conversation,
            'attempt':attempt,
        })


    # Check if a recording was already made here
    try:
        line_recording = LineRecording.objects.get(
            line = line,
            attempt = attempt,
        )
        your_recording_url = settings.MEDIA_URL + str(line_recording.response_recording)
        feedbacks = []
    except LineRecording.DoesNotExist:
        line_recording = None
        your_recording_url = None
        feedbacks = []



    next_line_url = "/practicing/%s/%s/" % (attempt.id, int(order) + 1)

    # For the players and recorders
    interviewer_recording_url = settings.MEDIA_URL + str(line.interviewer_recording) if line.interviewer_recording else ""
    speaker_recording_url = settings.MEDIA_URL + str(line.speaker_recording) if line.speaker_recording else ""
    response_upload_params = "type=line_response&line_id=%s&attempt_id=%s" \
            % (line.id, attempt.id)

    num_lines = Line.objects.filter(conversation=attempt.conversation).count()
    line_numbers = xrange(1,num_lines+1)
    annotated_line_numbers = zip(line_numbers,[line_number == order for line_number in line_numbers])
    return render(request,'convo.html', {
        'conversation':attempt.conversation,
        'attempt':attempt,
        'line':line,
        'next_line_url':next_line_url,

        'annotated_line_numbers':annotated_line_numbers,

        'interviewer_recording_url':interviewer_recording_url,
        'speaker_recording_url':speaker_recording_url,
        'response_upload_params':urllib.quote_plus(response_upload_params),

        'line_recording':line_recording,
        'your_recording_url':your_recording_url,
        'feedbacks':feedbacks,
    })




