from blog import views
from sending.apps import SendingConfig
from django.urls import path

from sending.views import index, ClientServiceListView, ClientServiceCreateView, ClientServiceUpdateView, \
    ClientServiceDeleteView, BlastsListView, BlastsCreateView, BlastsDeleteView, MessageListView, MessageCreateView, \
    MessageDeleteView, DeliveryAttemptListView, MessageUpdateView, BlastsUpdateView

app_name = SendingConfig.name

urlpatterns = [
    path('', index, name='index'),

    path('clients', ClientServiceListView.as_view(), name='clients'),
    path('clients_create/', ClientServiceCreateView.as_view(), name='clients_create'),
    path('clients_update/<int:pk>/', ClientServiceUpdateView.as_view(), name='clients_update'),
    path('clients_delete/<int:pk>/', ClientServiceDeleteView.as_view(), name='clients_delete'),

    path('blasts/', BlastsListView.as_view(), name='blasts'),
    path('blasts_create/', BlastsCreateView.as_view(), name='blasts_create'),
    path('blasts_update/<int:pk>/', BlastsUpdateView.as_view(), name='blasts_update'),
    path('blasts_delete/<int:pk>/', BlastsDeleteView.as_view(), name='blasts_delete'),

    path('message/', MessageListView.as_view(), name='message'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('DeliveryAttempt/', DeliveryAttemptListView.as_view(), name='DeliveryAttempt')


]
