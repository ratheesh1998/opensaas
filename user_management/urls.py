from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.SuperUserLoginView.as_view(), name='superuser_login'),
    path('logout/', views.SuperUserLogoutView.as_view(), name='superuser_logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
