from django.template.defaulttags import register

@register.filter
def concat(dates):
    return "|".join(dates)