"""
Importing reqiured packages
"""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render, render_to_response, Http404
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.forms.models import model_to_dict

from .forms import RemitterForm, CustomerForm, RTGSForm
from .models import Remitter, Customer, RTGS
# Create your views here.

import json


@login_required
def home(request):
    """This is just a Home Page and login in required to access"""
    return render(request, 'SequoiaApp/home.html', context={'active_dashboard': 'active'})


def disclaimer(request):
    """
    This is disclaimer for the application
    """
    return render(request, 'disclaimer.html')


@login_required
def remitter_create(request):
    """This function is used to create Remitter"""
    form = RemitterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            Remitter.objects.create(
                name=form.cleaned_data.get('name'),
                account_number=form.cleaned_data.get('account_number'),
                mobile_number=form.cleaned_data.get('mobile_number'),
                PAN=form.cleaned_data.get('PAN'),
                GSTIN=form.cleaned_data.get('GSTIN'),
                created_by=request.user
            )
            return HttpResponseRedirect(reverse(remitter_search))
    return render(request, 'SequoiaApp/remitter_create.html', {'form': form})


@login_required
def remitter_search(request):
    """This function is used to search Remitters"""
    user = request.user
    if user.is_superuser:
        remitter_list = Remitter.objects.all()
    else:
        remitter_list = Remitter.objects.filter(created_by=user)
    return render(request, 'SequoiaApp/remitter_search.html', {'filter': remitter_list})


@method_decorator(login_required, name='dispatch')
class RemitterUpdateView(UpdateView):
    """This function is used for Updating Remitter Data"""
    fields = ('name', 'account_number', 'mobile_number', 'PAN', 'GSTIN')
    model = Remitter

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object.created_by == request.user
        else:
            return False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(RemitterUpdateView, self).dispatch(request, *args, **kwargs)
        elif not self.user_passes_test(request):
            return redirect("remitter_search")
        return super(RemitterUpdateView, self).dispatch(request, *args, **kwargs)


@login_required
def remitter_delete(request, pk=None):
    """This function is used to delete Remitter"""
    remitter = get_object_or_404(Remitter, pk=pk)
    if request.user == remitter.created_by or request.user.is_superuser:
        remitter.delete()
        return redirect("remitter_search")
    else:
        return redirect("remitter_search")


@login_required
def customer_create(request):
    """This function is used to create Customer"""
    form = CustomerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            Customer.objects.create(
                name=form.cleaned_data.get('name'),
                bank_name=form.cleaned_data.get('bank_name'),
                bank_account_number=form.cleaned_data.get(
                    'bank_account_number'),
                bank_branch_name=form.cleaned_data.get('bank_branch_name'),
                bank_ifsc_code=form.cleaned_data.get('bank_ifsc_code'),
                PAN=form.cleaned_data.get('PAN'),
                mobile_number=form.cleaned_data.get('mobile_number'),
                GSTIN=form.cleaned_data.get('GSTIN'),
                created_by=request.user
            )
            return HttpResponseRedirect(reverse(customer_search))
    return render(request, 'SequoiaApp/customer_create.html', {'form': form})


@login_required
def customer_search(request):
    """This function is used to search Customers"""
    user = request.user
    if user.is_superuser:
        customer_list = Customer.objects.all()
    else:
        customer_list = Customer.objects.filter(created_by=user)
    return render(request, 'SequoiaApp/customer_search.html', {'filter': customer_list})


@method_decorator(login_required, name='dispatch')
class CustomerUpdateView(UpdateView):
    """This function is used to Update Customer"""
    fields = ('name', 'bank_name', 'bank_account_number', 'bank_branch_name',
              'bank_ifsc_code', 'PAN', 'mobile_number', 'GSTIN')
    model = Customer

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object.created_by == request.user
        else:
            return False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(CustomerUpdateView, self).dispatch(request, *args, **kwargs)
        elif not self.user_passes_test(request):
            return redirect("remitter_search")
        return super(CustomerUpdateView, self).dispatch(request, *args, **kwargs)


@login_required
def customer_delete(request, pk=None):
    """This function is used to delete Customers"""
    customer = get_object_or_404(Customer, pk=pk)
    if request.user == customer.created_by or request.user.is_superuser:
        customer.delete()
        return redirect("customer_search")
    else:
        return redirect("customer_search")


@login_required
def rtgs_create(request):
    # get or create the form
    form = RTGSForm(request.POST or None)
    if form.is_valid():
        # Get the customer id (hidden field) from the form
        customer_id = form.cleaned_data.get('customer_id')
        try:
            # get the customer instance
            customer = Customer.objects.get(id=customer_id)
        except (Customer.DoesNotExist, ValueError):
            # else create a new one
            customer = Customer()

        # if anything has been changed: update it
        for key, value in form.cleaned_data.items():
            if key in vars(customer).keys():
                if (getattr(customer, key) == '' or getattr(customer, key) == None or getattr(customer, key) != value):
                    setattr(customer, key, value)
        
        # finally
        customer.created_by = request.user
        customer.save()

        # use the customer instance created above
        rtgs = RTGS.objects.create(
            customer=customer,
            remitter=form.cleaned_data.get('remitter'),
            cheque_number=form.cleaned_data.get('cheque_number'),
            amount_in_figure=form.cleaned_data.get('amount_in_figure'),
            amount_in_word=form.cleaned_data.get('amount_in_word'),
            created_by=request.user
        )

        # redirect to the RTGS view, so that when the user navigates back
        # the browser doesn't POST again
        return redirect("rtgs", pk=rtgs.pk)
    
    # fetch the remitters created by the current logged in user to display as dropdown in the RTGS create form
    remitters = Remitter.objects.filter(created_by=request.user)

    # also: activate the "Create RTGS" in the side bar
    return render(request, 'SequoiaApp/rtgs_create.html', {'form': form, 'remitters': remitters, 'active_create_rtgs': 'active'})


@login_required
def rtgs_form(request):
    return render(request, 'SequoiaApp/rtgs_form.html')


@login_required
def rtgs_search(request):
    user = request.user
    rtgs_list = RTGS.objects.filter(created_by=user)
    return render(request, 'SequoiaApp/rtgs_list.html', {'rtgs_list': rtgs_list})


@login_required
def rtgs(request, pk):
    rtgs = get_object_or_404(RTGS, pk=pk)
    if request.user == rtgs.created_by or request.user.is_superuser:
        return render(request, 'SequoiaApp/rtgs_form.html', {'rtgs': rtgs})
    else:
        return redirect("rtgs_search")


@login_required
def customer_autocomplete(request):
    # fetch all the customers from the DB
    qs = Customer.objects.all()

    # if not present: return with error and status 404
    if qs.count() == 0:
        return JsonResponse({'result': [], 'error': 'Customers not present.'}, status=404)

    # get the 'q' param from the request
    q = request.GET.get('q', None)
    # print('"GET /ajax/customer/autocomplete/" q {}'.format(q))

    # if present: filter the customer set and match the ones that start with the string in q
    if q != "" and q != None:
        qs = qs.filter(name__istartswith=q)

    # make it return dict containg name and id
    qs = qs.values('name', 'id')

    # iterate over the queryset and assign a name to each id
    result_list = {}
    for obj in qs:
        result_list[obj.get('id')] = obj.get('name')

    return JsonResponse({'result': result_list})


@login_required
def customer_get_data(request):
    if request.method == 'POST':
        try:
            # get the customer id from the POSt and cast it to an integer
            customer_id = int(request.POST.get('id', None))
            # print('"POST /ajax/customer/customer_get_data/" customer_id {}'.format(customer_id))
            # get the customer instance
            customer = Customer.objects.get(id=customer_id)

            # make an iterable with the customer instance above and serialize it
            customerJSON = serializers.serialize('json', [customer, ])

            # create a dictionary from the JSON object
            struct = json.loads(customerJSON)

            # assign the fields of the customer to the customerJSON
            # that is what we want
            customerJSON = struct[0]['fields']
            # print('"POST /ajax/customer/customer_get_data/" customerJSON {}'.format(type(customerJSON)))

            # return
            return JsonResponse(customerJSON)

        # self-explanatory
        except (Customer.DoesNotExist, ValueError) as ex:
            return JsonResponse({'error': 'customer not present.'}, status=404)

    # if not "POST" request, return an error
    return JsonResponse({'Error': 'Invalid request.'}, status=403)
