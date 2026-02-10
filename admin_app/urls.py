from django.urls import path
from .import views

urlpatterns = [
    path('settings/credentials/', views.CreadentialsFormView.as_view(), name='credentials_form'),
]
