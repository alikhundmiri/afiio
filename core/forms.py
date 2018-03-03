from django import forms

from .models import product, Profile, product_category

import re

class CategoryForm(forms.ModelForm):
    class Meta:
        model = product_category
        fields = ['category_name']

    def clean_category_name(self):
        this_category = self.cleaned_data.get('category_name')
        user_category = product_category.objects.filter(user=self.user)
        if this_category in user_category:
            raise forms.ValidationError("You already have a catagory with this Name")
        return this_category

    def __init__(self, user, *args , **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["category_name"].help_text = "Enter A new unique category name!."
        self.user = kwargs.pop('user', None)

# form to create a new product
class ProductForm(forms.ModelForm):
    # revenue_source = forms.ModelMultipleChoiceField(queryset = revenue_source.objects.all(), widget=forms.CheckboxSelectMultiple())
    # tags = forms.ModelMultipleChoiceField(queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = product
        fields = [
        "product_type",
        "product_name",
        "product_description",
        "website",
        "public_display",
            ]
    
    def clean_product_name(self):
        # print("Validating...")
        pattern = r'[a-zA-Z0-9 ]'
        product_name = self.cleaned_data.get('product_name')
        
        if not re.search(pattern, product_name):
            # print("Not valid")
            raise forms.ValidationError("This Name contains invalid characters")
        # print("Valid")
        return product_name

    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["product_name"].help_text = "Your Product Name" 
        self.fields["product_description"].help_text = "Details about the project, within 280 characters" 
        self.fields["website"].help_text = "Project URL, please enter the protocols https:// or http:// as well" 
        self.fields["public_display"].help_text = "Do you wish to make this public?" 
        self.fields["product_type"].help_text = "Leave this empty to keep this general"
        self.fields["product_type"].queryset = product_category.objects.filter(user=user).all()

