# -*- coding: utf-8 -*-
"""
Models for the useraccounts are..
"""
from django.contrib.auth.models import User
from django.db import models
from librehatti.config import COUNTRY


class OrganisationType(models.Model):
    """
    describes the type of organisation where the user deals
    """

    type_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.type_desc


class Address(models.Model):
    """
    describes the address details of the admin organisation
    """

    street_address = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pin = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, default=COUNTRY)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.street_address + "," + self.district


class HattiUser(models.Model):
    """
    describes the details of the user's organisation
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=500)
    date_joined = models.DateTimeField(auto_now_add=True)
    fax = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=100, blank=True, null=True)
    stc_no = models.CharField(max_length=100, blank=True, null=True)
    gst_in = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    state_code = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.CharField(max_length=100, null=True, blank=True)
    tagline = models.CharField(max_length=140, blank=True, null=True)

    class Meta:
        abstract = True


class AdminOrganisations(HattiUser):
    """
    This class inherits the details of HattiUser specifying the title of
    organisation and its type
    """

    title = models.CharField(max_length=200)
    organisation_type = models.ForeignKey(
        OrganisationType, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Admin Organisations"

    def __str__(self):
        return self.title


class Customer(HattiUser):
    """
    This class inherits the details of HattiUser whether customer is
    organisation type or individual thus customer will confirm the Is org
    checkbox and then specifying the type of oganisation and its company
    name
    """

    title = models.CharField(max_length=200, blank=True, null=True)
    is_org = models.BooleanField(default=False)
    org_type = models.ForeignKey(OrganisationType, on_delete=models.CASCADE)
    company = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.user)
