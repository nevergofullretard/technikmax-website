from django import template
from blog.models import Section
register = template.Library()

@register.inclusion_tag('blog/sections.html', takes_context=True)
def sections(context):


    return {'sections': Section.objects.all()}