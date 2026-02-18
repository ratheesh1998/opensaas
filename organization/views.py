from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from admin_app.forms import CreadentialsForm
from admin_app.models import Creadentials, DeploymentTemplate, Project
from organization.forms import EnvForm, OrganizationForm
from organization.models import Env, Organization, Service
from organization.railway import  delete_organization, deploy_to_railway, deployment_status, project_create, update_service_id, update_service_variable, update_service_variable

# Create your views here.


class HomePageView(View):
    """Landing page for new visitors."""

    def get(self, request):
        return render(request, 'pages/home.html')


class CreateOrganizationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = OrganizationForm()

        return render(request, 'modals/create_modal.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_by = request.user
            organization.save()
            if not Project.objects.exists():
                project_id = project_create(service_name=request.POST.get('name'))
                project_id.save()
            organization.project_id = Project.objects.first()
            organization.default_domain = f"https://{request.POST.get('name')}-opensaas-production.up.railway.app"
            organization.save()
            project_id = Project.objects.first()
            if not project_id:
                return render(request, 'modals/create_modal.html', {'form': form, 'error': 'Failed to create or retrieve project'})
            workflow_id = deploy_to_railway(
                template_id=organization.deployment_template_id,
                service_name=request.POST.get('name'),
            )
            return redirect('list_organization')
        return render(request, 'modals/create_modal.html', {'form': form})

class ListOrganizationView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        organizations = Organization.objects.all().order_by("id")

        search = request.GET.get('search', '')
        if search:
            organizations = organizations.filter(name__icontains=search)

        paginator = Paginator(organizations, 12)  # items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        show_credentials_modal = request.session.pop('show_credentials_modal', False)
        # Also open credentials modal on list view when no credentials exist
        if not Creadentials.objects.exists():
            show_credentials_modal = True
        # Redirect superuser to admin when credentials prompt was needed (modal removed)
        if show_credentials_modal and request.user.is_superuser:
            return redirect('admin_dashboard')

        context = {
            "page_obj": page_obj,
            "search": search,
            "credentials_form": CreadentialsForm(instance=Creadentials.objects.first()),
            "show_credentials_modal": show_credentials_modal,
        }

        return render(request, "views/list_view.html", context)


    
class DetailedOrganizationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        organization = Organization.objects.get(id=kwargs['id'])
        project_id = organization.project_id
        try:
            update_service_id(organization)
        except Exception as e:
            print(e)
        env_form = EnvForm( initial={'organization_id': organization} )
        env_ids = Env.objects.filter(organization_id=organization)
        

        return render(request, 'views/detailed_view.html', {'organization': organization,'project_id':project_id, 'env_form': env_form, 'env_ids': env_ids})
    
class DeploymentReloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        organization = Organization.objects.get(id=kwargs['id'])

        return redirect('detailed_organization', id=organization.id)
    
class AddEnvView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = EnvForm(request.POST)
        organization = Organization.objects.get(id=kwargs['id'])
        if form.is_valid():
            env = form.save(commit=False)
            env.service = request.POST.get('service')
            env.organization_id = organization
            env.save()
            if env.service == 'service':
                service_id = Service.objects.filter(organization_id=env.organization_id).first()
                if service_id:
                    service_id = service_id.service_id
            if env.service == 'database':
                service_id = Service.objects.filter(organization_id=env.organization_id).first()
                if service_id:
                    service_id = service_id.postgres_service_id
            update_service_variable(organization, service_id, env.key, env.value)
            return redirect('detailed_organization', id=organization.id)
        
class UpdateEnvView(LoginRequiredMixin, View):
    def post(self, request,id, *args, **kwargs):
        env = Env.objects.get(id=id)
        env.key = request.POST.get('key')
        env.value = request.POST.get('value')
        env.service = request.POST.get('service')
        env.save()
        if env.service == 'service':
            service_id = Service.objects.filter(organization_id=env.organization_id).first()
            if service_id:
                service_id = service_id.service_id
        if env.service == 'database':
            service_id = Service.objects.filter(organization_id=env.organization_id).first()
            if service_id:
                service_id = service_id.postgres_service_id

        update_service_variable(env.organization_id, service_id, env.key, env.value)
        return redirect('detailed_organization', id=env.organization_id.id)
     
        
class DeleteOrganizationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        org = Organization.objects.get(id=kwargs['id'])
        delete_organization(org)
        org.delete()
        return redirect('list_organization')
    

class DeployementStatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        organization = Organization.objects.get(id=kwargs['id'])
        service = Service.objects.filter(organization_id=organization).first()
        status = deployment_status(service)
        print(status)
        return JsonResponse({'status': status},safe= False)