from django.contrib import admin

from .models import product, Profile


class ProductAdmin(admin.ModelAdmin):
	list_display = ['user', 'product_name', 'public_display',]
	list_filter = ['user', 'product_name', 'public_display',]
	list_editable = ['public_display',]
	search_fields = ['user', 'product_name','public_display']

class ProfileAdmin(admin.ModelAdmin):
	list_display = ["user", "bio", "profession", "paid_user",]
	list_filter = ["user", "bio", "profession", "paid_user",]
	list_editable = ["paid_user",]
	search_fields = ["user", "bio", "profession", "paid_user",]



admin.site.register(Profile, ProfileAdmin)
admin.site.register(product, ProductAdmin)


