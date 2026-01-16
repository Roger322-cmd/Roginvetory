from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import InventoryTracker, Product, Sale

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Split full name into first and last (simple heuristic)
        full_name = self.cleaned_data.get('full_name', '').strip()
        parts = full_name.split()
        user.first_name = parts[0] if parts else ''
        user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class TrackerForm(forms.ModelForm):
    class Meta:
        model = InventoryTracker
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'category', 'added_date', 'price', 'units_added']
        widgets = {
            'added_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        tracker = kwargs.pop('tracker', None)
        super().__init__(*args, **kwargs)
        if tracker:
            # Only products with remaining units
            self.fields['product'].queryset = tracker.products.all()

