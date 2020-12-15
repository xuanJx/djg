from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Customer, Product, Order, UserExtension
from .forms import CustomerForm, OrderForm, RegisterForm

# Create your views here.



def register(request):
    r_form = RegisterForm()
    message = ''
    success = ''

    if request.method == 'POST':
        r_form = RegisterForm(request.POST)
        if r_form.is_valid():
            name_get = r_form.cleaned_data['username']
            passwd1_get = r_form.cleaned_data['password1']
            passwd2_get = r_form.cleaned_data['password2']
            email_get = r_form.cleaned_data['email']
            phone_get = r_form.cleaned_data['phone']

            try:
                if passwd1_get == passwd2_get:
                    new_user = User.objects.create_user(username=name_get, password=passwd2_get, email=email_get)
                    UserExtension.objects.create(user=new_user, phone=phone_get)
                    success = 'registered successfully'
                    return redirect('djgapp:login-page')
                else:
                    message = 'Entered passwords differ'
            except:
                message = 'User name or mail has been registered'

    context = {
        'r_form': r_form,
        'message': message,
        'success': success
    }

    return render(request, 'djgapp/register.html', context)

def homepage(request):
    return render(request, 'djgapp/home.html')

def loginpage(request):
    message = ''

    if request.user.is_authenticated:
        return redirect('djgapp:index-page')
    else:
        if request.method == 'POST':
            name_get = request.POST.get('username')
            passwd_get = request.POST.get('password')

            user = authenticate(request, username=name_get, password=passwd_get)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('djgapp:login-page')
                else:
                    message = 'This account has baned'
            else:
                message = 'User or password error'

    context = {
        'message': message
    }
    return render(request, 'djgapp/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('djgapp:login-page')

@login_required(login_url='djgapp:login-page')
def indexpage(request):
    customer = Customer.objects.all()
    c_count = customer.count()

    order = Order.objects.all()
    o_count = order.count()
    order_p_count = Order.objects.filter(status='Pending').count()
    order_d_count = Order.objects.filter(status='Delivered').count()
    order_o_count = Order.objects.filter(status='Out for delivery').count()

    n = 0
    last_five = []
    for i in order:
        if n < 5:
            last_five.append(i)
            n += 1
        else:
            break

    if request.is_ajax and request.POST.get('order_del'):
        del_order_id = request.POST.get('order_del')
        print(del_order_id)
        del_order = Order.objects.get(id=del_order_id)
        del_order.delete()

    context = {
        'customer': customer,
        'c_count': c_count,
        'order': last_five,
        'order_p_count': order_p_count,
        'order_d_count': order_d_count,
        'o_count': o_count,
        'order_o_count': order_o_count
    }

    return render(request, 'djgapp/index.html', context)

def create_customer_page(request):
    c_form = CustomerForm()

    if request.method == 'POST':
        c_form = CustomerForm(request.POST)
        if c_form.is_valid():
            name_get = c_form.cleaned_data['name']
            phone_get = c_form.cleaned_data['phone']
            email_get = c_form.cleaned_data['email']
            custmoer = Customer.objects.create(name=name_get, phone=phone_get, email=email_get)
            custmoer.save()
            return redirect('djgapp:index-page')

    context = {
        'c_form': c_form
    }

    return render(request, 'djgapp/create-customer.html', context)

def create_order_page(request):
    o_form = OrderForm()

    if request.method == 'POST':
        o_form = OrderForm(request.POST)
        if o_form.is_valid():
            customer_get = o_form.cleaned_data['customer']
            product_get = o_form.cleaned_data['product']
            status_get = o_form.cleaned_data['status']
            order = Order.objects.create(customer=customer_get, product=product_get, status=status_get)
            order.save()
            return redirect('djgapp:index-page')

    context = {
        'o_form': o_form
    }

    return render(request, 'djgapp/create-order.html', context)

def update_order(request, pk):
    order = Order.objects.get(id=pk)

    o_form = OrderForm(instance=order)

    if request.method == 'POST':
        o_form = OrderForm(request.POST)
        if o_form.is_valid():
            customer_get = o_form.cleaned_data['customer']
            product_get = o_form.cleaned_data['product']
            status_get = o_form.cleaned_data['status']
            order = Order.objects.filter(id=pk)
            order.update(id=pk, customer=customer_get, product=product_get, status=status_get)
            return redirect('djgapp:index-page')

    context = {
        'order': order,
        'o_form': o_form
    }
    return render(request, 'djgapp/update-order.html', context)

def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('djgapp:index-page')

    context = {
        'order': order,
    }
    return render(request, 'djgapp/delete-order.html', context)
