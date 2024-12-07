import random
import string
from datetime import datetime

from django import forms
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe, SafeString

from .base import ListPlugin, ListItemFormMixin
from ..models import Resume


def generate_random_string(length=20) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class HTMLLinkWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None) -> SafeString:
        return mark_safe(value) if value else mark_safe("")


class TokenItemForm(ListItemFormMixin, forms.Form):
    token = forms.CharField(max_length=255, required=True, label="Token")
    receiver = forms.CharField(max_length=255)
    created = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    cv_link = forms.CharField(required=False, label="CV Link", widget=HTMLLinkWidget())

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if not self.initial.get("token"):
            self.fields["token"].initial = generate_random_string()
        self.token = self.initial.get("token") or self.fields["token"].initial

        if "created" in self.initial and isinstance(self.initial["created"], str):
            self.initial["created"] = datetime.fromisoformat(self.initial["created"])  # type: ignore
        else:
            # Set the 'created' field to the current time if it's not already set
            self.fields["created"].initial = timezone.now()

        self.generate_cv_link(self.resume)

    def generate_cv_link(self, resume: Resume) -> None:
        base_url = reverse("django_resume:cv", kwargs={"slug": resume.slug})
        link = f"{base_url}?token={self.token}"
        self.fields["cv_link"].initial = mark_safe(
            f'<a href="{link}" target="_blank">{link}</a>'
        )

    def clean_token(self) -> str:
        token = self.cleaned_data["token"]
        if not token:
            raise forms.ValidationError("Token required.")
        return token

    def clean_created(self) -> str:
        created = self.cleaned_data["created"]
        return created.isoformat()

    def clean(self) -> dict:
        cleaned_data = super().clean()
        if cleaned_data is None:
            return {}
        cleaned_data.pop("cv_link", None)  # Remove 'cv_link' from cleaned_data
        return cleaned_data


class TokenForm(forms.Form):
    token_required = forms.BooleanField(required=False, label="Token Required")


class TokenViaGetForm(forms.Form):
    token = forms.CharField(max_length=255, required=True, label="Token")


class TokenPlugin(ListPlugin):
    """
    Generate tokens for a resume.

    If you want to restrict access to a resume's resume, you can generate a token.
    The token can be shared with the resume, and they can access their resume using the token.
    """

    name = "token"
    verbose_name = "CV Token"
    flat_template = "django_resume/plain/token_flat.html"
    flat_form_template = "django_resume/plain/token_flat_form.html"

    @staticmethod
    def get_admin_item_form() -> type[forms.Form]:
        return TokenItemForm

    @staticmethod
    def get_admin_form() -> type[forms.Form]:
        return TokenForm

    @staticmethod
    def get_form_classes() -> dict[str, type[forms.Form]]:
        return {"item": TokenItemForm, "flat": TokenForm}

    @staticmethod
    def token_is_required(plugin_data: dict) -> bool:
        return plugin_data.get("flat", {"token_required": True}).get(
            "token_required", True
        )

    @staticmethod
    def check_permissions(request: HttpRequest, plugin_data: dict) -> None:
        token_required = TokenPlugin.token_is_required(plugin_data)
        if not token_required or request.user.is_authenticated:
            return None
        form = TokenViaGetForm(request.GET)
        if not form.is_valid():
            raise PermissionDenied("Token required to access this page.")
        token = form.cleaned_data["token"]
        if token is None:
            raise PermissionDenied("Token required to access this page.")
        tokens = set(item["token"] for item in plugin_data.get("items", []))
        if token in tokens:
            return None
        raise PermissionDenied("Invalid token.")

    def get_context(
        self,
        request: HttpRequest,
        plugin_data: dict,
        resume_pk: int,
        *,
        context: dict,
        edit: bool = False,
        theme: str = "plain",
    ) -> dict:
        self.check_permissions(request, plugin_data)
        return {}
