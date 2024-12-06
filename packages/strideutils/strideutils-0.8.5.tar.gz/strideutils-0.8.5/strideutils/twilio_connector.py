from typing import Iterable, List, Union

from twilio.rest import Client

from strideutils.stride_config import Environment as e
from strideutils.stride_config import config, get_env_or_raise


class TwilioClient:
    """
    Singleton client used to make phone calls
    """

    _instance = None
    call_template = """<Response><Say>{}</Say></Response>"""

    def __new__(cls):
        # Creates a new instance if one does not already exist
        if cls._instance is None:
            cls._instance = super(TwilioClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Prevent re-initialization if a client has already been created
        if hasattr(self, "client"):
            return

        self.account_id = get_env_or_raise(e.TWILIO_ACCOUNT_ID)
        self.api_token = get_env_or_raise(e.TWILIO_API_TOKEN)
        self.alert_numbers = get_env_or_raise(e.TWILIO_ALERTS_NUMBER)
        self.client = Client(self.account_id, self.api_token)

    def call(self, msg: str, to: Union[str, Iterable[str], List[str]]) -> None:
        """
        Make a phone call

        Args:
            msg: A timl formatted message to read aloud to the recipient
            to: A name or list of names that can be looked up in config.PHONE_NUMBERS
            mapping to a 11 digit phone number, with international prefix
            e.g. config.PHONE_NUMBERS['joe'] = +12223334545

        Note: SMS not available without opt-in logic for apps for toll-free verification
        """
        to = [to] if type(to) is str else to
        voice_message = self.call_template.format(msg)
        for destination in to:
            number = config.PHONE_NUMBERS[destination]
            self.client.calls.create(to=number, from_=config.TWILIO_ALERTS_NUMBER, twiml=voice_message)
