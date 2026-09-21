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


class SharePostForm(forms.Form):
     message = forms.CharField(
          label="message",
          widget=forms.Textarea(attrs={
               "rows":4,
               "placeholder":"write a message...",
          })
     )

     emails = forms.CharField(
          label="input emails",
          widget=forms.TextInput(attrs={
               "placeholder":"johndoe@gmail.com,example@gmail.com",
          }),
          help_text="Separate multiple email addresses with commas."
     )