from django import forms
from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']


class PostQueryForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput)