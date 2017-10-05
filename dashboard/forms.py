from django import forms


class DocumentForm(forms.Form):
    upload = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}))
