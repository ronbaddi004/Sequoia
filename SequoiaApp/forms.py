from django import forms
from .models import Customer, Remitter, RTGS

from .validators import validate_GSTIN, getCheckDigitOfGSTIN
from django.core.validators import RegexValidator

PAN_Validator = RegexValidator(
    r'\w{5}\d{4}\w', "Please make sure you have entered correct PAN")
GSTIN_Validator = RegexValidator(
    r'\d{2}\w{5}\d{4}\w\dZ\d', "Please make sure you have entered correct GSTIN")

class RTGSForm(forms.ModelForm):
    name = forms.CharField(max_length=256)
    bank_name = forms.CharField(max_length=256)
    bank_account_number = forms.CharField(
        max_length=256, required=True)
    bank_branch_name = forms.CharField(
        max_length=256, required=True)
    bank_ifsc_code = forms.CharField(max_length=256, required=True)
    PAN = forms.CharField(max_length=10, validators=[PAN_Validator])
    mobile_number = forms.CharField(max_length=10, required=True)
    GSTIN = forms.CharField(max_length=15, validators=[GSTIN_Validator])
    customer_id = forms.CharField()

    class Meta:
        model = RTGS
        fields = ['customer_id', 'remitter', 'cheque_number', 'amount_in_figure', 'amount_in_word', 'name',
                  'bank_name', 'bank_account_number', 'bank_branch_name', 'bank_ifsc_code', 'PAN', 'mobile_number', 'GSTIN']

    # def clean(self):
    #     cleaned_data = super(RTGSForm, self).clean()
    #     cheque_number = cleaned_data.get('cheque_number')
    #     amount_in_figure = cleaned_data.get('amount_in_figure')
    #     amount_in_word = cleaned_data.get('amount_in_word')
    #     bank_name = cleaned_data.get('bank_name')
    #     bank_account_number = cleaned_data.get('bank_account_number')
    #     bank_branch_name = cleaned_data.get('bank_branch_name')
    #     bank_ifsc_code = cleaned_data.get('bank_ifsc_code')
    #     PAN = cleaned_data.get('PAN')
    #     mobile_number = cleaned_data.get('mobile_number')
    #     GSTIN = cleaned_data.get('GSTIN')
    #     name = cleaned_data.get('name')

class RemitterForm(forms.ModelForm):
    PAN = forms.CharField(max_length=10, validators=[PAN_Validator])
    GSTIN = forms.CharField(max_length=15, validators=[GSTIN_Validator])
    class Meta:
        model = Remitter
        fields = ['name', 'account_number', 'mobile_number', 'PAN', 'GSTIN']

class CustomerForm(forms.ModelForm):
    PAN = forms.CharField(max_length=10, validators=[PAN_Validator])
    GSTIN = forms.CharField(max_length=15, validators=[GSTIN_Validator])
    class Meta:
        model = Customer
        fields = ['name', 'bank_name', 'bank_account_number', 'bank_branch_name', 'bank_ifsc_code', 'PAN', 'mobile_number', 'GSTIN']
