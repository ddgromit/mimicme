from practice.models import *
from django.contrib import admin

admin.site.register(Phrase)
admin.site.register(PhraseSet)
admin.site.register(Recording)
admin.site.register(Response)
admin.site.register(ResponseFeedback)

map(admin.site.register,[
    Conversation,
    Line,
    Attempt,
    LineRecording,
])
