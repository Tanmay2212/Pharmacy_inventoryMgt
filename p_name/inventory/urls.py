from . import views
from django.urls import path
from .views import (
    import_medicine_from_excel,
    add_purchase,
    add_sale,
    export_to_excel,  # Make sure this is imported
    view_inventory,    # Also include view_inventory if not already present
)

urlpatterns = [
    path('import-medicine/', import_medicine_from_excel, name='import_medicine'),
    path('add-purchase/', add_purchase, name='add_purchase'),
    path('add-sale/', add_sale, name='add_sale'),
    path('export-excel/', export_to_excel, name='export_to_excel'), 
    path('view-inventory/', view_inventory, name='view_inventory'),
]
