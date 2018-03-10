from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

def upload_location(Profile, filename):
    return "%s/%s/%s" %(Profile.app_name, Profile.user, filename)

class product_category(models.Model):
	user 					=			models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	category_name			=			models.CharField(max_length=20, blank=False, null=False, default="")
	slug 					=			models.SlugField(max_length=255, unique=True)

	def __str__(self):
		return(self.category_name)


class product(models.Model):
	# who is uploading this product
	user					=			models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	# the product name
	product_name			=			models.CharField(max_length=50, blank=False, null=False, default="")
	product_description		=			models.TextField(max_length=280, blank=True, null=True, default="")
	product_type			=			models.ForeignKey(product_category, related_name='type_category', blank=True, null=True, on_delete=models.CASCADE)

	slug					=			models.SlugField(max_length=255, unique=True)

	# To Avoid spam content
	public_display			=			models.BooleanField(default=False)
	# If the product is uploaded by the maker, this needs to be done manually.
	# product_verified 		=			models.BooleanField(default=False)
	website					=			models.URLField(max_length=1000, blank=False, null=False, help_text="Your Landing page URL. When you choose to advert, your advert will divert to this URL.")
	# other website which are twins to this

	timestamp				=			models.DateTimeField(auto_now=False, auto_now_add=True)
	updated					=			models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return(self.product_name)

	# def get_claim_url(self):
	# 	return reverse("user:claim_product", kwargs={"slug" : self.slug})

	def get_editable_url(self):
		return reverse("user:edit_product", kwargs={"slug" : self.slug, "username" : self.user.username})

	class Meta:
		ordering	 		=			["-timestamp", "-updated"]
		verbose_name 		= 			"Product"
		verbose_name_plural = 			"Products"


class Profile(models.Model):
	app_name 				=			'profiles'
	user 					=			models.OneToOneField(User, on_delete=models.CASCADE)
	bio 					=			models.TextField(max_length=500, blank=True)
	profession 				=			models.CharField(max_length=30, blank=True)
	avatar					=			models.ImageField(
		upload_to=upload_location,
		null = True,
		blank = True,
		height_field = "height_field",
		width_field = "width_field",
	)
	height_field 			=			models.IntegerField(default=0)
	width_field 			=			models.IntegerField(default=0)
	# what can i do for you
	hire_me_if_want			=			models.TextField(max_length=100, blank=True)
	looking_for				=			models.CharField(max_length=100, blank=True)

	paid_user				=			models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()



# SLUG FOR PRODUCT
def slug_for_product(instance, new_slug=None):
	slug = slugify(instance.product_name)
	if new_slug is not None:
		slug = new_slug
	qs = product.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		# print("slug: " + str(slug))
		a = slug.split('-')
		# print("a: " + str(a[0]))
		new_slug = "%s-%s" %(a[0], qs.first().id)
		# print("new_slug: " + str(new_slug))
		# new_slug = "%s-%s" %(slug, qs.first().id)
		return slug_for_product(instance, new_slug=new_slug)
	return slug
def pre_save_product(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_for_product(instance)

# SLUG FOR PRODUCT CATEGORY
def slug_for_product_category(instance, new_slug=None):
	slug = slugify(instance.category_name)
	if new_slug is not None:
		slug = new_slug
	qs = product_category.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		# print("slug: " + str(slug))
		a = slug.split('-')
		# print("a: " + str(a[0]))
		new_slug = "%s-%s" %(a[0], qs.first().id)
		# print("new_slug: " + str(new_slug))
		# new_slug = "%s-%s" %(slug, qs.first().id)
		return slug_for_product_category(instance, new_slug=new_slug)
	return slug
def pre_save_product_category(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slug_for_product_category(instance)


pre_save.connect(pre_save_product, sender=product)
pre_save.connect(pre_save_product_category, sender=product_category)
