from django.db import models
from django.contrib.auth.models import User
from barcode import Code128
from barcode.writer import ImageWriter
import uuid
import os


class InventoryTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trackers')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.name} ({self.user.username})"

def generate_barcode_image(barcode_value):
    filename = f"barcode_{barcode_value}"
    path = f"media/barcodes/{filename}"
    Code128(barcode_value, writer=ImageWriter()).save(path)
    return f"barcodes/{filename}.png"


class Product(models.Model):
    tracker = models.ForeignKey(InventoryTracker, on_delete=models.CASCADE, related_name='products')
    product_id = models.CharField(max_length=50)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    added_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    units_added = models.PositiveIntegerField()
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    barcode_image = models.ImageField(upload_to="barcodes/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = str(uuid.uuid4())[:12]  # generate unique 12‑digit code
            self.barcode_image = generate_barcode_image(self.barcode)
        super().save(*args, **kwargs)


    class Meta:
        unique_together = ('tracker', 'product_id')

    def __str__(self):
        return self.name

    @property
    def total_earnings_if_all_sold(self):
        return self.units_added * self.price

    @property
    def units_remaining(self):
        sold = sum(s.quantity for s in self.sales.all())
        return max(self.units_added - sold, 0)

class Sale(models.Model):
    tracker = models.ForeignKey(InventoryTracker, on_delete=models.CASCADE, related_name='sales')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    sold_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def cost(self):
        return self.quantity * self.product.price
