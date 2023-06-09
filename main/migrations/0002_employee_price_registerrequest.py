# Generated by Django 4.1.7 on 2023-02-27 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='RegisterRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=255, verbose_name='ФИО')),
                ('register_at', models.DateField()),
                ('medical_center', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='register_request', to='main.medicalcenter')),
                ('special', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='register_request', to='main.special')),
            ],
        ),
    ]
