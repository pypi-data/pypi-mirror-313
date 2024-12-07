import json
import logging
import requests


logger = logging.getLogger(__name__)


class Handler(object):
    @staticmethod
    def is_interested_in(event):
        raise NotImplementedError

    def handle_event(self, event):
        raise NotImplementedError


class HTTPBouncerMessageHandler(Handler):
    def __init__(self, destination):
        self.destination = destination

    @staticmethod
    def is_interested_in(event):
        return True

    def handle_event(self, event):
        message_id = event.message.id
        message_body = event.message.body
        if isinstance(message_body, memoryview):
            message_body = message_body.tobytes()
        try:
            r = requests.post(
                self.destination,
                json={
                    "headers": event.message.properties,
                    "msg": json.loads(message_body),
                },
                timeout=(10, 50),
            )
            logger.info(
                f"Sent {message_id} to {self.destination} - Result: {r.status_code}"
            )
        except (ValueError, TypeError):
            logger.error(
                "Can't json load event id %s - message body: %s"
                % (message_id, message_body)
            )
