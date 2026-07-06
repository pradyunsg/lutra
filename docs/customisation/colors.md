# Changing colors

Lutra allows customising colors to fit your brand’s identity.

The most common customisations can be easily configured in the `conf.py` file. Most others will require a few lines of CSS to change values of [CSS variables].

## Color Palette

### Primary

The primary color is used for text links, highlighting active page/section in the sidebars, and several other components. In order to change the primary color, set the following in `conf.py` to a [valid color name](#valid-color-names):

```{code-block} python
:caption: conf.py
:name: primary-color-code-block

html_theme_options = {
    "primary_color": "teal",
}
```

### Secondary

The secondary color is used for visited text links. In order to change the secondary color, set the following in `conf.py` to a [valid color name](#valid-color-names):

```{code-block} python
:caption: conf.py
:name: secondary-color-code-block

html_theme_options = {
    "secondary_color": "lime",
}
```

### Valid color names

Lutra's color palette is built from [Tailwind CSS's default color palette](https://tailwindcss.com/docs/customizing-colors#color-palette-reference). Thus, it supports the same set of colors:

```{todo}
Show preview of the colors here.
```

`slate` `gray` `zinc` `neutral` `stone` `red` `orange` `amber` `yellow` `lime` `green` `emerald` `teal` `cyan` `sky` `blue` `indigo` `violet` `purple` `fuchsia` `pink` `rose`

You can also set it to [`custom`](#custom-palette-colors). If any other color name is used, an {any}`invalid-color` error will be raised which will cause the build to fail.

## Custom colors

Lutra implements colors using [CSS variables] (also known as CSS custom properties). If you want to customize the colors to use specific colors (eg: to fit your project's broader branding), you can add an additional style sheet and tweak the values of the CSS variables on the `body`[^body] tag.

```{code-block} python
:caption: conf.py
:name: custom-colors-conf-py

html_static_path = ["_static"]
html_css_files = [
    "custom-colors.css",
]
```

```{code-block} css
:caption: _static/custom-colors.css
:name: custom-colors-css

/* Common across light and dark mode */
body {
  --color_text-link: red;
}
/* For only light mode */
:not(.dark) body {
  --color_text-link--hover: orange;
}
/* For only dark mode */
.dark body {
  --color_text-link--hover: salmon;
}
```

### Custom palette colors

It is possible to provide your own color values for the primary and secondary colors by setting {any}`primary_color` and {any}`secondary_color` to `custom` and providing those stylesheets in an additional style sheet.

```{code-block} python
:caption: conf.py
:name: custom-palette-colors-conf-py

html_static_path = ["_static"]
html_theme_options = {
    "primary_color": "custom",
}
```

```{code-block} css
:caption: _static/custom-colors.css
:name: custom-palette-colors-css

/* These colors are horrendous to look at, but demonstrate functionality. */
body {
  --color-custom-solid: rgb(255, 0, 0);
  --color-custom-solid_dark: lightred;
  --color-custom-highlight: orange;
  --color-custom-target: gold;
  --color-custom-target_dark: gold;
}
```

```{note}
It is possible to override values for the color names from the default color palette. Don't do that.
```

## Automatic light and dark mode

Lutra supports light and dark mode, each of which use a separate set of colors for various UI elements.

### How it works

Lutra uses Javascript to check whether the user's browser prefers dark mode (checking for `prefers-color-scheme: dark`) and uses dark mode if it is marked as preferred. Otherwise, it uses light mode. This means that light mode is also the only mode available to users if they have Javascript disabled (only 0.2% users do that[^js]).

Lutra will also automatically switch between light and dark appearance, when the user's browser indicates that a preference change has happened (which usually happens when the user's operating system theme changes during day and night times).

### Disable light/dark mode

Disabling light mode or dark mode is not supported. It is, instead, recommended to use the various mechanisms provided by Lutra to [adapt your documentation content for light and dark mode].

```{admonition} Seeking feedback
:class: feedback

If you still want this, we want to [hear from you](https://github.com/pradyunsg/lutra/discussions/new?category=questions) about what your usecase is.
```

### Change colors in only one mode

Lutra is built to use CSS variables for nearly all colors, to allow for changing them between light mode and dark mode. This also allows users to define their own CSS variables to override colors in specific modes.

See the [custom colors](#custom-colors) section above for the specific configuration needed to do this.

[css variables]: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
[prefers-color-scheme]: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme

[^body]: Why the `body` tag? Lutra's own CSS variable definitions are on the `html` tag. By setting custom values on the `body` tag, it ensures that the custom values take precedence over Lutra's CSS variable definitions.

[^js]: "0.2% of pageviews from worldwide traffic across all devices in the fourth quarter 2016 had javascript disabled." according to <https://deliberatedigital.com/blockmetry/javascript-disabled>
