from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from admin_app.forms import CreadentialsForm, WebsiteForm, WebsiteSectionForm
from django.contrib import messages
from admin_app.models import (
    Creadentials, DeploymentTemplate, Environment, TemplateService,
    Website, WebsiteSection, NICHE_PRESETS,
)
import json
from admin_app.forms import DeploymentTemplateForm, TemplateServiceForm, EnvironmentForm
from organization.models import Organization

User = get_user_model()


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Restrict view to superusers only. Redirect others to app home."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('list_organization')


class AdminDashboardView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """SaaS admin dashboard: stats and overview (not mixed with user app)."""
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = User.objects.count()
        context['organizations_count'] = Organization.objects.count()
        context['templates_count'] = DeploymentTemplate.objects.count()
        context['templates_published_count'] = DeploymentTemplate.objects.filter(published=True).count()
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        context['recent_organizations'] = Organization.objects.select_related(
            'deployment_template_id', 'created_by'
        ).order_by('-id')[:5]
        context['recent_templates'] = DeploymentTemplate.objects.order_by('-created_at')[:5]
        return context


class AdminUserListView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: list all users with search and pagination."""
    template_name = 'admin/user_list.html'

    def get(self, request, *args, **kwargs):
        qs = User.objects.order_by('-date_joined')
        search = request.GET.get('search', '')
        if search:
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        paginator = Paginator(qs, 15)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, self.template_name, {'page_obj': page_obj, 'search': search})


class AdminUserDetailView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: single user detail with their created organizations (links to admin org detail)."""
    template_name = 'admin/user_detail.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        organizations = Organization.objects.filter(created_by=user).select_related(
            'deployment_template_id'
        ).order_by('-id')
        return render(request, self.template_name, {
            'user_obj': user,
            'organizations': organizations,
        })


class AdminOrganizationListView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: list all organizations (admin layout)."""
    template_name = 'admin/organization_list.html'

    def get(self, request, *args, **kwargs):
        qs = Organization.objects.select_related(
            'deployment_template_id', 'created_by', 'project_id'
        ).order_by('-id')
        search = request.GET.get('search', '')
        if search:
            qs = qs.filter(name__icontains=search)
        paginator = Paginator(qs, 15)
        page_obj = paginator.get_page(request.GET.get('page'))
        return render(request, self.template_name, {'page_obj': page_obj, 'search': search})


class AdminOrganizationDetailView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: single organization detail with link to template detail."""
    template_name = 'admin/organization_detail.html'

    def get(self, request, *args, **kwargs):
        organization = get_object_or_404(
            Organization.objects.select_related('deployment_template_id', 'created_by', 'project_id'),
            pk=kwargs['pk']
        )
        from organization.models import Env, Service
        env_ids = Env.objects.filter(organization_id=organization)
        services = Service.objects.filter(organization_id=organization)
        return render(request, self.template_name, {
            'organization': organization,
            'env_ids': env_ids,
            'services': services,
        })


class AdminTemplateListView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: list all deployment templates (admin layout)."""
    template_name = 'admin/template_list.html'

    def get(self, request, *args, **kwargs):
        qs = DeploymentTemplate.objects.all().order_by('-created_at')
        search = request.GET.get('search', '')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        paginator = Paginator(qs, 15)
        page_obj = paginator.get_page(request.GET.get('page'))
        published_count = DeploymentTemplate.objects.filter(published=True).count()
        return render(request, self.template_name, {
            'page_obj': page_obj,
            'search': search,
            'published_count': published_count,
        })


class AdminTemplateCreateView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: create a new deployment template."""
    template_name = 'admin/template_create.html'
    form_class = DeploymentTemplateForm

    def form_valid(self, form):
        template = form.save()
        messages.success(self.request, f'Template "{template.name}" created. You can add services and env in the app.')
        return redirect('admin_template_detail', pk=template.pk)


class AdminTemplateUpdateView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: edit deployment template (name, description, published)."""
    template_name = 'admin/template_edit.html'
    form_class = DeploymentTemplateForm

    def get_object(self):
        return get_object_or_404(DeploymentTemplate, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Template updated.')
        return redirect('admin_template_detail', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = self.get_object()
        return context


class AdminTemplateDetailView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: single template detail with services, env, add/edit forms."""
    template_name = 'admin/template_detail.html'

    def get(self, request, *args, **kwargs):
        template = get_object_or_404(DeploymentTemplate, pk=kwargs['pk'])
        services = template.templateservice_set.all()
        return render(request, self.template_name, {
            'template': template,
            'services': services,
            'service_form': TemplateServiceForm(),
            'environment_form': EnvironmentForm(),
        })


class AdminServiceAddView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: add service to template. POST only, redirects to admin template detail."""
    form_class = TemplateServiceForm
    http_method_names = ['post']

    def form_valid(self, form):
        service = form.save(commit=False)
        service.deployment_template_id = self.kwargs['template_pk']
        service.save()
        messages.success(self.request, 'Service added.')
        return redirect('admin_template_detail', pk=self.kwargs['template_pk'])

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return redirect('admin_template_detail', pk=self.kwargs['template_pk'])


class AdminEnvironmentAddView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: add environment variable to service. POST only."""
    form_class = EnvironmentForm
    http_method_names = ['post']

    def form_valid(self, form):
        service = get_object_or_404(TemplateService, pk=self.kwargs['service_pk'])
        env = form.save(commit=False)
        env.template_service_id = service
        env.save()
        messages.success(self.request, 'Environment variable added.')
        return redirect('admin_template_detail', pk=service.deployment_template_id)

    def form_invalid(self, form):
        service = get_object_or_404(TemplateService, pk=self.kwargs['service_pk'])
        messages.error(self.request, 'Please fix the errors below.')
        return redirect('admin_template_detail', pk=service.deployment_template_id)


class AdminEnvironmentUpdateView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: update environment variable. POST only."""
    form_class = EnvironmentForm
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        env = get_object_or_404(Environment, pk=kwargs['pk'])
        form = EnvironmentForm(request.POST, instance=env)
        if form.is_valid():
            form.save()
            messages.success(request, 'Environment variable updated.')
            return redirect('admin_template_detail', pk=env.template_service_id.deployment_template_id)
        messages.error(request, 'Please fix the errors below.')
        return redirect('admin_template_detail', pk=env.template_service_id.deployment_template_id)


class AdminEnvironmentDeleteView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: delete environment variable. POST only."""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        env = get_object_or_404(Environment, pk=kwargs['pk'])
        template_pk = env.template_service_id.deployment_template_id
        env.delete()
        messages.success(request, 'Environment variable deleted.')
        return redirect('admin_template_detail', pk=template_pk)


















# ---------- Website (admin) ----------
class AdminWebsiteListView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: card view of all websites with Create button."""
    template_name = 'admin/website_list.html'

    def get(self, request, *args, **kwargs):
        websites = Website.objects.all().order_by('-is_default', 'name')
        return render(request, self.template_name, {'websites': websites})


class AdminWebsiteCreateView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: create a new website."""
    template_name = 'admin/website_create.html'
    form_class = WebsiteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['niche_presets_json'] = json.dumps(NICHE_PRESETS)
        return context

    def form_valid(self, form):
        website = form.save()
        messages.success(self.request, f'Website "{website.name}" created.')
        return redirect('admin_website_detail', pk=website.pk)


class AdminWebsiteDetailView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: website detail with edit form and sections (add/edit/delete)."""
    template_name = 'admin/website_detail.html'

    def get(self, request, *args, **kwargs):
        website = get_object_or_404(Website, pk=kwargs['pk'])
        sections = website.sections.all()
        return render(request, self.template_name, {
            'website': website,
            'sections': sections,
            'website_form': WebsiteForm(instance=website),
            'section_form': WebsiteSectionForm(),
            'niche_presets_json': json.dumps(NICHE_PRESETS),
        })


class AdminWebsiteUpdateView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: update website. POST only."""
    form_class = WebsiteForm
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        website = get_object_or_404(Website, pk=kwargs['pk'])
        form = WebsiteForm(request.POST, request.FILES, instance=website)
        if form.is_valid():
            form.save()
            messages.success(request, 'Website updated.')
            return redirect('admin_website_detail', pk=website.pk)
        messages.error(request, 'Please fix the errors below.')
        return redirect('admin_website_detail', pk=website.pk)


class AdminSectionAddView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: add section to website. POST only."""
    form_class = WebsiteSectionForm
    http_method_names = ['post']

    def form_valid(self, form):
        section = form.save(commit=False)
        section.website_id = self.kwargs['pk']
        section.save()
        messages.success(self.request, 'Section added.')
        return redirect('admin_website_detail', pk=self.kwargs['pk'])

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return redirect('admin_website_detail', pk=self.kwargs['pk'])


class AdminSectionEditView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """GET: show section edit form. Form POSTs to admin_section_update."""
    template_name = 'admin/section_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = get_object_or_404(WebsiteSection, pk=self.kwargs['section_pk'])
        context['section'] = section
        context['website'] = section.website
        context['section_form'] = WebsiteSectionForm(instance=section)
        return context


class AdminSectionUpdateView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Admin: update section. POST only."""
    form_class = WebsiteSectionForm
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        section = get_object_or_404(WebsiteSection, pk=kwargs['section_pk'])
        form = WebsiteSectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section updated.')
        else:
            messages.error(request, 'Please fix the errors below.')
        return redirect('admin_website_detail', pk=section.website_id)


class AdminSectionDeleteView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin: delete section. POST only."""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        section = get_object_or_404(WebsiteSection, pk=kwargs['section_pk'])
        website_pk = section.website_id
        section.delete()
        messages.success(request, 'Section deleted.')
        return redirect('admin_website_detail', pk=website_pk)


class AdminSettingsGeneralView(SuperuserRequiredMixin, LoginRequiredMixin, TemplateView):
    """Admin settings > General placeholder."""
    template_name = 'admin/settings_general.html'


class AdminCredentialsView(SuperuserRequiredMixin, LoginRequiredMixin, FormView):
    """Credentials form inside admin layout."""
    template_name = 'admin/credentials.html'
    form_class = CreadentialsForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Creadentials.objects.first()
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Credentials saved successfully.')
        return redirect('admin_credentials')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['credentials'] = Creadentials.objects.first()
        return context


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


# ---------- Public website (no auth) ----------
class PublicWebsiteView(TemplateView):
    """Render the default (main) website with sections. Modern SaaS landing."""
    template_name = 'website/public_site.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['website'] = Website.objects.filter(is_default=True).first()
        if context['website']:
            context['sections'] = context['website'].sections.filter(is_active=True)
            context['theme'] = context['website'].resolved_theme
            context['nav_links'] = context['website'].nav_links
        else:
            context['sections'] = []
            context['theme'] = {}
            context['nav_links'] = []
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if not context['website']:
            from django.urls import reverse
            return redirect(reverse('home'))
        return self.render_to_response(context)


class PublicWebsiteBySlugView(TemplateView):
    """Render a website by slug (e.g. /site/showcase/)."""
    template_name = 'website/public_site.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['website'] = get_object_or_404(Website, slug=self.kwargs['slug'])
        context['sections'] = context['website'].sections.filter(is_active=True)
        context['theme'] = context['website'].resolved_theme
        context['nav_links'] = context['website'].nav_links
        return context


