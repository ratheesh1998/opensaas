"""
website_extras.py
-----------------
Custom template filters used in the public website template.

Place this file at:
    your_app/templatetags/website_extras.py

Make sure your_app is in INSTALLED_APPS and the templatetags/ directory
contains an __init__.py.
"""

from django import template

register = template.Library()


@register.filter
def split_lines(value: str) -> list:
    """
    Split a multi-line string into a list of non-empty stripped lines.

    Usage in template:
        {% with lines=section.content|split_lines %}
    """
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]


@register.filter
def split_by(value: str, delimiter: str) -> list:
    """
    Split a string by a delimiter and return a list of parts.
    Always returns at least one element.

    Usage in template:
        {% with parts=line|split_by:" — " %}
        {{ parts.0 }}   {# title #}
        {{ parts.1 }}   {# description (may be empty) #}
    """
    if not value:
        return ['']
    parts = value.split(delimiter, 1)
    # Pad to length 2 so templates can safely use parts.0 and parts.1
    while len(parts) < 2:
        parts.append('')
    return [p.strip() for p in parts]


@register.simple_tag(takes_context=True)
def theme_var(context, key: str, default: str = '') -> str:
    """
    Return a resolved theme CSS variable value for the current website.

    Usage:
        {% theme_var "primary" "#6366f1" %}
    """
    theme = context.get('theme', {})
    return theme.get(key, default)