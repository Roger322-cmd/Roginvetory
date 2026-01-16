from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Sale

@receiver(post_save, sender=Sale)
def check_stock_after_sale(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        remaining = product.units_remaining
        if remaining < 5: #threshold
            send_mail(
                subject="Low stock Alert!",
                message=f"Product {product.name} is runninglow. Remaining units: {remaining}",
                from_email="mtangerodger@gmail.com",
                recipient_list=[instance.tracker.user.email],
                fail_silently=True
            )