from django.apps import AppConfig


# Slug, name, niche, tagline for each of the 4 niche template websites (7+ sections, with images).
NICHE_TEMPLATES = [
    ("template-health", "Health & Wellness", "health_wellness", "Better health starts with better data."),
    ("template-food", "Food & Agriculture", "food_agriculture", "From farm to table — with full traceability."),
    ("template-fintech", "Finance & FinTech", "fintech", "Financial intelligence at your fingertips."),
    ("template-ecommerce", "E-Commerce & Retail", "ecommerce", "Sell more. Stress less."),
]


def ensure_app_ready_website():
    """Ensure the App Ready (common_saas) website template exists."""
    try:
        from admin_app.models import Website
        if not Website.objects.filter(slug='app-ready').exists():
            Website.create_with_preset(
                name='App Ready',
                slug='app-ready',
                niche='common_saas',
                tagline='Ship faster. Scale smarter.',
                is_default=False,
            )
    except Exception:
        pass


def ensure_niche_template_websites():
    """Ensure all 4 niche template websites exist (heavy sections + images)."""
    try:
        from admin_app.models import Website
        for slug, name, niche, tagline in NICHE_TEMPLATES:
            if not Website.objects.filter(slug=slug).exists():
                Website.create_with_preset(
                    name=name,
                    slug=slug,
                    niche=niche,
                    tagline=tagline,
                    is_default=False,
                )
    except Exception:
        pass


def ensure_all_template_websites(**kwargs):
    ensure_app_ready_website()
    ensure_niche_template_websites()


class AdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_app'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(ensure_all_template_websites, sender=self, weak=False)
        ensure_all_template_websites()
