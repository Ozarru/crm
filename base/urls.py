from django.urls import path, re_path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('', home, name='home'),
    # ----------------------------------------------------------------------------
    path('clients/', clients, name='clients'),
    path('clients/create/', create_client, name='create_client'),
    path('clients/table/', clients_table, name='clients_table'),
    path('clients/filter/', filter_clients, name='filter_clients'),
    path('clients/<hashid:pk>/', client_details, name='client_details'),
    path('clients/<hashid:pk>/edit/', edit_client, name='edit_client'),
    path('clients/<hashid:pk>/sales/', client_sales, name='client_sales'),
    # ----------------------------------------------------------------------------
    path('categories/', categories, name='categories'),
    path('categories/table/', categories_table, name='categories_table'),
    path('categories/filter/', filter_categories, name='filter_categories'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/<hashid:pk>/', category_details, name='category_details'),
    path('categories/<hashid:pk>/edit/', edit_category, name='edit_category'),
    path('categories/<hashid:pk>/products/', category_products, name='category_products'),
    # ----------------------------------------------------------------------------
    path('products/', products, name='products'),
    path('products/table/', products_table, name='products_table'),
    path('products/filter/<str:pk>/', filter_products, name='filter_products'),
    path('products/by_category/', load_prod_by_cat, name='load_prod_by_cat'),
    path('products/picker/', products_picker, name='products_picker'),
    path('products/create/', create_product, name='create_product'),
    path('products/<hashid:pk>/', product_details, name='product_details'),
    path('products/<hashid:pk>/edit/', edit_product, name='edit_product'),
    path('products/<hashid:pk>/edit_price/', edit_prod_price, name='edit_prod_price'),
    # path('products/grid/', products_grid, name='products_grid'),
    # path('products/filter/', filter_products, name='filter_products'),
    # ----------------------------------------------------------------------------
    path('cart/', cart, name='cart'),
    path('cart/add_item/', add_to_cart, name='add_to_cart'),
    path('cart/remove_item/', remove_item, name='remove_item'),
    path('cart/clear_item/', clear_item, name='clear_item'),
    path('cart/clear_cart/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
    # ----------------------------------------------------------------------------
    path('pos/', sale_point, name='sale_point'),
    path('sales/', sales, name='sales'),
    path('sales/table/', sales_table, name='sales_table'),
    path('sales/<hashid:pk>/', sale_details, name='sale_details'),
    path('sales/<hashid:pk>/edit/', edit_sale, name='edit_sale'),
    path('sales/<hashid:pk>/invoice/', sale_invoice, name='sale_invoice'),
    re_path(r'^sales/filter(?:/(?P<pk>\d+))?/$',
            filter_sales, name='filter_sales'),
    # ----------------------------------------------------------------------------
    path('invoicing/', invoicing, name='invoicing'),
    path('create_invoice/', create_invoice, name='create_invoice'),
    # path('sales/filter/', filter_sales, name='filter_sales'),
    path('sales/<hashid:pk>/add_product/',
         add_prod_to_sale, name='add_prod_to_sale'),
    path('sales/<hashid:pk>/edit_product/',
         edit_prod_in_sale, name='edit_prod_in_sale'),
    # ----------------------------------------------------------------------------


    # --------------------------
    path('base/objects/<hashid:pk>/<str:model_name>/delete/',
         delete_base_object, name='delete_base_object'),
]
