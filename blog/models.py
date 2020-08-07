# from io import BytesIO
# from django.core.files import File

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# def compress(image):
#     im = Image.open(image)
#     # create a BytesIO object
#     im_io = BytesIO()
#     # save image to BytesIO object
#     im.save(im_io, 'JPEG', quality=75)
#     # create a django-friendly Files object
#     new_image = File(im_io, name=image.name)
#     return new_image

class Images(models.Model):
    name = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='images') # width_field='width_field', height_field='height_field'
    description = models.CharField(blank=True, max_length=150)
    # width_field = models.IntegerField(default=0)
    # height_field = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

    # def save(self, *args, **kwargs):
    #     super(Images, self).save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 1484 and img.width > 1980:
    #         output_size = (1980, 1484)
    #         img.thumbnail(output_size)
    #
    #     img = compress(img)
    #
    #     img.save(self.image.path)



    # def save(self, *args, **kwargs):
    #     super(Images, self).save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 1484 and img.width > 1980:
    #         output_size = (1980, 1484)
    #         img.thumbnail(output_size)
    #     img.save(self.image.path)
    #
    #     new_image = compress(self.image)
    #     # set self.image to new_image
    #     self.image = new_image
    #     # save
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Images, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        img.save(self.image.path)









class Section(models.Model): # zB "Software", "Hardware"
    name = models.CharField(blank=False, max_length=30, unique=True)
    color = models.CharField(blank=False, max_length=50)
    description = models.TextField(blank=True)
    meta_description = models.CharField(blank=True, max_length=159)
    tag_name = models.CharField(blank=True, max_length=35, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self, ):
        return reverse('sections', kwargs={'name': self.tag_name})

class Category(models.Model):  # zB "Python" oder "Arduino"
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    section = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)
    meta_description = models.CharField(blank=True, max_length=159)
    tag_name = models.CharField(blank=True, max_length=110, unique=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self, ):
        return reverse('category-detail', kwargs={'name': self.tag_name})

class Type(models.Model): # zB "Projekt" oder "Artikel"
    name = models.CharField(blank=False, max_length=30, unique=True)
    color = models.CharField(blank=False, max_length=50, default='#0033cc')
    description = models.TextField(blank=True)
    meta_description = models.CharField(blank=True, max_length=159)
    tag_name = models.CharField(blank=True, max_length=35, unique=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self, ):
        return reverse('types', kwargs={'name': self.tag_name})

class Post(models.Model):
    title = models.CharField(blank=False, max_length=62)
    title_tag = models.CharField(blank=False, max_length=100)
    description = models.TextField(blank=False)
    meta_description = models.CharField(blank=True, max_length=159)
    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category, related_name='post_categories')
    background_image = models.ForeignKey(Images, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    next = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    published = models.BooleanField(default=False)
    last_mod = models.DateTimeField(default=timezone.now)



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


class Texte(models.Model):
    title = models.CharField(blank=False, max_length=100, unique=True)
    content = models.TextField(blank=True) # this is with html content

    def __str__(self):
        return self.title