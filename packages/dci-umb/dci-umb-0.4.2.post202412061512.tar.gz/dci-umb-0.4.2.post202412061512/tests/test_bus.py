import mock
import requests

from dci_umb.bus import Bus
from dci_umb.handler import Handler

from tests.factories import Event


def test_bus_take_handlers_in_constructor():
    bus = Bus([Handler(), Handler()])
    assert len(bus.handlers) == 2


def test_bus_dispatch_an_event_to_only_interested_handlers():
    handler1 = mock.MagicMock()
    handler1.is_interested_in.return_value = False

    handler2 = mock.MagicMock()
    handler2.is_interested_in.return_value = True

    bus = Bus([handler1, handler2])
    event = Event({"topic": "/topic/VirtualTopic.eng.rtt.ci"}, {})
    bus.dispatch_event(event)

    handler1.handle_event.assert_not_called()
    handler2.handle_event.assert_called_once_with(event)


def test_bus_ignore_error_occuring_in_an_handler():
    handler1 = mock.MagicMock()
    handler1.is_interested_in.return_value = True
    handler1.handle_event.side_effect = requests.exceptions.ConnectionError()

    handler2 = mock.MagicMock()
    handler2.is_interested_in.return_value = True

    bus = Bus([handler1, handler2])
    event = Event({"topic": "/topic/VirtualTopic.eng.rtt.ci"}, {})
    bus.dispatch_event(event)

    handler1.handle_event.assert_called_once_with(event)
    handler2.handle_event.assert_called_once_with(event)
