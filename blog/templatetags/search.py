from django import template
from blog.models import Post
from django.contrib.auth.models import User
register = template.Library()

@register.inclusion_tag('blog/search.html', takes_context=True)
def search(context):

    all = ['yoo']



    # for word, unit, schule, sprache, post, user in zip(words, units, schulen, sprachen, posts, users):
    #     all.append(word)
    #     all.append(unit)
    #     all.append(sprache)
    #     all.append(schule)
    #     all.append(post)
    #     all.append(user)
    # print(words)

    return {'words': all}