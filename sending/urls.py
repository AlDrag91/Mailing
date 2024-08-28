from sending.apps import SendingConfig
from django.urls import path

from sending.views import index, ClientServiceListView, ClientServiceCreateView, ClientServiceUpdateView, \
    ClientServiceDeleteView, BlastsListView, BlastsCreateView, BlastsDeleteView

app_name = SendingConfig.name

urlpatterns = [
    path('', index, name='index'),

    path('clients', ClientServiceListView.as_view(), name='clients'),
    path('clients_create/', ClientServiceCreateView.as_view(), name='clients_create'),
    path('clients_update/<int:pk>/', ClientServiceUpdateView.as_view(), name='clients_update'),
    path('clients_delete/<int:pk>/', ClientServiceDeleteView.as_view(), name='clients_delete'),

    path('blasts/', BlastsListView.as_view(), name='blasts'),
    path('blasts_create/', BlastsCreateView.as_view(), name='blasts_create'),
    path('blasts_delete/<int:pk>/', BlastsDeleteView.as_view(), name='blasts_delete'),

]
