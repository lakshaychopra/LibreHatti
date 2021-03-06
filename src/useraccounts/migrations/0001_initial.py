# -*- coding: utf-8 -*-
# Generated by Django 3.0.4 on 2020-03-16 17:30
# flake8: noqa
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("street_address", models.CharField(max_length=100)),
                ("district", models.CharField(max_length=100)),
                ("pin", models.CharField(blank=True, max_length=10, null=True)),
                ("province", models.CharField(max_length=100)),
                (
                    "nationality",
                    models.CharField(default="Country", max_length=100),
                ),
            ],
            options={"verbose_name_plural": "Addresses"},
        ),
        migrations.CreateModel(
            name="OrganisationType",
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
                ("type_desc", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
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
                ("telephone", models.CharField(max_length=500)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "fax",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "pan_no",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "stc_no",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "gst_in",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "state",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "state_code",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "avatar",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "tagline",
                    models.CharField(blank=True, max_length=140, null=True),
                ),
                (
                    "title",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("is_org", models.BooleanField(default=False)),
                (
                    "company",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useraccounts.Address",
                    ),
                ),
                (
                    "org_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useraccounts.OrganisationType",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="AdminOrganisations",
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
                ("telephone", models.CharField(max_length=500)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "fax",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "pan_no",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "stc_no",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "gst_in",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "state",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "state_code",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "avatar",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "tagline",
                    models.CharField(blank=True, max_length=140, null=True),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useraccounts.Address",
                    ),
                ),
                (
                    "organisation_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useraccounts.OrganisationType",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name_plural": "Admin Organisations"},
        ),
    ]
