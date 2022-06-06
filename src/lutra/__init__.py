# Copyright (c) 2021 Pradyun Gedam
# Licensed under MIT License
# SPDX-License-Identifier: MIT
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""A clean and capable Sphinx documentation theme."""

__version__ = "2021.10.09.dev1"

import hashlib
import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import sphinx.application
import sphinx.config
from docutils import nodes
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Text
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.highlighting import PygmentsBridge
from sphinx.transforms.post_transforms import SphinxPostTransform

from .errors import LutraError
from .navigation import should_hide_toc, trim_sidebar_navigation

THEME_PATH = (Path(__file__).parent / "theme" / "lutra").resolve()

logger = logging.getLogger(__name__)

if "debugpy" in os.environ.get("LUTRA_DEBUG", ""):
    import debugpy

    debugpy.listen(5678)

# GLOBAL STATE
_KNOWN_STYLES_IN_USE: Dict[str, Optional[Style]] = {
    "light": None,
    "dark": None,
}


class WrapTableAndMathInAContainerTransform(SphinxPostTransform):
    """A Sphinx post-transform that wraps `table` and `div.math` in a container `div`.

    This makes it possible to handle these overflowing the content-width, which is
    necessary in a responsive theme.
    """

    formats = ("html",)
    default_priority = 500

    def run(self, **kwargs: Any) -> None:
        """Perform the post-transform on `self.document`."""
        for node in list(self.document.findall(nodes.table)):
            new_node = nodes.container(classes=["table-wrapper"])
            new_node.update_all_atts(node)
            node.parent.replace(node, new_node)
            new_node.append(node)

        for node in list(self.document.findall(nodes.math_block)):
            new_node = nodes.container(classes=["math-wrapper"])
            new_node.update_all_atts(node)
            node.parent.replace(node, new_node)
            new_node.append(node)


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


@lru_cache
def _asset_hash(path: str) -> str:
    """Append a `?digest=` to an url based on the file content."""
    full_path = THEME_PATH / "static" / path
    digest = hashlib.md5(full_path.read_bytes()).hexdigest()

    return f"_static/{path}?digest={digest}"


def _add_asset_hashes(static: List[str], add_digest_to: List[str]) -> None:
    for asset in add_digest_to:
        index = static.index("_static/" + asset)
        static[index].filename = _asset_hash(asset)  # type: ignore


def _html_page_context(
    app: sphinx.application.Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: Any,
) -> None:
    assert app.builder

    if "css_files" in context:
        _add_asset_hashes(
            context["css_files"],
            ["styles/lutra.css", "styles/lutra-extensions.css"],
        )
    if "scripts" in context:
        _add_asset_hashes(
            context["scripts"],
            ["scripts/lutra.js"],
        )

    # Basic constants
    context["lutra_version"] = __version__

    # Values computed from page-level context.
    toctree = context["toctree"]
    toctree_html = toctree(includehidden=True, titles_only=True, maxdepth=-1)

    was_trimmed, toctree_html = trim_sidebar_navigation(
        toctree_html, style=context["theme_navigation_style"]
    )
    context["lutra_trimmed_toctree"] = was_trimmed
    context["lutra_toctree_html"] = toctree_html
    context["lutra_hide_toc"] = should_hide_toc(context)
    context["lutra_modified"] = (
        app.builder.config.lutra_modified or app.config.html_theme != "lutra"
    )

    # Inject information about styles
    context["lutra_pygments"] = {
        "light": get_pygments_style_colors(
            _KNOWN_STYLES_IN_USE["light"],
            fallbacks=dict(
                foreground="black",
                background="white",
            ),
        ),
        "dark": get_pygments_style_colors(
            _KNOWN_STYLES_IN_USE["dark"],
            fallbacks=dict(
                foreground="white",
                background="black",
            ),
        ),
    }


def _builder_inited(app: sphinx.application.Sphinx) -> None:
    if not isinstance(app.builder, StandaloneHTMLBuilder):
        raise LutraError(
            reference="used-with-non-html-build",
            message="Lutra is being used as an extension for a non-HTML build!",
            hint_stmt=(
                "Did you list 'lutra' in the `extensions` in conf.py? "
                "If so, please remove it, since that will enable it for all Sphinx "
                "builders (rather than just HTML builders) which does not work."
            ),
        )

    if app.config.html_sidebars:
        raise LutraError(
            reference="using-html_sidebars",
            message="Lutra does not support the html_sidebars configuration.",
            hint_stmt="See http://pradyunsg.me/lutra/customisation/sidebar/",
        )

    # Our `lutra.js` file needs to be loaded as soon as possible.
    app.add_js_file("scripts/lutra.js", priority=200)

    # 500 is the default priority for extensions, we want this after this.
    app.add_css_file("styles/lutra-extensions.css", priority=600)

    builder = app.builder
    assert builder, "what?"
    assert (
        builder.highlighter is not None
    ), "there should be a default style known to Sphinx"
    assert (
        builder.dark_highlighter is None
    ), "there shouldn't be a dark style known to Sphinx"
    update_known_styles_state(app)

    def _update_default(key: str, /, *, new_default: Any) -> None:
        app.config.values[key] = (new_default, *app.config.values[key][1:])

    # Change the default permalinks icon
    _update_default("html_permalinks_icon", new_default="#")


def update_known_styles_state(app: sphinx.application.Sphinx) -> None:
    """Update a global store of known styles of this application."""
    global _KNOWN_STYLES_IN_USE

    _KNOWN_STYLES_IN_USE = {
        "light": _get_light_style(app),
        "dark": _get_dark_style(app),
    }


def _get_light_style(app: sphinx.application.Sphinx) -> Style:
    return app.builder.highlighter.formatter_args["style"]


def _get_dark_style(app: sphinx.application.Sphinx) -> Style:
    try:
        dark_style = app.config._raw_config["pygments_dark_style"]
    except KeyError:
        dark_style = app.config.pygments_dark_style
    return PygmentsBridge("html", dark_style).formatter_args["style"]


def get_pygments_stylesheet() -> str:
    """Generate the theme-specific pygments.css.

    There is no way to tell Sphinx how the theme handles dark mode; at this time.
    """
    light_formatter = HtmlFormatter(style=_KNOWN_STYLES_IN_USE["light"])
    dark_formatter = HtmlFormatter(style=_KNOWN_STYLES_IN_USE["dark"])

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


def _build_finished(
    app: sphinx.application.Sphinx,
    exception: Optional[Exception],
) -> None:
    if exception is not None:
        return

    # We overwrite the default pygments.css file, because this theme has different
    # needs from it, compared to what Sphinx generates.
    assert app.builder
    with open(os.path.join(app.builder.outdir, "_static", "pygments.css"), "w") as f:
        f.write(get_pygments_stylesheet())


def setup(app: sphinx.application.Sphinx) -> Dict[str, Any]:
    """Entry point for sphinx theming."""
    app.require_sphinx("4.0")

    app.add_config_value(
        "pygments_dark_style",
        default="lutra.styles.StyloDarkStyle",
        rebuild="env",
        types=[str],
    )
    app.add_config_value("lutra_modified", default=False, rebuild="env", types=[bool])

    app.add_html_theme("lutra", str(THEME_PATH))
    app.add_post_transform(WrapTableAndMathInAContainerTransform)

    app.connect("html-page-context", _html_page_context)
    app.connect("builder-inited", _builder_inited)
    app.connect("build-finished", _build_finished)

    app.setup_extension("sphinxext.opengraph")

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }
