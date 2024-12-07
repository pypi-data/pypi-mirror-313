import logging


logger = logging.getLogger(__name__)


class Bus(object):
    def __init__(self, handlers):
        self.handlers = handlers

    def _handle_event(self, handler, event):
        try:
            if handler.is_interested_in(event):
                handler.handle_event(event)
        except Exception as e:
            logger.exception(e)
            logger.error(
                "Can't handle event %s with handler %s"
                % (event.message.body, handler.__class__.__name__)
            )

    def dispatch_event(self, event):
        for handler in self.handlers:
            self._handle_event(handler, event)
