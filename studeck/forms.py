from django import forms
from .models import Feedbacks,rating_model

class Feedback_form(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['feed_back','picture']
