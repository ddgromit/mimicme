from practice.models import *
from django.contrib import admin
import urllib
import settings

class LineAdmin(admin.ModelAdmin):
    #change_form_template = 'admin/myapp/extras/openstreetmap_change_form.html'

    def change_view(self, request, object_id, extra_context=None):
        line = Line.objects.get(id=object_id)

        interviewer_recording_url = settings.MEDIA_URL + str(line.interviewer_recording) if line.interviewer_recording else ""
        interviewer_upload_params = "type=line_interviewer&line_id=%s" % line.id
        speaker_recording_url = settings.MEDIA_URL + str(line.speaker_recording) if line.speaker_recording else ""
        speaker_upload_params = "type=line_speaker&line_id=%s" % line.id

        my_context = {
            'line':line,
            'interviewer_recording_url':interviewer_recording_url,
            'interviewer_upload_params':urllib.quote_plus(interviewer_upload_params),
            'speaker_recording_url':speaker_recording_url,
            'speaker_upload_params':urllib.quote_plus(speaker_upload_params),
        }
        return super(LineAdmin, self).change_view(request, object_id,
            extra_context=my_context)




admin.site.register(Phrase)
admin.site.register(PhraseSet)
admin.site.register(Recording)
admin.site.register(Response)
admin.site.register(ResponseFeedback)

admin.site.register(Line,LineAdmin)

map(admin.site.register,[
    Conversation,
    Attempt,
    LineRecording,
])
