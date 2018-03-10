from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, Http404

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	update_session_auth_hash
)
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404

from .forms import UserLoginForm, UserRegisterForm
from core.models import Profile
from accounts.forms import ProfileForm, EditProfileForm
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

@login_required
def settings_page(request):
	# fetch bio and profession
	# ?fetch username
	context = {

	}
	return render(request, 'accounts/settings.html', context)

@login_required
def new_bio(request, username=None):
	form = ProfileForm(request.POST or None, request.FILES or None)
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

@login_required
def edit_bio(request, username=None):
	if request.user.username == username:
		pass
	else:
		raise Http404
	instance = get_object_or_404(Profile, user__username=request.user)
	form = ProfileForm(request.POST or None, request.FILES or None, instance=instance)
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

@login_required
def first_last_name(request, username=None):
	if request.user.username == username:
		pass
	else:
		raise Http404
	form = EditProfileForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect("/")
	context = {
		'form' : form,
		"tab_text" : "Update",
		"top_text" : "User Information",
		"form_text" : "Your personal information",

	}
	return render(request, 'general_form.html', context)
@login_required
def change_password(request, username=None):
	if request.user.username == username:
		pass
	else:
		raise Http404
	form = PasswordChangeForm(request.POST or None )
	if form.is_valid():
		form.save()
		update_session_auth_hash(request, form.user)
		return HttpResponseRedirect("/")
	
	context = {
		'form' : form,
		"tab_text" : "Update",
		"top_text" : "Change Password",
		"form_text" : "",

	}
	return render(request, 'general_form.html', context)

@login_required
def logout_view(request):
	logout(request)
	return redirect('/')
