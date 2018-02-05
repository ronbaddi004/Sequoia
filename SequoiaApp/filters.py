import django_filters
from .models import Remitter, Customer, RTGS

class RemitterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    account_number = django_filters.CharFilter(lookup_expr='icontains')
    mobile_number = django_filters.CharFilter(lookup_expr='icontains')
    PAN = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Remitter
        fields = ['name', 'account_number', 'mobile_number', 'PAN']


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    bank_name = django_filters.CharFilter(lookup_expr='icontains')
    bank_account_number = django_filters.CharFilter(lookup_expr='icontains')
    PAN = django_filters.CharFilter(lookup_expr='icontains')
    mobile_number = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ['name', 'bank_name', 'bank_account_number', 'PAN', 'mobile_number']
