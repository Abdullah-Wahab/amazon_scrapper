# Generated by Django 4.2.16 on 2024-10-30 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('asin', models.CharField(max_length=10, unique=True)),
                ('sku', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.URLField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.brand')),
            ],
        ),
    ]
