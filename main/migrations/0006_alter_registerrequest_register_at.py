# Generated by Django 4.1.7 on 2023-03-20 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_registerrequest_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerrequest',
            name='register_at',
            field=models.DateField(auto_now=True),
        ),
    ]
