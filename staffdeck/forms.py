from django import forms
from .models import MessUpload

class UploadMessMenu(forms.ModelForm):
    class Meta:
        model = MessUpload
        fields = ['file']
