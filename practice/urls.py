from django.conf.urls.defaults import *

urlpatterns = patterns('practice.views',
    (r'^practice/(?P<phrase_set_id>\d+)/?$','practice'),
    (r'^sets/?$','sets'),
    (r'^give_response_feedback/?$','response_feedback_handler'),
    (r'^review/?$','review'),
    (r'^testrecording/?$','testrecording'),
    (r'^submit_recording/?','submit_recording'),
    (r'^expert_recording/(?P<phrase_id>\d+)/?','expert_recording'),
    (r'^give_response/?','give_response'),
    (r'^finished/?','finished'),

    (r'^conversations/?$','conversations_handler'),
    (r'^conversation/(?P<conversation_id>\d+)/start$','start_conversation_handler'),
    (r'^practicing/(?P<attempt_id>\d+)/(?P<order>\d+)/$','practicing_handler'),

)
