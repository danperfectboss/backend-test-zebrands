"""zebrand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_products import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #Products
    path('add_data',views.add_data, name="addData" ),
    path('add_product',views.add_product, name="addProduct"),
    path('products',views.get_products, name="produc" ),
    path('update_products/<int:id_product>',views.update_product, name="updateProduct" ),
    path('delete_products/<int:id_product>',views.delete_product, name="deleteProduct" ),
    #login
    path('',views.login, name="login" ),
    path('options',views.options, name="option" ),
    #Admin
    path('create_admin',views.create_admin, name="createAdmin" ),
    path('show_admin',views.show_admin, name="getAllAdmin" ),
    path('update_admin/<int:id_admin>',views.update_admin, name="updateAdmin" ),
    path('delete_admin/<int:id_admin>',views.delete_admin, name="deleteAdmin" ),

    
]
