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

"""Transform the navigation tree, from Sphinx's toctree function's output."""

from functools import lru_cache
from typing import Any, Dict, Tuple

from bs4 import BeautifulSoup


@lru_cache
def trim_sidebar_navigation(toctree_html: str, *, style: str) -> Tuple[bool, str]:
    """Trim `toctree_html` based on what `style` is."""
    allowed_styles = ["plain", "scoped-sidebar"]
    assert (
        style in allowed_styles
    ), f"Got an invalid `navigation_style`: {style!r} (valid values: {allowed_styles})"

    if style == "plain":
        return False, toctree_html

    # TODO: explore if I can just... like... use regex or substrings for this next
    # block, instead of parsing the HTML. Or, like, operate on the DOM that Sphinx has
    # internally.
    soup = BeautifulSoup(toctree_html, features="html.parser")

    # Check if there's an active level-1 toctree element.
    node = soup.find("li", class_="toctree-l1 current")
    if not node:
        return False, toctree_html

    # If here, it's a page within a "section" of the documentation.
    retval = BeautifulSoup()

    # If there's a caption before this node, include that as well.
    if (
        node.parent
        and node.parent.previous_sibling
        and node.parent.previous_sibling.previous_sibling
        and node.parent.previous_sibling.previous_sibling.name == "p"
        and node.parent.previous_sibling.previous_sibling.get("class") == ["caption"]
    ):
        retval.append(node.parent.previous_sibling.previous_sibling)

    retval.append(node.parent)
    return True, str(retval)


@lru_cache
def has_not_enough_items_to_show_toc(toc: str) -> bool:
    """Check if the toc has one or fewer items."""
    assert toc

    soup = BeautifulSoup(toc, "html.parser")
    return len(soup.find_all("li")) <= 1


def should_hide_toc(context: Dict[str, Any]) -> bool:
    """Check whether the table of contents should be hidden."""
    file_meta = context.get("meta", None) or {}
    if "hide-toc" in file_meta:
        return True
    elif "toc" not in context:
        return True
    elif not context["toc"]:
        return True

    return has_not_enough_items_to_show_toc(context["toc"])
