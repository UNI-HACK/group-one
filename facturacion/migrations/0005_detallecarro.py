# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 19:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_auto_20160702_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleCarro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacion.Usuario')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacion.Producto')),
            ],
        ),
    ]