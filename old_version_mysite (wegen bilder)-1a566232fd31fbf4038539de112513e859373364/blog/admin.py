from django.contrib import admin
from .models import Post, Project, Category, Images, Section, Type, Texte

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Post)
admin.site.register(Images)
admin.site.register(Section)
admin.site.register(Type)
admin.site.register(Texte)


