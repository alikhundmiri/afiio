from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.urls import reverse

from .models import product, product_category
from .forms import ProductForm, CategoryForm
import datetime

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
		# p_roduct = product.objects.annotate(number_of_links=Count('user', distinct=True))

		all_category = product_category.objects.filter(user=user)
		product_exclude = product.objects.exclude(id__in=all_category.values_list('type_category__id',flat=True)).filter(user=user)

		# products = product.objects.filter(user=user).order_by('-public_display', '-updated')
	else:
		# products = product.objects.filter(user=user, public_display=True).order_by('-updated')
		all_category = product_category.objects.filter(user=user)
		product_exclude = product.objects.exclude(id__in=all_category.values_list('type_category__id',flat=True)).filter(user=user, public_display=True)
	print("============   All catagory   ===============")
	print(all_category)
	print("============   Product exclude   ===============")
	print(product_exclude)
	
	context = {
		# "products" : products,
		"user" : user,
		"all_category" : all_category,
		"product_exclude" : product_exclude,
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

	if request.method == 'POST':
		form = ProductForm(user, request.POST or None)
		if form.is_valid():
			# product_name = form.cleaned_data.get("product_name")
			instance = form.save(commit=False)
			instance.user = request.user

			instance.save()
			# form.save_m2m()
			# catagory_utils.set_revenue_details(instance.catagory.slug)
			return HttpResponseRedirect("/")
	else:
		form = ProductForm(user)

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
	user = get_object_or_404(User, username=username)


	form = ProductForm(user, request.POST or None, instance = instance)
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



# ===========

@login_required
def create_category(request, username=None):
	if not request.user.is_authenticated:
		raise Http404

	user = get_object_or_404(User, username=username)

	if user.profile.paid_user:
		pass
	else:
		category_ = 0
		category_ = product_category.objects.filter(user=user).count()
		if category_ <=2:
			pass
		else:
			return HttpResponseRedirect(reverse('user:limit_reach', args=[username]))

	if request.method == 'POST':
		form = CategoryForm(user, request.POST or None)
		if form.is_valid():
			# product_name = form.cleaned_data.get("product_name")
			instance = form.save(commit=False)
			instance.user = request.user

			instance.save()
			# form.save_m2m()
			# catagory_utils.set_revenue_details(instance.catagory.slug)
			return HttpResponseRedirect("/")
	else:
		form = CategoryForm(user)

	context = {
		'form' : form,
		"tab_text": "Submit New Category",
		"top_text": "New Category",
		"form_text": "Please enter A new unique Category name in the field below!",
	}
	return render(request, 'general_form.html', context)


@login_required
def edit_category(request, slug=None, username=None):
	instance = get_object_or_404(product_category, slug=slug)
	if instance.user != request.user:
		raise Http404
	user = get_object_or_404(User, username=username)


	form = CategoryForm(user, request.POST or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# form.save_m2m()
		# catagory_utils.set_revenue_details(instance.catagory.slug)
		return HttpResponseRedirect("/")

	context = {
		'form' : form,
		"tab_text": "Submit Changes",
		"top_text": "Edit Category",
		"form_text": "Please enter the new Category name in the field below!",

	}
	return render(request, 'general_form.html', context)



@user_passes_test(lambda u: u.is_superuser)
def super_user(request, username=None):
	time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)

	users = User.objects.all().count()
	links = product.objects.all().count()
	# no_links = products.objects.filter()
	no_links2 = product.objects.annotate(number_of_links=Count('user', distinct=True))
	# all_cats = product_catagory.objects.annotate(number_of_products=Count('catagory', distinct=True))
	print(no_links2)
	u_last24h = User.objects.filter(date_joined__gte=time_24_hours_ago)

	context = {
		"users" : users,
		'links' : links,
		"u_last24h" : u_last24h,
	}
	return render(request, 'core/super_user.html', context)