from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

# Function to calculate the total cost of a sale


def calculate_sale_total(sale):
    total = 0
    sold_products = SoldProduct.objects.filter(sale=sale)
    for sold_product in sold_products:
        total += sold_product.product.price * sold_product.quantity
    return total

# Signal to update the sale total after a SoldProduct is added or updated


@receiver(post_save, sender=SoldProduct)
def update_sale_total_on_save(sender, instance, **kwargs):
    sale = instance.sale
    sale.total = calculate_sale_total(sale)
    sale.save()

# Signal to update the sale total after a SoldProduct is deleted


@receiver(post_delete, sender=SoldProduct)
def update_sale_total_on_delete(sender, instance, **kwargs):
    sale = instance.sale
    sale.total = calculate_sale_total(sale)
    sale.save()


@receiver(post_save, sender=SoldProduct)
@receiver(post_delete, sender=SoldProduct)
def update_sale_total(sender, instance, **kwargs):
    sale = instance.sale
    sale_total = sum(
        [sp.quantity * sp.product.price for sp in sale.soldproduct_set.all()])
    sale.total = sale_total
    sale.save()


@receiver(post_save, sender=Product)
def update_sale_total_on_price_change(sender, instance, **kwargs):
    sold_products = SoldProduct.objects.filter(product=instance)
    for sold_product in sold_products:
        sale = sold_product.sale
        sale_total = sum(
            [sp.quantity * sp.product.price for sp in sale.soldproduct_set.all()])
        sale.total = sale_total
        sale.save()
