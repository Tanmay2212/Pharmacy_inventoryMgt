# Generated by Django 5.0.7 on 2024-10-05 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]