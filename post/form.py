from django import forms
from .models import Post


# class PostForm(forms.forms):
#     title = forms.CharField(max_length=100)
#     content = forms.CharField(widget=forms.Textarea)
#     author = forms.CharField(max_length=50)
#     status = forms.CharField(max_length=50)


class PostForm(forms.ModelForm):
    class Meta:
         model = Post
         fields =["title","content","author","status"]