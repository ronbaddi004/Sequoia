from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from SequoiaApp import views
from SequoiaApp.views import RemitterUpdateView, CustomerUpdateView


urlpatterns = [
    # miscellaneous urls
    url(r'^$', views.home, name='home'),
    url(r'^disclaimer/$', views.disclaimer, name='disclaimer'),

    # remitter urls
    url(r'^remitter/create/$', views.remitter_create, name='remitter_create'),
    url(r'^remitter/$', views.remitter_search, name='remitter_search'),
    url(r'^remitter/(?P<pk>\d+)/update/$',
        login_required(RemitterUpdateView.as_view()), name='remitter_update'),
    url(r'^remitter/(?P<pk>\d+)/delete/$',
        views.remitter_delete, name='remitter_delete'),

    #customer urls
    url(r'^customer/create/$', views.customer_create, name='customer_create'),
    url(r'^customer/$', views.customer_search, name='customer_search'),
    url(r'^customer/(?P<pk>\d+)/update/$',
        login_required(CustomerUpdateView.as_view()), name='customer_update'),
    url(r'^customer/(?P<pk>\d+)/delete/$',
        views.customer_delete, name='customer_delete'),

    #rtgs urls
    url(r'^rtgs/create/$', views.rtgs_create, name='rtgs_create'),
    url(r'^rtgs/(?P<pk>\d+)/$', views.rtgs, name='rtgs'),
    url(r'^rtgs/$', views.rtgs_search, name='rtgs_search'),
    # TODO need a delete view for RTGS

    # ajax urls
    url(r'^ajax/customer/autocomplete/$', views.customer_autocomplete,
        name='customer-autocomplete'),
    url(r'ajax/customer/get-id/',
        views.customer_get_data, name='customer-get-data'),
]
