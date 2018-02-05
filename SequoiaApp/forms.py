from django import forms
from .models import Customer, Remitter, RTGS

class RTGSForm(forms.ModelForm):
    class Meta:
        model = RTGS
        fields = ['customer', 'remitter', 'cheque_number', 'amount_in_figure', 'amount_in_word']

class RemitterForm(forms.ModelForm):
    class Meta:
        model = Remitter
        fields = ['name', 'account_number', 'mobile_number', 'PAN', 'GSTIN']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'bank_name', 'bank_account_number', 'bank_branch_name', 'bank_ifsc_code', 'PAN', 'mobile_number', 'GSTIN']
