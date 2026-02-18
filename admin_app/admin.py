from django.contrib import admin

from admin_app.models import (
    Creadentials,
    DeploymentTemplate,
    TemplateService,
    Environment,
    Project,
    Website,
    WebsiteSection,
)


# Custom ModelAdmin with list_display so list views show columns and bulk actions (checkboxes) appear.
# Django shows the action checkbox column when the admin has at least one action (default: Delete selected).
@admin.register(Creadentials)
class CreadentialsAdmin(admin.ModelAdmin):
    list_display = ("id", "railway_auth_token", "railway_workspace_id", "raiway_template_id")


@admin.register(DeploymentTemplate)
class DeploymentTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "published", "created_at", "project_id")
    list_filter = ("published",)


@admin.register(TemplateService)
class TemplateServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "deployment_template", "docker_image")
    list_filter = ("deployment_template",)


@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "template_service_id")
    list_filter = ("template_service_id",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_id", "environment_id")


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "niche", "is_default", "created_at")
    list_filter = ("niche", "is_default")
    list_editable = ("is_default",)
    search_fields = ("name", "slug", "tagline")


@admin.register(WebsiteSection)
class WebsiteSectionAdmin(admin.ModelAdmin):
    list_display = ("website", "section_type", "order", "title", "is_active")
    list_filter = ("section_type", "is_active", "website")
    list_editable = ("order", "is_active")
    search_fields = ("title", "content")