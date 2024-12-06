"""Common utils to support neos cli applications."""

import typing
from csv import DictWriter
from io import StringIO

from fastapi import FastAPI

from neos_common.util import get_routes


class RoutesPrinter:
    """Routes printer."""

    def __init__(self, app: FastAPI, ignore_routes: list[str]) -> None:
        self.routes = get_routes(app, ignore_routes)

    def echo(self, echo_fn: typing.Callable) -> None:
        """Print routes to console."""
        for route in self.routes:
            echo_fn(f"{route.summary}")
            echo_fn(f"{route.methods:<10}{route.path}")
            if route.permission_pairs:
                echo_fn("{:<12}{}".format("", route.logic_operator.upper()))
            for permission_pair in route.permission_pairs:
                echo_fn("{:<14}action:   {}".format("", permission_pair.action))
                echo_fn("{:<14}resource: {}".format("", permission_pair.resource))
                echo_fn()
            echo_fn()


class RoutesCSVPrinter(RoutesPrinter):
    """Routes CSV printer."""

    def echo(self, echo_fn: typing.Callable) -> None:
        """Print routes in csv format."""
        csv_output = StringIO()
        writer = DictWriter(csv_output, fieldnames=["methods", "path", "summary", "operator", "action", "resource"])
        writer.writeheader()

        for route in self.routes:
            header = True
            if len(route.permission_pairs) == 0:
                writer.writerow(
                    {
                        "methods": route.methods,
                        "path": route.path,
                        "summary": route.summary,
                        "operator": "",
                        "action": "",
                        "resource": "",
                    },
                )
            else:
                for permission_pair in route.permission_pairs:
                    writer.writerow(
                        {
                            "methods": route.methods if header else "",
                            "path": route.path if header else "",
                            "summary": route.summary,
                            "operator": route.logic_operator.upper(),
                            "action": permission_pair.action,
                            "resource": permission_pair.resource,
                        },
                    )
                    header = False

        csv_output.seek(0)
        echo_fn(csv_output.read())
