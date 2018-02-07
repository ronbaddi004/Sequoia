from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from SequoiaApp import views
from SequoiaApp.views import RemitterUpdateView, CustomerUpdateView


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^remitter/create/$', views.remitter_create, name='remitter_create'),
    url(r'^remitter/$', views.remitter_search, name='remitter_search'),
    url(r'^remitter/(?P<pk>\d+)/update/$',
        login_required(RemitterUpdateView.as_view()), name='remitter_update'),
    url(r'^remitter/(?P<pk>\d+)/delete/$',
        views.remitter_delete, name='remitter_delete'),
    url(r'^customer/create/$', views.customer_create, name='customer_create'),
    url(r'^customer/$', views.customer_search, name='customer_search'),
    url(r'^customer/(?P<pk>\d+)/update/$',
        login_required(CustomerUpdateView.as_view()), name='customer_update'),
    url(r'^customer/(?P<pk>\d+)/delete/$',
        views.customer_delete, name='customer_delete'),
    url(r'^rtgs/$', views.rtgs_list, name='rtgs_list'),
    url(r'^rtgs/(?P<pk>\d+)/$', views.rtgs, name='rtgs'),
    url(r'^rtgs/create/$', views.rtgs_create, name='rtgs_create'),
    url(r'^rtgs/form/$', views.rtgs_form, name='rtgs_form'),
]
