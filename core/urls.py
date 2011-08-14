from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
    ('^oldhomepage/?$','homepage'),
    ('^login/?$','login_handler'),
    ('^logout/?$','logout_handler'),
    ('^testtheme/$','testtheme_handler'),
    ('^/?$','themed_homepage_handler'),
    ('^register/?$','register_handler'),
)
