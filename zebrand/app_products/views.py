from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from app_products.models import Product
from django.shortcuts import render
from django.http import  HttpResponse
from .models import *
from .validations.regex import validateParams
from django.contrib import messages
from django.views.decorators.http import require_http_methods

# Create your views here.
def index(request):
    pass

def login(request):
    if request == 'POST':
        pass
    else:
         return render('login/login.html')

# # @require_http_methods(["GET"])
# def add_product(request):
#     return render(request,"add_product.html")

# # @require_http_methods(["POST"])

def add_data(request):
    return render(request, 'add_product.html')

def add_product(request):

    if request.method != 'POST':
        return HttpResponseRedirect("/addData")
    else:
        # Get all parameter for Form
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        # validate params for a kind of injection, sql or mongo inyection
        if validateParams(name, price, brand) is False:
            try:
                product = Product(name= name, price=price, brand= brand)
                product.save()
                messages.success(request,"The Product was added successfully")
            except:
                messages.error(request,"Error to add the product")
            
            return HttpResponseRedirect("/addData")

        else: return HttpResponseBadRequest("No bro")


def update_product(request):
    pass