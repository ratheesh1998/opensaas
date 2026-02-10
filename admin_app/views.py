from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from admin_app.forms import CreadentialsForm
from django.contrib import messages

from admin_app.models import Creadentials


class CreadentialsFormView(LoginRequiredMixin, FormView):
    template_name = 'organization_list.html'  # Redirect back to list view
    form_class = CreadentialsForm

    def post(self, request, *args, **kwargs):
        form = CreadentialsForm(request.POST, instance=Creadentials.objects.first())
        if form.is_valid():
            form.save()
            messages.success(request, 'Credentials saved successfully!')
            return redirect('list_organization')
        
        # If form has errors, render with the form errors
        # Get the list view context
        from organization.views import ListOrganizationView
        view = ListOrganizationView()
        view.request = request
        context = view.get_context_data()
        context['credentials_form'] = form  # Pass form with errors
        
        return render(request, 'organization_list.html', context)