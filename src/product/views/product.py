from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from datetime import datetime
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView,FormView,UpdateView
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.models import Variant,Product,ProductVariantPrice,ProductVariant,ProductImage
from product.forms import ProductForm,VariantForm,ProductVariantForm,ProductVariantPriceForm,ProductImageForm
from .serializers import ProductImageSerializer,ProductSerializer,ProductVariantPricetSerializer,ProductVariantSerializer,VariantSerializer
class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


# class ProductCreateView(FormView):
#     template_name = 'products/create.html'
#     form_class = ProductForm
#     success_url = reverse_lazy('products/list.html')


#     def form_valid(self,form):
#         product = form.save()
#         variant_form = ProductVariantForm(self.request.POST)

#         if variant_form.is_valid():
#             variant = variant_form.save(commit = False)
#             variant.product = product
#             variant.save()

#             price_form = ProductVariantPricetForm(self.request.POST)
#             if price_form.is_valid():
#                 price = price_form.save(commit=False)
#                 price.product_variant = variant
#                 price.save()

#                 image_form = ProductImageForm(self.request.POST, self.request.FILES)
#                 if image_form.is_valid():
#                     image = image_form.save(commit=False)
#                     image.product = product
#                     image.save()

#         serialized_data = {
#             'product': json.loads(json.dumps(product, cls=DjangoJSONEncoder)),
#             'variant': json.loads(json.dumps(variant, cls=DjangoJSONEncoder)),
#             'price': json.loads(json.dumps(price, cls=DjangoJSONEncoder)),
#             'image': json.loads(json.dumps(image, cls=DjangoJSONEncoder))
#         }

#         return JsonResponse(serialized_data)
# class ProductListView(ListView):
#     model = Product
#     template_name = 'products/list.html'
#     context_object_name = 'product_list'


class ProductVariantPriceListView(ListView):
    model = ProductVariantPrice
    template_name = 'products/list.html'
    context_object_name = 'product_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        product_title = self.request.GET.get('product_title')
        product_variant = self.request.GET.get('product_variant')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        date = self.request.GET.get('date')

        filter_query = Q()
        #appy filters
        if product_title:
            #print(f'this is queryset {queryset}')
            queryset = queryset.filter(product__title__contains = product_title)
        if product_variant:
            queryset = queryset.filter(
        Q(product_variant_one__variant_title__icontains=product_variant) |
        Q(product_variant_two__variant_title__icontains=product_variant) |
        Q(product_variant_three__variant_title__icontains=product_variant)
    )

        if min_price:
            queryset = queryset.filter(price__gte = min_price)
        if max_price:
            queryset = queryset.filter(price__lte = max_price)
        if date:
            try:
                date = datetime.strptime(date,'%d-%m-%Y').date()
                queryset = queryset.filter(date=date)
            except ValueError:
                pass
        return queryset
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['product_list'],self.paginate_by)
        page_number = self.request.GET.get('page')
        items_page = paginator.get_page(page_number)
        context['items_page'] = items_page
        context['variants'] = ProductVariant.objects.all().values('variant_title').distinct()
        return context

     # Update
    def get(self, request, *args, **kwargs):
        if 'update_id' in request.GET:
            return self.render_to_response({'update_form': ProductVariantPriceForm(instance=self.get_object(request.GET['update_id']))})
        else:
            return super().get(request, *args, **kwargs)

    def post_update(self, request):
        update_form = ProductVariantPriceForm(request.POST, instance=self.get_object(request.POST['update_id']))
        if update_form.is_valid():
            return self.form_valid(update_form)
        else:
            return self.form_invalid(update_form)

class ProductVariantPriceUpdateView(UpdateView):
    model = ProductVariantPrice
    #fields = ['product__title', 'product__description', 'product_variant', 'price', 'stock']  
    form_class = ProductVariantPriceForm
    #template_name = 'products/list.html'
    template_name = 'products/edit_product.html'
    success_url  = '/product/list/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Exclude fields from the form
        excluded_fields = ['product']
        for field_name in excluded_fields:
            if field_name in form.fields:
                del form.fields[field_name]
        return form

## API create

class ProductListAPI(APIView):
    
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class ProductVariantListAPI(APIView):
    def get(self,request):
        products = ProductVariant.objects.all()
        serializer = ProductVariantSerializer(products,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProductVariantSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProductVariantPriceAPI(APIView):
    def get(self,request):
        products = ProductVariantPrice.objects.all()
        serializer = ProductVariantPricetSerializer(products,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProductVariantPricetSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProductImageAPI(APIView):
    def get(self,request):
        products = ProductImage.objects.all()
        serializer = ProductImageSerializer(products,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProductImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)