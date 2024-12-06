from neos_common import error


def test_service_connection_error():
    e = error.ServiceConnectionError(message="message", debug="debug_message")

    assert e.reason == "service-connection-error"
    assert e.status == "unhandled"
    assert e.message == "message"
    assert e.debug == "debug_message"
