from practice.models import *
from django.contrib import admin


class LineAdmin(admin.ModelAdmin):

    # A template for a very customized change view:
    #change_form_template = 'admin/myapp/extras/openstreetmap_change_form.html'

    def get_osm_info(self):
        # ...
        pass

    def change_view(self, request, object_id, extra_context=None):
        line = Line.objects.get(id=object_id)

        interviewer_recording_url = ''
        interviewer_upload_params = ''
        speaker_recording_url = ''
        speaker_upload_params = ''

        my_context = {
            'line':line,
            'interviewer_recording_url':interviewer_recording_url,
            'interviewer_upload_params':interviewer_upload_params,
            'speaker_recording_url':speaker_recording_url,
            'speaker_upload_params':speaker_upload_params,
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
