import logging

from django import forms
from django.core.exceptions import ValidationError

from fh.discourse import discourse_client, parse_timestamps, DiscourseClientError

log = logging.getLogger(__name__)

class LoginForm(forms.Form):
    username = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean(self):
        """ authenticate user """
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
