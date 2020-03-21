from django import template
from blog.models import Type
register = template.Library()

@register.inclusion_tag('blog/types.html', takes_context=True)
def types(context):


    return {'types': Type.objects.all()}