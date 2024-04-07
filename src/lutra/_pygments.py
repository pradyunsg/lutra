from functools import lru_cache
from typing import Dict

from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Text
from sphinx.highlighting import PygmentsBridge


def get_pygments_style_colors(
    style: Style, *, fallbacks: Dict[str, str]
) -> Dict[str, str]:
    """Get background/foreground colors for given pygments style."""
    background = style.background_color
    text_colors = style.style_for_token(Text)
    foreground = text_colors["color"]

    if not background:
        background = fallbacks["background"]

    if not foreground:
        foreground = fallbacks["foreground"]
    else:
        foreground = f"#{foreground}"

    return {"background": background, "foreground": foreground}


@lru_cache(maxsize=2)
def get_colors_for_codeblocks(
    highlighter: PygmentsBridge, *, fg: str, bg: str
) -> Dict[str, str]:
    """Get background/foreground colors for given pygments style."""
    return get_pygments_style_colors(
        highlighter.formatter_args["style"],
        fallbacks={
            "foreground": fg,
            "background": bg,
        },
    )


def get_pygments_stylesheet(light_style: Style, dark_style: Style) -> str:
    """Generate the theme-specific pygments.css.

    There is no way to tell Sphinx how the theme handles dark mode; at this time.
    """
    light_formatter = HtmlFormatter(style=light_style)
    dark_formatter = HtmlFormatter(style=dark_style)

    light_prefix = "html:not(.dark) .highlight"
    dark_prefix = "html.dark .highlight"

    # This section uses the "internal" methods of HtmlFormatter, to get the styles
    # such that they're namespaced. This helps ensure that they only apply on the
    # relevant styles.
    lines = []
    lines.extend(
        [
            f"{light_prefix} {line}"
            for line in light_formatter.get_linenos_style_defs()
            if not line.startswith("pre {")
        ]
    )
    lines.extend(light_formatter.get_background_style_defs(light_prefix))
    lines.extend(light_formatter.get_token_style_defs(light_prefix))
    lines.extend(
        [
            f"{dark_prefix} {line}"
            for line in dark_formatter.get_linenos_style_defs()
            if not line.startswith("pre {")
        ]
    )
    lines.extend(dark_formatter.get_background_style_defs(dark_prefix))
    lines.extend(dark_formatter.get_token_style_defs(dark_prefix))

    return "\n".join(lines)
