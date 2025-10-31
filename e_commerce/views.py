from django.shortcuts import render, redirect
from .forms import VendorRegistrationForm
from .forms import CustomerRegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login as auth_login
from .forms import ProductForm
from .models import Vendor
from .models import Product
from django.shortcuts import render, get_object_or_404
from .models import CartItem, Order, OrderItem
from .forms import CheckoutForm
from django.contrib import messages
import stripe
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

#getting usertype
def get_user_type(request):
    username = request.GET.get('username')
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
        user_type = 'Vendor' if user.is_vendor else 'Customer'
        return JsonResponse({'user_type': user_type})
    except User.DoesNotExist:
        return JsonResponse({'user_type': 'Not found'})

#vender register
def vendor_registration(request):
        
    if request.method == 'POST':
        form = VendorRegistrationForm (request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = VendorRegistrationForm ()
    return render(request, 'register.html', {'form': form})


#customer register
def customer_registration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = CustomerRegistrationForm()
        print("Form fields in customer_registration:", form.fields.keys()) 
    return render(request, 'user_register.html', {'form': form})



#login
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_vendor:
                return redirect('vendor_dashboard')
            else:
                return redirect('customer_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')



#User dashboard
@login_required
def customer_dashboard(request):
    products = Product.objects.all() 
    return render(request, 'customer_dashboard.html',  {'products': products})


#vendor dashboard
def vendor_dashboard(request):
    #checking if user is vendor or not!!
    if not request.user.is_vendor:
        return HttpResponseForbidden()
    return render(request, 'vendor_dashboard.html')


#Add Product
def add_product(request):
    if not request.user.is_vendor:
        return redirect('homepage') 

    try:
        vendor = request.user.vendor
    except Vendor.DoesNotExist:
        return redirect('homepage')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm()
    
    return render(request, 'VendorAccess/AddProduct.html', {'form': form})


#vendorAccess
def my_products(request):
    if not request.user.is_vendor:
        return redirect('homepage')

    products = Product.objects.filter(vendor=request.user.vendor)
    return render(request, 'VendorAccess/ViewProducts.html', {'products': products})



#cart
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(customer=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    CartItem.objects.filter(customer=request.user, product_id=product_id).delete()
    return redirect('cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})



#checkout
@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(customer=request.user)

    if not cart_items.exists():
        return JsonResponse({'error': "Cart is empty"}, status=400)

    total = sum(item.product.price * item.quantity for item in cart_items)
    total_cents = int(total * 100)

    if request.method == 'POST':
        intent_id = request.POST.get('payment_intent_id')
        if intent_id:
            intent = stripe.PaymentIntent.retrieve(intent_id)
            if intent.status != 'succeeded':
                return JsonResponse({"error": "Payment not confirmed"}, status=400)

            order = Order.objects.create(
                customer=request.user,
                total=total,
                paid=True,
                stripe_payment_intent=intent_id
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            cart_items.delete()
            return JsonResponse({"order_id": order.id})
        
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        shipping_address_1 = request.POST.get('shipping_address_1', '')
        shipping_address_2 = request.POST.get('shipping_address_2', '')
        shipping_city = request.POST.get('shipping_city', '')
        shipping_state = request.POST.get('shipping_state', '')
        shipping_zip = request.POST.get('shipping_zip', '')
        shipping_country = request.POST.get('shipping_country', '')
        cardholder_name = request.POST.get('cardholder_name', '')
        delivery_instructions = request.POST.get('delivery_instructions', '')

        intent = stripe.PaymentIntent.create(
            amount=total_cents,
            currency='usd',
            metadata={
                'customer': request.user.username,
                'full_name': full_name[:500],
                'email': email[:500],
                'phone': phone[:500],
                'shipping_address_1': shipping_address_1[:500],
                'shipping_address_2': shipping_address_2[:500],
                'shipping_city': shipping_city[:500],
                'shipping_state': shipping_state[:500],
                'shipping_zip': shipping_zip[:500],
                'shipping_country': shipping_country[:500],
                'cardholder_name': cardholder_name[:500],
                'delivery_instructions': delivery_instructions[:500],
            }
        )
        return JsonResponse({'clientSecret': intent.client_secret})

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    })


#order completed
def payment_success(request):
    order_id = request.GET.get('order_id')

    if not order_id or not order_id.isdigit():
        messages.error(request, "Invalid or missing order ID.")
        return redirect('homepage')

    try:
        order = Order.objects.get(id=int(order_id), customer=request.user)
        return render(request, 'payment_complete.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('homepage')

@login_required
def my_orders_view(request):
    user_orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'my_order.html', {'my_orders': user_orders})
