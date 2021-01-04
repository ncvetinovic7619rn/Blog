from django.forms import ModelForm, Form
import django.forms as f
from .models import Thread,Comment


class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

