

from admin_app.models import Creadentials, DeploymentTemplate, Environment, TemplateService, Website, WebsiteSection
from django import forms


class CreadentialsForm(forms.ModelForm):
    class Meta:
        model = Creadentials
        fields = '__all__'

class DeploymentTemplateForm(forms.ModelForm):
    class Meta:
        model = DeploymentTemplate
        fields = ['name', 'description', 'published']

class TemplateServiceForm(forms.ModelForm):
    class Meta:
        model = TemplateService
        exclude = ['deployment_template']

class EnvironmentForm(forms.ModelForm):
    class Meta:
        model = Environment
        fields = ['name', 'value']


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'slug', 'tagline', 'niche', 'is_default']


class WebsiteSectionForm(forms.ModelForm):
    class Meta:
        model = WebsiteSection
        fields = ['section_type', 'order', 'title', 'subtitle', 'content', 'image', 'image_url', 'button_text', 'button_link', 'is_active']