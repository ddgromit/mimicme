from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django import http
from django.contrib.auth import authenticate, login, logout

def create_user(email, password, username):
    existing = User.objects.filter(email=email).count()
    if existing > 0:
        return None

    existing = User.objects.filter(username=username).count()
    if existing > 0:
        return None

    user = User.objects.create_user(
        username = username,
        email = email,
        password=password,
    )
    return user


class NewUserForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

def homepage(request):
    # If already logged in, goto sets
    if request.user.is_authenticated():
        return http.HttpResponseRedirect('/sets/')

    errors = ""

    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                username = form.cleaned_data['username'])

            if not user:
                errors = "Email or password already existed"
            else:
                # Login and goto sets page
                user = authenticate(
                    username = form.cleaned_data['username'],
                    password = form.cleaned_data['password'])
                login(request,user)
                return http.HttpResponseRedirect('/sets/')


    # Display form or errors
    return render(request,'homepage.html',{
        'form':form,
        'errors':errors,
    })

def login_handler(request):
  if request.method == 'POST':
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
      if user.is_active:
        login(request, user)
        # success
        return http.HttpResponseRedirect('/sets/')
      else:
        # disabled account
        raise Exception('invalid account')
    else:
      # invalid login
      raise Exception('invalid login')

  return render(request,'login.html',{})

def logout_handler(request):
    logout(request)
    return http.HttpResponseRedirect('/')
