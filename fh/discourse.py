from dateutil.parser import parse

from pydiscourse.client import DiscourseClient as BaseDiscourseClient
from pydiscourse.exceptions import DiscourseClientError

from fh.settings import SPEAKUP_DISCOURSE_URL, SPEAKUP_DISCOURSE_API_KEY


class DiscourseClient(BaseDiscourseClient):
    def mxit_user(self, mxit_id):
        """ Get a mxit user by id, if any. """
        return self._get('/mxit/users/{0}.json'.format(mxit_id))['user']

    def create_mxit_user(self, name, email, username, mxit_id, remote_ip, **kwargs):
        """ Get a mxit user by id, if any. """
        return self._post('/mxit/users', name=name, username=username, email=email,
                mxit_id=mxit_id, remote_ip=remote_ip, **kwargs)

    def authenticate_user(self, login, password):
        resp = self._post('/session', login=login, password=password)
        if 'error' in resp:
            raise DiscourseClientError(resp['error'])
        return resp['user']


# discourse client
def discourse_client(anonymous=False, username=None):
    """
    If `anonymous` is True, then return a client that
    doesn't authenticate with the server. This helps prevent
    Admin-only topics from being visible.
    """

    if anonymous:
        api_username = None
        api_key = None
    else:
        api_username = username or 'system'
        api_key = SPEAKUP_DISCOURSE_API_KEY

    return DiscourseClient(SPEAKUP_DISCOURSE_URL, api_username, api_key)

def parse_timestamps(data):
    if isinstance(data, dict):
        for key, val in data.iteritems():
            if val and key.endswith('_at'):
                data[key] = parse(val)
            else:
                parse_timestamps(val)

    elif isinstance(data, list):
        for item in data:
            parse_timestamps(item)
