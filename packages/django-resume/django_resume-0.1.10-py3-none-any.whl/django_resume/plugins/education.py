from django import forms

from .base import SimplePlugin


class EducationForm(forms.Form):
    school_name = forms.CharField(
        label="School name", max_length=100, initial="School name"
    )
    school_url = forms.URLField(
        label="School url",
        max_length=100,
        initial="https://example.com",
        assume_scheme="https",
    )
    start = forms.CharField(widget=forms.TextInput(), required=False, initial="start")
    end = forms.CharField(widget=forms.TextInput(), required=False, initial="end")


class EducationPlugin(SimplePlugin):
    name: str = "education"
    verbose_name: str = "Education"
    admin_form_class = inline_form_class = EducationForm
