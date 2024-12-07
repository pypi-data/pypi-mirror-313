import mock

from dci_umb.handler import HTTPBouncerMessageHandler

from tests.factories import Event


def test_is_interested_in_all_events():
    event = Event({}, {})
    handler = HTTPBouncerMessageHandler(destination="http://localhost:5000/events")
    assert handler.is_interested_in(event)


@mock.patch("dci_umb.handler.requests.post")
def test_HTTPBouncerMessageHandler_send_body_in_post_request(mocked_requests_post):
    event = Event({"id": "e1"}, {"message-id": "ID:id1234"})
    destination = "http://localhost:5000/events"
    handler = HTTPBouncerMessageHandler(destination=destination)
    handler.handle_event(event)
    mocked_requests_post.assert_called_once_with(
        destination,
        json={
            "msg": {"id": "e1"},
            "headers": {"message-id": "ID:id1234"},
        },
        timeout=(10, 50),
    )
