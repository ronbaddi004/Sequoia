from django import forms
from .models import Customer, Remitter, RTGS

class RTGSForm(forms.ModelForm):
    name = forms.CharField(max_length=256)
    bank_name = forms.CharField(max_length=256)
    bank_account_number = forms.CharField(
        max_length=256, required=True)
    bank_branch_name = forms.CharField(
        max_length=256, required=True)
    bank_ifsc_code = forms.CharField(max_length=256, required=True)
    PAN = forms.CharField(max_length=10)
    mobile_number = forms.CharField(max_length=10, required=True)
    GSTIN = forms.CharField(max_length=256)

    class Meta:
        model = RTGS
        fields = ['remitter', 'cheque_number', 'amount_in_figure', 'amount_in_word', 'name',
                  'bank_name', 'bank_account_number', 'bank_branch_name', 'bank_ifsc_code', 'PAN', 'mobile_number', 'GSTIN']

    # def clean(self):
    #     cleaned_data = super(RTGSForm, self).clean()
    #     customer = cleaned_data.get('customer')
    #     name = cleaned_data.get('name')

class RemitterForm(forms.ModelForm):
    class Meta:
        model = Remitter
        fields = ['name', 'account_number', 'mobile_number', 'PAN', 'GSTIN']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'bank_name', 'bank_account_number', 'bank_branch_name', 'bank_ifsc_code', 'PAN', 'mobile_number', 'GSTIN']
