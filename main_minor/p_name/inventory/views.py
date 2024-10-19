from django.utils import timezone
from django.forms import ValidationError
from django.http import HttpResponse
import pandas as pd
import openpyxl
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Medicine, Sale, Purchase, Vendor
from .forms import PurchaseForm, SaleForm
from django.shortcuts import get_object_or_404
def home(request):
    return render(request, 'inventory/home.html')

def view_inventory(request):
    medicines = Medicine.objects.all()
    purchases = Purchase.objects.all()
    return render(request, 'inventory/view_inventory.html', {
        'medicines': medicines,
        'purchases': purchases,
    })

def import_medicine_from_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active
        
        for index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            try:
                Medicine.objects.create(
                    name=row[0],
                    company_name=row[1],
                    batch_number=row[2],
                    quantity=row[3],  # Quantity should be an integer
                    price_per_unit=row[4],  # Price per unit should be a decimal
                    manufacture_date=row[5],  # Manufacture date should be a valid date
                    expiry_date=row[6],  # Expiry date should be a valid date
                    salts=row[7] if row[7] else None  # Optional salts field
                )
                messages.success(request, f"Successfully imported {row[0]}")
            
            except Exception as e:
                messages.error(request, f"Error importing row {index}: {e}")
        
        return redirect('view_inventory')
    return render(request, 'inventory/import.html')

def delete_medicine(request, medicine_id):
    # Fetch the medicine by ID and delete it
    medicine = get_object_or_404(Medicine, id=medicine_id)
    medicine.delete()

    # Provide a success message and redirect back to the inventory page
    messages.success(request, f"{medicine.name} has been successfully deleted.")
    return redirect('view_inventory')
# def export_to_excel(request):
#     medicines = Medicine.objects.all().values()
#     sales = Sale.objects.all().values()
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="medicines_sales.xlsx"'
    
#     with pd.ExcelWriter(response, engine='openpyxl') as writer:
#         pd.DataFrame(medicines).to_excel(writer, sheet_name='Medicines', index=False)
#         pd.DataFrame(sales).to_excel(writer, sheet_name='Sales', index=False)

#     return response
def export_to_excel(request):
    medicines = Medicine.objects.all().values(
        'name', 'company_name', 'batch_number', 'quantity', 'price_per_unit',
        'manufacture_date', 'expiry_date', 'salts'
    )
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="medicine_inventory.xlsx"'

    df_medicines = pd.DataFrame(medicines)  # Create DataFrame from medicines queryset

    # Use ExcelWriter to export DataFrame to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df_medicines.to_excel(writer, sheet_name='Medicines', index=False)

    return response


def add_purchase(request):
    if request.method == 'POST':
        medicine_id = request.POST.get('medicine_id')  # Check if the medicine_id is being captured
        vendor_id = request.POST.get('vendor_id')  # Check if the vendor_id is being captured
        quantity = request.POST.get('quantity')
        purchase_date = request.POST.get('purchase_date')

        try:
            quantity = int(quantity)
            medicine = Medicine.objects.get(id=medicine_id)
            vendor = Vendor.objects.get(id=vendor_id)

            Purchase.objects.create(
                medicine=medicine,
                vendor=vendor,
                quantity=quantity,
                purchase_date=purchase_date or timezone.now(),
            )

            messages.success(request, "Purchase added successfully!")
            return redirect('add_purchase')

        except ValueError:
            messages.error(request, "Error: Quantity must be a valid number.")
        except Medicine.DoesNotExist:
            messages.error(request, "Error: Medicine not found.")
        except Vendor.DoesNotExist:
            messages.error(request, "Error: Vendor not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('add_purchase')

    medicines = Medicine.objects.all()
    vendors = Vendor.objects.all()
    return render(request, 'inventory/add_purchase.html', {'medicines': medicines, 'vendors': vendors})


def add_sale(request):
    if request.method == 'POST':
        medicine_id = request.POST.get('medicine')
        quantity = int(request.POST.get('quantity', 0))
        sale_date = request.POST.get('sale_date')

        try:
            # Fetch the medicine object
            medicine = Medicine.objects.get(id=medicine_id)

            # Check if there is enough quantity in stock
            if quantity > medicine.quantity:
                messages.error(request, "Error: Not enough stock available.")
                return redirect('add_sale')

            # Create the Sale object
            sale = Sale.objects.create(
                medicine=medicine,
                quantity=quantity,
                sale_date=sale_date or timezone.now(),
                price=medicine.price_per_unit * quantity  # Calculate total price for the sale
            )

            messages.success(request, "Sale added successfully!")
            return redirect('add_sale')

        except Medicine.DoesNotExist:
            messages.error(request, "Error: Medicine not found.")
        except ValueError:
            messages.error(request, "Error: Invalid quantity entered.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        return redirect('add_sale')

    medicines = Medicine.objects.all()
    return render(request, 'inventory/add_sale.html', {'medicines': medicines})
