from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from admin_app.forms import CreadentialsForm
from django.contrib import messages
from admin_app.models import Creadentials, DeploymentTemplate, Environment, TemplateService
from admin_app.forms import DeploymentTemplateForm, TemplateServiceForm, EnvironmentForm


class CreadentialsFormView(LoginRequiredMixin, FormView):
    template_name = 'views/list_view.html'
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
        
        return render(request, 'views/list_view.html', context)


class TemplateListView(LoginRequiredMixin, FormView):
    template_name = 'views/template_list.html'
    form_class = DeploymentTemplateForm

    def get(self, request, *args, **kwargs):
        templates = DeploymentTemplate.objects.all().order_by('-created_at')
        search = request.GET.get('search', '')
        if search:
            templates = templates.filter(Q(name__icontains=search) | Q(description__icontains=search))

        paginator = Paginator(templates, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = self.get_context_data()
        context['page_obj'] = page_obj
        context['search'] = search
        context['deployment_template_form'] = self.form_class()
        context['published_count'] = DeploymentTemplate.objects.filter(published=True).count()
        return render(request, 'views/template_list.html', context)

    def post(self, request, *args, **kwargs):
        form = DeploymentTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deployment template saved successfully!')
            return redirect('template_list')

        templates = DeploymentTemplate.objects.all().order_by('-created_at')
        search = request.GET.get('search', '')
        if search:
            templates = templates.filter(Q(name__icontains=search) | Q(description__icontains=search))
        paginator = Paginator(templates, 10)
        page_obj = paginator.get_page(1)

        context = self.get_context_data()
        context['page_obj'] = page_obj
        context['search'] = search
        context['deployment_template_form'] = form
        context['show_create_modal'] = True
        context['published_count'] = DeploymentTemplate.objects.filter(published=True).count()
        return render(request, 'views/template_list.html', context)
    

class TemplateDetailedView(LoginRequiredMixin, FormView):
    template_name = 'template_detailed_view.html'
    form_class = DeploymentTemplateForm
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        template = DeploymentTemplate.objects.get(pk=pk)
        service_form = TemplateServiceForm()
        environment_form = EnvironmentForm()

        context = self.get_context_data()
        context['service_form'] = service_form
        context['services'] = template.templateservice_set.all()
        context['environment_form'] = environment_form
        context['template'] = template
        return render(request, 'views/detailed/template_detailed_view.html', context)
    
    
class ServiceFormView(LoginRequiredMixin, FormView):
    form_class = TemplateServiceForm

    def post(self, request, template_pk, *args, **kwargs):
        form = TemplateServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.deployment_template_id = template_pk
            service.save()
            messages.success(request, 'Service added successfully!')
            return redirect('template_detailed_view', pk=template_pk)
        messages.error(request, 'Please fix the errors below.')
        return redirect('template_detailed_view', pk=template_pk)


class EnvironmentFormView(LoginRequiredMixin, FormView):
    form_class = EnvironmentForm

    def post(self, request, service_pk, *args, **kwargs):
        service = TemplateService.objects.get(pk=service_pk)
        form = EnvironmentForm(request.POST)
        if form.is_valid():
            env = form.save(commit=False)
            env.template_service_id = service
            env.save()
            messages.success(request, 'Environment variable added successfully!')
            return redirect('template_detailed_view', pk=service.deployment_template_id)
        messages.error(request, 'Please fix the errors below.')
        return redirect('template_detailed_view', pk=service.deployment_template_id)


class EnvironmentUpdateView(LoginRequiredMixin, FormView):
    form_class = EnvironmentForm

    def post(self, request, pk, *args, **kwargs):
        env = Environment.objects.get(pk=pk)
        form = EnvironmentForm(request.POST, instance=env)
        if form.is_valid():
            form.save()
            messages.success(request, 'Environment variable updated successfully!')
            return redirect('template_detailed_view', pk=env.template_service_id.deployment_template_id)
        messages.error(request, 'Please fix the errors below.')
        return redirect('template_detailed_view', pk=env.template_service_id.deployment_template_id)


class EnvironmentDeleteView(LoginRequiredMixin, FormView):
    def post(self, request, pk, *args, **kwargs):
        env = Environment.objects.get(pk=pk)
        template_pk = env.template_service_id.deployment_template_id
        env.delete()
        messages.success(request, 'Environment variable deleted successfully!')
        return redirect('template_detailed_view', pk=template_pk)