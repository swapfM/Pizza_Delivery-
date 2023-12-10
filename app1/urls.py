from django.contrib import admin
from django.contrib.auth import logout
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.adminlogin, name='adminloginpage'),
    path('', views.home, name="home"),
    path('admin/homepage', views.adminhomepage, name="adminhomepage"),
    path('admin/adminlogout', views.user_logout, name="logout"),
    path('admin/adminauthenticate', views.user_authenticate, name='adminauthenticate'),
    path('admin/addpizza', views.addpizza, name="addpizza"),
    path('admin/deletepizza/<int:pizzapk>/', views.deletepizza),
    path('signup/', views.signup),
    path('loginuser/', views.userlogin),
    path('userauthenticate/', views.authenticate_user),
    path('customerpage/', views.customerwelcome),
    path('userlogout/', views.userlogout),
    path('placeorder/', views.placeorder),
    path('userorders/', views.userorders),
    path('adminorders/', views.adminorders),
    path('acceptorder/<int:orderpk>/', views.acceptorder),
    path('declineorder/<int:orderpk>/', views.declineorder),

]
