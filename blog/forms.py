from django import forms
from . import models



class UploadImageForm(forms.ModelForm):
    class Meta:
        model = models.Images
        fields = ['name', 'image']


class PostForm(forms.ModelForm):
    # existing_unit = forms.ModelMultipleChoiceField(queryset=models.Unit_name.objects.all())

    class Meta:
        model = models.Post
        fields = ['content', 'title', 'description', 'date', 'author', 'type',  'categories', 'background_image', 'next']