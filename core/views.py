from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django import http
from django.contrib.auth import authenticate, login, logout
from django.forms.util import ErrorList
from settings import LOGIN_REDIRECT_URL

def testtheme_handler(request):
    return render(request,'themeddash.html',{})

def themed_homepage_handler(request):
    return render(request,'themed_homepage.html',{})


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
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class':'text_field'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'text_field'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'text_field'})
    )

def register_handler(request):
    # If already logged in, goto sets
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(LOGIN_REDIRECT_URL)

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
                return http.HttpResponseRedirect(LOGIN_REDIRECT_URL)


    # Display form or errors
    return render(request,'register.html',{
        'form':form,
        'errors':errors,
    })


def homepage(request):
    # If already logged in, goto sets
    if request.user.is_authenticated():
        return http.HttpResponseRedirect(LOGIN_REDIRECT_URL)

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
                return http.HttpResponseRedirect(LOGIN_REDIRECT_URL)


    # Display form or errors
    return render(request,'homepage.html',{
        'form':form,
        'errors':errors,
    })


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'text_field'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'text_field'})
    )

def login_handler(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # success
                    return http.HttpResponseRedirect(LOGIN_REDIRECT_URL)
                else:
                    # disabled account
                    raise Exception('invalid account')
            else:
                # invalid login
                errors = form._errors.setdefault('username',ErrorList())
                errors.append(u"Incorrect Login")


    return render(request,'login.html', {
        'form':form,
    })


def logout_handler(request):
    logout(request)
    return http.HttpResponseRedirect('/')
