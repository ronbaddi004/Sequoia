from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .filters import RemitterFilter, CustomerFilter
from .forms import RemitterForm, CustomerForm
from .models import Remitter, Customer
# Create your views here.
@login_required
def home(request):
    return render(request, 'SequoiaApp/home.html')


@login_required
def remitter_create(request):
    form = RemitterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            Remitter.objects.create(
                name = form.cleaned_data.get('name'),
                account_number = form.cleaned_data.get('account_number'),
                mobile_number = form.cleaned_data.get('mobile_number'),
                PAN = form.cleaned_data.get('PAN'),
                GSTIN = form.cleaned_data.get('GSTIN')
            )
        return HttpResponseRedirect(reverse(remitter_search))
    return render(request, 'SequoiaApp/remitter_create.html', {'form':form})


@login_required
def remitter_search(request):
    remitter_list = Remitter.objects.all()
    remitter_filter = RemitterFilter(request.GET, queryset=remitter_list)
    return render(request, 'SequoiaApp/remitter_search.html', {'filter': remitter_filter})


@method_decorator(login_required, name='dispatch')
class RemitterUpdateView(UpdateView):
    fields = ('name', 'account_number', 'mobile_number', 'PAN')
    model = Remitter


@login_required
def remitter_delete(request, pk=None):
    remitter = get_object_or_404(Remitter, pk=pk)
    remitter.delete()
    return redirect("remitter_search")

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            Customer.objects.create(
                name = form.cleaned_data.get('name'),
                bank_name = form.cleaned_data.get('bank_name'),
                bank_account_number = form.cleaned_data.get('bank_account_number'),
                bank_branch_name = form.cleaned_data.get('bank_branch_name'),
                bank_ifsc_code = form.cleaned_data.get('bank_ifsc_code'),
                PAN = form.cleaned_data.get('PAN'),
                mobile_number = form.cleaned_data.get('mobile_number'),
                GSTIN = form.cleaned_data.get('GSTIN')
            )
            return HttpResponseRedirect(reverse(customer_search))
    return render(request, 'SequoiaApp/customer_create.html', {'form': form})


@login_required
def customer_search(request):
    customer_list = Customer.objects.all()
    customer_filter = CustomerFilter(request.GET, queryset=customer_list)
    return render(request, 'SequoiaApp/customer_search.html', {'filter': customer_filter})


@method_decorator(login_required, name='dispatch')
class CustomerUpdateView(UpdateView):
    fields = ('name', 'bank_name', 'bank_account_number', 'bank_branch_name',
                'bank_ifsc_code', 'PAN', 'mobile_number', 'GSTIN')
    model = Customer


@login_required
def customer_delete(request, pk=None):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect("customer_search")