from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .validators import validate_GSTIN, getCheckDigitOfGSTIN
from django.core.validators import RegexValidator

GSTIN_Validator = RegexValidator(
    r'\d{2}\w{5}\d{4}\w\dZ\d', "Please make sure you have entered correct GSTIN")

class Remitter(models.Model):
    name = models.CharField(max_length=256)
    account_number = models.CharField(max_length=256, blank=False)
    mobile_number = models.CharField(max_length=10, blank=False)
    PAN = models.CharField(max_length=10, blank=False, null=False)
    GSTIN = models.CharField(max_length=15, blank=False, null=False, validators=[GSTIN_Validator])
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Remitter", null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("remitter_search")


class Customer(models.Model):
    name = models.CharField(max_length=256)
    bank_name = models.CharField(max_length=256, blank=False, null=False)
    bank_account_number = models.CharField(max_length=256, blank=False, null=False)
    bank_branch_name = models.CharField(max_length=256, blank=False, null=False)
    bank_ifsc_code = models.CharField(max_length=256, blank=False, null=False)
    PAN = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=10, blank=False, null=False)
    GSTIN = models.CharField(max_length=15, validators=[GSTIN_Validator])
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Customer", null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("customer_search")

class RTGS(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="RTGS")
    remitter = models.ForeignKey(Remitter, on_delete=models.CASCADE, related_name="RTGS")
    cheque_number = models.CharField(max_length=15, blank=False)
    amount_in_figure = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_word = models.CharField(max_length=1024, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="RTGS", null=True)

    def __str__(self):
        return self.customer.name + " " + str(self.amount_in_figure)

    def __unicode__(self):
        return self.customer.name + " " + str(self.amount_in_figure)

    class Meta:
        verbose_name_plural = "RTGS"
