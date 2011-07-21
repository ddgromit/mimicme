from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import http
from django.core.files.storage import default_storage
import logging
import pprint

def uploadTarget(request):
    logging.warn('user: ' + str(request.user.is_authenticated()))
    logging.warn('uploadTarget')
    logging.warn('METHOD: ' + request.method)
    if request.method == 'POST':
        #logging.warn('post data: ' + request.raw_post_data)
        pprint.pprint(request.POST)
        pprint.pprint(request.POST.get('press'))
        logging.warn('encoding: ' + str(request.encoding))
        logging.warn('number files: ' + str(len(request.FILES)))
        pprint.pprint(request.FILES)
        logging.warn('has fileupload: ' + str("fileupload" in request.FILES))
        if "fileupload" in request.FILES:
            default_storage.save('latestfile',request.FILES['fileupload'])
        #pprint.pprint(request.META)
    else:
        pass
    return http.HttpResponse("<html><body><form method='POST' enctype='multipart/form-data'><input type='file' name='fileupload'><input type='submit' name='submit'></form></body></html>")

