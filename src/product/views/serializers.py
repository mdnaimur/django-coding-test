from rest_framework import serializers

from product.models import (Variant,Product,ProductImage,ProductVariant,ProductVariantPrice)



class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','sku','description']



class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['variant_title',]



class ProductVariantPricetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantPrice
        fields = ['price','stock']
   

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['file_path']