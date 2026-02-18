from django import template

register = template.Library()


@register.filter
def split_lines(value):
    """Split text by newlines and return list of non-empty stripped lines."""
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]


@register.filter
def split_by(value, arg):
    """Split by separator (e.g. ' — ') into max 2 parts. Returns list [first, rest] or [value]."""
    if not value:
        return []
    if not arg:
        return [value]
    parts = value.split(arg, 1)
    return [p.strip() for p in parts]


@register.filter
def expand_placeholders(value, website=None):
    """Replace {year} and {name} in content. Pass website for {name}, else uses 'Product'."""
    if not value:
        return ''
    import datetime
    out = value.replace('{year}', str(datetime.date.today().year))
    out = out.replace('{name}', (website.name if website else 'Product'))
    return out
