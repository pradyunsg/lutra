#!python3
"""Validate that the variables are properly defined in `variables.css`."""

from pathlib import Path

filename = (
    Path(__file__).parent.parent / "src/lutra/assets/styles/scaffold/variables.css"
)

# Poor man's CSS parser
by_selector = {}
with open(filename) as f:
    current_selector = None
    for i, raw_line in enumerate(f):
        lineno = i + 1
        line = raw_line.strip()

        if not line:
            continue
        elif line.startswith("/*"):
            if current_selector is not None:
                by_selector[current_selector].append(line)
        elif line.endswith(" {"):
            current_selector = line[:-2]
            if current_selector in by_selector:
                raise Exception(
                    f"{lineno}: {current_selector!r} already in {by_selector}"
                )
            by_selector[current_selector] = []
        elif line == "}":
            current_selector = None
        elif line.startswith("--"):
            variable_name, _, _ = line.partition(":")
            if variable_name in by_selector[current_selector]:
                raise Exception(
                    f"{lineno}: {variable_name!r} already in selector "
                    f"{current_selector!r}"
                )
            by_selector[current_selector].append(variable_name)


def ensure_no_common(*, base, theme):
    if common := set(base) & set(theme):
        raise Exception(f"Got theme-specific-override: {common}")


def colorized(line):
    if line.startswith("-"):
        return f"\033[31m{line}\033[0m"
    if line.startswith("+"):
        return f"\033[32m{line}\033[0m"
    return line


def ensure_all_same(*, light, dark):
    if light == dark:
        return

    import difflib

    diff = "\n".join(
        colorized(line)
        for line in difflib.unified_diff(
            light, dark, "only-in-light", "only-in-dark", lineterm="", n=5
        )
    )
    raise Exception(f"Deviation between light and dark variables!\n\n{diff}")


assert set(by_selector) == {"html", "html:not(.dark)", "html.dark"}
ensure_no_common(
    base=by_selector["html"],
    theme=by_selector["html:not(.dark)"],
)
ensure_no_common(
    base=by_selector["html"],
    theme=by_selector["html.dark"],
)
ensure_all_same(
    light=by_selector["html:not(.dark)"],
    dark=by_selector["html.dark"],
)
print("All good!")
