from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.SuperUserLoginView.as_view(), name='superuser_login'),
    path('logout/', views.SuperUserLogoutView.as_view(), name='superuser_logout'),
]
