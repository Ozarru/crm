from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.views.decorators.cache import cache_page
from base.cart import *
from base.models import *
from .forms import *
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


# ------------------------------------------------- auth views -------------------------------------------------

def loginView(req):
    if req.user.is_authenticated:
        return redirect('home')

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            if 'next' in req.POST:
                messages.success(req, f'Hello <<{user.email.split("@")[0]}>>, welcome to CRM...😎')
                return redirect(req.POST.get('next'))

            else:
                return redirect('home')
        else:
            messages.error(req, 'Email or password incorrect!!!')
    context = {
        "login_page": "active",
        "title": 'Login'}
    return render(req, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(req):
    logout(req)
    return redirect('home')


# ------------------------------------------------- users views -------------------------------------------------

@login_required(login_url='login')
def users(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied, for staff only...❗⛔❗")
        return redirect('home')

    context = {
        "users_page": "active",
        'title': 'Users',
    }
    return render(req, 'accounts/users.html', context)


@login_required(login_url='login')
def users_table(req):
    users = User.objects.annotate(
        # Count the number of sales per user
        sale_count=Count('sale'),
        # Sum the total value of sales per user
        sale_aggregate=Sum('sale__total')
    ).order_by('first_name')
    context = {
        'users': users,
    }
    return render(req, 'accounts/users_table.html', context)


@login_required(login_url='login')
def user_details(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)
    is_self = True if user == curr_obj else False

    sales = Sale.objects.filter(user=curr_obj)
    sales_aggregate = sales.aggregate(totals=Sum('total'))['totals'] or 0

    # Get the list of loyal clients
    loyal_clients = (
        sales.values('client')  # Group by client
        # Count number of purchases per client
        .annotate(purchase_count=Count('id'))
        # Filter clients with more than one purchase
        .filter(purchase_count__gt=1)
    )
    # Count the number of loyal clients
    loyal_clients_count = loyal_clients.count()

    context = {
        "users_page": "active",
        'title': 'user',
        'curr_obj': curr_obj,
        'is_self': is_self,
        'sales': sales,
        'sales_aggregate': sales_aggregate,
        'loyal_clients_count': loyal_clients_count,
    }
    return render(req, 'accounts/user_details.html', context)



@login_required(login_url='login')
def create_user(req):
    user = req.user
    if not user.is_superuser:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = CreateUserForm()
    if req.method == 'POST':
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, 'New user account created successfully...🎉')
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
        else:
            messages.error(req, 'There was an error!!!😥')
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Create a new user account'})


@login_required(login_url='login')
def edit_user(req, pk):
    user = req.user
    curr_obj = get_object_or_404(CustomUser, id=pk)

    if user != curr_obj:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    if req.method == 'POST':
        form = EditUserForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
            messages.success(req, 'User account edited successfully...🎉')
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
        else:
            messages.error(req, 'There was an error!!!😥')
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        form = EditUserForm(instance=curr_obj)
    return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Edit this user account'})


@login_required(login_url='login')
def filter_users(req):
    sex_query = req.POST.get('sex')
    first_name_query = req.POST.get('first_name')
    last_name_query = req.POST.get('last_name')
    phone_query = req.POST.get('phone')

    base_query = User.objects.all().order_by('first_name')

    if sex_query:
        base_query = base_query.filter(sex=sex_query)
    if first_name_query:
        base_query = base_query.filter(first_name__icontains=first_name_query)
    if last_name_query:
        base_query = base_query.filter(last_name__icontains=last_name_query)
    if phone_query:
        base_query = base_query.filter(phone__icontains=phone_query)

    users = base_query

    context = {"users": users}

    return render(req, 'accounts/users_table.html', context)
