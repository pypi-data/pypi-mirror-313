from dci_umb.cli import parse_arguments
from mock import patch


def test_parse_arguments():
    args = parse_arguments(
        [
            "--key",
            "/tmp/prod.key",
            "--crt",
            "/tmp/prod.crt",
            "--ca",
            "/tmp/RH-IT-Root-CA.crt",
            "--broker",
            "amqps://broker01.example.org:5671",
            "--broker",
            "amqps://broker02.example.org:5671",
            "--source",
            "topic://VirtualTopic.*>",
            "--destination",
            "http://localhost:5000/api/v1/events",
        ]
    )
    assert args["key_file"] == "/tmp/prod.key"
    assert args["crt_file"] == "/tmp/prod.crt"
    assert args["ca_file"] == "/tmp/RH-IT-Root-CA.crt"
    assert args["brokers"] == [
        "amqps://broker01.example.org:5671",
        "amqps://broker02.example.org:5671",
    ]
    assert args["sources"] == ["topic://VirtualTopic.*>"]
    assert args["destinations"] == ["http://localhost:5000/api/v1/events"]


def test_parse_arguments_from_env_variable():
    with patch.dict(
        "os.environ",
        {
            "KEY_FILE_PATH": "/tmp/umb.key",
            "CRT_FILE_PATH": "/tmp/umb.crt",
            "CA_FILE_PATH": "/tmp/umb.ca",
            "BROKERS": "amqps://broker01.example.org:5671 amqps://broker02.example.org:5671",
            "TOPIC_SOURCE": "topic://VirtualTopic.*>",
            "HTTP_DESTINATION_HOST": "http://localhost:5000/api/v1/events",
        },
    ):
        args = parse_arguments([])
        assert args["key_file"] == "/tmp/umb.key"
        assert args["crt_file"] == "/tmp/umb.crt"
        assert args["ca_file"] == "/tmp/umb.ca"
        assert args["brokers"] == [
            "amqps://broker01.example.org:5671",
            "amqps://broker02.example.org:5671",
        ]
        assert args["sources"] == ["topic://VirtualTopic.*>"]
        assert args["destinations"] == ["http://localhost:5000/api/v1/events"]


def test_parse_arguments_from_env_variable_api_v2():
    with patch.dict(
        "os.environ",
        {
            "KEY_FILE_PATH": "/tmp/umb.key",
            "CRT_FILE_PATH": "/tmp/umb.crt",
            "CA_FILE_PATH": "/tmp/umb.ca",
            "BROKERS": "amqps://broker01.example.org:5671 amqps://broker02.example.org:5671",
            "TOPIC_SOURCES": "topic://VirtualTopic.a topic://VirtualTopic.b",
            "HTTP_DESTINATION_HOST": "http://localhost:5000/api/v1/events",
        },
    ):
        args = parse_arguments([])
        assert args["key_file"] == "/tmp/umb.key"
        assert args["crt_file"] == "/tmp/umb.crt"
        assert args["ca_file"] == "/tmp/umb.ca"
        assert args["brokers"] == [
            "amqps://broker01.example.org:5671",
            "amqps://broker02.example.org:5671",
        ]
        assert args["sources"] == ["topic://VirtualTopic.a", "topic://VirtualTopic.b"]
        assert args["destinations"] == ["http://localhost:5000/api/v1/events"]


def test_parse_arguments_multiple_destinations():
    args = parse_arguments(
        [
            "--destination",
            "http://localhost:5000/api/v1/events",
            "--destination",
            "http://remote_host:5000/api/v1/events",
        ]
    )
    assert args["destinations"] == [
        "http://localhost:5000/api/v1/events",
        "http://remote_host:5000/api/v1/events",
    ]


def test_parse_arguments_from_env_variable_api_v2_multiple_destinations():
    with patch.dict(
        "os.environ",
        {
            "HTTP_DESTINATION_HOSTS": "http://localhost:5000/api/v1/events http://remote_host:5000/api/v1/events",
        },
    ):
        args = parse_arguments([])
        assert args["destinations"] == [
            "http://localhost:5000/api/v1/events",
            "http://remote_host:5000/api/v1/events",
        ]
