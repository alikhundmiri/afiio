from django.conf import settings
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import UserLoginForm, UserRegisterForm
from core.models import Profile
from accounts.forms import ProfileForm
def login_view(request):
	next = ""

	if request.GET:  
		next = request.GET['next']

	dbug = settings.DEBUG
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		if next == "":
			return HttpResponseRedirect("/")
			# return HttpResponseRedirect(reverse('user:home'))
		else:
			return HttpResponseRedirect(next)

	context = {
		"name_nav" : 'login',
		"nbar" : "login",
		"form" : form,
		"dbug" : dbug,
		'page' : 'full-page',

	}
	return render(request, 'accounts/login.html', context)

def register_view(request):
	next = ""

	if request.GET:
		next = request.GET['next']

	dbug = settings.DEBUG
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)

		login(request, new_user)
		# change redirect to edit bio page
		# return HttpResponseRedirect("/")
		return HttpResponseRedirect(reverse('user:edit_bio', args=[user.username]))
	context = {
		"name_nav" : 'register',	
		"nbar" : "register",
		"form" : form,
		'dbug' : dbug,
		'page' : 'full-page',
	}
	return render(request, 'accounts/login.html', context)

def new_bio(request, username=None):
	form = ProfileForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user

		instance.save()

		return HttpResponseRedirect("/")
	context = {
		"form" : form,
		"tab_text" : "Save"
		}
	return render(request, 'general_form.html', context)

def edit_bio(request, username=None):
	instance = get_object_or_404(Profile, user__username=username)
	form = ProfileForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user

		instance.save()

		return HttpResponseRedirect("/")
	context = {
		"form" : form,
		"tab_text" : "Save",
		"top_text" : "Bio Description",
		"form_text" : "Describe yourself and your work",

		}
	return render(request, 'general_form.html', context)

def logout_view(request):
	logout(request)
	return redirect('/')
