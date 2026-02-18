from django.db import models

# Create your models here.
class Creadentials(models.Model):
    railway_auth_token = models.CharField(max_length=255)
    railway_workspace_id = models.CharField(max_length=255)
    raiway_template_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Credentials"
        verbose_name_plural = "Credentials"


class Project(models.Model):
    project_id = models.CharField(max_length=100)
    environment_id = models.CharField(max_length=100)
 
    def __str__(self):
        return self.project_id
    
class DeploymentTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    default_domain = models.CharField(max_length=100, null=True, blank=True)
    workflow_id = models.CharField(max_length=100, null=True, blank=True)   
    def __str__(self):
        return self.name

class TemplateService(models.Model):
    name = models.CharField(max_length=255)
    deployment_template = models.ForeignKey(DeploymentTemplate, on_delete=models.CASCADE)
    docker_image = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
      
class Environment(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    template_service_id = models.ForeignKey(TemplateService, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
from django.db import models


# ---------------------------------------------------------------------------
# Niche presets – drives auto-fill when a website is created/edited
# ---------------------------------------------------------------------------
# "common_saas" is the app-ready default: one template that fits most B2B SaaS.
# Use it for new sites when you want a full, professional landing page out of the box.
# ---------------------------------------------------------------------------

NICHE_PRESETS = {
    "common_saas": {
        "label": "Common SaaS (app-ready)",
        "emoji": "🚀",
        "theme": {
            "primary":      "#6366f1",
            "primary_light": "#818cf8",
            "primary_glow": "rgba(99,102,241,0.4)",
            "accent":       "#22d3ee",
            "bg":           "#0a0a0f",
            "surface":      "#12121a",
            "border":       "#27272f",
        },
        "nav_links": [
            {"label": "Features",   "href": "#features"},
            {"label": "Pricing",    "href": "#pricing"},
            {"label": "Get started","href": "#cta"},
        ],
        "sections": [
            {
                "section_type": "hero",
                "order": 0,
                "title": "Ship faster. Scale smarter.",
                "subtitle": "The all-in-one platform that helps teams build, launch, and grow their product—without the complexity.",
                "button_text": "Start free trial",
                "button_link": "/user/register/",
                "content": "",
            },
            {
                "section_type": "features",
                "order": 1,
                "title": "Everything you need to win",
                "subtitle": "Powerful features that work together. No integrations required.",
                "content": (
                    "⚡ Launch in minutes — Get from signup to first value in under an hour, not weeks.\n"
                    "📊 Real-time analytics — Know exactly how your product is used and where to improve.\n"
                    "🔐 Enterprise-ready security — SSO, audit logs, and compliance controls built in.\n"
                    "🔗 APIs & webhooks — Connect to your stack; we play nice with every tool.\n"
                    "👥 Team collaboration — Roles, permissions, and shared workspaces from day one.\n"
                    "📈 Usage-based billing — Scale pricing with your customers; no surprise bills."
                ),
                "button_text": "",
                "button_link": "",
            },
            {
                "section_type": "pricing",
                "order": 2,
                "title": "Simple, transparent pricing",
                "subtitle": "No hidden fees. Upgrade or downgrade anytime.",
                "content": (
                    "Starter — $29 / mo — Up to 5 users · Core features · Email support\n"
                    "Pro — $79 / mo — Up to 25 users · Advanced analytics · Priority support\n"
                    "Enterprise — Custom — Unlimited users · SSO & SLA · Dedicated success"
                ),
                "button_text": "",
                "button_link": "",
            },
            {
                "section_type": "testimonial",
                "order": 3,
                "title": "",
                "subtitle": "",
                "content": (
                    '"We went live in a weekend. Our previous setup took months. '
                    'This is how modern software should work." — Alex K., Head of Product @ ScaleUp'
                ),
                "button_text": "",
                "button_link": "",
            },
            {
                "section_type": "cta",
                "order": 4,
                "title": "Ready to get started?",
                "subtitle": "Join thousands of teams already building on the platform. No credit card required.",
                "content": "",
                "button_text": "Create free account",
                "button_link": "/user/register/",
            },
            {
                "section_type": "footer",
                "order": 5,
                "title": "",
                "subtitle": "",
                "content": "© {year} {name}. All rights reserved.\nProduct · Pricing · Docs · Privacy · Terms · Contact",
                "button_text": "",
                "button_link": "",
            },
        ],
    },

    "business_software": {
        "label": "Business Software",
        "emoji": "💼",
        "theme": {
            "primary":      "#6366f1",
            "primary_light":"#818cf8",
            "primary_glow": "rgba(99,102,241,0.35)",
            "accent":       "#22d3ee",
            "bg":           "#0a0a0d",
            "surface":      "#12121a",
            "border":       "#27272f",
        },
        "nav_links": [
            {"label": "Features",   "href": "#features"},
            {"label": "Pricing",    "href": "#pricing"},
            {"label": "Enterprise", "href": "#cta"},
        ],
        "sections": [
            {
                "section_type": "hero",
                "order": 0,
                "title": "Run Your Business. Not Your Software.",
                "subtitle": "Automate workflows, centralise data, and ship faster with an all-in-one platform built for modern teams.",
                "button_text": "Start free trial",
                "button_link": "/register/",
                "content": "",
            },
            {
                "section_type": "features",
                "order": 1,
                "title": "Everything your team needs",
                "subtitle": "Powerful tools that work together out of the box.",
                "content": (
                    "⚡ Workflow Automation — Eliminate repetitive tasks with no-code automation builders.\n"
                    "📊 Real-Time Analytics — Live dashboards that surface the numbers that matter most.\n"
                    "🔗 500+ Integrations — Connect Slack, Stripe, Salesforce and every tool you already use.\n"
                    "🔒 Enterprise Security — SOC 2 Type II, SSO, and granular role-based permissions.\n"
                    "🌍 Multi-Workspace — Manage multiple teams or clients from a single account.\n"
                    "💬 Collaboration Hub — Comments, mentions, and shared views keep everyone aligned."
                ),
                "button_text": "",
                "button_link": "",
            },
            {
                "section_type": "pricing",
                "order": 2,
                "title": "Simple, transparent pricing",
                "subtitle": "No hidden fees. Cancel anytime.",
                "content": (
                    "Starter — $29 / mo — 5 users · 10 workflows · Community support\n"
                    "Growth — $79 / mo — 25 users · Unlimited workflows · Priority email support\n"
                    "Enterprise — Custom — Unlimited users · SLA · Dedicated success manager"
                ),
                "button_text": "",
                "button_link": "",
            },
            {
                "section_type": "testimonial",
                "order": 3,
                "title": "",
                "subtitle": "",
                "content": (
                    '"We replaced four separate tools with this platform and cut our ops overhead by 40 %. '
                    'Onboarding took one afternoon." — Sarah L., VP Operations @ Acme Corp'
                ),
                "button_text": "",
                "button_link": "",
            },
            {
                "section_type": "cta",
                "order": 4,
                "title": "Ready to take back your time?",
                "subtitle": "Join 12,000+ companies already running smarter.",
                "content": "",
                "button_text": "Get started — it's free",
                "button_link": "/register/",
            },
            {
                "section_type": "footer",
                "order": 5,
                "title": "",
                "subtitle": "",
                "content": "© {year} {name}. All rights reserved.\nProduct · Pricing · Docs · Privacy · Terms",
                "button_text": "",
                "button_link": "",
            },
        ],
    },

    "health_wellness": {
        "label": "Health & Wellness",
        "emoji": "🏥",
        "theme": {
            "primary":      "#10b981",
            "primary_light":"#34d399",
            "primary_glow": "rgba(16,185,129,0.35)",
            "accent":       "#f0abfc",
            "bg":           "#030d09",
            "surface":      "#071510",
            "border":       "#0d2b1c",
        },
        "nav_links": [
            {"label": "Features",  "href": "#features"},
            {"label": "Plans",     "href": "#pricing"},
            {"label": "Start",     "href": "#cta"},
        ],
        "sections": [
            {
                "section_type": "hero",
                "order": 0,
                "title": "Better Health Starts With Better Data.",
                "subtitle": "Track vitals, log habits, and get AI-powered insights that keep you and your patients on the path to wellness.",
                "button_text": "Try it free",
                "button_link": "/user/register/",
                "content": "",
                "image_url": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=800&q=80",
            },
            {
                "section_type": "features",
                "order": 1,
                "title": "Designed for health professionals & individuals",
                "subtitle": "Clinical-grade tools made beautifully simple.",
                "content": (
                    "🩺 Patient Dashboard — A full health timeline for every patient in one place.\n"
                    "📈 Trend Analysis — Spot patterns in vitals before they become problems.\n"
                    "💊 Medication Tracker — Automated reminders and adherence reports.\n"
                    "🤖 AI Health Coach — Personalised recommendations based on real data.\n"
                    "🔐 HIPAA Compliant — Enterprise-grade encryption for every record.\n"
                    "📱 Mobile-First — iOS & Android apps with offline mode support."
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&q=80",
            },
            {
                "section_type": "features",
                "order": 2,
                "title": "Why practices choose us",
                "subtitle": "From solo practitioners to large clinics.",
                "content": (
                    "🔄 Care Coordination — Share notes and handoffs across your team securely.\n"
                    "📋 Smart Forms — Custom intake and consent forms that pre-fill from history.\n"
                    "🔔 Reminders & Alerts — Reduce no-shows with automated SMS and email.\n"
                    "📊 Outcomes Dashboard — Track key metrics and compare to benchmarks."
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&q=80",
            },
            {
                "section_type": "pricing",
                "order": 3,
                "title": "Plans for every practice",
                "subtitle": "Transparent pricing, no lock-in.",
                "content": (
                    "Individual — Free — Personal tracking · 30-day history · Mobile app\n"
                    "Practitioner — $49 / mo — Up to 50 patients · Full analytics · EHR export\n"
                    "Clinic — $199 / mo — Unlimited patients · Team accounts · API access"
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=800&q=80",
            },
            {
                "section_type": "testimonial",
                "order": 4,
                "title": "",
                "subtitle": "",
                "content": (
                    '"Our clinic reduced missed follow-ups by 60 % in the first month. '
                    'The patient dashboard is simply the best I\'ve used." — Dr. Amina R., Family Physician'
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1612349317150-413f244a230c?w=200&q=80",
            },
            {
                "section_type": "testimonial",
                "order": 5,
                "title": "",
                "subtitle": "",
                "content": (
                    '"I finally have one place for all my health data. The AI insights helped me '
                    'spot a pattern my doctor had missed." — James T., Individual user'
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&q=80",
            },
            {
                "section_type": "cta",
                "order": 6,
                "title": "Your wellness journey starts today.",
                "subtitle": "Free forever for individuals. No credit card required.",
                "content": "",
                "button_text": "Create free account",
                "button_link": "/user/register/",
            },
            {
                "section_type": "footer",
                "order": 7,
                "title": "",
                "subtitle": "",
                "content": "© {year} {name}. All rights reserved.\nFeatures · Plans · HIPAA Policy · Privacy · Contact",
                "button_text": "",
                "button_link": "",
            },
        ],
    },

    "food_agriculture": {
        "label": "Food & Agriculture",
        "emoji": "🌾",
        "theme": {
            "primary":      "#d97706",
            "primary_light":"#fbbf24",
            "primary_glow": "rgba(217,119,6,0.35)",
            "accent":       "#86efac",
            "bg":           "#0d0900",
            "surface":      "#1a1100",
            "border":       "#2d1f00",
        },
        "nav_links": [
            {"label": "Features",  "href": "#features"},
            {"label": "Pricing",   "href": "#pricing"},
            {"label": "Get started","href": "#cta"},
        ],
        "sections": [
            {
                "section_type": "hero",
                "order": 0,
                "title": "From Farm to Table — with Full Traceability.",
                "subtitle": "Monitor quality, track batches, and ensure compliance at every step of your food supply chain.",
                "button_text": "Start monitoring",
                "button_link": "/user/register/",
                "content": "",
                "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800&q=80",
            },
            {
                "section_type": "features",
                "order": 1,
                "title": "Quality you can measure",
                "subtitle": "Built for producers, processors, and distributors.",
                "content": (
                    "🧪 Lab Test Integration — Import results from any accredited lab automatically.\n"
                    "📦 Batch Traceability — End-to-end tracking from raw input to consumer shelf.\n"
                    "⚠️ Recall Management — Instant contamination alerts and automated recall workflows.\n"
                    "📋 Compliance Reports — FSMA, HACCP, and ISO 22000 docs generated in one click.\n"
                    "🌡️ IoT Sensor Hub — Connect temperature, humidity, and pH sensors in real time.\n"
                    "📊 Quality Scorecards — Grade every supplier and batch against your own standards."
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1466637574441-749b8f19452f?w=800&q=80",
            },
            {
                "section_type": "features",
                "order": 2,
                "title": "From field to fork",
                "subtitle": "One platform for the entire supply chain.",
                "content": (
                    "🌾 Farm Management — Crop plans, harvest logs, and input tracking.\n"
                    "🚚 Logistics — Cold chain monitoring and delivery ETAs.\n"
                    "🏷️ Label & Certifications — Generate compliant labels and store certs.\n"
                    "📱 Mobile Receiving — Scan and log at intake with photos and temps."
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1574944985070-8f3ebcfe5e5e?w=800&q=80",
            },
            {
                "section_type": "pricing",
                "order": 3,
                "title": "Pricing that scales with your operation",
                "subtitle": "From small farms to global distributors.",
                "content": (
                    "Farmer — $39 / mo — 1 facility · 500 batches/yr · Email support\n"
                    "Processor — $149 / mo — 5 facilities · Unlimited batches · API + IoT\n"
                    "Enterprise — Custom — Multi-site · White-label · Dedicated onboarding"
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80",
            },
            {
                "section_type": "testimonial",
                "order": 4,
                "title": "",
                "subtitle": "",
                "content": (
                    '"We passed our first FDA audit without a single finding. '
                    'The automated compliance reports alone saved us weeks of manual work." — Tom H., Quality Manager @ FreshPack Ltd'
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=200&q=80",
            },
            {
                "section_type": "testimonial",
                "order": 5,
                "title": "",
                "subtitle": "",
                "content": (
                    '"Traceability used to mean spreadsheets and phone calls. Now we scan a code '
                    'and see the full journey in seconds." — Maria G., Operations @ GreenValley Farms'
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1594744803329-58c25983c757?w=200&q=80",
            },
            {
                "section_type": "cta",
                "order": 6,
                "title": "Quality isn't optional. Neither is your software.",
                "subtitle": "Start your 14-day free trial — no credit card needed.",
                "content": "",
                "button_text": "Start free trial",
                "button_link": "/user/register/",
            },
            {
                "section_type": "footer",
                "order": 7,
                "title": "",
                "subtitle": "",
                "content": "© {year} {name}. All rights reserved.\nFeatures · Pricing · Compliance · Privacy · Contact",
                "button_text": "",
                "button_link": "",
            },
        ],
    },

    "fintech": {
        "label": "Finance & FinTech",
        "emoji": "💳",
        "theme": {
            "primary":      "#3b82f6",
            "primary_light":"#93c5fd",
            "primary_glow": "rgba(59,130,246,0.35)",
            "accent":       "#f59e0b",
            "bg":           "#02050f",
            "surface":      "#050d1f",
            "border":       "#0f1f40",
        },
        "nav_links": [
            {"label": "Features",  "href": "#features"},
            {"label": "Pricing",   "href": "#pricing"},
            {"label": "Open account","href": "#cta"},
        ],
        "sections": [
            {
                "section_type": "hero",
                "order": 0,
                "title": "Financial Intelligence. At Your Fingertips.",
                "subtitle": "Real-time transaction monitoring, automated reconciliation, and AI-driven forecasting — for startups to enterprises.",
                "button_text": "Open free account",
                "button_link": "/user/register/",
                "content": "",
                "image_url": "https://images.unsplash.com/photo-1554224155-8d04cb21cd3c?w=800&q=80",
            },
            {
                "section_type": "features",
                "order": 1,
                "title": "Built for the way money actually moves",
                "subtitle": "Modern finance infrastructure without the complexity.",
                "content": (
                    "💰 Real-Time Ledger — Sub-second transaction processing across all accounts and currencies.\n"
                    "🔍 Fraud Detection — ML models flag anomalies before they become chargebacks.\n"
                    "📑 Auto-Reconciliation — Match bank statements to your books in seconds, not days.\n"
                    "📉 Cash Flow Forecasting — AI predictions with scenario modelling up to 12 months out.\n"
                    "🏦 Multi-Bank Aggregation — Connect all accounts via Open Banking APIs.\n"
                    "📊 Investor Reporting — One-click board decks with live financial metrics."
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1611974789855-9e2d742247ab?w=800&q=80",
            },
            {
                "section_type": "features",
                "order": 2,
                "title": "Enterprise-grade security & compliance",
                "subtitle": "Built for regulated environments.",
                "content": (
                    "🔐 SOC 2 & ISO 27001 — Audited controls and documented policies.\n"
                    "📋 Audit Trail — Immutable log of every action for examiners.\n"
                    "🌍 Multi-Currency — Real-time FX and multi-entity consolidation.\n"
                    "🔗 Open Banking — PSD2, Open Banking UK, and global APIs."
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1563986768609-322b135a9f9b?w=800&q=80",
            },
            {
                "section_type": "pricing",
                "order": 3,
                "title": "Transparent pricing. Zero surprises.",
                "subtitle": "Flat monthly fees — no per-transaction charges.",
                "content": (
                    "Startup — $59 / mo — 2 users · 3 bank connections · Core analytics\n"
                    "Scale — $199 / mo — 10 users · Unlimited connections · Forecasting + API\n"
                    "Enterprise — Custom — Unlimited users · Dedicated infra · SLA + compliance pack"
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80",
            },
            {
                "section_type": "testimonial",
                "order": 4,
                "title": "",
                "subtitle": "",
                "content": (
                    '"Month-end close used to take our team five days. Now it takes four hours. '
                    'The reconciliation engine is genuinely magical." — Priya S., CFO @ NexaPay'
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=200&q=80",
            },
            {
                "section_type": "testimonial",
                "order": 5,
                "title": "",
                "subtitle": "",
                "content": (
                    '"We replaced three legacy systems with one. Implementation was smooth '
                    'and our auditors loved the audit trail." — David L., Head of Finance'
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&q=80",
            },
            {
                "section_type": "cta",
                "order": 6,
                "title": "The smarter way to manage money.",
                "subtitle": "Join 3,000+ finance teams already saving hours every week.",
                "content": "",
                "button_text": "Get started free",
                "button_link": "/user/register/",
            },
            {
                "section_type": "footer",
                "order": 7,
                "title": "",
                "subtitle": "",
                "content": "© {year} {name}. All rights reserved.\nProduct · Pricing · Security · Privacy · Terms",
                "button_text": "",
                "button_link": "",
            },
        ],
    },

    "ecommerce": {
        "label": "E-Commerce & Retail",
        "emoji": "🛍️",
        "theme": {
            "primary":      "#ec4899",
            "primary_light":"#f9a8d4",
            "primary_glow": "rgba(236,72,153,0.35)",
            "accent":       "#fb923c",
            "bg":           "#0d0009",
            "surface":      "#1a0012",
            "border":       "#2d0020",
        },
        "nav_links": [
            {"label": "Features",  "href": "#features"},
            {"label": "Pricing",   "href": "#pricing"},
            {"label": "Launch",    "href": "#cta"},
        ],
        "sections": [
            {
                "section_type": "hero",
                "order": 0,
                "title": "Sell More. Stress Less.",
                "subtitle": "The e-commerce operating system that handles inventory, orders, and customer loyalty — so you can focus on growth.",
                "button_text": "Launch your store",
                "button_link": "/user/register/",
                "content": "",
                "image_url": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80",
            },
            {
                "section_type": "features",
                "order": 1,
                "title": "Every tool your store needs",
                "subtitle": "From first click to repeat customer.",
                "content": (
                    "🛒 Unified Inventory — Sync stock across Shopify, Amazon, WooCommerce, and your own store.\n"
                    "📦 Smart Fulfilment — Auto-route orders to the nearest warehouse for fastest delivery.\n"
                    "💌 Loyalty Engine — Points, rewards, and referral programs that actually convert.\n"
                    "📊 Revenue Analytics — Know your best products, customers, and channels at a glance.\n"
                    "🤖 AI Merchandising — Personalised product recommendations that lift AOV.\n"
                    "🔔 Abandoned Cart Recovery — Automated sequences that win back lost sales."
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=800&q=80",
            },
            {
                "section_type": "features",
                "order": 2,
                "title": "Sell everywhere your customers are",
                "subtitle": "One back office. Every channel.",
                "content": (
                    "🛍️ Multi-Channel Listings — Push to marketplaces and social shop in one click.\n"
                    "📱 Mobile-Optimised Checkout — Higher conversion on every device.\n"
                    "🌐 International — Multi-currency, tax, and shipping rules built in.\n"
                    "🔗 200+ Integrations — ERPs, 3PLs, marketing tools, and more."
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800&q=80",
            },
            {
                "section_type": "pricing",
                "order": 3,
                "title": "Grow without growing your costs",
                "subtitle": "Flat pricing — no GMV percentage, ever.",
                "content": (
                    "Starter — $49 / mo — 1 store · 1,000 orders/mo · Core analytics\n"
                    "Pro — $129 / mo — 3 stores · Unlimited orders · AI recommendations + loyalty\n"
                    "Agency — $349 / mo — Unlimited stores · White-label · Priority support"
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?w=800&q=80",
            },
            {
                "section_type": "testimonial",
                "order": 4,
                "title": "",
                "subtitle": "",
                "content": (
                    '"Revenue grew 34 % in 90 days after switching. The AI merchandising alone '
                    'covers our subscription cost three times over." — Marco V., Founder @ ThreadCo'
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&q=80",
            },
            {
                "section_type": "testimonial",
                "order": 5,
                "title": "",
                "subtitle": "",
                "content": (
                    '"We went from one store to 12 without adding headcount. The automation '
                    'and reporting are game-changers." — Sophie K., Operations Director'
                ),
                "button_text": "",
                "button_link": "",
                "image_url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&q=80",
            },
            {
                "section_type": "cta",
                "order": 6,
                "title": "Your next best month starts now.",
                "subtitle": "14-day free trial. No credit card. No commitments.",
                "content": "",
                "button_text": "Start free trial",
                "button_link": "/user/register/",
            },
            {
                "section_type": "footer",
                "order": 7,
                "title": "",
                "subtitle": "",
                "content": "© {year} {name}. All rights reserved.\nFeatures · Pricing · Integrations · Privacy · Contact",
                "button_text": "",
                "button_link": "",
            },
        ],
    },

    "custom": {
        "label": "Custom / Other",
        "emoji": "✨",
        "theme": {
            "primary":      "#8b5cf6",
            "primary_light":"#c4b5fd",
            "primary_glow": "rgba(139,92,246,0.35)",
            "accent":       "#34d399",
            "bg":           "#08060f",
            "surface":      "#100d1a",
            "border":       "#1e1830",
        },
        "nav_links": [
            {"label": "Features",   "href": "#features"},
            {"label": "Pricing",    "href": "#pricing"},
            {"label": "Get started","href": "#cta"},
        ],
        "sections": [],   # user fills everything manually
    },
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Website(models.Model):
    """SaaS product website. One can be set as default (main website)."""

    NICHE_CHOICES = [(k, v["label"]) for k, v in NICHE_PRESETS.items()]

    name       = models.CharField(max_length=255)
    slug       = models.SlugField(max_length=80, unique=True,
                                  help_text='URL-friendly identifier')
    is_default = models.BooleanField(
        default=False,
        help_text='When enabled, this is the main website shown to visitors'
    )
    tagline    = models.CharField(max_length=255, blank=True)

    # ── NEW ──────────────────────────────────────────────────────────────
    niche = models.CharField(
        max_length=40,
        choices=NICHE_CHOICES,
        default='common_saas',
        help_text='Niche preset used to auto-populate sections and theme. Common SaaS is app-ready.',
    )
    theme_overrides = models.JSONField(
        default=dict, blank=True,
        help_text='JSON dict that overrides individual theme CSS variables.',
    )
    # ─────────────────────────────────────────────────────────────────────

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', 'name']

    # ── helpers ──────────────────────────────────────────────────────────

    @property
    def preset(self):
        """Return the full NICHE_PRESETS dict entry for this website."""
        return NICHE_PRESETS.get(self.niche, NICHE_PRESETS['custom'])

    @property
    def resolved_theme(self):
        """Merge preset theme with any per-website overrides."""
        theme = dict(self.preset.get('theme', {}))
        theme.update(self.theme_overrides or {})
        return theme

    @property
    def nav_links(self):
        return self.preset.get('nav_links', [])

    # ─────────────────────────────────────────────────────────────────────

    def save(self, *args, **kwargs):
        if self.is_default:
            Website.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # ── factory method ───────────────────────────────────────────────────

    @classmethod
    def create_with_preset(cls, name: str, slug: str, niche: str,
                           tagline: str = '', is_default: bool = False) -> 'Website':
        """
        Create a Website AND seed its WebsiteSections from the niche preset.
        Usage:
            website = Website.create_with_preset(
                name='MilkScan', slug='milkscan',
                niche='food_agriculture', tagline='Quality milk. Every batch.'
            )
        """
        import datetime
        website = cls.objects.create(
            name=name, slug=slug, niche=niche,
            tagline=tagline, is_default=is_default,
        )
        preset = NICHE_PRESETS.get(niche, NICHE_PRESETS['custom'])
        year = datetime.date.today().year
        for s in preset.get('sections', []):
            content = s.get('content', '').replace('{year}', str(year)).replace('{name}', name)
            WebsiteSection.objects.create(
                website=website,
                section_type=s['section_type'],
                order=s.get('order', 0),
                title=s.get('title', ''),
                subtitle=s.get('subtitle', ''),
                content=content,
                image_url=s.get('image_url', ''),
                button_text=s.get('button_text', ''),
                button_link=s.get('button_link', ''),
                is_active=True,
            )
        return website


class WebsiteSection(models.Model):
    """Section of a website. Content and image per section."""

    SECTION_TYPES = [
        ('hero',        'Hero'),
        ('features',    'Features'),
        ('pricing',     'Pricing'),
        ('cta',         'Call to Action'),
        ('testimonial', 'Testimonial'),
        ('footer',      'Footer'),
    ]

    website      = models.ForeignKey(Website, on_delete=models.CASCADE,
                                     related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    order        = models.PositiveIntegerField(default=0)
    title        = models.CharField(max_length=255, blank=True)
    subtitle     = models.CharField(max_length=255, blank=True)
    content      = models.TextField(blank=True, help_text='Main text or HTML')
    image        = models.ImageField(upload_to='website_sections/', blank=True, null=True)
    image_url    = models.URLField(max_length=500, blank=True, help_text='Fallback image URL if no file uploaded')
    button_text  = models.CharField(max_length=64, blank=True)
    button_link  = models.URLField(max_length=500, blank=True)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.website.name} – {self.get_section_type_display()} ({self.order})"