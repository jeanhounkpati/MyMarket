
from django.urls import path, re_path
from django.conf.urls import url
from . import views
from .views import *
from .views import DeleteView ,UpdateView
from django.views.generic import TemplateView,View
app_name ="blog"
urlpatterns = [
  
    path('index',views.index, name='index'),
    path('home',views.home, name='home'),
    re_path(r'^show/(?P<id>[0-9]+)/$', views.show,name='show'),   
        
    

    # Cart
    re_path(r'^cart/(?P<id>[0-9]+)/$', views.cart,name='cart'),   
    path('addtocart', AddtoCart.as_view(),name='addtocart'),   
    path('emptycart', views.emptycart,name='emptycart'),
    path('managecart/<int:id>', ManageCart.as_view(),name='managecart'),
    # path('plat-update/<int:id>', PlatUpdate.as_view(),name='plat-update'),
    # path('plat-delete/<int:id>', PlatDelete.as_view(),name='plat-delete'),
    path('profil/order/<int:pk>',CustomerOrderDetail.as_view(),name='customerorderdetail'),
    path('adminorderdetail/<int:pk>',AdminOrderDetail.as_view(),name='adminorderdetail'),
    path('adminorderlist/',AdminOrderList.as_view(),name='adminorderlist'),
    # re_path(r'^adminorderdetail/(?P<pk>[0-9]+)/$', AdminOrderDetail.as_view(),name='adminorderdetail'),


    # CRUD
    path('', views.platform,name='platform'),
    
    re_path(r'^plat-update/(?P<pk>[0-9]+)/$', PlatUpdate.as_view(),name='plat-update'),
    re_path(r'^plat-delete/(?P<pk>[0-9]+)/$', PlatDelete.as_view(),name='plat-delete'),
   
    re_path(r'^checkout/$', CheckoutForm.as_view(),name='checkoutform'),
    re_path(r'^profil/$', CustomerProfil.as_view(),name='customerprofil'),
    # re_path(r'^profil/order/(?P<pk>[0-9]+)$', CustomerOrderDetail.as_view(),name='customerorderdetail'),

    # connnexion et authentification
    re_path(r'^registration/$', CustomerRegistrationForm.as_view(),name='customerregistrationform'),
    re_path(r'^login/$', CustomerLoginForm.as_view(),name='customerloginform'),
    re_path(r'^logout/$', CustomerLogoutForm.as_view(),name='customerlogoutform'),

    # admin pages
    re_path(r'^adminlogin/$', AdminLoginForm.as_view(),name='adminloginform'),
    re_path(r'^adminhome/$', AdminHome.as_view(),name='adminhome'),
    re_path(r'^search/$', SearchForm.as_view(),name='searchform'),
    path("admmin-order-<int:pk>-change", AdminOrderStatusChange.as_view(),name='adminorderstatuschange'),



]

