from django.conf.urls.defaults import *

urlpatterns = patterns('practice.views',
    (r'practice/(?P<phrase_set_id>\d+)/?$','practice'),
    (r'sets/?$','sets'),
    (r'review/?$','review'),
    (r'testrecording/?$','testrecording'),
    (r'submit_recording/?','submit_recording'),
)
