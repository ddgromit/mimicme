from django.conf.urls.defaults import *

urlpatterns = patterns('practice.views',
    (r'practice/?$','practice'),
    (r'sets/?$','sets'),
    (r'review/?$','review'),
)
