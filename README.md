<h1 align="center">Lutra</h1>
<p align="center">A clean, modern, customisable, searchable, mobile-friendly theme for documentation.</p>
<a href="https://pradyunsg.me/lutra/">
  <!-- <img align="center" src="https://github.com/pradyunsg/lutra/raw/main/docs/_static/demo.png" alt="Demo image"> -->
  <p>This theme is still under development. Things will change without notice! :)</p>
</a>

## Elevator pitch

<!-- start elevator-pitch -->

- **Statically awesome** — builds upon [Sphinx] and _huge_ ecosystem of extensions.
- **Responsive** — works across all sorts of screen resolutions.
- **Customisable** — change colors, fonts, page layout and more!
- **Clear typography** — borrowing the design language of this decade's websites.
- **Capable navigation** — scales with large documentation sets.
- **Capable search** — help readers find what they want quickly.
- **Modern architecture** — built with modern tooling (`sphinx-theme-builder`, Tailwind, `webpack`, and more).

[sphinx]: https://www.sphinx-doc.org/

<!-- end elevator-pitch -->

## Quickstart

<!-- start quickstart -->

To use the theme in your existing Sphinx documentation:

1. Install Lutra in documentation's build environment.

   ```console
   $ pip install lutra
   ```

1. Update the `html_theme` in `conf.py`. If there's any configuration variables that start with `html_` in this file, comment them out.

   ```py
   html_theme = "lutra"
   ```

1. Your Sphinx documentation's HTML pages will now be generated with this theme! 🎉

[pypi]: https://pypi.org/project/lutra/

<!-- end quickstart -->

For more information, visit [Lutra's documentation][quickstart-docs].

[quickstart-docs]: https://pradyunsg.me/lutra/quick-start/

## Contributing

Lutra is a volunteer maintained open source project, and we welcome contributions of all forms. Please take a look at our [Contributing Guide](https://pradyunsg.me/lutra/contributing/) for more information.

## Acknowledgements

Lutra draws inspiration from some excellent technical documentation websites:

- [mkdocs-material] for MkDocs
- [Gatsby] documentation
- [Tailwind CSS] documentation
- [Just the Docs] for Jekyll

We use [BrowserStack] to test on real devices and browsers. Shoutout to them for supporting OSS projects!

[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[just the docs]: https://just-the-docs.github.io/just-the-docs/
[gatsby]: https://www.gatsbyjs.com/docs/
[tailwind css]: https://tailwindcss.com/docs
[browserstack]: https://browserstack.com/
[sphinx]: https://www.sphinx-doc.org/

## What's with the name?

I plucked this out of the scientific name for [The Eurasian otter](https://en.wikipedia.org/wiki/Eurasian_otter): _Lutra lutra_. You can decide whether I picked the first one or the second one.

## Used By

No one yet!

## License

This project is licensed under the MIT License.
