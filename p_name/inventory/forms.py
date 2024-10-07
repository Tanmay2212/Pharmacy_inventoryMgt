from django import forms
from .models import Purchase, Sale

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['medicine', 'vendor', 'quantity','purchase_date']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['medicine', 'quantity']
