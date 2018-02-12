from django.db import models
from django.core.urlresolvers import reverse

# for validations
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

GSTN_CODEPOINT_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def validate_GSTIN(value):
    print(value)
    gstinWOCheckDigit = value[:len(value)-1]
    checkDigit = value[len(value)-1]
    generatedDigit = getCheckDigitOfGSTIN(gstinWOCheckDigit)
    if checkDigit != generatedDigit:
        print(generatedDigit)
        raise ValidationError(
            _('%(value)s check digit validation failed'),
            params={'value': value},
        )


def getCheckDigitOfGSTIN(gstinWOCheckDigit):
    factor = 2
    sum = 0
    checkCodePoint = 0

    if (gstinWOCheckDigit == None) or (gstinWOCheckDigit == ''):
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
    cpChars = GSTN_CODEPOINT_CHARS
    inputChars = gstinWOCheckDigit.strip().upper()

    mod = len(cpChars)
    i = len(inputChars) - 1
    while i >= 0:
        codePoint = -1
        j = 0
        for j in range(mod):
            if (cpChars[j] == inputChars[i]):
                codePoint = j
        digit = factor * codePoint
        factor = 1 if factor == 2 else 1
        digit = (digit // mod) + (digit % mod)
        sum += digit
        i -= 1
    checkCodePoint = (mod - (sum % mod)) % mod
    return cpChars[checkCodePoint]

class Remitter(models.Model):
    name = models.CharField(max_length=256)
    account_number = models.CharField(max_length=256, blank=False)
    mobile_number = models.CharField(max_length=10, blank=False)
    PAN = models.CharField(max_length=10, blank=False, null=False)
    GSTIN = models.CharField(max_length=256, blank=False, null=False, validators=[validate_GSTIN])

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
    GSTIN = models.CharField(max_length=256, validators=[validate_GSTIN])

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

    def __str__(self):
        return self.customer.name + " " + str(self.amount_in_figure)

    def __unicode__(self):
        return self.customer.name + " " + str(self.amount_in_figure)

    class Meta:
        verbose_name_plural = "RTGS"
