from .models import *

from django import forms

class CreateForm(forms.ModelForm):
    class Meta:
        model = FORUM
        fields = ['text', 'topic_type','forum_image']