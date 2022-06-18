# Unsupported customisations

Sphinx is extremely flexible and allows documentation authors to override every part of the theme that they use. Lutra does not support many of these mechanisms -- it usually doesn't go out of its way to disallow them but they're also unsupported.

Unsupported customisations may break with any new release and requests for changes to accommodate for them would be closed as "wontfix". See also {doc}`../stability` for more details.

## Rationale

The maintenance overhead of compatibility for all kinds of customisations that Sphinx provides is an unbounded cost for Sphinx themes. Further, many Sphinx documentation sets are highly coupled with their current theme. This already makes it difficult for Sphinx themes to evolve because, in addition to [Hyrum's Law], there's no clear definition of what the "API" of a Sphinx theme is. This also makes it difficult for the documentation authors to switch themes or, sometimes, even upgrade to a newer version of the same theme without breakages.

## Configuration options that might break the theme

Any configuration options that allow users to tweak what JS or CSS is used with this theme are considered unstable. This includes `html_style`, `html_static_path`, `html_css_files`, `html_js_files` among others.

## Sidebar customisation

Lutra does not support setting custom values for `html_sidebars`. There are no checks for preventing you from using this -- if you break something, you get to keep all the pieces.

## Overriding templates

Lutra does not support overriding templates, except as part of a derivative theme.

## Including "(modified)" in the footer

Lutra has basic checks for some Sphinx configuration options that are known to be problematic. This serves to make it easier to identify such configurations, when responding to issues on the project's communication channels.

These checks result in the website footer getting a "(modified)" marker.

[hyrum's law]: https://www.hyrumslaw.com/

[^1]: Quoted because [even that is not a promise](https://github.com/pradyunsg/lutra/blob/main/LICENSE#L13-L19).
