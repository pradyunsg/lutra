"""Directives that make doing achieving certain design styles easier."""

from typing import List

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.directives import SphinxDirective
from sphinx.environment.adapters.toctree import TocTree
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util import docname_join
from sphinx.util.nodes import clean_astext

from ._errors import LutraError


class LutraToctreeDirective(TocTree):
    """Custom toctree that has a description and allows for two-column layout.

    This is inspired by the design of the Gatsby documentation, which groups
    the documentation into various sections and sub-sections.
    """

    option_spec = {
        "name": directives.unchanged,
        "caption": directives.unchanged_required,
        "description": directives.unchanged_required,
        "maxdepth": int,
        "glob": directives.flag,
        "reversed": directives.flag,
    }

    def run(self) -> List[nodes.Node]:
        """Actual core implementation of this directive."""
        # Load the values that get special handling.
        caption = self.options.get("caption", "[caption]")
        description = self.options.get("description", "[description]")

        # Create the toctree node.
        toctree = addnodes.toctree()
        toctree["parent"] = self.env.docname

        toctree["entries"] = []
        toctree["includefiles"] = []
        toctree["glob"] = "glob" in self.options
        toctree["caption"] = caption

        # Things we don't allow configurability for, since they don't fit the
        # navigation design that this is designed for.
        toctree["maxdepth"] = -1
        toctree["numbered"] = 0
        toctree["hidden"] = False
        toctree["includehidden"] = True
        toctree["titlesonly"] = True

        # Compose the information available as follow:
        #
        # div.lutra-toctree-wrapper
        #   p.lutra-toctree-caption
        #     [caption]
        #   p.lutra-toctree-description
        #     [description]
        #   div.lutra-toctree-tree
        #       .toctree-wrapper
        #           [toctree]
        lutra_toctree_wrapper = nodes.container(classes=["lutra-toctree-wrapper"])
        lutra_toctree_context = nodes.container(
            classes=["lutra-toctree-context"], toctree=True
        )
        lutra_toctree_tree = nodes.container(classes=["lutra-toctree-tree"])
        lutra_toctree_caption = nodes.caption(classes=["lutra-toctree-caption"])
        lutra_toctree_description = nodes.container(
            classes=["lutra-toctree-description"]
        )
        toctree_wrapper = nodes.compound(classes=["toctree-wrapper"])

        lutra_toctree_caption += nodes.Text(caption)
        lutra_toctree_description += nodes.Text(description)

        lutra_toctree_wrapper.append(lutra_toctree_context)
        lutra_toctree_context.append(lutra_toctree_caption)
        lutra_toctree_context.append(lutra_toctree_description)

        lutra_toctree_wrapper.append(lutra_toctree_tree)
        lutra_toctree_tree.append(toctree_wrapper)
        toctree_wrapper.append(toctree)

        # Make it possible for Sphinx to present where the "main" nodes were
        # defined in source.
        self.set_source_info(toctree)
        self.set_source_info(lutra_toctree_wrapper)

        # Make the wrapper be the target for the name.
        self.add_name(lutra_toctree_wrapper)

        # Defer to Sphinx, for processing the toctree.
        value = self.parse_content(toctree)
        if value:
            raise LutraError(
                reference="unexpected-return-from-toctree-parse-content",
                message=(
                    "The Sphinx toctree directive's parsing returned a value, which is "
                    "not expected."
                ),
                hint_stmt=(
                    "This reflects that Sphinx has changed its behaviour. Please "
                    "file an issue against the Lutra project if this happens. "
                    "(don't forget to check for duplicates!)"
                ),
            )

        return [lutra_toctree_wrapper]


class LutraDocumentNode(nodes.Element):
    """A node that is used to represent the "lutra-document" result."""


class LutraDocumentDirective(SphinxDirective):
    """A card that points to a document, with a description.

    This is inspired by the design of docs.python.org's landing page and Gatsby's
    documentation, which both present documents in a two column layout with a
    description underneath.
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "show-child-pages": directives.flag,
    }

    def run(self) -> List[nodes.Node]:
        """Actual core implementation of this directive."""
        node = LutraDocumentNode(
            "",
            from_doc=self.env.docname,
            to_doc=self.arguments[0],
            show_child_pages="show-child-pages" in self.options,
        )
        self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class LutraDocumentPostTransform(SphinxPostTransform):
    """A post-transform that resolves documents in "lutra-document".

    This also wraps consecutive nodes of that directive in a container.
    """

    default_priority = 750

    def apply(self, **kwargs: str) -> None:
        """Apply this transformation."""
        self.stack = []  # type: List[LutraDocumentNode]

        for node in self.document.traverse(LutraDocumentNode):
            if not self.stack:
                self.stack.append(node)
                continue

            last_node = self.stack[-1]

            node_is_immediately_after_last_node = (
                node.parent == last_node.parent
                and node.parent.index(last_node) + 1 == node.parent.index(node)
            )
            if node_is_immediately_after_last_node:
                self.stack.append(node)
                continue

            # We have a new node, that's not a sibling of the last few,
            # so we need to finalise the previous ones.
            self._finalize_stack()

            assert not self.stack
            self.stack.append(node)

        if self.stack:
            self._finalize_stack()

    def _finalize_stack(self) -> None:
        parent = self.stack[0].parent
        assert parent

        # Wrap the stack in a container.
        container = nodes.container(classes=["lutra-document-container"])
        container.parent = parent
        for node in self.stack:
            container.append(self._with_resolved_references(node))

        # Replace all nodes within the parent, with the container.
        start_at = parent.index(self.stack[0])  # type: ignore
        end_at = parent.index(self.stack[-1])  # type: ignore
        parent.children = (
            list(parent.children[:start_at])
            + [container]
            + list(parent.children[end_at + 1 :])
        )

        # Reset the stack, since everything has been replaced.
        self.stack[:] = []

    def _with_resolved_references(self, node: LutraDocumentNode) -> nodes.container:
        """Generate the replacement for the node."""
        from_doc = node["from_doc"]
        to_doc = node["to_doc"]
        show_child_pages = node["show_child_pages"]
        document_ref = docname_join(from_doc, to_doc)

        if document_ref not in self.env.all_docs:
            raise LutraError(
                reference="missing-document",
                message=(
                    "Could not find document referenced by the lutra-document "
                    f"directive: {document_ref}\n"
                    f"File: {node.source}\n"
                    f"Line: {node.line}"
                ),
                hint_stmt=(
                    "This might be because the document was removed or "
                    "renamed. Check for typos."
                ),
            )

        refuri = self.app.builder.get_relative_uri(from_doc, document_ref)
        reference = nodes.reference("", "", internal=True, refuri=refuri)

        title_container = nodes.container(classes=["lutra-document-title-container"])
        title = clean_astext(self.env.titles[document_ref])
        title_container += nodes.inline(title, title, classes=["lutra-document-title"])

        replacement = addnodes.compact_paragraph()
        reference += title_container
        if not show_child_pages:
            reference["classes"] = ["lutra-document"]
            reference.extend(node.children)

            replacement += reference
        else:
            reference["classes"] = ["lutra-document-title-link"]
            ref_container = addnodes.compact_paragraph()
            ref_container += reference

            context = nodes.container(classes=["lutra-document-context"])
            context += ref_container
            context += node.children

            container = nodes.container(classes=["lutra-document-with-child-pages"])
            container += context

            children = self._get_child_lists(document_ref)
            container.append(children)

            replacement += container

        return replacement

    def _get_child_lists(self, document_ref: str) -> nodes.Node:
        doctree = self.env.get_doctree(document_ref)

        notes = []
        for toctreenode in doctree.findall(addnodes.toctree):
            result = TocTree(self.env).resolve(
                docname=document_ref,
                builder=self.app.builder,
                toctree=toctreenode,
                prune=True,
                maxdepth=1,
                titles_only=True,
                collapse=False,
                includehidden=True,
            )
            # Fix the references in the toctree, since it's all relative to
            # the document it was generated for.
            for reference in result.findall(nodes.reference):
                if reference["refuri"].startswith("#"):
                    continue
                reference["refuri"] = docname_join(document_ref, reference["refuri"])

            if result is not None:
                notes.append(result)

        retval = nodes.container(classes=["lutra-document-child-pages"])
        retval.extend(notes)
        return retval
