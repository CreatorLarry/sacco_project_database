# Generated by Django 5.1.3 on 2024-11-19 11:33

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_deposit'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to=app.models.generate_unique_name),
        ),
    ]
