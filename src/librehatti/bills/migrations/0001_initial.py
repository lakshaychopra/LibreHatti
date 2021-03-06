# -*- coding: utf-8 -*-
# Generated by Django 3.0.4 on 2020-03-16 17:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("catalog", "__first__"),
        ("useraccounts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NoteLine",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note", models.CharField(max_length=400)),
                ("is_permanent", models.BooleanField(default=False)),
            ],
            options={"verbose_name_plural": "Quoted Order Note"},
        ),
        migrations.CreateModel(
            name="QuotedOrder",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_debit",
                    models.BooleanField(
                        default=False, verbose_name="Non-Payment Job"
                    ),
                ),
                (
                    "reference",
                    models.CharField(max_length=200, verbose_name="Letter No."),
                ),
                (
                    "reference_date",
                    models.DateField(verbose_name="Letter Date"),
                ),
                (
                    "delivery_address",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Site",
                    ),
                ),
                ("date_time", models.DateField(auto_now_add=True)),
                ("total_discount", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Client",
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useraccounts.AdminOrganisations",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuotedTaxesApplied",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("surcharge_name", models.CharField(max_length=500)),
                ("surcharge_value", models.FloatField()),
                ("tax", models.IntegerField()),
                (
                    "quoted_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bills.QuotedOrder",
                    ),
                ),
                (
                    "surcharge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.Surcharge",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuotedOrderofSession",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quoted_order_session", models.IntegerField()),
                (
                    "quoted_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bills.QuotedOrder",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.FinancialSession",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuotedOrderNote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note", models.CharField(max_length=400)),
                (
                    "quoted_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bills.QuotedOrder",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuotedItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price_per_unit", models.IntegerField()),
                ("qty", models.IntegerField(verbose_name="Quantity")),
                ("price", models.IntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.Product",
                    ),
                ),
                (
                    "quoted_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bills.QuotedOrder",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuotedBill",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("delivery_charges", models.IntegerField()),
                ("total_cost", models.IntegerField()),
                ("totalplusdelivery", models.IntegerField()),
                ("total_tax", models.IntegerField()),
                ("grand_total", models.IntegerField()),
                ("amount_received", models.IntegerField()),
                (
                    "quoted_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bills.QuotedOrder",
                    ),
                ),
            ],
        ),
    ]
