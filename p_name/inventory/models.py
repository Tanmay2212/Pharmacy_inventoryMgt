from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

# Vendor Model
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

# Medicine Model
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    salts = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative.')

# Purchase Model
class Purchase(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    quantity = models.IntegerField()

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Purchase quantity cannot be negative.')
        
        # Ensure the quantity being purchased does not exceed medicine's current quantity
        if self.medicine and (self.medicine.quantity + self.quantity < 0):
            raise ValidationError('Not enough stock available.')

    def save(self, *args, **kwargs):
        # Ensure that quantity in Medicine does not go negative
        if self.medicine:
            self.medicine.quantity += self.quantity
            self.medicine.save()
        super().save(*args, **kwargs)

# Sale Model
class Sale(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)    

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Sale quantity cannot be negative.')
        
        # Ensure sale quantity does not exceed medicine's current quantity
        if self.medicine and self.quantity > self.medicine.quantity:
            raise ValidationError('Not enough stock available for sale.')

    def save(self, *args, **kwargs):
        # Deduct the sold quantity from the medicine stock
        if self.medicine:
            self.medicine.quantity -= self.quantity  # Deduct the sold quantity
            self.medicine.save()  # Save the updated quantity back to the database
            
        super().save(*args, **kwargs)

