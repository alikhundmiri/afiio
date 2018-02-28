from django import forms

from .models import product, Profile

import re

# form to create a new product
class ProductForm(forms.ModelForm):
    # revenue_source = forms.ModelMultipleChoiceField(queryset = revenue_source.objects.all(), widget=forms.CheckboxSelectMultiple())
    # tags = forms.ModelMultipleChoiceField(queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = product
        fields = [
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

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["product_name"].help_text = "Your Product Name" 
        self.fields["product_description"].help_text = "Details about the project, within 280 characters" 
        self.fields["website"].help_text = "Project URL, please enter the protocols https:// or http:// as well" 
        self.fields["public_display"].help_text = "Do you wish to make this public?" 

