from django.contrib import admin

from .models import product, Profile, product_category


class ProductAdmin(admin.ModelAdmin):
	list_display = ['user', 'product_name', 'public_display', "product_type",]
	list_filter = ['user', 'product_name', 'public_display', "product_type",]
	list_editable = ['public_display',]
	search_fields = ['user', 'product_name','public_display', "product_type",]

class ProfileAdmin(admin.ModelAdmin):
	list_display = ["user", "bio", "profession", "paid_user",]
	list_filter = ["user", "bio", "profession", "paid_user",]
	list_editable = ["paid_user",]
	search_fields = ["user", "bio", "profession", "paid_user",]

class CategoryAdmin(admin.ModelAdmin):
	list_display = ["user", "category_name"]
	list_filter = ["user", "category_name"]
	list_editable = ["category_name"]
	search_fields = ["user", "category_name", "slug"]


admin.site.register(product_category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(product, ProductAdmin)


