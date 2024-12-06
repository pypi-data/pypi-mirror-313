import re
from pathlib import Path

import pdoc
from changelog_gen.context import Context


def generate_docs(ctx: Context, _new: str) -> list[str]:
    output_dir = Path("./docs")
    modules = ctx.config.custom["pdoc"]["modules"]

    context = pdoc.Context()

    modules = [
        pdoc.Module(mod, context=context, skip_errors=ctx.config.custom["pdoc"].get("skip_errors", False))
        for mod in modules
    ]
    pdoc.link_inheritance(context)

    def recursive_mds(mod: pdoc.Module) -> pdoc.Module:
        yield mod
        for submod in mod.submodules():
            yield from recursive_mds(submod)

    paths = []

    for mod in modules:
        for module in recursive_mds(mod):
            path = re.sub(r"\.html$", ".md", module.url())
            out = output_dir / path
            out.parent.mkdir(exist_ok=True, parents=True)
            with out.open("w") as f:
                f.write(module.text(show_inherited_members=False))
            paths.append(str(out))

    return paths
