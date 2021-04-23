from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from app_products.models import Product
from django.shortcuts import render
from django.http import  HttpResponse
from .models import *
from .validations.regex import validateParams
from django.contrib import messages
from django.views.decorators.http import require_http_methods



######################## START Part for CRUD in PRODUCTS


def add_data(request):
    return render(request, 'add_product.html')

def add_product(request):
    
    if request.session.get("edit",False):

        if request.method != 'POST':
            return HttpResponseRedirect("/add_data")
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
                
                return HttpResponseRedirect("/add_data")

            else: return HttpResponseBadRequest("Not today bro!")

    else: return HttpResponseRedirect("/")

def get_products(request):
    products= Product.objects.all()

    return render(request,'get_products.html' ,{'all_products':products})

def update_product(request,id_product):

    if request.session.get("edit",False):
        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            brand = request.POST.get('brand')
            # validate params for a kind of injection, sql or mongo inyection
            if validateParams(name, price, brand) is False:
                try:
                    product = Product.objects.get(sku=id_product)
                    product.name = name
                    product.price = price
                    product.brand = brand
                    product.save()
                    messages.success(request,"The Product was edited successfully")
                except:
                    messages.error(request,"Error to edit the product")
                
                return HttpResponseRedirect("/update_products/"+str(id_product))

            else: return HttpResponseBadRequest("Not today bro!")
            
        else:
            if type(id_product) is int:
                product = Product.objects.get(sku=id_product)
                if product is None:
                    return HttpResponse("Product not found")
                else:
                    return render(request, 'edit_product.html',{'product':product})
                
    else: return HttpResponseRedirect("/")

def delete_product(request,id_product):
    if request.session.get("edit",False):
        if type(id_product) is int:
            product = Product.objects.get(sku=id_product)
            if product is None:
                return HttpResponse("Product not found")
            else:
                product.delete()
                messages.error(request,"Product successfuly deleted")
                
                return  HttpResponseRedirect("/products")
    else: return HttpResponseRedirect("/")


######################## ENDS Part for CRUD in PRODUCTS


######################## START Part for CRUD in ADMINS
def create_admin(request):
    if request.session.get("edit",False):
        if request.method != 'POST':
            # return HttpResponseRedirect("/create_admin")
            return render(request,'admin/add_admin.html')
        else:
            # Get all parameter for Form
            name = request.POST.get('name')
            permission = request.POST.get('permission')
            employeeNum = request.POST.get('employee_num')
            password = request.POST.get('password')
            
            # validate params for a kind of injection, sql or mongo inyection
            if validateParams(name, permission, employeeNum, password) is False:
                try:
                    admin = Admins(name= name, permissions=permission, num_employee= employeeNum, password=password)
                    admin.save()
                    messages.success(request,"The Admin was added successfully")
                except:
                    messages.error(request,"Error to add the admin")
                
                return HttpResponseRedirect("/create_admin")

            else: return HttpResponseBadRequest("Not today bro!")
    else: return HttpResponseRedirect("/")
    

def update_admin(request, id_admin):

    if request.session.get("edit",False):
        if request.method == 'POST':
            name = request.POST.get('name')
            permission = request.POST.get('permission')
            employeeNum = request.POST.get('employee_num')
            # validate params for a kind of injection, sql or mongo inyection
            if validateParams(name, permission, employeeNum) is False:
                try:
                    admin = Admins.objects.get(id=id_admin)
                    admin.name = name
                    admin.permissions = permission
                    admin.num_employee = employeeNum
                    admin.save()
                    messages.success(request,"The Admin was edited successfully")
                except:
                    messages.error(request,"Error to edit the admin")
                
                return HttpResponseRedirect("/update_admin/"+str(id_admin))

            else: return HttpResponseBadRequest("Not today bro!")
            
        else:
            if type(id_admin) is int:
                admin = Admins.objects.get(id=id_admin)
                if admin is None:
                    return HttpResponse("Admin not found")
                else:
                    return render(request, 'admin/edit_admin.html',{'admins':admin})
                return HttpResponse(id_product)
    else: return HttpResponseRedirect("/")


def show_admin(request):
    
    admins = Admins.objects.all()
    for admin in admins:
        print(admin.password)
    return render(request, 'admin/get_admin.html', {'admins':admins})

def delete_admin(request, id_admin):
    if request.session.get("edit",False):
        if type(id_admin) is int:
            admin = Admins.objects.get(sku=id_admin)
            if admin is None:
                return HttpResponse("admin not found")
            else:
                admin.delete()
                messages.error(request,"admin successfuly deleted")
                
                return  HttpResponseRedirect("/show_admin")
    else: return HttpResponseRedirect("/")

######################## END Part for CRUD in ADMINS


def login(request):
    
    if request.method == 'POST':
        user = request.POST.get('usr')
        psw = request.POST.get('pwd')
        if validateParams(user, psw) is False:
            try:
                admin = Admins.objects.get(name=user,password= psw )
                
                request.session['edit'] = admin.permissions
                request.session['user'] = admin.id
                
                return HttpResponseRedirect("/options")
            
                messages.success(request,"The Admin was added successfully")
            except:
                messages.error(request,"User o passwrod wrong")
                
                return HttpResponseRedirect("/")
            

        else: return HttpResponseBadRequest("Not today bro!")
        
    else:
        return render(request, 'login/login.html')



def options(request):

    permisos=request.session['edit']

    id= request.session['user']
    return render(request,'options.html',{'user':id, 'permisos':permisos })