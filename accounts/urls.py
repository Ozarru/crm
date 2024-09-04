from django.urls import path, register_converter
from .views import *
from utils import HashIdConverter

register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('login/', loginView, name='login'),
    path('logout/', logoutUser, name='logout'),
    # ----------------------------------------------------------------------------
    path('users/', users, name='users'),
    path('users/list/', users_table, name='users_table'),
    path('users/filter/', filter_users, name='filter_users'),
    path('users/create/', create_user, name='create_user'),
    path('users/<hashid:pk>/', user_details, name='user_details'),
    path('users/<hashid:pk>/edit/', edit_user, name='edit_user'),
]
