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
