---
layout: page
---

# Showcase

```{todo} Figure out how to do a gallery.

```

...

## First-party Samples

These are example documentation sets built with Lutra. These primarily serve to showcase the navigational and structural features that provide a lot of agency in picking a structure that fits your needs.

```{todo} Figure out how to do a gallery.

```

:::{private-gallery} https://lutra-samples.github.io/plain/

Regular documentation with no Lutra-specific customisations and a single `toctree`. This also doesn't use `lutra-document` or `lutra-toctree`.

This represents what most existing Sphinx documentation will look like, when ported over to Lutra.

:::

:::{private-gallery} https://lutra-samples.github.io/tabs-caption/

A documentation site built with multiple `toctree`s that each have a caption and `tabs-caption` as the navigation style.

This is structurally similar to what can be achieved with Material for MkDocs, with tabs enabled.[^nested-captions]

:::

:::{private-gallery} https://lutra-samples.github.io/tabs-document/

:::

:::{private-gallery} https://lutra-samples.github.io/tabs-document/

:::

:::{private-gallery} https://lutra-samples.github.io/tabs-document/

:::

[^nested-captions]: Lutra currently is unable to get the captions of toctree from documents other than the top document. This means that it is not possible to separate the content in the left sidebar using captions. See <https://github.com/sphinx-doc/sphinx/issues/10697> for the details.
