from dateutil.parser import parse

from pydiscourse.client import DiscourseClient as BaseDiscourseClient

from fh.settings import SPEAKUP_DISCOURSE_URL, SPEAKUP_DISCOURSE_USERNAME, SPEAKUP_DISCOURSE_API_KEY


class DiscourseClient(BaseDiscourseClient):
    def mxit_user(self, mxit_id):
        # TODO:
        return None




# discourse client
discourse_client = DiscourseClient(
    SPEAKUP_DISCOURSE_URL,
    api_username=SPEAKUP_DISCOURSE_USERNAME,
    api_key=SPEAKUP_DISCOURSE_API_KEY)

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
