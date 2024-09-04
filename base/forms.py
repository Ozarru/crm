from .models import *
from django import forms


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateInput(forms.DateInput):
    input_type = 'date'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'address', 
            'po_box',
            'city',
            'email', 
            'sex', 
            'phone', 
            'phone_alt')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),
            'address': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),
            'po_box': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),
            'city': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),
            'email': forms.EmailInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),
            'sex': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),
            'phone_alt': forms.TextInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),

        }

# ------------------------------------------ Product forms ------------------------------------------------------

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')
        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')
        labels= {'vat':'VAT (%)',}
        exclude = ('timestamp',)

        widgets = {
            'name': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'brand': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'reference': forms.TextInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'category': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'description': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'price': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'vat': forms.NumberInput(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),

        }


# ------------------------------------------ Sale forms ------------------------------------------------------
class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        observation = models.CharField(max_length=500, blank=True, null=True)
        exclude = ('products','timestamp','total',)
        widgets = {
            'user': forms.Select(attrs={'class': "input_selector mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'client': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'observation': forms.Textarea(attrs={"rows": "5", 'class': "mb-2 px-4 py-2 rounded-lg border focus:border-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),

        }


class SoldProductForm(forms.ModelForm):
    class Meta:
        model = SoldProduct
        fields = '__all__'
        exclude = ('sale', )

        labels = {
            'sale': 'Vente',
            'product': 'Produit',
            'quantity': 'Quantité',
        }
        widgets = {
            'sale': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'product': forms.Select(attrs={'class': "mb-1 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:outline-none focus:ring-1 focus:ring-sky-500 w-full"}),
            'quantity': forms.NumberInput(attrs={'class': "mb-2 px-3 py-2 rounded-lg border focus:border-none focus:outline-none focus:bg-gray-50 focus:ring-1 focus:ring-sky-500 w-full"}),
        }

