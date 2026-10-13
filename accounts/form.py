from django import forms



class LoginForm(forms.Form):
     username = forms.CharField(required=True,help_text="Please enter your username")
     password = forms.CharField(widget=forms.PasswordInput)
