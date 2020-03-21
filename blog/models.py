from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Images(models.Model):
    name = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='images') # width_field='width_field', height_field='height_field'
    description = models.CharField(blank=True, max_length=150)
    # width_field = models.IntegerField(default=0)
    # height_field = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super(Images, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        img.save(self.image.path)





class Section(models.Model): # zB "Software", "Hardware"
    name = models.CharField(blank=False, max_length=30, unique=True)
    color = models.CharField(blank=False, max_length=50)
    description = models.CharField(blank=True, max_length=500)

    def __str__(self):
        return self.name


class Category(models.Model):  # zB "Python" oder "Arduino"
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(blank=True, max_length=500)
    section = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Type(models.Model): # zB "Projekt" oder "Artikel"
    name = models.CharField(blank=False, max_length=30, unique=True)
    color = models.CharField(blank=False, max_length=50, default='#0033cc')
    description = models.CharField(blank=True, max_length=500)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(blank=False, max_length=100)
    title_tag = models.CharField(blank=False, max_length=100)
    description = models.CharField(blank=False, max_length=1000)
    type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='post_categories')
    background_image = models.ForeignKey(Images, null=True, blank=True, on_delete=True)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    next = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)




    def __str__(self):
        return self.title

    def get_absolute_url(self, ):
        return reverse('post-detail', kwargs={'pk': self.pk, 'name': self.title_tag})



class Project(models.Model):
    title = models.CharField(blank=False, max_length=100)
    title_tag = models.CharField(blank=False, max_length=100)
    description = models.CharField(blank=False, max_length=1000)
    font_color = models.CharField(default="white", max_length=100)
    categories = models.ManyToManyField(Category, related_name='project_categories')
    background_color = models.CharField(null=True, blank=True, max_length=50)
    background_image = models.ForeignKey(Images, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(default="")
    github = models.CharField(blank=True, max_length=200)

    title_en = models.CharField(default="", max_length=100)
    title_tag_en = models.CharField(default="", max_length=100)
    description_en = models.CharField(default="", max_length=1000)
    html_en = models.TextField(default="")


    def __str__(self):
        return self.title

    def get_absolute_url(self, ):
        return reverse('project-detail', kwargs={'pk': self.pk, 'name': self.title_tag})



