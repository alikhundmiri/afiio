from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.urls import reverse

from .models import product
from .forms import ProductForm

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('user:user_profile', args=[request.user.username]))
	context = {

	}
	return render(request, 'all_in_one.html', context)

def user_profile(request, username=None):
	# users = User.objects.all()

	user = get_object_or_404(User, username=username)#.select_related('profile')
	if username == request.user.username:
		products = product.objects.filter(user=user).order_by('-public_display', '-updated')
	else:
		products = product.objects.filter(user=user, public_display=True).order_by('-updated')
	
	context = {
		"products" : products,
		"user" : user,
	}
	return render(request, 'core/user_profile.html', context)


def limit_reach(request, username=None):
	return render(request, 'limit_reach.html')

def about(request):
	return render(request, 'about.html')

def price(request):
	return render(request, 'pricing.html')

@login_required
def create_product(request, username=None):
	if not request.user.is_authenticated:
		raise Http404

	user = get_object_or_404(User, username=username)

	if user.profile.paid_user:
		pass
	else:
		links = 0
		links = product.objects.filter(user=user).count()
		if links <=3:
			pass
		else:
			return HttpResponseRedirect(reverse('user:limit_reach', args=[username]))

	form = ProductForm(request.POST or None)
	if form.is_valid():
		# product_name = form.cleaned_data.get("product_name")
		instance = form.save(commit=False)
		instance.user = request.user

		instance.save()
		# form.save_m2m()
		# catagory_utils.set_revenue_details(instance.catagory.slug)
		return HttpResponseRedirect("/")

	context = {
		'form' : form,
		"tab_text": "Submit New Link",
		"top_text": "New Link",
		"form_text": "Please enter all the information below.",
	}
	return render(request, 'general_form.html', context)


@login_required
def edit_product(request, slug=None, username=None):
	instance = get_object_or_404(product, slug=slug)
	if instance.user != request.user:
		raise Http404
	form = ProductForm(request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# form.save_m2m()
		# catagory_utils.set_revenue_details(instance.catagory.slug)
		return HttpResponseRedirect("/")

	context = {
		'form' : form,
		"tab_text": "Submit Product",
		"top_text": "New Product",
		"form_text": "Please enter all the information below.",

	}
	return render(request, 'general_form.html', context)
