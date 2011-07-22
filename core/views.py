from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django import http

class NewUserForm(forms.Form):
    email = forms.CharField()
    first_name = forms.CharField()
    password = forms.CharField()

def homepage(request):
    return http.HttpResponseRedirect('/sets/')
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            pass#User.create_user()

    return render(request,'homepage.html',{
        'form':form,
    })

def login(request):
  if request.method == 'POST':
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
      if user.is_active:
        login(request, user)
        # success
        return HttpResponseRedirect('/sets/')
      else:
        # disabled account
        raise Exception('invalid account')
    else:
      # invalid login
      raise Exception('invalid login')

