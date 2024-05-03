from django.forms import forms, ModelForm, CharField,FloatField, TextInput, Textarea, BooleanField, CheckboxInput,SlugField

from product.models import Variant,Product,ProductImage,ProductVariant,ProductVariantPrice


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'active': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title','sku','description']
        widgets ={
            'title':TextInput(attrs={'class':'form-control'}),
            # 'sku': SlugField(attrs={'class':'form-control'}),
            'description': Textarea(attrs={'class':'form-control'}),
        }


class ProductVariantForm(ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['variant_title',]
        widgets ={
            # 'variant_title':CharField(attrs={'class':'form-control'}),
        }


class ProductVariantPriceForm(ModelForm):
    class Meta:
        model = ProductVariantPrice
        fields = "__all__"
        #fields = ['product_variant_one', 'product_variant_two', 'product_variant_three', 'price', 'stock', 'product']
        widgets ={
            # 'price':FloatField(attrs={'class':'form-control'}),
            # 'stock': FloatField(attrs={'class':'form-control'}),
        }

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'