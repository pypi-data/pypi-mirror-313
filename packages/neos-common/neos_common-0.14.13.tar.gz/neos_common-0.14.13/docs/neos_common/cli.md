Module neos_common.cli
======================
Common utils to support neos cli applications.

Classes
-------

`RoutesCSVPrinter(app: fastapi.applications.FastAPI, ignore_routes: list[str])`
:   Routes CSV printer.

    ### Ancestors (in MRO)

    * neos_common.cli.RoutesPrinter

    ### Methods

    `echo(self, echo_fn: Callable) ‑> None`
    :   Print routes in csv format.

`RoutesPrinter(app: fastapi.applications.FastAPI, ignore_routes: list[str])`
:   Routes printer.

    ### Descendants

    * neos_common.cli.RoutesCSVPrinter

    ### Methods

    `echo(self, echo_fn: Callable) ‑> None`
    :   Print routes to console.