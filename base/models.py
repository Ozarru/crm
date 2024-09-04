from django.utils import timezone
from django.db import models
from django.urls import reverse
from utils import h_encode
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


# ----------------------------------- clients models -----------------------------------
genders = (
    ('female', 'F'),
    ('male', 'M'),
)

class Client(models.Model):
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    address = models.CharField(max_length=255)
    po_box = models.CharField(max_length=255)
    city = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=10, choices=genders, db_index=True)
    phone = models.CharField(unique=True, max_length=255)
    phone_alt = models.CharField(
        unique=True, max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


    def get_absolute_url(self):
        return reverse('client_details', kwargs={'pk': self.pk})
    


# ----------------------------------- categories models -----------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    image = models.ImageField(
        upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('category_details', kwargs={'pk': self.pk})


# ----------------------------------- products models -----------------------------------
class Product(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    brand = models.CharField(max_length=256, default='Generic', db_index=True)
    reference = models.CharField(max_length=256, unique=True)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL, db_index=True)
    description = models.CharField(max_length=500, default='_', blank=True, null=True)
    price = models.FloatField(default=0, blank=True, null=True)
    vat = models.FloatField(default=18, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_hashid(self):
        return h_encode(self.id)

    def price_bt(self):
        return self.price / (1 + self.vat / 100)
        
    @property
    def model_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('product_details', kwargs={'pk': self.pk})
    

# ----------------------------------- sales models -----------------------------------
class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, db_index=True)
    products = models.ManyToManyField(
        Product, through='SoldProduct', blank=True, db_index=True)
    total = models.FloatField(default=0)
    observation = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return f'Sale N° {self.id} - Client : {self.client}'

    def calculate_total(self):
        self.total = sum(item.get_total for item in self.soldproduct_set.all())
        self.save(update_fields=['total', 'products'])

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__


class SoldProduct(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def total(self):
        res = self.product.price * self.quantity
        return res

    def __str__(self):
        return f'Sold {self.quantity} {self.product.name}'

    def get_hashid(self):
        return h_encode(self.id)

    @property
    def model_name(self):
        return self.__class__.__name__
