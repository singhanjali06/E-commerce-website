from django.urls import path
from . import views
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.vendor_registration, name='vendor_registration'),
    path('register/customer/', views.customer_registration, name='user_registration'),
    path('get_user_type/', views.get_user_type, name='get_user_type'),
    path('login/', views.login_view, name='login_view'),
    path('vendor_dashboard/',views.vendor_dashboard, name='vendor_dashboard'),
    path('customer_dashboard/',views.customer_dashboard, name='customer_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),

    
    #Vendor Access
    path('VendorAccess/Add-Product/', views.add_product, name='add_product'),
    path('VendorAccess/ViewProduct/', views.my_products, name='my_products'),


    #user Dashboard
    path('view_cart', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products/', views.product_list, name='product_list'),
    path('my-order', views.my_orders_view, name='my_orders'),

    #checkout
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment-complete/', views.payment_success, name='payment_complete'),


]
