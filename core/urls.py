from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
    ('^/?$','homepage'),
    ('^login/?$','login_handler'),
    ('^logout/?$','logout_handler'),
    ('^testtheme/$','testtheme_handler'),
    ('^themed_homepage/?$','themed_homepage_handler'),
)
