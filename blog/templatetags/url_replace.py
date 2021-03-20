from django import template
register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータを一部を置き換える"""

    url_dict = request.GET.copy()
    url_dict[field] = str(value) # Django2.1の一部対策。通常はvalueだけでOK
    return url_dict.urlencode()