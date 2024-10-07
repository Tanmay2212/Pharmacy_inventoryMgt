from django.utils import timezone
from django.forms import ValidationError
from django.http import HttpResponse
import pandas as pd
import openpyxl
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Medicine, Sale, Purchase, Vendor
from .forms import PurchaseForm, SaleForm

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
        for row in sheet.iter_rows(min_row=2, values_only=True):
            try:
                Medicine.objects.create(
                    name=row[0],
                    company_name=row[1],
                    batch_number=row[2],
                    quantity=row[3],
                    price_per_unit=row[4],
                    manufacture_date=row[5],
                    expiry_date=row[6],
                    salts=row[7]
                )
                messages.success(request, f'Successfully imported {row[0]}')
            except Exception as e:
                messages.error(request, f'Error importing {row[0]}: {e}')
        return render(request, 'inventory/import_success.html')
    return render(request, 'inventory/import.html')

def export_to_excel(request):
    medicines = Medicine.objects.all().values()
    sales = Sale.objects.all().values()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="medicines_sales.xlsx"'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        pd.DataFrame(medicines).to_excel(writer, sheet_name='Medicines', index=False)
        pd.DataFrame(sales).to_excel(writer, sheet_name='Sales', index=False)

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
