# Generated by Django 4.1.7 on 2023-03-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_registerrequest_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='medicalcenter',
            name='city',
            field=models.ManyToManyField(blank=True, null=True, to='main.city'),
        ),
    ]