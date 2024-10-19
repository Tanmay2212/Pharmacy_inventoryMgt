from django.contrib import admin
from .models import Medicine, Vendor, Purchase, Sale

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'batch_number', 'quantity', 'price_per_unit', 'expiry_date')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'address')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'vendor', 'purchase_date', 'quantity')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'sale_date', 'quantity', 'price')

# Remove the following lines to avoid double registration
# admin.site.register(Medicine)
# admin.site.register(Vendor)
# admin.site.register(Purchase)
# admin.site.register(Sale)
