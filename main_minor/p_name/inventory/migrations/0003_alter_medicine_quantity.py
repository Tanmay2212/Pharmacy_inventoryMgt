# Generated by Django 5.0.7 on 2024-10-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_sale_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
