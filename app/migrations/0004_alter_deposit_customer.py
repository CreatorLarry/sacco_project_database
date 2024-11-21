# Generated by Django 5.1.3 on 2024-11-20 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to='app.customer'),
        ),
    ]
