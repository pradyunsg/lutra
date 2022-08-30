# Changing fonts

Lutra uses the [system font stack](https://systemfontstack.com/) by default. This helps avoid network requests and parsing of multiple web fonts, which makes the page load quicker on first load and each render.

## Custom fonts

It is possible to override the default font used by Lutra, by providing your own CSS file.

```{code-block} python
:caption: conf.py
:name: custom-fonts-conf-py
html_static_path = ["_static"]
html_css_files = [
    "custom-fonts.css",
]
```

```{code-block} css
:caption: _static/custom-fonts.css
:name: custom-fonts-css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;700&display=swap');

html {
    font-family: 'Inter', sans-serif;
}
code, kbd, samp, pre {
    font-family: 'Source Code Pro', sans-serif;
}
```

### Font weight considerations

Lutra uses multiple font-weights, across the page. The specifics are:

- Regular font: 300 (light), 400 (regular), 500 (medium), 600 (semibold) and 700 (bold).
- Monospaced font: 400 (regular) and 700 (bold).

```{note}
Whether the bold font weight is used depends on the pygments theme being used, as set by {any}`pygments_style` and {any}`pygments_dark_style`.
```
