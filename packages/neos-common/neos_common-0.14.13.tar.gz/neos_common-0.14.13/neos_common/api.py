import importlib
import inspect

from fastapi import FastAPI

from neos_common import schema, util


def get_error_codes(module_names: str | list[str]) -> schema.ErrorCodes:
    """Get all error codes and messages from the error module."""
    errors = []

    if isinstance(module_names, str):
        module_names = [module_names]

    for module_name in module_names:
        module = importlib.import_module(module_name)

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if hasattr(obj, "title"):
                    o = obj("details")
                    type_ = o.type
                    title = o.title

                    errors.append(
                        schema.ErrorCode(
                            class_name=name,
                            type=type_,
                            title=title,
                        ),
                    )

                elif hasattr(obj, "reason_"):
                    o = obj("debug")
                    type_ = o.reason
                    title = o.message

                    errors.append(
                        schema.ErrorCode(
                            class_name=name,
                            type=type_,
                            title=title,
                        ),
                    )

    return schema.ErrorCodes(errors=errors)


def get_permissions(app: FastAPI, ignore_routes: list[str] | None = None) -> schema.FormattedRoutes:
    ignore_routes = ignore_routes or []
    routes = util.get_routes(app, ignore_routes)

    return schema.FormattedRoutes(routes=routes)
