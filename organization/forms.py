
from django import forms

from admin_app.models import DeploymentTemplate, TemplateService
from organization.models import Env, Organization


class OrganizationForm(forms.ModelForm):
    # Dropdown shows services (TemplateService); deployment_template_id is set from selected service's template on save
    service = forms.ModelChoiceField(
        queryset=DeploymentTemplate.objects.filter(published=True),
        label='Service',
        required=True,
        empty_label='Select a service',
    )

    class Meta:
        model = Organization
        fields = ['name']
        # deployment_template_id is set in save() from the selected service

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = DeploymentTemplate.objects.filter(published=True)

    def save(self, commit=True):
        instance = super().save(commit=False)
        service = self.cleaned_data.get('service')
        if service:
            instance.deployment_template_id = service
        if commit:
            instance.save()
        return instance


class EnvForm(forms.ModelForm):
    service = forms.ChoiceField( label='Service' , choices=[('service', 'Service'), ('database', 'Database')], required=True)
    class Meta:
        model = Env
        fields = ['key', 'value','organization_id']