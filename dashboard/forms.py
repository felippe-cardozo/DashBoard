from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'priority')


class DocumentForm(forms.Form):
    upload = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}), required=False)
