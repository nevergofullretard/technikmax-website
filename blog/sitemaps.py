from django.contrib.sitemaps import Sitemap
from .models import Post, Category, Section, Type

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.last_mod


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.all()


class SectionSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Section.objects.all()


class TypeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Type.objects.all()