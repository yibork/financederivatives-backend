from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from users.models import User


class CustomUserEditForm(UserEditForm):
    role = forms.ChoiceField(
        label=_('Role'),
        choices=User.ROLE_CHOICES,
        required=False,
    )

    phone_number = forms.CharField(
        label=_('Phone number'),
        required=False,
    )
    address = forms.CharField(
        label=_('Address'),
        required=False,
    )
    picture = forms.ImageField(
        label=_('Picture'),
        required=False,
    )
    

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        label=_('Role'),
        choices=User.ROLE_CHOICES,
        required=False,
    )
    phone_number = forms.CharField(
        label=_('Phone number'),
        required=False,
    )
    address = forms.CharField(
        label=_('Address'),
        required=False,
    )
    picture = forms.ImageField(
        label=_('Picture'),
        required=False,
    )
