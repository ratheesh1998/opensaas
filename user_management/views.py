from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

from .forms import SuperUserLoginForm, UserRegistrationForm


class RegisterView(View):
    """Registration for new users. After signup, log in and redirect to create organization."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('create_organization')
        form = UserRegistrationForm()
        return render(request, 'user_management/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'user_management/register.html', {'form': form})
        user = form.save()
        login(request, user)
        messages.success(request, f'Account created. Create your first organization below.')
        return redirect('create_organization')


class LoginView(View):
    """Login for all users. Superusers go to admin dashboard; normal users go to create organization."""

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('create_organization')
        form = SuperUserLoginForm()
        return render(request, 'user_management/login.html', {'form': form})

    def post(self, request):
        form = SuperUserLoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'user_management/login.html', {'form': form})

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'user_management/login.html', {'form': form})

        login(request, user)
        messages.success(request, f'Welcome back, {user.get_username()}.')

        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return redirect(next_url)
        if user.is_superuser:
            from admin_app.models import Creadentials
            if not Creadentials.objects.exists():
                request.session['show_credentials_modal'] = True
            return redirect('admin_dashboard')
        return redirect('create_organization')


class SuperUserLoginView(LoginView):
    """Alias for LoginView so existing URLs (superuser_login) keep working."""
    pass


class SuperUserLogoutView(View):
    """Log out the current user."""

    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('home')

    def post(self, request):
        return self.get(request)


class ProfileView(LoginRequiredMixin, View):
    """Show the current user's profile details."""

    def get(self, request):
        return render(request, 'user_management/profile.html', {'user': request.user})
