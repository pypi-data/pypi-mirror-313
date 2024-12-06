from unittest import mock

import pytest

cli = pytest.importorskip("neos_common.cli")


def test_routes_printer():
    fastapi_mock = mock.Mock(
        routes=[
            mock.Mock(
                path="/test",
                methods=["GET"],
                summary="Test endpoint",
                openapi_extra={
                    "x-iam-action": "do:test",
                    "x-iam-resource": "urn:test",
                },
            ),
            mock.Mock(
                path="/ignore",
                methods=["GET"],
                summary="Ignored endpoint",
                openapi_extra={
                    "x-iam-action": "do:test",
                    "x-iam-resource": "urn:test",
                },
            ),
        ],
    )

    echo_fn = mock.Mock()

    cli.RoutesPrinter(fastapi_mock, ["/ignore"]).echo(echo_fn)

    assert echo_fn.call_args_list == [
        mock.call("Test endpoint"),
        mock.call("GET       /test"),
        mock.call("            AND"),
        mock.call("              action:   do:test"),
        mock.call("              resource: urn:test"),
        mock.call(),
        mock.call(),
    ]


def test_routes_printer_no_permissions():
    fastapi_mock = mock.Mock(
        routes=[
            mock.Mock(
                path="/test",
                methods=["GET"],
                summary="Test endpoint",
                openapi_extra={},
            ),
            mock.Mock(
                path="/ignore",
                methods=["GET"],
                summary="Ignored endpoint",
                openapi_extra={
                    "x-iam-action": "do:test",
                    "x-iam-resource": "urn:test",
                },
            ),
        ],
    )

    echo_fn = mock.Mock()

    cli.RoutesPrinter(fastapi_mock, ["/ignore"]).echo(echo_fn)

    assert echo_fn.call_args_list == [
        mock.call("Test endpoint"),
        mock.call("GET       /test"),
        mock.call(),
    ]


def test_csv_routes_printer():
    fastapi_mock = mock.Mock(
        routes=[
            mock.Mock(
                path="/test",
                methods=["GET"],
                summary="Test endpoint",
                openapi_extra={
                    "x-iam-action": "do:test",
                    "x-iam-resource": "urn:test",
                },
            ),
            mock.Mock(
                path="/ignore",
                methods=["GET"],
                summary="Ignored endpoint",
                openapi_extra={
                    "x-iam-action": "do:test",
                    "x-iam-resource": "urn:test",
                },
            ),
        ],
    )

    echo_fn = mock.Mock()

    cli.RoutesCSVPrinter(fastapi_mock, ["/ignore"]).echo(echo_fn)

    assert echo_fn.call_args_list == [
        mock.call("methods,path,summary,operator,action,resource\r\nGET,/test,Test endpoint,AND,do:test,urn:test\r\n"),
    ]


def test_csv_routes_printer_no_permissions():
    fastapi_mock = mock.Mock(
        routes=[
            mock.Mock(
                path="/test",
                methods=["GET"],
                summary="Test endpoint",
                openapi_extra={},
            ),
            mock.Mock(
                path="/ignore",
                methods=["GET"],
                summary="Ignored endpoint",
                openapi_extra={
                    "x-iam-action": "do:test",
                    "x-iam-resource": "urn:test",
                },
            ),
        ],
    )

    echo_fn = mock.Mock()

    cli.RoutesCSVPrinter(fastapi_mock, ["/ignore"]).echo(echo_fn)

    assert echo_fn.call_args_list == [
        mock.call("methods,path,summary,operator,action,resource\r\nGET,/test,Test endpoint,,,\r\n"),
    ]
