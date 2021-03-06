# -*- coding: utf-8 -*-
"""
models of catalog are..
"""
import datetime

import mptt.fields
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from librehatti.config import (
    BUYER,
    DELIVERY_ADDRESS,
    IS_DEBIT,
    PURCHASED_ITEMS,
    QTY,
    REFERENCE,
    REFERENCE_DATE,
)
from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField


class FinancialSession(models.Model):
    """
    This class defines start date and end date for a financial session.
    """

    session_start_date = models.DateField()
    session_end_date = models.DateField()

    def __str__(self):
        return "%s : %s" % (self.session_start_date, self.session_end_date)


class mCategory(models.Model):
    """
    This class defines the name of category and parent category of product
    """

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.name)


class Unit(models.Model):
    """
    This class defines a unit variable for Categories
    """

    unit = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.unit)


class Category(MPTTModel):
    """
    This class defines the name of category, its parent and unit of
    each category the organisation deals with
    """

    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    unit = models.ForeignKey(
        Unit, null=True, blank=True, on_delete=models.CASCADE
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return "%s" % self.name


class Product(models.Model):
    """
    This class defines the name of product, category, price of each item of
    that product and the organisation with which user deals
    """

    name = models.CharField(max_length=500)
    category = mptt.fields.TreeForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    price_per_unit = models.IntegerField(blank=True, null=True)
    organisation = models.ForeignKey(
        "useraccounts.AdminOrganisations", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Attributes(models.Model):
    """
    This class defines the features of product
    """

    name = models.CharField(max_length=200)
    is_number = models.BooleanField(default=True)
    is_string = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Attributes"

    def __str__(self):
        return self.name


class ModeOfPayment(models.Model):
    """
    This class defines the details about user, its organisation, along with
    total discount and payment of job, and mode of payment
    """

    method = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = "Modes of payment"

    def __str__(self):
        return self.method


class Surcharge(models.Model):
    """
    This class defines the type of taxes, value, validation of taxes
    mentioning the startdate and end date
    """

    tax_name = models.CharField(max_length=200)
    value = models.FloatField()
    taxes_included = models.BooleanField(default=False)
    tax_effected_from = models.DateField(null=True)
    tax_valid_till = models.DateField(null=True)
    Remark = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.tax_name


class PurchaseOrder(models.Model):
    """
    This class defines members for orders to placed by users
    """

    buyer = models.ForeignKey(
        User, verbose_name=BUYER, on_delete=models.CASCADE
    )
    is_debit = models.BooleanField(default=False, verbose_name=IS_DEBIT)
    reference = models.CharField(max_length=200, verbose_name=REFERENCE)
    reference_date = models.DateField(
        blank=True, null=True, verbose_name=REFERENCE_DATE
    )
    delivery_address = models.CharField(
        max_length=500, blank=True, null=True, verbose_name=DELIVERY_ADDRESS
    )
    organisation = models.ForeignKey(
        "useraccounts.AdminOrganisations", default=1, on_delete=models.CASCADE
    )
    date_time = models.DateField(auto_now_add=True)
    purchase_order_time = models.TimeField(auto_now_add=True)
    total_discount = models.IntegerField(default=0)
    tds = models.IntegerField(default=0)
    mode_of_payment = models.ForeignKey(ModeOfPayment, on_delete=models.CASCADE)
    cheque_dd_number = models.CharField(max_length=50, blank=True)
    cheque_dd_date = models.DateField(max_length=50, blank=True, null=True)
    type_of_service = models.ForeignKey(
        "useraccounts.OrganisationType", on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        surchages = Surcharge.objects.filter(taxes_included=1)

        if surchages:
            pass
        else:
            raise ValidationError("No Active Taxes. Unable to add Order")
        now = datetime.datetime.now()
        financialsession = FinancialSession.objects.values(
            "id", "session_start_date", "session_end_date"
        )
        for value in financialsession:
            start_date = value["session_start_date"]
            end_date = value["session_end_date"]
            if start_date <= now.date() <= end_date:
                session_id = value["id"]
        try:
            session_id
            super(PurchaseOrder, self).save(*args, **kwargs)
        except BaseException:
            raise ValidationError("No Current Financial Session")

    def __str__(self):
        return "%s" % (self.id)


class PurchasedItem(models.Model):
    """
    This class defines members for items purchased in a purchase order
    """

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    price_per_unit = models.IntegerField()
    qty = models.IntegerField(verbose_name=QTY)
    price = models.IntegerField()
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        try:
            if self.purchase_order:
                self.price = self.price_per_unit * self.qty
                super(PurchasedItem, self).save(*args, **kwargs)
        except BaseException:
            raise ValidationError("No Active Taxes. Unable to add Items")

    def __str__(self):
        return "%s" % (self.item) + " - " "%s" % (self.purchase_order)

    class Meta:
        verbose_name = PURCHASED_ITEMS
        verbose_name_plural = PURCHASED_ITEMS


class Catalog(models.Model):
    """
    This class defines the features, value of product
    """

    attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.attribute.name


class TaxesApplied(models.Model):
    """
    This class defines the taxes applied on the purchase order
    """

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    surcharge = models.ForeignKey(Surcharge, on_delete=models.CASCADE)
    surcharge_name = models.CharField(max_length=500)
    surcharge_value = models.FloatField()
    tax = models.IntegerField()

    def __str__(self):
        return "%s" % (self.surcharge)


class Bill(models.Model):
    """
    This class defines the grand total of the purchase order
    """

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    delivery_charges = models.IntegerField()
    total_cost = models.IntegerField()
    totalplusdelivery = models.IntegerField()
    total_tax = models.IntegerField()
    grand_total = models.IntegerField()
    amount_received = models.IntegerField()


class HeaderFooter(models.Model):
    """
    This class is used to add, edit or delete Header and Footer to be
    used for Bills in the organisation
    """

    header = HTMLField()
    footer = HTMLField()
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            temp = HeaderFooter.objects.filter(is_active=1)
            if temp:
                HeaderFooter.objects.filter(is_active=1).update(is_active=0)
                super(HeaderFooter, self).save(*args, **kwargs)
            else:
                super(HeaderFooter, self).save(*args, **kwargs)
        else:
            super(HeaderFooter, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        verbose_name_plural = "Header and Footer"


class SurchargePaid(models.Model):
    surcharge = models.ForeignKey(Surcharge, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s paid on %s" % (self.surcharge, self.date)


class ChangeRequest(models.Model):
    """
    This class defines members which enables the user to select a purchase order
    to request a change in the Bill Amount
    """

    purchase_order_of_session = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE)
    previous_total = models.IntegerField()
    new_total = models.IntegerField()
    description = models.CharField(max_length=100)
    initiator = models.CharField(max_length=50)
    initiation_date = models.DateField(auto_now_add=True)


class RequestSurchargeChange(models.Model):
    """
    This class defines members for requesting the change in a Bill
    """

    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE)
    surcharge = models.ForeignKey(TaxesApplied, on_delete=models.CASCADE)
    previous_value = models.IntegerField()
    new_value = models.IntegerField()


class RequestStatus(models.Model):
    """
    This class defines members to specify status of the chnage request
    """

    change_request = models.ForeignKey(ChangeRequest, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    request_response = models.DateField(null=True)


class NonPaymentOrder(models.Model):
    """
    This class defines members for the purchase orders to be completed in
    future but the date is not determined
    """

    buyer = models.ForeignKey(
        User, verbose_name=BUYER, on_delete=models.CASCADE
    )
    reference = models.CharField(max_length=200, verbose_name=REFERENCE)
    reference_date = models.DateField(verbose_name=REFERENCE_DATE)
    date = models.DateField(auto_now_add=True)
    delivery_address = models.CharField(
        max_length=500, blank=True, null=True, verbose_name=DELIVERY_ADDRESS
    )
    item_type = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % (self.id)


class NonPaymentOrderOfSession(models.Model):
    """
    This class defines members for Non Payment order of a
    particular session
    """

    non_payment_order = models.ForeignKey(
        NonPaymentOrder, on_delete=models.CASCADE
    )
    non_payment_order_of_session = models.IntegerField()
    session = models.ForeignKey(FinancialSession, on_delete=models.CASCADE)


class SpecialCategories(models.Model):
    """
    This class defines members for special categories where no tax is applied
    and voucher is not generated
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    voucher = models.BooleanField(default=False)
    tax = models.BooleanField(default=False)
