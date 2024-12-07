from django import forms

from .base import SimplePlugin


class AboutForm(forms.Form):
    title = forms.CharField(label="Title", max_length=256, initial="About")
    text = forms.CharField(
        label="About",
        max_length=1024,
        initial="Some about text...",
        widget=forms.Textarea,
    )


class AboutPlugin(SimplePlugin):
    name: str = "about"
    verbose_name: str = "About"
    admin_form_class = inline_form_class = AboutForm
