import contextlib

from fastapi import FastAPI

from neos_common.schema import FormattedRoute, PermissionPair


def get_routes(app: FastAPI, ignore_routes: list[str]) -> list[FormattedRoute]:
    routes = []
    for route in app.routes:
        if route.path in ignore_routes:
            continue

        methods = ""
        if hasattr(route, "methods"):
            methods = ", ".join(sorted(route.methods))

        path = route.path
        summary = None
        with contextlib.suppress(AttributeError):
            summary = route.summary

        permission_pairs = []
        logic_operator = "and"
        if hasattr(route, "openapi_extra") and route.openapi_extra is not None:
            actions = []
            resources = []
            for key in sorted(route.openapi_extra):
                if key.startswith("x-iam-action"):
                    actions.append(route.openapi_extra[key])
                if key.startswith("x-iam-resource"):
                    resources.append(route.openapi_extra[key])

            permission_pairs = [PermissionPair(action=a, resource=r) for a, r in zip(actions, resources, strict=False)]
            logic_operator = route.openapi_extra.get("logic-operator", "and")

        routes.append(
            FormattedRoute(
                methods=methods,
                path=path,
                permission_pairs=permission_pairs,
                summary=summary,
                logic_operator=logic_operator,
            ),
        )

    return routes
