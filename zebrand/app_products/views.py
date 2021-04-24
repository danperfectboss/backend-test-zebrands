from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from app_products.models import Product
from django.shortcuts import render
from django.http import  HttpResponse
from .models import *
from .validations.regex import validateParams
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .telegram.messages import MessageTelegram



######################## START Part for CRUD in PRODUCTS


def add_data(request):
    return render(request, 'add_product.html')

def add_product(request):
    #validate if a session exist, if not put false to the session an redirect to login
    if request.session.get("edit",False):
        #validate the method http
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
                    #assigns the parameters to the object model for save the data
                    product = Product(name= name, price=price, brand= brand)
                    product.save()
                    messages.success(request,"The Product was added successfully")
                except:
                    messages.error(request,"Error to add the product")
                
                return HttpResponseRedirect("/add_data")
            # if a parameter contains some inusual redirect to this message
            else: return HttpResponseBadRequest("Not today bro!")

    else: return HttpResponseRedirect("/")

def get_products(request):
    # get all element in the data base
    products= Product.objects.all()

    #assing the value forn the session variable for pass to frontend
    canEdit= request.session['edit']

    return render(request,'get_products.html',{'all_products':products, 'canEdit':canEdit})

def update_product(request,id_product):

    #validate if a session exist, if not put false to the session an redirect to login
    if request.session.get("edit",False):
        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            brand = request.POST.get('brand')
            # validate params for a kind of injection, sql or mongo inyection
            if validateParams(name, price, brand) is False:
                try:
                    #Put the parameter into the object product
                    product = Product.objects.get(sku=id_product)
                    product.name = name
                    product.price = price
                    product.brand = brand
                    #and save it
                    product.save()
                    #create the variable that contains the text who edit these product
                    text= "The Employee No. {} modify the product with sku {}".format(request.session['noemplo'],id_product)
                           
                    #call the function for send the message to telegram chanel
                    MessageTelegram(text).sendMessage()
                    #send message to fronend
                    messages.success(request,"The Product was edited successfully")
                except:
                    messages.error(request,"Error to edit the product")
                
                return HttpResponseRedirect("/update_products/"+str(id_product))

            else: return HttpResponseBadRequest("Not today bro!")
            
        else:
            #if the request is get response with the product equals to id_product parameter
            if type(id_product) is int:
                product = Product.objects.get(sku=id_product)
                #if don't exist the id in the database return a error message
                if product is None:
                    return HttpResponse("Product not found")
                else:
                    # return the product queried the database
                    return render(request, 'edit_product.html',{'product':product})
                
    else: return HttpResponseRedirect("/")

def delete_product(request,id_product):
    if request.session.get("edit",False):
        #verified the type of the variable to follow with delete product
        if type(id_product) is int:
            #get the element by id of product
            product = Product.objects.get(sku=id_product)
            if product is None:
                return HttpResponse("Product not found")
            else:
                #delete  the product
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
            admin = Admins.objects.get(id =id_admin)
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
        #get the parameter from de frontend
        user = request.POST.get('usr')
        psw = request.POST.get('pwd')
        if validateParams(user, psw) is False:
            try:
                # If exist some admin with the same info joined, assing the values to session variables
                admin = Admins.objects.get(name=user,password= psw )
                
                request.session['edit'] = admin.permissions
                request.session['user'] = admin.id
                request.session['noemplo'] = admin.num_employee
                
                return HttpResponseRedirect("/options")
            
                messages.success(request,"The Admin was added successfully")
            except:
                messages.error(request,"User o passwrod wrong")
                
                return HttpResponseRedirect("/")
            

        else: return HttpResponseBadRequest("Not today bro!")
        
    else:
        return render(request, 'login/login.html',{'hide':True})

def logout(request):
    #validate the sessions and destroy it
    if request.session.get("edit",False):
        del request.session["edit"]

    if request.session.get("user",False):
        del request.session["user"]

    return HttpResponseRedirect("/")

def options(request):
    # Just show the only two options in the frontend
    permisos=request.session['edit']

    return render(request,'options.html',{'user':id, 'permisos':permisos })