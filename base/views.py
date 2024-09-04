from django.http import JsonResponse
from django.db.models.functions import Coalesce
from django.db.models import Count, Sum, Avg
from django.contrib import messages
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.db.models import Sum
from django.template.loader import render_to_string
from .models import *
from .forms import *
from .views import *
from .cart import Cart
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required(login_url='login')
def home(req):
    context = {
        "home": "active",
        'title': 'Home',
    }
    return render(req, 'base/index.html', context)


# ------------------------------------------------- categories views -------------------------------------------------
@login_required(login_url='login')
def categories(req):
    context = {
        "cat_page": "active",
        'title': 'Categories',
    }
    return render(req, 'base/products/categories.html', context)


@login_required(login_url='login')
def filter_categories(req):
    name_query = req.POST.get('name')
    base_query = Category.objects.filter(name__icontains=name_query)
    categories = base_query.annotate(
        prod_count=Count('product', distinct=True),
        prod_average_price=Avg('product__price'),
        sale_count=Count('product__sale', distinct=True)
    ).order_by('name')

    context = {
        'categories': categories,
    }
    return render(req, 'base/products/cat_table.html', context)


@login_required(login_url='login')
def categories_table(req):
    categories = Category.objects.annotate(
        prod_count=Count('product', distinct=True),
        prod_average_price=Avg('product__price'),
        sale_count=Count('product__sale', distinct=True)
    ).order_by('name')

    context = {
        'categories': categories,
    }
    return render(req, 'base/products/cat_table.html', context)


@login_required(login_url='login')
def category_details(req, pk):
    curr_obj = get_object_or_404(Category, id=pk)
    products = Product.objects.filter(category=curr_obj)


    price_stats = products.aggregate(
        total_price=Sum('price'), 
        average_price=Avg('price')
    )

    total_price = price_stats['total_price'] or 0
    average_price = price_stats['average_price'] or 0
    context = {
        "cat_page": "active",
        'title': 'Categories',
        'curr_obj': curr_obj,
        'products': products,
        'total_price': total_price,
        'average_price': average_price,
    }
    return render(req, 'base/products/cat_details.html', context)


@login_required(login_url='login')
def category_products(req, pk):
    curr_obj = get_object_or_404(Category, id=pk)
    prods = Product.objects.filter(category=curr_obj).order_by('name')
    products = prods.annotate(
        sale_count=Count('sale'),
        sale_aggregate=Sum('sale__total')
    )

    context = {
        'curr_obj': curr_obj,
        'products': products,
    }
    return render(req, 'base/products/table.html', context)


@login_required(login_url='login')
def create_category(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = CategoryForm()
    if req.method == 'POST':
        form = CategoryForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success(req,'New category added')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'Add a new category'})


@login_required(login_url='login')
def edit_category(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Category, id=pk)
    form = CategoryForm(instance=curr_obj)
    if req.method == 'POST':
        form = CategoryForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success(req, 'Edit completed successfully')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Edit this category'})


# ------------------------------------------------- products views -------------------------------------------------
@login_required(login_url='login')
def products(req):
    categories = Category.objects.all().order_by('name')
    context = {
        "prod_page": "active",
        'title': 'Products',
        'categories': categories,
    }
    return render(req, 'base/products/index.html', context)


@login_required(login_url='login')
def products_table(req):
    products = Product.objects.all().order_by('name')
    context = {
        "products": products,
    }
    return render(req, 'base/products/table.html', context)


@login_required(login_url='login')
def filter_products(req, pk):
    name_query = req.POST.get('name')
    brand_query = req.POST.get('brand')
    cat_query = req.POST.get('category')

    base_query = Product.objects.all().order_by('name')

    if name_query:
        base_query = base_query.filter(name__icontains=name_query)
    if brand_query:
        base_query = base_query.filter(brand__icontains=brand_query)
    if cat_query:
        base_query = base_query.filter(category__name__icontains=cat_query)

    products = base_query

    context = {
        "products": products,
    }
    if pk == 'reg':
        return render(req, 'base/products/table.html', context)
    else:
        return render(req, 'base/products/picker.html', context)


@login_required(login_url='login')
def products_picker(req):
    products = Product.objects.all().order_by('name')
    context = {
        "products": products,
    }
    return render(req, 'base/products/picker.html', context)


@login_required(login_url='login')
def product_details(req, pk):
    curr_obj = get_object_or_404(Product, id=pk)
    context = {
        'curr_obj': curr_obj,
    }
    return render(req, 'base/products/details.html', context)


@login_required(login_url='login')
def create_product(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ProductForm()
    if req.method == 'POST':
        form = ProductForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success(req,'New product added')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'base/products/form.html', context={'form': form, 'form_title': 'Add a new product'})


@login_required(login_url='login')
def edit_product(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Product, id=pk)
    form = ProductForm(instance=curr_obj)
    if req.method == 'POST':
        form = ProductForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
            msg_obj = {"message": "Nice! Edit completed successfully...🎉",
                       "type": "success"}
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed', 'HX-Trigger': f'"showMessage": {msg_obj}'})
        else:
            msg_obj = {"message": "Yikes!!! There was an error!!!😥",
                       "type": "error"}
            return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed', 'HX-Trigger':  f'"showMessage": {msg_obj}'})
    else:
        return render(req, 'base/products/form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Edit this product'})


@login_required(login_url='login')
def edit_prod_price(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect(req.META.get('HTTP_REFERER', '/'))

    curr_obj = get_object_or_404(Product, id=pk)
    if req.method == 'POST':
        new_price = float(req.POST['price'])
        curr_obj.price = new_price
        curr_obj.save()
        messages.success(req, 'Edit completed successfully')
        # HTMX response to close the modal and redirect
        return HttpResponse("<script>closeModalAndReload();</script>")

    else:
        return render(req, 'base/products/pricer.html', context={'curr_obj': curr_obj, 'form_title': 'Change product price'})


# ------------------------------------------------- sales views -------------------------------------------------
@login_required(login_url='login')
def sales(req):
    clients = Client.objects.all().order_by('first_name')
    users = User.objects.all().order_by('first_name')
    context = {
        "sales_page": "active",
        'title': 'Sales',
        'clients': clients,
        'users': users,
    }
    return render(req, 'base/sales/index.html', context)


@login_required(login_url='login')
def filter_sales(req, pk=None):
    min_date_query = req.POST.get('min_date')
    max_date_query = req.POST.get('max_date')
    client_query = req.POST.get('client_id')
    user_query = req.POST.get('user_id')

    if pk is not None:
        curr_client = get_object_or_404(Client, id=pk)
        base_query = Sale.objects.filter(
            client=curr_client).order_by('-timestamp')
    else:
        base_query = Sale.objects.all().order_by('-timestamp')

    if min_date_query:
        base_query = base_query.filter(timestamp__date__gte=min_date_query)
    if max_date_query:
        base_query = base_query.filter(timestamp__date__lte=max_date_query)
    if client_query:
        base_query = base_query.filter(client__id=client_query)
    if user_query:
        base_query = base_query.filter(user__id=user_query)

    sales = base_query

    context = {"sales": sales}

    return render(req, 'base/sales/table.html', context)


@login_required(login_url='login')
def sales_table(req):
    sales = Sale.objects.all().order_by('-timestamp')
    context = {
        'sales': sales,
    }
    return render(req, 'base/sales/table.html', context)


@login_required(login_url='login')
def sale_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = Sale.objects.get(id=pk)
    sold_items = SoldProduct.objects.filter(sale=curr_obj)

    context = {
        "sales": "active",
        'title': 'Details de sale',
        'curr_obj': curr_obj,
        'sold_items': sold_items,
    }
    return render(req, 'base/sales/details.html', context)


@login_required(login_url='login')
def edit_sale(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(Sale, id=pk)

    form = SaleForm(instance=curr_obj)
    if req.method == 'POST':
        form = SaleForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Edit this sale'})


@login_required(login_url='login')
def sale_invoice(req, pk):
    curr_obj = get_object_or_404(Sale, id=pk)
    items = SoldProduct.objects.filter(sale=curr_obj)
    total_bt = 0
    total_at = 0
    # Calculate the total before tax for each item
    for obj in items:
        total_bt += obj.product.price_bt()
    # Calculate the total after tax for each item
    for obj in items:
        total_at += obj.product.price

    categories = Category.objects.all().order_by('name')
    products = Product.objects.all().order_by('name')

    context = {
        'curr_obj': curr_obj,
        'items': items,
        'total_bt': total_bt,
        'total_at': total_at,
        'categories': categories,
        'products': products,
    }
    return render(req, 'base/sales/invoice.html', context)


@login_required(login_url='login')
def add_prod_to_sale(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    sale = get_object_or_404(Sale, id=pk)

    if req.method == 'POST':
        prod_id = int(req.POST['prod_id'])
        prod_qt = int(req.POST['prod_qt'])
        new_sold_prod = SoldProduct(
            sale=sale,
            product=get_object_or_404(Product, id=prod_id),
            quantity=prod_qt
        )
        new_sold_prod.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


def load_prod_by_cat(req):
    category_id = req.GET.get('category')
    products = Product.objects.filter(category_id=category_id).all()
    return JsonResponse(list(products.values('id', 'name')), safe=False)


@login_required(login_url='login')
def edit_prod_in_sale(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    curr_obj = get_object_or_404(SoldProduct, id=pk)

    form = SoldProductForm(instance=curr_obj)
    if req.method == 'POST':
        form = SoldProductForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Edit a product in the sale'})


@login_required(login_url='login')
def sale_point(req):
    categories = Category.objects.all().order_by('name')
    context = {
        "sale_point_page": "active",
        'title': "Point of sale",
        'categories': categories,
    }
    return render(req, 'base/sales/sale_point.html', context)


@login_required(login_url='login')
def invoicing(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect(req.META.get('HTTP_REFERER', '/'))

    categories = Category.objects.all().order_by('name')
    products = Product.objects.all().order_by('name')
    clients = Client.objects.all().order_by('first_name')

    context = {
        "invoicing_page": "active",
        'title': 'Invoicing',
        'categories': categories,
        'products': products,
        'clients': clients,
    }
    return render(req, 'base/sales/invoicing.html', context)


@login_required(login_url='login')
def create_invoice(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    print('sold!!!!')

    if req.method == 'POST':
        client_id = int(req.POST['client_id'])
        client = get_object_or_404(Client, id=client_id)
        print(client)

        # Create and save the Sale object
        sale = Sale(user=user, client=client)
        sale.save()

        # Get product and quantity from the form
        prod_id = int(req.POST['prod_id'])
        prod_qt = int(req.POST['prod_qt'])

        # Create and save the SoldProduct object
        product = get_object_or_404(Product, id=prod_id)
        new_sold_prod = SoldProduct(
            sale=sale,
            product=product,
            quantity=prod_qt
        )
        new_sold_prod.save()
        messages.success(req, 'New invoice created successfully...🎉')

        # Redirect to the sale details page after creation
        return redirect('sale_details', pk=sale.id)


# ------------------------------------------------- Clients -------------------------------------------------
@login_required(login_url='login')
def clients(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    context = {
        "clients_page": "active",
        'title': 'Clients',
    }
    return render(req, 'base/clients/index.html', context)


@login_required(login_url='login')
def client_details(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Client, id=pk)
    users = User.objects.all()
    sales = Sale.objects.filter(client=curr_obj)
    sales_aggregate = sales.aggregate(totals=Sum('total'))['totals'] or 0

    context = {
        "clients_page": "active",
        'title': 'Clients',
        'curr_obj': curr_obj,
        'users': users,
        'sales': sales,
        'sales_aggregate': sales_aggregate,
    }
    return render(req, 'base/clients/details.html', context)


@login_required(login_url='login')
def client_sales(req, pk):
    curr_obj = get_object_or_404(Client, id=pk)
    sales = Sale.objects.filter(client=curr_obj).order_by('-timestamp')

    context = {
        'curr_obj': curr_obj,
        'sales': sales,
    }
    return render(req, 'base/sales/table.html', context)


@login_required(login_url='login')
def clients_table(req):
    clients = Client.objects.annotate(
        sale_count=Count('sale'),
        sale_aggregate=Sum('sale__total')
    ).order_by('first_name')
    context = {
        'clients': clients,
    }
    return render(req, 'base/clients/table.html', context)


@login_required(login_url='login')
def create_client(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    form = ClientForm()
    if req.method == 'POST':
        form = ClientForm(req.POST)
        if form.is_valid():
            form.save()
        messages.success(req,'New client added')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'form': form, 'form_title': 'New client'})


@login_required(login_url='login')
def edit_client(req, pk):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')
    curr_obj = get_object_or_404(Client, id=pk)
    form = ClientForm(instance=curr_obj)
    if req.method == 'POST':
        form = ClientForm(req.POST, instance=curr_obj)
        if form.is_valid():
            form.save()
        messages.success(req, 'Edit completed successfully')
        return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})
    else:
        return render(req, 'form.html', context={'curr_obj': curr_obj, 'form': form, 'form_title': 'Edit this client'})


@login_required(login_url='login')
def filter_clients(req):
    sex_query = req.POST.get('sex')
    first_name_query = req.POST.get('first_name')
    last_name_query = req.POST.get('last_name')
    phone_query = req.POST.get('phone')
    city_query = req.POST.get('city')

    base_query = Client.objects.all().order_by('first_name')

    if sex_query:
        base_query = base_query.filter(sex=sex_query)
    if first_name_query:
        base_query = base_query.filter(first_name__icontains=first_name_query)
    if last_name_query:
        base_query = base_query.filter(last_name__icontains=last_name_query)
    if phone_query:
        base_query = base_query.filter(phone__icontains=phone_query)
    if city_query:
        base_query = base_query.filter(city__icontains=city_query)

    clients = base_query

    context = {"clients": clients}

    return render(req, 'base/clients/table.html', context)


# ------------------------------------------------- Cart views -------------------------------------------------
@login_required(login_url='login')
def cart(req):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    clients = Client.objects.all().order_by('-timestamp')
    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    cart_total = cart.get_total_price()

    context = {
        "cart_page": "active",
        'cart': cart,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'clients': clients,
    }
    return render(req, 'base/cart/index.html', context)


def cart_partial(req):
    cart = Cart(req)
    cart_count = len(cart)
    cart_items = cart.get_cart_items()
    total_price = cart.get_total_price()
    clients = Client.objects.all().order_by('-timestamp')

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_price': total_price,
        'clients': clients,
    }
    return render(req, 'store/partials/cart/items.html', context)


@login_required(login_url='login')
def add_to_cart(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        print(product_id)
        product = get_object_or_404(Product, id=product_id)
        cart.add_item(product)
        cart_count = len(cart)
        res = JsonResponse({'cart_count': cart_count})
        # print('added to cart')
        return res


@login_required(login_url='login')
def remove_item(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        # Save to a session
        cart.remove_item(product)
        # Use len(cart) to get the number of distinct items
        cart_count = len(cart)
        # Ensure the key matches in the AJAX call
        res = JsonResponse({'cart_count': cart_count})
        return res


@login_required(login_url='login')
def clear_item(req):
    cart = Cart(req)
    if req.POST.get('action') == 'post':
        product_id = int(req.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        # Save to a session
        cart.clear_item(product)
        # Use len(cart) to get the number of distinct items
        cart_count = len(cart)
        # Ensure the key matches in the AJAX call
        res = JsonResponse({'cart_count': cart_count})
        return res


@login_required(login_url='login')
def clear_cart(req):
    cart = Cart(req)
    cart.clear_cart()
    return redirect('cart')


# --------------------------Checkout--------------------------

@login_required(login_url='login')
def checkout(req):
    user = req.user
    cart = Cart(req)
    cart_items = cart.get_cart_items()
    cart_count = len(cart)
    cart_total = cart.get_total_price()

    if cart_count > 0:
        client_id = req.POST.get('client_id')
        client = Client.objects.filter(id=client_id).first()

        new_sale = Sale(
            user=user,
            client=client,
            total=cart_total,
        )

        new_sale.save()

        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            new_sold_prod = SoldProduct(
                sale=new_sale,
                product=product,
                quantity=quantity,
            )
            new_sold_prod.save()

        cart.clear_cart()
        messages.success(req, 'New sale created successfully...🎉')
        return redirect('sale_details', pk=new_sale.id)
    else:
        messages.info(req, "Your cart is empty.")
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


# ------------------------------------------------- Delete and 404 routes -------------------------------------------------
@require_http_methods(['DELETE'])
@login_required(login_url='login')
def delete_base_object(req, pk, model_name):
    user = req.user
    if not user.is_staff:
        messages.info(req, "Access denied!!!")
        return redirect('home')

    try:
        # Get the model class from the model name
        ModelClass = apps.get_model('base', model_name)
    except LookupError:
        return HttpResponse(status=404)  # Model not found

    obj = get_object_or_404(ModelClass, pk=pk)

    # Check user's permission and show snackabr
    if not user.is_superuser:
        messages.error = 'Access-denied'
        response = HttpResponse(status=403, headers={
                                'HX-Trigger': 'access-denied'})
        return response

    # Delete the object
    obj.delete()

    # Return a success response
    return HttpResponse(status=204, headers={'HX-Trigger': 'db_changed'})


@login_required(login_url='login')
def not_found(req, exception):
    context = {
        "not_found_page": "active",
        "title": 'Page 404',

    }
    return render(req, 'not_found.html', context)
