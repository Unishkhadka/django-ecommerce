# Generated by Django 5.0.2 on 2024-02-20 15:42

import django.db.models.deletion
import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_alter_billingaddress_id_alter_cart_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.payment'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=50, primary_key=True, serialize=False),
        ),
    ]
