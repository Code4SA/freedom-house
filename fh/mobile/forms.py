import logging

from django import forms
from django.core.exceptions import ValidationError

from fh.discourse import discourse_client, parse_timestamps
from pydiscourse.exceptions import DiscourseError, DiscourseClientError

log = logging.getLogger(__name__)

class LoginForm(forms.Form):
    username = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean(self):
        """ authenticate user """
        if not self._errors:
            # call discourse
            discourse = discourse_client()
            try:
                user = discourse.authenticate_user(login=self.cleaned_data['username'],
                                                   password=self.cleaned_data['password'])
                log.info("Authenticated as: %s" % user)
                self.discourse_username = user['username']
            except DiscourseClientError as e:
                raise ValidationError(e.message)

        return self.cleaned_data


class SignupForm(forms.Form):
    email = forms.EmailField(label='Email', help_text='Never shown to the public')
    username = forms.CharField(label='Username', help_text='Unique, no spaces, short')
    name = forms.CharField(label='Name', help_text='Your full name (optional)', required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='At least 8 characters')

    next = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean(self):
        """ create user """
        if not self._errors:
            # call discourse
            discourse = discourse_client()
            try:
                user = discourse.create_user(
                    name=self.cleaned_data['name'],
                    username=self.cleaned_data['username'],
                    email=self.cleaned_data['email'],
                    password=self.cleaned_data['password'],
                    active=True)

                log.info("Created user: %s" % user)
                self.discourse_username = self.cleaned_data['username']
            except DiscourseError as e:
                raise ValidationError(e.message)

        return self.cleaned_data


class ForgotPasswordForm(forms.Form):
    login = forms.CharField(label='Email or username', max_length=100)
