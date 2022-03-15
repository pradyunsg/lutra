# Ideas

## Landing page ideas

- https://demos.creative-tim.com/argon-design-system-pro/index.html
- https://demos.creative-tim.com/blk-design-system-pro/presentation.html
- https://ehya.designspace.io/
- https://ehya.designspace.io/apps/desktop.html
- https://ehya.designspace.io/landing/architecture.html
- https://ehya.designspace.io/services/software-library.html
- https://hellonext.co/
- https://preview.cruip.com/sienna/
- https://preview.cruip.com/sienna/additional.html
- https://preview.cruip.com/simple/
- https://reactjs.org/
- https://squidfunk.github.io/mkdocs-material/
- https://ui8.net/ui8/products/collab-landing-page-kit
- https://www.gatsbyjs.com/
- https://www.gatsbyjs.com/docs/
- https://www.gitbook.com/
- https://www.thunderbird.net/en-GB/

## Layout ideas

- https://docs.wasmer.io/
- https://vuepress.vuejs.org/
- https://ionicframework.com/docs/
- https://ionicframework.com/docs/v4/cli

## Illustrations

- https://isometric.online/
- https://iradesign.io/illustrations

```py

class UnsupportedConfigurationDetected(LutraError):
    def __init__(self, config_name):
        super().__init__(
            reference=f"custom-{config_name}-without-override",
            message=f"You cannot use `{config_name}` without setting a separate flag, for Lutra!",
            hint_stmt=(
                f"See https://pradyunsg.me/lutra/customisation/unsupported/ for more details."
            ),
        )

def _catch_unstable_modifications(builder: StandaloneHTMLBuilder) -> None:
    if builder.config.html_theme != "lutra":
        return

    breakpoint()
    if builder.config.lutra_with_modifications:
        return

    if builder.config.html_style:
        raise LutraError(
            reference="custom-stylesheet-without-override-flag-set",
            message="You cannot use `html_style` without setting a separate flag!",
            hint_stmt=(
                "See https://pradyunsg.me/lutra/customisation/unsupported/ for more details."
            ),
        )

    if builder.config.html_context:
        raise LutraError(
            reference="custom-context-without-override-flag-set",
            message="You cannot use `html_context` without setting a separate flag!",
            hint_stmt=(
                "See https://pradyunsg.me/lutra/customisation/unsupported/ for more details."
            ),
        )

    if builder.config.html_css_files:
        raise LutraError(
            reference="custom-css-without-override-flag-set",
            message="You cannot use `html_css_files` without setting a separate flag!",
            hint_stmt=(
                "See https://pradyunsg.me/lutra/customisation/unsupported/ for more details."
            ),
        )

    if builder.config.html_js_files:
        raise LutraError(
            reference="custom-js-without-override-flag-set",
            message="You cannot use `html_js_files` without setting a separate flag!",
            hint_stmt=(
                "See https://pradyunsg.me/lutra/customisation/unsupported/ for more details."
            ),
        )

    if builder.config.templates_path:
        raise LutraError(
            reference="custom-templates-without-override-flag-set",
            message="You cannot use `templates_path` without setting a separate flag!",
            hint_stmt=(
                "See https://pradyunsg.me/lutra/customisation/unsupported/ for more details."
            ),
        )


```
