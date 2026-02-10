from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SuperUserLoginForm


class SuperUserLoginView(View):
    """Login page that allows only superusers."""

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('list_organization')
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

        if not user.is_superuser:
            messages.error(
                request,
                'Access denied. Only superusers can sign in here.',
            )
            return render(request, 'user_management/login.html', {'form': form})

        login(request, user)
        messages.success(request, f'Welcome back, {user.get_username()}.')
        # If no credentials exist, show credentials modal when they land on list view
        from admin_app.models import Creadentials
        if not Creadentials.objects.exists():
            request.session['show_credentials_modal'] = True
        next_url = request.POST.get('next') or request.GET.get('next') or 'list_organization'
        return redirect(next_url)


class SuperUserLogoutView(View):
    """Log out the current user."""

    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('superuser_login')

    def post(self, request):
        return self.get(request)
