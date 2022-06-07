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
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Tuple, TypeVar

import docutils.nodes
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment.adapters.toctree import TocTree
from sphinx.locale import get_translation

_ = get_translation("lutra")
T = TypeVar("T")


class NavigationInformation(NamedTuple):
    """Container for information relevant to rendered navigation."""

    toctree_html: str
    tabs_html: str


def make_pairs(iterable: Iterable[T]) -> List[Tuple[T, T]]:
    """Given an iterable, make pairs of odd and even pair values."""
    double_iter = [iter(iterable)] * 2
    return list(zip(*double_iter))  # type: ignore


@lru_cache(maxsize=8)
def _get_toctree(builder: StandaloneHTMLBuilder) -> TocTree:
    assert builder.env
    return TocTree(builder.env)


def render_fragment(
    builder: StandaloneHTMLBuilder, node: docutils.nodes.Element
) -> str:
    """Render the given node as an HTML fragment, using the builder provided."""
    return builder.render_partial(node)["fragment"]


def _plain_navigation(
    builder: StandaloneHTMLBuilder,
    toctree: docutils.nodes.Element,
) -> NavigationInformation:
    """Use what Sphinx provides out-of-the-box. No tabs."""
    toctree_html = render_fragment(builder, toctree)

    return NavigationInformation(
        toctree_html=toctree_html,
        tabs_html="",
    )


def _get_fragment_for_current_top_level_bullet_list(
    toctree: docutils.nodes.Element,
) -> Optional[docutils.nodes.Element]:
    for index, element in enumerate(toctree):
        if not element.attributes.get("iscurrent"):
            continue

        toctree_fragment = element
        # If there's a caption before this bullet list, include it.
        if not index:
            return None
        if toctree[index - 1].tagname != "title":  # type: ignore
            return None

        toctree_fragment = toctree.copy()
        toctree_fragment.append(toctree[index - 1])
        toctree_fragment.append(element)
        return toctree_fragment

    return None


def _subtree_caption_navigation(
    builder: StandaloneHTMLBuilder,
    toctree: docutils.nodes.Element,
) -> NavigationInformation:
    """Show the top-level bullet list that the page is within, with caption. No tabs."""
    # Validation
    if len(toctree) <= 1:
        raise Exception(
            "Do not have enough toctrees for the navigation style used. "
            "TODO: Improve this message."
        )

    for index, element in enumerate(toctree):
        # Allow the first element to be anything. This permits use cases where
        # you don't add a caption for the first portion of toctree.
        if index == 0:
            continue
        if toctree[index].tagname == "bullet_list":  # type: ignore
            if toctree[index - 1].tagname != "title":  # type: ignore
                raise Exception(
                    "The declared toctree structure does not follow the style "
                    "needed for this navigation style. Expect all `toctree` "
                    "declarations to have a caption. TODO: improve this msg."
                )

    # Locate the current bullet_list, or use the entire tree.
    toctree_fragment = _get_fragment_for_current_top_level_bullet_list(toctree)
    if toctree_fragment is None:
        toctree_fragment = toctree

    toctree_html = render_fragment(builder, toctree_fragment)

    return NavigationInformation(
        toctree_html=toctree_html,
        tabs_html="",
    )


def _subtree_document_navigation(
    builder: StandaloneHTMLBuilder,
    toctree: docutils.nodes.Element,
) -> NavigationInformation:
    """Show the top-level document that the page is under. No tabs."""
    # Determine which top-level document this falls under
    parent_toctree = None
    top_level_document = None
    for element in toctree.children:
        assert isinstance(element, docutils.nodes.Element)
        if element.attributes.get("iscurrent"):
            parent_toctree = element
            break

    if parent_toctree is not None:
        for element in parent_toctree.children:
            assert isinstance(element, docutils.nodes.Element)
            if element.attributes.get("iscurrent"):
                top_level_document = element

    # Determine and render the toctree fragment
    if top_level_document is not None:
        assert parent_toctree
        bullet_list = parent_toctree.copy()
        bullet_list += top_level_document

        toctree_fragment = toctree.copy()
        toctree_fragment += bullet_list
    else:
        # No current tab found. Let's render the entire toctree.
        toctree_fragment = toctree

    toctree_html = render_fragment(builder, toctree_fragment)

    return NavigationInformation(
        toctree_html=toctree_html,
        tabs_html="",
    )


def _tabs_caption_navigation(
    builder: StandaloneHTMLBuilder,
    toctree: docutils.nodes.Element,
) -> NavigationInformation:
    """Use captions of every toctree as tabs, and show current toctree in the sidebar.

    The homepage gets the entire documentation tree.
    """
    for index, element in enumerate(toctree):
        # Validate that the toctree has the right structure: [title, bullet_list]*n
        if index % 2:
            if element.tagname != "bullet_list":
                raise Exception("Bad toctree structure!")
        else:
            if element.tagname != "title":
                raise Exception("Bad toctree structure!")

    documentation_sections = make_pairs(toctree)

    # Look for the "current" item (and associated tab/caption).
    current_tab = None  # None means no current tab.
    for caption, bullet_list in documentation_sections:
        if not bullet_list.attributes.get("iscurrent"):
            continue

        current_tab = (caption, bullet_list)
        toctree_fragment = toctree.copy()
        toctree_fragment.append(caption.deepcopy())
        toctree_fragment.append(bullet_list.deepcopy())
        break
    else:
        # No current tab found. Let's render the entire toctree.
        toctree_fragment = toctree

    # Sidebar
    toctree_html = render_fragment(builder, toctree_fragment)

    # Tabs
    tab_list_to_render = docutils.nodes.bullet_list(classes=["lutra-tabs"])

    # TODO: Figure out if I want to allow adding a `Home` tab here.
    # home_tab_item = docutils.nodes.list_item()
    # home_tab_item += docutils.nodes.Text(
    #     _("Home") + " [todo: figure out the reference]"
    # )
    # if current_tab is None:
    #     home_tab_item.attributes["classes"].append("current")
    # tab_list_to_render += home_tab_item

    for caption, bullet_list in documentation_sections:
        list_item = bullet_list[0]

        tab_item = list_item.copy()
        tab_item.attributes["classes"].remove("toctree-l1")
        tab_inner = list_item[0].deepcopy()
        tab_inner[0].clear()
        tab_inner[0] += docutils.nodes.Text(caption.astext())

        tab_item += tab_inner
        if (caption, bullet_list) == current_tab:
            tab_item.attributes["classes"].append("current")

        tab_list_to_render.append(tab_item)

    tabs_html = render_fragment(builder, tab_list_to_render)

    return NavigationInformation(
        toctree_html=toctree_html,
        tabs_html=tabs_html,
    )


def _tabs_document_navigation(
    builder: StandaloneHTMLBuilder,
    toctree: docutils.nodes.Element,
) -> NavigationInformation:
    """Use top-level documents as tabs, and show their subtree in the sidebar.

    The homepage gets the entire documentation tree.
    """
    # Collect all top-level documents, as tabs.
    tabs = []
    for bullet_list in toctree.children:
        assert isinstance(bullet_list, docutils.nodes.Element)
        if bullet_list.tagname != "bullet_list":
            continue
        for list_item in bullet_list.children:
            tab = list_item.copy()
            assert isinstance(tab, docutils.nodes.Element)
            tab.attributes["classes"].remove("toctree-l1")  # type: ignore
            tab.append(list_item.children[0].deepcopy())
            tabs.append(tab)

    # Determine which top-level document this falls under
    parent_toctree = None
    top_level_document = None
    for element in toctree.children:
        assert isinstance(element, docutils.nodes.Element)
        if element.attributes.get("iscurrent"):
            parent_toctree = element
            break

    if parent_toctree is not None:
        for element in parent_toctree.children:
            assert isinstance(element, docutils.nodes.Element)
            if element.attributes.get("iscurrent"):
                top_level_document = element

    # Determine and render the toctree fragment
    if top_level_document is not None:
        assert parent_toctree
        bullet_list = parent_toctree.copy()
        bullet_list.append(top_level_document)

        toctree_fragment = toctree.copy()
        toctree_fragment.append(bullet_list)
    else:
        # No current tab found. Let's render the entire toctree.
        toctree_fragment = toctree

    toctree_html = render_fragment(builder, toctree_fragment)

    # Render the tabs
    tab_list_to_render = docutils.nodes.bullet_list(classes=["lutra-tabs"])
    tab_list_to_render.extend(tabs)

    tabs_html = render_fragment(builder, tab_list_to_render)

    return NavigationInformation(
        toctree_html=toctree_html,
        tabs_html=tabs_html,
    )


def determine_navigation_information(
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
    style: str,
) -> NavigationInformation:
    """Trim `toctree_html` based on what `style` is."""
    style_handlers = {
        "plain": _plain_navigation,
        "subtree-caption": _subtree_caption_navigation,
        "subtree-document": _subtree_document_navigation,
        "tabs-caption": _tabs_caption_navigation,
        "tabs-document": _tabs_document_navigation,
    }

    assert (
        style in style_handlers
    ), f"Got an invalid `navigation_style`: {style!r} (valid values: {list(style_handlers)})"

    toctree = _get_toctree(builder).get_toctree_for(
        docname, builder, collapse=True, titles_only=True
    )
    assert toctree

    handler = style_handlers[style]
    return handler(builder, toctree)


def has_not_enough_items_to_show_toc(
    builder: StandaloneHTMLBuilder, docname: str
) -> bool:
    """Check if the toc has one or fewer items."""
    toctree = _get_toctree(builder).get_toc_for(docname, builder)
    try:
        self_toctree = toctree[0][1]
    except IndexError:
        val = True
    else:
        # There's only the page's own toctree in there.
        val = len(self_toctree) == 1 and self_toctree[0].tagname == "toctree"
    return val


def should_hide_toc(
    context: Dict[str, Any],
    *,
    builder: StandaloneHTMLBuilder,
    docname: str,
) -> bool:
    """Check whether the table of contents should be hidden."""
    file_meta = context.get("meta", None) or {}
    if "hide-toc" in file_meta:
        return True
    elif "toc" not in context:
        return True
    elif not context["toc"]:
        return True

    return has_not_enough_items_to_show_toc(builder, docname)
